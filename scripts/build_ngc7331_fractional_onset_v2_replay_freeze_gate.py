#!/usr/bin/env python3
"""Freeze the NGC7331 fractional-onset V2 replay protocol.

This gate turns the source-only fractional warp-onset result into an executable
V2 formula manifest, but does not score it.  It preserves the Paper 8 endpoint
boundary: the already scored NGC7331 V1 row remains the accepted caveated
endpoint, while this V2 row is replay/holdout-only until a separate predeclared
replay gate is run.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc7331_fractional_onset_v2_replay_freeze_not_score"


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

    v1 = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_manifest.csv"
    ).iloc[0]
    onset = pd.read_csv(DATA / "ngc7331_fractional_warp_onset_source_summary.csv").iloc[0]

    onset_ready = (
        str(onset["source_gate_status"])
        == "FRACTIONAL_WARP_ONSET_SOURCE_READY_REPLAY_REQUIRED"
    )
    replay_required = bool(onset["replay_or_holdout_required"])
    uses_vobs = bool(onset["uses_vobs_or_residual_in_construction"])
    formula_update_current_allowed = bool(onset["formula_update_allowed_for_current_endpoint"])
    v2_inner = float(onset["candidate_v2_window_inner_kpc"])
    v2_outer = float(onset["candidate_v2_window_outer_kpc"])
    v1_inner = float(v1["r_window_inner_kpc"])
    v1_outer = float(v1["r_window_outer_kpc"])

    manifest = v1.copy()
    manifest["formula_id"] = "NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1"
    manifest["parent_formula_id"] = str(v1["formula_id"])
    manifest["formula_version"] = "V2_REPLAY_FRACTIONAL_ONSET"
    manifest["kernel_text"] = (
        "K_vow_v2(R)=W_outer(R;R_onset_frac,R_HI)*"
        "(0.5/(1+R/R_s)+0.5*projected_hwhm_over_Rs)"
    )
    manifest["overlay_selection_rule"] = (
        "accepted_vertical_scale_fields_plus_Bosma_fractional_Holmberg_warp_onset"
    )
    manifest["r_window_inner_kpc"] = v2_inner
    manifest["r_window_outer_kpc"] = v2_outer
    manifest["v1_broad_window_inner_kpc"] = v1_inner
    manifest["v1_broad_window_outer_kpc"] = v1_outer
    manifest["fractional_onset_source_status"] = str(onset["source_gate_status"])
    manifest["fractional_warp_onset_arcmin"] = float(onset["approx_warp_onset_arcmin"])
    manifest["fractional_warp_onset_kpc"] = v2_inner
    manifest["fractional_warp_onset_over_Rdisk"] = float(
        onset["approx_warp_onset_over_Rdisk"]
    )
    manifest["fractional_warp_onset_over_RHI"] = float(onset["approx_warp_onset_over_RHI"])
    manifest["outer_warp_numeric_onset_available"] = True
    manifest["caveat_status"] = "V2_REPLAY_FRACTIONAL_ONSET_SOURCE_READY_NOT_SCORED"
    manifest["dimension_check"] = (
        "PASS: gamma_vow and K_vow_v2 are dimensionless; correction has velocity-squared units"
    )
    manifest["inactive_window_limit"] = "W_outer=0 before V2 onset implies v_mix=v_K_exponential_disk"
    manifest["formula_frozen_before_replay_scoring"] = True
    manifest["formula_update_allowed_for_current_endpoint"] = formula_update_current_allowed
    manifest["replay_or_holdout_required"] = replay_required
    manifest["v2_replay_scores_allowed_by_this_gate"] = False
    manifest["current_v1_endpoint_scores_allowed_by_this_gate"] = False
    manifest["uses_vobs_or_residual_in_construction"] = uses_vobs
    manifest["claim_boundary"] = CLAIM_BOUNDARY
    manifest = manifest.to_frame().T

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_V2G1_SOURCE_ONSET_READY",
                "gate_status": "PASS" if onset_ready else "BLOCKED",
                "evidence": str(onset["source_gate_status"]),
                "remaining_obligation": "none at V2 source-onset freeze level",
            },
            {
                "gate_id": "N7331_V2G2_WINDOW_REPLACEMENT_DEFINED",
                "gate_status": "PASS",
                "evidence": f"V1 window {v1_inner:.6g}->{v1_outer:.6g} kpc; V2 replay window {v2_inner:.6g}->{v2_outer:.6g} kpc",
                "remaining_obligation": "do not apply V2 window to the already scored V1 endpoint",
            },
            {
                "gate_id": "N7331_V2G3_DIMENSION_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "dimensionless window/kernel times velocity-squared carrier",
                "remaining_obligation": "none at formula-shell level",
            },
            {
                "gate_id": "N7331_V2G4_ENDPOINT_BLINDNESS",
                "gate_status": "PASS" if not uses_vobs else "BLOCKED",
                "evidence": "uses V1 source manifest and fractional-onset source gate only",
                "remaining_obligation": "replay scoring must remain a separate script",
            },
            {
                "gate_id": "N7331_V2G5_REPLAY_REQUIRED",
                "gate_status": "BLOCKED_REPLAY_REQUIRED" if replay_required else "PASS",
                "evidence": "V2 source onset was introduced after the V1 endpoint score",
                "remaining_obligation": "predeclare replay/holdout scoring before reading V2 endpoint RMSE",
            },
            {
                "gate_id": "N7331_V2G6_NO_RETROACTIVE_ENDPOINT_UPDATE",
                "gate_status": "PASS",
                "evidence": f"formula_update_allowed_for_current_endpoint={formula_update_current_allowed}",
                "remaining_obligation": "V1 accepted endpoint remains unchanged",
            },
        ]
    )
    gates["galaxy"] = "NGC7331"
    gates["formula_id"] = "NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1"
    gates["uses_vobs_or_residual"] = uses_vobs
    gates["v2_replay_scores_allowed_by_this_gate"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "formula_id",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "v2_replay_scores_allowed_by_this_gate",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC7331",
                "formula_id": "NGC7331_FRACTIONAL_ONSET_V2_REPLAY_FREEZE_V1",
                "v2_replay_freeze_status": "V2_REPLAY_PROTOCOL_READY_NOT_SCORED",
                "parent_v1_formula_id": str(v1["formula_id"]),
                "v1_window_inner_kpc": v1_inner,
                "v1_window_outer_kpc": v1_outer,
                "v2_window_inner_kpc": v2_inner,
                "v2_window_outer_kpc": v2_outer,
                "fractional_warp_onset_over_Rdisk": float(
                    onset["approx_warp_onset_over_Rdisk"]
                ),
                "fractional_warp_onset_over_RHI": float(onset["approx_warp_onset_over_RHI"]),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_replay_blocked": int(gates["gate_status"].eq("BLOCKED_REPLAY_REQUIRED").sum()),
                "uses_vobs_or_residual_in_construction": uses_vobs,
                "formula_update_allowed_for_current_endpoint": formula_update_current_allowed,
                "v2_replay_scores_allowed_by_this_gate": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ngc7331_fractional_onset_v2_replay_freeze_manifest.csv", index=False)
    gates.to_csv(DATA / "ngc7331_fractional_onset_v2_replay_freeze_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_fractional_onset_v2_replay_freeze_summary.csv", index=False)

    report = [
        "# NGC7331 Fractional-Onset V2 Replay Freeze Gate",
        "",
        "This gate freezes a V2 replay protocol from the fractional warp-onset source",
        "gate. It does not score the rotation curve and it does not update the",
        "already scored NGC7331 V1 accepted endpoint.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## V2 Frozen Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The V2 formula is replay/holdout-ready but not endpoint-scored. The current",
        "NGC7331 V1 score remains the caveated accepted endpoint. Any V2 score must",
        "come from a separate predeclared replay or holdout script.",
        "",
    ]
    (REPORTS / "ngc7331_fractional_onset_v2_replay_freeze_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
