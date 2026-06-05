#!/usr/bin/env python3
"""Derive an NGC4183 projection/outer-warp caveated formula shell.

This derivation is source-side only. It defines a dimensionally consistent
projection attenuation shell and a residual-blind kernel profile, but blocks
formula freeze because the coefficient rule and any numeric warp ramp are not
yet source-frozen.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_projection_outer_warp_formula_derivation_not_endpoint"
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


def smoothstep(x: float) -> float:
    y = min(1.0, max(0.0, x))
    return y * y * (3.0 - 2.0 * y)


def get_value(df: pd.DataFrame, observable_id: str) -> float:
    return float(df.loc[df["observable_id"].eq(observable_id), "value"].iloc[0])


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    obs = pd.read_csv(DATA / "ngc4183_mixed_overlay_observable_sheet.csv")
    label_summary = pd.read_csv(DATA / "ngc4183_projection_outer_warp_label_summary.csv").iloc[0]

    rhi_kpc = get_value(obs, "R_HI_source_native_kpc")
    rdisk_fraction = get_value(obs, "disk_scale_fraction_x_scale")
    p_edge = get_value(obs, "projection_edge_on_strength_p_edge")
    hi_extent = get_value(obs, "hi_extent_in_disk_scales")
    x_inner = max(0.15, min(0.35, 2.0 * rdisk_fraction))
    x_outer = 1.0

    derivation_steps = pd.DataFrame(
        [
            {
                "step_id": "D1_CARRIER",
                "definition_or_result": "v_carrier^2(R) is the predeclared smooth exponential-disk carrier",
                "status": "ASSUMPTION_FROM_EXISTING_SOURCE_LABEL",
                "dimension_check": "km^2/s^2",
                "limit_check": "carrier recovered when gamma_proj=0",
            },
            {
                "step_id": "D2_PROJECTION_OBSERVABLE",
                "definition_or_result": "p_edge = sin^2(i_HI)",
                "status": "DERIVED_FROM_SOURCE_NATIVE_HI_INCLINATION",
                "dimension_check": "dimensionless",
                "limit_check": "p_edge -> 0 face-on; p_edge -> 1 edge-on",
            },
            {
                "step_id": "D3_RADIAL_KERNEL",
                "definition_or_result": "K_proj(R)=p_edge*smoothstep((R/R_HI-x_inner)/(1-x_inner))",
                "status": "FORMULA_SHELL_DERIVED",
                "dimension_check": "dimensionless",
                "limit_check": "K_proj=0 inside inactive window; K_proj<=p_edge",
            },
            {
                "step_id": "D4_ATTENUATION_READOUT",
                "definition_or_result": "v_readout^2(R)=v_carrier^2(R)*(1-gamma_proj*K_proj(R))",
                "status": "FORMULA_CONDITIONAL_COEFFICIENT_UNFROZEN",
                "dimension_check": "km^2/s^2 because K_proj and gamma_proj are dimensionless",
                "limit_check": "gamma_proj=0 or K_proj=0 recovers carrier",
            },
            {
                "step_id": "D5_OUTER_WARP_CAVEAT",
                "definition_or_result": "outer warp statement can motivate caveat only, not a numeric added ramp",
                "status": "BLOCKS_WARP_RAMP_FREEZE",
                "dimension_check": "no numeric term introduced",
                "limit_check": "no warp amplitude means no added-source contribution",
            },
        ]
    )

    formulas = pd.DataFrame(
        [
            {
                "formula_id": "N4183_PROJECTION_ATTENUATION_SHELL",
                "formula": "v_readout^2(R)=v_carrier^2(R)*(1-gamma_proj*K_proj(R))",
                "kernel": "K_proj(R)=p_edge*smoothstep((R/R_HI-x_inner)/(1-x_inner))",
                "carrier": "smooth_exponential_disk_carrier",
                "sign": "attenuation",
                "amplitude_or_coefficient": "gamma_proj",
                "coefficient_status": "UNFROZEN_BLOCKS_FORMULA_FREEZE",
                "source_inputs": "R_HI_source_native_kpc; p_edge; Rdisk/RHI",
                "uses_vobs_or_residual": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    grid_rows = []
    for idx in range(31):
        x = idx / 30.0
        activation = smoothstep((x - x_inner) / (x_outer - x_inner))
        k_proj = p_edge * activation
        grid_rows.append(
            {
                "x_R_over_RHI": x,
                "R_kpc": x * rhi_kpc,
                "x_inner": x_inner,
                "p_edge": p_edge,
                "activation": activation,
                "K_proj": k_proj,
                "uses_vobs_or_residual": False,
            }
        )
    kernel_grid = pd.DataFrame(grid_rows)

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_FORMULA_G1_LABEL_DERIVATION_ALLOWED",
                "gate_status": "PASS",
                "evidence": str(label_summary["label_gate_status"]),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "derive only; freeze separately",
            },
            {
                "gate_id": "N4183_FORMULA_G2_DIMENSIONAL_CONSISTENCY",
                "gate_status": "PASS",
                "evidence": "gamma_proj and K_proj dimensionless; carrier has velocity-squared units",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none for shell",
            },
            {
                "gate_id": "N4183_FORMULA_G3_KNOWN_LIMITS",
                "gate_status": "PASS",
                "evidence": "gamma=0 and inactive kernel recover carrier; face-on p_edge tends to zero",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none for shell",
            },
            {
                "gate_id": "N4183_FORMULA_G4_COEFFICIENT_RULE",
                "gate_status": "BLOCKED",
                "evidence": "gamma_proj is not source-frozen",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "derive/freeze gamma_proj without residuals",
            },
            {
                "gate_id": "N4183_FORMULA_G5_WARP_RAMP",
                "gate_status": "BLOCKED",
                "evidence": "outer warp is qualitative only",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "do not include added warp ramp unless onset/amplitude is acquired",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "formula_derivation_status": "NGC4183_PROJECTION_OUTER_WARP_FORMULA_SHELL_DERIVED_FREEZE_BLOCKED",
                "galaxy": GALAXY,
                "candidate_readout": str(label_summary["replacement_candidate_readout"]),
                "rhi_kpc": rhi_kpc,
                "p_edge": p_edge,
                "hi_extent_in_disk_scales": hi_extent,
                "x_inner": x_inner,
                "coefficient_rule_frozen": False,
                "numeric_warp_ramp_frozen": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "source_blind_gamma_projection_coefficient_rule_or_freeze_blocker_resolution",
            }
        ]
    )

    derivation_steps.to_csv(
        DATA / "ngc4183_projection_outer_warp_formula_derivation_steps.csv", index=False
    )
    formulas.to_csv(DATA / "ngc4183_projection_outer_warp_formula_manifest.csv", index=False)
    kernel_grid.to_csv(DATA / "ngc4183_projection_outer_warp_formula_kernel_grid.csv", index=False)
    gates.to_csv(DATA / "ngc4183_projection_outer_warp_formula_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_projection_outer_warp_formula_summary.csv", index=False)

    report = f"""# NGC4183 Projection/Outer-Warp Formula Derivation

Status: `{summary.iloc[0]["formula_derivation_status"]}`

This is a formula-shell derivation only.  It does not freeze the coefficient and
does not authorize endpoint scoring.

## Summary

{markdown_table(summary)}

## Formula

{markdown_table(formulas)}

## Derivation Steps

{markdown_table(derivation_steps)}

## Kernel Grid Preview

{markdown_table(kernel_grid.head(12))}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Interpretation

The source-supported direction for NGC4183 is not a standalone added warp-ramp.
It is a projection-attenuation shell with an outer-warp caveat:

```text
K_proj(R) = p_edge * smoothstep((R/R_HI - x_inner) / (1 - x_inner))
v_readout^2(R) = v_carrier^2(R) * (1 - gamma_proj K_proj(R))
```

This shell is dimensionally consistent and has the right zero-overlay limits,
but it is not frozen because `gamma_proj` is not yet derived from source-side
evidence.  The qualitative outer-warp statement cannot be used as a numeric
added-source amplitude.
"""
    (REPORTS / "ngc4183_projection_outer_warp_formula_derivation.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
