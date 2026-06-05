#!/usr/bin/env python3
"""Audit which four-case caveats are reduced by the latest gates.

The audit is deliberately conservative: it does not rewrite endpoint statuses
and does not turn a caveated or retrospective row into validation.  It records
which caveats have been reduced by source-side gates or sharpened replay
controls, and which obligations remain open.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "four_case_caveat_reduction_audit_not_validation"


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

    four = pd.read_csv(DATA / "four_case_endpoint_status_cases.csv")
    sharpened = pd.read_csv(
        DATA / "mixed_kernel_sharpened_replay_holdout_endpoint_summary.csv"
    ).iloc[0]
    sharpened_by_galaxy = pd.read_csv(
        DATA / "mixed_kernel_sharpened_replay_holdout_control_by_galaxy.csv"
    )
    n4088_readiness = pd.read_csv(DATA / "ngc4088_formula_freeze_readiness_summary.csv").iloc[0]

    sharpened_specificity_pass = (
        int(sharpened["n_matched_beats_all_wrong_labels"]) == 2
        and int(sharpened["matched_permutation_rank"]) == 1
    )
    n7331_sharp = sharpened_by_galaxy.loc[sharpened_by_galaxy["galaxy"].eq("NGC7331")].iloc[0]
    n5907_sharp = sharpened_by_galaxy.loc[sharpened_by_galaxy["galaxy"].eq("NGC5907")].iloc[0]

    rows = []
    for _, row in four.iterrows():
        galaxy = str(row["galaxy"])
        if galaxy == "NGC4013":
            reduction = "RETROSPECTIVE_CAVEAT_ISOLATED_NOT_REMOVED"
            reduced = False
            evidence = (
                "row is retained as frozen-reference/protocol-ready evidence; "
                "not promoted to accepted endpoint"
            )
            remaining = (
                "needs a predeclared replay/holdout lane or future source-selected "
                "analogue to reduce the retrospective caveat"
            )
        elif galaxy == "NGC5907":
            reduction = "PRIOR_PROJECTION_CAVEAT_REDUCED_TO_CONTROL_CONTEXT"
            reduced = True
            evidence = (
                "accepted mixed endpoint records previous_projection_endpoint_used_as_mixed_evidence=false; "
                f"source-sharpened replay matched-minus-wrong-best={float(n5907_sharp['matched_minus_wrong_best']):.6g}"
            )
            remaining = "small-N and single-galaxy control status remain"
        elif galaxy == "NGC7331":
            reduction = "BROAD_WINDOW_CAVEAT_REDUCED_FOR_REPLAY_NOT_RETROACTIVE_ENDPOINT"
            reduced = True
            evidence = (
                "V2 fractional onset and V3 source-sharpened replay replace the broad V1 window for replay only; "
                f"source-sharpened replay matched-minus-wrong-best={float(n7331_sharp['matched_minus_wrong_best']):.6g}"
            )
            remaining = (
                "accepted V1 row remains broad-window caveated; V2/V3 replay result is not retroactive endpoint update"
            )
        elif galaxy == "NGC4088":
            b1 = str(n4088_readiness["b1_whisp_promotion_status"])
            reduction = "B1_PROVENANCE_CAVEAT_REDUCED_LAW_LEVEL_CAVEATS_REMAIN"
            reduced = True
            evidence = (
                f"B1 promotion status={b1}; B1 x_w accepted for formula freeze with WHISP graphical provenance"
            )
            remaining = (
                "WHISP graphical-overview provenance caveat travels with the formula; "
                "B2 physical normalization and B3 scale uniqueness remain law-level caveats"
            )
        else:  # pragma: no cover
            reduction = "UNCLASSIFIED"
            reduced = False
            evidence = "not audited"
            remaining = "not audited"

        rows.append(
            {
                "galaxy": galaxy,
                "original_endpoint_status": str(row["endpoint_status"]),
                "original_case_caveat": str(row["case_caveat"]),
                "caveat_reduction_status": reduction,
                "caveat_reduced": reduced,
                "reduction_evidence": evidence,
                "remaining_caveat": remaining,
                "endpoint_status_changed": False,
                "endpoint_scores_recomputed": False,
                "uses_vobs_or_residual_in_reduction": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    cases = pd.DataFrame(rows)
    summary = pd.DataFrame(
        [
            {
                "audit_status": "FOUR_CASE_CAVEAT_REDUCTION_AUDIT_COMPLETE",
                "n_cases": len(cases),
                "n_caveats_reduced": int(cases["caveat_reduced"].sum()),
                "n_caveats_isolated_not_removed": int((~cases["caveat_reduced"]).sum()),
                "sharpened_replay_specificity_pass": sharpened_specificity_pass,
                "endpoint_statuses_changed": False,
                "endpoint_scores_recomputed": False,
                "population_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    cases.to_csv(DATA / "four_case_caveat_reduction_cases.csv", index=False)
    summary.to_csv(DATA / "four_case_caveat_reduction_summary.csv", index=False)

    report = [
        "# Four-Case Caveat Reduction Audit",
        "",
        "This audit records caveat reductions after the source-side separation,",
        "kernel-sharpening, and sharpened replay/holdout gates. It does not",
        "change endpoint statuses and does not create a population-validation",
        "claim.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Case-Level Caveat Reduction",
        "",
        markdown_table(cases),
        "",
        "## Interpretation",
        "",
        "Three caveats are reduced, not erased. NGC5907's prior-projection caveat",
        "is reduced to control context because the accepted mixed gate excludes",
        "the previous projection endpoint as mixed evidence and the sharpened",
        "replay row keeps source-matched specificity. NGC7331's broad-window",
        "caveat is reduced for the replay path by the fractional-onset and",
        "source-sharpened kernels, but the accepted V1 endpoint remains caveated.",
        "NGC4088's B1 provenance caveat is reduced to a caveated WHISP graphical",
        "formula-freeze input; B2/B3 law-level caveats remain. NGC4013's",
        "retrospective caveat is isolated but not removed.",
        "",
    ]
    (REPORTS / "four_case_caveat_reduction_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
