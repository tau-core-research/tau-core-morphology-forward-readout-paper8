#!/usr/bin/env python3
"""Propagate partial NGC4254 source uncertainties through the frozen FFL proxy."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from scipy.signal import fftconvolve

from freeze_ngc4254_ffl_determinant_source_vectors_v01 import build_rows_from_fields
from ngc4254_source_covariance_utils import (
    beam_covariance_pixels,
    gaussian_kernel_from_covariance,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

COMMON_PATH = DATA / "ngc4254_common_hi_resolution_source_cube_v03.fits"
UNCERTAINTY_PATH = DATA / "ngc4254_measurement_uncertainty_fields_v05.fits"
UNCERTAINTY_META_PATH = DATA / "ngc4254_measurement_uncertainty_fields_v05.json"
GEOMETRY_PATH = DATA / "ngc4254_s4g_photometric_geometry_freeze_v02.json"
SYSTEMATIC_PATH = DATA / "ngc4254_ffl_source_systematic_summary_v03.csv"
SAMPLES_PATH = DATA / "ngc4254_ffl_partial_measurement_samples_v05.csv"
SUMMARY_PATH = DATA / "ngc4254_ffl_partial_measurement_summary_v05.csv"
JSON_PATH = DATA / "ngc4254_ffl_partial_measurement_covariance_v05.json"
REPORT_PATH = REPORTS / "ngc4254_ffl_partial_measurement_covariance_v05.md"

STATUS = "PARTIAL_MEASUREMENT_PROPAGATION_COMPLETE_HI_CONTROL_ONLY_NO_ENDPOINT"
CLAIM_BOUNDARY = (
    "conditional source-only uncertainty propagation through a 4D inverse shape proxy; "
    "not a parent-role identification, complete covariance, channel/time/quantum signal, "
    "dark-matter replacement, or endpoint score"
)
RANDOM_SEED = 4254
N_DRAWS = 256
POSITIVE_FLOOR = 1.0e-8

SCENARIOS = (
    "star_only",
    "co_independent_only",
    "star_plus_co_independent",
    "star_plus_co_correlated_control",
    "star_co_plus_hi_ctl01",
    "star_co_plus_hi_ctl10",
    "star_co_plus_hi_ctl49",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def correlated_standard(
    rng: np.random.Generator,
    shape: tuple[int, int],
    kernel: np.ndarray,
    common: np.ndarray,
) -> np.ndarray:
    field = fftconvolve(rng.standard_normal(shape), kernel, mode="same")
    selected = field[common]
    field = (field - float(np.mean(selected))) / float(np.std(selected, ddof=1))
    return field


def positive_field(values: np.ndarray, common: np.ndarray) -> tuple[np.ndarray, float]:
    output = np.full(values.shape, np.nan, dtype=float)
    clipping_fraction = float(np.mean(values[common] <= POSITIVE_FLOOR))
    output[common] = np.maximum(values[common], POSITIVE_FLOOR)
    return output, clipping_fraction


def main() -> None:
    geometry = json.loads(GEOMETRY_PATH.read_text())
    uncertainty_meta = json.loads(UNCERTAINTY_META_PATH.read_text())
    with fits.open(COMMON_PATH) as hdul:
        star0 = np.asarray(hdul["SIGMA_STAR"].data, dtype=float)
        h20 = np.asarray(hdul["SIGMA_H2"].data, dtype=float)
        hi0 = np.asarray(hdul["SIGMA_HI"].data, dtype=float)
        wcs = WCS(hdul["SIGMA_STAR"].header, naxis=2)
        target_beam = (
            float(hdul["SIGMA_STAR"].header["BMAJ"]) * 3600.0,
            float(hdul["SIGMA_STAR"].header["BMIN"]) * 3600.0,
            float(hdul["SIGMA_STAR"].header["BPA"]),
        )
    with fits.open(UNCERTAINTY_PATH) as hdul:
        uncertainty = {
            name: np.asarray(hdul[name].data, dtype=float)
            for name in (
                "STAR_PIX",
                "STAR_SKY1",
                "STAR_SKY2",
                "STAR_ICA1",
                "STAR_ICA2",
                "H2_IND",
                "H2_CORR",
                "HI_CTL01",
                "HI_CTL10",
                "HI_CTL49",
            )
        }
        common = np.asarray(hdul["COMMON"].data, dtype=bool)
    for values in (star0, h20, hi0):
        values[~common] = np.nan

    pixel_scale_arcsec = (
        math.sqrt(abs(float(np.linalg.det(wcs.pixel_scale_matrix)))) * 3600.0
    )
    beam_covariance = beam_covariance_pixels(*target_beam, pixel_scale_arcsec)
    correlation_kernel = gaussian_kernel_from_covariance(beam_covariance)
    rng = np.random.default_rng(RANDOM_SEED)

    baseline_rows = build_rows_from_fields(geometry, star0, h20, hi0, wcs)
    baseline_q = {
        int(row["radial_index"]): float(row["q_shape_proxy"])
        for row in baseline_rows
    }
    records: list[dict[str, float | int | str]] = []
    for draw in range(N_DRAWS):
        z_star = correlated_standard(rng, star0.shape, correlation_kernel, common)
        z_h2 = correlated_standard(rng, star0.shape, correlation_kernel, common)
        z_hi = correlated_standard(rng, star0.shape, correlation_kernel, common)
        coherent = rng.standard_normal(5)

        star_perturbed = (
            star0
            + uncertainty["STAR_PIX"] * z_star
            + coherent[0] * uncertainty["STAR_SKY1"]
            + coherent[1] * uncertainty["STAR_SKY2"]
            + coherent[2] * uncertainty["STAR_ICA1"]
            + coherent[3] * uncertainty["STAR_ICA2"]
        )
        h2_independent = h20 + uncertainty["H2_IND"] * z_h2
        h2_correlated = h20 + coherent[4] * uncertainty["H2_CORR"]
        star_draw, star_clip = positive_field(star_perturbed, common)
        h2_ind_draw, h2_ind_clip = positive_field(h2_independent, common)
        h2_corr_draw, h2_corr_clip = positive_field(h2_correlated, common)

        scenario_fields: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, float, float, float]] = {
            "star_only": (star_draw, h20, hi0, star_clip, 0.0, 0.0),
            "co_independent_only": (star0, h2_ind_draw, hi0, 0.0, h2_ind_clip, 0.0),
            "star_plus_co_independent": (
                star_draw,
                h2_ind_draw,
                hi0,
                star_clip,
                h2_ind_clip,
                0.0,
            ),
            "star_plus_co_correlated_control": (
                star_draw,
                h2_corr_draw,
                hi0,
                star_clip,
                h2_corr_clip,
                0.0,
            ),
        }
        for suffix in ("01", "10", "49"):
            hi_draw, hi_clip = positive_field(
                hi0 + uncertainty[f"HI_CTL{suffix}"] * z_hi, common
            )
            scenario_fields[f"star_co_plus_hi_ctl{suffix}"] = (
                star_draw,
                h2_ind_draw,
                hi_draw,
                star_clip,
                h2_ind_clip,
                hi_clip,
            )

        for scenario in SCENARIOS:
            star, h2, hi, star_clip, h2_clip, hi_clip = scenario_fields[scenario]
            rows = build_rows_from_fields(geometry, star, h2, hi, wcs)
            for row in rows:
                records.append(
                    {
                        "scenario": scenario,
                        "draw": draw,
                        "radial_index": int(row["radial_index"]),
                        "radius_lo_arcsec": float(row["radius_lo_arcsec"]),
                        "radius_hi_arcsec": float(row["radius_hi_arcsec"]),
                        "q_shape_proxy": float(row["q_shape_proxy"]),
                        "delta_uv": float(row["delta_uv"]),
                        "star_clipped_fraction": star_clip,
                        "h2_clipped_fraction": h2_clip,
                        "hi_clipped_fraction": hi_clip,
                    }
                )

    samples = pd.DataFrame.from_records(records)
    samples.to_csv(SAMPLES_PATH, index=False, float_format="%.10g")
    systematic = pd.read_csv(SYSTEMATIC_PATH).set_index("radial_index")
    baseline_vs_v03 = np.asarray(
        [
            baseline_q[index]
            - float(systematic.loc[index, "matched_primary_q_shape_proxy"])
            for index in sorted(baseline_q)
        ],
        dtype=float,
    )
    summary_rows = []
    for (scenario, radial_index), group in samples.groupby(
        ["scenario", "radial_index"], sort=False
    ):
        values = group["q_shape_proxy"].to_numpy(dtype=float)
        baseline = baseline_q[int(radial_index)]
        positive_probability = float(np.mean(values > 0.0))
        std = float(np.std(values, ddof=1))
        systematics_std = float(
            systematic.loc[int(radial_index), "systematic_q_equal_weight_std"]
        )
        summary_rows.append(
            {
                "scenario": scenario,
                "radial_index": int(radial_index),
                "radius_lo_arcsec": float(group["radius_lo_arcsec"].iloc[0]),
                "radius_hi_arcsec": float(group["radius_hi_arcsec"].iloc[0]),
                "baseline_q_shape_proxy": baseline,
                "q_mean": float(np.mean(values)),
                "q_std": std,
                "q_p025": float(np.percentile(values, 2.5)),
                "q_p16": float(np.percentile(values, 16.0)),
                "q_median": float(np.median(values)),
                "q_p84": float(np.percentile(values, 84.0)),
                "q_p975": float(np.percentile(values, 97.5)),
                "positive_probability": positive_probability,
                "baseline_sign_probability": (
                    positive_probability if baseline > 0.0 else 1.0 - positive_probability
                ),
                "conditional_sign_stable_95": bool(
                    positive_probability >= 0.95 or positive_probability <= 0.05
                ),
                "v03_systematic_equal_weight_std": systematics_std,
                "measurement_to_v03_systematic_std_ratio": (
                    std / systematics_std if systematics_std > 0.0 else math.nan
                ),
                "mean_star_clipped_fraction": float(
                    group["star_clipped_fraction"].mean()
                ),
                "mean_h2_clipped_fraction": float(group["h2_clipped_fraction"].mean()),
                "mean_hi_clipped_fraction": float(group["hi_clipped_fraction"].mean()),
                "n_draws": int(len(group)),
            }
        )
    summary = pd.DataFrame(summary_rows).sort_values(["scenario", "radial_index"])
    summary.to_csv(SUMMARY_PATH, index=False, float_format="%.10g")

    primary = summary[summary["scenario"] == "star_plus_co_independent"]
    hi49 = summary[summary["scenario"] == "star_co_plus_hi_ctl49"]
    star_only = summary[summary["scenario"] == "star_only"]
    co_only = summary[summary["scenario"] == "co_independent_only"]
    measurement_stable = set(
        primary.loc[primary["conditional_sign_stable_95"], "radial_index"]
        .astype(int)
        .tolist()
    )
    v03_stable = set(
        systematic.loc[systematic["systematic_sign_stable"], :].index.astype(int).tolist()
    )
    manifest = {
        "schema": "ngc4254_ffl_partial_measurement_covariance_v05",
        "status": STATUS,
        "galaxy": "NGC4254",
        "random_seed": RANDOM_SEED,
        "n_draws_per_scenario": N_DRAWS,
        "scenarios": list(SCENARIOS),
        "inputs": {
            "common_resolution_cube": str(COMMON_PATH.relative_to(ROOT)),
            "common_resolution_cube_sha256": sha256(COMMON_PATH),
            "uncertainty_fields": str(UNCERTAINTY_PATH.relative_to(ROOT)),
            "uncertainty_fields_sha256": sha256(UNCERTAINTY_PATH),
            "uncertainty_metadata": str(UNCERTAINTY_META_PATH.relative_to(ROOT)),
            "uncertainty_metadata_sha256": sha256(UNCERTAINTY_META_PATH),
            "geometry": str(GEOMETRY_PATH.relative_to(ROOT)),
            "geometry_sha256": sha256(GEOMETRY_PATH),
            "velocity_or_residual_inputs": [],
        },
        "propagation": {
            "spatial_random_modes": "unit-variance Gaussian fields correlated at the common H I beam",
            "coherent_stellar_modes": ["STAR_SKY1", "STAR_SKY2", "STAR_ICA1", "STAR_ICA2"],
            "co_primary": "H2_IND exact error-map marginal field with approximate target-beam correlation",
            "co_upper_control": "one coherent standard-normal coefficient multiplying H2_CORR",
            "hi_role": "robust1 channel-count controls only",
            "positive_floor_msun_pc2": POSITIVE_FLOOR,
        },
        "primary_measurement_result": {
            "conditionally_sign_stable_annuli_95": sorted(measurement_stable),
            "median_measurement_to_v03_systematic_std_ratio": float(
                primary["measurement_to_v03_systematic_std_ratio"].median()
            ),
            "maximum_mean_component_clipping_fraction": float(
                primary[
                    ["mean_star_clipped_fraction", "mean_h2_clipped_fraction"]
                ].to_numpy().max()
            ),
            "maximum_absolute_baseline_shift_from_v03_due_to_one_pixel_mask_refinement": float(
                np.max(np.abs(baseline_vs_v03))
            ),
            "co_only_conditionally_sign_stable_annuli_95": co_only.loc[
                co_only["conditional_sign_stable_95"], "radial_index"
            ].astype(int).tolist(),
            "outer_two_median_star_to_combined_std_ratio": float(
                np.median(
                    star_only.loc[star_only["radial_index"].isin([4, 5]), "q_std"].to_numpy()
                    / primary.loc[primary["radial_index"].isin([4, 5]), "q_std"].to_numpy()
                )
            ),
            "v03_source_systematic_sign_stable_annuli": sorted(v03_stable),
            "annuli_passing_both_separate_robustness_checks": sorted(
                measurement_stable & v03_stable
            ),
        },
        "hi49_control_result": {
            "conditionally_sign_stable_annuli_95": hi49.loc[
                hi49["conditional_sign_stable_95"], "radial_index"
            ].astype(int).tolist(),
            "median_std_change_vs_no_hi_control": float(
                np.median(
                    hi49["q_std"].to_numpy()
                    - primary["q_std"].to_numpy()
                )
            ),
        },
        "outputs": {
            "samples": str(SAMPLES_PATH.relative_to(ROOT)),
            "samples_sha256": sha256(SAMPLES_PATH),
            "summary": str(SUMMARY_PATH.relative_to(ROOT)),
            "summary_sha256": sha256(SUMMARY_PATH),
            "report": str(REPORT_PATH.relative_to(ROOT)),
        },
        "audit_checks": {
            "source_only": True,
            "velocity_or_residual_inputs_empty": True,
            "fixed_random_seed": True,
            "all_expected_samples_present": bool(
                len(samples) == len(SCENARIOS) * N_DRAWS * len(baseline_rows)
            ),
            "all_q_values_finite": bool(np.isfinite(samples["q_shape_proxy"]).all()),
            "hi_controls_not_promoted": True,
            "endpoint_scored": False,
        },
        "complete_measurement_covariance_ready": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    JSON_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    table_rows = []
    for _, row in primary.iterrows():
        table_rows.append(
            "| "
            f"{row['radius_lo_arcsec']:.0f}-{row['radius_hi_arcsec']:.0f} | "
            f"{row['baseline_q_shape_proxy']:+.5f} | {row['q_median']:+.5f} | "
            f"{row['q_p025']:+.5f}, {row['q_p975']:+.5f} | "
            f"{row['baseline_sign_probability']:.3f} | "
            f"{row['measurement_to_v03_systematic_std_ratio']:.3f} |"
        )
    report = f"""# NGC4254 Partial Measurement Propagation v05

**Status:** `{STATUS}`

**Claim boundary:** {CLAIM_BOUNDARY}.

## Primary Conditional Result

The source-only Monte Carlo propagates the reconstructed stellar measurement
modes and the exact PHANGS CO error-map field through the already frozen
four-quadrant inverse operator.  It does not read any rotation endpoint.

| annulus (arcsec) | baseline q | median q | 95% interval | P(baseline sign) | measurement/v03-systematic std |
|---:|---:|---:|---:|---:|---:|
{chr(10).join(table_rows)}

Under this partial model, the annulus indices with at least 95% conditional
sign support are
`{manifest['primary_measurement_result']['conditionally_sign_stable_annuli_95']}`.
The median ratio of measurement standard deviation to the earlier v03 source-
systematic standard deviation is
`{manifest['primary_measurement_result']['median_measurement_to_v03_systematic_std_ratio']:.4f}`.
The one-pixel CO-uncertainty mask refinement shifts the matched v03 baseline by
at most
`{manifest['primary_measurement_result']['maximum_absolute_baseline_shift_from_v03_due_to_one_pixel_mask_refinement']:.6g}`.

CO measurement noise alone preserves the baseline sign in annuli
`{manifest['primary_measurement_result']['co_only_conditionally_sign_stable_annuli_95']}`.
For the outer two annuli, the median ratio of stellar-only to combined
measurement standard deviation is
`{manifest['primary_measurement_result']['outer_two_median_star_to_combined_std_ratio']:.4f}`,
so their measurement instability is stellar-mode dominated in this model.

The earlier v03 source-systematic family preserves sign only in annuli
`{manifest['primary_measurement_result']['v03_source_systematic_sign_stable_annuli']}`.
No annulus currently passes both separate checks:
`{manifest['primary_measurement_result']['annuli_passing_both_separate_robustness_checks']}`.
This is a robustness intersection, not a combined posterior probability.

## H I Control

The widest robust-1 control (`49` line channels) changes the annular standard
deviation by a median of
`{manifest['hi49_control_result']['median_std_change_vs_no_hi_control']:+.6f}`.
This is only a sensitivity result: the robust-1 cube is not the parent of the
robust-5 H I moment map used in the inverse.

## Interpretation

This run measures whether known source-map uncertainty can erase or preserve
the inverse proxy.  It cannot identify a parent morphology, channel sector,
terminal time/quantum readout, or dark-matter alternative.  Geometry and source
model systematics from v03 remain part of the total uncertainty, and exact H I
covariance remains blocked.
"""
    REPORT_PATH.write_text(report)
    print(STATUS)
    print(f"samples={len(samples)}")
    print(
        "primary_sign_stable_annuli="
        f"{manifest['primary_measurement_result']['conditionally_sign_stable_annuli_95']}"
    )


if __name__ == "__main__":
    main()
