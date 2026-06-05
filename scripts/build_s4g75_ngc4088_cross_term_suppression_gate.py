#!/usr/bin/env python3
"""Build the NGC4088 cross-term suppression gate.

This gate records the next condition needed after conditional separability:
mixed source-source terms must be absent, negligible, or explicitly bounded.
It introduces a residual-blind symbolic epsilon_cross correction without using
endpoint velocities or residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_cross_term_suppression_gate_not_endpoint"


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


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    coupling_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_multiplicative_coupling_separability_summary.csv"
    ).iloc[0]
    lambda0 = float(coupling_summary["lambda_product_km2_s2"])

    model = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "model_id": "LEADING_PRODUCT_PLUS_EPSILON_CROSS",
                "leading_formula": "lambda_0 = sigma_warp q_warp x_w Vflat^2",
                "extended_formula": "lambda_w = lambda_0 * (1 + epsilon_cross)",
                "lambda0_km2_s2": lambda0,
                "epsilon_cross_status": "UNBOUNDED_SYMBOLIC_CORRECTION",
                "proof_status": "LEADING_ORDER_ONLY_UNTIL_CROSS_TERMS_SUPPRESSED",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    cross_terms = pd.DataFrame(
        [
            {
                "term_id": "CROSS_ORIENTATION_STRENGTH",
                "term_symbol": "epsilon_sigma_q",
                "term_status": "NOT_DERIVED",
                "interpretation": "orientation sign and source strength may couple beyond a product factor",
            },
            {
                "term_id": "CROSS_ONSET_STRENGTH",
                "term_symbol": "epsilon_x_q",
                "term_status": "NOT_DERIVED",
                "interpretation": "onset radius and warp source strength may have mixed dependence",
            },
            {
                "term_id": "CROSS_ONSET_CARRIER",
                "term_symbol": "epsilon_x_vflat",
                "term_status": "NOT_DERIVED",
                "interpretation": "onset support and asymptotic carrier may not separate exactly",
            },
            {
                "term_id": "CROSS_GEOMETRY_MEMORY",
                "term_symbol": "epsilon_memory",
                "term_status": "NOT_DERIVED",
                "interpretation": "morphological history/memory may modify the present-day source product",
            },
        ]
    )
    cross_terms["galaxy"] = GALAXY
    cross_terms["claim_boundary"] = CLAIM_BOUNDARY
    cross_terms = cross_terms[
        ["galaxy", "term_id", "term_symbol", "term_status", "interpretation", "claim_boundary"]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "X1_LEADING_PRODUCT_AVAILABLE",
                "gate_status": "PASS",
                "evidence": "lambda_0 = sigma q x_w Vflat^2 is conditionally derived under separability",
                "remaining_obligation": "none for leading product algebra",
            },
            {
                "gate_id": "X2_DIMENSIONAL_EXTENSION_VALID",
                "gate_status": "PASS",
                "evidence": "epsilon_cross is dimensionless, so lambda_w keeps km^2/s^2 units",
                "remaining_obligation": "none at dimensional level",
            },
            {
                "gate_id": "X3_CROSS_TERM_PARAMETER_DECLARED",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "epsilon_cross explicitly represents all omitted mixed source-source terms",
                "remaining_obligation": "derive or bound epsilon_cross from source data",
            },
            {
                "gate_id": "X4_ZERO_CROSS_TERM_LIMIT",
                "gate_status": "PASS",
                "evidence": "epsilon_cross = 0 recovers the current multiplicative readout formula",
                "remaining_obligation": "none for the limiting check",
            },
            {
                "gate_id": "X5_CROSS_TERM_SUPPRESSION_DERIVED",
                "gate_status": "BLOCKED",
                "evidence": "no Tau-side argument yet proves epsilon_cross is zero or higher-order",
                "remaining_obligation": "derive suppression from locality, independence, symmetry, or scale separation",
            },
            {
                "gate_id": "X6_SOURCE_BOUND_AVAILABLE",
                "gate_status": "BLOCKED",
                "evidence": "no residual-blind source bound on epsilon_cross is currently available",
                "remaining_obligation": "define source observables that bound mixed geometry/memory terms",
            },
            {
                "gate_id": "X7_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "epsilon_cross is symbolic and is not fit to observed rotation residuals",
                "remaining_obligation": "do not tune epsilon_cross in endpoint tests",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    status_counts = gates["gate_status"].value_counts().to_dict()
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "model_id": model["model_id"].iloc[0],
                "lambda0_km2_s2": lambda0,
                "n_cross_terms": len(cross_terms),
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "cross_term_status": "CROSS_TERMS_DECLARED_NOT_SUPPRESSED",
                "law_status": "LEADING_PRODUCT_ONLY_UNTIL_EPSILON_CROSS_BOUND",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return model, cross_terms, gates, summary


def write_report(
    model: pd.DataFrame,
    cross_terms: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Cross-Term Suppression Gate",
        "",
        "This gate records the correction structure that remains after the",
        "conditional separable product. The current product formula is a",
        "leading-order expression until mixed source-source terms are suppressed",
        "or bounded from residual-blind source observables.",
        "",
        "## Leading-Plus-Cross Model",
        "",
        markdown_table(model),
        "",
        "## Cross-Term Ledger",
        "",
        markdown_table(cross_terms),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "This is not an endpoint fit. epsilon_cross is symbolic and must not be",
        "tuned against observed rotation residuals.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_cross_term_suppression_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    model, cross_terms, gates, summary = build_gate()
    model.to_csv(DATA / "s4g75_ngc4088_cross_term_model.csv", index=False)
    cross_terms.to_csv(DATA / "s4g75_ngc4088_cross_term_ledger.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_cross_term_suppression_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_cross_term_suppression_summary.csv", index=False)
    write_report(model, cross_terms, gates, summary)
    print("PAPER8_NGC4088_CROSS_TERM_SUPPRESSION_GATE_COMPLETE")


if __name__ == "__main__":
    main()
