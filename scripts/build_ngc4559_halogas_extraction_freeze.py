#!/usr/bin/env python3
"""Freeze NGC4559 HALOGAS map extraction before any FITS pixel access."""

from __future__ import annotations

import csv
import hashlib
import json
import urllib.request
from pathlib import Path

from astropy.io import fits
from astropy.wcs import WCS


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
OUT = ROOT / "data" / "external" / "literature" / "ngc4559_halogas_route"
REPORTS = ROOT / "reports"
SOURCE_JSON = DATA / "ngc4559_halogas_moment_sources_v01.json"
HALPHA_POINTS = DATA / "ghasp_full_federation_side_points_v01.csv"
BARBIERI_URL = "https://www.aanda.org/articles/aa/pdf/2005/33/aa2395-04.pdf"
GHASP_MODEL_URL = "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/390/466/tableb2.dat"

# Source-frozen from Barbieri et al. 2005, Table 1 and Section 3.
PRIMARY_CENTER = {"ra_deg": 188.9916666667, "dec_deg": 27.9588888889, "role": "barbieri_kinematic_center"}
CENTER_VARIANTS = [
    {"ra_deg": 188.9900000000, "dec_deg": 27.9587222222, "role": "barbieri_optical_center"},
    {"ra_deg": 188.9887500000, "dec_deg": 27.9605555556, "role": "ghasp_kinematic_study_center"},
    {"ra_deg": 188.9900052840, "dec_deg": 27.9600007817, "role": "halogas_wcs_reference_center"},
]
HI_GEOMETRY = {
    "inclination_deg": 67.2,
    "inclination_error_deg": 0.6,
    "receding_pa_deg": 323.0,
    "pa_error_deg": 1.4,
    "systemic_velocity_km_s": 810.0,
    "systemic_velocity_error_km_s": 4.0,
}
COMMON_RADII_ARCSEC = [42.0, 84.0, 126.0, 168.0]
ANNULUS_WIDTH_ARCSEC = 42.0
MAJOR_AXIS_MIN_ABS_COS_THETA = 0.8
BOOTSTRAP_DRAWS = 2000
BOOTSTRAP_SEED = 4559001


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "tau-core-source-audit/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bracket(radii: list[float], target: float) -> tuple[float, float, float, float]:
    lower = max(radius for radius in radii if radius <= target)
    upper = min(radius for radius in radii if radius >= target)
    if lower == upper:
        return lower, upper, 1.0, 0.0
    upper_weight = (target - lower) / (upper - lower)
    return lower, upper, 1.0 - upper_weight, upper_weight


def main() -> None:
    source = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    if source["pixel_values_opened"] or source["source_only_rank"] != 2:
        raise RuntimeError("NGC4559 source gate is not pixel-blind rank 2")
    barbieri = download(BARBIERI_URL)
    ghasp_model = download(GHASP_MODEL_URL)
    barbieri_path = OUT / "barbieri_2005_ngc4559.pdf"
    ghasp_model_path = OUT / "ghasp_vii_tableb2.dat"
    barbieri_path.write_bytes(barbieri)
    ghasp_model_path.write_bytes(ghasp_model)
    ghasp_line = next(
        line for line in ghasp_model.decode("utf-8").splitlines() if line.startswith("UGC 7766")
    )
    ghasp_geometry = {
        "systemic_velocity_km_s": int(ghasp_line[18:22]),
        "systemic_velocity_error_km_s": int(ghasp_line[23:26]),
        "kinematic_inclination_deg": int(ghasp_line[33:35]),
        "kinematic_inclination_error_deg": int(ghasp_line[36:38]),
        "kinematic_pa_deg": int(ghasp_line[72:75]),
        "kinematic_pa_side": ghasp_line[75:76],
        "kinematic_pa_error_deg": int(ghasp_line[77:79]),
    }
    if ghasp_geometry["kinematic_pa_side"] != "a":
        raise RuntimeError("Expected GHASP PA to label the approaching side")
    ghasp_receding_pa = (ghasp_geometry["kinematic_pa_deg"] + 180) % 360

    manifest = source["manifest"]
    fits_paths = {
        Path(row["filename"]).stem: ROOT / row["local_path"] for row in manifest
    }
    header_audit = {}
    for key, path in fits_paths.items():
        with fits.open(path, memmap=True, lazy_load_hdus=True) as hdus:
            header = hdus[0].header
            wcs = WCS(header, naxis=2)
            x, y = wcs.world_to_pixel_values(PRIMARY_CENTER["ra_deg"], PRIMARY_CENTER["dec_deg"])
            header_audit[key] = {
                "source_sha256": sha256(path),
                "primary_center_pixel_zero_based": [float(x), float(y)],
                "pixel_scale_arcsec": abs(float(header["CDELT1"])) * 3600,
                "beam_major_arcsec": float(header["BMAJ"]) * 3600,
                "beam_minor_arcsec": float(header["BMIN"]) * 3600,
                "pixel_values_opened": False,
            }

    halpha = [
        row
        for row in csv.DictReader(HALPHA_POINTS.open(newline="", encoding="utf-8"))
        if row["sparc_match"] == "NGC4559"
    ]
    radii_by_side = {
        side: sorted(float(row["radius_arcsec"]) for row in halpha if row["side"] == side)
        for side in ("a", "r")
    }
    freeze_rows = []
    for radius in COMMON_RADII_ARCSEC:
        a0, a1, aw0, aw1 = bracket(radii_by_side["a"], radius)
        r0, r1, rw0, rw1 = bracket(radii_by_side["r"], radius)
        freeze_rows.append(
            {
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
            }
        )
    freeze_csv = DATA / "ngc4559_halogas_extraction_freeze_v01.csv"
    with freeze_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(freeze_rows[0]))
        writer.writeheader()
        writer.writerows(freeze_rows)

    result = {
        "schema": "ngc4559_halogas_extraction_freeze_v01",
        "status": "NGC4559_HALOGAS_PIXEL_EXTRACTION_AND_REPLICATION_RULE_FROZEN_PIXELS_UNOPENED",
        "galaxy": "NGC4559",
        "source_only_rank": 2,
        "source_geometry": {
            "primary_center": PRIMARY_CENTER,
            "center_variants": CENTER_VARIANTS,
            "hi": HI_GEOMETRY,
            "ghasp": ghasp_geometry,
            "ghasp_receding_pa_deg": ghasp_receding_pa,
            "hi_ghasp_receding_pa_difference_deg": abs(ghasp_receding_pa - HI_GEOMETRY["receding_pa_deg"]),
        },
        "source_provenance": {
            "barbieri_url": BARBIERI_URL,
            "barbieri_sha256": hashlib.sha256(barbieri).hexdigest(),
            "ghasp_model_url": GHASP_MODEL_URL,
            "ghasp_model_sha256": hashlib.sha256(ghasp_model).hexdigest(),
            "halpha_points_sha256": sha256(HALPHA_POINTS),
            "moment_headers": header_audit,
        },
        "common_radii_arcsec": COMMON_RADII_ARCSEC,
        "annulus_width_arcsec": ANNULUS_WIDTH_ARCSEC,
        "radial_bins_overlap": False,
        "major_axis_min_abs_cos_theta": MAJOR_AXIS_MIN_ABS_COS_THETA,
        "sky_geometry_rule": "east/north offsets rotated to PA east of north; disk radius sqrt(x_major^2+(x_minor/cos(i))^2)",
        "side_rule": "+x_major along PA=323 deg is receding; -x_major is approaching",
        "pixel_mask_rule": "finite moment0 and moment1 with moment0>0; no data-dependent clipping",
        "pixel_estimator": "moment0*abs(cos_theta)-weighted median of (v_los-v_sys)/cos_theta in each side/ring",
        "bootstrap_rule": "resample beam-sized spatial blocks independently within each side/ring",
        "bootstrap_draws": BOOTSTRAP_DRAWS,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "primary_map": "HR",
        "replication_map": "LR",
        "channel_statistic": "unchanged NGC3726 Delta_O=O_Halpha-O_HI on common angular support",
        "replication_gates": {
            "zero_odd_contrast_rejected_in_hr": "p<0.05",
            "zero_odd_contrast_rejected_in_lr": "p<0.05",
            "gls_mean_sign_agreement": True,
            "hr_lr_gls_mean_difference": "absolute difference <=2 combined standard errors",
            "minimum_same_sign_radius_fraction": 0.75,
        },
        "construction_blind_to": [
            "HALOGAS moment-map pixel values",
            "SPARC vobs and residuals",
            "H I-Halpha contrast",
            "baseline model scores",
            "required Tau amplitudes",
        ],
        "pixel_values_opened_during_freeze": False,
        "endpoint_access": False,
        "physical_a_row_constructed": False,
        "claim_boundary": "prospective map-extraction freeze only; later contrast remains a tracer diagnostic unless conventional systematics and common-parent response are controlled",
    }
    (DATA / "ngc4559_halogas_extraction_freeze_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    (REPORTS / "ngc4559_halogas_extraction_freeze_v01.md").write_text(
        f"""# NGC4559 HALOGAS Extraction Freeze v0.1

**Status:** `{result['status']}`

The geometry is source-frozen from Barbieri et al. (2005): kinematic center
`12:35:58.0 +27:57:32`, `i=67.2 +/- 0.6 deg`, receding
`PA=323 +/- 1.4 deg`, and `v_sys=810 +/- 4 km/s`. GHASP gives
`i={ghasp_geometry['kinematic_inclination_deg']} +/- {ghasp_geometry['kinematic_inclination_error_deg']} deg`
and approaching `PA={ghasp_geometry['kinematic_pa_deg']} +/- {ghasp_geometry['kinematic_pa_error_deg']} deg`,
equivalent to the same receding axis.

Four non-overlapping common rings are frozen at `42, 84, 126, 168 arcsec`,
each `42 arcsec` wide. This width is set by the LR beam, not by velocity-map
features. Only pixels with `|cos(theta)|>=0.8`, finite masked moments, and
positive moment-0 support enter. The side estimator is an
`I_HI*|cos(theta)|`-weighted median of `(v_los-v_sys)/cos(theta)`.

HR is primary and LR is mandatory replication. Beam-sized block bootstrap
uses `{BOOTSTRAP_DRAWS}` draws with seed `{BOOTSTRAP_SEED}`. A channel-positive
replication would require zero odd contrast to be rejected independently in
both resolutions, matching GLS signs, compatible GLS means, and at least 75%
radius-wise sign agreement.

No HALOGAS pixel, SPARC velocity/residual, cross-tracer contrast, baseline
score, or required Tau amplitude was opened while freezing this protocol.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
