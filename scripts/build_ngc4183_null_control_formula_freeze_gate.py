#!/usr/bin/env python3
"""Build the NGC4183 weak-projection null-control formula freeze gate.

The script is intentionally capable of writing a blocked freeze manifest.  It
only promotes the null-control formula if the independent tilted-ring review
response has accepted the source profile and explicitly authorized freeze.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_null_control_formula_freeze_gate_not_endpoint"
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


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    readiness = pd.read_csv(DATA / "ngc4183_null_control_freeze_readiness_summary.csv").iloc[0]
    weak = pd.read_csv(DATA / "ngc4183_weak_projection_control_summary.csv").iloc[0]
    visual = pd.read_csv(DATA / "ngc4183_visual_review_readiness_summary.csv").iloc[0]

    gamma_bound = float(weak["gamma_projection_upper_bound"])
    velocity_fraction = float(weak["max_velocity_fractional_change"])
    readiness_allows_freeze = truthy(readiness["formula_freeze_allowed"])
    freeze_status = (
        "NGC4183_NULL_CONTROL_FORMULA_FROZEN_NOT_ENDPOINT"
        if readiness_allows_freeze
        else "NGC4183_NULL_CONTROL_FORMULA_FREEZE_BLOCKED_REVIEW_REQUIRED"
    )

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": "N4183_WEAK_PROJECTION_NULL_CONTROL_BOUND",
                "freeze_status": freeze_status,
                "formula": "v_readout^2/v_carrier^2 in [1-gamma_bound, 1]",
                "carrier": "predeclared smooth exponential-disk carrier",
                "gamma_bound": gamma_bound,
                "max_velocity_fractional_change": velocity_fraction,
                "sign": "bounded_attenuation_or_zero",
                "kernel": "source-side orientation drift upper bound",
                "coefficient_rule": "gamma_bound = p_edge * max_R{sin^2(Delta PA), sin^2(Delta i)}",
                "coefficient_rule_status": (
                    "FROZEN_AFTER_INDEPENDENT_REVIEW"
                    if readiness_allows_freeze
                    else "BLOCKED_PENDING_INDEPENDENT_REVIEW"
                ),
                "uses_vobs_or_residual": False,
                "formula_freeze_allowed": readiness_allows_freeze,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    grid = pd.DataFrame(
        [
            {
                "x_R_over_RHI": x / 20.0,
                "v2_ratio_min": 1.0 - gamma_bound,
                "v2_ratio_max": 1.0,
                "max_velocity_fractional_change": velocity_fraction,
                "uses_vobs_or_residual": False,
            }
            for x in range(0, 21)
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_NCFF_G1_READINESS",
                "gate_status": "PASS" if readiness_allows_freeze else "BLOCKED",
                "evidence": str(readiness["null_control_freeze_readiness_status"]),
                "formula_freeze_allowed": readiness_allows_freeze,
                "endpoint_scores_allowed": False,
                "remaining_obligation": (
                    "none"
                    if readiness_allows_freeze
                    else "complete independent review response before freeze"
                ),
            },
            {
                "gate_id": "N4183_NCFF_G2_VISUAL_PACKET",
                "gate_status": "PASS",
                "evidence": str(visual["visual_review_readiness_status"]),
                "formula_freeze_allowed": readiness_allows_freeze,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "review response still required before freeze",
            },
            {
                "gate_id": "N4183_NCFF_G3_DIMENSIONS_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "v2 ratios are dimensionless; gamma_bound->0 recovers carrier",
                "formula_freeze_allowed": readiness_allows_freeze,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none for formula shell",
            },
            {
                "gate_id": "N4183_NCFF_G4_ENDPOINT_SCORE",
                "gate_status": "BLOCKED",
                "evidence": "null-control formula freeze is not endpoint validation",
                "formula_freeze_allowed": readiness_allows_freeze,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "separate accepted endpoint/control gate required after freeze",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "null_control_formula_freeze_status": freeze_status,
                "galaxy": GALAXY,
                "gamma_bound": gamma_bound,
                "max_velocity_fractional_change": velocity_fraction,
                "formula_freeze_allowed": readiness_allows_freeze,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": (
                    "accepted_null_control_gate"
                    if readiness_allows_freeze
                    else "complete_independent_review_response"
                ),
            }
        ]
    )

    manifest.to_csv(DATA / "ngc4183_null_control_formula_freeze_manifest.csv", index=False)
    grid.to_csv(DATA / "ngc4183_null_control_formula_freeze_grid.csv", index=False)
    gates.to_csv(DATA / "ngc4183_null_control_formula_freeze_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_null_control_formula_freeze_summary.csv", index=False)

    report = f"""# NGC4183 Null-Control Formula Freeze Gate

Status: `{summary.iloc[0]["null_control_formula_freeze_status"]}`

This gate freezes, or blocks freezing, the NGC4183 weak-projection/null-control
formula.  It does not run endpoint scoring.

## Summary

{markdown_table(summary)}

## Manifest

{markdown_table(manifest)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Frozen/Blocked Formula

```text
v_readout^2 / v_carrier^2 in [1 - gamma_bound, 1]
gamma_bound = p_edge * max_R {{ sin^2(Delta PA), sin^2(Delta i) }}
gamma_bound = {gamma_bound:.8f}
|Delta v|/v <= {velocity_fraction:.8f}
```

## Verdict

The formula shell is dimensionally consistent and has the correct carrier
limit.  It remains blocked until the independent tilted-ring review response
accepts or corrects the source profile and explicitly authorizes null-control
freeze.
"""
    (REPORTS / "ngc4183_null_control_formula_freeze_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
