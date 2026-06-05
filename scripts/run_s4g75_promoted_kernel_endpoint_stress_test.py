#!/usr/bin/env python3
"""Run the S4G75 promoted-kernel endpoint stress test.

This diagnostic is identical in structure to the filled-kernel stress test, but
uses direct S4G kernel measurement overrides where available.  It is not an
accepted endpoint because the strict subset currently has only two rows.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_promoted_kernel_endpoint_stress_test_not_validation"

sys.path.insert(0, str(ROOT / "scripts"))
import run_s4g75_filled_kernel_endpoint_stress_test as filled  # noqa: E402
import run_source_native_readout_formula_endpoint as src  # noqa: E402


def apply_promoted_observables(points: pd.DataFrame) -> pd.DataFrame:
    promoted = pd.read_csv(DATA / "s4g75_promoted_kernel_observable_fill.csv")
    out = points.copy()
    fill_map = promoted.set_index("galaxy")
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


def build_promoted_comparison(promoted_scores: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    comparison, summary = filled.build_comparison(promoted_scores)
    comparison = comparison.rename(
        columns={
            "filled_rmse_matched_family": "promoted_rmse_matched_family",
            "filled_rmse_wrong_family_mean": "promoted_rmse_wrong_family_mean",
            "filled_matched_minus_wrong_mean": "promoted_matched_minus_wrong_mean",
            "filled_matched_minus_tpg_v6": "promoted_matched_minus_tpg_v6",
            "filled_matched_minus_mond": "promoted_matched_minus_mond",
            "filled_matched_beats_wrong_mean": "promoted_matched_beats_wrong_mean",
            "filled_matched_beats_tpg_v6": "promoted_matched_beats_tpg_v6",
            "filled_matched_beats_mond": "promoted_matched_beats_mond",
            "filled_minus_old_matched_rmse": "promoted_minus_old_matched_rmse",
            "filled_improves_matched_rmse": "promoted_improves_matched_rmse",
            "filled_minus_old_matched_minus_wrong": "promoted_minus_old_matched_minus_wrong",
            "filled_improves_vs_wrong": "promoted_improves_vs_wrong",
            "filled_minus_old_matched_minus_tpg": "promoted_minus_old_matched_minus_tpg",
            "filled_improves_vs_tpg": "promoted_improves_vs_tpg",
            "filled_minus_old_matched_minus_mond": "promoted_minus_old_matched_minus_mond",
            "filled_improves_vs_mond": "promoted_improves_vs_mond",
        }
    )
    comparison["claim_boundary"] = CLAIM_BOUNDARY

    filled_delta = pd.read_csv(DATA / "s4g75_filled_vs_proxy_delta.csv")[
        [
            "galaxy",
            "filled_rmse_matched_family",
            "filled_matched_minus_tpg_v6",
            "filled_matched_minus_mond",
        ]
    ]
    comparison = comparison.merge(filled_delta, on="galaxy", how="left", validate="one_to_one")
    comparison["promoted_minus_filled_matched_rmse"] = (
        comparison["promoted_rmse_matched_family"] - comparison["filled_rmse_matched_family"]
    )
    comparison["promoted_minus_filled_matched_minus_tpg"] = (
        comparison["promoted_matched_minus_tpg_v6"] - comparison["filled_matched_minus_tpg_v6"]
    )
    comparison["promoted_minus_filled_matched_minus_mond"] = (
        comparison["promoted_matched_minus_mond"] - comparison["filled_matched_minus_mond"]
    )

    rows = []
    for split in ["all", "holdout", "train"]:
        sub = comparison if split == "all" else comparison.loc[comparison["split"] == split]
        rows.append(
            {
                "split": split,
                "n_galaxies": len(sub),
                "promoted_improves_old_matched_rmse_fraction": sub[
                    "promoted_improves_matched_rmse"
                ].mean(),
                "promoted_improves_old_vs_tpg_fraction": sub["promoted_improves_vs_tpg"].mean(),
                "promoted_improves_old_vs_mond_fraction": sub["promoted_improves_vs_mond"].mean(),
                "promoted_improves_filled_matched_rmse_fraction": (
                    sub["promoted_minus_filled_matched_rmse"] < 0
                ).mean(),
                "median_promoted_minus_filled_matched_rmse": sub[
                    "promoted_minus_filled_matched_rmse"
                ].median(),
                "median_promoted_minus_filled_vs_tpg": sub[
                    "promoted_minus_filled_matched_minus_tpg"
                ].median(),
                "median_promoted_minus_filled_vs_mond": sub[
                    "promoted_minus_filled_matched_minus_mond"
                ].median(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return comparison, pd.DataFrame(rows)


def write_report(
    summary: pd.DataFrame,
    by_family: pd.DataFrame,
    comparison_summary: pd.DataFrame,
    comparison: pd.DataFrame,
) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    changed = comparison.loc[
        (comparison["split"] == "holdout")
        & (comparison["promoted_minus_filled_matched_rmse"].abs() > 1.0e-12)
    ]
    lines = [
        "# S4G75 Promoted-Kernel Endpoint Stress Test",
        "",
        "This diagnostic reruns the S4G75 endpoint after replacing filled proxy "
        "values with direct S4G kernel measurements where available. It is not "
        "accepted validation.",
        "",
        "## Holdout Verdict",
        "",
        f"Holdout galaxies: {int(holdout['n_galaxies'])}.",
        f"Matched formula beats wrong-family mean: {holdout['matched_beats_wrong_fraction']:.4f}.",
        f"Matched formula beats TPG/v6: {holdout['matched_beats_tpg_v6_fraction']:.4f}.",
        f"Matched formula beats MOND: {holdout['matched_beats_mond_fraction']:.4f}.",
        "",
        "## Promoted Versus Filled",
        "",
        filled.markdown_table(comparison_summary),
        "",
        "## Holdout By Family",
        "",
        filled.markdown_table(by_family.loc[by_family["split"] == "holdout"]),
        "",
        "## Holdout Rows Changed By Direct Kernel Promotion",
        "",
        filled.markdown_table(
            changed[
                [
                    "galaxy",
                    "formula_family",
                    "filled_rmse_matched_family",
                    "promoted_rmse_matched_family",
                    "promoted_minus_filled_matched_rmse",
                    "promoted_minus_filled_matched_minus_tpg",
                    "promoted_minus_filled_matched_minus_mond",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This is a stress diagnostic over a two-row strict kernel-ready subset "
        "embedded in the S4G75 lane. It is too small for accepted endpoint "
        "validation.",
        "",
    ]
    (REPORTS / "s4g75_promoted_kernel_endpoint_stress_test.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    points, _labels = src.load_points()
    promoted_points = apply_promoted_observables(points)
    promoted_points = src.add_bridge_formula_kernels(promoted_points)
    amplitudes = src.fit_amplitudes(promoted_points)
    scored_points = src.add_predictions(promoted_points, amplitudes)
    galaxy_scores, _all_summary, _all_by_family = src.score_galaxies(scored_points)
    scores = filled.subset_scores(galaxy_scores)
    scores["claim_boundary"] = CLAIM_BOUNDARY
    summary = pd.DataFrame([filled.summarize(scores, split) for split in ["all", "holdout", "train"]])
    summary["claim_boundary"] = CLAIM_BOUNDARY
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
    by_family["claim_boundary"] = CLAIM_BOUNDARY
    comparison, comparison_summary = build_promoted_comparison(scores)

    scores.to_csv(DATA / "s4g75_promoted_kernel_endpoint_scores.csv", index=False)
    summary.to_csv(DATA / "s4g75_promoted_kernel_endpoint_summary.csv", index=False)
    by_family.to_csv(DATA / "s4g75_promoted_kernel_endpoint_by_family.csv", index=False)
    comparison.to_csv(DATA / "s4g75_promoted_vs_proxy_delta.csv", index=False)
    comparison_summary.to_csv(DATA / "s4g75_promoted_vs_filled_delta_summary.csv", index=False)
    write_report(summary, by_family, comparison_summary, comparison)

    print("PAPER8_S4G75_PROMOTED_KERNEL_ENDPOINT_STRESS_TEST_COMPLETE")
    print(summary.to_string(index=False))
    print()
    print(comparison_summary.to_string(index=False))


if __name__ == "__main__":
    main()
