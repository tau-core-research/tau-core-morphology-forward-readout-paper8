#!/usr/bin/env python3
"""Build the NGC4088 epsilon_cross bound-expression shell.

This script combines the residual-blind feature normalization with the blocked
B_i coefficient obligations. It produces the algebraic bound expression that is
ready for review, while keeping the numeric epsilon_cross bound blocked until
q_warp, m_history_warp, and B_i values are supplied without endpoint residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_epsilon_cross_bound_expression_shell_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def build_shell() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    features = pd.read_csv(DATA / "s4g75_ngc4088_bi_feature_normalization.csv")
    coefficients = pd.read_csv(DATA / "s4g75_ngc4088_bi_coefficient_obligations.csv")

    coefficient_by_feature = dict(
        zip(coefficients["multiplies_feature"], coefficients["coefficient_id"])
    )
    coefficient_status_by_feature = dict(
        zip(coefficients["multiplies_feature"], coefficients["status"])
    )
    coefficient_value_by_feature = dict(
        zip(coefficients["multiplies_feature"], coefficients["current_value"])
    )

    term_rows = []
    for _, feature in features.iterrows():
        feature_symbol = feature["feature_symbol"]
        coefficient_id = coefficient_by_feature[feature_symbol]
        feature_value = feature["feature_value"]
        coefficient_value = coefficient_value_by_feature[feature_symbol]
        feature_available = pd.notna(feature_value)
        coefficient_available = pd.notna(coefficient_value)
        if feature_available:
            term_expression = f"{float(feature_value):.6g}*{coefficient_id}"
        else:
            term_expression = f"{coefficient_id}*{feature_symbol}"
        term_rows.append(
            {
                "galaxy": GALAXY,
                "term_id": f"TERM_{coefficient_id}",
                "coefficient_id": coefficient_id,
                "feature_symbol": feature_symbol,
                "feature_value": feature_value,
                "feature_status": feature["status"],
                "coefficient_status": coefficient_status_by_feature[feature_symbol],
                "term_expression": term_expression,
                "term_numeric_value": (
                    float(feature_value) * float(coefficient_value)
                    if feature_available and coefficient_available
                    else None
                ),
                "term_status": (
                    "TERM_NUMERIC_PROTOCOL_BOUND_READY"
                    if feature_available and coefficient_available
                    else (
                        "TERM_SYMBOLIC_COEFFICIENT_BLOCKED"
                        if feature_available and not coefficient_available
                        else "TERM_BLOCKED_FEATURE_AND_COEFFICIENT"
                    )
                ),
                "unit": "dimensionless",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    terms = pd.DataFrame(term_rows)
    terms = terms[
        [
            "galaxy",
            "term_id",
            "coefficient_id",
            "feature_symbol",
            "feature_value",
            "feature_status",
            "coefficient_status",
            "term_expression",
            "term_numeric_value",
            "term_status",
            "unit",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    known_parts = list(
        terms.loc[
            terms["feature_value"].notna(), "term_expression"
        ].astype(str)
    )
    unknown_parts = list(
        terms.loc[
            terms["feature_value"].isna(), "term_expression"
        ].astype(str)
    )
    known_expression = " + ".join(known_parts) if known_parts else "none"
    unknown_expression = " + ".join(unknown_parts) if unknown_parts else "none"
    full_expression = " + ".join(terms["term_expression"].astype(str))
    all_terms_numeric = terms["term_numeric_value"].notna().all()
    numeric_bound = float(terms["term_numeric_value"].sum()) if all_terms_numeric else None
    next_required_action = (
        "numeric_protocol_bound_ready_interpret_with_caveats"
        if all_terms_numeric
        else (
            "independently_review_source_features_and_supply_B_i_values"
            if not unknown_parts
            else "fill_f_q_f_mem_and_B_i_values_before_numeric_bound"
        )
    )
    expression_status = (
        "NUMERIC_EPSILON_PROTOCOL_BOUND_READY_CAVEATED"
        if all_terms_numeric
        else "PARTIAL_FEATURE_EXPRESSION_READY_NUMERIC_BOUND_BLOCKED"
    )

    expression = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "expression_id": "NGC4088_EPSILON_CROSS_BOUND_EXPRESSION_SHELL",
                "bound_expression": f"|epsilon_cross| <= {full_expression}",
                "known_feature_subexpression": known_expression,
                "blocked_feature_subexpression": unknown_expression,
                "numeric_bound_value": numeric_bound,
                "expression_status": expression_status,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "expression_id": expression["expression_id"].iloc[0],
                "n_terms": len(terms),
                "n_terms_with_feature_values": int(terms["feature_value"].notna().sum()),
                "n_terms_numeric": int(terms["term_numeric_value"].notna().sum()),
                "n_blocked_terms": int((terms["term_numeric_value"].isna()).sum()),
                "bound_expression_status": expression["expression_status"].iloc[0],
                "numeric_bound_status": (
                    "NUMERIC_EPSILON_PROTOCOL_BOUND_AVAILABLE"
                    if all_terms_numeric
                    else "NUMERIC_EPSILON_BOUND_BLOCKED"
                ),
                "next_required_action": next_required_action,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return terms, expression, summary


def write_report(
    terms: pd.DataFrame,
    expression: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Epsilon-Cross Bound Expression Shell",
        "",
        "This shell combines the feature-normalization gate with the blocked B_i",
        "coefficient obligations. It computes a numeric protocol bound only",
        "when accepted source features and frozen residual-blind B_i values are",
        "available.",
        "",
        "## Expression",
        "",
        markdown_table(expression),
        "",
        "## Terms",
        "",
        markdown_table(terms),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "The expression is residual-blind. A numeric value, when present, is a",
        "conservative protocol upper bound for epsilon_cross, not an endpoint",
        "fit or a final sharp Tau-side amplitude derivation.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_epsilon_cross_bound_expression_shell.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    terms, expression, summary = build_shell()
    terms.to_csv(DATA / "s4g75_ngc4088_epsilon_cross_bound_terms.csv", index=False)
    expression.to_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_bound_expression.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_bound_expression_summary.csv",
        index=False,
    )
    write_report(terms, expression, summary)
    print("PAPER8_NGC4088_EPSILON_CROSS_BOUND_EXPRESSION_SHELL_COMPLETE")


if __name__ == "__main__":
    main()
