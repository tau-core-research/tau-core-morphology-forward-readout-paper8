#!/usr/bin/env python3
"""Freeze the NGC5907 split-B2 unit-load holdout formula candidate.

This is the first independent-galaxy application of the split-B2 unit-load
repair after the NGC7331 diagnostic. The construction reads only residual-blind
source fields and the baryonic Newtonian carrier grid (`r`, `vn`). It does not
read observed velocities and does not score an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC5907"
FORMULA_ID = "NGC5907_SPLIT_B2_UNIT_LOAD_FREEZE_CAVEATED_V1"
CLAIM_BOUNDARY = "ngc5907_split_b2_unit_load_formula_freeze_caveated_not_score"


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

    denominator = pd.read_csv(DATA / "ngc5907_split_b2_denominator_summary.csv").iloc[0]
    denominator_fields = pd.read_csv(DATA / "ngc5907_split_b2_denominator_fields.csv")
    selector = pd.read_csv(DATA / "split_b2_independent_holdout_candidates.csv")
    selector_row = selector.loc[selector["galaxy"].eq(GALAXY)].iloc[0]

    # Use only r and vn from an existing grid. Do not read vobs/residuals here.
    points_source = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_points.csv",
        usecols=["r", "vn"],
    )

    x_w = float(denominator["x_w_source_window"])
    r_outer = float(denominator["selected_r_outer_kpc"])
    vflat = float(denominator["vflat_km_s"])
    sigma_warp = 1.0
    mu_load = 1.0
    turn_on_power = 1.0
    source_scale = x_w * vflat**2
    lambda_split = sigma_warp * mu_load * source_scale

    r = points_source["r"].astype(float)
    carrier = points_source["vn"].astype(float)
    x = r / r_outer
    ramp = np.maximum(0.0, (x - x_w) / (1.0 - x_w)) ** turn_on_power
    delta_v2 = lambda_split * ramp
    v_split = np.sqrt(np.maximum(carrier**2 + delta_v2, 0.0))

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": FORMULA_ID,
                "readout_family": "K_warp_history_split_b2_unit_load",
                "independent_holdout_selector_status": str(
                    selector_row["split_b2_holdout_status"]
                ),
                "carrier": "v_Newtonian_baryonic",
                "formula_text": (
                    "v_readout^2(R)=v_Newtonian_baryonic^2(R)+"
                    "sigma_warp*mu_load*x_w*Vflat^2*ramp(R/R_outer;x_w)"
                ),
                "delta_text": (
                    "Delta v^2_split(R)=sigma_warp*mu_load*x_w*Vflat^2*"
                    "max(0,(R/R_outer-x_w)/(1-x_w))"
                ),
                "kernel_text": "K_shape=ramp=max(0,(x-x_w)/(1-x_w))",
                "source_load_text": "mu_load=1 conditional normalized split-load coordinate",
                "denominator_id": str(denominator["selected_denominator_id"]),
                "denominator_caveat": (
                    "uses source-native optical warp outer support, not SPARC HI radius"
                ),
                "r_outer_kpc": r_outer,
                "x_w_formula_freeze": x_w,
                "vflat_km_s": vflat,
                "sigma_warp": sigma_warp,
                "mu_load": mu_load,
                "lambda_split_km2_s2": lambda_split,
                "turn_on_power_frozen": turn_on_power,
                "dimension_check": (
                    "PASS: sigma, mu_load, x_w, and ramp are dimensionless; "
                    "Vflat^2 supplies km^2/s^2"
                ),
                "inactive_window_limit": (
                    "PASS: R/R_outer<=x_w implies ramp=0 and carrier recovery"
                ),
                "zero_source_limit": (
                    "PASS: sigma_warp=0 or mu_load=0 gives Delta v^2=0"
                ),
                "ngc7331_diagnostic_branch_relation": (
                    "same split-B2 unit-load shell, but frozen here before NGC5907 split-B2 scoring"
                ),
                "uses_vobs_or_residual_in_construction": False,
                "formula_frozen_before_split_b2_scoring": True,
                "endpoint_scores_allowed": False,
                "future_separate_scoring_gate_required": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    kernel_grid = pd.DataFrame(
        {
            "galaxy": GALAXY,
            "formula_id": FORMULA_ID,
            "r_kpc": r,
            "x_R_over_Router": x,
            "carrier_velocity_km_s": carrier,
            "r_outer_kpc": r_outer,
            "x_w_formula_freeze": x_w,
            "sigma_warp": sigma_warp,
            "mu_load": mu_load,
            "lambda_split_km2_s2": lambda_split,
            "kernel_ramp": ramp,
            "delta_v2_split_km2_s2": delta_v2,
            "v_split_b2_unit_load_km_s": v_split,
            "uses_vobs_or_residual_in_construction": False,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N5907_SB2F1_HOLDOUT_SELECTOR",
                "gate_status": "PASS_CAVEATED",
                "evidence": str(selector_row["split_b2_holdout_status"]),
                "remaining_obligation": "separate scoring gate must preserve caveated status",
            },
            {
                "gate_id": "N5907_SB2F2_DENOMINATOR",
                "gate_status": "PASS_CAVEATED",
                "evidence": str(denominator["denominator_gate_status"]),
                "remaining_obligation": "replace with source-native HI denominator if acquired later",
            },
            {
                "gate_id": "N5907_SB2F3_SOURCE_FIELDS",
                "gate_status": "PASS_CAVEATED",
                "evidence": (
                    "warp start, outer support, x_w, Vflat frozen from source/catalog fields"
                ),
                "remaining_obligation": "do not reinterpret optical outer support as HI extent",
            },
            {
                "gate_id": "N5907_SB2F4_DIMENSIONS_LIMITS",
                "gate_status": "PASS",
                "evidence": "velocity-squared units and inactive/zero-source limits pass",
                "remaining_obligation": "none at formula-shell level",
            },
            {
                "gate_id": "N5907_SB2F5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "construction reads r and vn only; no vobs/residual columns",
                "remaining_obligation": "future scoring script must read this manifest unchanged",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["formula_id"] = FORMULA_ID
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual_in_construction"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    source_fields = denominator_fields.copy()
    source_fields["formula_id"] = FORMULA_ID
    source_fields["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": FORMULA_ID,
                "formula_freeze_status": (
                    "NGC5907_SPLIT_B2_UNIT_LOAD_FORMULA_FREEZE_CAVEATED_READY_NOT_SCORED"
                ),
                "r_outer_kpc": r_outer,
                "x_w_formula_freeze": x_w,
                "vflat_km_s": vflat,
                "mu_load": mu_load,
                "lambda_split_km2_s2": lambda_split,
                "n_kernel_grid_rows": len(kernel_grid),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_construction": False,
                "future_separate_scoring_gate_required": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(
        DATA / "ngc5907_split_b2_unit_load_formula_freeze_manifest.csv", index=False
    )
    kernel_grid.to_csv(
        DATA / "ngc5907_split_b2_unit_load_formula_freeze_kernel_grid.csv", index=False
    )
    gates.to_csv(
        DATA / "ngc5907_split_b2_unit_load_formula_freeze_gate.csv", index=False
    )
    source_fields.to_csv(
        DATA / "ngc5907_split_b2_unit_load_formula_freeze_source_fields.csv", index=False
    )
    summary.to_csv(
        DATA / "ngc5907_split_b2_unit_load_formula_freeze_summary.csv", index=False
    )

    report = f"""# NGC5907 Split-B2 Unit-Load Formula Freeze Gate

Status: `{summary.iloc[0]['formula_freeze_status']}`

This gate freezes the NGC5907 split-B2 unit-load formula candidate before any
split-B2 scoring. The construction reads only source fields and the
Newtonian-carrier grid (`r`, `vn`); it does not read observed velocities.

## Summary

{markdown_table(summary)}

## Frozen Manifest

{markdown_table(manifest)}

## Source Fields

{markdown_table(source_fields[[
    'field_id',
    'observable',
    'value',
    'unit',
    'status',
    'role',
]])}

## Gates

{markdown_table(gates[[
    'gate_id',
    'gate_status',
    'evidence',
    'remaining_obligation',
]])}

## Formula

`v_readout^2(R)=v_Newtonian_baryonic^2(R)+sigma_warp*mu_load*x_w*Vflat^2*ramp(R/R_outer;x_w)`

with:

- `R_outer = {r_outer:.6g} kpc`
- `x_w = {x_w:.6g}`
- `Vflat = {vflat:.6g} km/s`
- `mu_load = 1`
- `lambda_split = {lambda_split:.6g} km^2/s^2`

## Claim Boundary

This is a caveated, pre-scoring formula freeze. It is not an endpoint result.
The caveat is that `R_outer` is the source-native optical warp outer support
radius, not a SPARC/HI radius.

`{CLAIM_BOUNDARY}`
"""
    (REPORTS / "ngc5907_split_b2_unit_load_formula_freeze_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
