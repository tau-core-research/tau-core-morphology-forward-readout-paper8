#!/usr/bin/env python3
"""Gate NGC4183 for accepted weak-projection/null-control use.

This is the post-freeze control gate.  It stays blocked until the null-control
formula is actually frozen.  Even then, endpoint scoring must be handled by a
separate scoring script.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_accepted_null_control_gate_not_endpoint"
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

    freeze = pd.read_csv(DATA / "ngc4183_null_control_formula_freeze_summary.csv").iloc[0]
    visual = pd.read_csv(DATA / "ngc4183_visual_review_readiness_summary.csv").iloc[0]
    lane = pd.read_csv(DATA / "readout_lane_freeze_assignments.csv")
    lane_row = lane.loc[lane["galaxy"].eq(GALAXY)].iloc[0]

    formula_frozen = truthy(freeze["formula_freeze_allowed"])
    accepted_control_allowed = formula_frozen

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_ANC_G1_LANE",
                "gate_status": "PASS",
                "evidence": str(lane_row["lane_freeze_status"]),
                "accepted_control_allowed": accepted_control_allowed,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none for lane preflight",
            },
            {
                "gate_id": "N4183_ANC_G2_VISUAL_REVIEW_PACKET",
                "gate_status": "PASS",
                "evidence": str(visual["visual_review_readiness_status"]),
                "accepted_control_allowed": accepted_control_allowed,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "independent response still required" if not formula_frozen else "none",
            },
            {
                "gate_id": "N4183_ANC_G3_FORMULA_FREEZE",
                "gate_status": "PASS" if formula_frozen else "BLOCKED",
                "evidence": str(freeze["null_control_formula_freeze_status"]),
                "accepted_control_allowed": accepted_control_allowed,
                "endpoint_scores_allowed": False,
                "remaining_obligation": (
                    "none" if formula_frozen else "complete review and freeze null-control formula"
                ),
            },
            {
                "gate_id": "N4183_ANC_G4_SCORING",
                "gate_status": "BLOCKED",
                "evidence": "accepted-control gate is not a score",
                "accepted_control_allowed": accepted_control_allowed,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "separate scoring script after accepted-control gate passes",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "accepted_null_control_gate_status": (
                    "NGC4183_ACCEPTED_NULL_CONTROL_READY_NOT_SCORED"
                    if accepted_control_allowed
                    else "NGC4183_ACCEPTED_NULL_CONTROL_BLOCKED_FORMULA_NOT_FROZEN"
                ),
                "galaxy": GALAXY,
                "frozen_lane": str(lane_row["frozen_lane"]),
                "formula_freeze_status": str(freeze["null_control_formula_freeze_status"]),
                "accepted_control_allowed": accepted_control_allowed,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": (
                    "run_null_control_scoring_gate"
                    if accepted_control_allowed
                    else "complete_independent_review_response_and_formula_freeze"
                ),
            }
        ]
    )

    gates.to_csv(DATA / "ngc4183_accepted_null_control_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_accepted_null_control_summary.csv", index=False)

    report = f"""# NGC4183 Accepted Null-Control Gate

Status: `{summary.iloc[0]["accepted_null_control_gate_status"]}`

This gate decides whether NGC4183 may be treated as an accepted
weak-projection/null-control case.  It does not run endpoint scoring.

## Summary

{markdown_table(summary)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Interpretation

NGC4183 has a source-supported weak-projection control direction, but it cannot
be accepted as a frozen null-control case until the independent tilted-ring
review response is complete and the null-control formula freeze gate passes.
This keeps NGC4183 out of the accepted endpoint/control score table for now,
while preserving a clean path for later promotion.
"""
    (REPORTS / "ngc4183_accepted_null_control_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
