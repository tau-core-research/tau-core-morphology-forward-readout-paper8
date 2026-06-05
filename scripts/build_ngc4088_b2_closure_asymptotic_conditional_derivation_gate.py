#!/usr/bin/env python3
"""Build the NGC4088 B2 closure/asymptotic conditional derivation gate.

This gate records the strongest current B2 statement: the NGC4088
normalization formula is algebraically derived from a declared target
closure functional and an asymptotic carrier premise, but the Tau-side origin
of those premises remains open.  It reads no endpoint velocities, residuals,
or scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "ngc4088_b2_closure_asymptotic_conditional_derivation_not_endpoint"


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


def bool_value(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    freeze = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_manifest.csv").iloc[0]
    b2 = pd.read_csv(DATA / "ngc4088_b2_physical_normalization_synthesis_summary.csv").iloc[0]
    closure = pd.read_csv(DATA / "s4g75_ngc4088_closure_functional_requirement_summary.csv").iloc[0]
    source_load = pd.read_csv(DATA / "ngc4088_b2_source_load_closure_functional_summary.csv").iloc[0]
    source_load_origin = pd.read_csv(
        DATA / "ngc4088_b2_source_load_origin_summary.csv"
    ).iloc[0]
    frozen_carrier = pd.read_csv(DATA / "ngc4088_b2_frozen_asymptotic_carrier_summary.csv").iloc[0]
    asymptotic = pd.read_csv(DATA / "s4g75_ngc4088_asymptotic_carrier_dominance_summary.csv").iloc[0]
    euler = pd.read_csv(DATA / "s4g75_ngc4088_minimal_euler_ansatz_summary.csv").iloc[0]
    separability = pd.read_csv(
        DATA / "s4g75_ngc4088_multiplicative_coupling_separability_summary.csv"
    ).iloc[0]
    cross = pd.read_csv(DATA / "s4g75_ngc4088_cross_term_suppression_summary.csv").iloc[0]

    sigma = float(freeze["sigma_warp"])
    q_warp = float(freeze["q_warp"])
    x_w = float(freeze["x_w_formula_freeze"])
    vflat = float(freeze["vflat_km_s"])
    lambda_w = sigma * q_warp * x_w * vflat**2
    manifest_lambda = float(freeze["lambda_w_km2_s2"])
    alignment_pass = abs(lambda_w - manifest_lambda) < 1.0e-6

    theorem = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "theorem_id": "B2_CLOSURE_ASYMPTOTIC_CONDITIONAL_DERIVATION",
                "conditional_statement": (
                    "If J_tau[lambda_w] has the target-stationary closure form with "
                    "positive stiffness, Vflat^2 is the Tau-side asymptotic carrier, "
                    "and the source factors sigma_warp, q_warp, and x_w enter "
                    "separably with suppressed cross terms, then the stationary "
                    "normalization is lambda_w = sigma_warp q_warp x_w Vflat^2."
                ),
                "derived_formula": "lambda_w = sigma_warp q_warp x_w Vflat^2",
                "numeric_lambda_w_km2_s2": lambda_w,
                "formula_freeze_manifest_lambda_w_km2_s2": manifest_lambda,
                "formula_freeze_alignment_pass": alignment_pass,
                "mathematical_status": "ALGEBRAICALLY_DERIVED_GIVEN_TARGET_FUNCTIONAL",
                "tau_side_law_status": "FORMULA_CONDITIONAL_PREMISES_OPEN",
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    conditions = pd.DataFrame(
        [
            {
                "condition_id": "B2D1_SOURCE_FREEZE_ALIGNMENT",
                "condition_type": "derived_status_input",
                "current_status": "PASS" if alignment_pass else "BLOCKED",
                "what_is_established": (
                    "the conditional formula uses the accepted formula-freeze x_w "
                    "and reproduces the frozen lambda_w"
                ),
                "what_remains_open": "none at formula-freeze alignment level",
                "source_status": str(freeze["formula_id"]),
            },
            {
                "condition_id": "B2D2_DIMENSIONAL_AND_LIMIT_CHECK",
                "condition_type": "derived_status_input",
                "current_status": "PASS",
                "what_is_established": (
                    "lambda_w has velocity-squared units; C_warp is dimensionless; "
                    "zero-source and inactive-window limits recover the carrier"
                ),
                "what_remains_open": "none at dimensional or limit-audit level",
                "source_status": str(freeze["dimension_check"]),
            },
            {
                "condition_id": "B2D3_EULER_STATIONARITY_GIVEN_TARGET",
                "condition_type": "conditional_derivation",
                "current_status": "FORMULA_CONDITIONAL_PASS",
                "what_is_established": (
                    "given a quadratic target functional, dJ/dlambda_w=0 solves "
                    "to lambda_w = sigma_warp q_warp x_w Vflat^2"
                ),
                "what_remains_open": "derive the target functional itself from Tau-side closure/readout data",
                "source_status": str(euler["euler_status"]),
            },
            {
                "condition_id": "B2D4_CLOSURE_FUNCTIONAL_ORIGIN",
                "condition_type": "law_level_premise",
                "current_status": "CONDITIONAL_FUNCTIONAL_CONSTRUCTED",
                "what_is_established": (
                    "an explicit source-load norm-square J_load[lambda_w] yields the "
                    "frozen normalization by Euler stationarity; the frozen source-load "
                    "factor ladder is partially grounded"
                ),
                "what_remains_open": (
                    "derive the source-load origin, closure weight, and uniqueness "
                    "from Tau-side morphology/readout data"
                ),
                "source_status": (
                    f"{closure['functional_status']}; "
                    f"{source_load['closure_functional_status']}; "
                    f"{source_load_origin['source_load_origin_status']}"
                ),
            },
            {
                "condition_id": "B2D5_ASYMPTOTIC_CARRIER_ORIGIN",
                "condition_type": "law_level_premise",
                "current_status": "CONDITIONAL_CARRIER_THEOREM",
                "what_is_established": (
                    "Vflat^2 is conditionally justified as the frozen protocol "
                    "carrier under residual-blind source-onset asymptotic criteria"
                ),
                "what_remains_open": (
                    "promote the frozen carrier theorem to final Tau-side law through "
                    "alternative-carrier exclusion and population transfer"
                ),
                "source_status": (
                    f"{asymptotic['dominance_status']}; "
                    f"{frozen_carrier['frozen_carrier_theorem_status']}"
                ),
            },
            {
                "condition_id": "B2D6_SEPARABILITY_AND_CROSS_TERM_BOUND",
                "condition_type": "law_level_premise",
                "current_status": "PARTIAL_SOURCE_BOUND",
                "what_is_established": (
                    "conditional product form is audited and cross-term handling has a "
                    "partial source-bound/sharp-coefficient protocol"
                ),
                "what_remains_open": (
                    "complete q/memory source observables, prove suppression, or carry "
                    "epsilon_cross as explicit source-side uncertainty"
                ),
                "source_status": (
                    f"{separability['coupling_status']}; {cross['cross_term_status']}; "
                    f"{source_load_origin['source_load_origin_status']}"
                ),
            },
            {
                "condition_id": "B2D7_POPULATION_TRANSFER",
                "condition_type": "claim_scope_premise",
                "current_status": "OPEN_FOR_CLAIMS",
                "what_is_established": "single-galaxy conditional theorem is now explicit",
                "what_remains_open": "repeat the gate on a predeclared warp/history source-rich sample",
                "source_status": str(b2["b2_synthesis_status"]),
            },
        ]
    )
    conditions["endpoint_scores_allowed"] = False
    conditions["uses_vobs_or_residual"] = False
    conditions["claim_boundary"] = CLAIM_BOUNDARY

    n_pass = int(
        conditions["current_status"]
        .isin(
            [
                "PASS",
                "FORMULA_CONDITIONAL_PASS",
                "CONDITIONAL_FUNCTIONAL_CONSTRUCTED",
                "CONDITIONAL_CARRIER_THEOREM",
            ]
        )
        .sum()
    )
    n_open_law = int(
        (
            conditions["condition_type"].eq("law_level_premise")
            & conditions["current_status"].isin(
                [
                    "OPEN",
                    "CONDITIONAL_FUNCTIONAL_CONSTRUCTED",
                    "CONDITIONAL_CARRIER_THEOREM",
                    "PARTIAL_SOURCE_BOUND",
                ]
            )
        ).sum()
    )
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "b2_conditional_derivation_status": (
                    "B2_CONDITIONAL_THEOREM_ALIGNED_TO_FREEZE_MANIFEST_LAW_PREMISES_OPEN"
                ),
                "numeric_lambda_w_km2_s2": lambda_w,
                "formula_freeze_alignment_pass": alignment_pass,
                "n_conditions": len(conditions),
                "n_pass_or_formula_conditional_pass": n_pass,
                "n_open_law_premises": n_open_law,
                "law_level_closed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "derive the Tau-side source-load origin, upgrade the frozen "
                    "Vflat^2 carrier theorem to a final carrier law/population "
                    "transfer result, and prove the cross-term suppression bound"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    theorem.to_csv(DATA / "ngc4088_b2_closure_asymptotic_conditional_theorem.csv", index=False)
    conditions.to_csv(DATA / "ngc4088_b2_closure_asymptotic_conditions.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b2_closure_asymptotic_summary.csv", index=False)

    report = [
        "# NGC4088 B2 Closure/Asymptotic Conditional Derivation Gate",
        "",
        "This gate records the strongest current B2 result without overclaiming.",
        "It proves the normalization only conditionally: if the Tau-side closure",
        "functional has the specified target-stationary form and `Vflat^2` is the",
        "derived asymptotic carrier, then the stationary normalization is",
        "`lambda_w = sigma_warp q_warp x_w Vflat^2`.",
        "",
        "It does not use endpoint velocities, residuals, or score ranks.",
        "",
        "## Conditional Theorem",
        "",
        markdown_table(theorem),
        "",
        "## Conditions",
        "",
        markdown_table(conditions),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "B2 is now stronger than an informal ansatz: the formula-freeze-aligned",
        "normalization is algebraically derived given the target functional and",
        "carrier premises.  It is not yet a final Tau-side law because the",
        "closure functional, the forced `Vflat^2` carrier theorem, and the",
        "separability/cross-term proof remain open.",
        "",
    ]
    (REPORTS / "ngc4088_b2_closure_asymptotic_conditional_derivation_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
