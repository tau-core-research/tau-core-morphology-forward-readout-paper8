#!/usr/bin/env python3
"""Freeze the residual-blind NGC4062 H I--Halpha endpoint before pixel access."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import tarfile
from pathlib import Path

from astropy.io import fits
from astropy.wcs import WCS


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
SOURCE = ROOT / "data/external/literature/ngc4062_halogas_confirmatory_v01"
HALPHA = DATA / "ghasp_full_federation_side_points_v01.csv"

EXPECTED_SHA256 = {
    "NGC4062-HR_mom0m.fits": "e0d6109305839768c129e6a93cafa889d323ee502173b1a5fb78ea93f6124605",
    "NGC4062-HR_mom1m.fits": "35fb55608e6dc25767386e77b5a53e0e2cd8eb65957d8607bf7656709f15754f",
    "NGC4062-LR_mom0m.fits": "4071706a881f551c41f8c91c5457190800d44f67e37b799e61d5a4e33f1e6502",
    "NGC4062-LR_mom1m.fits": "c9eb53e5324aa8b09de5281178aaa3d68315c017d3c795f497343a4cfc38d0f1",
    "ghasp_vi_tablec1.dat": "551a334477b6ba1b3aca6c5c91b9a74d1a8c7f01db6db400f622211687821282",
    "ghasp_vi_tablec2.dat": "6cefb0007e7d5fe9e74a0d9ee36591e5c23f690fbefa53194a03a5aa49706952",
    "ghasp_vi_tablec3.dat": "1999ab72d8eb6221c68aa720157a8a9b5489015e3eb2bbb5785f2912668e8ce9",
    "marasco2019_arxiv_1909.04048_source.tar.gz": "934e5027115408b11284bf1dc68d1d3916321cb9734f347fa72645dea9455398",
}

COMMON_RADII_ARCSEC = [42.0, 84.0]
ANNULUS_WIDTH_ARCSEC = 42.0
MIN_ABS_COS_THETA = 0.8
BOOTSTRAP_DRAWS = 2000
BOOTSTRAP_SEED = 4062001


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bracket(radii: list[float], target: float) -> tuple[float, float, float, float]:
    lower = max(value for value in radii if value <= target)
    upper = min(value for value in radii if value >= target)
    if lower == upper:
        return lower, upper, 1.0, 0.0
    upper_weight = (target - lower) / (upper - lower)
    return lower, upper, 1.0 - upper_weight, upper_weight


def main() -> None:
    for name, expected in EXPECTED_SHA256.items():
        path = SOURCE / name
        if sha256(path) != expected:
            raise RuntimeError(f"Source hash mismatch: {name}")

    c1 = next(line for line in (SOURCE / "ghasp_vi_tablec1.dat").read_text().splitlines() if line.startswith("UGC 7045"))
    c2 = next(line for line in (SOURCE / "ghasp_vi_tablec2.dat").read_text().splitlines() if line.startswith("UGC 7045"))
    c3 = next(line for line in (SOURCE / "ghasp_vi_tablec3.dat").read_text().splitlines() if line.startswith("UGC 7045"))
    ghasp = {
        "center_ra_deg": (12 + 4 / 60 + 3.8 / 3600) * 15,
        "center_dec_deg": 31 + 53 / 60 + 42 / 3600,
        "seeing_arcsec": float(c1[67:70]),
        "systemic_velocity_km_s": int(c2[18:22]),
        "systemic_velocity_error_km_s": int(c2[23:25]),
        "kinematic_inclination_deg": int(c2[32:34]),
        "kinematic_inclination_error_deg": int(c2[35:37]),
        "kinematic_pa_deg": int(c2[70:73]),
        "kinematic_pa_side_flag": c2[73:74],
        "kinematic_pa_error_deg": int(c2[75:77]),
        "d25_radius_arcsec": int(c3[61:64]),
    }
    if ghasp["kinematic_pa_side_flag"].strip():
        raise RuntimeError("NGC4062 GHASP PA was expected to be the default receding ray")

    archive = SOURCE / "marasco2019_arxiv_1909.04048_source.tar.gz"
    with tarfile.open(archive, "r:gz") as bundle:
        member = bundle.extractfile("extrahalogas.tex")
        if member is None:
            raise RuntimeError("Marasco source lacks extrahalogas.tex")
        marasco = io.TextIOWrapper(member, encoding="utf-8").read()
    source_row = "7045 & NGC\\,4062        &\tSAc &\t16.9 &\t68 &\t67.1\t&100.1"
    if source_row not in marasco:
        raise RuntimeError("NGC4062 3DBarolo geometry row changed")
    if "NGC\\,0949, NGC\\,1003, NGC\\,2541, NGC\\,4258, NGC\\,4414" not in marasco:
        raise RuntimeError("Marasco warp-list statement changed")

    headers = {}
    for resolution in ("HR", "LR"):
        path = SOURCE / f"NGC4062-{resolution}_mom0m.fits"
        header = fits.getheader(path, 0)
        wcs = WCS(header, naxis=2)
        x, y = wcs.world_to_pixel_values(ghasp["center_ra_deg"], ghasp["center_dec_deg"])
        headers[resolution] = {
            "shape": [int(header["NAXIS2"]), int(header["NAXIS1"])],
            "pixel_scale_arcsec": abs(float(header["CDELT1"])) * 3600,
            "beam_major_arcsec": float(header["BMAJ"]) * 3600,
            "beam_minor_arcsec": float(header["BMIN"]) * 3600,
            "beam_pa_deg": float(header["BPA"]),
            "ghasp_center_pixel_zero_based": [float(x), float(y)],
            "pixel_values_opened": False,
        }

    halpha_rows = [
        row for row in csv.DictReader(HALPHA.open(newline="", encoding="utf-8"))
        if "NGC4062" in row["aliases"].split(";")
    ]
    radii = {
        side: sorted(float(row["radius_arcsec"]) for row in halpha_rows if row["side"] == side)
        for side in ("a", "r")
    }
    common_max = min(max(radii["a"]), max(radii["r"]))
    if common_max < COMMON_RADII_ARCSEC[-1] + ANNULUS_WIDTH_ARCSEC / 2:
        raise RuntimeError("Two complete LR-beam rings no longer fit in Halpha support")

    freeze_rows = []
    for radius in COMMON_RADII_ARCSEC:
        a0, a1, aw0, aw1 = bracket(radii["a"], radius)
        r0, r1, rw0, rw1 = bracket(radii["r"], radius)
        freeze_rows.append({
            "radius_arcsec": radius,
            "annulus_inner_arcsec": radius - ANNULUS_WIDTH_ARCSEC / 2,
            "annulus_outer_arcsec": radius + ANNULUS_WIDTH_ARCSEC / 2,
            "halpha_approaching_lower_radius_arcsec": a0,
            "halpha_approaching_upper_radius_arcsec": a1,
            "halpha_approaching_lower_weight": aw0,
            "halpha_approaching_upper_weight": aw1,
            "halpha_receding_lower_radius_arcsec": r0,
            "halpha_receding_upper_radius_arcsec": r1,
            "halpha_receding_lower_weight": rw0,
            "halpha_receding_upper_weight": rw1,
            "endpoint_access": False,
        })
    csv_path = DATA / "ngc4062_halogas_confirmatory_freeze_v01.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(freeze_rows[0]))
        writer.writeheader()
        writer.writerows(freeze_rows)

    result = {
        "schema": "ngc4062_halogas_confirmatory_freeze_v01",
        "status": "NGC4062_SOURCE_GEOMETRY_COMPLETE_TWO_RING_ENDPOINT_FROZEN_PIXELS_UNOPENED",
        "galaxy": "NGC4062",
        "source_geometry": {
            "ghasp": ghasp,
            "halogas_3dbarolo": {"median_inclination_deg": 67.1, "median_pa_deg": 100.1},
            "primary": {
                "center_ra_deg": float(fits.getheader(SOURCE / "NGC4062-HR_mom0m.fits", 0)["CRVAL1"]),
                "center_dec_deg": float(fits.getheader(SOURCE / "NGC4062-HR_mom0m.fits", 0)["CRVAL2"]),
                "inclination_deg": 67.1,
                "receding_pa_deg": 100.1,
                "systemic_velocity_km_s": 769.0,
            },
            "variants": {
                "center": "GHASP kinematic-study center",
                "inclination_deg": [62.1, 72.1],
                "receding_pa_deg": [98.1, 102.1],
                "systemic_velocity_km_s": [758.0, 769.0],
            },
        },
        "source_interpretation": {
            "halogas_geometry_role": "median 3DBarolo thin-disc geometry; not a published radial i(R),PA(R) table",
            "constant_geometry_justification": "NGC4062 is not among the six systems Marasco et al. flag as having a substantial (~10 deg or more) H I warp",
            "limitation": "absence from that list is not proof of zero warp; constant geometry and systemic velocity are mandatory nuisance variants",
        },
        "headers": headers,
        "common_radii_arcsec": COMMON_RADII_ARCSEC,
        "annulus_width_arcsec": ANNULUS_WIDTH_ARCSEC,
        "radial_bins_overlap": False,
        "halpha_common_max_radius_arcsec": common_max,
        "major_axis_min_abs_cos_theta": MIN_ABS_COS_THETA,
        "bootstrap_draws": BOOTSTRAP_DRAWS,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "primary_map": "HR",
        "mandatory_replication_map": "LR",
        "pixel_mask_rule": "finite moment0 and moment1 with moment0>0; no data-dependent clipping",
        "pixel_estimator": "moment0*abs(cos_theta)-weighted median of (v_los-v_sys)/cos_theta in each side/ring",
        "channel_statistic": "Delta_O=O_Halpha-O_HI on two non-overlapping LR-beam rings",
        "replication_gates": {
            "zero_odd_contrast_rejected_in_hr": "p<0.05",
            "zero_odd_contrast_rejected_in_lr": "p<0.05",
            "gls_mean_sign_agreement": True,
            "hr_lr_gls_mean_difference": "absolute difference <=2 combined standard errors",
            "same_sign_radius_fraction": 1.0,
            "all_geometry_and_systemic_variants_preserve_gls_sign": True,
        },
        "construction_blind_to": [
            "HALOGAS moment-map pixel values", "H I-Halpha contrast", "SPARC vobs and residuals",
            "baseline scores", "required Tau amplitudes",
        ],
        "pixel_values_opened_during_freeze": False,
        "endpoint_access": False,
        "physical_a_row_constructed": False,
        "claim_boundary": "A passed score would be a two-tracer morphology/readout diagnostic, not a Tau detection, q_R derivation, parent-morphology measurement, Nature-occupation result, or dark-matter replacement.",
        "source_sha256": {name: sha256(SOURCE / name) for name in EXPECTED_SHA256},
        "halpha_points_sha256": sha256(HALPHA),
    }
    json_path = DATA / "ngc4062_halogas_confirmatory_freeze_v01.json"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (REPORTS / "ngc4062_halogas_confirmatory_freeze_v01.md").write_text(
        f"""# NGC4062 HALOGAS confirmatory freeze v0.1

**Status:** `{result['status']}`

GHASP supplies `i=68 +/- 2 deg`, a receding `PA=99 +/- 2 deg`, and
`v_sys=758 +/- 1 km/s`. The independent HALOGAS 3DBarolo analysis gives
median `i=67.1 deg`, `PA=100.1 deg`; NGC4062 is not in its list of six
substantially warped H I discs. That supports, but does not prove, the constant
geometry approximation.

Two non-overlapping, LR-beam-sized rings are frozen at `42` and `84 arcsec`.
HR is primary and LR mandatory replication. The primary H I geometry uses the
3DBarolo orientation and the HALOGAS catalogue systemic velocity; GHASP center,
`i +/- 5 deg`, `PA +/- 2 deg`, and both published systemic velocities are
mandatory nuisance variants.

Only FITS headers were read. No moment-map pixel, cross-tracer difference,
SPARC residual, baseline score, or required Tau amplitude was opened.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
