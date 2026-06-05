#!/usr/bin/env python3
"""Build first-pass residual-blind source-response fills for NGC4088.

This script fills provisional q_warp and morphological-history source responses
from the already frozen channel-map digitization response.  The fills are not
independently reviewed and are not endpoint-authorizing.  They exist to test
the algebraic epsilon_cross pipeline without using rotation residuals.  The
history proxy is morphology-carried source history, not a separate fundamental
memory object.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_first_pass_source_response_fill_not_endpoint"


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


def clipped(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def build_fill() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    response = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_template.csv"
    ).iloc[0]
    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    worksheet = pd.read_csv(DATA / "s4g75_ngc4088_channel_map_digitization_worksheet_summary.csv").iloc[0]

    inner_pa = float(response["inner_disk_axis_pa_deg"])
    side_a_pa = float(response["outer_ridge_axis_side_a_pa_deg"])
    side_b_pa = float(response["outer_ridge_axis_side_b_pa_deg"])
    delta_pa_a = abs(side_a_pa - inner_pa)
    delta_pa_b = abs(side_b_pa - inner_pa)
    delta_pa_max = max(delta_pa_a, delta_pa_b)

    side_onset_delta = abs(
        float(response["onset_radius_side_b_arcmin"])
        - float(response["onset_radius_side_a_arcmin"])
    )
    onset_uncertainty_fraction = float(xw["x_warp_uncertainty"]) / float(
        xw["x_warp_onset"]
    )

    q_warp = clipped(delta_pa_max / 90.0)
    q_uncertainty = clipped(max(onset_uncertainty_fraction, side_onset_delta / float(xw["hi_radius_arcmin"])))

    q_response = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "response_id": "QWARP_FIRST_PASS_SOURCE_RESPONSE_V1",
                "q_warp_measured": q_warp,
                "q_warp_uncertainty": q_uncertainty,
                "n_panels_used": int(worksheet["n_measurement_targets"]),
                "n_panel_measurements_required": int(worksheet["n_measurement_targets"]),
                "inner_axis_pa_deg": inner_pa,
                "outer_axis_side_a_pa_deg": side_a_pa,
                "outer_axis_side_b_pa_deg": side_b_pa,
                "source_rule": "clipped(max_outer_inner_PA_mismatch / 90deg)",
                "response_status": "FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED",
                "accepted_for_numeric_bound": False,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    memory_components = pd.DataFrame(
        [
            {
                "component_id": "H1_WARP_PERSISTENCE",
                "component_symbol": "h_warp_persist",
                "component_value": 1.0,
                "evidence": "warp/asymmetry visible across the frozen channel-map panel sequence",
                "component_status": "FIRST_PASS_FILLED_REVIEW_REQUIRED",
            },
            {
                "component_id": "H2_HI_LOPSIDEDNESS",
                "component_symbol": "h_lopsided_hi",
                "component_value": clipped(delta_pa_max / 90.0),
                "evidence": "side A outer ridge differs strongly from the inner axis while side B remains aligned",
                "component_status": "FIRST_PASS_FILLED_REVIEW_REQUIRED",
            },
            {
                "component_id": "H3_OUTER_DISK_ASYMMETRY",
                "component_symbol": "h_outer_asym",
                "component_value": clipped(max(delta_pa_max / 90.0, side_onset_delta / float(xw["hi_radius_arcmin"]))),
                "evidence": "outer ridge PA and onset side asymmetry are present in source digitization",
                "component_status": "FIRST_PASS_FILLED_REVIEW_REQUIRED",
            },
            {
                "component_id": "H4_INTERACTION_CONTEXT",
                "component_symbol": "h_env",
                "component_value": None,
                "evidence": "environment/interaction context not filled from source registry in this pass",
                "component_status": "SOURCE_REVIEW_REQUIRED",
            },
        ]
    )
    memory_components["galaxy"] = GALAXY
    memory_components["uses_vobs_or_residual"] = False
    memory_components["endpoint_scores_allowed"] = False
    memory_components["claim_boundary"] = CLAIM_BOUNDARY
    memory_components = memory_components[
        [
            "galaxy",
            "component_id",
            "component_symbol",
            "component_value",
            "evidence",
            "component_status",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    measured = memory_components["component_value"].notna()
    m_history = float(memory_components.loc[measured, "component_value"].mean())
    m_uncertainty = clipped(max(0.25, 1.0 - measured.mean()))
    memory_response = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "response_id": "NGC4088_MEMORY_HISTORY_FIRST_PASS_RESPONSE_V1",
                "m_history_warp": m_history,
                "m_history_uncertainty": m_uncertainty,
                "n_components_measured": int(measured.sum()),
                "n_components_required": len(memory_components),
                "source_ready_whisp": True,
                "response_status": "PARTIAL_FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED",
                "accepted_for_numeric_bound": False,
                "uses_rotation_inferred_proxy": False,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "FP1_Q_SOURCE_FILL_AVAILABLE",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "q_warp filled from source PA mismatch rule",
                "remaining_obligation": "independent source review before accepted numeric bound",
            },
            {
                "gate_id": "FP2_MEMORY_SOURCE_FILL_AVAILABLE",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "morphological-history proxy partially filled from source morphology components",
                "remaining_obligation": "fill environment context and independently review components",
            },
            {
                "gate_id": "FP3_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "fills use channel-map/source morphology and forbid endpoint residuals",
                "remaining_obligation": "keep endpoint scoring separate",
            },
            {
                "gate_id": "FP4_NUMERIC_BOUND_AUTHORIZATION",
                "gate_status": "BLOCKED",
                "evidence": "first-pass fills are not accepted inputs",
                "remaining_obligation": "accepted numeric bound requires independent review and B_i values",
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
                "fill_id": "NGC4088_FIRST_PASS_QWARP_MEMORY_SOURCE_RESPONSE_FILL",
                "q_warp_measured": q_warp,
                "m_history_warp": m_history,
                "n_memory_components_measured": int(measured.sum()),
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "fill_status": "FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED",
                "accepted_for_numeric_bound": False,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return q_response, memory_components, memory_response, gates, summary


def write_report(
    q_response: pd.DataFrame,
    memory_components: pd.DataFrame,
    memory_response: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 First-Pass Source Response Fill",
        "",
        "This artifact fills provisional q_warp and morphological-history source values",
        "from the already frozen channel-map digitization response. It does not",
        "authorize a numeric epsilon_cross bound.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## q_warp Response",
        "",
        markdown_table(q_response),
        "",
        "## Memory Components",
        "",
        markdown_table(memory_components),
        "",
        "## Memory Response",
        "",
        markdown_table(memory_response),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "These are first-pass source fills only. They are useful for checking the",
        "algebraic pipeline, but accepted numeric bounds still require independent",
        "review and B_i coefficient values.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_first_pass_source_response_fill.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    q_response, memory_components, memory_response, gates, summary = build_fill()
    q_response.to_csv(DATA / "s4g75_ngc4088_qwarp_first_pass_response.csv", index=False)
    memory_components.to_csv(
        DATA / "s4g75_ngc4088_memory_history_first_pass_components.csv",
        index=False,
    )
    memory_response.to_csv(
        DATA / "s4g75_ngc4088_memory_history_first_pass_response.csv",
        index=False,
    )
    gates.to_csv(DATA / "s4g75_ngc4088_first_pass_source_response_fill_gate.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_first_pass_source_response_fill_summary.csv",
        index=False,
    )
    write_report(q_response, memory_components, memory_response, gates, summary)
    print("PAPER8_NGC4088_FIRST_PASS_SOURCE_RESPONSE_FILL_COMPLETE")


if __name__ == "__main__":
    main()
