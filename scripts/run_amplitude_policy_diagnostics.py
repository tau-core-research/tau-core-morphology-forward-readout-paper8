#!/usr/bin/env python3
"""Diagnose amplitude-policy bottlenecks for source-native readout formulas."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import run_source_native_readout_formula_endpoint as src


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
POLICIES = [
    "family_unconstrained",
    "family_attractive_only",
    "global_unconstrained",
    "global_attractive_only",
    "family_shrink_50_to_global",
]


def fit_policy_amplitudes(points: pd.DataFrame, policy: str) -> pd.DataFrame:
    train = points.loc[points["split"] == "train"].copy()
    target = train["vobs"].pow(2) - train["v_v6"].pow(2)
    family_betas: dict[str, float] = {}
    for family in src.FORMULA_FAMILIES:
        sub = train.loc[train["formula_family"] == family]
        kernel = sub[f"kernel_{family}"]
        den = kernel.pow(2).sum()
        beta = float((target.loc[sub.index] * kernel).sum() / den) if den else 0.0
        family_betas[family] = beta

    matched_kernel = pd.Series(index=train.index, dtype=float)
    for family in src.FORMULA_FAMILIES:
        idx = train.index[train["formula_family"] == family]
        matched_kernel.loc[idx] = train.loc[idx, f"kernel_{family}"]
    global_den = matched_kernel.pow(2).sum()
    global_beta = float((target * matched_kernel).sum() / global_den) if global_den else 0.0

    rows = []
    for family in src.FORMULA_FAMILIES:
        if policy == "family_unconstrained":
            beta = family_betas[family]
        elif policy == "family_attractive_only":
            beta = max(0.0, family_betas[family])
        elif policy == "global_unconstrained":
            beta = global_beta
        elif policy == "global_attractive_only":
            beta = max(0.0, global_beta)
        elif policy == "family_shrink_50_to_global":
            beta = 0.5 * family_betas[family] + 0.5 * global_beta
        else:
            raise ValueError(policy)
        rows.append(
            {
                "amplitude_policy": policy,
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


def summarize_policy(points: pd.DataFrame, amplitudes: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    scored = src.add_predictions(points, amplitudes.rename(columns={"amplitude_policy": "_policy"}))
    galaxy_scores, summary, _ = src.score_galaxies(scored)
    policy = amplitudes["amplitude_policy"].iloc[0]
    galaxy_scores.insert(0, "amplitude_policy", policy)
    summary.insert(0, "amplitude_policy", policy)
    return galaxy_scores, summary


def write_report(summary: pd.DataFrame, amplitudes: pd.DataFrame) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].copy()
    lines = [
        "# Amplitude Policy Diagnostics",
        "",
        "This diagnostic keeps the source-native bridge formula kernels fixed and",
        "changes only the amplitude policy. It asks whether the current TPG/MOND",
        "baseline weakness is caused by amplitude normalization rather than by",
        "morphology-family formula specificity.",
        "",
        "## Holdout Policy Summary",
        "",
        markdown_table(holdout),
        "",
        "## Amplitudes",
        "",
        markdown_table(amplitudes),
        "",
        "## Claim Boundary",
        "",
        "This is not a new endpoint claim. It is an amplitude-policy stress test.",
        "A policy that improves baseline comparison must still be justified from",
        "Tau-side source normalization, not selected post hoc for fit quality.",
    ]
    (REPORTS / "amplitude_policy_diagnostics.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, _ = src.load_points()
    points = src.add_bridge_formula_kernels(points)
    all_amplitudes = []
    all_scores = []
    all_summaries = []
    for policy in POLICIES:
        amplitudes = fit_policy_amplitudes(points, policy)
        scores, summary = summarize_policy(points, amplitudes)
        all_amplitudes.append(amplitudes)
        all_scores.append(scores)
        all_summaries.append(summary)
    amplitudes_df = pd.concat(all_amplitudes, ignore_index=True)
    scores_df = pd.concat(all_scores, ignore_index=True)
    summary_df = pd.concat(all_summaries, ignore_index=True)
    amplitudes_df.to_csv(DATA / "amplitude_policy_diagnostics_amplitudes.csv", index=False)
    scores_df.to_csv(DATA / "amplitude_policy_diagnostics_scores_by_galaxy.csv", index=False)
    summary_df.to_csv(DATA / "amplitude_policy_diagnostics_summary.csv", index=False)
    write_report(summary_df, amplitudes_df)
    print("PAPER8_AMPLITUDE_POLICY_DIAGNOSTICS_COMPLETE")


if __name__ == "__main__":
    main()
