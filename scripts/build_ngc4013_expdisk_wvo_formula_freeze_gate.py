#!/usr/bin/env python3
"""Freeze the NGC4013 mixed exponential-disk + WVO formula.

This gate consumes the residual-blind mixed source-selection rule and the
already frozen warp/vertical-overlay kernel. It freezes the mixed formula
without reading observed velocities. Because the mixed lane was explored after
an NGC4013 wrong-family diagnostic, this gate does not retroactively convert
the existing diagnostic score into an accepted endpoint result.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_expdisk_wvo_formula_freeze_not_retroactive_endpoint"


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

    source_cases = pd.read_csv(DATA / "mixed_readout_source_selection_cases.csv")
    source_case = source_cases.loc[source_cases["galaxy"].eq("NGC4013")].iloc[0]
    source_rule_pass = bool(source_case["source_rule_pass"])

    wvo_manifest = pd.read_csv(
        DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_manifest.csv"
    ).iloc[0]
    wvo_kernel = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_kernel_grid.csv")

    formula_frozen = bool(wvo_manifest["formula_frozen_before_endpoint_scoring"])
    uses_vobs = False
    gamma_upper = float(wvo_manifest["gamma_overlay_upper"])

    manifest = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "formula_id": "NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1",
                "mixed_readout_candidate": "K_expdisk_warp_vertical_overlay",
                "carrier": "v_K_exponential_disk",
                "overlay_formula_id": str(wvo_manifest["formula_id"]),
                "formula_text": "v_mix^2(R)=v_K_exponential_disk^2(R)*(1-Gamma_wvo*K_wvo(R))",
                "delta_text": "Delta v_mix^2(R)=-Gamma_wvo*K_wvo(R)*v_K_exponential_disk^2(R)",
                "kernel_text": str(wvo_manifest["kernel_text"]),
                "sign_rule": "attenuation_not_added_gravity",
                "carrier_selection_rule": str(source_case["carrier_rule"]),
                "overlay_selection_rule": str(source_case["overlay_rule"]),
                "amplitude_rule": str(wvo_manifest["amplitude_rule"]),
                "gamma_overlay_upper": gamma_upper,
                "r_warp_kpc": float(wvo_manifest["r_warp_kpc"]),
                "r_outer_kpc": float(wvo_manifest["r_outer_kpc"]),
                "r_lag_start_kpc": float(wvo_manifest["r_lag_start_kpc"]),
                "r_lag_zero_kpc": float(wvo_manifest["r_lag_zero_kpc"]),
                "r_s_kpc": float(wvo_manifest["r_s_kpc"]),
                "z_ec_kpc": float(wvo_manifest["z_ec_kpc"]),
                "omega_z": float(wvo_manifest["omega_z"]),
                "omega_ec": float(wvo_manifest["omega_ec"]),
                "omega_lag": float(wvo_manifest["omega_lag"]),
                "dimension_check": "PASS: Gamma_wvo and K_wvo are dimensionless; correction has velocity-squared units",
                "inactive_window_limit": "K_wvo=0 implies v_mix=v_K_exponential_disk",
                "zero_amplitude_limit": "Gamma_wvo=0 implies v_mix=v_K_exponential_disk",
                "overlay_absent_limit": "source_rule_pass=False or overlay_modifier_gate=False blocks mixed formula",
                "uses_vobs_or_residual_in_construction": uses_vobs,
                "formula_frozen_before_scoring": True,
                "retrospective_endpoint_scores_allowed": False,
                "prospective_endpoint_protocol_ready": bool(source_rule_pass and formula_frozen),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "MXF1_GENERAL_MIXED_SOURCE_RULE",
                "gate_status": "PASS" if source_rule_pass else "BLOCKED",
                "evidence": str(source_case["case_status"]),
                "remaining_obligation": "none for source-rule selection; formula gate still needed",
            },
            {
                "gate_id": "MXF2_CARRIER_FREEZE",
                "gate_status": "PASS_CAVEATED",
                "evidence": "carrier is v_K_exponential_disk selected by the mixed source rule from disk component plus disk scale",
                "remaining_obligation": "future sample-level use should apply the same carrier rule before scoring",
            },
            {
                "gate_id": "MXF3_OVERLAY_KERNEL_REUSE",
                "gate_status": "PASS",
                "evidence": str(wvo_manifest["formula_id"]),
                "remaining_obligation": "none; use the already frozen WVO kernel unchanged",
            },
            {
                "gate_id": "MXF4_DIMENSION_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "dimensionless attenuation times velocity-squared carrier; K=0 and Gamma=0 recover carrier",
                "remaining_obligation": "none at formula-shell level",
            },
            {
                "gate_id": "MXF5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "manifest construction reads source-rule fields and WVO freeze manifest only; no vobs",
                "remaining_obligation": "scoring must remain in a separate script",
            },
            {
                "gate_id": "MXF6_RETROACTIVE_ENDPOINT_STATUS",
                "gate_status": "BLOCKED_RETROACTIVE_ENDPOINT",
                "evidence": "NGC4013 mixed branch was previously inspected diagnostically after wrong-family controls",
                "remaining_obligation": "use as prospective/preregistered formula protocol, not as retroactive accepted endpoint validation",
            },
        ]
    )
    gates["galaxy"] = "NGC4013"
    gates["formula_id"] = "NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1"
    gates["retrospective_endpoint_scores_allowed"] = False
    gates["prospective_endpoint_protocol_ready"] = bool(source_rule_pass and formula_frozen)
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "formula_id",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "retrospective_endpoint_scores_allowed",
            "prospective_endpoint_protocol_ready",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "formula_id": "NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1",
                "mixed_readout_candidate": "K_expdisk_warp_vertical_overlay",
                "source_rule_pass": bool(source_rule_pass),
                "overlay_formula_frozen": bool(formula_frozen),
                "uses_vobs_or_residual_in_construction": uses_vobs,
                "n_kernel_grid_rows": len(wvo_kernel),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_retrospective_blockers": int(
                    gates["gate_status"].str.contains("BLOCKED_RETROACTIVE").sum()
                ),
                "formula_freeze_status": "MIXED_FORMULA_FREEZE_READY_NOT_RETROACTIVE_ENDPOINT",
                "retrospective_endpoint_scores_allowed": False,
                "prospective_endpoint_protocol_ready": bool(source_rule_pass and formula_frozen),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_manifest.csv", index=False)
    gates.to_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_gate.csv", index=False)
    summary.to_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_summary.csv", index=False)

    report = [
        "# NGC4013 Exponential-Disk + WVO Mixed Formula Freeze Gate",
        "",
        "This gate freezes the mixed formula selected by the residual-blind mixed",
        "source rule. It does not read observed velocities and does not convert the",
        "existing diagnostic score into an accepted endpoint.",
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
        "## Claim Boundary",
        "",
        "The formula is now suitable as a prospective/preregistered mixed-readout",
        "protocol. The already inspected NGC4013 diagnostic score remains",
        "diagnostic evidence, not a retroactive accepted endpoint validation.",
        "",
    ]
    (REPORTS / "ngc4013_expdisk_wvo_formula_freeze_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
