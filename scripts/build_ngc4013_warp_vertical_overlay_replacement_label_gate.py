#!/usr/bin/env python3
"""Promote the NGC4013 warp/vertical-overlay replacement label.

This gate is source-side only. It decides whether the rejected compact lane can
be replaced by the warp/vertical-overlay readout label before a preliminary
endpoint diagnostic is run. It does not inspect observed rotation residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_warp_vertical_overlay_replacement_label_gate_not_score"


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


def get_observable(rows: pd.DataFrame, observable_name: str) -> pd.Series:
    match = rows.loc[rows["observable_name"] == observable_name]
    if match.empty:
        raise RuntimeError(f"missing NGC4013 observable: {observable_name}")
    return match.iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    extracted = pd.read_csv(DATA / "readout_subfamily_extracted_observables.csv")
    rows = extracted.loc[extracted["galaxy"] == "NGC4013"].copy()
    source = pd.read_csv(DATA / "ngc4013_compact_overlay_source_summary.csv").iloc[0]
    preflight = pd.read_csv(DATA / "ngc4013_warp_overlay_preflight_summary.csv").iloc[0]
    freeze = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_summary.csv").iloc[0]
    freeze_manifest = pd.read_csv(
        DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_manifest.csv"
    ).iloc[0]

    overlay = get_observable(rows, "compact_only_overlay_flag")
    onset = get_observable(rows, "line_of_sight_warp_onset")
    scaleheight = get_observable(rows, "final_hi_scaleheight_central")
    lag = get_observable(rows, "rotational_lag_profile")

    source_fields = pd.DataFrame(
        [
            {
                "field_id": "RL1_COMPACT_REJECTION",
                "field_name": "compact_lane_decision",
                "field_value": source["compact_lane_decision"],
                "field_status": "ACCEPTED_NEGATIVE_COMPACT_EVIDENCE",
                "source": "S4G decomposition + Comeron vertical decomposition review",
            },
            {
                "field_id": "RL2_WARP_OVERLAY_PRESSURE",
                "field_name": "compact_only_overlay_flag",
                "field_value": overlay["observable_value"],
                "field_status": "ACCEPTED_RECLASSIFICATION_PRESSURE",
                "source": overlay["source_file"],
            },
            {
                "field_id": "RL3_WARP_ONSET",
                "field_name": "line_of_sight_warp_onset",
                "field_value": onset["numeric_value"],
                "field_status": onset["extraction_status"],
                "source": onset["source_file"],
            },
            {
                "field_id": "RL4_VERTICAL_KERNEL",
                "field_name": "s4g_edge_disk_h_over_r",
                "field_value": source["s4g_edge_disk_h_over_r"],
                "field_status": "ACQUIRED_VERTICAL_KERNEL_EVIDENCE",
                "source": "S4G Pipeline 4 edge-disk decomposition",
            },
            {
                "field_id": "RL5_EXTENDED_COMPONENT",
                "field_name": "extended_component_mass_fraction",
                "field_value": source["extended_component_mass_fraction"],
                "field_status": "ACQUIRED_EXTENDED_VERTICAL_COMPONENT_EVIDENCE",
                "source": "Comeron et al. 2011",
            },
            {
                "field_id": "RL6_CENTRAL_HI_SCALEHEIGHT",
                "field_name": "final_hi_scaleheight_central",
                "field_value": scaleheight["numeric_value"],
                "field_status": scaleheight["extraction_status"],
                "source": scaleheight["source_file"],
            },
            {
                "field_id": "RL7_ROTATIONAL_LAG",
                "field_name": "rotational_lag_profile",
                "field_value": lag["observable_value"],
                "field_status": lag["extraction_status"],
                "source": lag["source_file"],
            },
        ]
    )
    source_fields["endpoint_scores_allowed"] = False
    source_fields["claim_boundary"] = CLAIM_BOUNDARY

    compact_rejected = source["compact_lane_decision"] == "COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED"
    replacement_recommended = (
        source["replacement_lane_recommendation"]
        == "PROMOTE_WARP_VERTICAL_OVERLAY_PREFLIGHT_NOT_ENDPOINT"
    )
    preflight_ready = (
        preflight["preflight_status"]
        == "COMPACT_REJECTED_WARP_OVERLAY_PREFLIGHT_READY_FORMULA_BLOCKED"
    )
    formula_ready = (
        freeze["formula_freeze_status"] == "FORMULA_FREEZE_PROTOCOL_READY_LABEL_BLOCKED"
    )
    blind = not bool(freeze_manifest["uses_vobs_or_residual_in_construction"])

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4013_RLG1_COMPACT_LABEL_REJECTED",
                "gate_status": "PASS" if compact_rejected else "BLOCKED",
                "evidence": str(source["compact_lane_decision"]),
                "remaining_obligation": "none if compact lane remains rejected",
            },
            {
                "gate_id": "N4013_RLG2_REPLACEMENT_LANE_RECOMMENDED",
                "gate_status": "PASS" if replacement_recommended else "BLOCKED",
                "evidence": str(source["replacement_lane_recommendation"]),
                "remaining_obligation": "none at source-recommendation level",
            },
            {
                "gate_id": "N4013_RLG3_WARP_VERTICAL_SOURCE_FIELDS",
                "gate_status": "PASS",
                "evidence": "warp onset, vertical thickness, extended component, and lag context are present",
                "remaining_obligation": "future review may refine R_o, K_lag, or weights without using endpoint residuals",
            },
            {
                "gate_id": "N4013_RLG4_PREFLIGHT_READY",
                "gate_status": "PASS" if preflight_ready else "BLOCKED",
                "evidence": str(preflight["preflight_status"]),
                "remaining_obligation": "none at preflight level",
            },
            {
                "gate_id": "N4013_RLG5_FORMULA_FREEZE_PROTOCOL_READY",
                "gate_status": "PASS_CAVEATED" if formula_ready else "BLOCKED",
                "evidence": str(freeze["formula_freeze_status"]),
                "remaining_obligation": "caveats: R_o=R25 proxy, linear K_lag shell, uniform weights",
            },
            {
                "gate_id": "N4013_RLG6_ENDPOINT_BLINDNESS",
                "gate_status": "PASS" if blind else "BLOCKED",
                "evidence": "freeze manifest forbids vobs/residual construction inputs",
                "remaining_obligation": "endpoint scoring must run in a separate script",
            },
        ]
    )

    blocked_count = int(gates["gate_status"].eq("BLOCKED").sum())
    label_promoted = blocked_count == 0
    endpoint_scores_allowed = label_promoted

    gates["galaxy"] = "NGC4013"
    gates["replacement_label"] = "K_warp_vertical_overlay_candidate"
    gates["endpoint_scores_allowed"] = endpoint_scores_allowed
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "replacement_label",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "rejected_label": "K_true_compact",
                "accepted_replacement_label": "K_warp_vertical_overlay_candidate",
                "n_source_fields": len(source_fields),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_blocked": blocked_count,
                "formula_id": freeze["formula_id"],
                "label_promotion_status": (
                    "CAVEATED_REPLACEMENT_LABEL_PROMOTED_ENDPOINT_SCORE_ALLOWED"
                    if label_promoted
                    else "REPLACEMENT_LABEL_PROMOTION_BLOCKED"
                ),
                "accepted_replacement_label_promoted": label_promoted,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    source_fields.to_csv(
        DATA / "ngc4013_warp_vertical_overlay_replacement_label_source_fields.csv",
        index=False,
    )
    gates.to_csv(DATA / "ngc4013_warp_vertical_overlay_replacement_label_gate.csv", index=False)
    summary.to_csv(
        DATA / "ngc4013_warp_vertical_overlay_replacement_label_summary.csv", index=False
    )

    report = [
        "# NGC4013 Warp/Vertical-Overlay Replacement-Label Gate",
        "",
        "This gate promotes the replacement readout label only at source-side,",
        "caveated preliminary endpoint level. It does not score the rotation curve",
        "and does not validate Tau Core.",
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
        "A promoted replacement label here means that the compact lane has failed",
        "source review and the warp/vertical-overlay lane has enough residual-blind",
        "source support to run a caveated preliminary endpoint. It is not a",
        "population validation claim.",
        "",
    ]
    (REPORTS / "ngc4013_warp_vertical_overlay_replacement_label_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
