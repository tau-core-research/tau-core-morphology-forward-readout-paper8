#!/usr/bin/env python3
"""Audit NGC7331 q_warp sensitivity to source-native measurement choices.

The goal is to decide whether the THINGS first-pass q_warp is robust enough
to become a formula-freeze input. This remains residual-blind and endpoint
blocked: the script reads moment-0 maps and geometry only.
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
CLAIM_BOUNDARY = "ngc7331_things_qwarp_measurement_sensitivity_audit_not_endpoint"


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


def read_image(path: Path) -> np.ndarray:
    return np.squeeze(np.asarray(fits.getdata(path), dtype=float))


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    total = float(np.sum(weights))
    if total <= 0:
        return math.nan
    return float(np.sum(values * weights) / total)


def weighted_quantile(values: np.ndarray, weights: np.ndarray, quantile: float) -> float:
    order = np.argsort(values)
    values_sorted = values[order]
    weights_sorted = weights[order]
    cumulative = np.cumsum(weights_sorted)
    if float(cumulative[-1]) <= 0:
        return math.nan
    cutoff = quantile * cumulative[-1]
    return float(values_sorted[np.searchsorted(cumulative, cutoff, side="left")])


def principal_axis(x: np.ndarray, y: np.ndarray, weights: np.ndarray) -> np.ndarray:
    x0 = weighted_mean(x, weights)
    y0 = weighted_mean(y, weights)
    dx = x - x0
    dy = y - y0
    total = float(np.sum(weights))
    cov = np.array(
        [
            [float(np.sum(weights * dx * dx) / total), float(np.sum(weights * dx * dy) / total)],
            [float(np.sum(weights * dx * dy) / total), float(np.sum(weights * dy * dy) / total)],
        ]
    )
    eigvals, eigvecs = np.linalg.eigh(cov)
    major = eigvecs[:, int(np.argmax(eigvals))]
    if major[0] < 0:
        major = -major
    return major


def measure(image: np.ndarray, geometry: pd.Series, threshold_fraction: float) -> dict[str, float]:
    y_idx, x_idx = np.indices(image.shape)
    x = x_idx.astype(float) - (float(geometry["crpix1"]) - 1.0)
    y = y_idx.astype(float) - (float(geometry["crpix2"]) - 1.0)
    r_circular = np.hypot(x, y)
    positive = np.where(np.isfinite(image), np.maximum(image, 0.0), 0.0)
    positive_values = positive[positive > 0]
    p95 = float(np.percentile(positive_values, 95))
    signal = positive >= threshold_fraction * p95
    warp_onset_pix = float(geometry["warp_onset_pix"])
    rhi_pix = float(geometry["rhi_pix"])
    inner_mask = signal & (r_circular <= warp_onset_pix)
    if int(np.sum(inner_mask)) < 100:
        inner_mask = signal & (r_circular <= 1.25 * warp_onset_pix)
    major = principal_axis(x[inner_mask], y[inner_mask], positive[inner_mask])
    minor = np.array([-major[1], major[0]])
    u = x * major[0] + y * major[1]
    v = x * minor[0] + y * minor[1]
    local_extent = max(rhi_pix - warp_onset_pix, 1.0)

    inner_reference = signal & (np.abs(u) >= 0.50 * warp_onset_pix) & (
        np.abs(u) <= warp_onset_pix
    )
    outer = signal & (np.abs(u) >= warp_onset_pix) & (np.abs(u) <= rhi_pix)
    q_centroid_sides = []
    q_envelope_sides = []
    side_weights = []
    for side_sign in [1, -1]:
        side_inner = inner_reference & ((side_sign * u) > 0)
        side_outer = outer & ((side_sign * u) > 0)
        v_inner = weighted_mean(v[side_inner], positive[side_inner])
        v_outer = weighted_mean(v[side_outer], positive[side_outer])
        q_centroid_sides.append(abs(v_outer - v_inner) / local_extent)
        outer_abs = np.abs(v[side_outer] - v_inner)
        q_envelope_sides.append(
            weighted_quantile(outer_abs, positive[side_outer], 0.80) / local_extent
        )
        side_weights.append(float(np.sum(positive[side_outer])))

    side_weights_np = np.asarray(side_weights, dtype=float)
    if float(np.sum(side_weights_np)) > 0:
        side_weights_np = side_weights_np / float(np.sum(side_weights_np))
    else:
        side_weights_np = np.array([0.5, 0.5])
    return {
        "q_centroid": float(np.sum(np.asarray(q_centroid_sides) * side_weights_np)),
        "q_envelope_p80": float(np.sum(np.asarray(q_envelope_sides) * side_weights_np)),
        "q_centroid_side_asymmetry": abs(q_centroid_sides[0] - q_centroid_sides[1])
        / max(float(np.mean(q_centroid_sides)), 1.0e-12),
        "q_envelope_side_asymmetry": abs(q_envelope_sides[0] - q_envelope_sides[1])
        / max(float(np.mean(q_envelope_sides)), 1.0e-12),
        "n_signal_pixels": int(np.sum(signal)),
        "n_outer_pixels": int(np.sum(outer)),
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    geometry = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_geometry.csv").iloc[0]
    manifest = pd.read_csv(DATA / "ngc7331_things_hi_product_manifest.csv")
    mom0 = manifest[manifest["product_id"].isin(["NA_MOM0", "RO_MOM0"])]
    threshold_fractions = [0.10, 0.15, 0.20, 0.25, 0.30]

    rows = []
    for _, product in mom0.iterrows():
        image = read_image(Path(product["local_cache_path"]))
        for threshold_fraction in threshold_fractions:
            measured = measure(image, geometry, threshold_fraction)
            measured.update(
                {
                    "galaxy": GALAXY,
                    "product_id": product["product_id"],
                    "threshold_fraction_of_p95": threshold_fraction,
                    "endpoint_scores_allowed": False,
                    "uses_vobs_or_residual": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            rows.append(measured)
    sensitivity = pd.DataFrame(rows)

    aggregate = (
        sensitivity.groupby("threshold_fraction_of_p95", as_index=False)
        .agg(
            q_centroid_mean=("q_centroid", "mean"),
            q_centroid_spread=("q_centroid", lambda x: float(np.max(x) - np.min(x))),
            q_envelope_p80_mean=("q_envelope_p80", "mean"),
            q_envelope_p80_spread=("q_envelope_p80", lambda x: float(np.max(x) - np.min(x))),
            q_centroid_side_asymmetry_max=("q_centroid_side_asymmetry", "max"),
            q_envelope_side_asymmetry_max=("q_envelope_side_asymmetry", "max"),
        )
    )
    aggregate["galaxy"] = GALAXY
    aggregate["endpoint_scores_allowed"] = False
    aggregate["uses_vobs_or_residual"] = False
    aggregate["claim_boundary"] = CLAIM_BOUNDARY
    aggregate = aggregate[
        [
            "galaxy",
            "threshold_fraction_of_p95",
            "q_centroid_mean",
            "q_centroid_spread",
            "q_envelope_p80_mean",
            "q_envelope_p80_spread",
            "q_centroid_side_asymmetry_max",
            "q_envelope_side_asymmetry_max",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    centroid_range = (
        float(aggregate["q_centroid_mean"].min()),
        float(aggregate["q_centroid_mean"].max()),
    )
    envelope_range = (
        float(aggregate["q_envelope_p80_mean"].min()),
        float(aggregate["q_envelope_p80_mean"].max()),
    )
    conclusion = (
        "CENTROID_STABLE_BUT_ENVELOPE_STRONGER_REVIEW_REQUIRED"
        if envelope_range[0] > 2.0 * centroid_range[1]
        else "QWARP_SENSITIVITY_REVIEW_REQUIRED"
    )
    gates = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "gate_id": "N7331_QWS1_CENTROID_STABILITY",
                "gate_status": "REVIEW_REQUIRED",
                "evidence": f"centroid q range={centroid_range[0]:.6g}..{centroid_range[1]:.6g}",
                "remaining_obligation": "choose whether centroid or envelope observable is the correct q_warp carrier",
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": GALAXY,
                "gate_id": "N7331_QWS2_ENVELOPE_STRENGTH",
                "gate_status": "REVIEW_REQUIRED",
                "evidence": f"envelope p80 q range={envelope_range[0]:.6g}..{envelope_range[1]:.6g}",
                "remaining_obligation": "review whether warp/readout strength should track ridge centroid or outer envelope",
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": GALAXY,
                "gate_id": "N7331_QWS3_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "sensitivity audit reads THINGS moment-0 maps and geometry only",
                "remaining_obligation": "none at endpoint-blindness level",
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "sensitivity_status": conclusion,
                "q_centroid_mean_min": centroid_range[0],
                "q_centroid_mean_max": centroid_range[1],
                "q_envelope_p80_mean_min": envelope_range[0],
                "q_envelope_p80_mean_max": envelope_range[1],
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "freeze a source-native q_warp observable definition after independent review"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    sensitivity.to_csv(DATA / "ngc7331_things_qwarp_measurement_sensitivity.csv", index=False)
    aggregate.to_csv(
        DATA / "ngc7331_things_qwarp_measurement_sensitivity_aggregate.csv", index=False
    )
    gates.to_csv(DATA / "ngc7331_things_qwarp_measurement_sensitivity_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_things_qwarp_measurement_sensitivity_summary.csv", index=False)

    report = [
        "# NGC7331 THINGS q_warp Measurement Sensitivity Audit",
        "",
        f"Status: `{conclusion}`.",
        "",
        "This audit compares a conservative centroid q_warp observable with an",
        "outer-envelope p80 observable across fixed moment-0 signal thresholds.",
        "It is residual-blind and endpoint-blocked.",
        "",
        "The purpose is to decide which source-native observable should be frozen",
        "before any exact-transfer formula or endpoint score is allowed.",
        "",
        "## Aggregate sensitivity",
        "",
        markdown_table(aggregate),
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
    (REPORTS / "ngc7331_things_qwarp_measurement_sensitivity_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
