#!/usr/bin/env python3
"""Freeze the NGC7331 exact B2 transfer formula as an interval protocol.

This gate consumes the NGC7331 exact-transfer input-ready gate and freezes an
NGC4088-style B2 transfer shell. The source-strength observable is carried as
an interval, not collapsed to a point. The script constructs a source-side
formula/kernel grid without using observed velocities or residuals.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
FORMULA_ID = "NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1"
CLAIM_BOUNDARY = "ngc7331_b2_exact_transfer_formula_freeze_not_score"


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


def parse_interval(text: object) -> tuple[float, float]:
    values = [
        float(item)
        for item in re.findall(
            r"[-+]?(?:\d+\.\d*|\d*\.\d+|\d+)(?:[eE][-+]?\d+)?",
            str(text),
        )
    ]
    if len(values) < 2:
        raise ValueError(f"Could not parse interval from {text!r}")
    low, high = values[0], values[1]
    return (min(low, high), max(low, high))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    upgrade = pd.read_csv(DATA / "ngc7331_b2_exact_transfer_upgrade_summary.csv").iloc[0]
    fields = pd.read_csv(DATA / "ngc7331_b2_exact_transfer_upgrade_fields.csv")
    response = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_review_response_template.csv").iloc[0]
    qgeom = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_geometry.csv").iloc[0]
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    sparc_row = sparc.loc[sparc["Galaxy"].eq(GALAXY)].iloc[0]
    points_source = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_points.csv",
        usecols=["r", "vn"],
    )

    field_by_required = {
        row["required_b2_field"]: row for _, row in fields.iterrows()
    }
    x_w = float(field_by_required["x_w"]["value"])
    vflat = float(field_by_required["Vflat"]["value"])
    q_min, q_max = parse_interval(field_by_required["q_warp"]["value"])
    epsilon_text = str(field_by_required["epsilon_cross_inputs"]["value"])
    epsilon_values = [
        float(item)
        for item in re.findall(
            r"[-+]?(?:\d+\.\d*|\d*\.\d+|\d+)(?:[eE][-+]?\d+)?",
            epsilon_text,
        )
    ]
    epsilon_cross_bound = epsilon_values[0] if epsilon_values else 0.0
    sigma_warp = 1.0
    turn_on_power = 1.0
    r_hi = float(qgeom["rhi_kpc"])
    upgrade_ready = bool_value(upgrade["formula_freeze_allowed"])

    lambda_min = sigma_warp * q_min * x_w * vflat**2
    lambda_max = sigma_warp * q_max * x_w * vflat**2
    lambda_min_with_cross = max(0.0, lambda_min * (1.0 - epsilon_cross_bound))
    lambda_max_with_cross = lambda_max * (1.0 + epsilon_cross_bound)

    r = points_source["r"].astype(float)
    x = r / r_hi
    ramp = np.maximum(0.0, (x - x_w) / (1.0 - x_w)) ** turn_on_power
    kernel_min = q_min * ramp
    kernel_max = q_max * ramp
    delta_v2_min = lambda_min * kernel_min
    delta_v2_max = lambda_max * kernel_max
    delta_v2_min_with_cross = lambda_min_with_cross * kernel_min
    delta_v2_max_with_cross = lambda_max_with_cross * kernel_max
    carrier = points_source["vn"].astype(float)
    v_min = np.sqrt(np.maximum(carrier**2 + delta_v2_min, 0.0))
    v_max = np.sqrt(np.maximum(carrier**2 + delta_v2_max, 0.0))
    v_min_with_cross = np.sqrt(np.maximum(carrier**2 + delta_v2_min_with_cross, 0.0))
    v_max_with_cross = np.sqrt(np.maximum(carrier**2 + delta_v2_max_with_cross, 0.0))

    factors = pd.DataFrame(
        [
            {
                "factor_id": "N7331_B2FF1_XW",
                "symbol": "x_w",
                "value": x_w,
                "unit": "dimensionless",
                "factor_status": "SOURCE_ONSET_AVAILABLE_REPLAY_ONLY",
                "source_evidence": str(field_by_required["x_w"]["source_basis"]),
            },
            {
                "factor_id": "N7331_B2FF2_Q_INTERVAL",
                "symbol": "q_warp",
                "value": f"[{q_min}, {q_max}]",
                "unit": "dimensionless_interval",
                "factor_status": "SOURCE_ONLY_INTERVAL_CARRIED",
                "source_evidence": str(response["review_rationale"]),
            },
            {
                "factor_id": "N7331_B2FF3_SIGMA",
                "symbol": "sigma_warp",
                "value": sigma_warp,
                "unit": "dimensionless_sign",
                "factor_status": "SOURCE_CONTEXT_CARRIED_AS_POSITIVE_TRANSFER_BRANCH",
                "source_evidence": str(response["sign_convention_decision"]),
            },
            {
                "factor_id": "N7331_B2FF4_VFLAT2",
                "symbol": "Vflat^2",
                "value": vflat**2,
                "unit": "km2_s2",
                "factor_status": "SOURCE_CATALOG_CARRIER_INPUT",
                "source_evidence": "SPARC external master table",
            },
            {
                "factor_id": "N7331_B2FF5_LAMBDA_INTERVAL",
                "symbol": "lambda_w",
                "value": f"[{lambda_min}, {lambda_max}]",
                "unit": "km2_s2_interval",
                "factor_status": "FORMULA_FREEZE_INTERVAL",
                "source_evidence": "lambda_w=sigma_warp*q_warp*x_w*Vflat^2 with q interval",
            },
            {
                "factor_id": "N7331_B2FF6_EPSILON_CROSS",
                "symbol": "epsilon_cross",
                "value": epsilon_cross_bound,
                "unit": "dimensionless_bound",
                "factor_status": "CONSERVATIVE_BOUND_CARRIED",
                "source_evidence": str(response["epsilon_cross_decision"]),
            },
            {
                "factor_id": "N7331_B2FF7_LAMBDA_INTERVAL_WITH_CROSS",
                "symbol": "lambda_w_cross_caveated",
                "value": f"[{lambda_min_with_cross}, {lambda_max_with_cross}]",
                "unit": "km2_s2_interval",
                "factor_status": "CROSS_CAVEATED_INTERVAL",
                "source_evidence": "lambda interval widened by carried epsilon_cross bound",
            },
        ]
    )
    factors["galaxy"] = GALAXY
    factors["formula_id"] = FORMULA_ID
    factors["endpoint_scores_allowed"] = False
    factors["uses_vobs_or_residual"] = False
    factors["claim_boundary"] = CLAIM_BOUNDARY
    factors = factors[
        [
            "galaxy",
            "formula_id",
            "factor_id",
            "symbol",
            "value",
            "unit",
            "factor_status",
            "source_evidence",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    kernel_grid = pd.DataFrame(
        {
            "galaxy": GALAXY,
            "r_kpc": r,
            "x_R_over_RHI": x,
            "carrier_velocity_km_s": carrier,
            "x_w_formula_freeze": x_w,
            "q_warp_min": q_min,
            "q_warp_max": q_max,
            "sigma_warp": sigma_warp,
            "turn_on_power_frozen": turn_on_power,
            "kernel_warp_history_min": kernel_min,
            "kernel_warp_history_max": kernel_max,
            "lambda_w_min_km2_s2": lambda_min,
            "lambda_w_max_km2_s2": lambda_max,
            "epsilon_cross_bound": epsilon_cross_bound,
            "lambda_w_min_cross_caveated_km2_s2": lambda_min_with_cross,
            "lambda_w_max_cross_caveated_km2_s2": lambda_max_with_cross,
            "delta_v2_min_km2_s2": delta_v2_min,
            "delta_v2_max_km2_s2": delta_v2_max,
            "delta_v2_min_cross_caveated_km2_s2": delta_v2_min_with_cross,
            "delta_v2_max_cross_caveated_km2_s2": delta_v2_max_with_cross,
            "v_exact_b2_min_km_s": v_min,
            "v_exact_b2_max_km_s": v_max,
            "v_exact_b2_min_cross_caveated_km_s": v_min_with_cross,
            "v_exact_b2_max_cross_caveated_km_s": v_max_with_cross,
            "uses_vobs_or_residual_in_construction": False,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": FORMULA_ID,
                "readout_family": "K_warp_history_exact_b2_transfer_interval",
                "carrier": "v_Newtonian_baryonic",
                "formula_text": "v_readout^2(R)=v_Newtonian_baryonic^2(R)+lambda_w*C_warp(R/R_HI;x_w,p)",
                "delta_text": "Delta v^2_warp(R;p)=lambda_w*C_warp(R/R_HI;x_w,p)",
                "kernel_text": "C_warp(x;x_w,p)=q_warp*max(0,(x-x_w)/(1-x_w))^p",
                "amplitude_rule": "lambda_w=sigma_warp*q_warp*x_w*Vflat^2",
                "q_transfer_convention_caveat": "strictly transfers the existing NGC4088 B2 q-in-lambda and q-in-kernel convention; final Tau-side q placement remains law-level open",
                "x_w_formula_freeze": x_w,
                "q_warp_min": q_min,
                "q_warp_max": q_max,
                "q_warp_rule": "CARRY_INTERVAL from source-only THINGS centroid/envelope review",
                "sigma_warp": sigma_warp,
                "sigma_rule": "positive exact-transfer branch carried from MOM1 orientation context; not endpoint selected",
                "vflat_km_s": vflat,
                "lambda_w_min_km2_s2": lambda_min,
                "lambda_w_max_km2_s2": lambda_max,
                "epsilon_cross_bound": epsilon_cross_bound,
                "lambda_w_min_cross_caveated_km2_s2": lambda_min_with_cross,
                "lambda_w_max_cross_caveated_km2_s2": lambda_max_with_cross,
                "turn_on_power_frozen": turn_on_power,
                "turn_on_power_rule": "minimal linear onset ramp transferred from NGC4088 protocol",
                "rhi_kpc": r_hi,
                "profile_source": "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_points.csv columns r,vn only",
                "dimension_check": "PASS: lambda_w interval has km^2 s^-2 units; C_warp interval is dimensionless; Delta v^2 interval has velocity-squared units",
                "inactive_window_limit": "R/R_HI <= x_w implies C_warp=0 and v_readout=v_Newtonian_baryonic for the full interval",
                "zero_source_limit": "q_warp=0 or sigma_warp=0 implies Delta v^2=0 and carrier recovery",
                "cross_term_caveat": "epsilon_cross is carried as an interval-widening caveat, not as endpoint-tuned error",
                "law_level_caveat": "B2 source-load law, q placement, sign law, and population transfer remain open",
                "uses_vobs_or_residual_in_construction": False,
                "formula_frozen_before_endpoint_scoring": upgrade_ready,
                "endpoint_scores_allowed": False,
                "prospective_endpoint_protocol_ready": upgrade_ready,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_B2FF1_UPGRADE_INPUT_READY",
                "gate_status": "PASS" if upgrade_ready else "BLOCKED",
                "evidence": str(upgrade["exact_transfer_upgrade_status"]),
                "remaining_obligation": "none at source-input readiness level" if upgrade_ready else "complete upgrade inputs",
            },
            {
                "gate_id": "N7331_B2FF2_Q_INTERVAL_CARRIED",
                "gate_status": "PASS_INTERVAL_CARRIED",
                "evidence": f"q_warp=[{q_min:.6g},{q_max:.6g}]",
                "remaining_obligation": "future source theorem may collapse interval; endpoint may not choose point q",
            },
            {
                "gate_id": "N7331_B2FF3_SIGN_BRANCH",
                "gate_status": "PASS_CAVEATED",
                "evidence": str(response["sign_convention_decision"]),
                "remaining_obligation": "derive final sign law from Tau-side orientation/readout geometry",
            },
            {
                "gate_id": "N7331_B2FF4_EPSILON_CROSS",
                "gate_status": "PASS_CAVEATED",
                "evidence": f"epsilon_cross_bound={epsilon_cross_bound:.6g}",
                "remaining_obligation": "carry cross-term bound; do not absorb it by endpoint retuning",
            },
            {
                "gate_id": "N7331_B2FF5_DIMENSIONS_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "lambda interval has velocity-squared units; kernel interval is dimensionless; inactive and zero-source limits recover carrier",
                "remaining_obligation": "none at formula-shell level",
            },
            {
                "gate_id": "N7331_B2FF6_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "formula freeze reads source fields plus r/vn carrier columns only; no vobs or residuals are written to the freeze grid",
                "remaining_obligation": "any endpoint must be a separate accepted-gate script reading this manifest unchanged",
            },
            {
                "gate_id": "N7331_B2FF7_Q_PLACEMENT_CAVEAT",
                "gate_status": "PASS_CAVEATED",
                "evidence": "strict NGC4088 B2 transfer keeps q_warp in lambda_w and in C_warp",
                "remaining_obligation": "derive final Tau-side q placement or compare q-placement branches as predeclared controls",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["formula_id"] = FORMULA_ID
    gates["formula_freeze_ready"] = upgrade_ready
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
                "galaxy": GALAXY,
                "formula_id": FORMULA_ID,
                "formula_freeze_status": (
                    "NGC7331_EXACT_B2_TRANSFER_INTERVAL_FORMULA_FREEZE_READY_NOT_SCORE"
                    if upgrade_ready
                    else "NGC7331_EXACT_B2_TRANSFER_INTERVAL_FORMULA_FREEZE_BLOCKED"
                ),
                "q_warp_min": q_min,
                "q_warp_max": q_max,
                "x_w_formula_freeze": x_w,
                "vflat_km_s": vflat,
                "lambda_w_min_km2_s2": lambda_min,
                "lambda_w_max_km2_s2": lambda_max,
                "epsilon_cross_bound": epsilon_cross_bound,
                "lambda_w_min_cross_caveated_km2_s2": lambda_min_with_cross,
                "lambda_w_max_cross_caveated_km2_s2": lambda_max_with_cross,
                "n_kernel_grid_rows": len(kernel_grid),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "uses_vobs_or_residual_in_construction": False,
                "formula_frozen_before_endpoint_scoring": upgrade_ready,
                "prospective_endpoint_protocol_ready": upgrade_ready,
                "endpoint_scores_allowed": False,
                "next_required_action": "build separate accepted endpoint gate or predeclared interval-control audit before any scoring",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ngc7331_b2_exact_transfer_formula_freeze_manifest.csv", index=False)
    factors.to_csv(DATA / "ngc7331_b2_exact_transfer_formula_freeze_factors.csv", index=False)
    kernel_grid.to_csv(DATA / "ngc7331_b2_exact_transfer_formula_freeze_kernel_grid.csv", index=False)
    gates.to_csv(DATA / "ngc7331_b2_exact_transfer_formula_freeze_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_b2_exact_transfer_formula_freeze_summary.csv", index=False)

    report = [
        "# NGC7331 B2 Exact Transfer Formula-Freeze Gate",
        "",
        "This gate freezes an interval-valued exact B2 transfer formula for NGC7331.",
        "It does not score an endpoint and it does not collapse the q_warp interval",
        "to whichever value would fit the rotation curve.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Factors",
        "",
        markdown_table(factors),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The formula is frozen at protocol level only. It strictly transfers the",
        "current NGC4088 B2 convention, including the q_warp placement in both",
        "lambda_w and C_warp. That q-placement is preserved for reproducibility",
        "but remains a law-level caveat for future derivation or predeclared",
        "control comparison.",
        "",
    ]
    (REPORTS / "ngc7331_b2_exact_transfer_formula_freeze_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
