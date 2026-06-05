#!/usr/bin/env python3
"""Build the NGC4088 target-functional origin gate.

The minimal Euler ansatz proves that the selected scale follows from a
quadratic target functional.  This gate decomposes the target into source-side
factors and records which parts are already source grounded versus which parts
remain Tau-side derivation obligations.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_target_functional_origin_gate_not_endpoint"


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
    constants = pd.read_csv(DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_constants.csv")
    euler_summary = pd.read_csv(DATA / "s4g75_ngc4088_minimal_euler_ansatz_summary.csv").iloc[0]
    values = dict(zip(constants["constant_name"], constants["constant_value"]))
    target = float(euler_summary["solved_lambda_km2_s2"])

    factors = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "factor_id": "SIGMA_WARP_ORIENTATION",
                "factor_symbol": "sigma_warp",
                "factor_value": float(values["sigma_warp_orientation"]),
                "unit": "dimensionless",
                "origin_status": "THEORY_CONDITIONAL_ORIENTATION_SIGN",
                "origin_evidence": "positive warp/asymmetry orientation lane",
                "remaining_obligation": "derive orientation sign from Tau-side readout geometry",
            },
            {
                "galaxy": GALAXY,
                "factor_id": "Q_WARP_SOURCE_STRENGTH",
                "factor_symbol": "q_warp",
                "factor_value": float(values["q_warp"]),
                "unit": "dimensionless",
                "origin_status": "SOURCE_NATIVE_QUALITATIVE_GATE",
                "origin_evidence": "qualitative warp/asymmetry source strength imported before endpoint scoring",
                "remaining_obligation": "replace qualitative q_warp=1 by source-measured amplitude in population tests",
            },
            {
                "galaxy": GALAXY,
                "factor_id": "X_WARP_ONSET",
                "factor_symbol": "x_w",
                "factor_value": float(values["c_warp_candidate"]),
                "unit": "dimensionless",
                "origin_status": "SOURCE_MEASURED_ONSET_FRACTION",
                "origin_evidence": "x_w = R_warp/R_HI from residual-blind channel-map digitization protocol",
                "remaining_obligation": "independent digitization review and population transfer",
            },
            {
                "galaxy": GALAXY,
                "factor_id": "VFLAT2_CARRIER",
                "factor_symbol": "Vflat^2",
                "factor_value": float(values["velocity_scale_candidate"]),
                "unit": "km2_s2",
                "origin_status": "SOURCE_CATALOG_SCALE_CANDIDATE_NOT_DERIVED_CARRIER",
                "origin_evidence": "catalog flat-speed-squared scale selected by conditional carrier rule",
                "remaining_obligation": "derive asymptotic carrier dominance from Tau-side closure/readout functional",
            },
            {
                "galaxy": GALAXY,
                "factor_id": "MULTIPLICATIVE_COUPLING",
                "factor_symbol": "sigma_warp * q_warp * x_w * Vflat^2",
                "factor_value": target,
                "unit": "km2_s2",
                "origin_status": "TARGET_COMPOSITE_FORMULA_CONDITIONAL",
                "origin_evidence": "composite target is dimensionally valid and Euler-solvable",
                "remaining_obligation": "derive multiplicative coupling rather than composing source factors by ansatz",
            },
            {
                "galaxy": GALAXY,
                "factor_id": "QUADRATIC_TARGET_PENALTY",
                "factor_symbol": "(lambda_w - target)^2",
                "factor_value": 1.0,
                "unit": "formal",
                "origin_status": "TARGET_PENALTY_NOT_TAU_SIDE_DERIVED",
                "origin_evidence": "minimal convex penalty yields explicit stationarity",
                "remaining_obligation": "derive penalty form from closure/readout geometry",
            },
        ]
    )
    factors["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "T1_SOURCE_FACTORS_AVAILABLE",
                "gate_status": "PASS",
                "evidence": "sigma_warp, q_warp, x_w, and Vflat^2 are present before endpoint scoring",
                "remaining_obligation": "none at availability level",
            },
            {
                "gate_id": "T2_DIMENSIONAL_PRODUCT_VALID",
                "gate_status": "PASS",
                "evidence": "sigma_warp q_warp x_w Vflat^2 has km^2/s^2 units",
                "remaining_obligation": "none at dimensional level",
            },
            {
                "gate_id": "T3_ONSET_FACTOR_SOURCE_GROUNDED",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "x_w is measured by a residual-blind protocol but still needs independent review",
                "remaining_obligation": "complete independent digitization review",
            },
            {
                "gate_id": "T4_ASYMPTOTIC_CARRIER_SOURCE_GROUNDED",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "Vflat^2 is source/catalog grounded but not derived as a Tau-side carrier",
                "remaining_obligation": "derive asymptotic carrier dominance",
            },
            {
                "gate_id": "T5_MULTIPLICATIVE_COUPLING_DERIVED",
                "gate_status": "BLOCKED",
                "evidence": "the product form is selected by ansatz, not derived",
                "remaining_obligation": "derive why source strength, onset, orientation, and carrier multiply linearly",
            },
            {
                "gate_id": "T6_QUADRATIC_PENALTY_DERIVED",
                "gate_status": "BLOCKED",
                "evidence": "the quadratic target penalty is minimal and convex but not Tau-side derived",
                "remaining_obligation": "derive penalty geometry or replace with a derived closure cost",
            },
            {
                "gate_id": "T7_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "no observed velocity or residual score is used in target construction",
                "remaining_obligation": "keep endpoint testing separate",
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
                "target_lambda_km2_s2": target,
                "n_factors": len(factors),
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "target_origin_status": "SOURCE_FACTORS_AVAILABLE_COUPLING_NOT_DERIVED",
                "law_status": "TARGET_TERM_NOT_TAU_SIDE_DERIVED",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return factors, gates, summary


def write_report(factors: pd.DataFrame, gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Target-Functional Origin Gate",
        "",
        "This gate decomposes the minimal Euler target into source factors and",
        "records which parts are source grounded versus still ansatz-level.",
        "",
        "## Verdict",
        "",
        "The source factors are available and dimensionally consistent. The",
        "multiplicative coupling and quadratic penalty are not yet Tau-side",
        "derived, so the target functional remains conditional.",
        "",
        "## Target Factors",
        "",
        markdown_table(factors),
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
        "This is not an endpoint test and not a law derivation. It preserves the",
        "negative result that the target term itself still needs a Tau-side",
        "origin.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_target_functional_origin_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    factors, gates, summary = build_gate()
    factors.to_csv(DATA / "s4g75_ngc4088_target_functional_origin_factors.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_target_functional_origin_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_target_functional_origin_summary.csv", index=False)
    write_report(factors, gates, summary)
    print("PAPER8_NGC4088_TARGET_FUNCTIONAL_ORIGIN_GATE_COMPLETE")


if __name__ == "__main__":
    main()
