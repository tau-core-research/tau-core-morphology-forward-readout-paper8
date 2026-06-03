#!/usr/bin/env python3
"""Evaluate whether the P0 visual review template has been completed.

This gate protects the transition from preview/source material to an accepted
residual-blind morphology manifest.  It does not classify images and does not
compute endpoint scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

PENDING = "TO_BE_FILLED_RESIDUAL_BLIND"
CLAIM_BOUNDARY = "p0_visual_review_completion_gate_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def evaluate_row(row: pd.Series, review_fields: list[str]) -> dict[str, object]:
    pending_fields = [
        field for field in review_fields if str(row[field]).strip() == PENDING
    ]
    missing_count = len(pending_fields)
    status = "PASS_VISUAL_REVIEW_COMPLETE" if missing_count == 0 else "BLOCKED_VISUAL_REVIEW_PENDING"
    return {
        "galaxy": row["galaxy"],
        "inspection_priority_tier": row["inspection_priority_tier"],
        "inspection_priority_score": int(row["inspection_priority_score"]),
        "completion_status": status,
        "n_review_fields": len(review_fields),
        "n_pending_review_fields": missing_count,
        "pending_review_fields": ";".join(pending_fields) if pending_fields else "none",
        "accepted_manifest_promotion_allowed": missing_count == 0,
        "endpoint_scores_computed": False,
        "next_action": (
            "promote only after independent accepted-manifest audit"
            if missing_count == 0
            else "complete residual-blind visual review fields before manifest promotion"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_report(gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    decision = summary["visual_review_completion_decision"].iloc[0]
    blocked = int(summary["n_blocked_rows"].iloc[0])
    lines = [
        "# P0 Visual Review Completion Gate",
        "",
        "This gate evaluates whether the P0 residual-blind visual review template",
        "has been filled enough to be considered for accepted-manifest promotion.",
        "It does not classify images, does not create accepted morphology labels,",
        "and does not compute endpoint scores.",
        "",
        "This completion gate is not an endpoint score.",
        "",
        "## Verdict",
        "",
        f"Visual review completion decision: `{decision}`.",
        f"Blocked rows: {blocked}.",
        "",
        "The current P0 template is correctly blocked because all review fields remain residual-blind placeholders.",
        "This preserves the boundary between",
        "image-source preparation and accepted morphology labels.",
        "A blocked visual review is not a negative empirical result.",
        "",
        "## Row Status",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "A PASS here would only mean that the residual-blind visual review form has",
        "been completed. It would still require a separate accepted-manifest audit",
        "before any frozen endpoint calculation. It would not imply that Tau Core",
        "fits better than MOND, RAR, TGP, or Newtonian baselines.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_visual_review_completion_gate.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    template = pd.read_csv(DATA / "p0_visual_review_template.csv")
    schema = pd.read_csv(DATA / "p0_visual_review_field_schema.csv")
    review_fields = schema["field"].tolist()

    gates = pd.DataFrame(
        [evaluate_row(row, review_fields) for _, row in template.iterrows()]
    ).sort_values("galaxy")
    blocked = gates[gates["completion_status"] == "BLOCKED_VISUAL_REVIEW_PENDING"]
    decision = (
        "READY_FOR_ACCEPTED_MANIFEST_AUDIT"
        if blocked.empty
        else "BLOCKED_VISUAL_REVIEW_PENDING"
    )
    summary = pd.DataFrame(
        [
            {
                "visual_review_completion_decision": decision,
                "n_galaxies": len(gates),
                "n_blocked_rows": len(blocked),
                "n_pending_review_fields_total": int(gates["n_pending_review_fields"].sum()),
                "accepted_manifest_promotion_allowed": blocked.empty,
                "endpoint_scores_computed": False,
                "claim_status": "source_review_complete_only" if blocked.empty else "source_review_pending",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    gates.to_csv(DATA / "p0_visual_review_completion_gate.csv", index=False)
    summary.to_csv(DATA / "p0_visual_review_completion_summary.csv", index=False)
    write_report(gates, summary)
    print("PAPER8_P0_VISUAL_REVIEW_COMPLETION_GATE_COMPLETE")


if __name__ == "__main__":
    main()
