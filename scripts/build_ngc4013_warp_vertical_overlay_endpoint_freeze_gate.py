#!/usr/bin/env python3
"""Build the NGC4013 warp/vertical-overlay endpoint-freeze gate.

This freezes the remaining source-side formula ingredients for the
warp/vertical-overlay readout shell. It still does not score the rotation curve:
NGC4013 remains endpoint-label blocked because the compact lane was rejected and
the replacement subfamily has not yet been promoted by an accepted morphology
manifest.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_warp_vertical_overlay_endpoint_freeze_gate_not_score"


def smoothstep(x: np.ndarray) -> np.ndarray:
    clipped = np.clip(x, 0.0, 1.0)
    return clipped * clipped * (3.0 - 2.0 * clipped)


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

    formula = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_formula_summary.csv").iloc[0]
    source = pd.read_csv(DATA / "ngc4013_compact_overlay_source_summary.csv").iloc[0]
    preflight = pd.read_csv(DATA / "ngc4013_warp_overlay_preflight_summary.csv").iloc[0]

    r_warp = float(preflight["warp_onset_kpc"])
    r25 = 11.2
    r_lag_start = 5.8
    r_lag_zero = r25
    lag_inner_value = -35.0
    r_outer = r25
    h_over_rs = float(source["s4g_edge_disk_h_over_r"])
    r_s_kpc = float(source["s4g_edge_disk_hr_kpc"])
    z_ec = float(source["extended_component_scaleheight_kpc"])
    gamma_upper = float(formula["gamma_overlay_upper"])

    weights = {
        "omega_z": 1.0 / 3.0,
        "omega_ec": 1.0 / 3.0,
        "omega_lag": 1.0 / 3.0,
    }

    r_grid = np.array(
        sorted(
            {
                0.0,
                r_lag_start,
                r_warp,
                r_outer,
                1.25 * r_outer,
                1.5 * r_outer,
                2.0 * r_outer,
            }
        )
    )
    w_warp = smoothstep((r_grid - r_warp) / max(r_outer - r_warp, 1.0e-9))
    k_z = 1.0 / (1.0 + r_grid / max(r_s_kpc, 1.0e-9))
    k_ec = 1.0 / (1.0 + r_grid / z_ec)
    k_lag = np.clip((r_lag_zero - r_grid) / max(r_lag_zero - r_lag_start, 1.0e-9), 0.0, 1.0)
    k_wvo = w_warp * (
        weights["omega_z"] * k_z
        + weights["omega_ec"] * k_ec
        + weights["omega_lag"] * k_lag
    )

    radial_kernel = pd.DataFrame(
        {
            "galaxy": "NGC4013",
            "r_kpc": r_grid,
            "W_warp": w_warp,
            "K_z": k_z,
            "K_EC": k_ec,
            "K_lag": k_lag,
            "K_wvo": k_wvo,
            "kernel_status": "SOURCE_FROZEN_KERNEL_GRID_NOT_ENDPOINT_SCORE",
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    manifest = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "formula_id": "NGC4013_WARP_VERTICAL_OVERLAY_V1",
                "readout_subfamily": "K_warp_vertical_overlay_candidate",
                "formula_text": "v_wvo^2(R)=v_TPG^2(R)*(1-Gamma_wvo*K_wvo(R))",
                "kernel_text": "K_wvo=W_warp*(omega_z*K_z+omega_EC*K_EC+omega_lag*K_lag)",
                "warp_window_text": "W_warp=smoothstep((R-R_w)/(R_o-R_w))",
                "K_z_text": "K_z=1/(1+R/R_s)",
                "K_EC_text": "K_EC=1/(1+R/z_EC)",
                "K_lag_text": "K_lag=clip((R25-R)/(R25-R_lag_start),0,1)",
                "sign_rule": "attenuation_not_added_gravity",
                "weight_rule": "uniform_over_three_source_supported_channels",
                "amplitude_rule": "Gamma_wvo <= 0.5*h_over_Rs + 0.5*f_EC",
                "r_warp_kpc": r_warp,
                "r_outer_kpc": r_outer,
                "r25_kpc": r25,
                "r_lag_start_kpc": r_lag_start,
                "r_lag_zero_kpc": r_lag_zero,
                "lag_inner_value_km_s_kpc": lag_inner_value,
                "r_s_kpc": r_s_kpc,
                "h_over_rs": h_over_rs,
                "z_ec_kpc": z_ec,
                "gamma_overlay_upper": gamma_upper,
                **weights,
                "uses_vobs_or_residual_in_construction": False,
                "formula_frozen_before_endpoint_scoring": True,
                "accepted_replacement_label_promoted": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4013_EFG1_FORMULA_SHELL_DERIVED",
                "gate_status": "PASS",
                "evidence": str(formula["derivation_status"]),
                "remaining_obligation": "none at formula-shell level",
            },
            {
                "gate_id": "N4013_EFG2_OUTER_WARP_WINDOW_FREEZE",
                "gate_status": "PASS_CAVEATED",
                "evidence": "source gives R25=11.2 kpc and line-of-sight warp onset near 10 kpc",
                "remaining_obligation": "independent review should verify whether R25 is acceptable as R_o",
            },
            {
                "gate_id": "N4013_EFG3_LAG_KERNEL_FREEZE",
                "gate_status": "PASS_CAVEATED",
                "evidence": "lag shallows from -35 km/s/kpc at 5.8 kpc to zero near R25",
                "remaining_obligation": "source figure digitization can later replace the linear lag-shell",
            },
            {
                "gate_id": "N4013_EFG4_WEIGHT_RULE_FREEZE",
                "gate_status": "PASS_CAVEATED",
                "evidence": "uniform weights are used because all three channels are source-supported and no residual-blind hierarchy is available",
                "remaining_obligation": "derive evidence-strength weights before promotion beyond caveated freeze",
            },
            {
                "gate_id": "N4013_EFG5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "construction uses source fields and the predeclared TPG carrier; vobs is forbidden",
                "remaining_obligation": "keep scoring in a separate script only after label promotion",
            },
            {
                "gate_id": "N4013_EFG6_REPLACEMENT_LABEL_PROMOTION",
                "gate_status": "BLOCKED",
                "evidence": "compact lane is rejected, but K_warp_vertical_overlay_candidate is not yet an accepted endpoint label",
                "remaining_obligation": "promote replacement label with an accepted morphology manifest before endpoint scoring",
            },
        ]
    )
    gates["galaxy"] = "NGC4013"
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "formula_id": "NGC4013_WARP_VERTICAL_OVERLAY_V1",
                "r_warp_kpc": r_warp,
                "r_outer_kpc": r_outer,
                "r_lag_start_kpc": r_lag_start,
                "r_lag_zero_kpc": r_lag_zero,
                "r_s_kpc": r_s_kpc,
                "gamma_overlay_upper": gamma_upper,
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "formula_freeze_status": "FORMULA_FREEZE_PROTOCOL_READY_LABEL_BLOCKED",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(
        DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_manifest.csv", index=False
    )
    gates.to_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_gate.csv", index=False)
    radial_kernel.to_csv(
        DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_kernel_grid.csv", index=False
    )
    summary.to_csv(
        DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_summary.csv", index=False
    )

    report = [
        "# NGC4013 Warp/Vertical-Overlay Endpoint-Freeze Gate",
        "",
        "This gate freezes the source-side formula ingredients for the replacement",
        "warp/vertical-overlay shell. It does not score the rotation curve because",
        "the replacement readout label is not yet accepted for endpoint use.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Frozen Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Kernel Grid",
        "",
        markdown_table(radial_kernel),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The formula ingredients are source-frozen at caveated protocol level. The",
        "row remains endpoint-label blocked: scoring before replacement-label",
        "promotion would demote the result to a diagnostic.",
        "",
    ]
    (REPORTS / "ngc4013_warp_vertical_overlay_endpoint_freeze_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
