#!/usr/bin/env python3
"""Freeze the NGC7331 mixed exponential-disk + vertical/outer-warp formula.

This gate is residual-blind and caveated. It uses accepted vertical source
fields plus outer-warp context to freeze a prospective mixed formula before
any mixed-readout scoring. The outer-warp onset is not numerically extracted,
so the radial window is broad and source-scale anchored.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_not_score"


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

    caveat = pd.read_csv(DATA / "ngc7331_outer_warp_vertical_caveat_summary.csv").iloc[0]
    queue = pd.read_csv(DATA / "mixed_readout_candidate_acquisition_queue.csv")
    candidate = queue.loc[queue["galaxy"].eq("NGC7331")].iloc[0]

    formula_allowed = bool(caveat["formula_freeze_attempt_allowed"])
    uses_vobs = False
    rdisk = float(caveat["rdisk_kpc"])
    rhi = float(caveat["rhi_kpc"])
    intrinsic_h_over_rs = float(caveat["intrinsic_h_over_Rs_mid"])
    projected_hwhm_over_rs = float(caveat["projected_hwhm_over_Rs"])
    vertical_activation = float(caveat["vertical_activation_candidate"])
    gamma_vow = min(0.75, 0.5 * vertical_activation)

    manifest = pd.DataFrame(
        [
            {
                "galaxy": "NGC7331",
                "formula_id": "NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1",
                "mixed_readout_candidate": str(candidate["candidate_mixed_readout"]),
                "carrier": "v_K_exponential_disk",
                "formula_text": "v_mix^2(R)=v_K_exponential_disk^2(R)*(1-gamma_vow*K_vow(R))",
                "delta_text": "Delta v_mix^2(R)=-gamma_vow*K_vow(R)*v_K_exponential_disk^2(R)",
                "kernel_text": "K_vow(R)=W_outer(R;R_s,R_HI)*(0.5/(1+R/R_s)+0.5*projected_hwhm_over_Rs)",
                "sign_rule": "attenuation_not_added_gravity",
                "carrier_selection_rule": "smooth_exponential_disk_carrier_from_positive_SPARK_Rdisk_and_caveated_mixed_queue",
                "overlay_selection_rule": "accepted_vertical_scale_fields_plus_context_outer_warp_caveat",
                "amplitude_rule": "gamma_vow=min(0.75,0.5*vertical_activation_candidate)",
                "r_window_inner_kpc": rdisk,
                "r_window_outer_kpc": rhi,
                "intrinsic_h_over_Rs_mid": intrinsic_h_over_rs,
                "projected_hwhm_over_Rs": projected_hwhm_over_rs,
                "projected_hwhm_over_RHI": float(caveat["projected_hwhm_over_RHI"]),
                "vertical_activation_candidate": vertical_activation,
                "gamma_vow": gamma_vow,
                "outer_warp_numeric_onset_available": bool(caveat["outer_warp_numeric_onset_available"]),
                "outer_warp_context_present": bool(caveat["outer_warp_context_present"]),
                "dimension_check": "PASS: gamma_vow and K_vow are dimensionless; correction has velocity-squared units",
                "inactive_window_limit": "W_outer=0 implies v_mix=v_K_exponential_disk",
                "zero_amplitude_limit": "gamma_vow=0 implies v_mix=v_K_exponential_disk",
                "vertical_absent_limit": "vertical_activation_candidate=0 blocks the mixed overlay amplitude",
                "caveat_status": "CAVEATED_BROAD_OUTER_WINDOW_NO_NUMERIC_WARP_ONSET",
                "source_rule_candidate": bool(candidate["source_rule_candidate"]),
                "uses_vobs_or_residual_in_construction": uses_vobs,
                "formula_frozen_before_mixed_scoring": True,
                "mixed_endpoint_scores_allowed": False,
                "prospective_mixed_protocol_ready": bool(formula_allowed and not uses_vobs),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_MXF1_CAVEAT_GATE",
                "gate_status": "PASS_CAVEATED" if formula_allowed else "BLOCKED",
                "evidence": str(caveat["caveat_gate_status"]),
                "remaining_obligation": "numeric outer-warp onset still absent; broad source-scale window only",
            },
            {
                "gate_id": "N7331_MXF2_VERTICAL_AMPLITUDE_MAPPING",
                "gate_status": "PASS",
                "evidence": f"vertical_activation_candidate={vertical_activation:.6g}; gamma_vow={gamma_vow:.6g}",
                "remaining_obligation": "amplitude is source-rule candidate, not final Tau-side vertical law",
            },
            {
                "gate_id": "N7331_MXF3_BROAD_OUTER_WINDOW",
                "gate_status": "PASS_CAVEATED",
                "evidence": f"R_inner=Rdisk={rdisk:.6g} kpc; R_outer=RHI={rhi:.6g} kpc",
                "remaining_obligation": "replace with numeric HI/projection warp onset if extracted later",
            },
            {
                "gate_id": "N7331_MXF4_DIMENSION_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "dimensionless attenuation times velocity-squared carrier; inactive window and gamma=0 recover carrier",
                "remaining_obligation": "none at formula-shell level",
            },
            {
                "gate_id": "N7331_MXF5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "construction reads caveat summary, source queue, and SPARC scale metadata only; no vobs or residuals",
                "remaining_obligation": "mixed scoring, if run, must be a separate script reading this manifest unchanged",
            },
        ]
    )
    gates["galaxy"] = "NGC7331"
    gates["formula_id"] = "NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1"
    gates["mixed_endpoint_scores_allowed"] = False
    gates["prospective_mixed_protocol_ready"] = bool(
        manifest["prospective_mixed_protocol_ready"].iloc[0]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "formula_id",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "mixed_endpoint_scores_allowed",
            "prospective_mixed_protocol_ready",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC7331",
                "formula_id": "NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1",
                "mixed_readout_candidate": str(candidate["candidate_mixed_readout"]),
                "source_rule_candidate": bool(candidate["source_rule_candidate"]),
                "caveat_gate_allows_formula_freeze": formula_allowed,
                "uses_vobs_or_residual_in_construction": uses_vobs,
                "outer_warp_numeric_onset_available": bool(caveat["outer_warp_numeric_onset_available"]),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "formula_freeze_status": "CAVEATED_MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING",
                "mixed_endpoint_scores_allowed": False,
                "prospective_mixed_protocol_ready": bool(
                    manifest["prospective_mixed_protocol_ready"].iloc[0]
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_manifest.csv",
        index=False,
    )
    gates.to_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_summary.csv",
        index=False,
    )

    report = [
        "# NGC7331 Exponential-Disk + Vertical/Outer-Warp Mixed Formula Freeze Gate",
        "",
        "This gate freezes a caveated NGC7331 mixed formula before mixed scoring.",
        "It does not score the mixed endpoint. The broad outer window is used",
        "because the current source layer has outer-warp context but no numeric",
        "warp-onset radius.",
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
        "The formula is a prospective, caveated protocol. It is not an endpoint",
        "score and not proof that the mixed NGC7331 readout fits the observed",
        "rotation curve. A future numeric HI/projection warp-onset extraction",
        "should replace the broad Rdisk-to-RHI window.",
        "",
    ]
    (REPORTS / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
