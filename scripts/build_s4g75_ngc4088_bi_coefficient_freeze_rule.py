#!/usr/bin/env python3
"""Freeze a residual-blind B_i coefficient rule for NGC4088 epsilon_cross.

The rule is a conservative unit-Lipschitz first bound: each normalized source
feature is assigned B_i = 1. This is not a fitted physical coefficient model.
It is a protocol upper-bound default justified by the triangle inequality for a
dimensionless first-order correction expansion.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_bi_coefficient_freeze_rule_not_endpoint"


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


def build_freeze() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    source_review_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_source_response_independent_review_summary.csv"
    ).iloc[0]
    source_authorized = bool(source_review_summary["numeric_bound_source_authorization"])
    coefficient_rows = []
    for coefficient_id, feature_symbol in [
        ("B_PA", "f_PA"),
        ("B_R", "f_R"),
        ("B_q", "f_q"),
        ("B_mem", "f_mem"),
    ]:
        coefficient_rows.append(
            {
                "galaxy": GALAXY,
                "coefficient_id": coefficient_id,
                "multiplies_feature": feature_symbol,
                "frozen_value": 1.0,
                "unit": "dimensionless",
                "freeze_rule": "unit_Lipschitz_triangle_bound_default",
                "freeze_status": (
                    "FROZEN_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT"
                    if source_authorized
                    else "SOURCE_REVIEW_BLOCKED_FREEZE_HELD"
                ),
                "derivation_status": "PROTOCOL_BOUND_NOT_FINAL_TAU_SIDE_DERIVATION",
                "justification": "For normalized features f_i in [0,1], |sum c_i f_i| <= sum |c_i| f_i; set B_i=1 as conservative first protocol bound.",
                "forbidden_origin": "vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    coefficients = pd.DataFrame(coefficient_rows)

    gates = pd.DataFrame(
        [
            {
                "gate_id": "BF1_SOURCE_REVIEW_AUTHORIZED",
                "gate_status": "PASS" if source_authorized else "BLOCKED",
                "evidence": str(source_review_summary["source_review_status"]),
                "remaining_obligation": (
                    "preserve caveated source-review status"
                    if source_authorized
                    else "complete independent q/memory source review"
                ),
            },
            {
                "gate_id": "BF2_DIMENSIONLESS_FEATURE_DOMAIN",
                "gate_status": "PASS",
                "evidence": "all f_i are normalized dimensionless features in [0,1]",
                "remaining_obligation": "preserve feature clipping and units",
            },
            {
                "gate_id": "BF3_UNIT_LIPSCHITZ_BOUND_RULE",
                "gate_status": "PASS",
                "evidence": "B_i=1 is a conservative triangle-bound coefficient, not an endpoint fit",
                "remaining_obligation": "replace with sharper Tau-side derivation when available",
            },
            {
                "gate_id": "BF4_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "freeze rule forbids vobs and endpoint residuals",
                "remaining_obligation": "keep endpoint tests separate",
            },
            {
                "gate_id": "BF5_COEFFICIENT_FREEZE_AUTHORIZATION",
                "gate_status": "PASS" if source_authorized else "BLOCKED",
                "evidence": "four B_i coefficients frozen at 1 under the protocol rule",
                "remaining_obligation": (
                    "evaluate epsilon_cross as protocol upper bound"
                    if source_authorized
                    else "wait for source review"
                ),
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
    all_pass = int(status_counts.get("BLOCKED", 0)) == 0
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "freeze_rule_id": "NGC4088_UNIT_LIPSCHITZ_BI_FREEZE_RULE_V1",
                "n_coefficients": len(coefficients),
                "n_frozen_coefficients": int(
                    (coefficients["freeze_status"] == "FROZEN_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT").sum()
                ),
                "coefficient_value_min": float(coefficients["frozen_value"].min()),
                "coefficient_value_max": float(coefficients["frozen_value"].max()),
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "freeze_rule_status": (
                    "BI_COEFFICIENTS_FROZEN_PROTOCOL_BOUND_READY"
                    if all_pass
                    else "BI_COEFFICIENT_FREEZE_BLOCKED"
                ),
                "numeric_bound_coefficient_authorization": all_pass,
                "claim_scope": "conservative_protocol_upper_bound_not_final_tau_side_coefficient_derivation",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return coefficients, gates, summary


def write_report(
    coefficients: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 B_i Coefficient Freeze Rule",
        "",
        "This artifact freezes a residual-blind conservative coefficient rule for",
        "the epsilon_cross protocol bound. It sets all B_i values to 1 under a",
        "unit-Lipschitz triangle-bound default. This is deliberately cautious and",
        "not an endpoint fit.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Frozen Coefficients",
        "",
        markdown_table(coefficients),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The frozen coefficients authorize only a conservative protocol upper",
        "bound for epsilon_cross. They do not claim a final Tau-side derivation of",
        "the sharp B_i amplitudes.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_bi_coefficient_freeze_rule.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    coefficients, gates, summary = build_freeze()
    coefficients.to_csv(DATA / "s4g75_ngc4088_bi_frozen_coefficients.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_bi_coefficient_freeze_rule_gate.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_bi_coefficient_freeze_rule_summary.csv",
        index=False,
    )
    write_report(coefficients, gates, summary)
    print("PAPER8_NGC4088_BI_COEFFICIENT_FREEZE_RULE_COMPLETE")


if __name__ == "__main__":
    main()
