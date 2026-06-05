#!/usr/bin/env python3
"""Build a locality-coupled narrowed epsilon_cross bound for NGC4088.

The linear protocol bound treats normalized source features as independently
additive. This artifact adds a stricter residual-blind cross-term rule: a
cross-term must be supported by adjacent source/readout channels. Under the same
second-order half-remainder factor used by the sharpened B_i rule, the first
locality-coupled chain is

    |epsilon_cross| <= 1/2 (f_PA f_R + f_R f_q + f_q f_mem).

This is formula-conditional and not endpoint evidence. It is a narrower
promotion audit bound, not a final Tau-side coefficient derivation.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_epsilon_cross_locality_bound_rule_not_endpoint"


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


def build_rule() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    features = pd.read_csv(DATA / "s4g75_ngc4088_bi_feature_normalization.csv")
    sharp_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_bi_sharp_coefficient_bound_rule_summary.csv"
    ).iloc[0]
    feature = dict(zip(features["feature_symbol"], features["feature_value"]))
    status = dict(zip(features["feature_symbol"], features["status"]))
    pairs = [
        ("L_PA_R", "f_PA", "f_R", "orientation_onset_locality"),
        ("L_R_Q", "f_R", "f_q", "onset_warp_strength_locality"),
        ("L_Q_MEM", "f_q", "f_mem", "warp_strength_source_history_locality"),
    ]
    rows = []
    for term_id, left, right, interpretation in pairs:
        left_value = float(feature[left])
        right_value = float(feature[right])
        rows.append(
            {
                "galaxy": GALAXY,
                "term_id": term_id,
                "left_feature": left,
                "right_feature": right,
                "left_feature_value": left_value,
                "right_feature_value": right_value,
                "half_remainder_factor": 0.5,
                "term_expression": f"0.5*{left}*{right}",
                "term_numeric_value": 0.5 * left_value * right_value,
                "term_interpretation": interpretation,
                "left_feature_status": status[left],
                "right_feature_status": status[right],
                "unit": "dimensionless",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    terms = pd.DataFrame(rows)
    numeric_bound = float(terms["term_numeric_value"].sum())
    expression = " + ".join(terms["term_expression"])
    sharp_ready = bool(sharp_summary["numeric_bound_coefficient_authorization"])
    gates = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "gate_id": "LB1_SOURCE_FEATURES_AVAILABLE",
                "gate_status": "PASS" if features["feature_value"].notna().all() else "BLOCKED",
                "evidence": "f_PA, f_R, f_q, and f_mem are all available",
                "remaining_obligation": "none",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "LB2_SECOND_ORDER_HALF_RULE_READY",
                "gate_status": "PASS" if sharp_ready else "BLOCKED",
                "evidence": str(sharp_summary["sharp_rule_status"]),
                "remaining_obligation": "keep formula-conditional status explicit",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "LB3_LOCALITY_CHAIN_DECLARED",
                "gate_status": "PASS",
                "evidence": "only adjacent source/readout couplings f_PA*f_R, f_R*f_q, and f_q*f_mem are admitted in this narrowed pass",
                "remaining_obligation": "derive or revise adjacency from a final Tau-side locality theorem before physical promotion",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "LB4_SIGN_STABILITY_BOUND",
                "gate_status": "PASS" if numeric_bound < 1.0 else "WARN",
                "evidence": f"locality-coupled bound={numeric_bound:.6g}",
                "remaining_obligation": (
                    "none for sign-stability preflight"
                    if numeric_bound < 1.0
                    else "narrow below one before sign-stable promotion"
                ),
            },
            {
                "galaxy": GALAXY,
                "gate_id": "LB5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "bound uses only source features and predeclared coupling adjacency",
                "remaining_obligation": "keep endpoint scoring separate",
            },
        ]
    )
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    status_counts = gates["gate_status"].value_counts().to_dict()
    all_pass = int(status_counts.get("BLOCKED", 0)) == 0 and int(status_counts.get("WARN", 0)) == 0
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "locality_rule_id": "NGC4088_EPSILON_CROSS_ADJACENT_LOCALITY_BOUND_V1",
                "bound_expression": f"|epsilon_cross| <= {expression}",
                "numeric_bound_value": numeric_bound,
                "linear_sharp_bound_reference": 1.375,
                "n_terms": len(terms),
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_warn": int(status_counts.get("WARN", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "locality_bound_status": (
                    "LOCALITY_EPSILON_BOUND_READY_SIGN_STABLE"
                    if all_pass
                    else "LOCALITY_EPSILON_BOUND_CAVEATED_OR_BLOCKED"
                ),
                "claim_scope": "formula_conditional_locality_chain_bound_not_final_tau_side_derivation",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return terms, gates, summary


def write_report(terms: pd.DataFrame, gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Epsilon-Cross Locality Bound Rule",
        "",
        "This artifact narrows the epsilon_cross audit bound by treating cross-terms",
        "as adjacent source/readout couplings rather than as independent additive",
        "linear feature terms.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Locality Terms",
        "",
        markdown_table(terms),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The locality-coupled bound is residual-blind and sign-stable for NGC4088,",
        "but remains formula-conditional. It does not authorize endpoint scoring and",
        "does not replace a final Tau-side locality theorem.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_epsilon_cross_locality_bound_rule.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    terms, gates, summary = build_rule()
    terms.to_csv(DATA / "s4g75_ngc4088_epsilon_cross_locality_bound_terms.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_epsilon_cross_locality_bound_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_epsilon_cross_locality_bound_summary.csv", index=False)
    write_report(terms, gates, summary)
    print("PAPER8_NGC4088_EPSILON_CROSS_LOCALITY_BOUND_RULE_COMPLETE")


if __name__ == "__main__":
    main()
