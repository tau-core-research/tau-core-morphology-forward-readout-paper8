#!/usr/bin/env python3
"""Run an S4G75 filled-kernel endpoint stress test.

This script reuses the source-native bridge formula endpoint machinery, then
overrides only the S4G75 holdout repair rows with the residual-blind
kernel-observable fill values.  Train amplitudes remain train-only and are not
selected from the filled holdout endpoint.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_filled_kernel_endpoint_stress_test_not_validation"

sys.path.insert(0, str(ROOT / "scripts"))
import run_source_native_readout_formula_endpoint as src  # noqa: E402


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


def apply_filled_observables(points: pd.DataFrame) -> pd.DataFrame:
    filled = pd.read_csv(DATA / "s4g75_kernel_observable_fill.csv")
    out = points.copy()
    fill_map = filled.set_index("galaxy")
    for galaxy, row in fill_map.iterrows():
        mask = out["galaxy"] == galaxy
        if not mask.any():
            continue
        if pd.notna(row["scale_radius_kpc"]):
            out.loc[mask, "scale_radius_proxy_kpc"] = row["scale_radius_kpc"]
        if pd.notna(row["tail_inner_radius_kpc"]):
            out.loc[mask, "tail_inner_radius_proxy_kpc"] = row["tail_inner_radius_kpc"]
        if pd.notna(row["tail_cutoff_radius_kpc"]):
            out.loc[mask, "tail_cutoff_radius_proxy_kpc"] = row["tail_cutoff_radius_kpc"]
        if pd.notna(row["compact_support_radius_kpc"]):
            out.loc[mask, "compact_support_radius_proxy_kpc"] = row["compact_support_radius_kpc"]
        if pd.notna(row["thickness_h_over_rs"]):
            out.loc[mask, "thickness_h_over_rs_proxy"] = row["thickness_h_over_rs"]
    return out


def summarize(scores: pd.DataFrame, split: str) -> dict[str, object]:
    sub = scores if split == "all" else scores.loc[scores["split"] == split]
    return {
        "split": split,
        "n_galaxies": len(sub),
        "matched_beats_wrong_fraction": sub["matched_beats_wrong_mean"].mean(),
        "matched_rank1_fraction": (sub["matched_family_rank"] == 1).mean(),
        "matched_beats_tpg_v6_fraction": sub["matched_beats_tpg_v6"].mean(),
        "matched_beats_mond_fraction": sub["matched_beats_mond"].mean(),
        "median_matched_minus_wrong": sub["matched_minus_wrong_mean"].median(),
        "median_matched_minus_tpg_v6": sub["matched_minus_tpg_v6"].median(),
        "median_matched_minus_mond": sub["matched_minus_mond"].median(),
    }


def subset_scores(galaxy_scores: pd.DataFrame) -> pd.DataFrame:
    source = pd.read_csv(DATA / "morphology_information_gain_source_expansion.csv")
    s4g75 = source.loc[source["s4g_scale_ready"].astype(bool), ["galaxy"]]
    scores = s4g75.merge(galaxy_scores, on="galaxy", how="left", validate="one_to_one")
    scores["claim_boundary"] = CLAIM_BOUNDARY
    return scores


def build_comparison(filled_scores: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    old_scores = pd.read_csv(DATA / "s4g75_scale_source_subset_endpoint_scores.csv")
    if "matched_minus_tpg_v6" not in old_scores.columns:
        old_scores["matched_minus_tpg_v6"] = (
            old_scores["rmse_matched_family"] - old_scores["rmse_tpg_v6"]
        )
    if "matched_minus_mond" not in old_scores.columns:
        old_scores["matched_minus_mond"] = (
            old_scores["rmse_matched_family"] - old_scores["rmse_mond"]
        )
    keep = [
        "galaxy",
        "split",
        "formula_family",
        "rmse_matched_family",
        "rmse_wrong_family_mean",
        "rmse_tpg_v6",
        "rmse_mond",
        "matched_minus_wrong_mean",
        "matched_minus_tpg_v6",
        "matched_minus_mond",
        "matched_beats_wrong_mean",
        "matched_beats_tpg_v6",
        "matched_beats_mond",
    ]
    old = old_scores[keep].rename(
        columns={
            "rmse_matched_family": "old_rmse_matched_family",
            "rmse_wrong_family_mean": "old_rmse_wrong_family_mean",
            "matched_minus_wrong_mean": "old_matched_minus_wrong_mean",
            "matched_minus_tpg_v6": "old_matched_minus_tpg_v6",
            "matched_minus_mond": "old_matched_minus_mond",
            "matched_beats_wrong_mean": "old_matched_beats_wrong_mean",
            "matched_beats_tpg_v6": "old_matched_beats_tpg_v6",
            "matched_beats_mond": "old_matched_beats_mond",
        }
    )
    new = filled_scores[keep].rename(
        columns={
            "rmse_matched_family": "filled_rmse_matched_family",
            "rmse_wrong_family_mean": "filled_rmse_wrong_family_mean",
            "matched_minus_wrong_mean": "filled_matched_minus_wrong_mean",
            "matched_minus_tpg_v6": "filled_matched_minus_tpg_v6",
            "matched_minus_mond": "filled_matched_minus_mond",
            "matched_beats_wrong_mean": "filled_matched_beats_wrong_mean",
            "matched_beats_tpg_v6": "filled_matched_beats_tpg_v6",
            "matched_beats_mond": "filled_matched_beats_mond",
        }
    )
    compare = old.merge(
        new.drop(columns=["split", "formula_family", "rmse_tpg_v6", "rmse_mond"]),
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    compare["filled_minus_old_matched_rmse"] = (
        compare["filled_rmse_matched_family"] - compare["old_rmse_matched_family"]
    )
    compare["filled_improves_matched_rmse"] = compare["filled_minus_old_matched_rmse"] < 0
    compare["filled_minus_old_matched_minus_wrong"] = (
        compare["filled_matched_minus_wrong_mean"] - compare["old_matched_minus_wrong_mean"]
    )
    compare["filled_improves_vs_wrong"] = compare["filled_minus_old_matched_minus_wrong"] < 0
    compare["filled_minus_old_matched_minus_tpg"] = (
        compare["filled_matched_minus_tpg_v6"] - compare["old_matched_minus_tpg_v6"]
    )
    compare["filled_improves_vs_tpg"] = compare["filled_minus_old_matched_minus_tpg"] < 0
    compare["filled_minus_old_matched_minus_mond"] = (
        compare["filled_matched_minus_mond"] - compare["old_matched_minus_mond"]
    )
    compare["filled_improves_vs_mond"] = compare["filled_minus_old_matched_minus_mond"] < 0
    compare["claim_boundary"] = CLAIM_BOUNDARY

    rows = []
    for split in ["all", "holdout", "train"]:
        sub = compare if split == "all" else compare.loc[compare["split"] == split]
        rows.append(
            {
                "split": split,
                "n_galaxies": len(sub),
                "filled_improves_matched_rmse_fraction": sub[
                    "filled_improves_matched_rmse"
                ].mean(),
                "filled_improves_vs_wrong_fraction": sub["filled_improves_vs_wrong"].mean(),
                "filled_improves_vs_tpg_fraction": sub["filled_improves_vs_tpg"].mean(),
                "filled_improves_vs_mond_fraction": sub["filled_improves_vs_mond"].mean(),
                "median_filled_minus_old_matched_rmse": sub[
                    "filled_minus_old_matched_rmse"
                ].median(),
                "median_filled_minus_old_matched_minus_wrong": sub[
                    "filled_minus_old_matched_minus_wrong"
                ].median(),
                "median_filled_minus_old_matched_minus_tpg": sub[
                    "filled_minus_old_matched_minus_tpg"
                ].median(),
                "median_filled_minus_old_matched_minus_mond": sub[
                    "filled_minus_old_matched_minus_mond"
                ].median(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return compare, pd.DataFrame(rows)


def write_report(
    summary: pd.DataFrame,
    by_family: pd.DataFrame,
    comparison_summary: pd.DataFrame,
    comparison: pd.DataFrame,
) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    repair_holdout = comparison.loc[
        (comparison["split"] == "holdout")
        & (comparison["filled_minus_old_matched_rmse"] != 0)
    ]
    lines = [
        "# S4G75 Filled-Kernel Endpoint Stress Test",
        "",
        "This stress test reruns the source-native bridge formula endpoint after "
        "overriding the S4G75 repair rows with concrete residual-blind filled "
        "kernel observables. It is not accepted validation.",
        "",
        "## Holdout Verdict",
        "",
        f"Holdout galaxies: {int(holdout['n_galaxies'])}.",
        f"Matched formula beats wrong-family mean: {holdout['matched_beats_wrong_fraction']:.4f}.",
        f"Matched formula beats TPG/v6: {holdout['matched_beats_tpg_v6_fraction']:.4f}.",
        f"Matched formula beats MOND: {holdout['matched_beats_mond_fraction']:.4f}.",
        f"Median matched-minus-wrong: {holdout['median_matched_minus_wrong']:.6g}.",
        f"Median matched-minus-TPG/v6: {holdout['median_matched_minus_tpg_v6']:.6g}.",
        f"Median matched-minus-MOND: {holdout['median_matched_minus_mond']:.6g}.",
        "",
        "## Filled Versus Old S4G75 Proxy",
        "",
        markdown_table(comparison_summary),
        "",
        "## Holdout By Family",
        "",
        markdown_table(by_family.loc[by_family["split"] == "holdout"]),
        "",
        "## Holdout Rows Changed By Filled Observables",
        "",
        markdown_table(
            repair_holdout[
                [
                    "galaxy",
                    "formula_family",
                    "old_rmse_matched_family",
                    "filled_rmse_matched_family",
                    "filled_minus_old_matched_rmse",
                    "filled_minus_old_matched_minus_tpg",
                    "filled_minus_old_matched_minus_mond",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "The filled observables are concrete but mostly source-constrained or "
        "formula-conditional candidates. This is a pre-endpoint stress test, not "
        "an empirical Tau Core validation claim.",
    ]
    (REPORTS / "s4g75_filled_kernel_endpoint_stress_test.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    points, _labels = src.load_points()
    filled_points = apply_filled_observables(points)
    filled_points = src.add_bridge_formula_kernels(filled_points)
    amplitudes = src.fit_amplitudes(filled_points)
    scored_points = src.add_predictions(filled_points, amplitudes)
    galaxy_scores, _all_summary, _all_by_family = src.score_galaxies(scored_points)
    scores = subset_scores(galaxy_scores)
    summary = pd.DataFrame([summarize(scores, split) for split in ["all", "holdout", "train"]])
    by_family = (
        scores.groupby(["split", "formula_family"])
        .agg(
            n_galaxies=("galaxy", "count"),
            matched_beats_wrong_fraction=("matched_beats_wrong_mean", "mean"),
            matched_rank1_fraction=("matched_family_rank", lambda s: float((s == 1).mean())),
            matched_beats_tpg_v6_fraction=("matched_beats_tpg_v6", "mean"),
            matched_beats_mond_fraction=("matched_beats_mond", "mean"),
            median_matched_minus_wrong=("matched_minus_wrong_mean", "median"),
            median_matched_minus_tpg_v6=("matched_minus_tpg_v6", "median"),
            median_matched_minus_mond=("matched_minus_mond", "median"),
        )
        .reset_index()
    )
    comparison, comparison_summary = build_comparison(scores)

    scores.to_csv(DATA / "s4g75_filled_kernel_endpoint_scores.csv", index=False)
    summary.to_csv(DATA / "s4g75_filled_kernel_endpoint_summary.csv", index=False)
    by_family.to_csv(DATA / "s4g75_filled_kernel_endpoint_by_family.csv", index=False)
    comparison.to_csv(DATA / "s4g75_filled_vs_proxy_delta.csv", index=False)
    comparison_summary.to_csv(DATA / "s4g75_filled_vs_proxy_delta_summary.csv", index=False)
    write_report(summary, by_family, comparison_summary, comparison)

    print("PAPER8_S4G75_FILLED_KERNEL_ENDPOINT_STRESS_TEST_COMPLETE")
    print(summary.to_string(index=False))
    print()
    print(comparison_summary.to_string(index=False))


if __name__ == "__main__":
    main()
