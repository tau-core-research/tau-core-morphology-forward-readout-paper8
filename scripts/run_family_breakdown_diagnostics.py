#!/usr/bin/env python3
"""Break down train-selected shrinkage performance by morphology family."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


def load_selected_scores() -> tuple[pd.DataFrame, pd.DataFrame]:
    selections_path = DATA / "train_selected_shrinkage_selection.csv"
    scores_path = DATA / "amplitude_shrinkage_path_scores_by_galaxy.csv"
    if not selections_path.exists():
        raise FileNotFoundError(
            f"{selections_path} is missing; run scripts/run_train_selected_shrinkage_diagnostic.py"
        )
    if not scores_path.exists():
        raise FileNotFoundError(
            f"{scores_path} is missing; run scripts/run_amplitude_shrinkage_path.py"
        )
    selections = pd.read_csv(selections_path)
    selected_paths = sorted(selections["selected_amplitude_path_id"].unique())
    scores = pd.read_csv(scores_path)
    scores = scores.loc[scores["amplitude_path_id"].isin(selected_paths)].copy()
    return selections, scores


def summarize_by_family(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (path_id, split, family), sub in scores.groupby(
        ["amplitude_path_id", "split", "formula_family"], sort=True
    ):
        rows.append(
            {
                "amplitude_path_id": path_id,
                "split": split,
                "formula_family": family,
                "n_galaxies": int(len(sub)),
                "matched_beats_wrong_fraction": float(sub["matched_beats_wrong_mean"].mean()),
                "matched_rank1_fraction": float((sub["matched_family_rank"] == 1).mean()),
                "matched_beats_tpg_v6_fraction": float(sub["matched_beats_tpg_v6"].mean()),
                "matched_beats_mond_fraction": float(sub["matched_beats_mond"].mean()),
                "mean_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].mean()),
                "median_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].median()),
                "mean_matched_minus_tpg_v6": float(sub["matched_minus_tpg_v6"].mean()),
                "median_matched_minus_tpg_v6": float(sub["matched_minus_tpg_v6"].median()),
                "mean_matched_minus_mond": float(sub["matched_minus_mond"].mean()),
                "median_matched_minus_mond": float(sub["matched_minus_mond"].median()),
            }
        )
    out = pd.DataFrame(rows)
    out["specificity_status"] = out["matched_beats_wrong_fraction"].map(
        lambda x: "strong" if x >= 0.80 else "weak"
    )
    out["baseline_status"] = out.apply(classify_baseline_status, axis=1)
    return out


def classify_baseline_status(row: pd.Series) -> str:
    mond = row["matched_beats_mond_fraction"]
    tpg = row["matched_beats_tpg_v6_fraction"]
    if mond >= 0.60 and tpg >= 0.50:
        return "competitive_with_mond_and_tpg"
    if mond >= 0.60 and tpg < 0.50:
        return "mond_competitive_tpg_blocked"
    if mond < 0.60 and tpg >= 0.50:
        return "tpg_competitive_mond_blocked"
    return "baseline_blocked"


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


def write_report(selections: pd.DataFrame, by_family: pd.DataFrame) -> None:
    holdout = by_family.loc[by_family["split"] == "holdout"].copy()
    holdout = holdout.sort_values(
        ["matched_beats_wrong_fraction", "matched_beats_mond_fraction", "matched_beats_tpg_v6_fraction"],
        ascending=False,
    )
    train = by_family.loc[by_family["split"] == "train"].copy()
    train = train.sort_values(["formula_family"])
    selected = selections[
        ["selection_rule", "selected_family_weight", "selected_amplitude_path_id"]
    ].drop_duplicates()
    columns = [
        "formula_family",
        "n_galaxies",
        "matched_beats_wrong_fraction",
        "matched_rank1_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
        "mean_matched_minus_wrong",
        "mean_matched_minus_tpg_v6",
        "mean_matched_minus_mond",
        "specificity_status",
        "baseline_status",
    ]
    lines = [
        "# Family Breakdown Diagnostic",
        "",
        "This diagnostic uses only the train-selected shrinkage policy and breaks",
        "the result down by residual-blind morphology family. It does not refit",
        "per family and does not choose a new endpoint policy.",
        "",
        "## Selected Policies",
        "",
        markdown_table(selected),
        "",
        "## Holdout Family Breakdown",
        "",
        markdown_table(holdout[columns]),
        "",
        "## Train Family Breakdown",
        "",
        markdown_table(train[columns]),
        "",
        "## Interpretation Boundary",
        "",
        "The useful question is not only whether the global endpoint improves.",
        "The family breakdown identifies which morphology families preserve",
        "matched-vs-wrong specificity and which families remain blocked by",
        "TPG/v6 or MOND comparators. This is a preparation diagnostic, not an",
        "empirical validation claim.",
    ]
    (REPORTS / "family_breakdown_diagnostics.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    selections, scores = load_selected_scores()
    by_family = summarize_by_family(scores)
    by_family.to_csv(DATA / "family_breakdown_diagnostics.csv", index=False)
    write_report(selections, by_family)
    print("PAPER8_FAMILY_BREAKDOWN_DIAGNOSTICS_COMPLETE")


if __name__ == "__main__":
    main()
