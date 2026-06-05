#!/usr/bin/env python3
"""Build the S4G75 source-rich lane action plan.

The S4G75 subset is the current source-rich scale-radius lane. This script
turns the failure-mode and repair-priority diagnostics into a concrete
residual-blind source action plan. It does not create accepted labels and does
not compute or change endpoint scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_source_rich_lane_action_plan_not_endpoint"


SOURCE_PLAN = {
    "P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT": {
        "source_targets": "S4G;SPARC_DISTANCE;NED_NEDD",
        "action": "audit existing S4G scale radius against distance/projection caveat and freeze usable scale if residual-blind consistency passes",
        "promotion_use": "fastest repair path for source-rich rows with existing scale support",
    },
    "P1_INCLINATION_PROJECTION_REVIEW": {
        "source_targets": "NED_NEDD;S4G;SPARC_METADATA",
        "action": "review inclination, distance uncertainty, and projection caveats before using scale-sensitive readout",
        "promotion_use": "projection-safety gate for low-inclination or distance-caveated rows",
    },
    "P1_VERTICAL_GEOMETRY_SOURCE": {
        "source_targets": "S4G;DustPedia;HI_SURVEYS;PHANGS_IF_AVAILABLE",
        "action": "seek vertical thickness, flare, warp, edge/projection, or gas-plane evidence for thick/flared readout support",
        "promotion_use": "source-native support for thick/flared orientation and vertical damping",
    },
    "P2_SOURCE_NORMALIZATION_REVIEW": {
        "source_targets": "S4G;SPARC_BARYONIC;HI_SURVEYS",
        "action": "inspect source-normalization inputs after projection/scale-clean status; do not tune from endpoint residuals",
        "promotion_use": "normalization-law stress test rather than source acquisition",
    },
    "P2_DISTANCE_SCALE_SOURCE": {
        "source_targets": "NED_NEDD;SPARC_DISTANCE;S4G_IF_AVAILABLE",
        "action": "acquire or review distance/scale source support before promoting source-native scale",
        "promotion_use": "distance-scale blocker repair",
    },
}


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


def build_action_plan() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    queue = pd.read_csv(DATA / "s4g75_repair_priority_queue.csv")
    scores = pd.read_csv(DATA / "s4g75_scale_source_subset_endpoint_scores.csv")

    action_rows = []
    for _, row in queue.iterrows():
        priority = row["repair_priority"]
        spec = SOURCE_PLAN.get(
            priority,
            {
                "source_targets": "S4G;NED_NEDD",
                "action": "monitor; no immediate source-rich lane repair action",
                "promotion_use": "support-only monitoring",
            },
        )
        action_rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "formula_family": row["formula_family"],
                "repair_priority": priority,
                "repair_status": row["repair_status"],
                "failure_mode": row["failure_mode"],
                "source_targets": spec["source_targets"],
                "residual_blind_action": spec["action"],
                "promotion_use": spec["promotion_use"],
                "matched_minus_wrong_mean": row["matched_minus_wrong_mean"],
                "source_norm_minus_tpg_v6": row["source_norm_minus_tpg_v6"],
                "source_norm_minus_mond": row["source_norm_minus_mond"],
                "accepted_label_output_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    plan = pd.DataFrame(action_rows).sort_values(
        [
            "split",
            "repair_priority",
            "formula_family",
            "galaxy",
        ]
    )

    source_summary = (
        plan.groupby(["split", "repair_priority", "source_targets"])
        .agg(
            n_galaxies=("galaxy", "count"),
            n_hard_specific=(
                "matched_minus_wrong_mean",
                lambda s: int((s < 0).sum()),
            ),
            median_matched_minus_wrong=("matched_minus_wrong_mean", "median"),
            median_source_norm_minus_tpg_v6=("source_norm_minus_tpg_v6", "median"),
            median_source_norm_minus_mond=("source_norm_minus_mond", "median"),
        )
        .reset_index()
        .sort_values(["split", "repair_priority"])
    )

    lane_context = (
        scores.groupby(["split", "inclusion_lane", "allowed_use"])
        .agg(
            n_s4g75_galaxies=("galaxy", "count"),
            hard_beats_wrong_fraction=("matched_beats_wrong_mean", "mean"),
            tau_l2_beats_tpg_v6_fraction=("source_norm_beats_tpg_v6", "mean"),
            tau_l2_beats_mond_fraction=("source_norm_beats_mond", "mean"),
        )
        .reset_index()
        .sort_values(["split", "inclusion_lane", "allowed_use"])
    )
    return plan, source_summary, lane_context


def write_report(
    plan: pd.DataFrame, source_summary: pd.DataFrame, lane_context: pd.DataFrame
) -> None:
    holdout_plan = plan.loc[plan["split"] == "holdout"]
    p0 = plan.loc[plan["repair_priority"] == "P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT"]
    p1 = plan.loc[
        plan["repair_priority"].isin(
            ["P1_INCLINATION_PROJECTION_REVIEW", "P1_VERTICAL_GEOMETRY_SOURCE"]
        )
    ]
    lines = [
        "# S4G75 Source-Rich Lane Action Plan",
        "",
        "The S4G75 lane is the current source-rich scale-radius subset. This plan "
        "keeps it separate from the full 175-row stress sample and lists the "
        "next residual-blind source repairs.",
        "",
        "## Verdict",
        "",
        f"S4G75 rows: {pd.read_csv(DATA / 's4g75_scale_source_subset_endpoint_scores.csv').shape[0]}.",
        f"Holdout S4G75 rows: {holdout_plan['galaxy'].nunique()}.",
        f"P0 existing-scale plus distance-audit rows: {p0['galaxy'].nunique()}.",
        f"P1 projection/vertical-geometry rows: {p1['galaxy'].nunique()}.",
        "",
        "The next improvement should stay on the 75-row source-rich lane first. "
        "The full 175-row sample remains useful as a stress/acquisition lane, "
        "but not as the main accepted-claim lane.",
        "",
        "## Source Action Summary",
        markdown_table(source_summary),
        "",
        "## Lane Context",
        markdown_table(lane_context),
        "",
        "## Holdout Repair Queue",
        markdown_table(
            holdout_plan[
                [
                    "galaxy",
                    "formula_family",
                    "repair_priority",
                    "repair_status",
                    "failure_mode",
                    "source_targets",
                    "residual_blind_action",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "This action plan does not create accepted labels, does not run a new "
        "endpoint, and does not claim empirical validation. It identifies which "
        "source evidence should be acquired or reviewed before the next frozen "
        "S4G75 source-rich endpoint stress test.",
    ]
    (REPORTS / "s4g75_source_rich_lane_action_plan.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    plan, source_summary, lane_context = build_action_plan()
    plan.to_csv(DATA / "s4g75_source_rich_lane_action_plan.csv", index=False)
    source_summary.to_csv(
        DATA / "s4g75_source_rich_lane_source_action_summary.csv", index=False
    )
    lane_context.to_csv(DATA / "s4g75_source_rich_lane_context_summary.csv", index=False)
    write_report(plan, source_summary, lane_context)
    print("PAPER8_S4G75_SOURCE_RICH_LANE_ACTION_PLAN_COMPLETE")
    print(source_summary.to_string(index=False))


if __name__ == "__main__":
    main()
