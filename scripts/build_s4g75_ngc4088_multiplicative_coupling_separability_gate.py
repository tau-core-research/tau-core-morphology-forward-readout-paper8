#!/usr/bin/env python3
"""Build the NGC4088 multiplicative-coupling separability gate.

This gate turns the product sigma_warp * q_warp * x_w * Vflat^2 into a
conditional separability statement.  It does not prove that the Tau-side
readout is separable; it records the precise assumptions under which the
product form follows from independent orientation, source-strength,
onset-support, and asymptotic-carrier factors.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_multiplicative_coupling_separability_gate_not_endpoint"


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
    factors = pd.read_csv(DATA / "s4g75_ngc4088_target_functional_origin_factors.csv")
    values = dict(zip(factors["factor_id"], factors["factor_value"]))
    target = float(values["MULTIPLICATIVE_COUPLING"])

    theorem = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "theorem_id": "CONDITIONAL_SEPARABLE_SOURCE_READOUT_PRODUCT",
                "statement": (
                    "If the warp/asymmetry readout amplitude separates into "
                    "orientation sign, source strength, onset support fraction, "
                    "and asymptotic carrier factors, then the first-order target "
                    "scale is lambda_w = sigma_warp q_warp x_w Vflat^2."
                ),
                "derived_product_formula": "lambda_w = sigma_warp q_warp x_w Vflat^2",
                "derived_product_value_km2_s2": target,
                "proof_status": "FORMULA_DERIVED_GIVEN_SEPARABILITY_ASSUMPTIONS",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    assumptions = pd.DataFrame(
        [
            {
                "assumption_id": "S1_FACTOR_SEPARABILITY",
                "assumption_status": "ASSUMPTION_NOT_DERIVED",
                "content": "readout amplitude factorizes into independent local source factors",
            },
            {
                "assumption_id": "S2_ORIENTATION_SIGN",
                "assumption_status": "THEORY_CONDITIONAL",
                "content": "sigma_warp supplies the readout orientation/sign",
            },
            {
                "assumption_id": "S3_SOURCE_STRENGTH",
                "assumption_status": "SOURCE_NATIVE_QUALITATIVE_GATE",
                "content": "q_warp supplies source strength; currently q_warp=1 qualitative gate",
            },
            {
                "assumption_id": "S4_ONSET_SUPPORT",
                "assumption_status": "SOURCE_MEASURED_FORMULA_CONDITIONAL",
                "content": "x_w supplies the dimensionless onset/support fraction",
            },
            {
                "assumption_id": "S5_ASYMPTOTIC_CARRIER",
                "assumption_status": "SOURCE_CATALOG_CANDIDATE_NOT_DERIVED",
                "content": "Vflat^2 supplies the dimensionful asymptotic carrier",
            },
            {
                "assumption_id": "S6_NO_CROSS_TERMS_AT_FIRST_ORDER",
                "assumption_status": "ASSUMPTION_NOT_DERIVED",
                "content": "mixed source-source coupling terms are absent or higher-order",
            },
        ]
    )
    assumptions["galaxy"] = GALAXY
    assumptions["claim_boundary"] = CLAIM_BOUNDARY
    assumptions = assumptions[
        ["galaxy", "assumption_id", "assumption_status", "content", "claim_boundary"]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "M1_PRODUCT_ALGEBRA",
                "gate_status": "PASS",
                "evidence": "the factor product reproduces lambda_w = 8324.016 km^2/s^2",
                "remaining_obligation": "none at algebra level",
            },
            {
                "gate_id": "M2_DIMENSIONAL_CONSISTENCY",
                "gate_status": "PASS",
                "evidence": "dimensionless factors times Vflat^2 yield km^2/s^2",
                "remaining_obligation": "none at dimensional level",
            },
            {
                "gate_id": "M3_SEPARABILITY_ASSUMPTION",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "product follows if the local source readout is separable",
                "remaining_obligation": "derive separability from Tau-side slice/readout geometry",
            },
            {
                "gate_id": "M4_SOURCE_FACTOR_GROUNDING",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "q_warp and x_w are source-side factors but q_warp is qualitative and x_w needs independent review",
                "remaining_obligation": "replace qualitative strength and independently review onset",
            },
            {
                "gate_id": "M5_CARRIER_GROUNDING",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "Vflat^2 is a source-catalog carrier candidate",
                "remaining_obligation": "derive asymptotic carrier dominance",
            },
            {
                "gate_id": "M6_NO_CROSS_TERMS",
                "gate_status": "BLOCKED",
                "evidence": "no derivation yet excludes mixed source-source coupling corrections",
                "remaining_obligation": "derive absence/suppression of cross terms",
            },
            {
                "gate_id": "M7_POPULATION_TRANSFER",
                "gate_status": "BLOCKED",
                "evidence": "the separability statement is currently NGC4088-specific",
                "remaining_obligation": "run on a predeclared warp/asymmetry source-rich sample",
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
                "theorem_id": theorem["theorem_id"].iloc[0],
                "lambda_product_km2_s2": target,
                "n_assumptions": len(assumptions),
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "coupling_status": "CONDITIONAL_PRODUCT_DERIVED_IF_SEPARABLE",
                "law_status": "SEPARABILITY_AND_CROSS_TERM_SUPPRESSION_NOT_DERIVED",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return theorem, assumptions, gates, summary


def write_report(
    theorem: pd.DataFrame,
    assumptions: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Multiplicative-Coupling Separability Gate",
        "",
        "This gate records a conditional derivation of the product target. It",
        "shows what follows if the Tau-side source readout is separable, while",
        "preserving the fact that separability and cross-term suppression are not",
        "yet derived.",
        "",
        "## Conditional Theorem",
        "",
        markdown_table(theorem),
        "",
        "## Assumptions",
        "",
        markdown_table(assumptions),
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
        "This is not an endpoint test and not a final law. It upgrades the",
        "multiplicative coupling from arbitrary composition to a conditional",
        "separability result.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_multiplicative_coupling_separability_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    theorem, assumptions, gates, summary = build_gate()
    theorem.to_csv(DATA / "s4g75_ngc4088_multiplicative_coupling_theorem.csv", index=False)
    assumptions.to_csv(
        DATA / "s4g75_ngc4088_multiplicative_coupling_assumptions.csv", index=False
    )
    gates.to_csv(DATA / "s4g75_ngc4088_multiplicative_coupling_separability_gate.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_multiplicative_coupling_separability_summary.csv", index=False
    )
    write_report(theorem, assumptions, gates, summary)
    print("PAPER8_NGC4088_MULTIPLICATIVE_COUPLING_SEPARABILITY_GATE_COMPLETE")


if __name__ == "__main__":
    main()
