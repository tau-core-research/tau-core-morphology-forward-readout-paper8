#!/usr/bin/env python3
"""Validate the NGC7331 q_warp observable-choice review response.

This is an intake gate, not a reviewer. With the current pending response it
must remain blocked. If a future response is filled, the gate checks that the
review uses an allowed decision, avoids forbidden inputs, and does not claim
formula-freeze readiness unless q, sign, and epsilon handling are all present.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_qwarp_observable_choice_review_intake_not_endpoint"
PENDING = "PENDING_INDEPENDENT_REVIEW"


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


def split_tokens(value: object) -> set[str]:
    if pd.isna(value):
        return set()
    text = str(value).strip()
    if not text or text == PENDING:
        return set()
    return {item.strip() for item in text.replace(",", ";").split(";") if item.strip()}


def bool_value(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def parse_float(value: object) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    packet = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_review_packet.csv").iloc[0]
    options = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_review_options.csv")
    response = pd.read_csv(
        DATA / "ngc7331_qwarp_observable_choice_review_response_template.csv"
    ).iloc[0]

    allowed_decisions = set(str(packet["accepted_review_outcomes"]).split(";"))
    forbidden_inputs = set(str(packet["forbidden_inputs"]).split(";"))
    allowed_sources = set(str(packet["allowed_source_inputs"]).split(";"))
    decision = str(response["review_decision"])
    response_pending = decision == PENDING
    response_sources = split_tokens(response["source_inputs_used"])
    response_forbidden = split_tokens(response["forbidden_inputs_used"])
    forbidden_overlap = sorted(forbidden_inputs & response_forbidden)
    source_unknown = sorted(response_sources - allowed_sources)

    q_centroid = float(packet["q_centroid_mid"])
    q_envelope = float(packet["q_envelope_mid"])
    q_value = parse_float(response["accepted_q_warp_value"])
    q_interval_text = str(response["accepted_q_warp_interval"])

    decision_allowed = (decision in allowed_decisions) and not response_pending
    forbidden_clean = (not forbidden_overlap) and not response_pending
    sources_clean = (not source_unknown) and bool(response_sources) and not response_pending

    numeric_q_valid = False
    interval_valid = False
    if decision == "ACCEPT_CENTROID":
        numeric_q_valid = q_value is not None and math.isclose(q_value, q_centroid, rel_tol=1e-9)
    elif decision == "ACCEPT_ENVELOPE":
        numeric_q_valid = q_value is not None and math.isclose(q_value, q_envelope, rel_tol=1e-9)
    elif decision == "CARRY_INTERVAL":
        interval_valid = (
            str(q_centroid) in q_interval_text
            or f"{q_centroid:.12g}" in q_interval_text
        ) and (
            str(q_envelope) in q_interval_text
            or f"{q_envelope:.12g}" in q_interval_text
        )
    elif decision == "REJECT_Q_FREEZE":
        numeric_q_valid = str(response["accepted_q_warp_value"]) in {
            "not_applicable",
            PENDING,
            "",
        }

    q_decision_valid = decision_allowed and (
        numeric_q_valid or interval_valid or decision == "REJECT_Q_FREEZE"
    )
    sign_ready = str(response["sign_convention_decision"]) not in {PENDING, "", "nan"}
    epsilon_ready = str(response["epsilon_cross_decision"]) not in {PENDING, "", "nan"}
    freeze_claimed = bool_value(response["formula_freeze_allowed_after_review"])
    formula_freeze_allowed = (
        q_decision_valid
        and forbidden_clean
        and sources_clean
        and sign_ready
        and epsilon_ready
        and freeze_claimed
        and decision != "REJECT_Q_FREEZE"
    )

    validation = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "validation_id": "N7331_QWARP_REVIEW_INTAKE_V1",
                "response_pending": response_pending,
                "decision_allowed": decision_allowed,
                "q_decision_valid": q_decision_valid,
                "sources_clean": sources_clean,
                "forbidden_clean": forbidden_clean,
                "sign_ready": sign_ready,
                "epsilon_ready": epsilon_ready,
                "formula_freeze_claimed": freeze_claimed,
                "formula_freeze_allowed": formula_freeze_allowed,
                "forbidden_overlap": ";".join(forbidden_overlap) if forbidden_overlap else "none",
                "unknown_sources": ";".join(source_unknown) if source_unknown else "none",
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_QINT1_RESPONSE_PRESENT",
                "gate_status": "BLOCKED_RESPONSE_PENDING" if response_pending else "PASS",
                "evidence": f"review_decision={decision}",
                "remaining_obligation": "fill independent review response" if response_pending else "none",
            },
            {
                "gate_id": "N7331_QINT2_ALLOWED_DECISION",
                "gate_status": "PASS" if decision_allowed else "BLOCKED",
                "evidence": f"decision={decision}; allowed={';'.join(sorted(allowed_decisions))}",
                "remaining_obligation": "select exactly one allowed decision",
            },
            {
                "gate_id": "N7331_QINT3_FORBIDDEN_INPUTS",
                "gate_status": "PASS" if forbidden_clean else "BLOCKED",
                "evidence": f"forbidden_overlap={validation.iloc[0]['forbidden_overlap']}",
                "remaining_obligation": "remove forbidden review inputs",
            },
            {
                "gate_id": "N7331_QINT4_SOURCE_INPUTS",
                "gate_status": "PASS" if sources_clean else "BLOCKED",
                "evidence": f"unknown_sources={validation.iloc[0]['unknown_sources']}",
                "remaining_obligation": "cite only allowed source-side inputs",
            },
            {
                "gate_id": "N7331_QINT5_Q_VALUE_OR_INTERVAL",
                "gate_status": "PASS" if q_decision_valid else "BLOCKED",
                "evidence": f"decision={decision}; q_value={response['accepted_q_warp_value']}; interval={response['accepted_q_warp_interval']}",
                "remaining_obligation": "make q value/interval consistent with selected review option",
            },
            {
                "gate_id": "N7331_QINT6_SIGN_EPSILON",
                "gate_status": "PASS" if sign_ready and epsilon_ready else "BLOCKED",
                "evidence": f"sign_ready={sign_ready}; epsilon_ready={epsilon_ready}",
                "remaining_obligation": "fill sign convention and epsilon_cross handling",
            },
            {
                "gate_id": "N7331_QINT7_FORMULA_FREEZE",
                "gate_status": "PASS" if formula_freeze_allowed else "BLOCKED",
                "evidence": f"formula_freeze_allowed={formula_freeze_allowed}",
                "remaining_obligation": "all intake gates plus explicit freeze claim required",
            },
            {
                "gate_id": "N7331_QINT8_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "intake validates forbidden inputs and does not score endpoint",
                "remaining_obligation": "none at intake level",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    if response_pending:
        status = "NGC7331_QWARP_REVIEW_INTAKE_BLOCKED_RESPONSE_PENDING"
    elif formula_freeze_allowed:
        status = "NGC7331_QWARP_REVIEW_INTAKE_FORMULA_FREEZE_INPUT_READY_NOT_ENDPOINT"
    else:
        status = "NGC7331_QWARP_REVIEW_INTAKE_RESPONSE_REJECTED_OR_INCOMPLETE"

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "review_intake_status": status,
                "response_pending": response_pending,
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "fill independent review response"
                    if response_pending
                    else "proceed to exact-transfer formula freeze gate"
                    if formula_freeze_allowed
                    else "repair incomplete/rejected response"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    validation.to_csv(DATA / "ngc7331_qwarp_observable_choice_review_intake_validation.csv", index=False)
    gates.to_csv(DATA / "ngc7331_qwarp_observable_choice_review_intake_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_qwarp_observable_choice_review_intake_summary.csv", index=False)

    if response_pending:
        status_note = [
            "This intake validates the review response. It currently blocks because",
            "the independent review response is still pending. It does not score an endpoint.",
        ]
    elif formula_freeze_allowed:
        status_note = [
            "This intake validates the review response. The response now passes the",
            "allowed-decision, source-input, forbidden-input, q, sign, and epsilon",
            "checks needed for formula-freeze input readiness. It still does not score",
            "an endpoint.",
        ]
    else:
        status_note = [
            "This intake validates the review response. A response is present, but at",
            "least one required source-side consistency gate remains blocked. It does",
            "not score an endpoint.",
        ]

    report = [
        "# NGC7331 q_warp Observable-Choice Review Intake",
        "",
        f"Status: `{status}`.",
        "",
        *status_note,
        "",
        "## Validation",
        "",
        markdown_table(validation),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
    ]
    (REPORTS / "ngc7331_qwarp_observable_choice_review_intake.md").write_text(
        "\n".join(report), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
