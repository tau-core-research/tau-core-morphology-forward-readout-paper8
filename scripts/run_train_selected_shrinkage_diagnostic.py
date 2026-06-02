#!/usr/bin/env python3
"""Select shrinkage weights on train only and evaluate holdout."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


def load_summary() -> pd.DataFrame:
    path = DATA / "amplitude_shrinkage_path_summary.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} is missing; run scripts/run_amplitude_shrinkage_path.py first"
        )
    return pd.read_csv(path)


def add_selection_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["specificity_ok"] = out["matched_beats_wrong_fraction"] >= 0.80
    out["mond_win_ok"] = out["matched_beats_mond_fraction"] >= 0.55
    out["tpg_win_ok"] = out["matched_beats_tpg_v6_fraction"] >= 0.50
    out["balanced_score"] = (
        out["matched_beats_wrong_fraction"]
        + out["matched_beats_mond_fraction"]
        + out["matched_beats_tpg_v6_fraction"]
        - 0.02 * out["mean_matched_minus_wrong"].clip(lower=0.0)
    )
    out["baseline_score"] = (
        out["matched_beats_mond_fraction"]
        + out["matched_beats_tpg_v6_fraction"]
        - 0.02 * out["mean_matched_minus_mond"].clip(lower=0.0)
        - 0.02 * out["mean_matched_minus_tpg_v6"].clip(lower=0.0)
    )
    out["specificity_score"] = (
        out["matched_beats_wrong_fraction"]
        - 0.02 * out["mean_matched_minus_wrong"].clip(lower=0.0)
    )
    return out


def select_rules(summary: pd.DataFrame) -> pd.DataFrame:
    train = summary.loc[summary["split"] == "train"].copy()
    rows = []

    def pick(rule: str, candidates: pd.DataFrame, sort_cols: list[str], ascending: list[bool]) -> None:
        selected = candidates.sort_values(sort_cols, ascending=ascending).iloc[0]
        rows.append(
            {
                "selection_rule": rule,
                "selected_family_weight": float(selected["family_weight"]),
                "selected_amplitude_path_id": selected["amplitude_path_id"],
                "train_balanced_score": float(selected["balanced_score"]),
                "train_baseline_score": float(selected["baseline_score"]),
                "train_specificity_score": float(selected["specificity_score"]),
                "train_specificity_ok": bool(selected["specificity_ok"]),
                "train_mond_win_ok": bool(selected["mond_win_ok"]),
                "train_tpg_win_ok": bool(selected["tpg_win_ok"]),
            }
        )

    pick(
        "train_balanced_max",
        train,
        ["balanced_score", "matched_beats_wrong_fraction", "matched_beats_mond_fraction"],
        [False, False, False],
    )
    pick(
        "train_specificity_then_baseline",
        train.loc[train["specificity_ok"]],
        ["baseline_score", "matched_beats_wrong_fraction"],
        [False, False],
    )
    pick(
        "train_mond_gap_min_with_specificity",
        train.loc[train["specificity_ok"]],
        ["mean_matched_minus_mond", "matched_beats_wrong_fraction"],
        [True, False],
    )
    pick(
        "train_tpg_gap_min_with_specificity",
        train.loc[train["specificity_ok"]],
        ["mean_matched_minus_tpg_v6", "matched_beats_wrong_fraction"],
        [True, False],
    )
    return pd.DataFrame(rows)


def evaluate_holdout(summary: pd.DataFrame, selections: pd.DataFrame) -> pd.DataFrame:
    holdout = summary.loc[summary["split"] == "holdout"].copy()
    rows = []
    for _, selected in selections.iterrows():
        row = holdout.loc[holdout["family_weight"] == selected["selected_family_weight"]].iloc[0]
        merged = selected.to_dict()
        for col in [
            "n_galaxies",
            "matched_beats_wrong_fraction",
            "matched_rank1_fraction",
            "matched_beats_tpg_v6_fraction",
            "matched_beats_mond_fraction",
            "mean_matched_minus_wrong",
            "median_matched_minus_wrong",
            "mean_matched_minus_tpg_v6",
            "median_matched_minus_tpg_v6",
            "mean_matched_minus_mond",
            "median_matched_minus_mond",
        ]:
            merged[f"holdout_{col}"] = row[col]
        rows.append(merged)
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


def write_report(selections: pd.DataFrame, evaluation: pd.DataFrame) -> None:
    lines = [
        "# Train-Selected Shrinkage Diagnostic",
        "",
        "This diagnostic selects the family-to-global shrinkage weight using train",
        "split metrics only, then evaluates the selected policy on holdout. It is",
        "designed to prevent reading the shrinkage weight directly from holdout.",
        "",
        "## Train Selections",
        "",
        markdown_table(selections),
        "",
        "## Holdout Evaluation",
        "",
        markdown_table(evaluation),
        "",
        "## Claim Boundary",
        "",
        "This is still a diagnostic, not a validated amplitude-normalization law.",
        "A train-selected weight that transfers to holdout is evidence for a stable",
        "normalization range, but the range must still be derived from Tau-side",
        "source normalization before it can be used as a paper endpoint policy.",
    ]
    (REPORTS / "train_selected_shrinkage_diagnostic.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    summary = add_selection_scores(load_summary())
    selections = select_rules(summary)
    evaluation = evaluate_holdout(summary, selections)
    selections.to_csv(DATA / "train_selected_shrinkage_selection.csv", index=False)
    evaluation.to_csv(DATA / "train_selected_shrinkage_holdout.csv", index=False)
    write_report(selections, evaluation)
    print("PAPER8_TRAIN_SELECTED_SHRINKAGE_DIAGNOSTIC_COMPLETE")


if __name__ == "__main__":
    main()
