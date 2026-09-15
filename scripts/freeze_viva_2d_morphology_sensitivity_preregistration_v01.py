#!/usr/bin/env python3
"""Freeze a velocity-blind VIVA 2D morphology-sensitivity control cohort."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
ATLAS_URL = "https://ui.adsabs.harvard.edu/abs/2009AJ....138.1741C/abstract"
DATA_ROOT = "https://www.astro.yale.edu/viva/cubes"

# Values are from Chung et al. (2009), Table 1.  Labels below use only the
# published H I/stellar morphology and interaction descriptions, not velocity
# residuals or a Tau/standard-gravity endpoint.
COHORT = [
    {
        "galaxy": "NGC4298", "role": "disturbed", "ra_deg": 185.38625,
        "dec_deg": 14.606944, "d25_arcmin": 3.24, "pa_deg": 140.0,
        "inclination_deg": 57.0, "cube": "ngc4298.cube.fits.gz",
        "source_morphology_reason": "asymmetric H I extent and stellar disk; close physical pair with NGC4302; interaction may explain lopsidedness",
    },
    {
        "galaxy": "NGC4424", "role": "disturbed", "ra_deg": 186.797917,
        "dec_deg": 9.420833, "d25_arcmin": 3.63, "pa_deg": 95.0,
        "inclination_deg": 62.0, "cube": "ngc4424.cube.fits.gz",
        "source_morphology_reason": "strongly disturbed stellar disk with shells and banana-shaped isophotes; gravitational interaction or collision indicated",
    },
    {
        "galaxy": "NGC4654", "role": "disturbed", "ra_deg": 190.985833,
        "dec_deg": 13.125833, "d25_arcmin": 4.90, "pa_deg": 128.0,
        "inclination_deg": 56.0, "cube": "ngc4654.cube.fits.gz",
        "source_morphology_reason": "extended one-sided H I tail, compressed opposite edge, and disturbed stellar disk; ram pressure plus gravitational interaction candidate",
    },
    {
        "galaxy": "NGC4450", "role": "quiet", "ra_deg": 187.1225,
        "dec_deg": 17.084722, "d25_arcmin": 5.25, "pa_deg": 175.0,
        "inclination_deg": 43.0, "cube": "ngc4450.cube.fits.gz",
        "source_morphology_reason": "weak tightly wound optical structure with no obvious tidal or ongoing ICM interaction reported",
    },
    {
        "galaxy": "NGC4579", "role": "quiet", "ra_deg": 189.434167,
        "dec_deg": 11.819722, "d25_arcmin": 5.89, "pa_deg": 95.0,
        "inclination_deg": 38.0, "cube": "ngc4579.cube.fits.gz",
        "source_morphology_reason": "H I distribution reported symmetric and regular with no indication of ongoing interaction; central bar retained as explicit caveat",
    },
    {
        "galaxy": "NGC4689", "role": "quiet", "ra_deg": 191.940833,
        "dec_deg": 13.764167, "d25_arcmin": 4.27, "pa_deg": 161.0,
        "inclination_deg": 37.0, "cube": "ngc4689.cube.fits.gz",
        "source_morphology_reason": "H I morphology reported fairly regular and symmetric with no signature of ongoing ram pressure or tidal interaction",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    csv_path = DATA / "viva_2d_morphology_sensitivity_preregistration_v01.csv"
    json_path = DATA / "viva_2d_morphology_sensitivity_preregistration_v01.json"
    report_path = REPORTS / "viva_2d_morphology_sensitivity_preregistration_v01.md"

    if {row["role"] for row in COHORT} != {"disturbed", "quiet"}:
        raise RuntimeError("Both conventional roles are required")
    if sum(row["role"] == "disturbed" for row in COHORT) != 3 or sum(
        row["role"] == "quiet" for row in COHORT
    ) != 3:
        raise RuntimeError("The exact 3+3 frozen cohort changed")
    if any(not 30.0 <= row["inclination_deg"] <= 70.0 for row in COHORT):
        raise RuntimeError("Frozen inclination eligibility failed")

    fields = list(COHORT[0]) + ["cube_url"]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in COHORT:
            writer.writerow({**row, "cube_url": f"{DATA_ROOT}/{row['cube']}"})

    result = {
        "schema": "viva_2d_morphology_sensitivity_preregistration_v01",
        "status": "SOURCE_FROZEN_CONVENTIONAL_SENSITIVITY_CONTROL_READY_FOR_ACQUISITION",
        "survey": "VIVA H I",
        "primary_source": {
            "citation": "Chung et al. 2009, AJ 138, 1741",
            "atlas_url": ATLAS_URL,
            "data_root": DATA_ROOT,
            "local_atlas_pdf": "data/external/literature/ngc4254_ffl_uncertainty_v04/viva_atlas.pdf",
        },
        "cohort": COHORT,
        "cohort_rule": "exact named 3 disturbed plus 3 quiet morphology controls; no substitution after velocity opening",
        "construction": {
            "source_morphology_mode": 1,
            "velocity_target_upper_sideband": 2,
            "sideband_identity": "an in-plane morphology mode m enters line-of-sight velocity at k=m-1 and k=m+1; retain k=m+1",
            "radial_support": "four fixed equal-width annuli over 0.20 <= R/R25 <= 1.00",
            "source_template": "per-annulus normalized H I moment-0 m=1 cosine/sine coefficient and its single global quadrature companion",
            "nuisance": "per-annulus {constant, cos(theta), sin(theta)} plus frozen center/PA/inclination finite-difference tangents when supported",
            "score": "cross-validated held-out-sector SSE reduction of nuisance+matched template relative to nuisance alone",
            "wrong_templates": ["radial_annulus_reversal", "nonconstant_annulus_phase_permutation", "cross_galaxy_same_role_template"],
            "primary_contrast": "mean matched-minus-wrong specificity in disturbed minus quiet controls",
            "inference": "exact one-sided 3-of-6 role-label permutation; smallest attainable p is 0.05",
            "success_gate": "positive primary contrast, exact p <= 0.05, and positive disturbed median specificity",
        },
        "cube_reduction_freeze": {
            "noise": "per-channel 1.4826*MAD about the channel median",
            "emission_seed": "positive emission above 3 sigma in at least two adjacent channels",
            "mask_growth": "one spectral channel and one image pixel after adjacency seed",
            "pixel_gate": "integrated positive-emission S/N >= 5",
            "sampling": "one sample per geometric-mean synthesized-beam diameter on a fixed image grid",
            "azimuth_sectors": 12,
            "minimum_occupied_sectors_per_annulus": 8,
            "minimum_beam_independent_samples_per_annulus": 24,
        },
        "hard_stops": [
            "any missing or changed named cube",
            "inclination outside 30--70 degrees",
            "fewer than eight occupied sectors or 24 beam-independent samples in any annulus",
            "projected matched-template rank below two",
            "geometry tangent consumes the target span",
        ],
        "construction_uses_velocity_or_rotation_residual": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": "source-frozen conventional 2D morphology-sensitivity preregistration; not a Tau endpoint, parent-loss measurement, gravity correction, dark-matter alternative, or physical validation",
    }
    result["cohort_csv"] = str(csv_path.relative_to(ROOT))
    result["cohort_csv_sha256"] = sha256(csv_path)
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(
        "# VIVA 2D morphology-sensitivity preregistration v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "Before opening or downloading any of the six velocity cubes, this packet freezes an exact "
        "three-disturbed/three-quiet VIVA cohort from the morphology and interaction descriptions in "
        "Chung et al. (2009). The source-side m=1 H I morphology is tested only through its k=2 "
        "line-of-sight upper sideband after per-annulus systemic, circular, and radial nuisance removal.\n\n"
        "The primary statistic is matched-template specificity relative to radial-reversal, annular-phase, "
        "and cross-galaxy controls. Exact 3-of-6 label permutation is primary; with only 20 assignments, "
        "p=0.05 is the strongest attainable result. Failure demotes this terminal, not Tau Core. Success "
        "would demonstrate conventional morphology-correlated kinematic sensitivity only.\n\n"
        "The cohort and all reduction, rank, missing-data, and inference rules are machine-frozen in "
        f"`{json_path.relative_to(ROOT)}` and `{csv_path.relative_to(ROOT)}`.\n",
        encoding="utf-8",
    )
    print(result["status"], result["cohort_csv_sha256"])


if __name__ == "__main__":
    main()
