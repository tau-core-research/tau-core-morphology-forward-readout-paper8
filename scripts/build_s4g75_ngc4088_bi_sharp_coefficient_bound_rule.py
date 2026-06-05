#!/usr/bin/env python3
"""Build a sharper residual-blind B_i coefficient bound for NGC4088.

The existing B_i=1 rule is a conservative unit-Lipschitz triangle bound. This
artifact adds a stricter formula-conditional rule: if epsilon_cross is treated
as a normalized second-order remainder and the residual-blind source-space
Hessian norm is capped by one, each first-order feature contribution receives a
1/2 Taylor-remainder coefficient. This is still not a final Tau-side sharp
amplitude derivation.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_bi_sharp_coefficient_bound_rule_not_endpoint"


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
    source_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_source_response_independent_review_summary.csv"
    ).iloc[0]
    unit_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_bi_coefficient_freeze_rule_summary.csv"
    ).iloc[0]
    source_ready = bool(source_summary["numeric_bound_source_authorization"])
    unit_ready = bool(unit_summary["numeric_bound_coefficient_authorization"])
    active = source_ready and unit_ready

    rows = []
    for coefficient_id, feature_symbol in [
        ("B_PA", "f_PA"),
        ("B_R", "f_R"),
        ("B_q", "f_q"),
        ("B_mem", "f_mem"),
    ]:
        rows.append(
            {
                "galaxy": GALAXY,
                "coefficient_id": coefficient_id,
                "multiplies_feature": feature_symbol,
                "sharp_value": 0.5,
                "unit": "dimensionless",
                "sharp_rule": "second_order_remainder_half_bound",
                "sharp_status": (
                    "SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT"
                    if active
                    else "SHARPENED_RULE_HELD_UNTIL_SOURCE_AND_UNIT_BOUND_READY"
                ),
                "derivation_status": "FORMULA_CONDITIONAL_NOT_FINAL_TAU_SIDE_AMPLITUDE_DERIVATION",
                "justification": "For a normalized second-order remainder with source-space Hessian cap <= 1, the Taylor remainder contributes a factor 1/2 before the normalized feature magnitude.",
                "forbidden_origin": "vobs; endpoint residuals; endpoint-selected family; post-hoc endpoint fit",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    coefficients = pd.DataFrame(rows)

    gates = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "gate_id": "SB1_SOURCE_REVIEW_READY",
                "gate_status": "PASS" if source_ready else "BLOCKED",
                "evidence": str(source_summary["source_review_status"]),
                "remaining_obligation": "complete source review" if not source_ready else "none",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "SB2_CONSERVATIVE_BASELINE_EXISTS",
                "gate_status": "PASS" if unit_ready else "BLOCKED",
                "evidence": str(unit_summary["freeze_rule_status"]),
                "remaining_obligation": "keep B_i=1 baseline available for comparison",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "SB3_SECOND_ORDER_REMAINDER_ASSUMPTION_DECLARED",
                "gate_status": "PASS",
                "evidence": "B_i=0.5 is conditional on the normalized second-order remainder/Hessian-cap interpretation",
                "remaining_obligation": "derive the Hessian cap from Tau-side geometry before calling this final",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "SB4_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "sharp rule uses no vobs, residuals, or endpoint scores",
                "remaining_obligation": "keep endpoint tests separate",
            },
        ]
    )
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    status_counts = gates["gate_status"].value_counts().to_dict()
    all_pass = int(status_counts.get("BLOCKED", 0)) == 0
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "sharp_rule_id": "NGC4088_SECOND_ORDER_REMAINDER_BI_HALF_BOUND_V1",
                "n_coefficients": len(coefficients),
                "n_sharp_coefficients": int(
                    (coefficients["sharp_status"] == "SHARPENED_RESIDUAL_BLIND_PROTOCOL_COEFFICIENT").sum()
                ),
                "coefficient_value_min": float(coefficients["sharp_value"].min()),
                "coefficient_value_max": float(coefficients["sharp_value"].max()),
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "sharp_rule_status": (
                    "BI_COEFFICIENTS_SHARPENED_PROTOCOL_BOUND_READY"
                    if all_pass
                    else "BI_SHARPENED_RULE_BLOCKED"
                ),
                "numeric_bound_coefficient_authorization": all_pass,
                "claim_scope": "formula_conditional_second_order_protocol_bound_not_final_tau_side_derivation",
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
        "# NGC4088 Sharpened B_i Coefficient Bound Rule",
        "",
        "This artifact adds a residual-blind sharper B_i rule on top of the",
        "conservative B_i=1 baseline. The active coefficient is B_i=0.5 only under",
        "the declared second-order Taylor-remainder interpretation with normalized",
        "source-space Hessian cap <= 1.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Sharpened Coefficients",
        "",
        markdown_table(coefficients),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The sharpened coefficients are formula-conditional protocol coefficients.",
        "They are residual-blind and stricter than the unit bound, but they are not",
        "yet a final Tau-side derivation of the sharp cross-term amplitudes.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_bi_sharp_coefficient_bound_rule.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    coefficients, gates, summary = build_rule()
    coefficients.to_csv(DATA / "s4g75_ngc4088_bi_sharp_coefficients.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_bi_sharp_coefficient_bound_rule_gate.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_bi_sharp_coefficient_bound_rule_summary.csv",
        index=False,
    )
    write_report(coefficients, gates, summary)
    print("PAPER8_NGC4088_BI_SHARP_COEFFICIENT_BOUND_RULE_COMPLETE")


if __name__ == "__main__":
    main()
