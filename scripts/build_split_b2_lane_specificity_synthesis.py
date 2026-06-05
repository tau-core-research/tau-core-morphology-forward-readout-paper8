#!/usr/bin/env python3
"""Synthesize split-B2 diagnostic and holdout results into a lane-specificity gate.

This script does not tune formulas and does not promote a population endpoint.
It compares:

    - NGC7331: same-curve diagnostic where split-B2 repaired a q-role failure.
    - NGC5907: independent caveated holdout where split-B2 failed and projection
      readout remained strong.

The scientific point is to preserve both facts and decide whether the evidence
supports a universal split-B2 rule or a morphology/readout-lane-specific rule.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "split_b2_lane_specificity_synthesis_not_population_validation"


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

    ngc7331 = pd.read_csv(
        DATA / "ngc7331_b2_split_unit_load_diagnostic_comparison_summary.csv"
    ).iloc[0]
    ngc5907_score = pd.read_csv(
        DATA / "ngc5907_split_b2_unit_load_caveated_holdout_endpoint_summary.csv"
    ).iloc[0]
    ngc5907_failure = pd.read_csv(
        DATA / "ngc5907_split_b2_failure_mode_summary.csv"
    ).iloc[0]
    selector = pd.read_csv(DATA / "split_b2_independent_holdout_candidates.csv")

    cases = pd.DataFrame(
        [
            {
                "galaxy": "NGC7331",
                "case_role": "diagnostic_origin_same_curve",
                "readout_lane_under_test": "split_B2_added_warp_history",
                "status": "POSITIVE_DIAGNOSTIC_NOT_ENDPOINT",
                "primary_metric": "RMSE",
                "split_b2_rmse_km_s": float(ngc7331["split_b2_rmse_km_s"]),
                "comparison_model": str(ngc7331["best_baseline_model"]),
                "comparison_rmse_km_s": float(ngc7331["best_baseline_rmse_km_s"]),
                "delta_vs_comparison_km_s": float(
                    ngc7331["split_minus_best_baseline_rmse_km_s"]
                ),
                "interpretation": (
                    "split-B2 unit-load repairs the failed exact-transfer q-role "
                    "diagnostic on the same galaxy; useful but not independent"
                ),
                "endpoint_evidence_strength": "DIAGNOSTIC_ONLY",
            },
            {
                "galaxy": "NGC5907",
                "case_role": "independent_caveated_holdout",
                "readout_lane_under_test": "split_B2_added_warp_history",
                "status": "NEGATIVE_HOLDOUT_PRELIMINARY_CONTROL",
                "primary_metric": "RMSE",
                "split_b2_rmse_km_s": float(ngc5907_score["split_b2_rmse_km_s"]),
                "comparison_model": str(ngc5907_score["best_existing_tau_context_model"]),
                "comparison_rmse_km_s": float(
                    ngc5907_score["best_existing_tau_context_rmse_km_s"]
                ),
                "delta_vs_comparison_km_s": float(
                    ngc5907_score[
                        "split_minus_best_existing_tau_context_rmse_km_s"
                    ]
                ),
                "interpretation": str(ngc5907_failure["primary_interpretation"]),
                "endpoint_evidence_strength": "CAVEATED_NEGATIVE_CONTROL",
            },
        ]
    )
    cases["formula_tuned_in_synthesis"] = False
    cases["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "SB2LS_G1_PRESERVE_NGC7331_DIAGNOSTIC",
                "gate_status": "PASS",
                "evidence": (
                    "NGC7331 split-B2 repair improves the failed same-curve exact-transfer diagnostic"
                ),
                "consequence": "keep as q-role/source-load diagnostic, not validation",
            },
            {
                "gate_id": "SB2LS_G2_PRESERVE_NGC5907_NEGATIVE",
                "gate_status": "PASS",
                "evidence": (
                    "NGC5907 split-B2 holdout RMSE is much worse than projection/TPG-like context"
                ),
                "consequence": "do not universalize split-B2 added-readout",
            },
            {
                "gate_id": "SB2LS_G3_UNIVERSAL_SPLIT_B2_RULE",
                "gate_status": "REJECTED_BY_CURRENT_EVIDENCE",
                "evidence": (
                    "positive same-curve diagnostic plus negative independent holdout"
                ),
                "consequence": "split-B2 is not a universal morphology readout formula",
            },
            {
                "gate_id": "SB2LS_G4_LANE_SPECIFICITY",
                "gate_status": "SUPPORTED_PRELIMINARY",
                "evidence": (
                    "projection-dominated NGC5907 rejects added split-B2 but accepts projection/TPG-like readout"
                ),
                "consequence": (
                    "readout-lane selection is physically/scientifically central, not cosmetic"
                ),
            },
            {
                "gate_id": "SB2LS_G5_POPULATION_VALIDATION",
                "gate_status": "OPEN",
                "evidence": "only one diagnostic origin and one caveated negative holdout",
                "consequence": "requires more predeclared galaxies before population claim",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    next_cases = selector.loc[
        selector["galaxy"].isin(["NGC4013", "NGC4183", "NGC5907"]),
        [
            "galaxy",
            "split_b2_holdout_status",
            "sparc_status",
            "split_b2_blockers",
            "recommended_next_action",
        ],
    ].copy()
    next_cases["recommended_lane_after_synthesis"] = [
        "secondary analogue only after fresh source freeze"
        if galaxy == "NGC4013"
        else "source acquisition before any split-B2 scoring"
        if galaxy == "NGC4183"
        else "projection lane remains accepted; split-B2 lane negative control"
        for galaxy in next_cases["galaxy"]
    ]
    next_cases["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "synthesis_status": "SPLIT_B2_LANE_SPECIFICITY_SYNTHESIS_COMPLETE",
                "universal_split_b2_rule_status": "REJECTED_BY_CURRENT_EVIDENCE",
                "lane_specificity_status": "SUPPORTED_PRELIMINARY_NOT_VALIDATED",
                "ngc7331_role": "positive_same_curve_diagnostic",
                "ngc5907_role": "negative_caveated_independent_control",
                "population_validation_status": "OPEN",
                "formula_tuned": False,
                "endpoint_scores_allowed": False,
                "recommended_next_gate": (
                    "predeclare another added-readout candidate from source fields, "
                    "or strengthen projection/readout lane taxonomy before more scoring"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    cases.to_csv(DATA / "split_b2_lane_specificity_cases.csv", index=False)
    gates.to_csv(DATA / "split_b2_lane_specificity_gates.csv", index=False)
    next_cases.to_csv(DATA / "split_b2_lane_specificity_next_cases.csv", index=False)
    summary.to_csv(DATA / "split_b2_lane_specificity_summary.csv", index=False)

    report = f"""# Split-B2 Lane-Specificity Synthesis

Status: `{summary.iloc[0]['synthesis_status']}`

This synthesis preserves both the NGC7331 split-B2 diagnostic improvement and
the NGC5907 split-B2 negative holdout. It does not tune a formula and it does
not claim population validation.

## Summary

{markdown_table(summary)}

## Cases

{markdown_table(cases)}

## Gates

{markdown_table(gates)}

## Next Cases

{markdown_table(next_cases)}

## Interpretation

The evidence now argues against treating split-B2 as a universal Tau Core
readout formula. NGC7331 remains useful because it exposed and repaired a
q-role/source-load issue. NGC5907 is useful in the opposite direction: it
rejects the added split-B2 lane while projection/TPG-like readouts remain
strong.

This is a good scientific outcome for the bridge because it supports the
central Paper 8 idea: morphology/readout lane selection matters. The right
question is not whether one Tau formula fits all galaxies, but whether the
source-selected readout lane explains which baseline-like behavior should be
strong.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    (REPORTS / "split_b2_lane_specificity_synthesis.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(cases[["galaxy", "status", "split_b2_rmse_km_s", "comparison_model", "comparison_rmse_km_s", "delta_vs_comparison_km_s"]].to_string(index=False))


if __name__ == "__main__":
    main()
