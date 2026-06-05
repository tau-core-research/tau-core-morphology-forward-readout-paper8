#!/usr/bin/env python3
"""Build a residual-blind first-pass q_warp measurement from THINGS maps.

This script uses only cached THINGS H I moment maps and scalar geometry
prepared by the worksheet. It does not read observed rotation velocities,
endpoint residuals, baseline scores, or best-fit family results.

The output is deliberately review-required: it promotes a reproducible
source-native measurement candidate, not an accepted formula-freeze input.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_things_qwarp_first_pass_measurement_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def read_fits_image(path: Path) -> np.ndarray:
    data = np.asarray(fits.getdata(path), dtype=float)
    return np.squeeze(data)


def weighted_percentile(values: np.ndarray, weights: np.ndarray, percentile: float) -> float:
    order = np.argsort(values)
    values_sorted = values[order]
    weights_sorted = weights[order]
    cumulative = np.cumsum(weights_sorted)
    cutoff = percentile / 100.0 * cumulative[-1]
    return float(values_sorted[np.searchsorted(cumulative, cutoff, side="left")])


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    total = float(np.sum(weights))
    if total <= 0:
        return math.nan
    return float(np.sum(values * weights) / total)


def principal_axis(x: np.ndarray, y: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, float, float]:
    x0 = weighted_mean(x, weights)
    y0 = weighted_mean(y, weights)
    dx = x - x0
    dy = y - y0
    total = float(np.sum(weights))
    cov_xx = float(np.sum(weights * dx * dx) / total)
    cov_xy = float(np.sum(weights * dx * dy) / total)
    cov_yy = float(np.sum(weights * dy * dy) / total)
    cov = np.array([[cov_xx, cov_xy], [cov_xy, cov_yy]])
    eigvals, eigvecs = np.linalg.eigh(cov)
    major = eigvecs[:, int(np.argmax(eigvals))]
    if major[0] < 0:
        major = -major
    pa_image_deg = math.degrees(math.atan2(float(major[1]), float(major[0])))
    axis_ratio = math.sqrt(float(np.min(eigvals) / np.max(eigvals)))
    return major, pa_image_deg, axis_ratio


def measure_product(product_id: str, local_path: Path, geometry: pd.Series) -> dict[str, object]:
    image = read_fits_image(local_path)
    if image.ndim != 2:
        raise ValueError(f"{product_id} is not a 2D squeezed image: shape={image.shape}")

    y_idx, x_idx = np.indices(image.shape)
    x = x_idx.astype(float) - (float(geometry["crpix1"]) - 1.0)
    y = y_idx.astype(float) - (float(geometry["crpix2"]) - 1.0)
    r_circular = np.hypot(x, y)

    positive = np.where(np.isfinite(image), np.maximum(image, 0.0), 0.0)
    positive_values = positive[positive > 0]
    if positive_values.size == 0:
        raise ValueError(f"{product_id} has no positive moment-0 pixels")

    p95 = float(np.percentile(positive_values, 95))
    threshold = 0.20 * p95
    signal = positive >= threshold

    warp_onset_pix = float(geometry["warp_onset_pix"])
    rhi_pix = float(geometry["rhi_pix"])
    inner_mask = signal & (r_circular <= warp_onset_pix)
    if int(np.sum(inner_mask)) < 100:
        inner_mask = signal & (r_circular <= 1.25 * warp_onset_pix)

    major, pa_image_deg, axis_ratio = principal_axis(
        x[inner_mask], y[inner_mask], positive[inner_mask]
    )
    minor = np.array([-major[1], major[0]])
    u = x * major[0] + y * major[1]
    v = x * minor[0] + y * minor[1]

    inner_reference = signal & (np.abs(u) >= 0.50 * warp_onset_pix) & (
        np.abs(u) <= warp_onset_pix
    )
    outer = signal & (np.abs(u) >= warp_onset_pix) & (np.abs(u) <= rhi_pix)
    side_a_inner = inner_reference & (u > 0)
    side_b_inner = inner_reference & (u < 0)
    side_a_outer = outer & (u > 0)
    side_b_outer = outer & (u < 0)

    v_inner_a = weighted_mean(v[side_a_inner], positive[side_a_inner])
    v_inner_b = weighted_mean(v[side_b_inner], positive[side_b_inner])
    v_outer_a = weighted_mean(v[side_a_outer], positive[side_a_outer])
    v_outer_b = weighted_mean(v[side_b_outer], positive[side_b_outer])
    offset_a = abs(v_outer_a - v_inner_a)
    offset_b = abs(v_outer_b - v_inner_b)
    local_extent = max(rhi_pix - warp_onset_pix, 1.0)
    q_side_a = offset_a / local_extent
    q_side_b = offset_b / local_extent

    weight_a = float(np.sum(positive[side_a_outer]))
    weight_b = float(np.sum(positive[side_b_outer]))
    total_side_weight = weight_a + weight_b
    side_a_weight = weight_a / total_side_weight if total_side_weight > 0 else math.nan
    side_b_weight = weight_b / total_side_weight if total_side_weight > 0 else math.nan
    q_warp = side_a_weight * q_side_a + side_b_weight * q_side_b
    side_asymmetry_fraction = abs(q_side_a - q_side_b) / max(q_warp, 1.0e-12)

    return {
        "galaxy": GALAXY,
        "product_id": product_id,
        "source_product_path": str(local_path.relative_to(ROOT)),
        "threshold_rule": "positive_mom0_pixels_above_0p20_p95",
        "p95_positive_mom0": p95,
        "signal_threshold": threshold,
        "inner_signal_pixels": int(np.sum(inner_mask)),
        "outer_side_a_pixels": int(np.sum(side_a_outer)),
        "outer_side_b_pixels": int(np.sum(side_b_outer)),
        "inner_disk_pa_image_deg": pa_image_deg,
        "inner_axis_ratio_from_mom0": axis_ratio,
        "v_inner_side_a_pix": v_inner_a,
        "v_inner_side_b_pix": v_inner_b,
        "v_outer_side_a_pix": v_outer_a,
        "v_outer_side_b_pix": v_outer_b,
        "outer_ridge_offset_side_a_pix": offset_a,
        "outer_ridge_offset_side_b_pix": offset_b,
        "local_disk_reference_extent_pix": local_extent,
        "side_a_weight": side_a_weight,
        "side_b_weight": side_b_weight,
        "q_side_a": q_side_a,
        "q_side_b": q_side_b,
        "q_warp_first_pass": q_warp,
        "side_asymmetry_fraction": side_asymmetry_fraction,
        "endpoint_scores_allowed": False,
        "uses_vobs_or_residual": False,
        "measurement_status": "FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    geometry = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_geometry.csv").iloc[0]
    manifest = pd.read_csv(DATA / "ngc7331_things_hi_product_manifest.csv")
    mom0_manifest = manifest[manifest["product_id"].isin(["NA_MOM0", "RO_MOM0"])].copy()
    measurements = []
    for _, row in mom0_manifest.iterrows():
        measurements.append(
            measure_product(row["product_id"], Path(row["local_cache_path"]), geometry)
        )
    measurement_df = pd.DataFrame(measurements)

    q_values = measurement_df["q_warp_first_pass"].to_numpy(dtype=float)
    q_weights = measurement_df[["side_a_weight", "side_b_weight"]].mean(axis=1).to_numpy(dtype=float)
    q_first_pass = weighted_mean(q_values, q_weights)
    q_product_spread = float(np.max(q_values) - np.min(q_values))
    q_side_asymmetry = float(measurement_df["side_asymmetry_fraction"].max())
    q_uncertainty = max(0.5 * q_product_spread, 0.5 * abs(q_first_pass) * q_side_asymmetry)

    pa_values = measurement_df["inner_disk_pa_image_deg"].to_numpy(dtype=float)
    pa_mean = float(np.mean(pa_values))
    pa_spread = float(np.max(pa_values) - np.min(pa_values))

    response = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "response_id": "N7331_THINGS_QWARP_FIRST_PASS_RESPONSE_V1",
                "inner_disk_pa_image_deg_first_pass": pa_mean,
                "inner_disk_pa_product_spread_deg": pa_spread,
                "q_warp_first_pass": q_first_pass,
                "q_warp_uncertainty_first_pass": q_uncertainty,
                "side_asymmetry_fraction_max": q_side_asymmetry,
                "sigma_warp_sign": pd.NA,
                "epsilon_cross_bound_or_interval": pd.NA,
                "response_status": "FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_QWFP1_SOURCE_PRODUCTS",
                "gate_status": "PASS",
                "evidence": "NA_MOM0 and RO_MOM0 THINGS maps measured from local FITS cache",
                "remaining_obligation": "none at product availability level",
            },
            {
                "gate_id": "N7331_QWFP2_SOURCE_NATIVE_PA",
                "gate_status": "FIRST_PASS_REVIEW_REQUIRED",
                "evidence": f"inner PA image-frame mean={pa_mean:.6g} deg; product spread={pa_spread:.6g} deg",
                "remaining_obligation": "independent reviewer or literature PA profile must accept/reject orientation reference",
            },
            {
                "gate_id": "N7331_QWFP3_QWARP_MEASUREMENT",
                "gate_status": "FIRST_PASS_REVIEW_REQUIRED",
                "evidence": f"q_warp_first_pass={q_first_pass:.6g}; uncertainty={q_uncertainty:.6g}",
                "remaining_obligation": "review threshold, ridge definition, and product agreement before formula freeze",
            },
            {
                "gate_id": "N7331_QWFP4_SIGN_AND_CROSS_TERMS",
                "gate_status": "BLOCKED_REVIEW_REQUIRED",
                "evidence": "source-native q_warp candidate exists, but sigma sign and epsilon_cross remain unfilled",
                "remaining_obligation": "derive sign and cross-term bound from MOM1/context before exact transfer",
            },
            {
                "gate_id": "N7331_QWFP5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "script reads THINGS moment maps and geometry only; no vobs/residual/baseline columns",
                "remaining_obligation": "keep endpoint scoring in a separate script after freeze",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "qwarp_first_pass_status": "NGC7331_THINGS_QWARP_FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED",
                "n_products_measured": int(len(measurement_df)),
                "q_warp_first_pass": q_first_pass,
                "q_warp_uncertainty_first_pass": q_uncertainty,
                "inner_disk_pa_image_deg_first_pass": pa_mean,
                "sign_ready": False,
                "epsilon_cross_ready": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "independent review of PA/ridge threshold plus MOM1 sign and epsilon_cross extraction"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    measurement_df.to_csv(DATA / "ngc7331_things_qwarp_first_pass_measurements.csv", index=False)
    response.to_csv(DATA / "ngc7331_things_qwarp_first_pass_response.csv", index=False)
    gates.to_csv(DATA / "ngc7331_things_qwarp_first_pass_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_things_qwarp_first_pass_summary.csv", index=False)

    report = [
        "# NGC7331 THINGS q_warp First-Pass Measurement",
        "",
        "Status: `NGC7331_THINGS_QWARP_FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED`.",
        "",
        "This is a residual-blind source-native measurement candidate. It uses cached",
        "THINGS H I moment-0 products and the previously frozen scalar geometry only.",
        "It does not read observed rotation velocities, residuals, baseline scores, or",
        "best-fit readout-family information.",
        "",
        "The result is not an accepted formula input. The PA/ridge definition, sign rule,",
        "and epsilon_cross bound still require independent review before exact-transfer",
        "formula freeze or endpoint scoring.",
        "",
        "## Product measurements",
        "",
        markdown_table(measurement_df),
        "",
        "## First-pass response",
        "",
        markdown_table(response),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
    ]
    (REPORTS / "ngc7331_things_qwarp_first_pass_measurement.md").write_text(
        "\n".join(report), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
