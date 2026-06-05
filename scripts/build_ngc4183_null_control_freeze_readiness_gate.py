#!/usr/bin/env python3
"""Gate NGC4183 weak-projection null-control formula freeze readiness."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_null_control_freeze_readiness_gate_not_endpoint"
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


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    weak = pd.read_csv(DATA / "ngc4183_weak_projection_control_summary.csv").iloc[0]
    review = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_summary.csv").iloc[0]
    packet = pd.read_csv(DATA / "ngc4183_tilted_ring_independent_review_summary.csv").iloc[0]

    review_accepts_freeze = truthy(review["formula_freeze_allowed"])
    weak_control_ready = (
        str(weak["weak_control_preflight_status"])
        == "NGC4183_WEAK_PROJECTION_CONTROL_PREFLIGHT_COMPLETE_NOT_ENDPOINT"
    )
    gamma_bound = float(weak["gamma_projection_upper_bound"])
    velocity_fraction = float(weak["max_velocity_fractional_change"])

    readiness = pd.DataFrame(
        [
            {
                "readiness_item": "weak_control_preflight",
                "status": "PASS" if weak_control_ready else "BLOCKED",
                "evidence": str(weak["weak_control_preflight_status"]),
                "required_for_freeze": True,
            },
            {
                "readiness_item": "independent_review_packet",
                "status": "PASS",
                "evidence": str(packet["review_packet_status"]),
                "required_for_freeze": True,
            },
            {
                "readiness_item": "independent_review_response",
                "status": "PASS" if review_accepts_freeze else "BLOCKED",
                "evidence": str(review["review_response_intake_status"]),
                "required_for_freeze": True,
            },
            {
                "readiness_item": "source_side_bound",
                "status": "PASS",
                "evidence": f"gamma_bound={gamma_bound:.6g}; max |Delta v|/v={velocity_fraction:.6g}",
                "required_for_freeze": True,
            },
            {
                "readiness_item": "endpoint_scoring",
                "status": "BLOCKED",
                "evidence": "freeze readiness is not endpoint scoring",
                "required_for_freeze": False,
            },
        ]
    )

    formula_freeze_allowed = weak_control_ready and review_accepts_freeze

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_NCFR_G1_PREFLIGHT",
                "gate_status": "PASS" if weak_control_ready else "BLOCKED",
                "evidence": str(weak["weak_control_preflight_status"]),
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none" if weak_control_ready else "complete weak-control preflight",
            },
            {
                "gate_id": "N4183_NCFR_G2_REVIEW_RESPONSE",
                "gate_status": "PASS" if review_accepts_freeze else "BLOCKED",
                "evidence": str(review["review_response_intake_status"]),
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": False,
                "remaining_obligation": (
                    "none" if review_accepts_freeze else "independent review response must authorize null-control freeze"
                ),
            },
            {
                "gate_id": "N4183_NCFR_G3_FORMULA_FREEZE",
                "gate_status": "READY" if formula_freeze_allowed else "BLOCKED",
                "evidence": "all required freeze preconditions pass" if formula_freeze_allowed else "review response missing or blocked",
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": False,
                "remaining_obligation": (
                    "run separate null-control formula freeze script"
                    if formula_freeze_allowed
                    else "do not freeze formula yet"
                ),
            },
            {
                "gate_id": "N4183_NCFR_G4_ENDPOINT_SCORE",
                "gate_status": "BLOCKED",
                "evidence": "null-control freeze readiness is not endpoint validation",
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "endpoint scoring would require a separate accepted endpoint gate",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "null_control_freeze_readiness_status": (
                    "NGC4183_NULL_CONTROL_FREEZE_READY_REVIEW_ACCEPTED_NOT_ENDPOINT"
                    if formula_freeze_allowed
                    else "NGC4183_NULL_CONTROL_FREEZE_BLOCKED_REVIEW_REQUIRED"
                ),
                "galaxy": GALAXY,
                "gamma_projection_upper_bound": gamma_bound,
                "max_velocity_fractional_change": velocity_fraction,
                "weak_control_preflight_pass": weak_control_ready,
                "review_accepts_freeze": review_accepts_freeze,
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": (
                    "build_null_control_formula_freeze"
                    if formula_freeze_allowed
                    else "complete_independent_review_response"
                ),
            }
        ]
    )

    readiness.to_csv(DATA / "ngc4183_null_control_freeze_readiness_items.csv", index=False)
    gates.to_csv(DATA / "ngc4183_null_control_freeze_readiness_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_null_control_freeze_readiness_summary.csv", index=False)

    report = f"""# NGC4183 Null-Control Freeze Readiness Gate

Status: `{summary.iloc[0]["null_control_freeze_readiness_status"]}`

This gate decides whether the weak-projection/null-control formula may be
frozen.  It does not run endpoint scoring.

## Summary

{markdown_table(summary)}

## Readiness Items

{markdown_table(readiness)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Interpretation

The source-side null-control bound is already derived:

```text
gamma_proj <= {gamma_bound:.8f}
|Delta v|/v <= {velocity_fraction:.8f}
```

But the formula cannot be frozen until the review response explicitly
authorizes null-control freeze. An accepted independent source review without
freeze authorization is still not enough. This keeps NGC4183 as a controlled
pre-endpoint case rather than a retrofitted endpoint.
"""
    (REPORTS / "ngc4183_null_control_freeze_readiness_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
