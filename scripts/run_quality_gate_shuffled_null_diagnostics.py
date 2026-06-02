#!/usr/bin/env python3
"""Run shuffled-family nulls inside predeclared quality gates."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import run_family_observable_quality_diagnostics as quality
import run_predeclared_quality_gate_diagnostics as gates


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FORMULA_FAMILIES = [
    "K_compact_finite",
    "K_scale_tail_spiral",
    "K_exponential_disk",
    "K_thick_flared",
]
N_SHUFFLES = 1000
SHUFFLE_SEED = 20260602


def observed_for_subset(sub: pd.DataFrame) -> dict[str, float]:
    return {
        "observed_mean_minus_wrong": float(sub["matched_minus_wrong_mean"].mean()),
        "observed_beats_wrong_fraction": float(sub["matched_beats_wrong_mean"].mean()),
        "observed_rank1_fraction": float((sub["matched_family_rank"] == 1).mean()),
    }


def shuffled_for_subset(
    sub: pd.DataFrame, split: str, quality_gate: str, rng: np.random.Generator
) -> pd.DataFrame:
    sub = sub.reset_index(drop=True)
    true_labels = sub["formula_family"].to_numpy()
    observed = observed_for_subset(sub)
    rows = []
    for shuffle_id in range(N_SHUFFLES):
        shuffled = rng.permutation(true_labels)
        minus_wrong = []
        beats_wrong = []
        rank1 = []
        for row_idx, family in enumerate(shuffled):
            scores = {
                candidate: float(sub.loc[row_idx, f"rmse_{candidate}"])
                for candidate in FORMULA_FAMILIES
            }
            selected = scores[family]
            wrong = [value for candidate, value in scores.items() if candidate != family]
            wrong_mean = float(sum(wrong) / len(wrong))
            ranks = sorted(FORMULA_FAMILIES, key=lambda candidate: scores[candidate])
            minus_wrong.append(selected - wrong_mean)
            beats_wrong.append(selected < wrong_mean)
            rank1.append(ranks.index(family) == 0)
        rows.append(
            {
                "split": split,
                "quality_gate": quality_gate,
                "shuffle_id": shuffle_id,
                "seed": SHUFFLE_SEED,
                "n_galaxies": int(len(sub)),
                "mean_shuffled_minus_wrong": float(np.mean(minus_wrong)),
                "shuffled_beats_wrong_fraction": float(np.mean(beats_wrong)),
                "shuffled_rank1_fraction": float(np.mean(rank1)),
                **observed,
            }
        )
    return pd.DataFrame(rows)


def summarize_null(shuffled: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (split, quality_gate), sub in shuffled.groupby(["split", "quality_gate"], sort=True):
        observed = sub.iloc[0]
        n = len(sub)
        rows.append(
            {
                "split": split,
                "quality_gate": quality_gate,
                "n_galaxies": int(observed["n_galaxies"]),
                "n_shuffles": int(n),
                "seed": SHUFFLE_SEED,
                "observed_mean_minus_wrong": float(observed["observed_mean_minus_wrong"]),
                "null_mean_minus_wrong_mean": float(sub["mean_shuffled_minus_wrong"].mean()),
                "null_mean_minus_wrong_median": float(sub["mean_shuffled_minus_wrong"].median()),
                "p_mean_minus_wrong_at_least_as_good": float(
                    (1 + (sub["mean_shuffled_minus_wrong"] <= observed["observed_mean_minus_wrong"]).sum())
                    / (n + 1)
                ),
                "observed_beats_wrong_fraction": float(observed["observed_beats_wrong_fraction"]),
                "null_beats_wrong_fraction_mean": float(sub["shuffled_beats_wrong_fraction"].mean()),
                "null_beats_wrong_fraction_median": float(sub["shuffled_beats_wrong_fraction"].median()),
                "p_beats_wrong_fraction_at_least_as_good": float(
                    (
                        1
                        + (
                            sub["shuffled_beats_wrong_fraction"]
                            >= observed["observed_beats_wrong_fraction"]
                        ).sum()
                    )
                    / (n + 1)
                ),
                "observed_rank1_fraction": float(observed["observed_rank1_fraction"]),
                "null_rank1_fraction_mean": float(sub["shuffled_rank1_fraction"].mean()),
                "null_rank1_fraction_median": float(sub["shuffled_rank1_fraction"].median()),
                "p_rank1_fraction_at_least_as_good": float(
                    (1 + (sub["shuffled_rank1_fraction"] >= observed["observed_rank1_fraction"]).sum())
                    / (n + 1)
                ),
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


def write_report(summary: pd.DataFrame) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].copy()
    holdout = holdout.sort_values(
        ["p_beats_wrong_fraction_at_least_as_good", "observed_beats_wrong_fraction"]
    )
    columns = [
        "quality_gate",
        "n_galaxies",
        "observed_beats_wrong_fraction",
        "null_beats_wrong_fraction_mean",
        "p_beats_wrong_fraction_at_least_as_good",
        "observed_mean_minus_wrong",
        "null_mean_minus_wrong_mean",
        "p_mean_minus_wrong_at_least_as_good",
        "observed_rank1_fraction",
        "null_rank1_fraction_mean",
        "p_rank1_fraction_at_least_as_good",
    ]
    lines = [
        "# Quality Gate Shuffled Null Diagnostics",
        "",
        "This diagnostic reruns the shuffled-family label null inside each",
        "predeclared quality gate under the fixed train-selected shrinkage",
        "policy. It tests whether a quality gate keeps morphology-family",
        "specificity beyond what shuffled labels produce.",
        "",
        "## Holdout Shuffled Null Summary",
        "",
        markdown_table(holdout[columns]),
        "",
        "## Claim Boundary",
        "",
        "A low shuffled-null p-value is evidence for morphology-label specificity",
        "inside the selected quality gate, not empirical validation of Tau Core.",
        "Quality gates must be declared before endpoint scoring in any future",
        "paper endpoint, and caveated rows remain scientifically relevant.",
    ]
    (REPORTS / "quality_gate_shuffled_null_diagnostics.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    joined = quality.load_joined()
    rng = np.random.default_rng(SHUFFLE_SEED)
    shuffled_frames = []
    for split in sorted(joined["split"].unique()):
        split_df = joined.loc[joined["split"] == split]
        for gate_id, expression in gates.QUALITY_GATES.items():
            sub = split_df.loc[gates.apply_gate(split_df, expression)].copy()
            if len(sub) < 4:
                continue
            shuffled_frames.append(shuffled_for_subset(sub, split, gate_id, rng))
    shuffled = pd.concat(shuffled_frames, ignore_index=True)
    summary = summarize_null(shuffled)
    shuffled.to_csv(DATA / "quality_gate_shuffled_null.csv", index=False)
    summary.to_csv(DATA / "quality_gate_shuffled_null_summary.csv", index=False)
    write_report(summary)
    print("PAPER8_QUALITY_GATE_SHUFFLED_NULL_DIAGNOSTICS_COMPLETE")


if __name__ == "__main__":
    main()
