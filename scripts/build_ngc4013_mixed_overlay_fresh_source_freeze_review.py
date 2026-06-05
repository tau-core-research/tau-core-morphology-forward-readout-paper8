#!/usr/bin/env python3
"""Review whether NGC4013 mixed-overlay source freeze can be treated as fresh.

The current NGC4013 mixed formula has already been inspected diagnostically,
so it cannot become a retroactive accepted endpoint. This review asks a
different question: are the source-side lane and formula-freeze ingredients
residual-blind enough to define a future/prospective mixed-overlay protocol?

No endpoint is scored here.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4013"
CLAIM_BOUNDARY = "ngc4013_mixed_overlay_fresh_source_freeze_review_not_endpoint"


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

    source_evidence = pd.read_csv(DATA / "ngc4013_mixed_source_rule_evidence.csv")
    source_summary = pd.read_csv(DATA / "ngc4013_mixed_source_rule_summary.csv").iloc[0]
    formula_manifest = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_manifest.csv").iloc[0]
    formula_summary = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_summary.csv").iloc[0]
    lane_freeze = pd.read_csv(DATA / "readout_lane_freeze_assignments.csv")
    lane_row = lane_freeze.loc[lane_freeze["galaxy"].eq(GALAXY)].iloc[0]

    allowed_evidence = source_evidence.loc[
        source_evidence["endpoint_label_input_allowed"].astype(bool)
    ].copy()
    forbidden_evidence = source_evidence.loc[
        ~source_evidence["endpoint_label_input_allowed"].astype(bool)
    ].copy()

    smooth_pass = bool(source_summary["smooth_disk_source_supported"])
    overlay_pass = bool(source_summary["overlay_source_supported"])
    compact_rejected = bool(source_summary["compact_only_rejected"])
    source_rule_pass = bool(source_summary["general_mixed_source_rule_pass"])
    diagnostic_score_used = bool(source_summary["diagnostic_score_used_as_label_input"])
    formula_blind = not bool(formula_manifest["uses_vobs_or_residual_in_construction"])
    formula_ready = bool(formula_manifest["prospective_endpoint_protocol_ready"])
    retro_blocked = not bool(formula_manifest["retrospective_endpoint_scores_allowed"])

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4013_FSFR1_SOURCE_RULE",
                "gate_status": "PASS" if source_rule_pass else "BLOCKED",
                "evidence": str(source_summary["source_support_status"]),
                "remaining_obligation": "none at source-rule level",
            },
            {
                "gate_id": "N4013_FSFR2_FORBIDDEN_SCORE_EXCLUDED",
                "gate_status": "PASS" if not diagnostic_score_used else "BLOCKED",
                "evidence": (
                    "diagnostic score row is endpoint_label_input_allowed=False"
                ),
                "remaining_obligation": (
                    "do not use previous RMSE as source-label evidence"
                ),
            },
            {
                "gate_id": "N4013_FSFR3_SOURCE_TRIAD",
                "gate_status": (
                    "PASS" if smooth_pass and overlay_pass and compact_rejected else "BLOCKED"
                ),
                "evidence": (
                    f"smooth={smooth_pass}; overlay={overlay_pass}; compact_rejected={compact_rejected}"
                ),
                "remaining_obligation": "lag map digitization can strengthen but is not required for protocol",
            },
            {
                "gate_id": "N4013_FSFR4_FORMULA_FREEZE_BLINDNESS",
                "gate_status": "PASS" if formula_blind else "BLOCKED",
                "evidence": (
                    "formula manifest uses_vobs_or_residual_in_construction=False"
                ),
                "remaining_obligation": "future scoring script must read manifest unchanged",
            },
            {
                "gate_id": "N4013_FSFR5_PROSPECTIVE_READY",
                "gate_status": "PASS_CAVEATED" if formula_ready and retro_blocked else "BLOCKED",
                "evidence": (
                    f"prospective_ready={formula_ready}; retroactive_scores_allowed={not retro_blocked}"
                ),
                "remaining_obligation": (
                    "may be used prospectively, but not as retroactive accepted validation"
                ),
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    reviewed_fields = allowed_evidence[
        [
            "evidence_id",
            "evidence_lane",
            "source_field",
            "source_value",
            "pass_status",
            "interpretation",
        ]
    ].copy()
    reviewed_fields["galaxy"] = GALAXY
    reviewed_fields["claim_boundary"] = CLAIM_BOUNDARY

    forbidden = forbidden_evidence[
        [
            "evidence_id",
            "evidence_lane",
            "source_field",
            "source_value",
            "pass_status",
            "interpretation",
        ]
    ].copy()
    forbidden["galaxy"] = GALAXY
    forbidden["claim_boundary"] = CLAIM_BOUNDARY

    review_pass = (
        source_rule_pass and not diagnostic_score_used and formula_blind and formula_ready and retro_blocked
    )
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "fresh_source_freeze_review_status": (
                    "NGC4013_MIXED_OVERLAY_SOURCE_FREEZE_PASS_CAVEATED_PROSPECTIVE_ONLY"
                    if review_pass
                    else "NGC4013_MIXED_OVERLAY_SOURCE_FREEZE_BLOCKED"
                ),
                "previous_lane_freeze_status": str(lane_row["lane_freeze_status"]),
                "recommended_lane_status_update": (
                    "L_mixed_overlay_protocol_ready_not_retroactive"
                    if review_pass
                    else "L_mixed_overlay_pending"
                ),
                "source_rule_pass": source_rule_pass,
                "formula_blind": formula_blind,
                "prospective_protocol_ready": formula_ready,
                "retroactive_endpoint_scores_allowed": not retro_blocked,
                "n_allowed_source_evidence": len(reviewed_fields),
                "n_forbidden_evidence_rows": len(forbidden),
                "endpoint_scores_allowed": False,
                "future_prospective_scoring_allowed_after_separate_gate": bool(review_pass),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    reviewed_fields.to_csv(
        DATA / "ngc4013_mixed_overlay_fresh_source_freeze_fields.csv", index=False
    )
    forbidden.to_csv(
        DATA / "ngc4013_mixed_overlay_fresh_source_freeze_forbidden_evidence.csv",
        index=False,
    )
    gates.to_csv(
        DATA / "ngc4013_mixed_overlay_fresh_source_freeze_gates.csv", index=False
    )
    summary.to_csv(
        DATA / "ngc4013_mixed_overlay_fresh_source_freeze_summary.csv", index=False
    )

    report = f"""# NGC4013 Mixed Overlay Fresh Source-Freeze Review

Status: `{summary.iloc[0]['fresh_source_freeze_review_status']}`

This review separates the source-side mixed-overlay protocol from the earlier
diagnostic score. It does not score an endpoint.

## Summary

{markdown_table(summary)}

## Allowed Source Evidence

{markdown_table(reviewed_fields)}

## Forbidden/Non-Label Evidence

{markdown_table(forbidden)}

## Gates

{markdown_table(gates)}

## Interpretation

NGC4013 has enough residual-blind source evidence to be treated as a
prospective mixed-overlay protocol case: smooth disk carrier evidence, overlay
evidence, and compact-only rejection are all present. The earlier diagnostic
RMSE remains explicitly forbidden as label evidence. Therefore this case can
be moved from `pending` to a prospective-only lane status, but it still cannot
be counted as retroactive endpoint validation.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    (REPORTS / "ngc4013_mixed_overlay_fresh_source_freeze_review.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
