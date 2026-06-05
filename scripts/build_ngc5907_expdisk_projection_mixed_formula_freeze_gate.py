#!/usr/bin/env python3
"""Freeze the NGC5907 mixed exponential-disk + projection formula.

This gate consumes the residual-blind mixed candidate queue and the already
frozen NGC5907 projection protocol. It freezes a fresh mixed formula before
any mixed-readout scoring. The prior projection endpoint is not used as
mixed-readout evidence.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc5907_expdisk_projection_mixed_formula_freeze_not_score"


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

    queue = pd.read_csv(DATA / "mixed_readout_candidate_acquisition_queue.csv")
    candidate = queue.loc[queue["galaxy"].eq("NGC5907")].iloc[0]
    projection_manifest = pd.read_csv(
        DATA / "ngc5907_projection_accepted_endpoint_manifest.csv"
    ).iloc[0]
    projection_freeze = pd.read_csv(DATA / "ngc5907_projection_freeze_summary.csv").iloc[0]

    source_rule_candidate = bool(candidate["source_rule_candidate"])
    uses_vobs = False
    projection_formula_ready = bool(projection_manifest["formula_frozen_before_endpoint_scoring"])
    previous_projection_endpoint_caveat = True

    manifest = pd.DataFrame(
        [
            {
                "galaxy": "NGC5907",
                "formula_id": "NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1",
                "mixed_readout_candidate": str(candidate["candidate_mixed_readout"]),
                "carrier": "v_K_exponential_disk",
                "overlay_formula_id": str(projection_manifest["formula_id"]),
                "formula_text": "v_mix^2(R)=v_K_exponential_disk^2(R)*(1-gamma_proj*K_proj(R))",
                "delta_text": "Delta v_mix^2(R)=-gamma_proj*K_proj(R)*v_K_exponential_disk^2(R)",
                "kernel_text": str(projection_manifest["kernel_text"]),
                "sign_rule": str(projection_manifest["sign_rule"]),
                "carrier_selection_rule": "smooth_exponential_disk_carrier_from_source_disk_truncation_scales_and_positive_disk_scale",
                "overlay_selection_rule": "source_windowed_projection_warp_vertical_overlay_from_NGC5907_projection_freeze",
                "amplitude_rule": str(projection_manifest["amplitude_rule"]),
                "r_in_kpc": float(projection_manifest["r_in_kpc"]),
                "r_out_kpc": float(projection_manifest["r_out_kpc"]),
                "truncation_contrast": float(projection_manifest["truncation_contrast"]),
                "pi_projection": float(projection_manifest["pi_projection"]),
                "h_over_r": float(projection_manifest["h_over_r"]),
                "gamma_projection": float(projection_manifest["gamma_projection"]),
                "disk_scale_kpc": float(candidate["disk_scale_kpc"]),
                "warp_displacement_kpc": float(projection_freeze["warp_displacement_kpc"]),
                "dimension_check": "PASS: gamma_proj and K_proj are dimensionless; correction has velocity-squared units",
                "inactive_window_limit": "K_proj=0 implies v_mix=v_K_exponential_disk",
                "zero_amplitude_limit": "gamma_proj=0 implies v_mix=v_K_exponential_disk",
                "projection_absent_limit": "source_rule_candidate=False blocks mixed formula use",
                "source_rule_candidate": source_rule_candidate,
                "uses_vobs_or_residual_in_construction": uses_vobs,
                "formula_frozen_before_mixed_scoring": True,
                "previous_projection_endpoint_used_as_mixed_evidence": False,
                "previous_projection_endpoint_caveat": previous_projection_endpoint_caveat,
                "mixed_endpoint_scores_allowed": False,
                "prospective_mixed_protocol_ready": bool(
                    source_rule_candidate and projection_formula_ready and not uses_vobs
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N5907_MXF1_QUEUE_SOURCE_RULE",
                "gate_status": "PASS" if source_rule_candidate else "BLOCKED",
                "evidence": str(candidate["candidate_priority"]),
                "remaining_obligation": "source rule supports formula-freeze candidate only; scoring remains separate",
            },
            {
                "gate_id": "N5907_MXF2_CARRIER_FREEZE",
                "gate_status": "PASS_CAVEATED",
                "evidence": f"carrier=v_K_exponential_disk; disk_scale_kpc={float(candidate['disk_scale_kpc']):.6g}; disk/truncation scales are source fields",
                "remaining_obligation": "future population use must apply the same carrier rule before mixed scoring",
            },
            {
                "gate_id": "N5907_MXF3_PROJECTION_KERNEL_REUSE",
                "gate_status": "PASS",
                "evidence": str(projection_manifest["formula_id"]),
                "remaining_obligation": "use the already frozen projection kernel unchanged",
            },
            {
                "gate_id": "N5907_MXF4_DIMENSION_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "dimensionless attenuation times velocity-squared carrier; K=0 and gamma=0 recover carrier",
                "remaining_obligation": "none at formula-shell level",
            },
            {
                "gate_id": "N5907_MXF5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "construction reads queue row and projection freeze manifest only; no vobs or residuals",
                "remaining_obligation": "mixed scoring, if run, must be a separate script reading this manifest unchanged",
            },
            {
                "gate_id": "N5907_MXF6_PRIOR_PROJECTION_ENDPOINT_CAVEAT",
                "gate_status": "PASS_CAVEATED",
                "evidence": "prior projection endpoint exists, but previous_projection_endpoint_used_as_mixed_evidence=False",
                "remaining_obligation": "do not count the earlier projection endpoint as mixed-readout validation",
            },
        ]
    )
    gates["galaxy"] = "NGC5907"
    gates["formula_id"] = "NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1"
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
                "galaxy": "NGC5907",
                "formula_id": "NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1",
                "mixed_readout_candidate": str(candidate["candidate_mixed_readout"]),
                "source_rule_candidate": source_rule_candidate,
                "projection_formula_frozen": projection_formula_ready,
                "uses_vobs_or_residual_in_construction": uses_vobs,
                "previous_projection_endpoint_used_as_mixed_evidence": False,
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "formula_freeze_status": "MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING",
                "mixed_endpoint_scores_allowed": False,
                "prospective_mixed_protocol_ready": bool(
                    manifest["prospective_mixed_protocol_ready"].iloc[0]
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_manifest.csv", index=False)
    gates.to_csv(DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_gate.csv", index=False)
    summary.to_csv(DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_summary.csv", index=False)

    report = [
        "# NGC5907 Exponential-Disk + Projection Mixed Formula Freeze Gate",
        "",
        "This gate freezes a fresh mixed readout formula for NGC5907. It does not",
        "score the mixed endpoint and it does not reuse the previous projection",
        "endpoint as mixed-readout evidence.",
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
        "The formula is ready as a prospective mixed protocol prior to mixed",
        "scoring. Because NGC5907 already has a projection endpoint, the earlier",
        "projection score is treated only as a caveat/control context, not as",
        "evidence for the mixed formula.",
        "",
    ]
    (REPORTS / "ngc5907_expdisk_projection_mixed_formula_freeze_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
