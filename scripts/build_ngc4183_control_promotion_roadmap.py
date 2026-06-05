#!/usr/bin/env python3
"""Build the NGC4183 weak-projection control promotion roadmap.

This roadmap keeps NGC4183 separate from accepted endpoint evidence.  It records
the exact promotion path from source-audit through optional null-control scoring
without allowing residual-driven shortcuts.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_control_promotion_roadmap_not_endpoint"
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


def s(path: str) -> pd.Series:
    return pd.read_csv(DATA / path).iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    source = s("ngc4183_mixed_overlay_source_audit_summary.csv")
    obs = s("ngc4183_mixed_overlay_observable_sheet_summary.csv")
    label = s("ngc4183_projection_outer_warp_label_summary.csv")
    formula = s("ngc4183_projection_outer_warp_formula_summary.csv")
    profile = s("ngc4183_tilted_ring_orientation_profile_summary.csv")
    upper = s("ngc4183_projection_gamma_upper_bound_summary.csv")
    weak = s("ngc4183_weak_projection_control_summary.csv")
    packet = s("ngc4183_tilted_ring_independent_review_summary.csv")
    visual = s("ngc4183_visual_review_readiness_summary.csv")
    review = s("ngc4183_tilted_ring_review_response_summary.csv")
    readiness = s("ngc4183_null_control_freeze_readiness_summary.csv")
    freeze = s("ngc4183_null_control_formula_freeze_summary.csv")
    accepted = s("ngc4183_accepted_null_control_summary.csv")
    scoring = s("ngc4183_weak_projection_null_control_scoring_summary.csv")

    rows = [
        {
            "stage_order": 1,
            "stage": "source_audit",
            "status": source["source_audit_status"],
            "state": "COMPLETE",
            "endpoint_scores_allowed": False,
            "next_action": "none",
        },
        {
            "stage_order": 2,
            "stage": "observable_sheet",
            "status": obs["observable_sheet_status"],
            "state": "PARTIAL_PASS",
            "endpoint_scores_allowed": False,
            "next_action": "do not use broad overlay fields until acquired",
        },
        {
            "stage_order": 3,
            "stage": "label_narrowing",
            "status": label["label_gate_status"],
            "state": "COMPLETE_FOR_DERIVATION",
            "endpoint_scores_allowed": False,
            "next_action": "keep narrowed projection/outer-warp caveated label",
        },
        {
            "stage_order": 4,
            "stage": "formula_shell",
            "status": formula["formula_derivation_status"],
            "state": "DERIVED_NOT_FROZEN",
            "endpoint_scores_allowed": False,
            "next_action": "coefficient/review gates required",
        },
        {
            "stage_order": 5,
            "stage": "tilted_ring_profile",
            "status": profile["tilted_ring_profile_status"],
            "state": "EXTRACTED_REVIEW_REQUIRED",
            "endpoint_scores_allowed": False,
            "next_action": "independent visual review response",
        },
        {
            "stage_order": 6,
            "stage": "projection_upper_bound",
            "status": upper["upper_bound_gate_status"],
            "state": "WEAK_BOUND_DERIVED",
            "endpoint_scores_allowed": False,
            "next_action": "preserve weak-control interpretation",
        },
        {
            "stage_order": 7,
            "stage": "weak_control_preflight",
            "status": weak["weak_control_preflight_status"],
            "state": "COMPLETE_NOT_ENDPOINT",
            "endpoint_scores_allowed": False,
            "next_action": "review before freeze",
        },
        {
            "stage_order": 8,
            "stage": "review_packet",
            "status": packet["review_packet_status"],
            "state": "PACKET_CREATED",
            "endpoint_scores_allowed": False,
            "next_action": "send/fill review response",
        },
        {
            "stage_order": 9,
            "stage": "visual_review_readiness",
            "status": visual["visual_review_readiness_status"],
            "state": "READY_RESPONSE_REQUIRED",
            "endpoint_scores_allowed": False,
            "next_action": (
                "review response already present; keep visual packet for audit trail"
                if bool(visual["review_response_received"])
                else "fill independent review response"
            ),
        },
        {
            "stage_order": 10,
            "stage": "review_response_intake",
            "status": review["review_response_intake_status"],
            "state": "BLOCKED" if not bool(review["response_received"]) else "RESPONSE_RECEIVED",
            "endpoint_scores_allowed": False,
            "next_action": (
                "preserve accepted source-review state or obtain explicit freeze authorization"
                if bool(review["response_received"])
                else "complete independent review response"
            ),
        },
        {
            "stage_order": 11,
            "stage": "freeze_readiness",
            "status": readiness["null_control_freeze_readiness_status"],
            "state": "BLOCKED" if not bool(readiness["formula_freeze_allowed"]) else "READY",
            "endpoint_scores_allowed": False,
            "next_action": "freeze only after review acceptance",
        },
        {
            "stage_order": 12,
            "stage": "formula_freeze",
            "status": freeze["null_control_formula_freeze_status"],
            "state": "BLOCKED" if not bool(freeze["formula_freeze_allowed"]) else "FROZEN",
            "endpoint_scores_allowed": False,
            "next_action": "accepted-control gate after freeze",
        },
        {
            "stage_order": 13,
            "stage": "accepted_control_gate",
            "status": accepted["accepted_null_control_gate_status"],
            "state": "BLOCKED" if not bool(accepted["accepted_control_allowed"]) else "ACCEPTED_NOT_SCORED",
            "endpoint_scores_allowed": False,
            "next_action": "separate scoring gate only if accepted-control passes",
        },
        {
            "stage_order": 14,
            "stage": "scoring_gate",
            "status": scoring["scoring_gate_status"],
            "state": (
                "SCORED_PRELIMINARY_CONTROL"
                if bool(scoring["endpoint_scores_allowed"])
                else
                "IMPLEMENTATION_REQUIRED"
                if bool(accepted["accepted_control_allowed"]) and not bool(scoring["endpoint_scores_allowed"])
                else "BLOCKED"
            ),
            "endpoint_scores_allowed": bool(scoring["endpoint_scores_allowed"]),
            "next_action": (
                "none"
                if bool(scoring["endpoint_scores_allowed"])
                else
                "implement reviewed scoring branch"
                if bool(accepted["accepted_control_allowed"]) and not bool(scoring["endpoint_scores_allowed"])
                else "complete review freeze and accepted-control gates first"
            ),
        },
    ]
    roadmap = pd.DataFrame(rows)
    roadmap["claim_boundary"] = CLAIM_BOUNDARY

    blocked = roadmap[
        roadmap["state"].str.contains(
            "BLOCKED|RESPONSE_REQUIRED|REVIEW_REQUIRED|IMPLEMENTATION_REQUIRED",
            regex=True,
        )
    ]
    actionable_blocked = blocked[
        blocked["stage"].isin(
            [
                "review_response_intake",
                "freeze_readiness",
                "formula_freeze",
                "accepted_control_gate",
                "scoring_gate",
            ]
        )
    ]
    if actionable_blocked.empty:
        next_blocker = None
        roadmap_status = "NGC4183_CONTROL_PROMOTION_ROADMAP_SCORING_COMPLETE_PRELIMINARY_CONTROL"
        first_stage = "none"
        first_status = "none"
        next_gate = "none"
    else:
        next_blocker = actionable_blocked.sort_values("stage_order").iloc[0]
        roadmap_status = (
            "NGC4183_CONTROL_PROMOTION_ROADMAP_READY_FOR_SCORING_IMPLEMENTATION"
            if str(next_blocker["stage"]) == "scoring_gate"
            else "NGC4183_CONTROL_PROMOTION_ROADMAP_COMPLETE_BLOCKED_AT_REVIEW_RESPONSE"
        )
        first_stage = str(next_blocker["stage"])
        first_status = str(next_blocker["status"])
        next_gate = str(next_blocker["next_action"]).replace(" ", "_")
    summary = pd.DataFrame(
        [
            {
                "control_roadmap_status": roadmap_status,
                "galaxy": GALAXY,
                "n_stages": len(roadmap),
                "n_complete_or_ready_stages": int(
                    roadmap["state"].str.contains("COMPLETE|READY|DERIVED|PACKET_CREATED|WEAK_BOUND|ACCEPTED_NOT_SCORED|SCORED_PRELIMINARY_CONTROL").sum()
                ),
                "n_blocked_or_review_required_stages": int(len(blocked)),
                "first_actionable_blocking_stage": first_stage,
                "first_actionable_blocking_status": first_status,
                "gamma_projection_upper_bound": float(upper["gamma_projection_upper_bound"]),
                "max_velocity_fractional_change": float(weak["max_velocity_fractional_change"]),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": next_gate,
            }
        ]
    )

    roadmap.to_csv(DATA / "ngc4183_control_promotion_roadmap.csv", index=False)
    summary.to_csv(DATA / "ngc4183_control_promotion_roadmap_summary.csv", index=False)

    report = f"""# NGC4183 Control Promotion Roadmap

Status: `{summary.iloc[0]["control_roadmap_status"]}`

This roadmap keeps NGC4183 separate from accepted endpoint evidence.  It tracks
the route from source audit to optional weak-projection/null-control scoring.

## Summary

{markdown_table(summary)}

## Roadmap

{markdown_table(roadmap)}

## Interpretation

NGC4183 is scientifically useful as a weak-projection/null-control candidate,
not as a strong projection endpoint.  The current source-side bound is:

```text
gamma_proj <= {float(upper["gamma_projection_upper_bound"]):.8f}
|Delta v|/v <= {float(weak["max_velocity_fractional_change"]):.8f}
```

The current first blocker is the next operational blocker in the lane. If the
source-review and freeze gates have already passed, the blocker moves forward to
scoring-branch implementation rather than remaining pinned to review state.
"""
    (REPORTS / "ngc4183_control_promotion_roadmap.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
