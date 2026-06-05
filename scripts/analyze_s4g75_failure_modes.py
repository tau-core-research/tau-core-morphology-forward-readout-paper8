#!/usr/bin/env python3
"""Analyze failure modes in the S4G 75 scale-source subset.

The subset is source-richer for disk scale, but it is not an accepted endpoint
lane. This script turns the S4G75 stress-test output into a diagnostic repair
queue and family/lane breakdown without changing any endpoint gate.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_failure_mode_diagnostic_not_endpoint"


def bool_value(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"true", "1", "yes"}
    return bool(value)


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def markdown_table(df: pd.DataFrame) -> str:
    columns = list(df.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(fmt(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def classify(row: pd.Series) -> tuple[str, str]:
    hard_specific = bool_value(row["matched_beats_wrong_mean"])
    hard_beats_any_baseline = bool_value(row["matched_beats_tpg_v6"]) or bool_value(
        row["matched_beats_mond"]
    )
    tau_beats_tpg = bool_value(row["source_norm_beats_tpg_v6"])
    tau_beats_mond = bool_value(row["source_norm_beats_mond"])
    tau_beats_any_baseline = tau_beats_tpg or tau_beats_mond
    tau_beats_both = tau_beats_tpg and tau_beats_mond
    projection_or_scale_issue = row["repair_status"] != "NO_PROJECTION_SCALE_REPAIR_REQUIRED"

    if hard_specific and tau_beats_both:
        return (
            "SPECIFICITY_TRANSFERS_TO_BOTH_BASELINES",
            "matched family beats wrong-family mean and Tau L2 beats both baselines",
        )
    if hard_specific and tau_beats_any_baseline:
        return (
            "SPECIFICITY_PARTLY_TRANSFERS_TO_BASELINES",
            "matched family beats wrong-family mean and Tau L2 beats one baseline",
        )
    if hard_specific and projection_or_scale_issue:
        return (
            "SPECIFICITY_SURVIVES_PROJECTION_SCALE_REPAIR_NEEDED",
            "family specificity survives, but projection/scale repair is still needed",
        )
    if hard_specific:
        return (
            "SPECIFICITY_SURVIVES_NORMALIZATION_WEAK",
            "family specificity survives, but Tau L2 does not beat TPG/MOND",
        )
    if hard_beats_any_baseline:
        return (
            "BASELINE_COMPETITIVE_WITHOUT_FAMILY_SPECIFICITY",
            "hard matched family can beat a baseline but not the wrong-family mean",
        )
    return (
        "NO_SPECIFICITY_NO_BASELINE_TRANSFER",
        "neither family specificity nor baseline transfer is visible in this diagnostic",
    )


def repair_priority(row: pd.Series) -> tuple[int, str]:
    hard_specific = bool_value(row["matched_beats_wrong_mean"])
    tau_weak = not (
        bool_value(row["source_norm_beats_tpg_v6"])
        or bool_value(row["source_norm_beats_mond"])
    )
    status = row["repair_status"]
    split_boost = 2 if row["split"] == "holdout" else 0
    specificity_boost = 3 if hard_specific and tau_weak else 0

    if status == "REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT":
        return (100 + split_boost + specificity_boost, "P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT")
    if status == "NEEDS_INCLINATION_PROJECTION_REVIEW":
        return (80 + split_boost + specificity_boost, "P1_INCLINATION_PROJECTION_REVIEW")
    if status == "NEEDS_VERTICAL_GEOMETRY_SOURCE":
        return (70 + split_boost + specificity_boost, "P1_VERTICAL_GEOMETRY_SOURCE")
    if status == "NEEDS_DISTANCE_SCALE_SOURCE":
        return (60 + split_boost + specificity_boost, "P2_DISTANCE_SCALE_SOURCE")
    if hard_specific and tau_weak:
        return (50 + split_boost, "P2_SOURCE_NORMALIZATION_REVIEW")
    return (10 + split_boost, "P3_MONITOR_NO_IMMEDIATE_REPAIR")


def main() -> None:
    scores = pd.read_csv(DATA / "s4g75_scale_source_subset_endpoint_scores.csv")

    rows = []
    for _, row in scores.iterrows():
        mode, reason = classify(row)
        priority_score, priority_label = repair_priority(row)
        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "formula_family": row["formula_family"],
                "inclusion_lane": row["inclusion_lane"],
                "allowed_use": row["allowed_use"],
                "repair_status": row["repair_status"],
                "projection_reason": row["projection_reason"],
                "matched_beats_wrong_mean": bool_value(row["matched_beats_wrong_mean"]),
                "matched_beats_tpg_v6": bool_value(row["matched_beats_tpg_v6"]),
                "matched_beats_mond": bool_value(row["matched_beats_mond"]),
                "source_norm_beats_old_l2_intake": bool_value(
                    row["source_norm_beats_old_l2_intake"]
                ),
                "source_norm_beats_tpg_v6": bool_value(row["source_norm_beats_tpg_v6"]),
                "source_norm_beats_mond": bool_value(row["source_norm_beats_mond"]),
                "matched_minus_wrong_mean": row["matched_minus_wrong_mean"],
                "source_norm_minus_tpg_v6": row["source_norm_minus_tpg_v6"],
                "source_norm_minus_mond": row["source_norm_minus_mond"],
                "failure_mode": mode,
                "failure_reason": reason,
                "repair_priority": priority_label,
                "repair_priority_score": priority_score,
                "endpoint_scores_reused": True,
                "classification_changes_endpoint_gate": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    audit = pd.DataFrame(rows).sort_values(
        ["split", "failure_mode", "repair_priority_score", "galaxy"],
        ascending=[True, True, False, True],
    )
    summary = (
        audit.groupby(["split", "formula_family", "failure_mode"])
        .agg(
            n_galaxies=("galaxy", "count"),
            hard_beats_wrong_fraction=("matched_beats_wrong_mean", "mean"),
            tau_l2_beats_tpg_v6_fraction=("source_norm_beats_tpg_v6", "mean"),
            tau_l2_beats_mond_fraction=("source_norm_beats_mond", "mean"),
            median_matched_minus_wrong=("matched_minus_wrong_mean", "median"),
            median_tau_l2_minus_tpg_v6=("source_norm_minus_tpg_v6", "median"),
            median_tau_l2_minus_mond=("source_norm_minus_mond", "median"),
        )
        .reset_index()
        .sort_values(["split", "formula_family", "failure_mode"])
    )
    repair_summary = (
        audit.groupby(["split", "repair_priority", "repair_status"])
        .agg(
            n_galaxies=("galaxy", "count"),
            hard_specific_count=("matched_beats_wrong_mean", "sum"),
            tau_l2_tpg_win_count=("source_norm_beats_tpg_v6", "sum"),
            tau_l2_mond_win_count=("source_norm_beats_mond", "sum"),
            median_priority_score=("repair_priority_score", "median"),
        )
        .reset_index()
        .sort_values(["split", "median_priority_score"], ascending=[True, False])
    )
    priority = audit.loc[
        audit["repair_priority"] != "P3_MONITOR_NO_IMMEDIATE_REPAIR"
    ].sort_values(
        [
            "repair_priority_score",
            "split",
            "matched_minus_wrong_mean",
            "source_norm_minus_tpg_v6",
        ],
        ascending=[False, True, True, False],
    )

    audit.to_csv(DATA / "s4g75_failure_mode_breakdown.csv", index=False)
    summary.to_csv(DATA / "s4g75_failure_mode_summary.csv", index=False)
    repair_summary.to_csv(DATA / "s4g75_repair_priority_summary.csv", index=False)
    priority.to_csv(DATA / "s4g75_repair_priority_queue.csv", index=False)

    holdout = audit.loc[audit["split"] == "holdout"]
    report = [
        "# S4G 75 Failure-Mode Breakdown",
        "",
        "This diagnostic decomposes the S4G scale-source 75-row subset by family, "
        "lane, repair status, and baseline-transfer behavior. It reuses endpoint "
        "stress-test scores but does not change any endpoint gate.",
        "",
        "## Holdout Headline",
        "",
        f"Holdout rows: {len(holdout)}.",
        f"Hard family beats wrong-family mean: {holdout['matched_beats_wrong_mean'].mean():.4f}.",
        f"Tau L2 beats TPG/v6: {holdout['source_norm_beats_tpg_v6'].mean():.4f}.",
        f"Tau L2 beats MOND: {holdout['source_norm_beats_mond'].mean():.4f}.",
        "",
        "## Failure Mode Summary",
        markdown_table(summary),
        "",
        "## Repair Priority Summary",
        markdown_table(repair_summary),
        "",
        "## Top Repair Queue",
        markdown_table(
            priority[
                [
                    "galaxy",
                    "split",
                    "formula_family",
                    "repair_priority",
                    "repair_status",
                    "failure_mode",
                    "matched_minus_wrong_mean",
                    "source_norm_minus_tpg_v6",
                    "source_norm_minus_mond",
                ]
            ].head(30)
        ),
        "",
        "## Claim Boundary",
        "These labels are diagnostic and repair-oriented. They are not accepted "
        "morphology labels, not endpoint validation, and not evidence that a "
        "repair will necessarily improve the endpoint.",
    ]
    (REPORTS / "s4g75_failure_mode_breakdown.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print("PAPER8_S4G75_FAILURE_MODE_ANALYSIS_COMPLETE")
    print(summary.to_string(index=False))
    print()
    print(repair_summary.to_string(index=False))


if __name__ == "__main__":
    main()
