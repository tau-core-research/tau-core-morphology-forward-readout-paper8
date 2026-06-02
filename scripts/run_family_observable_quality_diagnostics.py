#!/usr/bin/env python3
"""Diagnose whether family-level failures track available-data quality limits."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


def load_joined() -> pd.DataFrame:
    scores_path = DATA / "amplitude_shrinkage_path_scores_by_galaxy.csv"
    selections_path = DATA / "train_selected_shrinkage_selection.csv"
    manifest_path = DATA / "morphology_parameter_manifest.csv"
    for path in [scores_path, selections_path, manifest_path]:
        if not path.exists():
            raise FileNotFoundError(f"{path} is missing; run scripts/reproduce.py first")
    scores = pd.read_csv(scores_path)
    selections = pd.read_csv(selections_path)
    manifest = pd.read_csv(manifest_path)
    selected_paths = sorted(selections["selected_amplitude_path_id"].unique())
    scores = scores.loc[scores["amplitude_path_id"].isin(selected_paths)].copy()
    manifest_cols = [
        "galaxy",
        "formula_family",
        "manifest_confidence",
        "manifest_caveat",
        "inc_bin",
        "distance_quality",
        "distance_frac_error",
        "inclination_deg",
        "inclination_error_deg",
        "n_points",
        "r_max",
        "mean_gas",
        "mean_bulge",
        "scale_radius_proxy_kpc",
        "thickness_h_over_rs_proxy",
    ]
    joined = scores.merge(
        manifest[manifest_cols],
        on=["galaxy", "formula_family"],
        how="left",
        validate="many_to_one",
    )
    joined = joined.rename(
        columns={
            "n_points_x": "n_points_scored",
            "n_points_y": "n_points_manifest",
        }
    )
    if joined["manifest_confidence"].isna().any():
        missing = sorted(joined.loc[joined["manifest_confidence"].isna(), "galaxy"].unique())
        raise ValueError(f"Missing manifest rows for scored galaxies: {missing[:8]}")
    joined["low_confidence"] = joined["manifest_confidence"] < 0.75
    joined["low_inclination"] = joined["manifest_caveat"].str.contains("low_inclination")
    joined["large_distance_error"] = joined["manifest_caveat"].str.contains("large_distance_error")
    joined["few_rotation_points"] = joined["manifest_caveat"].str.contains("few_rotation_points")
    joined["any_quality_caveat"] = joined[
        ["low_confidence", "low_inclination", "large_distance_error", "few_rotation_points"]
    ].any(axis=1)
    joined["baseline_win_any"] = joined["matched_beats_tpg_v6"] | joined["matched_beats_mond"]
    joined["baseline_win_both"] = joined["matched_beats_tpg_v6"] & joined["matched_beats_mond"]
    return joined


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (split, family), sub in df.groupby(["split", "formula_family"], sort=True):
        rows.append(
            {
                "split": split,
                "formula_family": family,
                "n_galaxies": int(len(sub)),
                "mean_manifest_confidence": float(sub["manifest_confidence"].mean()),
                "low_confidence_fraction": float(sub["low_confidence"].mean()),
                "any_quality_caveat_fraction": float(sub["any_quality_caveat"].mean()),
                "low_inclination_fraction": float(sub["low_inclination"].mean()),
                "large_distance_error_fraction": float(sub["large_distance_error"].mean()),
                "few_rotation_points_fraction": float(sub["few_rotation_points"].mean()),
                "median_n_points": float(sub["n_points_manifest"].median()),
                "median_r_max": float(sub["r_max"].median()),
                "matched_beats_wrong_fraction": float(sub["matched_beats_wrong_mean"].mean()),
                "matched_beats_tpg_v6_fraction": float(sub["matched_beats_tpg_v6"].mean()),
                "matched_beats_mond_fraction": float(sub["matched_beats_mond"].mean()),
                "baseline_win_any_fraction": float(sub["baseline_win_any"].mean()),
                "baseline_win_both_fraction": float(sub["baseline_win_both"].mean()),
                "mean_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].mean()),
                "mean_matched_minus_tpg_v6": float(sub["matched_minus_tpg_v6"].mean()),
                "mean_matched_minus_mond": float(sub["matched_minus_mond"].mean()),
            }
        )
    out = pd.DataFrame(rows)
    out["quality_status"] = out.apply(classify_quality_status, axis=1)
    return out


def classify_quality_status(row: pd.Series) -> str:
    if row["any_quality_caveat_fraction"] >= 0.50 or row["low_confidence_fraction"] >= 0.40:
        return "quality_limited"
    if row["matched_beats_wrong_fraction"] < 0.80:
        return "formula_or_normalization_limited"
    if row["matched_beats_tpg_v6_fraction"] < 0.50 or row["matched_beats_mond_fraction"] < 0.60:
        return "baseline_limited"
    return "current_best_case"


def compare_caveated_vs_clean(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split in sorted(df["split"].unique()):
        split_df = df.loc[df["split"] == split]
        for caveat_state, sub in [
            ("clean_manifest_proxy", split_df.loc[~split_df["any_quality_caveat"]]),
            ("quality_caveated", split_df.loc[split_df["any_quality_caveat"]]),
        ]:
            if sub.empty:
                continue
            rows.append(
                {
                    "split": split,
                    "quality_group": caveat_state,
                    "n_galaxies": int(len(sub)),
                    "matched_beats_wrong_fraction": float(sub["matched_beats_wrong_mean"].mean()),
                    "matched_beats_tpg_v6_fraction": float(sub["matched_beats_tpg_v6"].mean()),
                    "matched_beats_mond_fraction": float(sub["matched_beats_mond"].mean()),
                    "mean_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].mean()),
                    "mean_matched_minus_tpg_v6": float(sub["matched_minus_tpg_v6"].mean()),
                    "mean_matched_minus_mond": float(sub["matched_minus_mond"].mean()),
                }
            )
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda x: f"{x:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def write_report(summary: pd.DataFrame, quality_groups: pd.DataFrame) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].copy()
    holdout = holdout.sort_values(["quality_status", "formula_family"])
    columns = [
        "formula_family",
        "n_galaxies",
        "mean_manifest_confidence",
        "any_quality_caveat_fraction",
        "low_inclination_fraction",
        "large_distance_error_fraction",
        "few_rotation_points_fraction",
        "matched_beats_wrong_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
        "quality_status",
    ]
    lines = [
        "# Family Observable Quality Diagnostics",
        "",
        "This diagnostic joins the train-selected shrinkage scores with the",
        "residual-blind morphology parameter manifest. It asks whether weak",
        "family rows are primarily data/manifest-quality limited or formula/",
        "normalization limited under the current available-data proxy setup.",
        "",
        "## Holdout Family Quality Map",
        "",
        markdown_table(holdout[columns]),
        "",
        "## Clean-vs-Caveated Manifest Comparison",
        "",
        markdown_table(quality_groups),
        "",
        "## Claim Boundary",
        "",
        "This is not a new fit and does not choose a new morphology family or",
        "amplitude policy. It is a failure-map diagnostic. If a family is marked",
        "quality-limited, the next step is better residual-blind morphology",
        "observable extraction. If it is formula/normalization-limited, the next",
        "step is a stronger Tau-side source normalization or readout kernel.",
    ]
    (REPORTS / "family_observable_quality_diagnostics.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    joined = load_joined()
    summary = summarize(joined)
    quality_groups = compare_caveated_vs_clean(joined)
    summary.to_csv(DATA / "family_observable_quality_diagnostics.csv", index=False)
    quality_groups.to_csv(
        DATA / "family_observable_quality_clean_vs_caveated.csv", index=False
    )
    write_report(summary, quality_groups)
    print("PAPER8_FAMILY_OBSERVABLE_QUALITY_DIAGNOSTICS_COMPLETE")


if __name__ == "__main__":
    main()
