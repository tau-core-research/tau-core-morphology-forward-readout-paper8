#!/usr/bin/env python3
"""Build a residual-blind preflight for sharper mixed-readout kernels.

The previous source-side gate showed that NGC5907 and NGC7331 separate in
source-observable space, while the replay/holdout endpoint showed that the
current two attenuation kernels remain too similar in endpoint controls.  This
script derives a source-native *preflight* kernel distinction without scoring a
rotation curve.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "mixed_kernel_sharpening_preflight_not_endpoint"


def smoothstep(x: np.ndarray) -> np.ndarray:
    clipped = np.clip(x, 0.0, 1.0)
    return clipped * clipped * (3.0 - 2.0 * clipped)


def normalize_profile(values: np.ndarray) -> np.ndarray:
    max_value = float(np.max(np.abs(values)))
    if max_value == 0.0:
        return values
    return values / max_value


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denom = float(np.linalg.norm(left) * np.linalg.norm(right))
    if denom == 0.0:
        return 0.0
    return float(np.dot(left, right) / denom)


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    separation = pd.read_csv(DATA / "mixed_kernel_observable_separation_summary.csv").iloc[0]
    if separation["gate_status"] != "SOURCE_KERNEL_OBSERVABLE_SEPARATION_PASS":
        raise RuntimeError("source-side kernel observable separation has not passed")

    ngc5907 = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_manifest.csv"
    ).iloc[0]
    ngc7331 = pd.read_csv(DATA / "ngc7331_fractional_onset_v2_replay_freeze_manifest.csv").iloc[
        0
    ]

    u = np.linspace(0.0, 1.0, 201)
    window = smoothstep(u)

    truncation_contrast = float(ngc5907["truncation_contrast"])
    projection_bound = float(ngc5907["pi_projection"])
    projection_edge_exponent = 1.0 + projection_bound + truncation_contrast

    old_projection = window * (1.0 + truncation_contrast * window) / (
        1.0 + truncation_contrast
    )
    sharp_projection = np.power(window, projection_edge_exponent) * (
        1.0 + truncation_contrast * window
    ) / (1.0 + truncation_contrast)

    r_inner = float(ngc7331["r_window_inner_kpc"])
    r_outer = float(ngc7331["r_window_outer_kpc"])
    r = r_inner + u * (r_outer - r_inner)
    projected_hwhm_over_rs = float(ngc7331["projected_hwhm_over_Rs"])
    onset_over_rhi = float(ngc7331["fractional_warp_onset_over_RHI"])
    vertical_activation = float(ngc7331["vertical_activation_candidate"])
    projected_thickness_norm = min(1.0, projected_hwhm_over_rs / 0.25)
    vertical_decay = 1.0 + onset_over_rhi + vertical_activation

    old_vow = window * (0.5 / (1.0 + r / max(r_inner, 1.0e-9)) + 0.5 * projected_hwhm_over_rs)
    sharp_vow = window * np.exp(-vertical_decay * u) + projected_thickness_norm * window * (
        1.0 - window
    )

    old_projection = normalize_profile(old_projection)
    old_vow = normalize_profile(old_vow)
    sharp_projection = normalize_profile(sharp_projection)
    sharp_vow = normalize_profile(sharp_vow)

    profile = pd.DataFrame(
        {
            "u_active_window": u,
            "K_projection_current_normalized": old_projection,
            "K_vertical_outer_warp_current_normalized": old_vow,
            "K_projection_source_sharpened_normalized": sharp_projection,
            "K_vertical_outer_warp_source_sharpened_normalized": sharp_vow,
            "uses_vobs_or_residual": False,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    formulas = pd.DataFrame(
        [
            {
                "formula_label": "K_projection_source_sharpened",
                "source_lane": "NGC5907 projection/truncation dominated mixed lane",
                "kernel_formula": (
                    "K_proj_sharp(u)=S(u)^(1+Pi_projection+C_trunc) "
                    "*(1+C_trunc*S(u))/(1+C_trunc)"
                ),
                "source_parameters": (
                    f"Pi_projection={projection_bound:.6g}; "
                    f"C_trunc={truncation_contrast:.6g}"
                ),
                "dimension_check": "PASS: u, S(u), Pi_projection, and C_trunc are dimensionless",
                "known_limit_check": (
                    "Pi_projection=0 and C_trunc=0 recovers a simple active-window kernel; "
                    "inactive window gives K=0"
                ),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "formula_label": "K_vertical_outer_warp_source_sharpened",
                "source_lane": "NGC7331 V2 fractional-onset vertical/outer-warp mixed lane",
                "kernel_formula": (
                    "K_vow_sharp(u)=S(u)*exp(-(1+R_onset/R_HI+A_vertical)u) "
                    "+ T_projected*S(u)*(1-S(u))"
                ),
                "source_parameters": (
                    f"R_onset/R_HI={onset_over_rhi:.6g}; "
                    f"A_vertical={vertical_activation:.6g}; "
                    f"T_projected={projected_thickness_norm:.6g}"
                ),
                "dimension_check": (
                    "PASS: u, S(u), R_onset/R_HI, A_vertical, and T_projected are dimensionless"
                ),
                "known_limit_check": (
                    "absent fractional onset or absent vertical activation blocks this lane; "
                    "inactive window gives K=0"
                ),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    current_cross = cosine_similarity(old_projection, old_vow)
    sharpened_cross = cosine_similarity(sharp_projection, sharp_vow)
    separation_gain = current_cross - sharpened_cross
    summary = pd.DataFrame(
        [
            {
                "preflight_status": (
                    "SOURCE_KERNEL_SHARPENING_PREFLIGHT_READY_NOT_ENDPOINT"
                    if separation_gain > 0.2
                    else "SOURCE_KERNEL_SHARPENING_PREFLIGHT_INSUFFICIENT"
                ),
                "diagnostic_status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
                "current_kernel_cross_similarity": current_cross,
                "source_sharpened_kernel_cross_similarity": sharpened_cross,
                "kernel_shape_separation_gain": separation_gain,
                "projection_edge_exponent": projection_edge_exponent,
                "vertical_decay": vertical_decay,
                "projected_thickness_norm": projected_thickness_norm,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "endpoint_score_inputs_read": False,
                "dimension_check": "PASS: all sharpened kernel arguments and coefficients are dimensionless",
                "known_limit_check": "PASS: inactive source windows recover zero correction; carrier recovery remains available at gamma=0",
                "next_obligation": (
                    "freeze V2/V3 manifests with these source-sharpened kernels before any "
                    "new replay/holdout endpoint score"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    profile.to_csv(DATA / "mixed_kernel_sharpening_preflight_profiles.csv", index=False)
    formulas.to_csv(DATA / "mixed_kernel_sharpening_preflight_formulas.csv", index=False)
    summary.to_csv(DATA / "mixed_kernel_sharpening_preflight_summary.csv", index=False)

    report = [
        "# Mixed Kernel Sharpening Preflight",
        "",
        "Status label: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`.",
        "",
        "This is a source-side formula-shape preflight. It does not score",
        "rotation curves and does not modify accepted endpoint rows. It follows",
        "from the source-observable separation gate: the fresh NGC5907 and",
        "NGC7331 lanes separate in source-observable space, but their current",
        "attenuation kernels are too similar for strict replay/holdout",
        "specificity.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source-Sharpened Formula Shells",
        "",
        markdown_table(formulas),
        "",
        "## Profile Grid",
        "",
        markdown_table(profile.head(12)),
        "",
        "## Interpretation",
        "",
        "The current normalized projection and vertical/outer-warp kernels have",
        f"cross-similarity {current_cross:.6g}. The source-sharpened preflight",
        f"reduces that to {sharpened_cross:.6g}, a separation gain of",
        f" {separation_gain:.6g}. This is not a fit improvement claim. It is a",
        "formula-shape obligation: future V2/V3 replay manifests should freeze",
        "source-sharpened kernels before scoring, then rerun the same",
        "wrong-label and shuffled-label replay/holdout controls.",
        "",
        "## Claim Boundary",
        "",
        "No observed velocity, residual, RMSE, or endpoint rank is read by this",
        "gate. The result is a residual-blind kernel-design preflight, not an",
        "endpoint result and not empirical validation.",
        "",
    ]
    (REPORTS / "mixed_kernel_sharpening_preflight.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
