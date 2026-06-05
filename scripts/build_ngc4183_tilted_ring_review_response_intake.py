#!/usr/bin/env python3
"""Intake independent review response for NGC4183 tilted-ring profile.

This script records whether an independent source review has been received and
accepted, and whether that review also authorizes null-control freeze. It
exists to make the review gate reproducible and auditable.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_tilted_ring_review_response_intake_not_endpoint"


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


def accepted_or_corrected(value: object) -> bool:
    return str(value).strip().upper() in {
        "ACCEPT",
        "ACCEPTED",
        "PASS",
        "YES",
        "CORRECT",
        "CORRECTED",
        "ACCEPT_WITH_CORRECTIONS",
    }


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def independent_reviewer(value: object) -> bool:
    lowered = str(value).strip().lower()
    blocked_tokens = ["codex", "internal", "not_independent", "not-independent"]
    return bool(lowered) and lowered != "nan" and not any(
        token in lowered for token in blocked_tokens
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    template_path = DATA / "ngc4183_tilted_ring_independent_review_response_template.csv"
    response = pd.read_csv(template_path)
    row = response.iloc[0]

    required_fields = [
        "source_identity_decision",
        "radius_series_decision",
        "orientation_series_decision",
        "velocity_columns_decision",
        "upper_bound_conclusion_decision",
    ]
    missing = [
        field
        for field in required_fields
        if not str(row.get(field, "")).strip() or str(row.get(field, "")).lower() == "nan"
    ]
    all_required_accepted = not missing and all(
        accepted_or_corrected(row[field]) for field in required_fields
    )
    may_freeze = truthy(row.get("may_freeze_null_control_after_review", False))
    reviewer_is_independent = independent_reviewer(row.get("reviewer", ""))
    review_verdict = str(row.get("review_verdict", "")).strip()
    response_received = not missing and bool(review_verdict)
    formula_freeze_allowed = all_required_accepted and may_freeze and reviewer_is_independent

    intake = pd.DataFrame(
        [
            {
                "reviewer": str(row.get("reviewer", "")),
                "reviewer_is_independent": reviewer_is_independent,
                "response_received": response_received,
                "missing_response_fields": ";".join(missing),
                "all_required_accepted": all_required_accepted,
                "review_verdict": review_verdict,
                "may_freeze_null_control_after_review": may_freeze,
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_RI_G1_RESPONSE_RECEIVED",
                "gate_status": "PASS" if response_received else "BLOCKED",
                "evidence": "response template fields filled" if response_received else "response template still blank",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "fill independent review response" if not response_received else "none",
            },
            {
                "gate_id": "N4183_RI_G2_REQUIRED_ACCEPTANCE",
                "gate_status": "PASS" if all_required_accepted else "BLOCKED",
                "evidence": (
                    "all required fields accepted or corrected"
                    if all_required_accepted
                    else "required accept/correct decisions missing"
                ),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "accept/correct/rebuild profile before freeze",
            },
            {
                "gate_id": "N4183_RI_G3_INDEPENDENT_REVIEWER",
                "gate_status": "PASS" if reviewer_is_independent else "BLOCKED",
                "evidence": (
                    "reviewer identity is independent"
                    if reviewer_is_independent
                    else "response is internal/non-independent"
                ),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "obtain independent reviewer response",
            },
            {
                "gate_id": "N4183_RI_G4_NULL_CONTROL_FREEZE",
                "gate_status": "PASS" if formula_freeze_allowed else "BLOCKED",
                "evidence": "review allows null-control freeze" if may_freeze else "review has not authorized freeze",
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "null-control freeze script remains blocked" if not formula_freeze_allowed else "freeze script may run next",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    if formula_freeze_allowed:
        status = "NGC4183_TILTED_RING_REVIEW_RESPONSE_ACCEPTED_NULL_CONTROL_FREEZE_ALLOWED"
        next_gate = "freeze_null_control_formula"
    elif response_received and all_required_accepted and reviewer_is_independent:
        status = "NGC4183_TILTED_RING_REVIEW_RESPONSE_ACCEPTED_INDEPENDENT_SOURCE_ONLY_FREEZE_BLOCKED"
        next_gate = "review_freeze_authorization_or_preserve_source_only_block"
    elif response_received and all_required_accepted and not reviewer_is_independent:
        status = "NGC4183_TILTED_RING_REVIEW_RESPONSE_ACCEPTED_INTERNAL_FREEZE_BLOCKED"
        next_gate = "obtain_independent_review_response"
    else:
        status = "NGC4183_TILTED_RING_REVIEW_RESPONSE_MISSING_OR_BLOCKED"
        next_gate = "fill_independent_review_response"

    summary = pd.DataFrame(
        [
            {
                "review_response_intake_status": status,
                "reviewer_is_independent": reviewer_is_independent,
                "response_received": response_received,
                "all_required_accepted": all_required_accepted,
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": next_gate,
            }
        ]
    )

    intake.to_csv(DATA / "ngc4183_tilted_ring_review_response_intake.csv", index=False)
    gates.to_csv(DATA / "ngc4183_tilted_ring_review_response_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_tilted_ring_review_response_summary.csv", index=False)

    if not response_received:
        interpretation = (
            "No review response has been accepted yet. The source-review lane "
            "remains blocked before any freeze decision."
        )
    elif reviewer_is_independent and all_required_accepted and not formula_freeze_allowed:
        interpretation = (
            "An independent source review has been received and accepted, but it "
            "does not authorize null-control freeze. The source transcription is "
            "accepted while the formula-freeze lane remains blocked."
        )
    elif not reviewer_is_independent and all_required_accepted:
        interpretation = (
            "A non-independent internal response is present and useful as a "
            "consistency check, but an independent reviewer is still required "
            "before any freeze decision."
        )
    else:
        interpretation = (
            "A response is present, but at least one required review condition "
            "is still unresolved."
        )

    report = f"""# NGC4183 Tilted-Ring Review Response Intake

Status: `{summary.iloc[0]["review_response_intake_status"]}`

This intake validates the source-review response state. It does not authorize
endpoint scoring.

## Summary

{markdown_table(summary)}

## Intake

{markdown_table(intake)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Interpretation

{interpretation}

## Current Response Template

{markdown_table(response)}
"""
    (REPORTS / "ngc4183_tilted_ring_review_response_intake.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
