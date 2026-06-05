#!/usr/bin/env python3
"""Narrow NGC4183 from broad mixed-overlay to a source-supported label.

The gate does not freeze a formula and does not allow endpoint scoring.  It
only decides whether the residual-blind source observables support replacing
the broad mixed label with a narrower projection/outer-warp label for the next
formula-derivation step.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_projection_outer_warp_label_gate_not_endpoint"
GALAXY = "NGC4183"


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


def get_observable(observables: pd.DataFrame, observable_id: str) -> pd.Series:
    return observables.loc[observables["observable_id"].eq(observable_id)].iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    obs = pd.read_csv(DATA / "ngc4183_mixed_overlay_observable_sheet.csv")
    obs_summary = pd.read_csv(DATA / "ngc4183_mixed_overlay_observable_sheet_summary.csv").iloc[0]
    worklist = pd.read_csv(DATA / "mixed_overlay_future_protocol_worklist.csv")
    worklist_row = worklist.loc[worklist["galaxy"].eq(GALAXY)].iloc[0]

    p_edge = float(get_observable(obs, "projection_edge_on_strength_p_edge")["value"])
    rhi_diff = float(get_observable(obs, "R_HI_source_vs_SPARC_relative_difference")["value"])
    outer_warp_status = str(get_observable(obs, "outer_warp_flag")["status"])
    warp_kernel_status = str(get_observable(obs, "warp_onset_or_amplitude")["status"])
    broad_overlay_status = str(get_observable(obs, "bar_core_history_overlay")["status"])

    source_evidence = pd.DataFrame(
        [
            {
                "evidence_id": "E1_EDGE_ON_PROJECTION",
                "evidence_status": "SUPPORTS_NARROW_LABEL",
                "value": p_edge,
                "threshold_or_reason": "p_edge > 0.95",
                "interpretation": "edge-on projection observable is strong enough for projection-overlay derivation",
            },
            {
                "evidence_id": "E2_RHI_DENOMINATOR_CONSISTENCY",
                "evidence_status": "SUPPORTS_NARROW_LABEL",
                "value": rhi_diff,
                "threshold_or_reason": "relative difference < 0.02",
                "interpretation": "source-native H I diameter and SPARC RHI agree as support scale",
            },
            {
                "evidence_id": "E3_OUTER_WARP_CONTEXT",
                "evidence_status": "SUPPORTS_CAVEATED_LABEL_ONLY",
                "value": outer_warp_status,
                "threshold_or_reason": "qualitative source note only",
                "interpretation": "outer-warp context can name the caveat but cannot freeze a numeric ramp",
            },
            {
                "evidence_id": "E4_NUMERIC_WARP_KERNEL",
                "evidence_status": "BLOCKS_WARP_RAMP_FREEZE",
                "value": warp_kernel_status,
                "threshold_or_reason": "no onset/amplitude",
                "interpretation": "do not use standalone warp-ramp or added-source formula yet",
            },
            {
                "evidence_id": "E5_BROAD_BAR_CORE_HISTORY",
                "evidence_status": "REJECTS_BROAD_LABEL_FOR_NOW",
                "value": broad_overlay_status,
                "threshold_or_reason": "required field missing",
                "interpretation": "broad proposed label is too specific for available source evidence",
            },
        ]
    )

    proposed = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "previous_candidate_readout": str(worklist_row["candidate_readout"]),
                "replacement_candidate_readout": "K_expdisk_edge_on_projection_outer_warp_caveated",
                "replacement_lane": "L_projection_attenuation_with_outer_warp_caveat",
                "label_gate_status": "NARROW_REPLACEMENT_LABEL_SUPPORTED_FOR_FORMULA_DERIVATION_NOT_ENDPOINT",
                "formula_derivation_allowed": True,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_selection": False,
                "why_narrowed": (
                    "source supports high-inclination projection plus qualitative outer warp; "
                    "bar/core/history overlay fields remain missing"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_LABEL_G1_NO_RESIDUAL_SELECTION",
                "gate_status": "PASS",
                "evidence": "label gate reads observable sheet only",
                "remaining_obligation": "separate endpoint script may read vobs only after freeze",
            },
            {
                "gate_id": "N4183_LABEL_G2_BROAD_LABEL_REJECTED",
                "gate_status": "PASS",
                "evidence": "bar/core/history overlay observables missing",
                "remaining_obligation": "do not score broad label",
            },
            {
                "gate_id": "N4183_LABEL_G3_NARROW_LABEL_SUPPORTED",
                "gate_status": "PASS_CAVEATED",
                "evidence": "p_edge=0.985 and RHI denominator consistency plus qualitative outer warp",
                "remaining_obligation": "derive projection attenuation formula shell and coefficient rule",
            },
            {
                "gate_id": "N4183_LABEL_G4_ENDPOINT_ALLOWED",
                "gate_status": "BLOCKED",
                "evidence": "no frozen formula yet",
                "remaining_obligation": "formula derivation and source-side formula freeze",
            },
        ]
    )
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "label_gate_status": str(proposed.iloc[0]["label_gate_status"]),
                "galaxy": GALAXY,
                "replacement_candidate_readout": str(proposed.iloc[0]["replacement_candidate_readout"]),
                "replacement_lane": str(proposed.iloc[0]["replacement_lane"]),
                "formula_derivation_allowed": True,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "p_edge": p_edge,
                "rhi_relative_difference": rhi_diff,
                "observable_sheet_status": str(obs_summary["observable_sheet_status"]),
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "derive_projection_attenuation_outer_warp_caveated_formula_shell",
            }
        ]
    )

    source_evidence.to_csv(DATA / "ngc4183_projection_outer_warp_label_evidence.csv", index=False)
    proposed.to_csv(DATA / "ngc4183_projection_outer_warp_label_gate.csv", index=False)
    gates.to_csv(DATA / "ngc4183_projection_outer_warp_label_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_projection_outer_warp_label_summary.csv", index=False)

    report = f"""# NGC4183 Projection/Outer-Warp Label Gate

Status: `{summary.iloc[0]["label_gate_status"]}`

This is a label-narrowing gate.  It does not freeze a formula and does not
authorize endpoint scoring.

## Summary

{markdown_table(summary)}

## Source Evidence

{markdown_table(source_evidence)}

## Proposed Replacement

{markdown_table(proposed)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Verdict

The broad `K_expdisk_bar_core_projection_history_overlay_review` label is too
strong for the available NGC4183 source evidence.  A narrower
`K_expdisk_edge_on_projection_outer_warp_caveated` label is supported for
formula derivation because the galaxy has a strong edge-on projection observable
and a source-native H I support scale that agrees with SPARC.  The qualitative
outer-warp statement is a caveat, not a numeric warp ramp.  Endpoint scoring
remains blocked until a dimensionally checked projection formula is frozen
without using residuals.
"""
    (REPORTS / "ngc4183_projection_outer_warp_label_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
