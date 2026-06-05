#!/usr/bin/env python3
"""Freeze the NGC4088 warp/history formula at protocol level.

This gate consumes the residual-blind B1/B2/B3 blocker ledgers and freezes the
first executable NGC4088 warp/history readout shell.  It deliberately preserves
the law-level caveats: B2 is still formula-conditional, and B3 is still
protocol-unique rather than a final Tau-side uniqueness theorem.  No observed
velocities or residuals are used to construct the manifest or kernel grid.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_warp_history_formula_freeze_protocol_not_score"


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


def bool_value(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    b1 = pd.read_csv(DATA / "ngc4088_b1_whisp_promotion_review_summary.csv").iloc[0]
    b2 = pd.read_csv(DATA / "ngc4088_b2_physical_normalization_synthesis_summary.csv").iloc[0]
    b2_formula = pd.read_csv(DATA / "ngc4088_b2_physical_normalization_formula_status.csv").iloc[0]
    b3 = pd.read_csv(DATA / "ngc4088_b3_scale_uniqueness_synthesis_summary.csv").iloc[0]
    scale_selection = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_selection_summary.csv"
    ).iloc[0]
    mapping = pd.read_csv(DATA / "s4g75_ngc4088_filled_warp_closure_mapping.csv").iloc[0]
    normalization = pd.read_csv(
        DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_summary.csv"
    ).iloc[0]
    profile = pd.read_csv(DATA / "s4g75_ngc4088_readout_preflight_profile.csv")

    x_w = float(b1["x_w_source_consistency_value"])
    first_pass_x_w = float(b1["first_pass_x_w"])
    vflat_km_s = float(normalization["vflat_km_s"])
    q_warp = float(mapping["known_source_strength_q_warp"])
    sigma_warp = 1.0
    turn_on_power = 1.0
    lambda_w = sigma_warp * q_warp * x_w * vflat_km_s**2

    b1_ready = bool_value(b1["accepted_x_w_for_formula_freeze"])
    b2_formula_conditional_ready = (
        str(b2["formula_quality"]) == "DIMENSIONALLY_VALID_RESIDUAL_BLIND_EXECUTABLE"
        and str(b2_formula["status"]) == "FORMULA_CONDITIONAL_NOT_FINAL_LAW"
    )
    b3_protocol_unique = bool_value(b3["conditional_uniqueness_resolved"]) and (
        str(b3["selected_scale_ids"]) == "CURRENT_XW_VFLAT2"
    )
    no_residual_inputs = not any(
        [
            bool_value(b1["uses_vobs_or_residual"]),
            bool_value(b2["uses_vobs_or_residual"]),
            bool_value(b3["uses_vobs_or_residual"]),
            bool_value(scale_selection["endpoint_scores_allowed"]),
        ]
    )
    formula_freeze_ready = (
        b1_ready and b2_formula_conditional_ready and b3_protocol_unique and no_residual_inputs
    )

    x = profile["x_R_over_RHI"].astype(float)
    kernel = q_warp * np.maximum(0.0, (x - x_w) / (1.0 - x_w)) ** turn_on_power
    delta_v2 = lambda_w * kernel
    v_carrier = profile["vn"].astype(float)
    v_freeze = np.sqrt(np.maximum(v_carrier**2 + delta_v2, 0.0))

    # Do not copy vobs into this construction grid; endpoint scoring must be separate.
    kernel_grid = pd.DataFrame(
        {
            "galaxy": "NGC4088",
            "split": profile["split"],
            "r_kpc": profile["r"].astype(float),
            "x_R_over_RHI": x,
            "carrier_velocity_km_s": v_carrier,
            "x_w_formula_freeze": x_w,
            "q_warp": q_warp,
            "sigma_warp": sigma_warp,
            "turn_on_power_frozen": turn_on_power,
            "kernel_warp_history": kernel,
            "lambda_w_km2_s2": lambda_w,
            "delta_v2_warp_history_km2_s2": delta_v2,
            "v_warp_history_formula_freeze_km_s": v_freeze,
            "uses_vobs_or_residual_in_construction": False,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    manifest = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "formula_id": "NGC4088_WARP_HISTORY_FREEZE_V1",
                "readout_family": "K_warp_history",
                "carrier": "v_Newtonian_baryonic",
                "formula_text": "v_readout^2(R)=v_Newtonian_baryonic^2(R)+lambda_w*C_warp(R/R_HI;x_w,p)",
                "delta_text": "Delta v^2_warp(R;p)=lambda_w*C_warp(R/R_HI;x_w,p)",
                "kernel_text": "C_warp(x;x_w,p)=q_warp*max(0,(x-x_w)/(1-x_w))^p",
                "amplitude_rule": "lambda_w=sigma_warp*q_warp*x_w*Vflat^2",
                "x_w_formula_freeze": x_w,
                "x_w_first_pass": first_pass_x_w,
                "x_w_source": "WHISP graphical-overview frozen extraction, caveated",
                "x_w_provenance_caveat": "accepted for formula freeze from residual-blind WHISP graphical overview; direct source-coordinate H I/FITS product remains uncached",
                "q_warp": q_warp,
                "q_warp_source": "source-response review / filled warp closure mapping",
                "sigma_warp": sigma_warp,
                "sigma_rule": "positive outer warp/history added-readout sign frozen from source-side orientation protocol",
                "vflat_km_s": vflat_km_s,
                "lambda_w_km2_s2": lambda_w,
                "turn_on_power_frozen": turn_on_power,
                "turn_on_power_rule": "minimal linear onset ramp is the predeclared formula-freeze branch",
                "turn_on_power_sensitivity_control": "p=2 remains a sensitivity/control branch only, not the endpoint formula",
                "selected_scale_id": str(b3["selected_scale_ids"]),
                "selection_principle": str(b3["selection_principle"]),
                "dimension_check": "PASS: lambda_w has km^2 s^-2 units; C_warp is dimensionless; Delta v^2 has velocity-squared units",
                "inactive_window_limit": "R/R_HI <= x_w implies C_warp=0 and v_readout=v_Newtonian_baryonic",
                "zero_source_limit": "q_warp=0 or sigma_warp=0 implies Delta v^2=0 and carrier recovery",
                "law_level_caveat": "B2 physical-normalization law and B3 law-level uniqueness remain open; this is a protocol formula freeze",
                "b1_formula_freeze_status": str(b1["b1_resolution_status"]),
                "b2_protocol_status": "B2_PROTOCOL_FORMULA_FREEZE_READY_LAW_LEVEL_OPEN"
                if b2_formula_conditional_ready
                else "B2_PROTOCOL_BLOCKED",
                "b3_protocol_status": "B3_PROTOCOL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_OPEN"
                if b3_protocol_unique
                else "B3_PROTOCOL_BLOCKED",
                "uses_vobs_or_residual_in_construction": False,
                "formula_frozen_before_endpoint_scoring": formula_freeze_ready,
                "endpoint_scores_allowed": False,
                "prospective_endpoint_protocol_ready": formula_freeze_ready,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gate_rows = [
        {
            "gate_id": "N4088_FF1_B1_XW_FREEZE",
            "gate_status": "PASS_CAVEATED" if b1_ready else "BLOCKED",
            "evidence": f"x_w={x_w:.6g}; {b1['promotion_review_status']}",
            "remaining_obligation": "cache direct source-coordinate H I/FITS product when available; carry WHISP graphical-overview caveat",
        },
        {
            "gate_id": "N4088_FF2_B2_DIMENSIONAL_FORMULA",
            "gate_status": "PASS_CAVEATED" if b2_formula_conditional_ready else "BLOCKED",
            "evidence": f"{b2['formula_quality']}; {b2_formula['status']}; lambda_w recomputed from caveated x_w",
            "remaining_obligation": "derive final Tau-side physical-normalization law; do not claim law-level validation",
        },
        {
            "gate_id": "N4088_FF3_B3_PROTOCOL_SCALE_UNIQUENESS",
            "gate_status": "PASS_CAVEATED" if b3_protocol_unique else "BLOCKED",
            "evidence": f"selected_scale_id={b3['selected_scale_ids']}; conditional_uniqueness_resolved={b3['conditional_uniqueness_resolved']}",
            "remaining_obligation": "law-level uniqueness still depends on B2 closure/asymptotic-carrier derivation",
        },
        {
            "gate_id": "N4088_FF4_BRANCH_FREEZE",
            "gate_status": "PASS_CAVEATED",
            "evidence": "p=1 selected by minimal linear onset ramp; p=2 retained only as sensitivity control",
            "remaining_obligation": "future endpoint/control scripts must not choose p from residuals",
        },
        {
            "gate_id": "N4088_FF5_DIMENSIONS_AND_LIMITS",
            "gate_status": "PASS",
            "evidence": "dimensionless kernel times lambda_w[km^2/s^2]; inactive-window and zero-source carrier limits pass",
            "remaining_obligation": "none at formula-shell level",
        },
        {
            "gate_id": "N4088_FF6_ENDPOINT_BLINDNESS",
            "gate_status": "PASS" if no_residual_inputs else "BLOCKED",
            "evidence": "manifest and kernel grid are built from source ledgers and preflight carrier columns; vobs is not copied into the freeze grid",
            "remaining_obligation": "accepted endpoint gate and scoring must be separate and read this manifest unchanged",
        },
    ]
    gates = pd.DataFrame(gate_rows)
    gates["galaxy"] = "NGC4088"
    gates["formula_id"] = "NGC4088_WARP_HISTORY_FREEZE_V1"
    gates["formula_freeze_ready"] = formula_freeze_ready
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual_in_construction"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "formula_id",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "formula_freeze_ready",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual_in_construction",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "formula_id": "NGC4088_WARP_HISTORY_FREEZE_V1",
                "formula_freeze_status": (
                    "NGC4088_WARP_HISTORY_FORMULA_FREEZE_READY_LAW_CAVEATED_NOT_SCORE"
                    if formula_freeze_ready
                    else "NGC4088_WARP_HISTORY_FORMULA_FREEZE_BLOCKED"
                ),
                "b1_status": str(b1["b1_resolution_status"]),
                "b2_protocol_status": manifest["b2_protocol_status"].iloc[0],
                "b3_protocol_status": manifest["b3_protocol_status"].iloc[0],
                "b2_law_level_open": True,
                "b3_law_level_open": True,
                "x_w_formula_freeze": x_w,
                "vflat_km_s": vflat_km_s,
                "q_warp": q_warp,
                "sigma_warp": sigma_warp,
                "turn_on_power_frozen": turn_on_power,
                "lambda_w_km2_s2": lambda_w,
                "n_kernel_grid_rows": len(kernel_grid),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "uses_vobs_or_residual_in_construction": False,
                "formula_frozen_before_endpoint_scoring": formula_freeze_ready,
                "prospective_endpoint_protocol_ready": formula_freeze_ready,
                "endpoint_scores_allowed": False,
                "next_required_action": "build a separate accepted endpoint gate before any scoring; preserve B1/B2/B3 law/provenance caveats",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ngc4088_warp_history_formula_freeze_manifest.csv", index=False)
    kernel_grid.to_csv(
        DATA / "ngc4088_warp_history_formula_freeze_kernel_grid.csv", index=False
    )
    gates.to_csv(DATA / "ngc4088_warp_history_formula_freeze_gate.csv", index=False)
    summary.to_csv(DATA / "ngc4088_warp_history_formula_freeze_summary.csv", index=False)

    report = [
        "# NGC4088 Warp/History Formula-Freeze Gate",
        "",
        "This gate freezes the NGC4088 warp/history formula at protocol level. It",
        "does not score an endpoint and it does not claim a final Tau-side",
        "physical-normalization law.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Frozen Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Kernel Preview",
        "",
        markdown_table(kernel_grid.head(12)),
        "",
        "## Claim Boundary",
        "",
        "The formula is frozen before endpoint scoring as a prospective NGC4088",
        "warp/history protocol. B1 is caveated by the WHISP graphical-overview",
        "source, B2 remains formula-conditional rather than law-derived, and B3 is",
        "protocol-unique rather than law-level unique. Any endpoint score must be",
        "run by a separate accepted endpoint script that reads this manifest",
        "unchanged.",
        "",
    ]
    (REPORTS / "ngc4088_warp_history_formula_freeze_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
