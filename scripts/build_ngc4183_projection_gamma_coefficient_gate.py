#!/usr/bin/env python3
"""Audit whether NGC4183 has a source-blind projection coefficient rule."""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_projection_gamma_coefficient_gate_not_endpoint"
GALAXY = "NGC4183"


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


def attenuation_from_inclinations(i_used_deg: float, i_true_deg: float) -> float:
    """Return v_true^2/v_used^2 attenuation deficit from inclination correction.

    If velocities are deprojected with i_used but the source-native inclination
    should be i_true, then v_true/v_used = sin(i_used)/sin(i_true).  A
    multiplicative attenuation shell can represent this as
    v_true^2 = v_used^2 * (1 - gamma), where gamma = 1 - ratio^2.
    """
    ratio = math.sin(math.radians(i_used_deg)) / math.sin(math.radians(i_true_deg))
    return 1.0 - ratio * ratio


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    formula_summary = pd.read_csv(DATA / "ngc4183_projection_outer_warp_formula_summary.csv").iloc[0]
    obs = pd.read_csv(DATA / "ngc4183_mixed_overlay_observable_sheet.csv")

    i_sparc = 82.0
    i_hi = 83.0
    gamma_82_to_83 = attenuation_from_inclinations(i_sparc, i_hi)
    p_edge = float(obs.loc[obs["observable_id"].eq("projection_edge_on_strength_p_edge"), "value"].iloc[0])

    candidates = pd.DataFrame(
        [
            {
                "candidate_rule": "inclination_difference_only",
                "candidate_gamma_proj": gamma_82_to_83,
                "source_inputs": "SPARC Inc=82 deg; source-native HI inclination=83 deg",
                "status": "SOURCE_DERIVED_BUT_TOO_SMALL_AND_SIGNIFICANCE_LIMITED",
                "freeze_allowed": False,
                "reason": "only compares two nearly identical high inclinations; does not encode warp/profile overlay",
            },
            {
                "candidate_rule": "edge_on_strength_direct",
                "candidate_gamma_proj": p_edge,
                "source_inputs": "p_edge=sin^2(i_HI)",
                "status": "REJECTED_DIMENSIONLESS_BUT_NOT_A_COEFFICIENT_DERIVATION",
                "freeze_allowed": False,
                "reason": "p_edge belongs inside the kernel; using it again as gamma would double-count projection",
            },
            {
                "candidate_rule": "residual_fit_gamma",
                "candidate_gamma_proj": pd.NA,
                "source_inputs": "endpoint residuals",
                "status": "FORBIDDEN_FOR_FREEZE",
                "freeze_allowed": False,
                "reason": "would violate residual-blind endpoint protocol",
            },
            {
                "candidate_rule": "source_native_tilted_ring_gamma",
                "candidate_gamma_proj": pd.NA,
                "source_inputs": "radial tilted-ring inclination/PA or velocity-field model",
                "status": "PREFERRED_BUT_MISSING",
                "freeze_allowed": False,
                "reason": "requires source-native radial orientation model not currently extracted",
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_GAMMA_G1_GEOMETRIC_CANDIDATE",
                "gate_status": "PASS_AS_DIAGNOSTIC_ONLY",
                "evidence": f"82->83 deg gives gamma={gamma_82_to_83:.6g}",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "do not freeze because it only captures a near-identical inclination comparison",
            },
            {
                "gate_id": "N4183_GAMMA_G2_NO_DOUBLE_COUNTING",
                "gate_status": "PASS_BLOCKS_BAD_RULE",
                "evidence": "p_edge already enters K_proj",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "gamma must be an independent coefficient rule",
            },
            {
                "gate_id": "N4183_GAMMA_G3_RESIDUAL_BLINDNESS",
                "gate_status": "PASS_BLOCKS_ENDPOINT_FIT",
                "evidence": "no vobs/residual used",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "source-native radial model required",
            },
            {
                "gate_id": "N4183_GAMMA_G4_FREEZE",
                "gate_status": "BLOCKED",
                "evidence": "no acceptable gamma_proj rule is frozen",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "acquire tilted-ring/profile source or declare NGC4183 blocked",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "gamma_gate_status": "NGC4183_PROJECTION_GAMMA_RULE_BLOCKED_SOURCE_NATIVE_RADIAL_MODEL_REQUIRED",
                "galaxy": GALAXY,
                "formula_derivation_status": str(formula_summary["formula_derivation_status"]),
                "gamma_82_to_83_diagnostic": gamma_82_to_83,
                "p_edge_kernel_value": p_edge,
                "coefficient_rule_frozen": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "acquire_or_extract_source_native_tilted_ring_orientation_profile",
            }
        ]
    )

    candidates.to_csv(DATA / "ngc4183_projection_gamma_coefficient_candidates.csv", index=False)
    gates.to_csv(DATA / "ngc4183_projection_gamma_coefficient_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_projection_gamma_coefficient_summary.csv", index=False)

    report = f"""# NGC4183 Projection Gamma Coefficient Gate

Status: `{summary.iloc[0]["gamma_gate_status"]}`

This gate asks whether the projection attenuation formula can be frozen without
using endpoint residuals.

## Summary

{markdown_table(summary)}

## Candidate Rules

{markdown_table(candidates)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Verdict

The projection formula shell is useful, but the coefficient is not frozen.
The only purely local inclination comparison, 82 to 83 degrees, gives a tiny
diagnostic attenuation `gamma={gamma_82_to_83:.6g}` and cannot represent the
radial projection/warp structure.  Using `p_edge` as both kernel and coefficient
would double-count the same evidence.  Therefore NGC4183 needs a source-native
tilted-ring or orientation-profile extraction before endpoint scoring.
"""
    (REPORTS / "ngc4183_projection_gamma_coefficient_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
