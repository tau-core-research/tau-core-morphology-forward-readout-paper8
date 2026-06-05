#!/usr/bin/env python3
"""Build a conditional derivation gate for the split-B2 mu_load term.

The gate asks whether the preferred split branch

    Delta v^2 = sigma_warp * mu_load * x_w * Vflat^2 * ramp(x;x_w)

can use mu_load=1 as a residual-blind protocol constant. This is a theory
gate, not endpoint scoring. It records the assumptions under which the unit
load follows, and the source-observable conditions under which it must remain
open.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_b2_mu_load_derivation_gate_not_endpoint"


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

    split_summary = pd.read_csv(
        DATA / "ngc7331_b2_split_q_source_load_summary.csv"
    ).iloc[0]
    freeze = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_formula_freeze_manifest.csv"
    ).iloc[0]
    q_role = pd.read_csv(DATA / "ngc7331_b2_q_role_separation_summary.csv").iloc[0]

    x_w = float(freeze["x_w_formula_freeze"])
    vflat = float(freeze["vflat_km_s"])
    source_scale = x_w * vflat**2

    assumptions = pd.DataFrame(
        [
            {
                "assumption_id": "MU1_SPLIT_ROLE",
                "assumption_text": (
                    "q_shape is a morphology/kernel observable and is not "
                    "identified with the source-load amplitude"
                ),
                "status": "SUPPORTED_BY_DIAGNOSTIC",
                "evidence": str(q_role["audit_status"]),
            },
            {
                "assumption_id": "MU2_MINIMAL_CARRIER",
                "assumption_text": (
                    "x_w Vflat^2 is the minimally factorized asymptotic source "
                    "carrier for the split branch"
                ),
                "status": "FORMULA_CONDITIONAL",
                "evidence": (
                    "inherits the NGC4088 B2 asymptotic-carrier premise; "
                    "not a final Tau-side law"
                ),
            },
            {
                "assumption_id": "MU3_NO_EXTRA_LOAD_OBSERVABLE",
                "assumption_text": (
                    "no independent residual-blind load observable is accepted "
                    "beyond x_w, Vflat, sign, and the radial active window"
                ),
                "status": "CONDITIONAL_DEFAULT",
                "evidence": (
                    "current NGC7331 split gate lists candidates, but none is "
                    "source-frozen as a primary load rule"
                ),
            },
            {
                "assumption_id": "MU4_NORMALIZED_LOAD_COORDINATE",
                "assumption_text": (
                    "mu_load is defined as the dimensionless coefficient left "
                    "after factoring out x_w Vflat^2"
                ),
                "status": "DEFINITION",
                "evidence": "Delta v^2 = sigma mu_load x_w Vflat^2 K_shape",
            },
            {
                "assumption_id": "MU5_ZERO_SOURCE_AND_INACTIVE_LIMITS",
                "assumption_text": (
                    "inactive window and zero-sign/zero-load limits recover "
                    "the Newtonian carrier"
                ),
                "status": "PASS",
                "evidence": "ramp=0 for x<=x_w; mu_load=0 or sigma=0 gives Delta v^2=0",
            },
        ]
    )
    assumptions["galaxy"] = GALAXY
    assumptions["endpoint_scores_allowed"] = False
    assumptions["uses_vobs_or_residual"] = False
    assumptions["claim_boundary"] = CLAIM_BOUNDARY

    theorem = pd.DataFrame(
        [
            {
                "theorem_id": "SPLIT_B2_UNIT_LOAD_CONDITIONAL_THEOREM",
                "statement": (
                    "Given role separation, minimal carrier factorization, and "
                    "absence of an accepted independent load observable, the "
                    "canonical dimensionless split-load coordinate is mu_load=1."
                ),
                "proof_sketch": (
                    "After factoring x_w Vflat^2 from the source-load term, "
                    "mu_load is dimensionless. If no additional source-load "
                    "observable is admitted, any non-unit constant is either a "
                    "new unexplained scale or a fit parameter. The normalized "
                    "coordinate choice therefore fixes the protocol constant to "
                    "1 until a residual-blind source observable replaces it."
                ),
                "derived_formula": (
                    "Delta v^2_split(R)=sigma_warp x_w Vflat^2 ramp(R/R_HI;x_w)"
                ),
                "mathematical_status": "CONDITIONAL_COORDINATE_NORMALIZATION",
                "tau_side_law_status": "NOT_FINAL_LAW_SOURCE_LOAD_ORIGIN_OPEN",
                "dimension_check": (
                    "PASS: x_w and ramp are dimensionless; Vflat^2 has km^2/s^2"
                ),
                "known_limits": (
                    "inactive window recovers carrier; sigma=0 recovers carrier"
                ),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    theorem["galaxy"] = GALAXY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "MULD1_ROLE_SEPARATION",
                "gate_status": "PASS",
                "evidence": "q_shape/mu_load split gate built",
                "remaining_obligation": "none for diagnostic role separation",
            },
            {
                "gate_id": "MULD2_DIMENSIONLESS_MU",
                "gate_status": "PASS",
                "evidence": "mu_load is dimensionless after factoring x_w Vflat^2",
                "remaining_obligation": "none at dimensional level",
            },
            {
                "gate_id": "MULD3_UNIT_LOAD_COORDINATE",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "unit value follows as normalized coordinate if no extra load observable is admitted",
                "remaining_obligation": "derive Tau-side reason for minimal-load coordinate",
            },
            {
                "gate_id": "MULD4_SOURCE_LOAD_ORIGIN",
                "gate_status": "OPEN",
                "evidence": "HI support/history/vertical candidates are not source-frozen as mu_load laws",
                "remaining_obligation": "derive or acquire residual-blind mu_load observable",
            },
            {
                "gate_id": "MULD5_ENDPOINT_ELIGIBILITY",
                "gate_status": "BLOCKED",
                "evidence": "post-failure theory derivation gate only",
                "remaining_obligation": "predeclare and freeze a new split-B2 branch before scoring",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "mu_load_derivation_status": "SPLIT_B2_UNIT_MU_LOAD_CONDITIONAL_DERIVATION_BUILT_ENDPOINT_BLOCKED",
                "mu_load_protocol_value": 1.0,
                "source_scale_xw_vflat2_km2_s2": source_scale,
                "derived_split_formula": (
                    "Delta v^2=sigma_warp*x_w*Vflat^2*ramp(x;x_w)"
                ),
                "n_assumptions": len(assumptions),
                "n_gates": len(gates),
                "n_pass": int(gates["gate_status"].eq("PASS").sum()),
                "n_formula_conditional": int(
                    gates["gate_status"].eq("FORMULA_CONDITIONAL").sum()
                ),
                "n_open": int(gates["gate_status"].eq("OPEN").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_status": (
                    "mu_load=1 is conditionally derived as a normalized split-load "
                    "coordinate, not as final Tau-side evidence or endpoint validation"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    assumptions.to_csv(DATA / "ngc7331_b2_mu_load_derivation_assumptions.csv", index=False)
    theorem.to_csv(DATA / "ngc7331_b2_mu_load_derivation_theorem.csv", index=False)
    gates.to_csv(DATA / "ngc7331_b2_mu_load_derivation_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_b2_mu_load_derivation_summary.csv", index=False)

    report = [
        "# NGC7331 B2 mu_load conditional derivation gate",
        "",
        "This gate does not score an endpoint. It records when the split B2",
        "branch may use `mu_load=1` as a normalized protocol coordinate.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Assumptions",
        "",
        markdown_table(assumptions),
        "",
        "## Conditional theorem",
        "",
        markdown_table(theorem),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Verdict",
        "",
        "`mu_load=1` is now a formula-conditional normalized split-load rule:",
        "it is allowed only under the minimal-carrier, no-extra-load-observable",
        "premise. It is not yet a final Tau-side law. If a residual-blind",
        "HI-support, history, projection, or vertical-overlay load observable is",
        "accepted later, it must replace or modify the unit-load coordinate before",
        "any future endpoint freeze.",
        "",
    ]
    (REPORTS / "ngc7331_b2_mu_load_derivation_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
