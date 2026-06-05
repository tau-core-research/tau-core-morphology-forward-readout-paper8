#!/usr/bin/env python3
"""Run the S4G scale-source 75-row endpoint stress-test subset.

This is a residual-blind source-subset diagnostic. It does not create an
accepted endpoint-validation lane; it asks how the existing source-native
bridge formula and Tau-side L2 normalization behave on galaxies with S4G
scale-radius source candidates.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


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


def summarize(sub: pd.DataFrame, split: str) -> dict[str, object]:
    return {
        "split": split,
        "n_galaxies": len(sub),
        "hard_beats_wrong_fraction": sub["matched_beats_wrong_mean"].mean(),
        "hard_rank1_fraction": (sub["matched_family_rank"] == 1).mean(),
        "hard_beats_tpg_v6_fraction": sub["matched_beats_tpg_v6"].mean(),
        "hard_beats_mond_fraction": sub["matched_beats_mond"].mean(),
        "tau_l2_beats_old_l2_fraction": sub["source_norm_beats_old_l2_intake"].mean(),
        "tau_l2_beats_tpg_v6_fraction": sub["source_norm_beats_tpg_v6"].mean(),
        "tau_l2_beats_mond_fraction": sub["source_norm_beats_mond"].mean(),
        "median_hard_minus_wrong": sub["matched_minus_wrong_mean"].median(),
        "median_tau_l2_minus_tpg_v6": sub["source_norm_minus_tpg_v6"].median(),
        "median_tau_l2_minus_mond": sub["source_norm_minus_mond"].median(),
    }


def main() -> None:
    source = pd.read_csv(DATA / "morphology_information_gain_source_expansion.csv")
    hard = pd.read_csv(DATA / "source_native_readout_formula_scores_by_galaxy.csv")
    tau_l2 = pd.read_csv(DATA / "tau_side_source_normalized_l2_endpoint_scores.csv")
    repair = pd.read_csv(DATA / "projection_scale_repair_audit.csv")
    inclusion = pd.read_csv(DATA / "inclusion_lane_expansion_audit.csv")

    subset = source.loc[
        source["s4g_scale_ready"].astype(bool),
        [
            "galaxy",
            "split",
            "formula_family",
            "s4g_scale_ready",
            "q_expdisk_scale_candidate",
        ],
    ].copy()

    scores = subset.merge(
        hard[
            [
                "galaxy",
                "rmse_matched_family",
                "rmse_wrong_family_mean",
                "rmse_tpg_v6",
                "rmse_mond",
                "matched_beats_wrong_mean",
                "matched_beats_tpg_v6",
                "matched_beats_mond",
                "matched_family_rank",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    scores = scores.merge(
        tau_l2[
            [
                "galaxy",
                "rmse_tau_source_normalized_l2",
                "source_norm_beats_old_l2_intake",
                "source_norm_beats_tpg_v6",
                "source_norm_beats_mond",
                "source_norm_minus_tpg_v6",
                "source_norm_minus_mond",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    scores = scores.merge(
        repair[["galaxy", "repair_status", "projection_reason"]],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    scores = scores.merge(
        inclusion[["galaxy", "inclusion_lane", "allowed_use"]],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    scores["matched_minus_wrong_mean"] = (
        scores["rmse_matched_family"] - scores["rmse_wrong_family_mean"]
    )

    summary = pd.DataFrame(
        [
            summarize(scores if split == "all" else scores.loc[scores["split"] == split], split)
            for split in ["all", "holdout", "train"]
        ]
    )
    by_family = (
        scores.groupby(["split", "formula_family"])
        .agg(
            n_galaxies=("galaxy", "count"),
            hard_beats_wrong_fraction=("matched_beats_wrong_mean", "mean"),
            hard_rank1_fraction=("matched_family_rank", lambda s: float((s == 1).mean())),
            hard_beats_tpg_v6_fraction=("matched_beats_tpg_v6", "mean"),
            hard_beats_mond_fraction=("matched_beats_mond", "mean"),
            tau_l2_beats_tpg_v6_fraction=("source_norm_beats_tpg_v6", "mean"),
            tau_l2_beats_mond_fraction=("source_norm_beats_mond", "mean"),
            median_hard_minus_wrong=("matched_minus_wrong_mean", "median"),
            median_tau_l2_minus_tpg_v6=("source_norm_minus_tpg_v6", "median"),
            median_tau_l2_minus_mond=("source_norm_minus_mond", "median"),
        )
        .reset_index()
    )
    repair_summary = (
        scores.groupby(["split", "repair_status"])
        .agg(n_galaxies=("galaxy", "count"))
        .reset_index()
    )
    lane_summary = (
        scores.groupby(["split", "inclusion_lane", "allowed_use"])
        .agg(n_galaxies=("galaxy", "count"))
        .reset_index()
    )

    scores.to_csv(DATA / "s4g75_scale_source_subset_endpoint_scores.csv", index=False)
    summary.to_csv(DATA / "s4g75_scale_source_subset_endpoint_summary.csv", index=False)
    by_family.to_csv(DATA / "s4g75_scale_source_subset_endpoint_by_family.csv", index=False)
    repair_summary.to_csv(DATA / "s4g75_scale_source_subset_repair_summary.csv", index=False)
    lane_summary.to_csv(DATA / "s4g75_scale_source_subset_lane_summary.csv", index=False)

    report = [
        "# S4G 75 Scale-Source Subset Endpoint Stress Test",
        "",
        "This is a source-subset stress test over galaxies with S4G scale-radius "
        "source candidates. It is not an accepted endpoint-validation lane.",
        "",
        "## Summary",
        markdown_table(summary),
        "",
        "## By Family",
        markdown_table(by_family),
        "",
        "## Lane Summary",
        markdown_table(lane_summary),
        "",
        "## Repair Status",
        markdown_table(repair_summary),
        "",
        "## Claim Boundary",
        "The 75-row subset is source-richer than the full sample for disk scale, "
        "but it still mixes strict, caution, and acquisition lanes. The result "
        "is a sensitivity/preflight test, not Tau Core empirical validation.",
    ]
    (REPORTS / "s4g75_scale_source_subset_endpoint_stress_test.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print("PAPER8_S4G75_SCALE_SOURCE_SUBSET_ENDPOINT_STRESS_TEST_COMPLETE")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
