#!/usr/bin/env python3
"""Derive a source-side upper bound for NGC4183 projection attenuation.

This gate uses the residual-blind tilted-ring orientation profile to ask how
large a projection coefficient could be if it is sourced only by the observed
radial orientation drift.  It intentionally does not score an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_projection_gamma_upper_bound_gate_not_endpoint"
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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    profile = pd.read_csv(DATA / "ngc4183_tilted_ring_orientation_profile.csv")
    profile_summary = pd.read_csv(
        DATA / "ngc4183_tilted_ring_orientation_profile_summary.csv"
    ).iloc[0]
    formula_summary = pd.read_csv(
        DATA / "ngc4183_projection_outer_warp_formula_summary.csv"
    ).iloc[0]

    p_edge = float(formula_summary["p_edge"])
    max_twist = float(profile_summary["max_twist_kernel_sin2_delta_pa"])
    max_inclination_kernel = float(profile["inclination_kernel_sin2_delta_i"].max())
    raw_orientation_bound = max(max_twist, max_inclination_kernel)
    gamma_upper_bound = p_edge * raw_orientation_bound

    profile_bound = profile.copy()
    profile_bound["orientation_kernel_upper"] = profile_bound[
        ["twist_kernel_sin2_delta_pa", "inclination_kernel_sin2_delta_i"]
    ].max(axis=1)
    profile_bound["gamma_profile_bound"] = p_edge * profile_bound["orientation_kernel_upper"]
    profile_bound["max_fractional_v2_attenuation_bound"] = profile_bound[
        "gamma_profile_bound"
    ] * profile_bound["activation_bound_assumed"] if "activation_bound_assumed" in profile_bound else profile_bound["gamma_profile_bound"]

    components = pd.DataFrame(
        [
            {
                "component_id": "edge_on_kernel_strength",
                "value": p_edge,
                "unit": "dimensionless",
                "source": "NGC4183 projection formula summary",
                "status": "SOURCE_SIDE_ACCEPTED_CAVEATED",
                "interpretation": "large edge-on factor, already assigned to K_proj",
            },
            {
                "component_id": "max_pa_twist_kernel",
                "value": max_twist,
                "unit": "dimensionless",
                "source": "tilted-ring PA drift profile",
                "status": "OCR_REVIEW_REQUIRED",
                "interpretation": "small radial orientation drift",
            },
            {
                "component_id": "max_inclination_drift_kernel",
                "value": max_inclination_kernel,
                "unit": "dimensionless",
                "source": "tilted-ring inclination drift profile",
                "status": "OCR_REVIEW_REQUIRED",
                "interpretation": "zero inclination drift in extracted profile",
            },
            {
                "component_id": "gamma_projection_upper_bound",
                "value": gamma_upper_bound,
                "unit": "dimensionless",
                "source": "p_edge * max(orientation drift kernels)",
                "status": "FORMULA_CONDITIONAL_UPPER_BOUND_NOT_FREEZE",
                "interpretation": "source-side bound is too small for a strong correction",
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_UB_G1_SOURCE_PROFILE_AVAILABLE",
                "gate_status": "PASS_REVIEW_REQUIRED",
                "evidence": str(profile_summary["tilted_ring_profile_status"]),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "independent review of OCR/profile extraction",
            },
            {
                "gate_id": "N4183_UB_G2_DIMENSIONLESS_BOUND",
                "gate_status": "PASS",
                "evidence": "p_edge and orientation drift kernels are dimensionless",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none for upper-bound algebra",
            },
            {
                "gate_id": "N4183_UB_G3_BOUND_STRENGTH",
                "gate_status": "WEAK_CORRECTION_BOUND",
                "evidence": f"gamma_upper_bound={gamma_upper_bound:.6g}",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "treat as limiting evidence, not a strong endpoint candidate",
            },
            {
                "gate_id": "N4183_UB_G4_ENDPOINT_SCORE_ALLOWED",
                "gate_status": "BLOCKED",
                "evidence": "upper bound only; no frozen predictive coefficient rule",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "either freeze as a null/weak-control formula after review or acquire stronger source profile",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "upper_bound_gate_status": "NGC4183_PROJECTION_GAMMA_UPPER_BOUND_DERIVED_WEAK_NOT_ENDPOINT",
                "galaxy": GALAXY,
                "p_edge": p_edge,
                "max_twist_kernel_sin2_delta_pa": max_twist,
                "max_inclination_kernel_sin2_delta_i": max_inclination_kernel,
                "gamma_projection_upper_bound": gamma_upper_bound,
                "strong_projection_endpoint_supported": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "decide_ngc4183_as_weak_projection_control_or_acquire_higher_quality_orientation_profile",
            }
        ]
    )

    components.to_csv(DATA / "ngc4183_projection_gamma_upper_bound_components.csv", index=False)
    profile_bound.to_csv(DATA / "ngc4183_projection_gamma_upper_bound_profile.csv", index=False)
    gates.to_csv(DATA / "ngc4183_projection_gamma_upper_bound_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_projection_gamma_upper_bound_summary.csv", index=False)

    report = f"""# NGC4183 Projection Gamma Upper-Bound Gate

Status: `{summary.iloc[0]["upper_bound_gate_status"]}`

This is a source-side upper-bound derivation, not an endpoint score.  It asks
whether the extracted NGC4183 tilted-ring orientation profile can support a
large projection attenuation coefficient.

## Summary

{markdown_table(summary)}

## Components

{markdown_table(components)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Profile Bound Preview

{markdown_table(profile_bound[["radius_arcsec", "x_R_over_RHI", "delta_pa_deg", "delta_i_deg", "gamma_profile_bound"]].head(12))}

## Derived Bound

Definition:

```text
gamma_proj <= p_edge * max_R {{ sin^2(Delta PA(R)), sin^2(Delta i(R)) }}
```

For the current NGC4183 source profile:

```text
p_edge = {p_edge:.6f}
max sin^2(Delta PA) = {max_twist:.6f}
max sin^2(Delta i)  = {max_inclination_kernel:.6f}
gamma_proj <= {gamma_upper_bound:.6f}
```

## Verdict

The source-side projection bound is very small.  This is useful limiting
evidence: NGC4183 can remain a projection/outer-warp caveated object, but the
currently extracted orientation profile does not support a strong projection
attenuation endpoint.  The fair next choice is either to treat NGC4183 as a
weak-projection control after independent review, or to acquire a higher-quality
machine-readable tilted-ring/velocity-field source before scoring.
"""
    (REPORTS / "ngc4183_projection_gamma_upper_bound_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
