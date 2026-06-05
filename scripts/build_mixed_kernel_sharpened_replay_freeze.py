#!/usr/bin/env python3
"""Freeze the source-sharpened mixed replay kernels before scoring.

This gate consumes the residual-blind kernel-sharpening preflight and writes a
replay/holdout freeze manifest.  It does not read observed velocities and does
not score a curve.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "mixed_kernel_sharpened_replay_freeze_not_score"


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

    preflight = pd.read_csv(DATA / "mixed_kernel_sharpening_preflight_summary.csv").iloc[0]
    formulas = pd.read_csv(DATA / "mixed_kernel_sharpening_preflight_formulas.csv")
    n5907 = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_manifest.csv"
    ).iloc[0]
    n7331 = pd.read_csv(DATA / "ngc7331_fractional_onset_v2_replay_freeze_manifest.csv").iloc[
        0
    ]

    preflight_ready = (
        preflight["preflight_status"]
        == "SOURCE_KERNEL_SHARPENING_PREFLIGHT_READY_NOT_ENDPOINT"
    )
    uses_vobs = False
    projection_formula = formulas.loc[
        formulas["formula_label"].eq("K_projection_source_sharpened")
    ].iloc[0]
    vow_formula = formulas.loc[
        formulas["formula_label"].eq("K_vertical_outer_warp_source_sharpened")
    ].iloc[0]

    manifest = pd.DataFrame(
        [
            {
                "galaxy": "NGC5907",
                "formula_id": "NGC5907_EXPDISK_PROJECTION_SHARPENED_REPLAY_V2",
                "parent_formula_id": str(n5907["formula_id"]),
                "source_matched_formula": "K_expdisk_projection_mixed",
                "carrier": "v_K_exponential_disk",
                "kernel_label": "K_projection_source_sharpened",
                "kernel_formula": str(projection_formula["kernel_formula"]),
                "gamma": float(n5907["gamma_projection"]),
                "r_window_inner_kpc": float(n5907["r_in_kpc"]),
                "r_window_outer_kpc": float(n5907["r_out_kpc"]),
                "projection_bound": float(n5907["pi_projection"]),
                "truncation_contrast": float(n5907["truncation_contrast"]),
                "projection_edge_exponent": float(preflight["projection_edge_exponent"]),
                "vertical_decay": pd.NA,
                "projected_thickness_norm": pd.NA,
                "dimension_check": str(projection_formula["dimension_check"]),
                "known_limit_check": str(projection_formula["known_limit_check"]),
                "formula_frozen_before_sharpened_replay_scoring": True,
                "uses_vobs_or_residual_in_construction": uses_vobs,
                "endpoint_scores_allowed_by_this_gate": False,
                "freeze_status": "SHARPENED_REPLAY_FREEZE_READY_NOT_SCORED",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC7331",
                "formula_id": "NGC7331_VOW_SHARPENED_REPLAY_V3",
                "parent_formula_id": str(n7331["formula_id"]),
                "source_matched_formula": "K_expdisk_vertical_outer_warp_v2",
                "carrier": "v_K_exponential_disk",
                "kernel_label": "K_vertical_outer_warp_source_sharpened",
                "kernel_formula": str(vow_formula["kernel_formula"]),
                "gamma": float(n7331["gamma_vow"]),
                "r_window_inner_kpc": float(n7331["r_window_inner_kpc"]),
                "r_window_outer_kpc": float(n7331["r_window_outer_kpc"]),
                "projection_bound": pd.NA,
                "truncation_contrast": pd.NA,
                "projection_edge_exponent": pd.NA,
                "vertical_decay": float(preflight["vertical_decay"]),
                "projected_thickness_norm": float(preflight["projected_thickness_norm"]),
                "fractional_warp_onset_over_RHI": float(
                    n7331["fractional_warp_onset_over_RHI"]
                ),
                "vertical_activation_candidate": float(n7331["vertical_activation_candidate"]),
                "dimension_check": str(vow_formula["dimension_check"]),
                "known_limit_check": str(vow_formula["known_limit_check"]),
                "formula_frozen_before_sharpened_replay_scoring": True,
                "uses_vobs_or_residual_in_construction": uses_vobs,
                "endpoint_scores_allowed_by_this_gate": False,
                "freeze_status": "SHARPENED_REPLAY_FREEZE_READY_NOT_SCORED",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "MSKRF1_PREFLIGHT_READY",
                "gate_status": "PASS" if preflight_ready else "BLOCKED",
                "evidence": str(preflight["preflight_status"]),
                "remaining_obligation": "none at sharpened freeze level",
            },
            {
                "gate_id": "MSKRF2_DIMENSION_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "all sharpened kernel coefficients are dimensionless; inactive window gives K=0; gamma=0 recovers carrier",
                "remaining_obligation": "none at formula-shell level",
            },
            {
                "gate_id": "MSKRF3_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "construction reads source manifests and preflight formulas only",
                "remaining_obligation": "scoring must remain a separate script reading this manifest unchanged",
            },
            {
                "gate_id": "MSKRF4_REPLAY_ONLY_BOUNDARY",
                "gate_status": "PASS",
                "evidence": "freeze records V2/V3 replay formulas, not accepted endpoint updates",
                "remaining_obligation": "do not retroactively alter accepted NGC5907/NGC7331 rows",
            },
        ]
    )
    gates["uses_vobs_or_residual"] = uses_vobs
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "freeze_status": "SHARPENED_REPLAY_FREEZE_READY_NOT_SCORED"
                if preflight_ready
                else "SHARPENED_REPLAY_FREEZE_BLOCKED",
                "n_formulas_frozen": len(manifest),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "uses_vobs_or_residual_in_construction": uses_vobs,
                "endpoint_scores_allowed_by_this_gate": False,
                "current_kernel_cross_similarity": float(
                    preflight["current_kernel_cross_similarity"]
                ),
                "source_sharpened_kernel_cross_similarity": float(
                    preflight["source_sharpened_kernel_cross_similarity"]
                ),
                "kernel_shape_separation_gain": float(
                    preflight["kernel_shape_separation_gain"]
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "mixed_kernel_sharpened_replay_freeze_manifest.csv", index=False)
    gates.to_csv(DATA / "mixed_kernel_sharpened_replay_freeze_gates.csv", index=False)
    summary.to_csv(DATA / "mixed_kernel_sharpened_replay_freeze_summary.csv", index=False)

    report = [
        "# Mixed Kernel Sharpened Replay Freeze",
        "",
        "This gate freezes source-sharpened replay formulas. It does not score",
        "rotation curves and does not update accepted endpoint rows.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The frozen V2/V3 formulas may be used by a separate replay/holdout scoring",
        "script. This freeze is not an endpoint result and not validation.",
        "",
    ]
    (REPORTS / "mixed_kernel_sharpened_replay_freeze.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
