#!/usr/bin/env python3
"""Audit NGC4088 readout sensitivity to the epsilon_cross protocol bound.

This script does not score against observed velocities. It propagates the
residual-blind epsilon_cross upper bound through the generated source-native
candidate readout profile to estimate how loose the cross-term bound remains.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint"


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


def classify_bound(bound: float) -> str:
    if bound < 0.25:
        return "CROSS_TERM_BOUND_TIGHT"
    if bound < 0.75:
        return "CROSS_TERM_BOUND_MODERATE"
    if bound < 1.0:
        return "CROSS_TERM_BOUND_STILL_MATERIAL"
    return "CROSS_TERM_BOUND_LOOSE_SIGN_AMBIGUOUS"


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    expression = pd.read_csv(DATA / "s4g75_ngc4088_epsilon_cross_bound_expression.csv").iloc[0]
    locality_path = DATA / "s4g75_ngc4088_epsilon_cross_locality_bound_summary.csv"
    locality = pd.read_csv(locality_path).iloc[0] if locality_path.exists() else None
    terms = pd.read_csv(DATA / "s4g75_ngc4088_epsilon_cross_bound_terms.csv")
    profile = pd.read_csv(DATA / "s4g75_ngc4088_readout_preflight_profile.csv")
    linear_bound = float(expression["numeric_bound_value"])
    if (
        locality is not None
        and str(locality["locality_bound_status"])
        == "LOCALITY_EPSILON_BOUND_READY_SIGN_STABLE"
    ):
        bound = float(locality["numeric_bound_value"])
        active_bound_expression = str(locality["bound_expression"])
        active_bound_source = "adjacent_locality_chain_bound"
    else:
        bound = linear_bound
        active_bound_expression = str(expression["bound_expression"])
        active_bound_source = "linear_sharp_bound"

    branch_columns = [
        column
        for column in profile.columns
        if column.startswith("delta_v2_warp_candidate_")
    ]
    scenarios = [-bound, -0.5 * bound, 0.0, 0.5 * bound, bound]
    rows = []
    for branch_column in branch_columns:
        branch_id = branch_column.replace("delta_v2_warp_candidate_", "")
        for epsilon_cross in scenarios:
            corrected_delta = profile[branch_column].astype(float) * (1.0 + epsilon_cross)
            cross_increment = profile[branch_column].astype(float) * epsilon_cross
            rows.append(
                {
                    "galaxy": GALAXY,
                    "branch_id": branch_id,
                    "epsilon_cross_scenario": epsilon_cross,
                    "lambda_multiplier": 1.0 + epsilon_cross,
                    "min_corrected_delta_v2": float(corrected_delta.min()),
                    "max_corrected_delta_v2": float(corrected_delta.max()),
                    "max_abs_cross_increment_v2": float(cross_increment.abs().max()),
                    "max_leading_delta_v2": float(profile[branch_column].astype(float).max()),
                    "sign_flip_possible": bool((1.0 + epsilon_cross) < 0.0),
                    "uses_vobs_or_residual": False,
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    scenario_audit = pd.DataFrame(rows)

    term_sum = float(terms["term_numeric_value"].sum())
    max_leading_delta = float(
        max(profile[column].astype(float).max() for column in branch_columns)
    )
    max_cross_increment = max_leading_delta * bound
    sensitivity_status = classify_bound(bound)
    gates = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "gate_id": "RSA1_NUMERIC_BOUND_AVAILABLE",
                "gate_status": "PASS" if pd.notna(bound) else "BLOCKED",
                "evidence": f"active epsilon_cross bound={bound:.6g}; linear term sum={term_sum:.6g}",
                "remaining_obligation": "none" if pd.notna(bound) else "compute numeric bound first",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "RSA2_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "audit propagates generated source-native profiles and does not compute residual scores",
                "remaining_obligation": "keep observed velocity columns contextual only",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "RSA3_BOUND_TIGHTNESS",
                "gate_status": "PASS" if bound < 1.0 else "WARN",
                "evidence": f"|epsilon_cross| <= {bound:.6g} gives max |cross increment| <= {max_cross_increment:.6g} km2/s2",
                "remaining_obligation": (
                    "derive tighter Tau-side/locality/sign constraints before promotion"
                    if bound >= 1.0
                    else "stress-test under source uncertainty"
                ),
            },
            {
                "galaxy": GALAXY,
                "gate_id": "RSA4_SIGN_STABILITY",
                "gate_status": "PASS" if bound < 1.0 else "WARN",
                "evidence": "negative epsilon scenario can invert the leading correction if bound exceeds one",
                "remaining_obligation": (
                    "derive sign or monotonicity constraints"
                    if bound >= 1.0
                    else "preserve sign-stable bound"
                ),
            },
        ]
    )
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    status_counts = gates["gate_status"].value_counts().to_dict()
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "audit_id": "NGC4088_EPSILON_CROSS_READOUT_SENSITIVITY_AUDIT",
                "numeric_epsilon_cross_bound": bound,
                "linear_sharp_bound_reference": linear_bound,
                "active_bound_expression": active_bound_expression,
                "active_bound_source": active_bound_source,
                "n_terms": len(terms),
                "n_branches": len(branch_columns),
                "n_scenarios": len(scenarios),
                "max_leading_delta_v2": max_leading_delta,
                "max_abs_cross_increment_v2": max_cross_increment,
                "sensitivity_status": sensitivity_status,
                "promotion_implication": (
                    "cross-term bound is sharper than unit baseline but still too loose for endpoint promotion"
                    if bound >= 1.0
                    else "cross-term bound may be usable after source-uncertainty stress tests"
                ),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_warn": int(status_counts.get("WARN", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return scenario_audit, gates, summary


def write_report(
    scenario_audit: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Epsilon-Cross Readout Sensitivity Audit",
        "",
        "This audit propagates the residual-blind epsilon_cross protocol bound",
        "through the generated NGC4088 readout profile. It does not compare to",
        "observed rotation residuals and does not authorize endpoint scoring.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Scenario Audit",
        "",
        markdown_table(scenario_audit),
        "",
        "## Claim Boundary",
        "",
        "The audit estimates cross-term readout sensitivity only. A loose bound is",
        "a preserved negative/preparatory result, not a failure of the whole Tau",
        "Core morphology program and not endpoint evidence.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    scenario_audit, gates, summary = build_audit()
    scenario_audit.to_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_readout_sensitivity_scenarios.csv",
        index=False,
    )
    gates.to_csv(DATA / "s4g75_ngc4088_epsilon_cross_readout_sensitivity_gate.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_readout_sensitivity_summary.csv",
        index=False,
    )
    write_report(scenario_audit, gates, summary)
    print("PAPER8_NGC4088_EPSILON_CROSS_READOUT_SENSITIVITY_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
