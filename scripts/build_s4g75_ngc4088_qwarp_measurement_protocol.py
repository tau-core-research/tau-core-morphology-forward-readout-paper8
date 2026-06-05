#!/usr/bin/env python3
"""Build a residual-blind q_warp measurement protocol for NGC4088.

q_warp is currently a qualitative source-strength gate set to one.  This
protocol defines how a quantitative q_warp_measured value could be extracted
from channel-map/HI morphology sources without using rotation-curve endpoint
residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_qwarp_measurement_protocol_not_endpoint"


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


def build_protocol() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    worksheet_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_worksheet_summary.csv"
    ).iloc[0]
    response = pd.read_csv(DATA / "s4g75_ngc4088_channel_map_digitization_response_template.csv").iloc[0]

    protocol = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "protocol_id": "QWARP_CHANNEL_MAP_SOURCE_STRENGTH_PROTOCOL",
                "definition": (
                    "q_warp_measured = clipped_mean_over_target_panels("
                    "outer_asymmetry_extent / local_disk_reference_extent)"
                ),
                "allowed_sources": "page76 channel-map ROI; worksheet overlay; page77 PA cross-check; HI morphology maps",
                "forbidden_inputs": "vobs; endpoint residuals; best-fit amplitude; endpoint-selected family",
                "normalization": "dimensionless ratio with q=0 no detected outer warp/asymmetry and q=1 strong source lane",
                "current_status": "PROTOCOL_READY_MEASUREMENT_RESPONSE_EMPTY",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    measurement_fields = pd.DataFrame(
        [
            {
                "field_id": "F1_OUTER_ASYMMETRY_EXTENT",
                "field_name": "outer_asymmetry_extent_px",
                "description": "outer displaced HI ridge or warp/asymmetry extent in panel coordinates",
                "required": True,
            },
            {
                "field_id": "F2_LOCAL_DISK_REFERENCE_EXTENT",
                "field_name": "local_disk_reference_extent_px",
                "description": "local inner/ordinary disk reference extent in the same panel",
                "required": True,
            },
            {
                "field_id": "F3_PANEL_WEIGHT",
                "field_name": "panel_source_weight",
                "description": "residual-blind panel reliability/source strength weight",
                "required": True,
            },
            {
                "field_id": "F4_SIDE_LABEL",
                "field_name": "side_label",
                "description": "approaching/receding or side A/B label used only for source symmetry checks",
                "required": True,
            },
            {
                "field_id": "F5_REVIEW_FLAG",
                "field_name": "review_flag",
                "description": "independent-review status and caveat flag",
                "required": True,
            },
        ]
    )
    measurement_fields["galaxy"] = GALAXY
    measurement_fields["claim_boundary"] = CLAIM_BOUNDARY
    measurement_fields = measurement_fields[
        ["galaxy", "field_id", "field_name", "description", "required", "claim_boundary"]
    ]

    response_template = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "response_id": "QWARP_MEASUREMENT_RESPONSE_V1",
                "q_warp_measured": None,
                "q_warp_uncertainty": None,
                "n_panels_used": 0,
                "n_panel_measurements_required": int(worksheet_summary["n_measurement_targets"]),
                "inner_axis_pa_deg": float(response["inner_disk_axis_pa_deg"]),
                "outer_axis_side_a_pa_deg": float(response["outer_ridge_axis_side_a_pa_deg"]),
                "outer_axis_side_b_pa_deg": float(response["outer_ridge_axis_side_b_pa_deg"]),
                "response_status": "MEASUREMENT_EMPTY",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "Q1_PROTOCOL_DEFINED",
                "gate_status": "PASS",
                "evidence": "dimensionless q_warp measurement rule is declared",
                "remaining_obligation": "none at protocol-definition level",
            },
            {
                "gate_id": "Q2_SOURCE_IMAGES_AVAILABLE",
                "gate_status": "PASS",
                "evidence": "page76 ROI, worksheet overlay, and page77 cross-check are already present",
                "remaining_obligation": "none at source-availability level",
            },
            {
                "gate_id": "Q3_PANEL_WORKSHEET_READY",
                "gate_status": "PASS",
                "evidence": f"{int(worksheet_summary['n_measurement_targets'])} measurement targets are available",
                "remaining_obligation": "fill q_warp-specific measurement fields",
            },
            {
                "gate_id": "Q4_RESPONSE_FILLED",
                "gate_status": "BLOCKED",
                "evidence": "q_warp_measured and uncertainty are empty",
                "remaining_obligation": "perform residual-blind source measurement",
            },
            {
                "gate_id": "Q5_INDEPENDENT_REVIEW",
                "gate_status": "BLOCKED",
                "evidence": "no independent q_warp review exists",
                "remaining_obligation": "independent reviewer must verify measurement",
            },
            {
                "gate_id": "Q6_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "protocol forbids vobs and endpoint residuals",
                "remaining_obligation": "keep endpoint scoring separate",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    status_counts = gates["gate_status"].value_counts().to_dict()
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "protocol_id": protocol["protocol_id"].iloc[0],
                "n_measurement_fields": len(measurement_fields),
                "n_panel_measurements_required": int(worksheet_summary["n_measurement_targets"]),
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "q_warp_status": "QWARP_PROTOCOL_READY_MEASUREMENT_BLOCKED",
                "epsilon_cross_impact": "UNBLOCKS_Q_COMPONENT_AFTER_MEASUREMENT_AND_REVIEW",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return protocol, measurement_fields, response_template, gates, summary


def write_report(
    protocol: pd.DataFrame,
    measurement_fields: pd.DataFrame,
    response_template: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 q_warp Measurement Protocol",
        "",
        "This protocol turns the qualitative q_warp=1 gate into a residual-blind",
        "measurement task. It does not fill q_warp and does not use endpoint",
        "residuals.",
        "",
        "## Protocol",
        "",
        markdown_table(protocol),
        "",
        "## Measurement Fields",
        "",
        markdown_table(measurement_fields),
        "",
        "## Response Template",
        "",
        markdown_table(response_template),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "q_warp remains qualitative until this protocol is measured and",
        "independently reviewed.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_qwarp_measurement_protocol.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    protocol, fields, response, gates, summary = build_protocol()
    protocol.to_csv(DATA / "s4g75_ngc4088_qwarp_measurement_protocol.csv", index=False)
    fields.to_csv(DATA / "s4g75_ngc4088_qwarp_measurement_fields.csv", index=False)
    response.to_csv(DATA / "s4g75_ngc4088_qwarp_measurement_response_template.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_qwarp_measurement_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_qwarp_measurement_summary.csv", index=False)
    write_report(protocol, fields, response, gates, summary)
    print("PAPER8_NGC4088_QWARP_MEASUREMENT_PROTOCOL_COMPLETE")


if __name__ == "__main__":
    main()
