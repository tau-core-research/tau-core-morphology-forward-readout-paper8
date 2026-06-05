#!/usr/bin/env python3
"""Build the NGC4088 epsilon_cross input review packet.

The epsilon_cross bound is blocked by missing source measurements and missing
coefficient rules. This packet consolidates the residual-blind q_warp,
memory/history, and B_i coefficient obligations into one review artifact. It
does not fill measurements, derive coefficients, or compute endpoint scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_epsilon_cross_input_review_packet_not_endpoint"


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


def build_packet() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    q_summary = pd.read_csv(DATA / "s4g75_ngc4088_qwarp_measurement_summary.csv").iloc[0]
    memory_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_memory_history_proxy_summary.csv"
    ).iloc[0]
    epsilon_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_source_bound_summary.csv"
    ).iloc[0]
    q_first_pass_path = DATA / "s4g75_ngc4088_qwarp_first_pass_response.csv"
    memory_first_pass_path = DATA / "s4g75_ngc4088_memory_history_first_pass_response.csv"
    q_first_pass = pd.read_csv(q_first_pass_path).iloc[0] if q_first_pass_path.exists() else None
    memory_first_pass = (
        pd.read_csv(memory_first_pass_path).iloc[0] if memory_first_pass_path.exists() else None
    )
    source_review_path = DATA / "s4g75_ngc4088_source_response_independent_review.csv"
    freeze_summary_path = DATA / "s4g75_ngc4088_bi_coefficient_freeze_rule_summary.csv"
    sharp_summary_path = DATA / "s4g75_ngc4088_bi_sharp_coefficient_bound_rule_summary.csv"
    source_review = (
        pd.read_csv(source_review_path) if source_review_path.exists() else pd.DataFrame()
    )
    freeze_summary = (
        pd.read_csv(freeze_summary_path).iloc[0] if freeze_summary_path.exists() else None
    )
    sharp_summary = (
        pd.read_csv(sharp_summary_path).iloc[0] if sharp_summary_path.exists() else None
    )
    source_status_by_target = {}
    if not source_review.empty:
        source_status_by_target = dict(
            zip(source_review["review_target"], source_review["review_status"])
        )
    q_status = source_status_by_target.get(
        "q_warp_measured",
        str(q_first_pass["response_status"]) if q_first_pass is not None else q_summary["q_warp_status"],
    )
    memory_status = source_status_by_target.get(
        "m_history_warp",
        str(memory_first_pass["response_status"])
        if memory_first_pass is not None
        else memory_summary["memory_proxy_status"],
    )
    coefficient_status = (
        "SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT"
        if sharp_summary is not None
        and bool(sharp_summary["numeric_bound_coefficient_authorization"])
        else (
            "FROZEN_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT"
            if freeze_summary is not None
            and bool(freeze_summary["numeric_bound_coefficient_authorization"])
            else "COEFFICIENT_RULE_MISSING"
        )
    )
    source_review_ready = set(source_status_by_target) >= {
        "q_warp_measured",
        "m_history_warp",
    }
    coefficients_ready = coefficient_status in {
        "FROZEN_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT",
        "SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT",
    }
    numeric_ready = source_review_ready and coefficients_ready

    obligations = pd.DataFrame(
        [
            {
                "obligation_id": "EIN_Q_WARP_MEASUREMENT",
                "obligation_class": "SOURCE_MEASUREMENT",
                "required_input": "q_warp_measured",
                "source_artifact": "s4g75_ngc4088_qwarp_measurement_response_template.csv",
                "current_status": q_status,
                "unblocks": "B4_QUANTITATIVE_Q_WARP_AVAILABLE",
                "endpoint_scores_allowed": False,
            },
            {
                "obligation_id": "EIN_MEMORY_HISTORY_PROXY",
                "obligation_class": "SOURCE_MEASUREMENT",
                "required_input": "m_history_warp",
                "source_artifact": "s4g75_ngc4088_memory_history_proxy_response_template.csv",
                "current_status": memory_status,
                "unblocks": "B5_MEMORY_PROXY_AVAILABLE",
                "endpoint_scores_allowed": False,
            },
            {
                "obligation_id": "EIN_B_PA_COEFFICIENT",
                "obligation_class": "COEFFICIENT_RULE",
                "required_input": "B_PA",
                "source_artifact": "tau-side geometry/predeclared coefficient rule",
                "current_status": coefficient_status,
                "unblocks": "B6_BOUND_COEFFICIENTS_DERIVED",
                "endpoint_scores_allowed": False,
            },
            {
                "obligation_id": "EIN_B_R_COEFFICIENT",
                "obligation_class": "COEFFICIENT_RULE",
                "required_input": "B_R",
                "source_artifact": "tau-side geometry/predeclared coefficient rule",
                "current_status": coefficient_status,
                "unblocks": "B6_BOUND_COEFFICIENTS_DERIVED",
                "endpoint_scores_allowed": False,
            },
            {
                "obligation_id": "EIN_B_Q_COEFFICIENT",
                "obligation_class": "COEFFICIENT_RULE",
                "required_input": "B_q",
                "source_artifact": "tau-side geometry/predeclared coefficient rule",
                "current_status": coefficient_status,
                "unblocks": "B6_BOUND_COEFFICIENTS_DERIVED",
                "endpoint_scores_allowed": False,
            },
            {
                "obligation_id": "EIN_B_MEM_COEFFICIENT",
                "obligation_class": "COEFFICIENT_RULE",
                "required_input": "B_mem",
                "source_artifact": "tau-side geometry/predeclared coefficient rule",
                "current_status": coefficient_status,
                "unblocks": "B6_BOUND_COEFFICIENTS_DERIVED",
                "endpoint_scores_allowed": False,
            },
        ]
    )
    obligations["galaxy"] = GALAXY
    obligations["uses_vobs_or_residual"] = False
    obligations["claim_boundary"] = CLAIM_BOUNDARY
    obligations = obligations[
        [
            "galaxy",
            "obligation_id",
            "obligation_class",
            "required_input",
            "source_artifact",
            "current_status",
            "unblocks",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "EIN1_Q_PROTOCOL_READY",
                "gate_status": "PASS",
                "evidence": q_status,
                "remaining_obligation": (
                    "none"
                    if source_review_ready
                    else "independently review q_warp measurement response"
                ),
            },
            {
                "gate_id": "EIN2_MEMORY_PROTOCOL_READY",
                "gate_status": "PASS",
                "evidence": memory_status,
                "remaining_obligation": (
                    "none"
                    if memory_status == "ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND"
                    else "carry morphological-history caveat"
                    if source_review_ready
                    else "complete environment context and independently review morphological-history response"
                ),
            },
            {
                "gate_id": "EIN3_COEFFICIENT_RULES_DECLARED",
                "gate_status": "PASS" if coefficients_ready else "BLOCKED",
                "evidence": (
                    str(sharp_summary["sharp_rule_status"])
                    if sharp_summary is not None
                    and bool(sharp_summary["numeric_bound_coefficient_authorization"])
                    else str(freeze_summary["freeze_rule_status"])
                    if coefficients_ready and freeze_summary is not None
                    else "B_PA, B_R, B_q, and B_mem are not derived or predeclared"
                ),
                "remaining_obligation": (
                    "interpret as formula-conditional sharpened protocol coefficients"
                    if coefficient_status == "SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT"
                    else "interpret as conservative protocol coefficients"
                    if coefficient_status == "FROZEN_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT"
                    else "derive or freeze residual-blind coefficient rule before numeric bound"
                ),
            },
            {
                "gate_id": "EIN4_NUMERIC_BOUND_AUTHORIZED",
                "gate_status": "PASS" if numeric_ready else "BLOCKED",
                "evidence": (
                    "accepted source review and residual-blind B_i rule are available"
                    if numeric_ready
                    else epsilon_summary["epsilon_cross_status"]
                ),
                "remaining_obligation": (
                    "evaluate numeric epsilon_cross protocol bound"
                    if numeric_ready
                    else "requires q_warp, m_history_warp, coefficient rule, and independent review"
                ),
            },
            {
                "gate_id": "EIN5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "packet forbids vobs, endpoint residuals, and endpoint-selected models",
                "remaining_obligation": "keep endpoint scoring in separate frozen protocol",
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
                "packet_id": "NGC4088_EPSILON_CROSS_INPUT_REVIEW_PACKET",
                "n_obligations": len(obligations),
                "n_source_measurement_obligations": int(
                    (obligations["obligation_class"] == "SOURCE_MEASUREMENT").sum()
                ),
                "n_coefficient_rule_obligations": int(
                    (obligations["obligation_class"] == "COEFFICIENT_RULE").sum()
                ),
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "input_review_status": (
                    "INPUT_REVIEW_PACKET_NUMERIC_PROTOCOL_BOUND_READY"
                    if numeric_ready
                    else (
                        "INPUT_REVIEW_PACKET_FIRST_PASS_FILLED_NUMERIC_BOUND_BLOCKED"
                        if q_first_pass is not None and memory_first_pass is not None
                        else "INPUT_REVIEW_PACKET_READY_NUMERIC_BOUND_BLOCKED"
                    )
                ),
                "next_required_action": (
                    "evaluate_numeric_epsilon_cross_protocol_bound"
                    if numeric_ready
                    else (
                        "independently_review_source_responses_then_freeze_Bi_rule"
                        if q_first_pass is not None and memory_first_pass is not None
                        else "fill_qwarp_and_memory_responses_then_freeze_Bi_rule"
                    )
                ),
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return obligations, gates, summary


def write_report(
    obligations: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Epsilon-Cross Input Review Packet",
        "",
        "This packet consolidates the residual-blind inputs for turning",
        "`epsilon_cross` from a symbolic correction into a bounded correction.",
        "First-pass q/morphological-history source fills may be present. If an",
        "independent residual-blind review and a frozen B_i protocol rule are",
        "also present, this packet authorizes a numeric protocol bound. It does",
        "not compute endpoint scores.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Obligations",
        "",
        markdown_table(obligations),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The packet is an input-review artifact only. Any numeric epsilon_cross",
        "value authorized downstream is a residual-blind protocol upper bound,",
        "not an endpoint fit and not a final sharp Tau-side coefficient",
        "derivation.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_epsilon_cross_input_review_packet.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    obligations, gates, summary = build_packet()
    obligations.to_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_input_review_obligations.csv",
        index=False,
    )
    gates.to_csv(DATA / "s4g75_ngc4088_epsilon_cross_input_review_gate.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_input_review_summary.csv",
        index=False,
    )
    write_report(obligations, gates, summary)
    print("PAPER8_NGC4088_EPSILON_CROSS_INPUT_REVIEW_PACKET_COMPLETE")


if __name__ == "__main__":
    main()
