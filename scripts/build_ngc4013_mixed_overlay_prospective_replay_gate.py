#!/usr/bin/env python3
"""Build the NGC4013 mixed-overlay prospective replay gate.

This gate ties together:

    - the fresh source-freeze review,
    - the frozen mixed formula manifest,
    - the existing frozen-protocol score.

It explicitly labels the score as a prospective-protocol replay / continuity
check, not as retroactive endpoint validation.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4013"
CLAIM_BOUNDARY = "ngc4013_mixed_overlay_prospective_replay_gate_not_validation"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    review = pd.read_csv(
        DATA / "ngc4013_mixed_overlay_fresh_source_freeze_summary.csv"
    ).iloc[0]
    freeze = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_summary.csv").iloc[0]
    scores = pd.read_csv(DATA / "ngc4013_expdisk_wvo_frozen_protocol_scores.csv").iloc[0]
    lane = pd.read_csv(DATA / "readout_lane_freeze_assignments.csv")
    lane_row = lane.loc[lane["galaxy"].eq(GALAXY)].iloc[0]

    replay_allowed = (
        bool(review["future_prospective_scoring_allowed_after_separate_gate"])
        and bool(freeze["prospective_endpoint_protocol_ready"])
        and not bool(freeze["retrospective_endpoint_scores_allowed"])
        and str(lane_row["lane_freeze_status"])
        == "FROZEN_PASS_CAVEATED_PROSPECTIVE_ONLY"
    )

    score_summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": str(scores["formula_id"]),
                "n_points": int(scores["n_points"]),
                "rmse_expdisk_wvo_frozen_protocol": float(
                    scores["rmse_expdisk_wvo_frozen_protocol"]
                ),
                "rmse_exponential_disk": float(scores["rmse_exponential_disk"]),
                "rmse_warp_vertical_overlay": float(
                    scores["rmse_warp_vertical_overlay"]
                ),
                "rmse_tpg_v6": float(scores["rmse_tpg_v6"]),
                "rmse_mond": float(scores["rmse_mond"]),
                "frozen_minus_expdisk": float(scores["frozen_minus_expdisk"]),
                "frozen_minus_wvo": float(scores["frozen_minus_wvo"]),
                "frozen_minus_tpg_v6": float(scores["frozen_minus_tpg_v6"]),
                "score_role": "prospective_protocol_replay_continuity_check",
                "validation_claim_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4013_PRG1_SOURCE_FREEZE_REVIEW",
                "gate_status": "PASS_CAVEATED"
                if bool(review["source_rule_pass"])
                else "BLOCKED",
                "evidence": str(review["fresh_source_freeze_review_status"]),
                "remaining_obligation": "keep prior diagnostic score out of label evidence",
            },
            {
                "gate_id": "N4013_PRG2_LANE_FREEZE",
                "gate_status": "PASS_CAVEATED"
                if str(lane_row["lane_freeze_status"])
                == "FROZEN_PASS_CAVEATED_PROSPECTIVE_ONLY"
                else "BLOCKED",
                "evidence": str(lane_row["frozen_lane"]),
                "remaining_obligation": "no retroactive validation claim",
            },
            {
                "gate_id": "N4013_PRG3_FORMULA_FREEZE",
                "gate_status": "PASS"
                if bool(freeze["prospective_endpoint_protocol_ready"])
                else "BLOCKED",
                "evidence": str(freeze["formula_freeze_status"]),
                "remaining_obligation": "use same manifest unchanged in future population tests",
            },
            {
                "gate_id": "N4013_PRG4_RETROACTIVE_CLAIM_BOUNDARY",
                "gate_status": "PASS"
                if not bool(freeze["retrospective_endpoint_scores_allowed"])
                else "BLOCKED",
                "evidence": "retrospective_endpoint_scores_allowed=False",
                "remaining_obligation": "score can be continuity evidence only",
            },
            {
                "gate_id": "N4013_PRG5_REPLAY_SCORE",
                "gate_status": "PASS_RECORDED_NOT_VALIDATION" if replay_allowed else "BLOCKED",
                "evidence": (
                    f"frozen protocol RMSE={float(scores['rmse_expdisk_wvo_frozen_protocol']):.6g}"
                ),
                "remaining_obligation": "repeat prospectively on future predeclared cases",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["validation_claim_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "prospective_replay_gate_status": (
                    "NGC4013_MIXED_OVERLAY_PROSPECTIVE_REPLAY_RECORDED_NOT_VALIDATION"
                    if replay_allowed
                    else "NGC4013_MIXED_OVERLAY_PROSPECTIVE_REPLAY_BLOCKED"
                ),
                "lane_status": str(lane_row["lane_freeze_status"]),
                "formula_freeze_status": str(freeze["formula_freeze_status"]),
                "rmse_frozen_protocol": float(
                    scores["rmse_expdisk_wvo_frozen_protocol"]
                ),
                "beats_tpg_v6_by_km_s": -float(scores["frozen_minus_tpg_v6"]),
                "beats_expdisk_by_km_s": -float(scores["frozen_minus_expdisk"]),
                "beats_wvo_by_km_s": -float(scores["frozen_minus_wvo"]),
                "validation_claim_allowed": False,
                "endpoint_scores_allowed": False,
                "future_population_protocol_candidate": bool(replay_allowed),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    score_summary.to_csv(
        DATA / "ngc4013_mixed_overlay_prospective_replay_scores.csv", index=False
    )
    gates.to_csv(
        DATA / "ngc4013_mixed_overlay_prospective_replay_gates.csv", index=False
    )
    summary.to_csv(
        DATA / "ngc4013_mixed_overlay_prospective_replay_summary.csv", index=False
    )

    report = f"""# NGC4013 Mixed Overlay Prospective Replay Gate

Status: `{summary.iloc[0]['prospective_replay_gate_status']}`

This gate records the frozen NGC4013 mixed-overlay score under the new
readout-lane freeze discipline. It is a replay/continuity check, not
retroactive endpoint validation.

## Summary

{markdown_table(summary)}

## Score Summary

{markdown_table(score_summary)}

## Gates

{markdown_table(gates)}

## Interpretation

The frozen mixed-overlay protocol remains numerically strong for NGC4013:
`RMSE = {float(scores['rmse_expdisk_wvo_frozen_protocol']):.6g} km/s`, better
than the TPG/v6 proxy by `{(-float(scores['frozen_minus_tpg_v6'])):.6g} km/s`.
However, because this galaxy had already been inspected diagnostically, this
score is not an accepted endpoint validation. Its proper role is to define a
future population protocol candidate.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    (REPORTS / "ngc4013_mixed_overlay_prospective_replay_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
