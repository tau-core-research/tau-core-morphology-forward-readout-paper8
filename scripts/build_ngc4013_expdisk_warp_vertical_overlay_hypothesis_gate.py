#!/usr/bin/env python3
"""Build the NGC4013 exponential-disk + warp/vertical-overlay hypothesis gate.

This gate records a follow-up mixed-readout hypothesis after the NGC4013
wrong-family audit. Because the mixed carrier is motivated partly by endpoint
scores, the first run is diagnostic-only and cannot be promoted as an accepted
endpoint without a new residual-blind source-label rule.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint"


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

    source = pd.read_csv(DATA / "ngc4013_compact_overlay_source_summary.csv").iloc[0]
    label = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_replacement_label_summary.csv").iloc[0]
    control = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_control_summary.csv").iloc[0]
    freeze = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_manifest.csv").iloc[0]

    source_fields = pd.DataFrame(
        [
            {
                "field_id": "MIX1_EDGE_DISK_COMPONENT",
                "field_name": "s4g_edge_disk_component",
                "field_value": source["s4g_components"],
                "field_status": "SOURCE_SUPPORTS_SMOOTH_DISK_CARRIER",
                "interpretation": "S4G decomposition has an edge-disk component; no compact bulge component is present.",
            },
            {
                "field_id": "MIX2_VERTICAL_OVERLAY",
                "field_name": "s4g_edge_disk_h_over_r",
                "field_value": source["s4g_edge_disk_h_over_r"],
                "field_status": "SOURCE_SUPPORTS_VERTICAL_OVERLAY",
                "interpretation": "The edge-disk h/R field supports a vertical/projection overlay kernel.",
            },
            {
                "field_id": "MIX3_EXTENDED_COMPONENT",
                "field_name": "extended_component_mass_fraction",
                "field_value": source["extended_component_mass_fraction"],
                "field_status": "SOURCE_SUPPORTS_EXTENDED_VERTICAL_COMPONENT",
                "interpretation": "The extended component supports a non-compact vertical overlay lane.",
            },
            {
                "field_id": "MIX4_WARP_VERTICAL_LABEL",
                "field_name": "replacement_label_status",
                "field_value": label["label_promotion_status"],
                "field_status": "CAVEATED_SOURCE_GATE_PRESENT",
                "interpretation": "The warp/vertical overlay label is caveated endpoint-score allowed.",
            },
            {
                "field_id": "MIX5_WRONG_FAMILY_SIGNAL",
                "field_name": "wrong_family_best_rmse",
                "field_value": control["wrong_family_best_rmse"],
                "field_status": "ENDPOINT_DIAGNOSTIC_SIGNAL_NOT_LABEL_INPUT",
                "interpretation": "The exponential-disk family beat the pure overlay endpoint in the control audit; this cannot promote a label by itself.",
            },
        ]
    )
    source_fields["endpoint_scores_allowed"] = False
    source_fields["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "MIXG1_COMPACT_REJECTED",
                "gate_status": "PASS",
                "evidence": str(source["compact_lane_decision"]),
                "remaining_obligation": "none for rejecting the compact-only lane",
            },
            {
                "gate_id": "MIXG2_SMOOTH_DISK_SOURCE_SUPPORT",
                "gate_status": "PASS_CAVEATED",
                "evidence": f"S4G components={source['s4g_components']}; edge disk h/R={float(source['s4g_edge_disk_h_over_r']):.6g}",
                "remaining_obligation": "derive a residual-blind rule for when the exponential-disk carrier is selected",
            },
            {
                "gate_id": "MIXG3_WARP_VERTICAL_FORMULA_AVAILABLE",
                "gate_status": "PASS",
                "evidence": str(freeze["formula_id"]),
                "remaining_obligation": "none at overlay-kernel level",
            },
            {
                "gate_id": "MIXG4_SCORE_INFERENCE_CAVEAT",
                "gate_status": "BLOCKED_FOR_ENDPOINT",
                "evidence": str(control["control_status"]),
                "remaining_obligation": "mixed family is diagnostic-only until selected by source rules before scoring",
            },
        ]
    )
    gates["galaxy"] = "NGC4013"
    gates["mixed_readout_candidate"] = "K_expdisk_warp_vertical_overlay"
    gates["endpoint_scores_allowed"] = False
    gates["diagnostic_scores_allowed"] = True
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "mixed_readout_candidate",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "diagnostic_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "mixed_readout_candidate": "K_expdisk_warp_vertical_overlay",
                "carrier": "K_exponential_disk",
                "overlay_formula_id": str(freeze["formula_id"]),
                "n_source_fields": len(source_fields),
                "n_gates": len(gates),
                "n_endpoint_blocked": int(gates["gate_status"].str.contains("BLOCKED").sum()),
                "hypothesis_status": "DIAGNOSTIC_ONLY_MIXED_READOUT_HYPOTHESIS",
                "endpoint_scores_allowed": False,
                "diagnostic_scores_allowed": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    source_fields.to_csv(DATA / "ngc4013_expdisk_wvo_hypothesis_source_fields.csv", index=False)
    gates.to_csv(DATA / "ngc4013_expdisk_wvo_hypothesis_gate.csv", index=False)
    summary.to_csv(DATA / "ngc4013_expdisk_wvo_hypothesis_summary.csv", index=False)

    report = [
        "# NGC4013 Exponential-Disk + Warp/Vertical-Overlay Hypothesis Gate",
        "",
        "This gate creates a mixed-readout diagnostic hypothesis. It is not an",
        "accepted endpoint label because the exponential-disk carrier was motivated",
        "by a wrong-family control result as well as source-side disk evidence.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source Fields",
        "",
        markdown_table(source_fields),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The mixed readout may be inspected diagnostically. Promotion requires a",
        "future residual-blind source rule selecting the exponential-disk carrier",
        "before endpoint scoring.",
        "",
    ]
    (REPORTS / "ngc4013_expdisk_wvo_hypothesis_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
