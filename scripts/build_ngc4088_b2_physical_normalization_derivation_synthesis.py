#!/usr/bin/env python3
"""Synthesize the NGC4088 B2 physical-normalization derivation status.

B2 asks whether the conditional normalization

    lambda_w = sigma_warp q_warp x_w Vflat^2

is a derived Tau-side closure/readout law, rather than only a dimensionally
consistent source-side formula shell.  This synthesis combines the existing
selection, derivation, Euler, target-origin, separability, and cross-term gates.
It does not score rotations and does not promote endpoint use.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_b2_physical_normalization_derivation_synthesis_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    physical = pd.read_csv(DATA / "s4g75_ngc4088_physical_normalization_law_summary.csv").iloc[0]
    freeze_manifest_path = DATA / "ngc4088_warp_history_formula_freeze_manifest.csv"
    freeze_manifest = (
        pd.read_csv(freeze_manifest_path).iloc[0] if freeze_manifest_path.exists() else None
    )
    selection = pd.read_csv(DATA / "s4g75_ngc4088_tau_side_scale_selection_summary.csv").iloc[0]
    derivation = pd.read_csv(DATA / "s4g75_ngc4088_tau_side_scale_derivation_summary.csv").iloc[0]
    closure = pd.read_csv(DATA / "s4g75_ngc4088_closure_functional_requirement_summary.csv").iloc[0]
    asymptotic = pd.read_csv(DATA / "s4g75_ngc4088_asymptotic_carrier_dominance_summary.csv").iloc[0]
    target = pd.read_csv(DATA / "s4g75_ngc4088_target_functional_origin_summary.csv").iloc[0]
    euler = pd.read_csv(DATA / "s4g75_ngc4088_minimal_euler_ansatz_summary.csv").iloc[0]
    separability = pd.read_csv(
        DATA / "s4g75_ngc4088_multiplicative_coupling_separability_summary.csv"
    ).iloc[0]
    cross = pd.read_csv(DATA / "s4g75_ngc4088_cross_term_suppression_summary.csv").iloc[0]

    first_pass_lambda = float(physical["normalization_prefactor_km2_s2"])
    if freeze_manifest is not None:
        x_w = float(freeze_manifest["x_w_formula_freeze"])
        q_warp = float(freeze_manifest["q_warp"])
        sigma_warp = float(freeze_manifest["sigma_warp"])
        vflat = float(freeze_manifest["vflat_km_s"])
        numeric_lambda = sigma_warp * q_warp * x_w * vflat**2
        manifest_lambda = float(freeze_manifest["lambda_w_km2_s2"])
        formula_freeze_alignment_pass = abs(numeric_lambda - manifest_lambda) < 1.0e-6
        normalization_source = "FORMULA_FREEZE_MANIFEST_REVIEW_ACCEPTED_XW"
        source_note = (
            "aligned to the caveated formula-freeze manifest; the earlier physical-normalization "
            "law gate value is retained as superseded first-pass provenance"
        )
    else:
        x_w = float("nan")
        q_warp = float("nan")
        sigma_warp = float("nan")
        vflat = float("nan")
        numeric_lambda = first_pass_lambda
        manifest_lambda = float("nan")
        formula_freeze_alignment_pass = False
        normalization_source = "FIRST_PASS_PHYSICAL_NORMALIZATION_LAW_SUMMARY"
        source_note = "formula-freeze manifest not available; using first-pass conditional value"

    formula = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "candidate_formula": (
                    "delta_v2_warp(R;p) = lambda_w C_warp(R/R_HI; x_w,p)"
                ),
                "lambda_w_conditional": "sigma_warp q_warp x_w Vflat^2",
                "numeric_lambda_w_km2_s2": numeric_lambda,
                "formula_freeze_manifest_lambda_w_km2_s2": manifest_lambda,
                "first_pass_lambda_w_km2_s2": first_pass_lambda,
                "x_w_formula_freeze": x_w,
                "q_warp": q_warp,
                "sigma_warp": sigma_warp,
                "vflat_km_s": vflat,
                "normalization_source": normalization_source,
                "formula_freeze_alignment_pass": formula_freeze_alignment_pass,
                "source_note": source_note,
                "status": "FORMULA_CONDITIONAL_NOT_FINAL_LAW",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    components = pd.DataFrame(
        [
            {
                "component_id": "B2C1_DIMENSIONAL_AND_RESIDUAL_BLIND_FORMULA",
                "component_status": str(physical["law_status"]),
                "what_is_established": (
                    "formula is executable, dimensionally consistent, generated without endpoint "
                    "residuals, and aligned to the accepted formula-freeze source manifest"
                ),
                "what_is_missing": "law-level Tau-side derivation",
            },
            {
                "component_id": "B2C2_SCALE_SELECTION",
                "component_status": str(selection["selection_status"]),
                "what_is_established": "minimal source-onset asymptotic-carrier rule selects CURRENT_XW_VFLAT2",
                "what_is_missing": "selection rule itself is conditional, not a final law",
            },
            {
                "component_id": "B2C3_SCALE_DERIVATION_GATE",
                "component_status": str(derivation["derivation_status"]),
                "what_is_established": "derivation skeleton identifies the needed Tau-side assumptions",
                "what_is_missing": "asymptotic carrier dominance and closure functional derivation",
            },
            {
                "component_id": "B2C4_ASYMPTOTIC_CARRIER",
                "component_status": str(asymptotic["dominance_status"]),
                "what_is_established": "Vflat^2 is a valid residual-blind source/catalog carrier candidate",
                "what_is_missing": "proof that Vflat^2 is forced as Tau-side asymptotic carrier",
            },
            {
                "component_id": "B2C5_CLOSURE_FUNCTIONAL",
                "component_status": str(closure["functional_status"]),
                "what_is_established": "required functional form and solved target are specified",
                "what_is_missing": "actual Tau-side closure functional and Euler stationarity proof",
            },
            {
                "component_id": "B2C6_TARGET_ORIGIN",
                "component_status": str(target["target_origin_status"]),
                "what_is_established": "source factors for the target lambda are available",
                "what_is_missing": "source-factor coupling is not derived as Tau-side law",
            },
            {
                "component_id": "B2C7_EULER_ANSATZ",
                "component_status": str(euler["euler_status"]),
                "what_is_established": "given a target quadratic ansatz, the Euler condition solves to the candidate lambda",
                "what_is_missing": "the target ansatz itself is not yet Tau-side derived",
            },
            {
                "component_id": "B2C8_SEPARABILITY",
                "component_status": str(separability["coupling_status"]),
                "what_is_established": "conditional product form follows if separable source factors and suppressed cross terms hold",
                "what_is_missing": "separability and cross-term suppression are not final derived laws",
            },
            {
                "component_id": "B2C9_CROSS_TERM_SUPPRESSION",
                "component_status": str(cross["cross_term_status"]),
                "what_is_established": "cross-term status has an explicit source-side audit",
                "what_is_missing": "final Tau-side bound/vanishing theorem for cross terms",
            },
        ]
    )
    components["endpoint_scores_allowed"] = False
    components["claim_boundary"] = CLAIM_BOUNDARY

    law_obligations = pd.DataFrame(
        [
            {
                "obligation_id": "B2O1_CLOSURE_FUNCTIONAL_CONSTRUCTION",
                "obligation_status": "OPEN",
                "requirement": (
                    "construct J_tau[lambda_w] from Tau-side morphology/readout and closure data, "
                    "not from endpoint residuals"
                ),
                "why_required": "without J_tau, the Euler solution remains an ansatz rather than a derivation",
            },
            {
                "obligation_id": "B2O2_ASYMPTOTIC_CARRIER_THEOREM",
                "obligation_status": "OPEN",
                "requirement": "derive Vflat^2 as the asymptotic Tau-side readout carrier",
                "why_required": "otherwise Vflat^2 is a good residual-blind catalog scale, not a forced carrier",
            },
            {
                "obligation_id": "B2O3_SEPARABILITY_OR_CROSS_TERM_BOUND",
                "obligation_status": "OPEN",
                "requirement": (
                    "prove separable product coupling or freeze a source-side cross-term uncertainty interval"
                ),
                "why_required": "otherwise sigma*q*x_w*Vflat^2 is conditional on unproved coupling assumptions",
            },
            {
                "obligation_id": "B2O4_POPULATION_TRANSFER",
                "obligation_status": "OPEN_FOR_CLAIMS",
                "requirement": "repeat the same derivation gate on a predeclared warp/history source-rich sample",
                "why_required": "single-galaxy derivation support cannot justify broad population claims",
            },
        ]
    )
    law_obligations["endpoint_scores_allowed"] = False
    law_obligations["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "b2_synthesis_status": "B2_FORMULA_CONDITIONAL_DERIVATION_SYNTHESIZED_LAW_STILL_OPEN",
                "formula_quality": "DIMENSIONALLY_VALID_RESIDUAL_BLIND_EXECUTABLE",
                "law_quality": "NOT_DERIVED_TAU_SIDE_PHYSICAL_NORMALIZATION_LAW",
                "formula_freeze_alignment_status": (
                    "ALIGNED_TO_FORMULA_FREEZE_MANIFEST"
                    if formula_freeze_alignment_pass
                    else "NOT_ALIGNED_TO_FORMULA_FREEZE_MANIFEST"
                ),
                "numeric_lambda_w_km2_s2": numeric_lambda,
                "first_pass_lambda_w_km2_s2": first_pass_lambda,
                "normalization_source": normalization_source,
                "n_components": len(components),
                "n_open_law_obligations": len(law_obligations),
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "construct closure functional and asymptotic-carrier theorem, "
                    "or explicitly demote NGC4088 to sensitivity-only formula shell"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    formula.to_csv(DATA / "ngc4088_b2_physical_normalization_formula_status.csv", index=False)
    components.to_csv(DATA / "ngc4088_b2_physical_normalization_components.csv", index=False)
    law_obligations.to_csv(DATA / "ngc4088_b2_physical_normalization_obligations.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b2_physical_normalization_synthesis_summary.csv", index=False)

    report = [
        "# NGC4088 B2 Physical-Normalization Derivation Synthesis",
        "",
        "This report consolidates the B2 status. It asks whether the conditional",
        "normalization `lambda_w = sigma_warp q_warp x_w Vflat^2` is already a",
        "Tau-side physical law. The answer is no: it is a strong formula shell and",
        "a conditional derivation path, but the final law-level proof is still open.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Candidate Formula",
        "",
        markdown_table(formula),
        "",
        "The numerical normalization is aligned to the accepted formula-freeze",
        "manifest when that manifest is present. This supersedes the earlier",
        "first-pass physical-normalization value for the endpoint formula, while",
        "preserving the first-pass value as provenance rather than deleting it.",
        "",
        "## Components",
        "",
        markdown_table(components),
        "",
        "## Remaining Law Obligations",
        "",
        markdown_table(law_obligations),
        "",
        "## Interpretation",
        "",
        "B2 has been narrowed substantially. The package now knows exactly how the",
        "candidate law would look and which assumptions make it work. However, the",
        "Tau-side closure functional, the asymptotic-carrier theorem, and the",
        "separability/cross-term bound remain open. Therefore the formula remains",
        "formula-conditional and endpoint-blocked.",
        "",
    ]
    (REPORTS / "ngc4088_b2_physical_normalization_derivation_synthesis.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
