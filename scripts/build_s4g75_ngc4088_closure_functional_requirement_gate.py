#!/usr/bin/env python3
"""Build the NGC4088 closure-functional requirement gate.

This gate refines the blocked requirement that a Tau-side closure/readout
functional should derive the selected scale carrier.  It records the minimum
functional ingredients and Euler/closure implications needed before the
NGC4088 warp/asymmetry readout can be promoted beyond a conditional formula.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint"


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
    asymptotic_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_asymptotic_carrier_dominance_summary.csv"
    ).iloc[0]
    derivation_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_derivation_summary.csv"
    ).iloc[0]

    ansatz = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "functional_id": "NGC4088_WARP_ASYMMETRY_CLOSURE_FUNCTIONAL_REQUIREMENT",
                "required_form": (
                    "J_tau[lambda_w] = closure_cost(lambda_w; Q_D, Q_N, x_w, "
                    "C_warp) + asymptotic_carrier_penalty(lambda_w; Vflat^2) "
                    "+ autonomy_penalty(lambda_w; external_comparators)"
                ),
                "solved_scale_if_derived": "lambda_w = sigma_warp q_warp x_w Vflat^2",
                "readout_formula_if_derived": (
                    "delta_v2_warp(R;p) = lambda_w C_warp(R/R_HI; x_w, p)"
                ),
                "current_status": "FUNCTIONAL_REQUIREMENT_NOT_CONSTRUCTED",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "F1_SOURCE_BASIS_AVAILABLE",
                "gate_status": "PASS",
                "evidence": "C_warp(R/R_HI; x_w, p) exists as a residual-blind filled source basis",
                "remaining_obligation": "none at basis-availability level",
            },
            {
                "gate_id": "F2_DIMENSIONFUL_CARRIER_CANDIDATE_AVAILABLE",
                "gate_status": "PASS",
                "evidence": "x_w * Vflat^2 is selected by the conditional scale-selection gate",
                "remaining_obligation": "derive the carrier rather than selecting it by protocol",
            },
            {
                "gate_id": "F3_FUNCTIONAL_VARIABLE_DECLARED",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "lambda_w can parameterize the warp/asymmetry delta-v-squared amplitude",
                "remaining_obligation": "derive lambda_w as a Tau-side readout variable",
            },
            {
                "gate_id": "F4_CLOSURE_COST_DEFINED",
                "gate_status": "BLOCKED",
                "evidence": "no explicit Tau-side closure_cost has been constructed",
                "remaining_obligation": "define a residual-blind closure/readout cost from Tau-side morphology and slice mismatch",
            },
            {
                "gate_id": "F5_EULER_CONDITION_DERIVED",
                "gate_status": "BLOCKED",
                "evidence": "no stationarity equation currently yields lambda_w = x_w * Vflat^2",
                "remaining_obligation": "derive dJ_tau/dlambda_w = 0 and solve it without endpoint residuals",
            },
            {
                "gate_id": "F6_ASYMPTOTIC_CARRIER_TERM_DERIVED",
                "gate_status": "BLOCKED",
                "evidence": asymptotic_summary["dominance_status"],
                "remaining_obligation": "derive why the asymptotic term is Vflat^2 rather than another source-native carrier",
            },
            {
                "gate_id": "F7_COMPARATOR_AUTONOMY_DERIVED",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "selection protocol excludes external TPG-like comparators",
                "remaining_obligation": "derive comparator autonomy as a functional constraint",
            },
            {
                "gate_id": "F8_POPULATION_TRANSFER_REQUIRED",
                "gate_status": "BLOCKED",
                "evidence": derivation_summary["derivation_status"],
                "remaining_obligation": "apply the same functional requirement gate to a predeclared warp/asymmetry sample",
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
                "functional_id": ansatz["functional_id"].iloc[0],
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "functional_status": "CLOSURE_FUNCTIONAL_REQUIREMENT_SPECIFIED_NOT_DERIVED",
                "law_status": "NO_TAU_SIDE_EULER_CLOSURE_DERIVATION_YET",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return ansatz, gates, summary


def write_report(ansatz: pd.DataFrame, gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Closure-Functional Requirement Gate",
        "",
        "This gate specifies what a Tau-side closure/readout functional would",
        "need to prove before the selected NGC4088 warp/asymmetry normalization",
        "can be promoted from conditional formula to derived readout law.",
        "",
        "## Verdict",
        "",
        "The source basis and dimensionful carrier candidate are available, but",
        "the functional itself is not constructed. The Euler/closure condition",
        "that would solve for `lambda_w = x_w Vflat^2` remains blocked.",
        "",
        "## Functional Requirement",
        "",
        markdown_table(ansatz),
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
        "This is a derivation-requirement ledger, not a derivation. It preserves",
        "the negative result that no Tau-side closure functional currently",
        "generates the selected scale law.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_closure_functional_requirement_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    ansatz, gates, summary = build_gate()
    ansatz.to_csv(DATA / "s4g75_ngc4088_closure_functional_requirement.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_closure_functional_requirement_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_closure_functional_requirement_summary.csv", index=False)
    write_report(ansatz, gates, summary)
    print("PAPER8_NGC4088_CLOSURE_FUNCTIONAL_REQUIREMENT_GATE_COMPLETE")


if __name__ == "__main__":
    main()
