#!/usr/bin/env python3
"""Diagnose whether manifest quality is the bottleneck for Paper 8 preflights."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
SHUFFLE_SEED = 16180
N_SHUFFLES = 1000
FAMILIES = [
    "K_compact_finite",
    "K_scale_tail_spiral",
    "K_exponential_disk",
    "K_thick_flared",
]


def load_joined() -> pd.DataFrame:
    scores = pd.read_csv(DATA / "source_native_readout_formula_scores_by_galaxy.csv")
    manifest = pd.read_csv(
        DATA / "morphology_parameter_manifest.csv",
        usecols=[
            "galaxy",
            "manifest_confidence",
            "manifest_caveat",
            "type_bin",
            "inc_bin",
            "distance_frac_error",
            "inclination_error_deg",
        ],
    )
    return scores.merge(manifest, on="galaxy", how="left")


def summarize_subset(name: str, sub: pd.DataFrame) -> dict[str, object]:
    return {
        "subset": name,
        "n_galaxies": int(len(sub)),
        "mean_confidence": float(sub["manifest_confidence"].mean()) if len(sub) else np.nan,
        "matched_beats_wrong_fraction": float(sub["matched_beats_wrong_mean"].mean()) if len(sub) else np.nan,
        "matched_rank1_fraction": float((sub["matched_family_rank"] == 1).mean()) if len(sub) else np.nan,
        "matched_beats_tpg_v6_fraction": float(sub["matched_beats_tpg_v6"].mean()) if len(sub) else np.nan,
        "matched_beats_mond_fraction": float(sub["matched_beats_mond"].mean()) if len(sub) else np.nan,
        "mean_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].mean()) if len(sub) else np.nan,
        "median_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].median()) if len(sub) else np.nan,
        "mean_matched_minus_tpg_v6": float(sub["matched_minus_tpg_v6"].mean()) if len(sub) else np.nan,
        "median_matched_minus_tpg_v6": float(sub["matched_minus_tpg_v6"].median()) if len(sub) else np.nan,
        "mean_matched_minus_mond": float(sub["matched_minus_mond"].mean()) if len(sub) else np.nan,
        "median_matched_minus_mond": float(sub["matched_minus_mond"].median()) if len(sub) else np.nan,
    }


def build_subsets(joined: pd.DataFrame) -> dict[str, pd.DataFrame]:
    subsets = {
        "all": joined,
        "confidence_ge_0_75": joined.loc[joined["manifest_confidence"] >= 0.75],
        "confidence_ge_0_85": joined.loc[joined["manifest_confidence"] >= 0.85],
        "confidence_ge_0_95": joined.loc[joined["manifest_confidence"] >= 0.95],
        "no_manifest_caveat": joined.loc[joined["manifest_caveat"] == "none"],
        "no_low_inclination": joined.loc[~joined["manifest_caveat"].str.contains("low_inclination")],
        "no_large_distance_error": joined.loc[
            ~joined["manifest_caveat"].str.contains("large_distance_error")
        ],
    }
    return {name: sub.copy() for name, sub in subsets.items() if len(sub) >= 5}


def run_shuffle_for_subset(name: str, sub: pd.DataFrame) -> dict[str, object]:
    rng = np.random.default_rng(SHUFFLE_SEED)
    sub = sub.reset_index(drop=True)
    true_labels = sub["formula_family"].to_numpy()
    observed_mean = float(sub["matched_minus_wrong_mean"].mean())
    observed_beats = float(sub["matched_beats_wrong_mean"].mean())
    observed_rank1 = float((sub["matched_family_rank"] == 1).mean())
    shuffled_mean = []
    shuffled_beats = []
    shuffled_rank1 = []
    for _ in range(N_SHUFFLES):
        labels = rng.permutation(true_labels)
        minus_wrong = []
        beats_wrong = []
        ranks = []
        for row_idx, family in enumerate(labels):
            scores = {candidate: float(sub.loc[row_idx, f"rmse_{candidate}"]) for candidate in FAMILIES}
            selected = scores[family]
            wrong = [value for candidate, value in scores.items() if candidate != family]
            wrong_mean = float(sum(wrong) / len(wrong))
            minus_wrong.append(selected - wrong_mean)
            beats_wrong.append(selected < wrong_mean)
            ranks.append(sorted(FAMILIES, key=lambda candidate: scores[candidate]).index(family) + 1)
        shuffled_mean.append(float(np.mean(minus_wrong)))
        shuffled_beats.append(float(np.mean(beats_wrong)))
        shuffled_rank1.append(float(np.mean(np.array(ranks) == 1)))
    shuffled_mean_arr = np.asarray(shuffled_mean)
    shuffled_beats_arr = np.asarray(shuffled_beats)
    shuffled_rank1_arr = np.asarray(shuffled_rank1)
    return {
        "subset": name,
        "n_shuffles": N_SHUFFLES,
        "seed": SHUFFLE_SEED,
        "observed_mean_minus_wrong": observed_mean,
        "null_mean_minus_wrong_mean": float(shuffled_mean_arr.mean()),
        "p_mean_minus_wrong_at_least_as_good": float(
            (1 + (shuffled_mean_arr <= observed_mean).sum()) / (N_SHUFFLES + 1)
        ),
        "observed_beats_wrong_fraction": observed_beats,
        "null_beats_wrong_fraction_mean": float(shuffled_beats_arr.mean()),
        "p_beats_wrong_fraction_at_least_as_good": float(
            (1 + (shuffled_beats_arr >= observed_beats).sum()) / (N_SHUFFLES + 1)
        ),
        "observed_rank1_fraction": observed_rank1,
        "null_rank1_fraction_mean": float(shuffled_rank1_arr.mean()),
        "p_rank1_fraction_at_least_as_good": float(
            (1 + (shuffled_rank1_arr >= observed_rank1).sum()) / (N_SHUFFLES + 1)
        ),
    }


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


def write_report(summary: pd.DataFrame, shuffled: pd.DataFrame) -> None:
    holdout = summary.loc[summary["subset"].str.startswith("holdout:")].copy()
    holdout_shuffled = shuffled.loc[shuffled["subset"].str.startswith("holdout:")].copy()
    lines = [
        "# Manifest Confidence Diagnostics",
        "",
        "This diagnostic asks whether the source-native bridge formula endpoint",
        "improves when restricted to higher-confidence morphology-parameter",
        "manifest subsets. It is a data-quality and manifest-quality diagnostic,",
        "not a new fit.",
        "",
        "## Holdout Subsets",
        "",
        markdown_table(holdout),
        "",
        "## Holdout Shuffled Nulls",
        "",
        markdown_table(holdout_shuffled),
        "",
        "## Claim Boundary",
        "",
        "If high-confidence subsets improve baseline performance, the bottleneck is",
        "likely morphology parameter quality. If they do not, the bottleneck is",
        "more likely amplitude policy, formula normalization, or missing source-native",
        "morphology observables.",
    ]
    (REPORTS / "manifest_confidence_diagnostics.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    joined = load_joined()
    rows = []
    shuffled_rows = []
    for split, split_df in joined.groupby("split"):
        for subset_name, sub in build_subsets(split_df).items():
            name = f"{split}:{subset_name}"
            rows.append(summarize_subset(name, sub))
            shuffled_rows.append(run_shuffle_for_subset(name, sub))
    summary = pd.DataFrame(rows).sort_values("subset")
    shuffled = pd.DataFrame(shuffled_rows).sort_values("subset")
    summary.to_csv(DATA / "manifest_confidence_diagnostics_summary.csv", index=False)
    shuffled.to_csv(DATA / "manifest_confidence_diagnostics_shuffled.csv", index=False)
    write_report(summary, shuffled)
    print("PAPER8_MANIFEST_CONFIDENCE_DIAGNOSTICS_COMPLETE")


if __name__ == "__main__":
    main()
