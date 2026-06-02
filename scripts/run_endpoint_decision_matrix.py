#!/usr/bin/env python3
"""Build a claim-bounded endpoint decision matrix from quality-gate diagnostics."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    gate_path = DATA / "predeclared_quality_gate_diagnostics.csv"
    null_path = DATA / "quality_gate_shuffled_null_summary.csv"
    for path in [gate_path, null_path]:
        if not path.exists():
            raise FileNotFoundError(f"{path} is missing; run scripts/reproduce.py first")
    gates = pd.read_csv(gate_path)
    nulls = pd.read_csv(null_path)
    return gates, nulls


def build_matrix(gates: pd.DataFrame, nulls: pd.DataFrame) -> pd.DataFrame:
    merged = gates.merge(
        nulls,
        on=["split", "quality_gate", "n_galaxies"],
        how="left",
        validate="one_to_one",
        suffixes=("", "_null"),
    )
    holdout = merged.loc[merged["split"] == "holdout"].copy()
    holdout["baseline_competitive"] = (
        (holdout["matched_beats_tpg_v6_fraction"] >= 0.50)
        & (holdout["matched_beats_mond_fraction"] >= 0.60)
    )
    holdout["specificity_fraction_pass"] = holdout["matched_beats_wrong_fraction"] >= 0.80
    holdout["shuffle_fraction_pass"] = (
        holdout["p_beats_wrong_fraction_at_least_as_good"] <= 0.05
    )
    holdout["shuffle_mean_pass"] = (
        holdout["p_mean_minus_wrong_at_least_as_good"] <= 0.05
    )
    holdout["null_support_status"] = holdout.apply(classify_null_support, axis=1)
    holdout["recommended_endpoint_role"] = holdout.apply(recommend_role, axis=1)
    holdout["decision_score"] = holdout.apply(decision_score, axis=1)
    columns = [
        "quality_gate",
        "n_galaxies",
        "n_families_present",
        "matched_beats_wrong_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
        "p_beats_wrong_fraction_at_least_as_good",
        "p_mean_minus_wrong_at_least_as_good",
        "baseline_competitive",
        "null_support_status",
        "recommended_endpoint_role",
        "decision_score",
    ]
    return holdout[columns].sort_values(
        ["recommended_endpoint_role", "decision_score"], ascending=[True, False]
    )


def classify_null_support(row: pd.Series) -> str:
    if row["shuffle_fraction_pass"] and row["shuffle_mean_pass"]:
        return "strong_fraction_and_mean_null"
    if row["shuffle_mean_pass"]:
        return "mean_null_only"
    if row["shuffle_fraction_pass"]:
        return "fraction_null_only"
    return "weak_null"


def recommend_role(row: pd.Series) -> str:
    if row["baseline_competitive"] and row["null_support_status"] == "strong_fraction_and_mean_null":
        return "primary_endpoint_candidate"
    if row["baseline_competitive"]:
        return "baseline_competitiveness_secondary"
    if row["null_support_status"] == "strong_fraction_and_mean_null":
        return "specificity_null_primary"
    if row["matched_beats_wrong_fraction"] >= 0.80:
        return "specificity_only_diagnostic"
    return "limited_or_negative_control"


def decision_score(row: pd.Series) -> float:
    p_fraction = max(float(row["p_beats_wrong_fraction_at_least_as_good"]), 1e-12)
    p_mean = max(float(row["p_mean_minus_wrong_at_least_as_good"]), 1e-12)
    null_score = (1.0 - p_fraction) + (1.0 - p_mean)
    baseline_score = (
        float(row["matched_beats_tpg_v6_fraction"]) + float(row["matched_beats_mond_fraction"])
    )
    specificity_score = float(row["matched_beats_wrong_fraction"])
    sample_score = min(float(row["n_galaxies"]) / 44.0, 1.0)
    return specificity_score + baseline_score + 0.5 * null_score + 0.25 * sample_score


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


def write_report(matrix: pd.DataFrame) -> None:
    columns = [
        "quality_gate",
        "n_galaxies",
        "matched_beats_wrong_fraction",
        "matched_beats_tpg_v6_fraction",
        "matched_beats_mond_fraction",
        "p_beats_wrong_fraction_at_least_as_good",
        "p_mean_minus_wrong_at_least_as_good",
        "null_support_status",
        "recommended_endpoint_role",
    ]
    primary = matrix.loc[matrix["recommended_endpoint_role"] == "primary_endpoint_candidate"]
    specificity = matrix.loc[matrix["recommended_endpoint_role"] == "specificity_null_primary"]
    baseline = matrix.loc[
        matrix["recommended_endpoint_role"] == "baseline_competitiveness_secondary"
    ]
    lines = [
        "# Endpoint Decision Matrix",
        "",
        "This matrix combines the predeclared quality-gate endpoint metrics with",
        "the shuffled-family null diagnostics. It is a protocol decision aid, not",
        "a new fit and not an empirical validation claim.",
        "",
        "## Holdout Decision Matrix",
        "",
        markdown_table(matrix[columns]),
        "",
        "## Claim-Safe Endpoint Recommendation",
        "",
    ]
    if not primary.empty:
        best = primary.sort_values("decision_score", ascending=False).iloc[0]
        lines.append(
            "At least one gate currently satisfies both baseline-competitiveness and "
            "strong shuffled-null support. This would be the natural primary endpoint "
            "candidate, subject to predeclaration."
        )
        lines.append(
            f"Current primary endpoint candidate: {best['quality_gate']} "
            f"(n={int(best['n_galaxies'])})."
        )
    else:
        lines.extend(
            [
                "No current gate simultaneously satisfies baseline competitiveness and",
                "strong shuffled-null support on holdout. The claim-safe Paper 8",
                "strategy is therefore two-lane:",
                "",
                "1. Use the strongest null-supported gate as the primary",
                "morphology-specificity endpoint.",
                "2. Use the cleaner observability gates as secondary baseline-",
                "competitiveness endpoints.",
            ]
        )
    if not primary.empty and not specificity.empty:
        best = specificity.sort_values("decision_score", ascending=False).iloc[0]
        lines.append(
            f"Fuller-sample specificity support remains visible in: {best['quality_gate']} "
            f"(n={int(best['n_galaxies'])})."
        )
    elif not specificity.empty:
        best = specificity.sort_values("decision_score", ascending=False).iloc[0]
        lines.append(
            f"Current specificity-null primary candidate: {best['quality_gate']} "
            f"(n={int(best['n_galaxies'])})."
        )
    if not baseline.empty:
        best = baseline.sort_values("decision_score", ascending=False).iloc[0]
        lines.append(
            f"Current baseline-competitiveness secondary candidate: {best['quality_gate']} "
            f"(n={int(best['n_galaxies'])})."
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "This recommendation must not be read as selecting a winning endpoint",
            "after seeing the data. It records the present preparation-state tradeoff",
            "so that a future Paper 8 run can predeclare its primary and secondary",
            "endpoint lanes before endpoint scoring.",
        ]
    )
    (REPORTS / "endpoint_decision_matrix.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    gates, nulls = load_inputs()
    matrix = build_matrix(gates, nulls)
    matrix.to_csv(DATA / "endpoint_decision_matrix.csv", index=False)
    write_report(matrix)
    print("PAPER8_ENDPOINT_DECISION_MATRIX_COMPLETE")


if __name__ == "__main__":
    main()
