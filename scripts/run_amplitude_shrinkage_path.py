#!/usr/bin/env python3
"""Scan family-to-global amplitude shrinkage for bridge formula kernels."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import run_amplitude_policy_diagnostics as amp
import run_source_native_readout_formula_endpoint as src


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FAMILY_WEIGHTS = [round(x, 2) for x in np.linspace(0.0, 1.0, 21)]


def raw_betas(points: pd.DataFrame) -> tuple[dict[str, float], float]:
    train = points.loc[points["split"] == "train"].copy()
    target = train["vobs"].pow(2) - train["v_v6"].pow(2)
    family_betas = {}
    matched_kernel = pd.Series(index=train.index, dtype=float)
    for family in src.FORMULA_FAMILIES:
        sub = train.loc[train["formula_family"] == family]
        kernel = sub[f"kernel_{family}"]
        den = kernel.pow(2).sum()
        family_betas[family] = float((target.loc[sub.index] * kernel).sum() / den) if den else 0.0
        matched_kernel.loc[sub.index] = kernel
    global_den = matched_kernel.pow(2).sum()
    global_beta = float((target * matched_kernel).sum() / global_den) if global_den else 0.0
    return family_betas, global_beta


def amplitudes_for_weight(
    family_betas: dict[str, float], global_beta: float, family_weight: float
) -> pd.DataFrame:
    rows = []
    for family in src.FORMULA_FAMILIES:
        beta = family_weight * family_betas[family] + (1.0 - family_weight) * global_beta
        rows.append(
            {
                "shrinkage_policy": "family_to_global_linear",
                "family_weight": family_weight,
                "global_weight": 1.0 - family_weight,
                "formula_family": family,
                "beta_delta_v2_amplitude": beta,
                "raw_family_beta": family_betas[family],
                "raw_global_beta": global_beta,
                "is_negative": beta < 0,
                "kernel": f"kernel_{family}",
                "formula_source": src.FORMULA_SOURCES[family],
            }
        )
    return pd.DataFrame(rows)


def scan(points: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    family_betas, global_beta = raw_betas(points)
    all_amplitudes = []
    all_scores = []
    all_summary = []
    for family_weight in FAMILY_WEIGHTS:
        amplitudes = amplitudes_for_weight(family_betas, global_beta, family_weight)
        scored = src.add_predictions(points, amplitudes)
        galaxy_scores, summary, _ = src.score_galaxies(scored)
        label = f"shrink_family_weight_{family_weight:.2f}"
        amplitudes.insert(0, "amplitude_path_id", label)
        galaxy_scores.insert(0, "amplitude_path_id", label)
        summary.insert(0, "amplitude_path_id", label)
        summary.insert(1, "family_weight", family_weight)
        summary.insert(2, "global_weight", 1.0 - family_weight)
        all_amplitudes.append(amplitudes)
        all_scores.append(galaxy_scores)
        all_summary.append(summary)
    return (
        pd.concat(all_amplitudes, ignore_index=True),
        pd.concat(all_scores, ignore_index=True),
        pd.concat(all_summary, ignore_index=True),
    )


def select_tradeoff(summary: pd.DataFrame) -> pd.DataFrame:
    holdout = summary.loc[summary["split"] == "holdout"].copy()
    holdout["specificity_ok"] = holdout["matched_beats_wrong_fraction"] >= 0.80
    holdout["mond_win_ok"] = holdout["matched_beats_mond_fraction"] >= 0.60
    holdout["tpg_win_ok"] = holdout["matched_beats_tpg_v6_fraction"] >= 0.50
    holdout["tradeoff_score"] = (
        holdout["matched_beats_wrong_fraction"]
        + holdout["matched_beats_mond_fraction"]
        + holdout["matched_beats_tpg_v6_fraction"]
        - 0.02 * holdout["mean_matched_minus_wrong"].clip(lower=0.0)
    )
    return holdout.sort_values(["specificity_ok", "mond_win_ok", "tradeoff_score"], ascending=False)


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


def write_report(summary: pd.DataFrame, tradeoff: pd.DataFrame) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].copy()
    lines = [
        "# Amplitude Shrinkage Path",
        "",
        "This scan varies only the linear family-to-global amplitude shrinkage",
        "weight for the source-native bridge formula kernels. It is a diagnostic",
        "for the Tau-side amplitude-normalization gate, not a selected endpoint.",
        "",
        "## Holdout Path",
        "",
        markdown_table(
            holdout[
                [
                    "family_weight",
                    "matched_beats_wrong_fraction",
                    "matched_beats_tpg_v6_fraction",
                    "matched_beats_mond_fraction",
                    "mean_matched_minus_wrong",
                    "mean_matched_minus_tpg_v6",
                    "mean_matched_minus_mond",
                ]
            ]
        ),
        "",
        "## Tradeoff Ranking",
        "",
        markdown_table(
            tradeoff[
                [
                    "family_weight",
                    "specificity_ok",
                    "mond_win_ok",
                    "tpg_win_ok",
                    "tradeoff_score",
                    "matched_beats_wrong_fraction",
                    "matched_beats_tpg_v6_fraction",
                    "matched_beats_mond_fraction",
                    "mean_matched_minus_mond",
                ]
            ].head(8)
        ),
        "",
        "## Claim Boundary",
        "",
        "The best-looking shrinkage point is not a validated physical policy.",
        "It identifies the amplitude-normalization range that the Tau-side theory",
        "would need to justify before Paper 8 can claim baseline competitiveness.",
    ]
    (REPORTS / "amplitude_shrinkage_path.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, _ = src.load_points()
    points = src.add_bridge_formula_kernels(points)
    amplitudes, scores, summary = scan(points)
    tradeoff = select_tradeoff(summary)
    amplitudes.to_csv(DATA / "amplitude_shrinkage_path_amplitudes.csv", index=False)
    scores.to_csv(DATA / "amplitude_shrinkage_path_scores_by_galaxy.csv", index=False)
    summary.to_csv(DATA / "amplitude_shrinkage_path_summary.csv", index=False)
    tradeoff.to_csv(DATA / "amplitude_shrinkage_path_tradeoff.csv", index=False)
    write_report(summary, tradeoff)
    print("PAPER8_AMPLITUDE_SHRINKAGE_PATH_COMPLETE")


if __name__ == "__main__":
    main()
