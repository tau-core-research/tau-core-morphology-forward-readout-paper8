#!/usr/bin/env python3
"""Build the NGC4088 B2 source-load origin derivation gate.

This gate decomposes the frozen source-load

    Lambda_tau = sigma_warp q_warp x_w Vflat^2

using the accepted formula-freeze manifest.  It is not an endpoint score and
does not use observed velocities or residuals.  The purpose is to distinguish
which factors are source-frozen, which are still protocol-conditional, and
which remain genuine Tau-side law obligations.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "ngc4088_b2_source_load_origin_derivation_gate_not_endpoint"


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


def b(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    freeze = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_manifest.csv").iloc[0]
    source_load = pd.read_csv(DATA / "ngc4088_b2_source_load_closure_functional_summary.csv").iloc[0]
    asymptotic = pd.read_csv(DATA / "s4g75_ngc4088_asymptotic_carrier_dominance_summary.csv").iloc[0]
    frozen_carrier = pd.read_csv(DATA / "ngc4088_b2_frozen_asymptotic_carrier_summary.csv").iloc[0]
    epsilon = pd.read_csv(DATA / "s4g75_ngc4088_epsilon_cross_source_bound_summary.csv").iloc[0]
    bi_sharp = pd.read_csv(DATA / "s4g75_ngc4088_bi_sharp_coefficient_bound_rule_summary.csv").iloc[0]

    sigma = float(freeze["sigma_warp"])
    q_warp = float(freeze["q_warp"])
    x_w = float(freeze["x_w_formula_freeze"])
    vflat = float(freeze["vflat_km_s"])
    lambda_tau = sigma * q_warp * x_w * vflat**2
    manifest_lambda = float(freeze["lambda_w_km2_s2"])
    alignment_pass = abs(lambda_tau - manifest_lambda) < 1.0e-6

    factors = pd.DataFrame(
        [
            {
                "factor_id": "SLF1_ORIENTATION_SIGN",
                "symbol": "sigma_warp",
                "value": sigma,
                "unit": "dimensionless",
                "factor_status": "SOURCE_PROTOCOL_FROZEN_CONDITIONAL",
                "source_evidence": str(freeze["sigma_rule"]),
                "remaining_law_obligation": "derive the sign from Tau-side orientation/readout geometry",
            },
            {
                "factor_id": "SLF2_SOURCE_STRENGTH",
                "symbol": "q_warp",
                "value": q_warp,
                "unit": "dimensionless",
                "factor_status": "SOURCE_PROTOCOL_FROZEN_QUALITATIVE",
                "source_evidence": str(freeze["q_warp_source"]),
                "remaining_law_obligation": "replace qualitative q_warp=1 by source-native amplitude law or uncertainty interval",
            },
            {
                "factor_id": "SLF3_ONSET_SUPPORT",
                "symbol": "x_w",
                "value": x_w,
                "unit": "dimensionless",
                "factor_status": "SOURCE_FROZEN_CAVEATED_ACCEPTED",
                "source_evidence": str(freeze["x_w_source"]),
                "remaining_law_obligation": "carry WHISP graphical provenance caveat; direct H I product remains provenance upgrade",
            },
            {
                "factor_id": "SLF4_ASYMPTOTIC_CARRIER",
                "symbol": "Vflat^2",
                "value": vflat**2,
                "unit": "km2_s2",
                "factor_status": "SOURCE_CATALOG_CANDIDATE_LAW_OPEN",
                "source_evidence": (
                    f"{freeze['selection_principle']}; "
                    f"{frozen_carrier['frozen_carrier_theorem_status']}"
                ),
                "remaining_law_obligation": "upgrade the frozen-protocol Vflat^2 carrier theorem to a final Tau-side carrier law and population-transfer result",
            },
            {
                "factor_id": "SLF5_SOURCE_LOAD_PRODUCT",
                "symbol": "Lambda_tau",
                "value": lambda_tau,
                "unit": "km2_s2",
                "factor_status": "FREEZE_ALIGNED_PRODUCT_CONDITIONAL",
                "source_evidence": str(freeze["amplitude_rule"]),
                "remaining_law_obligation": "derive source-load uniqueness and separability/cross-term suppression",
            },
        ]
    )
    factors["galaxy"] = GALAXY
    factors["claim_boundary"] = CLAIM_BOUNDARY
    factors = factors[
        [
            "galaxy",
            "factor_id",
            "symbol",
            "value",
            "unit",
            "factor_status",
            "source_evidence",
            "remaining_law_obligation",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "SLO1_FREEZE_ALIGNMENT",
                "gate_status": "PASS" if alignment_pass else "BLOCKED",
                "evidence": "source-load product reproduces the formula-freeze manifest lambda_w",
                "remaining_obligation": "none at freeze-alignment level",
            },
            {
                "gate_id": "SLO2_DIMENSION_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "dimensionless factors times Vflat^2 yield km^2/s^2; zero-source and inactive-window limits pass",
                "remaining_obligation": "none at dimension/limit level",
            },
            {
                "gate_id": "SLO3_CLOSURE_FUNCTIONAL_STATIONARITY",
                "gate_status": "PASS",
                "evidence": str(source_load["closure_functional_status"]),
                "remaining_obligation": "derive closure weight and source-load origin from Tau-side geometry",
            },
            {
                "gate_id": "SLO4_ONSET_SOURCE_ACCEPTANCE",
                "gate_status": "PASS_CAVEATED",
                "evidence": "x_w is accepted for formula freeze from WHISP graphical-overview extraction",
                "remaining_obligation": "direct source-coordinate H I/FITS product would reduce provenance caveat",
            },
            {
                "gate_id": "SLO5_STRENGTH_AND_SIGN_LAW",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "sigma_warp and q_warp are frozen by source protocol, but not derived as Tau-side laws",
                "remaining_obligation": "derive sign/strength mapping from orientation and source response",
            },
            {
                "gate_id": "SLO6_ASYMPTOTIC_CARRIER_THEOREM",
                "gate_status": "CONDITIONAL_CARRIER_THEOREM",
                "evidence": (
                    f"{asymptotic['dominance_status']}; "
                    f"{frozen_carrier['frozen_carrier_theorem_status']}"
                ),
                "remaining_obligation": "promote frozen single-galaxy carrier theorem to final Tau-side/population law",
            },
            {
                "gate_id": "SLO7_CROSS_TERM_SUPPRESSION_BOUND",
                "gate_status": "PARTIAL",
                "evidence": (
                    f"{epsilon['bound_status']}; "
                    f"{bi_sharp['sharp_rule_status']}; "
                    f"numeric_bound_authorized={b(bi_sharp['numeric_bound_coefficient_authorization'])}"
                ),
                "remaining_obligation": "complete q/memory source observables or keep epsilon_cross as explicit uncertainty",
            },
            {
                "gate_id": "SLO8_POPULATION_TRANSFER",
                "gate_status": "OPEN_FOR_CLAIMS",
                "evidence": "NGC4088-only source-load origin ladder",
                "remaining_obligation": "repeat on a predeclared warp/history source-rich sample",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    pass_like = {"PASS", "PASS_CAVEATED"}
    status_counts = gates["gate_status"].value_counts().to_dict()
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "source_load_origin_status": "SOURCE_LOAD_ORIGIN_PARTIALLY_GROUNDED_CARRIER_AND_CROSS_OPEN",
                "lambda_tau_km2_s2": lambda_tau,
                "formula_freeze_alignment_pass": alignment_pass,
                "n_factors": len(factors),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].isin(pass_like).sum()),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_partial": int(status_counts.get("PARTIAL", 0)),
                "n_conditional_carrier_theorem": int(
                    status_counts.get("CONDITIONAL_CARRIER_THEOREM", 0)
                ),
                "n_open_or_open_for_claims": int(
                    gates["gate_status"].isin(["OPEN", "OPEN_FOR_CLAIMS"]).sum()
                ),
                "law_level_closed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "upgrade frozen Vflat^2 carrier dominance to a final Tau-side law "
                    "and close or carry epsilon_cross as source-side uncertainty"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    factors.to_csv(DATA / "ngc4088_b2_source_load_origin_factors.csv", index=False)
    gates.to_csv(DATA / "ngc4088_b2_source_load_origin_gate.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b2_source_load_origin_summary.csv", index=False)

    report = [
        "# NGC4088 B2 Source-Load Origin Derivation Gate",
        "",
        "This gate decomposes the frozen `Lambda_tau` source-load using the",
        "accepted formula-freeze manifest. It does not score rotations and does",
        "not use endpoint residuals.",
        "",
        "## Factors",
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
        "## Interpretation",
        "",
        "The source-load is now partially grounded at protocol level: the product",
        "is aligned to the frozen manifest, the conditional source-load closure",
        "functional supplies the stationarity equation, and the onset factor is",
        "accepted with a provenance caveat. The remaining law-level work is the",
        "forced `Vflat^2` carrier theorem and a closed or explicitly carried",
        "`epsilon_cross` source-side uncertainty.",
        "",
    ]
    (REPORTS / "ngc4088_b2_source_load_origin_derivation_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
