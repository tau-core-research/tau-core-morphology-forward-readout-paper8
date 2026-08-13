#!/usr/bin/env python3
"""Freeze beam-matched source-systematic scenarios for the NGC4254 FFL proxy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS

from freeze_ngc4254_ffl_determinant_photometric_v02 import geometry_variants, variant_geometry
from freeze_ngc4254_ffl_determinant_source_vectors_v01 import build_rows_from_fields


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

GEOMETRY_PATH = DATA / "ngc4254_s4g_photometric_geometry_freeze_v02.json"
CUBE_PATH = DATA / "ngc4254_common_hi_resolution_source_cube_v03.fits"
CUBE_META_PATH = DATA / "ngc4254_common_hi_resolution_source_cube_v03.json"
UNMATCHED_PRIMARY_PATH = DATA / "ngc4254_ffl_determinant_photometric_vectors_v02.csv"
BEAM_OVERLAP_PATH = DATA / "ngc4254_ffl_determinant_beam_overlap_correlation_v02.csv"
SCENARIO_PATH = DATA / "ngc4254_ffl_source_systematic_scenarios_v03.csv"
SUMMARY_PATH = DATA / "ngc4254_ffl_source_systematic_summary_v03.csv"
SCENARIO_COVARIANCE_PATH = DATA / "ngc4254_ffl_source_scenario_covariance_v03.csv"
DRIVER_SUMMARY_PATH = DATA / "ngc4254_ffl_source_systematic_driver_summary_v03.csv"
JSON_PATH = DATA / "ngc4254_ffl_source_systematics_v03.json"
REPORT_PATH = REPORTS / "ngc4254_ffl_source_systematics_v03.md"

STATUS = "BEAM_MATCHED_SOURCE_SYSTEMATICS_FROZEN_MEASUREMENT_COVARIANCE_NOT_IDENTIFIABLE"
CLAIM_BOUNDARY = (
    "equal-weight source-systematic sensitivity ensemble and exact beam-overlap rank; "
    "not a probability model, complete measurement covariance, physical q_det, channel signal, or endpoint score"
)
H2_CONVERSION_FACTORS = [0.7, 1.0, 1.3]
STAR_SCALE_INVARIANCE_CONTROLS = [0.7, 1.0, 1.3]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    geometry = json.loads(GEOMETRY_PATH.read_text(encoding="utf-8"))
    cube_meta = json.loads(CUBE_META_PATH.read_text(encoding="utf-8"))
    if cube_meta["inputs"]["velocity_or_residual_inputs"]:
        raise ValueError("Common-resolution cube declares forbidden endpoint inputs")

    with fits.open(CUBE_PATH) as hdul:
        h2 = np.asarray(hdul["SIGMA_H2"].data, dtype=float)
        hi = np.asarray(hdul["SIGMA_HI"].data, dtype=float)
        wcs = WCS(hdul["SIGMA_STAR"].header, naxis=2)
        star_controls = {
            "psf_0arcsec_primary": np.asarray(hdul["STAR_P00"].data, dtype=float),
            "psf_2arcsec_control": np.asarray(hdul["STAR_P20"].data, dtype=float),
            "psf_4arcsec_control": np.asarray(hdul["STAR_P40"].data, dtype=float),
        }

    variants = [
        row
        for row in geometry_variants(geometry)
        if row["variant_class"] in ("photometric_primary", "photometric_control")
    ]
    records = []
    for variant in variants:
        scenario_geometry = variant_geometry(geometry, variant)
        for psf_name, star in star_controls.items():
            for h2_factor in H2_CONVERSION_FACTORS:
                rows = build_rows_from_fields(
                    scenario_geometry,
                    star,
                    h2,
                    hi,
                    wcs,
                    h2_scale=h2_factor,
                )
                for row in rows:
                    records.append(
                        {
                            "geometry_variant": variant["variant"],
                            "geometry_variant_class": variant["variant_class"],
                            "stellar_psf_scenario": psf_name,
                            "h2_conversion_factor": h2_factor,
                            "radial_index": row["radial_index"],
                            "radius_lo_arcsec": row["radius_lo_arcsec"],
                            "radius_hi_arcsec": row["radius_hi_arcsec"],
                            "n_pixels_total": row["n_pixels_total"],
                            "delta_uv": row["delta_uv"],
                            "q_shape_proxy": row["q_shape_proxy"],
                        }
                    )
    scenarios = pd.DataFrame(records)
    scenarios.to_csv(SCENARIO_PATH, index=False, float_format="%.12g", lineterminator="\n")

    expected_scenarios = len(variants) * len(star_controls) * len(H2_CONVERSION_FACTORS)
    per_annulus = scenarios.groupby("radial_index").size()
    if not per_annulus.eq(expected_scenarios).all():
        raise ValueError("Not every source-systematic scenario produced every annulus")

    primary = scenarios.loc[
        scenarios["geometry_variant"].eq("s4g_global_thin_primary")
        & scenarios["stellar_psf_scenario"].eq("psf_0arcsec_primary")
        & scenarios["h2_conversion_factor"].eq(1.0)
    ].sort_values("radial_index")
    unmatched = pd.read_csv(UNMATCHED_PRIMARY_PATH).sort_values("radial_index")
    if len(primary) != len(unmatched):
        raise ValueError("Matched and unmatched primary vectors have different lengths")

    summary_rows = []
    for radial_index, group in scenarios.groupby("radial_index", sort=True):
        primary_row = primary.loc[primary["radial_index"].eq(radial_index)].iloc[0]
        unmatched_row = unmatched.loc[unmatched["radial_index"].eq(radial_index)].iloc[0]
        q_values = group["q_shape_proxy"].to_numpy(float)
        signs = np.sign(q_values)
        summary_rows.append(
            {
                "radial_index": int(radial_index),
                "radius_lo_arcsec": float(group["radius_lo_arcsec"].iloc[0]),
                "radius_hi_arcsec": float(group["radius_hi_arcsec"].iloc[0]),
                "unmatched_primary_q_shape_proxy": float(unmatched_row["q_shape_proxy"]),
                "matched_primary_q_shape_proxy": float(primary_row["q_shape_proxy"]),
                "matched_minus_unmatched_q": float(
                    primary_row["q_shape_proxy"] - unmatched_row["q_shape_proxy"]
                ),
                "beam_matching_changes_primary_sign": bool(
                    np.sign(primary_row["q_shape_proxy"])
                    != np.sign(unmatched_row["q_shape_proxy"])
                ),
                "systematic_q_min": float(np.min(q_values)),
                "systematic_q_max": float(np.max(q_values)),
                "systematic_q_equal_weight_std": float(np.std(q_values, ddof=1)),
                "systematic_sign_stable": bool(
                    np.all(signs > 0.0) or np.all(signs < 0.0)
                ),
                "minimum_delta_uv": float(group["delta_uv"].min()),
                "maximum_delta_uv": float(group["delta_uv"].max()),
                "n_source_systematic_scenarios": int(len(group)),
            }
        )
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(SUMMARY_PATH, index=False, float_format="%.12g", lineterminator="\n")

    driver_masks = {
        "geometry_only": scenarios["stellar_psf_scenario"].eq("psf_0arcsec_primary")
        & scenarios["h2_conversion_factor"].eq(1.0),
        "stellar_psf_only": scenarios["geometry_variant"].eq(
            "s4g_global_thin_primary"
        )
        & scenarios["h2_conversion_factor"].eq(1.0),
        "h2_conversion_only": scenarios["geometry_variant"].eq(
            "s4g_global_thin_primary"
        )
        & scenarios["stellar_psf_scenario"].eq("psf_0arcsec_primary"),
    }
    driver_records = []
    for driver, select in driver_masks.items():
        for radial_index, group in scenarios.loc[select].groupby(
            "radial_index", sort=True
        ):
            values = group["q_shape_proxy"].to_numpy(float)
            signs = np.sign(values)
            driver_records.append(
                {
                    "driver": driver,
                    "radial_index": int(radial_index),
                    "q_min": float(np.min(values)),
                    "q_max": float(np.max(values)),
                    "q_range": float(np.max(values) - np.min(values)),
                    "sign_stable": bool(
                        np.all(signs > 0.0) or np.all(signs < 0.0)
                    ),
                    "n_scenarios": int(len(group)),
                }
            )
    driver_summary = pd.DataFrame(driver_records)
    driver_summary.to_csv(
        DRIVER_SUMMARY_PATH,
        index=False,
        float_format="%.12g",
        lineterminator="\n",
    )

    scenario_key = ["geometry_variant", "stellar_psf_scenario", "h2_conversion_factor"]
    matrix = scenarios.pivot(index=scenario_key, columns="radial_index", values="q_shape_proxy")
    scenario_covariance = np.cov(matrix.to_numpy(float), rowvar=False, ddof=1)
    covariance_records = []
    for row_index in range(scenario_covariance.shape[0]):
        for column_index in range(scenario_covariance.shape[1]):
            covariance_records.append(
                {
                    "row_radial_index": row_index,
                    "column_radial_index": column_index,
                    "equal_weight_scenario_covariance": scenario_covariance[
                        row_index, column_index
                    ],
                }
            )
    pd.DataFrame(covariance_records).to_csv(
        SCENARIO_COVARIANCE_PATH,
        index=False,
        float_format="%.12g",
        lineterminator="\n",
    )

    max_star_scale_difference = 0.0
    for scale in STAR_SCALE_INVARIANCE_CONTROLS:
        controlled = build_rows_from_fields(
            geometry,
            star_controls["psf_0arcsec_primary"],
            h2,
            hi,
            wcs,
            star_scale=scale,
        )
        differences = np.abs(
            np.asarray([row["q_shape_proxy"] for row in controlled])
            - primary["q_shape_proxy"].to_numpy(float)
        )
        max_star_scale_difference = max(
            max_star_scale_difference, float(np.max(differences))
        )

    beam_long = pd.read_csv(BEAM_OVERLAP_PATH)
    n_annuli = len(summary)
    beam_matrix = beam_long.pivot(
        index="row_radial_index",
        columns="column_radial_index",
        values="beam_overlap_correlation_proxy",
    ).to_numpy(float)
    beam_eigenvalues = np.linalg.eigvalsh(beam_matrix)[::-1]
    beam_effective_rank = float(
        np.sum(beam_eigenvalues) ** 2 / np.sum(beam_eigenvalues**2)
    )
    if beam_matrix.shape != (n_annuli, n_annuli):
        raise ValueError("Beam-overlap matrix shape disagrees with source scenarios")

    stable_indices = summary.loc[summary["systematic_sign_stable"], "radial_index"].tolist()
    sign_change_indices = summary.loc[
        summary["beam_matching_changes_primary_sign"], "radial_index"
    ].tolist()
    manifest = {
        "schema": "ngc4254_ffl_source_systematics_v03",
        "status": STATUS,
        "galaxy": "NGC4254",
        "inputs": {
            "photometric_geometry": str(GEOMETRY_PATH.relative_to(ROOT)),
            "photometric_geometry_sha256": sha256(GEOMETRY_PATH),
            "common_hi_resolution_cube": str(CUBE_PATH.relative_to(ROOT)),
            "common_hi_resolution_cube_sha256": sha256(CUBE_PATH),
            "common_hi_resolution_metadata": str(CUBE_META_PATH.relative_to(ROOT)),
            "common_hi_resolution_metadata_sha256": sha256(CUBE_META_PATH),
            "unmatched_primary_vectors": str(UNMATCHED_PRIMARY_PATH.relative_to(ROOT)),
            "unmatched_primary_vectors_sha256": sha256(UNMATCHED_PRIMARY_PATH),
            "beam_overlap_matrix": str(BEAM_OVERLAP_PATH.relative_to(ROOT)),
            "beam_overlap_matrix_sha256": sha256(BEAM_OVERLAP_PATH),
            "velocity_or_residual_inputs": [],
        },
        "frozen_systematics": {
            "photometric_geometry_variants": [row["variant"] for row in variants],
            "stellar_native_psf_fwhm_arcsec": [0.0, 2.0, 4.0],
            "h2_conversion_factors": H2_CONVERSION_FACTORS,
            "stellar_global_scale_invariance_controls": STAR_SCALE_INVARIANCE_CONTROLS,
            "n_equal_weight_scenarios": expected_scenarios,
            "scenario_weights_have_probability_interpretation": False,
        },
        "summary": {
            "n_annuli": n_annuli,
            "systematic_sign_stable_radial_indices": [int(value) for value in stable_indices],
            "systematic_sign_unstable_radial_indices": [
                int(value)
                for value in summary.loc[
                    ~summary["systematic_sign_stable"], "radial_index"
                ].tolist()
            ],
            "beam_matching_primary_sign_change_radial_indices": [
                int(value) for value in sign_change_indices
            ],
            "maximum_q_change_under_global_stellar_scale": max_star_scale_difference,
            "beam_overlap_participation_effective_rank": beam_effective_rank,
            "beam_overlap_eigenvalues": beam_eigenvalues.tolist(),
            "radial_rows_are_independent": False,
        },
        "covariance_boundary": {
            "equal_weight_scenario_covariance_available": True,
            "equal_weight_scenario_covariance_is_measurement_covariance": False,
            "beam_overlap_correlation_available": True,
            "beam_overlap_is_complete_q_covariance": False,
            "complete_measurement_covariance_identifiable_from_available_products": False,
            "reason": "no moment0 uncertainty maps or calibration covariance, nonlinear quadrant medians, and only about 1.75 beam-overlap radial modes",
            "diagonal_six_row_likelihood_allowed": False,
        },
        "outputs": {
            "systematic_scenarios": str(SCENARIO_PATH.relative_to(ROOT)),
            "systematic_scenarios_sha256": sha256(SCENARIO_PATH),
            "systematic_summary": str(SUMMARY_PATH.relative_to(ROOT)),
            "systematic_summary_sha256": sha256(SUMMARY_PATH),
            "equal_weight_scenario_covariance": str(
                SCENARIO_COVARIANCE_PATH.relative_to(ROOT)
            ),
            "equal_weight_scenario_covariance_sha256": sha256(
                SCENARIO_COVARIANCE_PATH
            ),
            "systematic_driver_summary": str(DRIVER_SUMMARY_PATH.relative_to(ROOT)),
            "systematic_driver_summary_sha256": sha256(DRIVER_SUMMARY_PATH),
            "report": str(REPORT_PATH.relative_to(ROOT)),
        },
        "audit_checks": {
            "velocity_or_residual_inputs_empty": True,
            "all_scenarios_complete": True,
            "psf_and_h2_one_factor_signs_stable_in_all_annuli": bool(
                driver_summary.loc[
                    driver_summary["driver"].isin(
                        ["stellar_psf_only", "h2_conversion_only"]
                    ),
                    "sign_stable",
                ].all()
            ),
            "geometry_one_factor_has_sign_instability": bool(
                (~driver_summary.loc[
                    driver_summary["driver"].eq("geometry_only"), "sign_stable"
                ]).any()
            ),
            "stellar_global_scale_cancels_in_centered_log_shape": bool(
                max_star_scale_difference < 1.0e-12
            ),
            "beam_matrix_symmetric_unit_diagonal_psd": bool(
                np.allclose(beam_matrix, beam_matrix.T, atol=1.0e-12)
                and np.allclose(np.diag(beam_matrix), 1.0, atol=1.0e-12)
                and float(np.min(beam_eigenvalues)) >= -1.0e-10
            ),
        },
        "physical_amplitude_ready": False,
        "complete_measurement_covariance_ready": False,
        "endpoint_scoring_authorized": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    table_lines = [
        "| annulus | unmatched q | matched q | all-systematic range | sign stable | min Delta_uv |",
        "|---:|---:|---:|---:|:---:|---:|",
    ]
    for row in summary.itertuples(index=False):
        table_lines.append(
            f"| {row.radius_lo_arcsec:.0f}-{row.radius_hi_arcsec:.0f} | "
            f"{row.unmatched_primary_q_shape_proxy:+.6f} | "
            f"{row.matched_primary_q_shape_proxy:+.6f} | "
            f"[{row.systematic_q_min:+.6f}, {row.systematic_q_max:+.6f}] | "
            f"{'yes' if row.systematic_sign_stable else 'no'} | "
            f"{row.minimum_delta_uv:.6f} |"
        )
    report = f"""# NGC4254 FFL Source Systematics v03

**Status:** `{STATUS}`

**Claim boundary:** {CLAIM_BOUNDARY}.

The source-only proxy was recomputed after matching stellar and CO maps to the
exact VIVA H I beam. The finite ensemble crosses eight predeclared S4G
photometric geometries, three stellar native-PSF assumptions, and the inherited
0.7/1.0/1.3 molecular-conversion controls. No velocity, rotation curve,
residual, or dark-discrepancy value is read.

{chr(10).join(table_lines)}

Beam matching changes the primary sign in radial indices
`{[int(value) for value in sign_change_indices]}`. Across all 72 source
scenarios, only indices `{[int(value) for value in stable_indices]}` retain a
fixed sign. The one-factor decomposition attributes the sign instability to
the photometric geometry ensemble: the stellar-PSF and H2-conversion controls
alone preserve every primary sign. A global stellar conversion factor cancels from the centered-log
body tangent to numerical precision (maximum q change
`{max_star_scale_difference:.3e}`), so it is verified as an invariance rather
than counted repeatedly in the scenario covariance.

The equal-weight scenario covariance is an engineering sensitivity summary,
not a probability distribution. Separately, the exact H I beam-overlap matrix
has participation effective rank `{beam_effective_rank:.3f}` for six radial
rows. With no moment0 error maps or calibration covariance and with nonlinear
quadrant medians, a complete q covariance is not identifiable from the
available products. A diagonal six-row likelihood is forbidden.

This closes beam matching and finite source-systematic propagation for the
proxy, but it does not authorize endpoint scoring. Physical `eta`, primitive
`kappa_X/kappa_Y`, terminal gain, role-to-probe identity, paired-side
involution, and an untouched side-resolved terminal remain open.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")
    JSON_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(STATUS)
    print(
        f"scenarios={expected_scenarios} stable={stable_indices} "
        f"beam_rank={beam_effective_rank:.6f}"
    )


if __name__ == "__main__":
    main()
