#!/usr/bin/env python3
"""Build the NGC4088 minimal Euler-ansatz gate.

This gate records the first explicit stationarity calculation for the
NGC4088 warp/asymmetry normalization.  It shows that a minimal quadratic
target functional yields lambda_w = sigma q x_w Vflat^2, while preserving the
claim boundary that the target functional itself is still an ansatz, not a
derived Tau-side closure functional.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_minimal_euler_ansatz_gate_not_endpoint"


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
    values = dict(zip(constants["constant_name"], constants["constant_value"]))
    sigma = float(values["sigma_warp_orientation"])
    q_warp = float(values["q_warp"])
    x_w = float(values["c_warp_candidate"])
    vflat2 = float(values["velocity_scale_candidate"])
    target = sigma * q_warp * x_w * vflat2

    ansatz = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "ansatz_id": "MINIMAL_QUADRATIC_TARGET_EULER_ANSATZ",
                "functional_ansatz": (
                    "J_min(lambda_w) = 1/2 kappa_lambda "
                    "(lambda_w - sigma_warp q_warp x_w Vflat^2)^2"
                ),
                "stationarity_equation": (
                    "dJ_min/dlambda_w = kappa_lambda "
                    "(lambda_w - sigma_warp q_warp x_w Vflat^2) = 0"
                ),
                "solved_lambda_km2_s2": target,
                "solved_lambda_formula": "lambda_w = sigma_warp q_warp x_w Vflat^2",
                "proof_status": "EULER_SOLVES_TARGET_GIVEN_ANSATZ",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "E1_DIMENSIONAL_TARGET_VALID",
                "gate_status": "PASS",
                "evidence": "lambda_w and sigma q x_w Vflat^2 both carry km^2/s^2",
                "remaining_obligation": "none at dimensional level",
            },
            {
                "gate_id": "E2_STATIONARITY_ALGEBRA",
                "gate_status": "PASS",
                "evidence": "dJ/dlambda_w=0 gives lambda_w=sigma q x_w Vflat^2 for kappa_lambda != 0",
                "remaining_obligation": "none for the conditional ansatz algebra",
            },
            {
                "gate_id": "E3_CONVEXITY",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "kappa_lambda > 0 would make the target stationary point a minimum",
                "remaining_obligation": "derive positive kappa_lambda from Tau-side closure geometry",
            },
            {
                "gate_id": "E4_TARGET_TERM_TAU_ORIGIN",
                "gate_status": "BLOCKED",
                "evidence": "the quadratic target is chosen to encode the selected scale",
                "remaining_obligation": "derive the target term from Tau-side morphology/readout, not by reverse engineering",
            },
            {
                "gate_id": "E5_WEIGHT_OR_STIFFNESS_DERIVATION",
                "gate_status": "BLOCKED",
                "evidence": "kappa_lambda is not derived",
                "remaining_obligation": "derive or eliminate the closure stiffness without endpoint residuals",
            },
            {
                "gate_id": "E6_NONTRIVIAL_SOURCE_COUPLING",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "x_w and q_warp enter the target as source-side factors",
                "remaining_obligation": "derive why they enter multiplicatively and linearly",
            },
            {
                "gate_id": "E7_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "the ansatz uses constants generated before endpoint scoring",
                "remaining_obligation": "keep endpoint evaluation separate",
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
                "ansatz_id": "MINIMAL_QUADRATIC_TARGET_EULER_ANSATZ",
                "solved_lambda_km2_s2": target,
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "euler_status": "EULER_CONDITION_SOLVED_GIVEN_TARGET_ANSATZ",
                "law_status": "TARGET_FUNCTIONAL_NOT_TAU_SIDE_DERIVED",
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
        "# NGC4088 Minimal Euler-Ansatz Gate",
        "",
        "This gate performs the first explicit stationarity calculation for the",
        "NGC4088 warp/asymmetry normalization. It is conditional on a quadratic",
        "target functional and does not prove the Tau-side origin of that target.",
        "",
        "## Verdict",
        "",
        "Given the minimal quadratic target ansatz, the Euler condition gives",
        "`lambda_w = sigma_warp q_warp x_w Vflat^2`. The algebra is explicit and",
        "dimensionally consistent. The target functional itself remains blocked",
        "as a Tau-side derivation.",
        "",
        "## Ansatz",
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
        "This is a conditional Euler calculation, not a final physical law. It",
        "does not use endpoint velocities or residuals.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_minimal_euler_ansatz_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    ansatz, gates, summary = build_gate()
    ansatz.to_csv(DATA / "s4g75_ngc4088_minimal_euler_ansatz.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_minimal_euler_ansatz_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_minimal_euler_ansatz_summary.csv", index=False)
    write_report(ansatz, gates, summary)
    print("PAPER8_NGC4088_MINIMAL_EULER_ANSATZ_GATE_COMPLETE")


if __name__ == "__main__":
    main()
