#!/usr/bin/env python3
"""Scoring gate for NGC4183 weak-projection/null-control.

This gate stays blocked until the accepted null-control gate passes. After
that, it points to or records the reviewed interval-control scoring branch.
Observed velocities may be read only by that separate scoring branch.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_weak_projection_null_control_scoring_gate_not_endpoint"
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

    accepted = pd.read_csv(DATA / "ngc4183_accepted_null_control_summary.csv").iloc[0]
    freeze = pd.read_csv(DATA / "ngc4183_null_control_formula_freeze_summary.csv").iloc[0]
    roadmap = pd.read_csv(DATA / "ngc4183_control_promotion_roadmap_summary.csv").iloc[0]
    endpoint_summary_path = (
        DATA / "ngc4183_weak_projection_null_control_accepted_endpoint_summary.csv"
    )

    accepted_control_allowed = truthy(accepted["accepted_control_allowed"])
    formula_freeze_allowed = truthy(freeze["formula_freeze_allowed"])
    endpoint_summary = (
        pd.read_csv(endpoint_summary_path).iloc[0] if endpoint_summary_path.exists() else None
    )

    if accepted_control_allowed and endpoint_summary is not None:
        scoring_status = str(endpoint_summary["endpoint_status"])
        construction_reads_vobs = False
        scoring_would_read_vobs = True
        endpoint_scores_allowed = truthy(endpoint_summary["endpoint_scores_allowed"])
        blocker = "none"
    elif accepted_control_allowed:
        scoring_status = "NGC4183_ACCEPTED_NULL_CONTROL_SCORING_READY_NOT_RUN"
        construction_reads_vobs = False
        scoring_would_read_vobs = False
        endpoint_scores_allowed = False
        blocker = "run reviewed interval-control scoring branch"
    else:
        scoring_status = "NGC4183_WEAK_PROJECTION_NULL_CONTROL_SCORING_BLOCKED_PRE_ACCEPTANCE"
        construction_reads_vobs = False
        scoring_would_read_vobs = False
        endpoint_scores_allowed = False
        blocker = "accepted null-control gate has not passed"

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_SCORE_G1_ACCEPTED_CONTROL",
                "gate_status": "PASS" if accepted_control_allowed else "BLOCKED",
                "evidence": str(accepted["accepted_null_control_gate_status"]),
                "construction_reads_vobs": False,
                "scoring_reads_vobs": False,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "remaining_obligation": (
                    "none"
                    if accepted_control_allowed and endpoint_summary is not None
                    else "run reviewed interval-control scoring branch"
                    if accepted_control_allowed
                    else "complete review, freeze, and accepted-control gates"
                ),
            },
            {
                "gate_id": "N4183_SCORE_G2_FORMULA_FREEZE",
                "gate_status": "PASS" if formula_freeze_allowed else "BLOCKED",
                "evidence": str(freeze["null_control_formula_freeze_status"]),
                "construction_reads_vobs": False,
                "scoring_reads_vobs": False,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "remaining_obligation": (
                    "none" if formula_freeze_allowed else "formula freeze required"
                ),
            },
            {
                "gate_id": "N4183_SCORE_G3_NO_PREMATURE_VOBS",
                "gate_status": "PASS",
                "evidence": "blocked branch does not read observed velocities",
                "construction_reads_vobs": construction_reads_vobs,
                "scoring_reads_vobs": scoring_would_read_vobs,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "remaining_obligation": "keep blocked branch vobs-free",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "scoring_gate_status": scoring_status,
                "galaxy": GALAXY,
                "accepted_control_allowed": accepted_control_allowed,
                "formula_freeze_allowed": formula_freeze_allowed,
                "construction_reads_vobs": construction_reads_vobs,
                "scoring_reads_vobs": scoring_would_read_vobs,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "primary_blocker": blocker,
                "control_roadmap_status": str(roadmap["control_roadmap_status"]),
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": (
                    "none"
                    if accepted_control_allowed and endpoint_summary is not None
                    else "run_ngc4183_weak_projection_null_control_accepted_endpoint"
                    if accepted_control_allowed
                    else "complete_independent_review_response_and_formula_freeze"
                ),
            }
        ]
    )

    gates.to_csv(DATA / "ngc4183_weak_projection_null_control_scoring_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_weak_projection_null_control_scoring_summary.csv", index=False)

    interpretation = (
        "The accepted null-control interval endpoint has been run from the frozen "
        "manifest. Observed velocities were read only in the scoring block, and "
        "the branch remains interval-based rather than a residual-tuned point fit."
        if endpoint_summary is not None and accepted_control_allowed
        else "The scoring path is intentionally blocked until the accepted null-control gate "
        "passes. After that, a separate reviewed scoring branch may read observed "
        "velocities. The branch remains interval-based and does not choose a post-hoc "
        "point coefficient from residuals."
    )

    report = f"""# NGC4183 Weak-Projection Null-Control Scoring Gate

Status: `{summary.iloc[0]["scoring_gate_status"]}`

This gate controls when the separate NGC4183 interval-control scoring branch
may read observed rotation velocities.

## Summary

{markdown_table(summary)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Interpretation

{interpretation}
"""
    (REPORTS / "ngc4183_weak_projection_null_control_scoring_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
