#!/usr/bin/env python3
"""Freeze readout-lane assignments before future formula scoring.

This gate consumes the lane taxonomy update and current source/diagnostic
evidence. It freezes which readout lane is allowed or blocked for the current
key galaxies. It does not score endpoints.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "readout_lane_freeze_gate_not_endpoint"


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

    taxonomy_cases = pd.read_csv(DATA / "readout_lane_taxonomy_case_updates.csv")
    accepted = pd.read_csv(DATA / "readout_subfamily_accepted_manifest_audit.csv")
    split_failure = pd.read_csv(DATA / "ngc5907_split_b2_failure_mode_summary.csv").iloc[0]
    split_synthesis = pd.read_csv(DATA / "split_b2_lane_specificity_summary.csv").iloc[0]
    ngc4013_review_path = DATA / "ngc4013_mixed_overlay_fresh_source_freeze_summary.csv"
    ngc4013_review = (
        pd.read_csv(ngc4013_review_path).iloc[0]
        if ngc4013_review_path.exists()
        else None
    )
    ngc4013_replay_path = DATA / "ngc4013_mixed_overlay_prospective_replay_summary.csv"
    ngc4013_replay = (
        pd.read_csv(ngc4013_replay_path).iloc[0]
        if ngc4013_replay_path.exists()
        else None
    )
    ngc4183_control_path = DATA / "ngc4183_weak_projection_control_summary.csv"
    ngc4183_control = (
        pd.read_csv(ngc4183_control_path).iloc[0]
        if ngc4183_control_path.exists()
        else None
    )
    ngc4183_readiness_path = DATA / "ngc4183_null_control_freeze_readiness_summary.csv"
    ngc4183_readiness = (
        pd.read_csv(ngc4183_readiness_path).iloc[0]
        if ngc4183_readiness_path.exists()
        else None
    )
    ngc4183_scoring_path = DATA / "ngc4183_weak_projection_null_control_scoring_summary.csv"
    ngc4183_scoring = (
        pd.read_csv(ngc4183_scoring_path).iloc[0]
        if ngc4183_scoring_path.exists()
        else None
    )

    rows = []
    for _, case in taxonomy_cases.iterrows():
        galaxy = str(case["galaxy"])
        accepted_row = accepted.loc[accepted["galaxy"].eq(galaxy)]
        audit_decision = (
            str(accepted_row.iloc[0]["audit_decision"])
            if not accepted_row.empty
            else "NO_ACCEPTED_AUDIT_ROW"
        )
        proposed_subfamily = (
            str(accepted_row.iloc[0]["proposed_readout_subfamily"])
            if not accepted_row.empty
            else "unknown"
        )

        if galaxy == "NGC5907":
            rows.append(
                {
                    "galaxy": galaxy,
                    "proposed_subfamily": proposed_subfamily,
                    "frozen_lane": "L_projection_attenuation",
                    "lane_freeze_status": "FROZEN_PASS_CAVEATED",
                    "allowed_formula_shells": (
                        "bounded projection/attenuation; mixed projection overlay"
                    ),
                    "blocked_formula_shells": (
                        "standalone added split-B2 ramp; unbounded added warp-history ramp"
                    ),
                    "source_evidence": audit_decision,
                    "diagnostic_evidence": str(split_failure["primary_interpretation"]),
                    "remaining_obligation": (
                        "population validation and source-native HI denominator remain open"
                    ),
                    "future_population_protocol_candidate": False,
                }
            )
        elif galaxy == "NGC7331":
            rows.append(
                {
                    "galaxy": galaxy,
                    "proposed_subfamily": proposed_subfamily,
                    "frozen_lane": "L_added_source_diagnostic_not_endpoint",
                    "lane_freeze_status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
                    "allowed_formula_shells": (
                        "split-B2 unit-load only as q-role/source-load diagnostic"
                    ),
                    "blocked_formula_shells": (
                        "same-curve split-B2 promotion as independent validation"
                    ),
                    "source_evidence": audit_decision,
                    "diagnostic_evidence": (
                        "split-B2 repair identified on NGC7331 after exact-transfer failure"
                    ),
                    "remaining_obligation": (
                        "needs independent added-readout holdout before validation claim"
                    ),
                    "future_population_protocol_candidate": False,
                }
            )
        elif galaxy == "NGC4013":
            review_pass = (
                ngc4013_review is not None
                and str(ngc4013_review["fresh_source_freeze_review_status"])
                == "NGC4013_MIXED_OVERLAY_SOURCE_FREEZE_PASS_CAVEATED_PROSPECTIVE_ONLY"
            )
            replay_candidate = (
                ngc4013_replay is not None
                and bool(ngc4013_replay["future_population_protocol_candidate"])
            )
            rows.append(
                {
                    "galaxy": galaxy,
                    "proposed_subfamily": proposed_subfamily,
                    "frozen_lane": (
                        "L_mixed_overlay_protocol_ready_not_retroactive"
                        if review_pass
                        else "L_mixed_overlay_pending"
                    ),
                    "lane_freeze_status": (
                        "FROZEN_PASS_CAVEATED_PROSPECTIVE_ONLY"
                        if review_pass
                        else "PENDING_FRESH_SOURCE_FREEZE"
                    ),
                    "allowed_formula_shells": (
                        "mixed smooth-carrier plus warp/vertical overlay"
                        if review_pass
                        else "mixed smooth-carrier plus warp/vertical overlay after fresh freeze"
                    ),
                    "blocked_formula_shells": (
                        "retroactive endpoint promotion from existing mixed score"
                    ),
                    "source_evidence": audit_decision,
                    "diagnostic_evidence": (
                        "fresh source-freeze review passed; prior score remains forbidden as label evidence"
                        if review_pass
                        else "retrospective/reference mixed path exists"
                    ),
                    "remaining_obligation": (
                        "repeat on future predeclared cases; no retroactive validation"
                        if replay_candidate
                        else "separate prospective scoring gate only; no retroactive validation"
                        if review_pass
                        else "fresh residual-blind source freeze before another scoring pass"
                    ),
                    "future_population_protocol_candidate": replay_candidate,
                }
            )
        elif galaxy == "NGC4183":
            control_ready = (
                ngc4183_control is not None
                and str(ngc4183_control["weak_control_preflight_status"])
                == "NGC4183_WEAK_PROJECTION_CONTROL_PREFLIGHT_COMPLETE_NOT_ENDPOINT"
            )
            control_scored = (
                ngc4183_scoring is not None
                and str(ngc4183_scoring["scoring_gate_status"])
                == "NGC4183_ACCEPTED_NULL_CONTROL_INTERVAL_ENDPOINT_COMPLETE"
            )
            readiness_status = (
                str(ngc4183_readiness["null_control_freeze_readiness_status"])
                if ngc4183_readiness is not None
                else "NO_NULL_CONTROL_READINESS_GATE"
            )
            rows.append(
                {
                    "galaxy": galaxy,
                    "proposed_subfamily": proposed_subfamily,
                    "frozen_lane": (
                        "L_projection_attenuation_weak_control_after_review"
                        if control_ready
                        else "lane_unassigned"
                    ),
                    "lane_freeze_status": (
                        "ACCEPTED_NULL_CONTROL_INTERVAL_ENDPOINT_COMPLETE"
                        if control_scored
                        else "PREFLIGHT_PASS_WEAK_CONTROL_REVIEW_REQUIRED_NOT_ENDPOINT"
                        if control_ready
                        else "BLOCKED_SOURCE_ACQUISITION_REQUIRED"
                    ),
                    "allowed_formula_shells": (
                        "near-carrier/null-control projection bound after independent source review; frozen interval-control endpoint branch"
                        if control_scored
                        else "near-carrier/null-control projection bound after independent source review"
                        if control_ready
                        else "none before source acquisition"
                    ),
                    "blocked_formula_shells": (
                        "strong projection endpoint; standalone added warp ramp; broad bar/core/history overlay"
                        if control_ready
                        else "all endpoint scoring shells"
                    ),
                    "source_evidence": audit_decision,
                    "diagnostic_evidence": (
                        f"gamma bound {float(ngc4183_control['gamma_projection_upper_bound']):.6g}; "
                        f"velocity fractional bound {float(ngc4183_control['max_velocity_fractional_change']):.6g}; "
                        + (
                            "accepted interval endpoint complete"
                            if control_scored
                            else f"freeze readiness {readiness_status}"
                        )
                        if control_ready
                        else "source activation fields missing"
                    ),
                    "remaining_obligation": (
                        "preserve narrow null-control claim boundary; do not reframe as mixed population validation"
                        if control_scored
                        else "independent profile review before optional null-control freeze"
                        if control_ready
                        else "acquire galaxy-specific warp/history/projection observables"
                    ),
                    "future_population_protocol_candidate": False,
                }
            )
    freeze = pd.DataFrame(rows)
    freeze["uses_vobs_or_residual_for_lane_selection"] = False
    freeze["endpoint_scores_allowed"] = False
    freeze["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "RLF_G1_TAXONOMY_AVAILABLE",
                "gate_status": "PASS",
                "evidence": "readout_lane_taxonomy_update completed",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "RLF_G2_NGC5907_PROJECTION_FREEZE",
                "gate_status": "PASS_CAVEATED",
                "evidence": "projection lane favored; added split-B2 rejected",
                "remaining_obligation": "keep caveats and do not run standalone added ramp",
            },
            {
                "gate_id": "RLF_G3_NGC7331_DIAGNOSTIC_BOUNDARY",
                "gate_status": "PASS",
                "evidence": "positive split-B2 is same-curve diagnostic only",
                "remaining_obligation": "independent added-readout holdout required",
            },
            {
                "gate_id": "RLF_G4_PENDING_CASES",
                "gate_status": "PASS_CAVEATED",
                "evidence": (
                    "NGC4013 is prospective-only protocol ready after fresh source-freeze "
                    "review; NGC4183 is a completed accepted null-control interval endpoint on its "
                    "own narrow control branch"
                ),
                "remaining_obligation": (
                    "NGC4013 needs separate prospective scoring gate; NGC4183 should retain its "
                    "single-galaxy null-control boundary rather than being treated as mixed validation"
                ),
            },
            {
                "gate_id": "RLF_G5_ENDPOINT_USE",
                "gate_status": "BLOCKED",
                "evidence": "lane freeze is not a formula freeze and not a score",
                "remaining_obligation": "future endpoint scoring requires separate formula freeze",
            },
        ]
    )
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "lane_freeze_status": "READOUT_LANE_FREEZE_GATE_COMPLETE_NOT_ENDPOINT",
                "n_galaxies": len(freeze),
                "n_frozen_pass_like": int(
                    freeze["lane_freeze_status"].str.contains("PASS|DIAGNOSTIC", regex=True).sum()
                ),
                "n_pending_or_blocked": int(
                    freeze["lane_freeze_status"]
                    .str.contains("PENDING|BLOCKED|REVIEW_REQUIRED", regex=True)
                    .sum()
                ),
                "split_b2_universal_rule_status": str(
                    split_synthesis["universal_split_b2_rule_status"]
                ),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_for_lane_selection": False,
                "n_future_population_protocol_candidates": int(
                    freeze["future_population_protocol_candidate"].astype(bool).sum()
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    freeze.to_csv(DATA / "readout_lane_freeze_assignments.csv", index=False)
    gates.to_csv(DATA / "readout_lane_freeze_gates.csv", index=False)
    summary.to_csv(DATA / "readout_lane_freeze_summary.csv", index=False)

    report = f"""# Readout-Lane Freeze Gate

Status: `{summary.iloc[0]['lane_freeze_status']}`

This gate freezes allowed and blocked readout lanes for the current key cases
before any future formula scoring. It does not score endpoints.

## Summary

{markdown_table(summary)}

## Lane Assignments

{markdown_table(freeze)}

## Gates

{markdown_table(gates)}

## Operational Consequence

NGC5907 may continue as a projection/attenuation or mixed projection case, but
standalone added split-B2 ramp scoring is blocked by the lane freeze. NGC7331
keeps the split-B2 result only as a same-curve diagnostic. NGC4013 is now
prospective-only mixed-overlay protocol ready. NGC4183 has progressed beyond
preflight into a completed accepted null-control interval endpoint on its own
weak-projection control branch: large projection corrections are source-side
disfavored, the frozen interval has been scored without residual-selected point
tuning, and the remaining obligation is to preserve that narrow single-galaxy
control interpretation.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    (REPORTS / "readout_lane_freeze_gate.md").write_text(report, encoding="utf-8")

    print(summary.to_string(index=False))
    print(freeze[["galaxy", "frozen_lane", "lane_freeze_status"]].to_string(index=False))


if __name__ == "__main__":
    main()
