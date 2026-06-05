#!/usr/bin/env python3
"""Build a source-bound protocol for NGC4088 epsilon_cross.

The cross-term suppression gate introduced epsilon_cross as a symbolic
correction.  This protocol defines residual-blind source observables that could
bound epsilon_cross without fitting rotation-curve residuals, and records which
inputs are currently available for NGC4088.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_epsilon_cross_source_bound_protocol_not_endpoint"


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
    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    response = pd.read_csv(DATA / "s4g75_ngc4088_channel_map_digitization_response_template.csv").iloc[0]
    cross_summary = pd.read_csv(DATA / "s4g75_ngc4088_cross_term_suppression_summary.csv").iloc[0]

    observables = pd.DataFrame(
        [
            {
                "observable_id": "O1_ORIENTATION_MISMATCH",
                "observable_symbol": "Delta_PA_outer_inner",
                "source_role": "bounds orientation-strength and onset-carrier cross terms",
                "current_value": abs(float(response["outer_ridge_axis_side_a_pa_deg"]) - float(response["inner_disk_axis_pa_deg"])),
                "unit": "deg",
                "availability_status": "AVAILABLE_FIRST_PASS_NOT_INDEPENDENTLY_REVIEWED",
                "source": "NGC4088 channel-map digitization response",
            },
            {
                "observable_id": "O2_SIDE_ASYMMETRY",
                "observable_symbol": "Delta_R_onset_sides",
                "source_role": "bounds onset-strength asymmetry cross term",
                "current_value": abs(float(response["onset_radius_side_b_arcmin"]) - float(response["onset_radius_side_a_arcmin"])),
                "unit": "arcmin",
                "availability_status": "AVAILABLE_FIRST_PASS_NOT_INDEPENDENTLY_REVIEWED",
                "source": "NGC4088 channel-map digitization response",
            },
            {
                "observable_id": "O3_ONSET_UNCERTAINTY_FRACTION",
                "observable_symbol": "sigma_xw_over_xw",
                "source_role": "bounds onset-support ambiguity",
                "current_value": float(xw["x_warp_uncertainty"]) / float(xw["x_warp_onset"]),
                "unit": "dimensionless",
                "availability_status": "AVAILABLE_FIRST_PASS_NOT_INDEPENDENTLY_REVIEWED",
                "source": "x_w conversion audit",
            },
            {
                "observable_id": "O4_SOURCE_STRENGTH_AMPLITUDE",
                "observable_symbol": "q_warp_measured",
                "source_role": "bounds q_warp-strength cross terms",
                "current_value": None,
                "unit": "dimensionless",
                "availability_status": "MISSING_QUANTITATIVE_SOURCE_AMPLITUDE",
                "source": "requires source-measured warp/asymmetry amplitude",
            },
            {
                "observable_id": "O5_MEMORY_HISTORY_PROXY",
                "observable_symbol": "m_history_warp",
                "source_role": "bounds geometry-memory cross term",
                "current_value": None,
                "unit": "dimensionless",
                "availability_status": "MISSING_HISTORY_MEMORY_SOURCE_PROXY",
                "source": "requires residual-blind morphology memory/history proxy",
            },
        ]
    )
    observables["galaxy"] = GALAXY
    observables["claim_boundary"] = CLAIM_BOUNDARY
    observables = observables[
        [
            "galaxy",
            "observable_id",
            "observable_symbol",
            "source_role",
            "current_value",
            "unit",
            "availability_status",
            "source",
            "claim_boundary",
        ]
    ]

    protocol = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "protocol_id": "EPSILON_CROSS_RESIDUAL_BLIND_SOURCE_BOUND_PROTOCOL",
                "bound_form": (
                    "|epsilon_cross| <= B_PA f_PA + B_R f_R + B_q f_q + B_mem f_mem"
                ),
                "allowed_inputs": (
                    "orientation mismatch; side onset asymmetry; onset uncertainty; "
                    "source-measured warp amplitude; memory/history proxy"
                ),
                "forbidden_inputs": "vobs; endpoint residuals; endpoint-selected family or amplitude",
                "current_status": "BOUND_FORM_DECLARED_NUMERIC_BOUND_BLOCKED",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "B1_BOUND_FORM_DECLARED",
                "gate_status": "PASS",
                "evidence": "a residual-blind symbolic bound form is declared",
                "remaining_obligation": "derive coefficients B_i from Tau-side geometry or predeclare them",
            },
            {
                "gate_id": "B2_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "bound protocol forbids vobs and endpoint residuals",
                "remaining_obligation": "keep endpoint evaluation separate",
            },
            {
                "gate_id": "B3_PARTIAL_SOURCE_OBSERVABLES_AVAILABLE",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "orientation mismatch, side asymmetry, and onset uncertainty are available from first-pass digitization",
                "remaining_obligation": "independent digitization review",
            },
            {
                "gate_id": "B4_QUANTITATIVE_Q_WARP_AVAILABLE",
                "gate_status": "BLOCKED",
                "evidence": "q_warp is currently qualitative q_warp=1",
                "remaining_obligation": "measure quantitative source amplitude from channel maps or HI morphology",
            },
            {
                "gate_id": "B5_MEMORY_PROXY_AVAILABLE",
                "gate_status": "BLOCKED",
                "evidence": "no NGC4088-specific memory/history source proxy is currently accepted",
                "remaining_obligation": "construct residual-blind memory/history proxy for warp/asymmetry lane",
            },
            {
                "gate_id": "B6_BOUND_COEFFICIENTS_DERIVED",
                "gate_status": "BLOCKED",
                "evidence": "B_i coefficients are not derived from Tau-side geometry",
                "remaining_obligation": "derive or predeclare coefficient rule before endpoint use",
            },
            {
                "gate_id": "B7_CROSS_TERM_GATE_CONNECTION",
                "gate_status": "PASS",
                "evidence": cross_summary["cross_term_status"],
                "remaining_obligation": "use this protocol to move epsilon_cross from symbolic to bounded",
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
    n_available = int(
        observables["availability_status"].str.startswith("AVAILABLE").sum()
    )
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "protocol_id": protocol["protocol_id"].iloc[0],
                "n_observables": len(observables),
                "n_available_observables": n_available,
                "n_missing_observables": len(observables) - n_available,
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "bound_status": "SOURCE_BOUND_PROTOCOL_PARTIAL_NUMERIC_BOUND_BLOCKED",
                "epsilon_cross_status": "SYMBOLIC_UNBOUNDED_UNTIL_Q_AND_MEMORY_READY",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return observables, protocol, gates, summary


def write_report(
    observables: pd.DataFrame,
    protocol: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Epsilon-Cross Source-Bound Protocol",
        "",
        "This protocol defines residual-blind source observables that could bound",
        "`epsilon_cross`. It does not fit endpoint residuals and does not yet",
        "produce a numeric bound.",
        "",
        "## Bound Protocol",
        "",
        markdown_table(protocol),
        "",
        "## Source Observables",
        "",
        markdown_table(observables),
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
        "`epsilon_cross` remains symbolic until quantitative q_warp, memory/history",
        "proxy, and bound coefficients are residual-blindly supplied.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_epsilon_cross_source_bound_protocol.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    observables, protocol, gates, summary = build_protocol()
    observables.to_csv(DATA / "s4g75_ngc4088_epsilon_cross_source_observables.csv", index=False)
    protocol.to_csv(DATA / "s4g75_ngc4088_epsilon_cross_bound_protocol.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_epsilon_cross_source_bound_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_epsilon_cross_source_bound_summary.csv", index=False)
    write_report(observables, protocol, gates, summary)
    print("PAPER8_NGC4088_EPSILON_CROSS_SOURCE_BOUND_PROTOCOL_COMPLETE")


if __name__ == "__main__":
    main()
