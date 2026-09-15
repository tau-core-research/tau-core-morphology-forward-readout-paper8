#!/usr/bin/env python3
"""Freeze a velocity-blind LITTLE THINGS 2D morphology population intake."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
DATA_PAGE = "https://science.nrao.edu/science/surveys/littlethings/data"
PRODUCT_ROOT = "https://things.cv.nrao.edu/littlethings"

# Hunter et al. (2012), Tables 1, 3, and 6, plus Holwerda et al. (2013),
# Appendix A.  These are source-side quantities; no velocity pixels or rotation
# residuals were inspected to build this table.  Tuple fields are
# (name, slug, product stem, R_H arcmin, PA deg, inclination deg,
#  robust beam major/minor arcsec, published H I asymmetry and uncertainty).
ROWS = [
    ("CVnIdwA", "cvnidwa", "CVnIdwA", 0.87, 80.0, 41.0, 10.9, 10.5, 1.941, 0.092),
    ("DDO43", "ddo43", "DDO43", 0.89, 6.5, 48.5, 8.1, 6.0, 1.793, 0.049),
    ("DDO46", "ddo46", "DDO46", None, 84.0, 28.6, 6.3, 5.2, 1.384, 0.050),
    ("DDO47", "ddo47", "DDO47", 2.24, -70.0, 64.4, 10.4, 9.0, 0.612, 0.058),
    ("DDO50", "ddo50", "DDO50", 3.97, 18.0, 46.7, 7.0, 6.1, 1.742, 0.014),
    ("DDO52", "ddo52", "DDO52", 1.08, 5.0, 51.1, 6.8, 5.2, 1.239, 0.159),
    ("DDO53", "ddo53", "DDO53", 1.37, 81.0, 64.4, 6.3, 5.7, 1.951, 0.052),
    ("DDO63", "ddo63", "DDO63", 2.17, 0.0, 0.0, 7.8, 6.0, 1.449, 0.041),
    ("DDO69", "ddo69", "DDO69", 2.40, -64.0, 60.3, 5.8, 5.4, 1.551, 0.154),
    ("DDO70", "ddo70", "DDO70", 3.71, 88.0, 57.8, 13.8, 13.2, 1.136, 0.037),
    ("DDO75", "ddo75", "DDO75", 3.09, 41.0, 33.5, 7.6, 6.5, 2.000, 0.000),
    ("DDO87", "ddo87", "DDO87", 1.15, 76.5, 58.6, 7.6, 6.2, 0.736, 0.066),
    ("DDO101", "ddo101", "DDO101", 1.05, -69.0, 49.4, 8.3, 7.0, 1.682, 0.162),
    ("DDO126", "ddo126", "DDO126", 1.76, -41.0, 67.7, 6.9, 5.6, 1.360, 0.266),
    ("DDO133", "ddo133", "DDO133", 2.33, -6.0, 49.4, 12.4, 10.8, 1.820, 0.091),
    ("DDO154", "ddo154", "DDO154", 1.55, 46.0, 65.2, 7.9, 6.3, 1.519, 0.058),
    ("DDO155", "ddo155", "DDO155", 0.95, 51.0, 47.6, 11.3, 10.1, 1.481, 0.138),
    ("DDO165", "ddo165", "DDO165", 2.14, 89.0, 61.9, 10.0, 7.6, 1.955, 0.055),
    ("DDO167", "ddo167", "DDO167", 0.75, -23.0, 52.8, 7.3, 5.3, 1.847, 0.167),
    ("DDO168", "ddo168", "DDO168", 2.32, -24.5, 54.5, 7.8, 5.8, 1.137, 0.043),
    ("DDO187", "ddo187", "DDO187", 1.06, 37.0, 39.0, 6.2, 5.5, 1.438, 0.252),
    ("DDO210", "ddo210", "DDO210", 1.31, -85.0, 66.9, 11.7, 8.6, 2.000, 0.000),
    ("DDO216", "ddo216", "DDO216", 4.00, -58.0, 69.4, 16.2, 15.4, 1.688, 0.101),
    ("F564-V3", "f564v3", "F564-V3", None, 8.5, 35.8, 12.5, 8.1, 1.670, 0.204),
    ("IC10", "ic10", "IC10", None, -38.0, 41.0, 5.9, 5.5, 1.984, 0.003),
    ("IC1613", "ic1613", "IC1613", 9.10, 71.0, 37.9, 7.7, 6.5, 1.076, 0.029),
    ("LGS3", "lgs3", "LGS3", 0.96, -3.5, 64.4, 11.8, 9.3, 1.179, 0.092),
    ("M81dwA", "m81dwa", "M81DWA", None, 86.0, 45.8, 7.8, 6.3, 2.000, 0.000),
    ("NGC1569", "ngc1569", "NGC1569", None, -59.0, 61.1, 5.9, 5.2, 1.987, 0.002),
    ("NGC2366", "ngc2366", "NGC2366", 4.72, 32.5, 72.1, 6.9, 5.9, 1.565, 0.084),
    ("NGC3738", "ngc3738", "NGC3738", 2.40, 0.0, 0.0, 6.3, 5.5, 1.916, 0.019),
    ("NGC4163", "ngc4163", "NGC4163", 1.47, 18.0, 53.7, 9.7, 5.9, 1.281, 0.136),
    ("NGC4214", "ngc4214", "NGC4214", 4.67, 16.0, 25.8, 7.6, 6.4, 0.969, 0.040),
    ("SagDIG", "sagdig", "SAGDIG", None, 87.5, 62.7, 28.2, 16.9, 2.000, 0.000),
    ("UGC8508", "ugc8508", "UGC8508", 1.28, -60.0, 61.9, 5.9, 4.9, 1.937, 0.086),
    ("WLM", "wlm", "WLM", 5.81, -2.0, 70.3, 7.6, 5.1, 2.000, 0.000),
    ("Haro29", "haro29", "Haro29", 0.84, 86.0, 58.6, 6.8, 5.6, 0.949, 0.088),
    ("Haro36", "haro36", "Haro36", None, 2.0, 37.9, 7.0, 5.8, 1.605, 0.076),
    ("Mrk178", "mrk178", "Mrk178", 1.01, -50.0, 68.6, 6.2, 5.5, 1.254, 0.142),
    ("VIIZw403", "viizw403", "VIIZw403", 1.11, -10.0, 66.0, 9.4, 7.7, 2.000, 0.000),
]

# Hunter et al. (2012), Table 6 optical centers.  Only the 25 rows allowed into
# the moment-0 preflight need coordinates here; excluded rows are never opened.
CENTERS = {
    "DDO47": ("07:41:55.3", "+16:48:08"),
    "DDO50": ("08:19:08.7", "+70:43:25"),
    "DDO52": ("08:28:28.5", "+41:51:21"),
    "DDO53": ("08:34:08.0", "+66:10:37"),
    "DDO69": ("09:59:25.0", "+30:44:42"),
    "DDO70": ("10:00:00.9", "+05:19:50"),
    "DDO75": ("10:10:59.2", "-04:41:56"),
    "DDO87": ("10:49:34.7", "+65:31:46"),
    "DDO126": ("12:27:06.5", "+37:08:23"),
    "DDO133": ("12:32:55.4", "+31:32:14"),
    "DDO154": ("12:54:06.2", "+27:09:02"),
    "DDO165": ("13:06:25.3", "+67:42:25"),
    "DDO168": ("13:14:27.2", "+45:55:46"),
    "DDO187": ("14:15:56.7", "+23:03:19"),
    "DDO216": ("23:28:35.0", "+14:44:30"),
    "F564-V3": ("09:02:53.9", "+20:04:29"),
    "IC10": ("00:20:21.9", "+59:17:39"),
    "IC1613": ("01:04:49.2", "+02:07:48"),
    "M81dwA": ("08:23:57.2", "+71:01:51"),
    "NGC1569": ("04:30:49.8", "+64:50:51"),
    "NGC4163": ("12:12:09.2", "+36:10:13"),
    "SagDIG": ("19:30:00.6", "-17:40:56"),
    "UGC8508": ("13:30:44.9", "+54:54:29"),
    "Haro36": ("12:46:56.3", "+51:36:48"),
    "Mrk178": ("11:33:29.0", "+49:14:24"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, slug, stem, rh, pa, inc, bmaj, bmin, asym, asym_err in ROWS:
        beams_per_rh = None if rh is None else 60.0 * rh / math.sqrt(bmaj * bmin)
        if not 30.0 <= inc <= 70.0:
            status = "EXCLUDED_SOURCE_GEOMETRY"
        elif beams_per_rh is None:
            status = "SOURCE_MOM0_SUPPORT_PENDING"
        elif beams_per_rh < 10.0:
            status = "EXCLUDED_PUBLISHED_SUPPORT_LT_10_BEAMS_PER_RH"
        else:
            status = "PROVISIONAL_SOURCE_CANDIDATE"
        rows.append({
            "galaxy": name,
            "metadata_slug": slug,
            "product_stem": stem,
            "holmberg_radius_arcmin": rh,
            "optical_pa_deg": pa,
            "optical_inclination_deg": inc,
            "robust_beam_major_arcsec": bmaj,
            "robust_beam_minor_arcsec": bmin,
            "published_hi_asymmetry": asym,
            "published_hi_asymmetry_error": asym_err,
            "catalog_ra_hms": CENTERS.get(name, (None, None))[0],
            "catalog_dec_dms": CENTERS.get(name, (None, None))[1],
            "published_beams_per_rh": beams_per_rh,
            "source_status": status,
            "metadata_url": f"{DATA_PAGE}/{slug.replace('ddo', 'd', 1) if slug.startswith('ddo') else slug.replace('ngc', 'n', 1) if slug.startswith('ngc') else slug.replace('ugc', 'u', 1) if slug.startswith('ugc') else slug}.html",
            "moment0_url": f"{PRODUCT_ROOT}/{slug}/HI/{stem}_R_X0_P_R.FITS",
        })

    csv_path = DATA / "little_things_2d_morphology_population_preregistration_v01.csv"
    json_path = DATA / "little_things_2d_morphology_population_preregistration_v01.json"
    report_path = REPORTS / "little_things_2d_morphology_population_preregistration_v01.md"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    counts = {status: sum(row["source_status"] == status for row in rows) for status in {
        row["source_status"] for row in rows
    }}
    result = {
        "schema": "little_things_2d_morphology_population_preregistration_v01",
        "status": "SOURCE_POPULATION_FROZEN_MOM0_ONLY_ACQUISITION_ALLOWED",
        "survey": "LITTLE THINGS robust-weighted H I products",
        "primary_sources": [
            {"citation": "Hunter et al. 2012, AJ 144, 134", "arxiv": "https://arxiv.org/abs/1208.5834"},
            {"citation": "Holwerda et al. 2013, MNRAS 433, 47", "arxiv": "https://arxiv.org/abs/1307.2085"},
            {"data_page": DATA_PAGE},
        ],
        "population_rule": "all 40 galaxies common to the published LITTLE THINGS morphology and product tables; no disturbed/quiet label selection",
        "source_gates": {
            "inclination_deg": [30.0, 70.0],
            "minimum_published_or_measured_beams_per_source_radius": 10.0,
            "published_radius_role": "screen only; final support is remeasured from moment-0 before any velocity-field access",
            "missing_published_radius": "retain for moment-0-only support preflight",
        },
        "counts": counts,
        "rows": rows,
        "test_design": {
            "source_mode": "moment-0 m=1 radial envelope and phase, normalized within galaxy",
            "velocity_target": "one global two-quadrature k=2 upper sideband after nuisance projection; never 2J independent gains",
            "adaptive_radial_capacity": "J_cap=min(5,floor(0.8*B_source/2)); require J>=2 and freeze J before velocity access",
            "nuisance": "systemic plus k=1 circular/radial terms and only source-supported center/PA/inclination tangents",
            "primary_score": "per-galaxy cross-validated matched-minus-wrong-template specificity; population one-sided signed-rank/sign sensitivity across all eligible galaxies",
            "wrong_templates": ["radial_reversal", "nonconstant_annular_phase_scramble", "cross_galaxy_derangement"],
            "forbidden_wrong_template": "a global phase rotation is the same two-quadrature target subspace and therefore is not a valid negative control",
            "secondary_effect_modifier": "published H I asymmetry, restricted to non-boundary values with nonzero quoted uncertainty",
            "population_sensitivity": "at n=19 provisional galaxies, normal-theory one-sided alpha=0.05 and 80% power corresponds to paired standardized effect about 0.57; this is an engineering sensitivity statement, not evidence",
        },
        "cross_validation": {
            "blocks": "deterministic contiguous beam-separated azimuth blocks; K>=6, K=8 preferred",
            "minimum_independent_beams_per_block": 2,
            "each_radial_zone_minimum_blocks": 4,
            "maximum_azimuth_gap_rad": math.pi / 2.0,
            "rank": "each training fold preserves nuisance rank and adds exactly two projected target dimensions; held-out target rank=2",
            "condition_number_max": 100.0,
            "maximum_leverage": 0.25,
            "minimum_residual_df": "max(10, nuisance_rank+2)",
        },
        "opening_order": [
            "freeze this source population",
            "download/open robust moment-0 maps only",
            "freeze source masks, support, radial capacity, m=1 templates, folds, and wrong controls",
            "run injection/recovery calibration without observed velocity pixels",
            "only then permit robust moment-1 acquisition and endpoint scoring",
        ],
        "velocity_product_acquisition_allowed": False,
        "velocity_pixels_opened": False,
        "tau_endpoint_allowed": False,
        "claim_boundary": "velocity-blind conventional sensitivity design; it cannot select parent morphology, establish parent loss, modify gravity, replace dark matter, or validate Tau Core",
    }
    result["cohort_csv"] = str(csv_path.relative_to(ROOT))
    result["cohort_csv_sha256"] = sha256(csv_path)
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(
        "# LITTLE THINGS 2D morphology population preregistration v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "This velocity-blind packet replaces the underpowered VIVA 3+3 role-label pilot with a "
        "continuous, all-object source intake. The published tables yield 19 provisional source "
        "candidates, six moment-0 support-pending cases, nine published support failures, and six "
        "geometry exclusions. No observed velocity pixel or rotation residual entered the selection.\n\n"
        "Only robust-weighted moment-0 acquisition is now allowed. Source masks, actual support, "
        "adaptive radial capacity, the normalized m=1 template, cross-validation blocks, rank gates, "
        "and wrong-template controls must be frozen before any moment-1 product is acquired. The "
        "primary population statistic is within-galaxy matched-minus-wrong specificity; published "
        "asymmetry is only a secondary continuous effect modifier, not a disturbed/quiet selector.\n\n"
        "A pass would show that ordinary H I morphology predicts held-out H I kinematics better than "
        "predeclared wrong templates. Conventional gas dynamics can produce such a pass, so this is "
        "not a Tau, parent-loss, gravity, or dark-matter endpoint.\n",
        encoding="utf-8",
    )
    print(result["status"], counts, result["cohort_csv_sha256"])


if __name__ == "__main__":
    main()
