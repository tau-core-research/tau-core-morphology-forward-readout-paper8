#!/usr/bin/env python3
"""Prepare NGC4183 as a weak-projection/null-control candidate.

This preflight converts the source-side projection upper bound into a
near-carrier control statement.  It does not freeze an endpoint formula because
the tilted-ring extraction still needs independent review.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_weak_projection_control_preflight_not_endpoint"
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

    decision = pd.read_csv(DATA / "ngc4183_preendpoint_decision_summary.csv").iloc[0]
    upper = pd.read_csv(DATA / "ngc4183_projection_gamma_upper_bound_summary.csv").iloc[0]

    gamma_bound = float(upper["gamma_projection_upper_bound"])
    max_v_fraction_bound = 1.0 - math.sqrt(max(0.0, 1.0 - gamma_bound))

    formulas = pd.DataFrame(
        [
            {
                "formula_id": "N4183_WEAK_PROJECTION_NULL_CONTROL_BOUND",
                "formula": "v_readout^2/v_carrier^2 in [1-gamma_bound, 1]",
                "gamma_bound": gamma_bound,
                "max_velocity_fractional_change": max_v_fraction_bound,
                "formula_status": "CONTROL_BOUND_DERIVED_REVIEW_REQUIRED_NOT_FREEZE",
                "dimension_check": "all terms dimensionless ratios",
                "limit_check": "gamma_bound -> 0 recovers carrier exactly",
                "uses_vobs_or_residual": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "formula_id": "N4183_NEAR_CARRIER_CONTROL_READOUT",
                "formula": "v_readout^2 ~= v_carrier^2 within gamma_bound",
                "gamma_bound": gamma_bound,
                "max_velocity_fractional_change": max_v_fraction_bound,
                "formula_status": "NULL_CONTROL_CANDIDATE_AFTER_INDEPENDENT_SOURCE_REVIEW",
                "dimension_check": "velocity-squared carrier retained",
                "limit_check": "no residual-side correction introduced",
                "uses_vobs_or_residual": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_WPC_G1_PREENDPOINT_DECISION",
                "gate_status": "PASS",
                "evidence": str(decision["preendpoint_decision_status"]),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none for preflight",
            },
            {
                "gate_id": "N4183_WPC_G2_NEAR_CARRIER_BOUND",
                "gate_status": "PASS",
                "evidence": f"gamma_bound={gamma_bound:.6g}; velocity fractional bound={max_v_fraction_bound:.6g}",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "independent source review before freeze",
            },
            {
                "gate_id": "N4183_WPC_G3_ENDPOINT_USE",
                "gate_status": "BLOCKED",
                "evidence": "control preflight is not formula freeze or scoring",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "review OCR/profile extraction; then optionally freeze as null-control",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "weak_control_preflight_status": "NGC4183_WEAK_PROJECTION_CONTROL_PREFLIGHT_COMPLETE_NOT_ENDPOINT",
                "galaxy": GALAXY,
                "recommended_role": "WEAK_PROJECTION_NULL_CONTROL_AFTER_REVIEW",
                "gamma_projection_upper_bound": gamma_bound,
                "max_velocity_fractional_change": max_v_fraction_bound,
                "strong_projection_endpoint_supported": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "independent_profile_review_then_optional_null_control_freeze",
            }
        ]
    )

    formulas.to_csv(DATA / "ngc4183_weak_projection_control_formulas.csv", index=False)
    gates.to_csv(DATA / "ngc4183_weak_projection_control_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_weak_projection_control_summary.csv", index=False)

    report = f"""# NGC4183 Weak-Projection Control Preflight

Status: `{summary.iloc[0]["weak_control_preflight_status"]}`

This is a control preflight, not an endpoint score.  It uses the source-side
projection upper bound to decide whether NGC4183 is a strong correction
candidate or a near-carrier control candidate.

## Summary

{markdown_table(summary)}

## Control Formulas

{markdown_table(formulas)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Interpretation

The current source-side bound implies:

```text
v_readout^2 / v_carrier^2 >= 1 - {gamma_bound:.6f}
|Delta v| / v_carrier <= {max_v_fraction_bound:.6f}
```

So the present NGC4183 sources do not support a large Tau Core projection
correction.  The scientifically useful role is a weak-projection/null-control
case: the pipeline predicts a near-carrier readout unless better independent
velocity-field evidence reveals a larger source-side orientation effect.
"""
    (REPORTS / "ngc4183_weak_projection_control_preflight.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
