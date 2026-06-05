#!/usr/bin/env python3
"""Freeze the NGC7331 split-B2 unit-load formula candidate.

This freeze candidate follows the q-role separation and conditional mu_load
derivation gates:

    Delta v^2 = sigma_warp * x_w * Vflat^2 * ramp(R/R_HI; x_w)

It reads no observed velocities or residuals. Because the branch was selected
after the negative exact-transfer interval audit, it is not an accepted NGC7331
endpoint freeze. It is a diagnostic/theory-candidate freeze that can be used to
define a future predeclared holdout or independent-galaxy protocol.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
FORMULA_ID = "NGC7331_SPLIT_B2_UNIT_LOAD_FREEZE_DIAGNOSTIC_V1"
CLAIM_BOUNDARY = "ngc7331_b2_split_unit_load_formula_freeze_diagnostic_not_endpoint"


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

    exact_freeze = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_formula_freeze_manifest.csv"
    ).iloc[0]
    mu_summary = pd.read_csv(DATA / "ngc7331_b2_mu_load_derivation_summary.csv").iloc[0]
    split_summary = pd.read_csv(
        DATA / "ngc7331_b2_split_q_source_load_summary.csv"
    ).iloc[0]
    q_review = pd.read_csv(
        DATA / "ngc7331_qwarp_source_only_review_response_summary.csv"
    ).iloc[0]
    points_source = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_points.csv",
        usecols=["r", "vn"],
    )

    x_w = float(exact_freeze["x_w_formula_freeze"])
    vflat = float(exact_freeze["vflat_km_s"])
    r_hi = float(exact_freeze["rhi_kpc"])
    sigma_warp = 1.0
    mu_load = float(mu_summary["mu_load_protocol_value"])
    source_scale = x_w * vflat**2
    lambda_split = sigma_warp * mu_load * source_scale
    turn_on_power = 1.0

    r = points_source["r"].astype(float)
    carrier = points_source["vn"].astype(float)
    x = r / r_hi
    ramp = np.maximum(0.0, (x - x_w) / (1.0 - x_w)) ** turn_on_power
    delta_v2 = lambda_split * ramp
    v_split = np.sqrt(np.maximum(carrier**2 + delta_v2, 0.0))

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": FORMULA_ID,
                "readout_family": "K_warp_history_split_b2_unit_load",
                "parent_failed_formula_id": str(exact_freeze["formula_id"]),
                "branch_origin": str(split_summary["split_gate_status"]),
                "mu_load_origin": str(mu_summary["mu_load_derivation_status"]),
                "carrier": "v_Newtonian_baryonic",
                "formula_text": (
                    "v_readout^2(R)=v_Newtonian_baryonic^2(R)+"
                    "sigma_warp*mu_load*x_w*Vflat^2*ramp(R/R_HI;x_w)"
                ),
                "delta_text": (
                    "Delta v^2_split(R)=sigma_warp*mu_load*x_w*Vflat^2*"
                    "max(0,(R/R_HI-x_w)/(1-x_w))"
                ),
                "kernel_text": "K_shape=ramp=max(0,(x-x_w)/(1-x_w))",
                "source_load_text": "mu_load=1 conditional normalized split-load coordinate",
                "q_shape_handling": (
                    "q_shape interval is carried as morphology evidence and is "
                    "not multiplied into both amplitude and kernel"
                ),
                "q_shape_interval": str(q_review["q_warp_interval"]),
                "x_w_formula_freeze": x_w,
                "rhi_kpc": r_hi,
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
                    "PASS: R/R_HI<=x_w implies ramp=0 and carrier recovery"
                ),
                "zero_source_limit": (
                    "PASS: sigma_warp=0 or mu_load=0 gives Delta v^2=0"
                ),
                "ngc4088_recovery_limit": (
                    "recovers the original NGC4088 protocol when q_shape=1 and mu_load=1"
                ),
                "selection_caveat": (
                    "branch identified after NGC7331 exact-transfer failure; "
                    "not an accepted endpoint freeze for this same scored curve"
                ),
                "uses_vobs_or_residual_in_construction": False,
                "formula_frozen_before_endpoint_scoring": False,
                "endpoint_scores_allowed": False,
                "future_predeclared_protocol_candidate": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    kernel_grid = pd.DataFrame(
        {
            "galaxy": GALAXY,
            "formula_id": FORMULA_ID,
            "r_kpc": r,
            "x_R_over_RHI": x,
            "carrier_velocity_km_s": carrier,
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
                "gate_id": "SPLITB2F1_PARENT_FAILURE_LOCALIZED",
                "gate_status": "PASS",
                "evidence": str(split_summary["split_gate_status"]),
                "remaining_obligation": "none for diagnostic freeze candidate",
            },
            {
                "gate_id": "SPLITB2F2_MU_LOAD_CONDITIONAL",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": str(mu_summary["mu_load_derivation_status"]),
                "remaining_obligation": (
                    "derive final Tau-side source-load origin or acquire accepted "
                    "residual-blind load observable"
                ),
            },
            {
                "gate_id": "SPLITB2F3_DIMENSIONS_LIMITS",
                "gate_status": "PASS",
                "evidence": "velocity-squared units and inactive/zero-source limits pass",
                "remaining_obligation": "none at dimensional/protocol level",
            },
            {
                "gate_id": "SPLITB2F4_ENDPOINT_BLIND_CONSTRUCTION",
                "gate_status": "PASS",
                "evidence": "grid uses r and vn only; no vobs/residual columns",
                "remaining_obligation": "none for construction blindness",
            },
            {
                "gate_id": "SPLITB2F5_SAME_CURVE_ENDPOINT_ELIGIBILITY",
                "gate_status": "BLOCKED_POST_FAILURE_BRANCH",
                "evidence": "branch selected after exact B2 failure audit on NGC7331",
                "remaining_obligation": (
                    "use only as diagnostic or predeclare for independent holdout/population test"
                ),
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["formula_id"] = FORMULA_ID
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual_in_construction"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": FORMULA_ID,
                "formula_freeze_status": (
                    "NGC7331_SPLIT_B2_UNIT_LOAD_FORMULA_FREEZE_DIAGNOSTIC_READY_NOT_ENDPOINT"
                ),
                "lambda_split_km2_s2": lambda_split,
                "x_w_formula_freeze": x_w,
                "vflat_km_s": vflat,
                "mu_load": mu_load,
                "n_kernel_grid_rows": len(kernel_grid),
                "n_gates": len(gates),
                "n_pass": int(gates["gate_status"].eq("PASS").sum()),
                "n_formula_conditional": int(
                    gates["gate_status"].eq("FORMULA_CONDITIONAL").sum()
                ),
                "n_blocked": int(
                    gates["gate_status"].eq("BLOCKED_POST_FAILURE_BRANCH").sum()
                ),
                "uses_vobs_or_residual_in_construction": False,
                "formula_frozen_before_endpoint_scoring": False,
                "endpoint_scores_allowed": False,
                "future_predeclared_protocol_candidate": True,
                "claim_status": (
                    "diagnostic formula-freeze candidate only; not an accepted "
                    "NGC7331 endpoint because branch selection followed the failure audit"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ngc7331_b2_split_unit_load_formula_freeze_manifest.csv", index=False)
    kernel_grid.to_csv(
        DATA / "ngc7331_b2_split_unit_load_formula_freeze_kernel_grid.csv", index=False
    )
    gates.to_csv(DATA / "ngc7331_b2_split_unit_load_formula_freeze_gate.csv", index=False)
    summary.to_csv(
        DATA / "ngc7331_b2_split_unit_load_formula_freeze_summary.csv", index=False
    )

    report = [
        "# NGC7331 split-B2 unit-load formula-freeze candidate",
        "",
        "This freezes the split-B2 unit-load branch as a diagnostic/theory",
        "candidate without reading observed velocities. It is not an accepted",
        "same-curve endpoint because the branch was identified after the",
        "NGC7331 exact-transfer failure audit.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Interpretation",
        "",
        "The freeze candidate repairs the q-role conflation by carrying the",
        "`q_shape` interval as morphology evidence and using the conditional",
        "normalized split-load coordinate `mu_load=1`. The resulting branch may",
        "be used for future predeclared holdout/population tests, but on NGC7331",
        "it remains diagnostic because its selection followed a failed transfer",
        "audit.",
        "",
    ]
    (REPORTS / "ngc7331_b2_split_unit_load_formula_freeze_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
