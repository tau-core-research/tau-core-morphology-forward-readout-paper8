#!/usr/bin/env python3
"""Build the NGC4088 B2 source-load closure functional gate.

This gate makes the closure-functional premise more explicit.  It constructs a
residual-blind conditional functional whose Euler equation yields the frozen
NGC4088 normalization, while preserving that the source-load origin and
asymptotic-carrier theorem remain open.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "ngc4088_b2_source_load_closure_functional_gate_not_endpoint"


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

    freeze = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_manifest.csv").iloc[0]
    asymptotic = pd.read_csv(DATA / "s4g75_ngc4088_asymptotic_carrier_dominance_summary.csv").iloc[0]
    cross = pd.read_csv(DATA / "s4g75_ngc4088_cross_term_suppression_summary.csv").iloc[0]

    sigma = float(freeze["sigma_warp"])
    q_warp = float(freeze["q_warp"])
    x_w = float(freeze["x_w_formula_freeze"])
    vflat = float(freeze["vflat_km_s"])
    lambda_source = sigma * q_warp * x_w * vflat**2
    lambda_manifest = float(freeze["lambda_w_km2_s2"])
    alignment_pass = abs(lambda_source - lambda_manifest) < 1.0e-6

    functional = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "functional_id": "B2_SOURCE_LOAD_CLOSURE_FUNCTIONAL",
                "kernel": "C_warp(R/R_HI; x_w,p)",
                "source_load": "Lambda_tau = sigma_warp q_warp x_w Vflat^2",
                "functional": (
                    "J_load[lambda_w] = 1/2 kappa_lambda || "
                    "(lambda_w - Lambda_tau) C_warp ||_W^2"
                ),
                "euler_equation": (
                    "dJ_load/dlambda_w = kappa_lambda <C_warp,C_warp>_W "
                    "(lambda_w - Lambda_tau) = 0"
                ),
                "stationary_solution": "lambda_w = Lambda_tau = sigma_warp q_warp x_w Vflat^2",
                "numeric_lambda_w_km2_s2": lambda_source,
                "formula_freeze_alignment_pass": alignment_pass,
                "mathematical_status": "EULER_DERIVED_FROM_CONDITIONAL_SOURCE_LOAD_FUNCTIONAL",
                "tau_side_law_status": "SOURCE_LOAD_AND_CARRIER_ORIGIN_OPEN",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "SL1_KERNEL_IS_RESIDUAL_BLIND_AND_DIMENSIONLESS",
                "gate_status": "PASS",
                "evidence": "C_warp is frozen from source-side x_w, p, q_warp and is dimensionless",
                "remaining_obligation": "none at kernel/dimension level",
            },
            {
                "gate_id": "SL2_SOURCE_LOAD_ALIGNED_TO_FREEZE",
                "gate_status": "PASS" if alignment_pass else "BLOCKED",
                "evidence": "Lambda_tau computed from frozen sigma, q_warp, x_w, and Vflat reproduces lambda_w",
                "remaining_obligation": "none at formula-freeze alignment level",
            },
            {
                "gate_id": "SL3_EULER_STATIONARITY",
                "gate_status": "PASS",
                "evidence": "for kappa_lambda>0 and nonzero kernel norm, dJ/dlambda_w=0 yields lambda_w=Lambda_tau",
                "remaining_obligation": "derive kappa_lambda and norm weight from Tau-side closure geometry",
            },
            {
                "gate_id": "SL4_ZERO_SOURCE_LIMIT",
                "gate_status": "PASS",
                "evidence": "sigma_warp=0 or q_warp=0 gives Lambda_tau=0 and the stationary correction vanishes",
                "remaining_obligation": "none at zero-source limit level",
            },
            {
                "gate_id": "SL5_INACTIVE_WINDOW_LIMIT",
                "gate_status": "PASS",
                "evidence": "C_warp=0 for R/R_HI <= x_w, so the readout recovers the carrier in the inactive window",
                "remaining_obligation": "none at inactive-window limit level",
            },
            {
                "gate_id": "SL6_SOURCE_LOAD_ORIGIN",
                "gate_status": "OPEN",
                "evidence": "the source-load form is explicit but not derived as the unique Tau-side closure load",
                "remaining_obligation": "derive why Lambda_tau must be sigma_warp q_warp x_w Vflat^2",
            },
            {
                "gate_id": "SL7_ASYMPTOTIC_CARRIER_ORIGIN",
                "gate_status": "OPEN",
                "evidence": str(asymptotic["dominance_status"]),
                "remaining_obligation": "derive Vflat^2 as the forced asymptotic carrier",
            },
            {
                "gate_id": "SL8_CROSS_TERM_BOUND",
                "gate_status": "OPEN",
                "evidence": str(cross["cross_term_status"]),
                "remaining_obligation": "prove cross-term suppression or freeze a source-side uncertainty interval",
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

    status_counts = gates["gate_status"].value_counts().to_dict()
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "closure_functional_status": (
                    "SOURCE_LOAD_CLOSURE_FUNCTIONAL_CONSTRUCTED_CONDITIONALLY"
                ),
                "numeric_lambda_w_km2_s2": lambda_source,
                "formula_freeze_alignment_pass": alignment_pass,
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_open": int(status_counts.get("OPEN", 0)),
                "law_level_closed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "derive the source-load origin, the Vflat^2 carrier theorem, "
                    "and the cross-term suppression bound"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    functional.to_csv(DATA / "ngc4088_b2_source_load_closure_functional.csv", index=False)
    gates.to_csv(DATA / "ngc4088_b2_source_load_closure_functional_gate.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b2_source_load_closure_functional_summary.csv", index=False)

    report = [
        "# NGC4088 B2 Source-Load Closure Functional Gate",
        "",
        "This gate constructs an explicit conditional closure functional for the",
        "NGC4088 frozen warp/history normalization. It does not use endpoint",
        "velocities, residuals, or score ranks.",
        "",
        "## Functional",
        "",
        markdown_table(functional),
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
        "The closure-functional premise is now sharper: given the source-load",
        "`Lambda_tau = sigma_warp q_warp x_w Vflat^2`, the explicit norm-square",
        "functional has an Euler equation whose stationary solution is the frozen",
        "normalization. This is still not a final Tau-side physical law, because",
        "the source-load origin, forced `Vflat^2` carrier theorem, and cross-term",
        "suppression remain open.",
        "",
    ]
    (REPORTS / "ngc4088_b2_source_load_closure_functional_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
