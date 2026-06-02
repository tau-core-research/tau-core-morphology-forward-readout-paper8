#!/usr/bin/env python3
"""Evaluate predeclared morphology-quality gates under the fixed selected policy."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

import run_family_observable_quality_diagnostics as quality


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


QUALITY_GATES: dict[str, str] = {
    "all": "True",
    "confidence_ge_0_75": "manifest_confidence >= 0.75",
    "confidence_ge_0_85": "manifest_confidence >= 0.85",
    "no_low_inclination": "~low_inclination",
    "no_large_distance_error": "~large_distance_error",
    "no_few_rotation_points": "~few_rotation_points",
    "clean_manifest_proxy": "~any_quality_caveat",
    "confidence_ge_0_75_and_clean": "(manifest_confidence >= 0.75) & (~any_quality_caveat)",
}


def apply_gate(df: pd.DataFrame, expression: str) -> pd.Series:
    if expression == "True":
        return pd.Series(True, index=df.index)
    return df.eval(expression)


def summarize_gate(df: pd.DataFrame, gate_id: str, expression: str) -> dict[str, object]:
    mask = apply_gate(df, expression)
    sub = df.loc[mask].copy()
    row: dict[str, object] = {
        "quality_gate": gate_id,
        "gate_expression": expression,
        "n_galaxies": int(len(sub)),
        "n_families_present": int(sub["formula_family"].nunique()) if len(sub) else 0,
    }
    if sub.empty:
        for col in [
            "matched_beats_wrong_fraction",
            "matched_rank1_fraction",
            "matched_beats_tpg_v6_fraction",
            "matched_beats_mond_fraction",
            "mean_matched_minus_wrong",
            "mean_matched_minus_tpg_v6",
            "mean_matched_minus_mond",
        ]:
            row[col] = float("nan")
        row["gate_status"] = "empty"
        return row
    row.update(
        {
            "matched_beats_wrong_fraction": float(sub["matched_beats_wrong_mean"].mean()),
            "matched_rank1_fraction": float((sub["matched_family_rank"] == 1).mean()),
            "matched_beats_tpg_v6_fraction": float(sub["matched_beats_tpg_v6"].mean()),
            "matched_beats_mond_fraction": float(sub["matched_beats_mond"].mean()),
            "mean_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].mean()),
            "mean_matched_minus_tpg_v6": float(sub["matched_minus_tpg_v6"].mean()),
            "mean_matched_minus_mond": float(sub["matched_minus_mond"].mean()),
        }
    )
    row["gate_status"] = classify_gate(row)
    return row


def classify_gate(row: dict[str, object]) -> str:
    n = int(row["n_galaxies"])
    if n < 10:
        return "too_small"
    if (
        float(row["matched_beats_wrong_fraction"]) >= 0.80
        and float(row["matched_beats_mond_fraction"]) >= 0.60
        and float(row["matched_beats_tpg_v6_fraction"]) >= 0.50
    ):
        return "candidate_predeclared_gate"
    if float(row["matched_beats_wrong_fraction"]) >= 0.80:
        return "specificity_only"
    return "weak"


def summarize_by_gate_and_family(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gate_id, expression in QUALITY_GATES.items():
        gated = df.loc[apply_gate(df, expression)].copy()
        for (split, family), sub in gated.groupby(["split", "formula_family"], sort=True):
            rows.append(
                {
                    "quality_gate": gate_id,
                    "split": split,
                    "formula_family": family,
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


def write_report(summary: pd.DataFrame, by_family: pd.DataFrame) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].copy()
    holdout = holdout.sort_values(
        ["gate_status", "matched_beats_wrong_fraction", "matched_beats_mond_fraction"],
        ascending=[True, False, False],
    )
    family_holdout = by_family.loc[
        (by_family["split"] == "holdout")
        & (by_family["quality_gate"].isin(["all", "clean_manifest_proxy"]))
    ].copy()
    columns = [
        "quality_gate",
        "n_galaxies",
        "n_families_present",
        "matched_beats_wrong_fraction",
        "matched_rank1_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
        "mean_matched_minus_wrong",
        "mean_matched_minus_tpg_v6",
        "mean_matched_minus_mond",
        "gate_status",
    ]
    lines = [
        "# Predeclared Quality Gate Diagnostics",
        "",
        "This diagnostic evaluates several predeclared quality gates under the",
        "fixed train-selected shrinkage policy. It does not choose a gate by",
        "peeking at individual galaxy residuals; it reports which quality rules",
        "would be plausible candidates for a future endpoint protocol.",
        "",
        "## Holdout Quality Gates",
        "",
        markdown_table(holdout[columns]),
        "",
        "## Family Rows for All vs Clean Manifest Gate",
        "",
        markdown_table(family_holdout),
        "",
        "## Claim Boundary",
        "",
        "A candidate quality gate is not a discovery claim. It is a proposed",
        "predeclared observability rule for the next run. Any final Paper 8",
        "endpoint must declare the quality gate before endpoint scoring and keep",
        "the excluded/caveated rows as negative or limited-observability evidence.",
    ]
    (REPORTS / "predeclared_quality_gate_diagnostics.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    joined = quality.load_joined()
    rows = []
    for split in sorted(joined["split"].unique()):
        split_df = joined.loc[joined["split"] == split]
        for gate_id, expression in QUALITY_GATES.items():
            row = summarize_gate(split_df, gate_id, expression)
            row["split"] = split
            rows.append(row)
    summary = pd.DataFrame(rows)
    by_family = summarize_by_gate_and_family(joined)
    summary.to_csv(DATA / "predeclared_quality_gate_diagnostics.csv", index=False)
    by_family.to_csv(DATA / "predeclared_quality_gate_by_family.csv", index=False)
    write_report(summary, by_family)
    print("PAPER8_PREDECLARED_QUALITY_GATE_DIAGNOSTICS_COMPLETE")


if __name__ == "__main__":
    main()
