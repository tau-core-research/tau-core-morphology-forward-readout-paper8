#!/usr/bin/env python3
"""Build the NGC5907 projection accepted-endpoint freeze gate.

This gate promotes the already source-field accepted NGC5907 projection lane
from diagnostic-only formula inspection to an endpoint-score-eligible frozen
protocol. It still does not score the rotation curve. Scoring is performed by a
separate script after the formula, sign, amplitude rule, and source window are
frozen.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc5907_projection_accepted_endpoint_freeze_gate_not_score"


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

    freeze = pd.read_csv(DATA / "ngc5907_projection_freeze_summary.csv").iloc[0]
    audit = pd.read_csv(DATA / "readout_subfamily_accepted_manifest_audit.csv")
    audit_row = audit.loc[audit["galaxy"] == "NGC5907"].iloc[0]

    accepted_label = bool(audit_row["accepted_subfamily_label_promoted"])
    source_status_ok = (
        str(audit_row["audit_decision"])
        == "ACCEPTED_SUBFAMILY_SOURCE_FIELDS_ENDPOINT_STILL_BLOCKED"
    )
    freeze_ready = (
        str(freeze["projection_freeze_status"])
        == "PROJECTION_PROTOCOL_BOUND_READY_NOT_ENDPOINT"
    )
    n_blocked = int(freeze["n_blocked"])
    pi_projection = float(freeze["frozen_projection_bound"])
    h_over_r = float(freeze["thickness_h_over_rs"])
    gamma_projection = 0.5 * pi_projection * h_over_r

    manifest = pd.DataFrame(
        [
            {
                "galaxy": "NGC5907",
                "accepted_readout_subfamily": "K_projection_dominated",
                "formula_id": "NGC5907_PROJECTION_ATTENUATION_V1",
                "formula_text": "v_proj^2(R)=v_TPG^2(R)*(1-gamma_proj*K_proj(R))",
                "kernel_text": "K_proj=smoothstep((R-r_in)/(r_out-r_in))*(1+truncation_contrast*smoothstep((R-r_in)/(r_out-r_in)))/(1+truncation_contrast)",
                "sign_rule": "attenuation_not_added_gravity",
                "amplitude_rule": "gamma_proj=0.5*Pi_projection*h_over_r",
                "baseline_carrier": "v_TPG",
                "r_in_kpc": float(freeze["warp_r_inner_kpc"]),
                "r_out_kpc": float(freeze["warp_r_outer_kpc"]),
                "truncation_contrast": float(freeze["truncation_contrast"]),
                "pi_projection": pi_projection,
                "h_over_r": h_over_r,
                "gamma_projection": gamma_projection,
                "formula_frozen_before_endpoint_scoring": True,
                "uses_vobs_or_residual_in_construction": False,
                "posthoc_retuning_allowed": False,
                "endpoint_scores_allowed": bool(
                    accepted_label and source_status_ok and freeze_ready and n_blocked == 0
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "AEG1_ACCEPTED_SOURCE_SUBFAMILY",
                "gate_status": "PASS" if accepted_label and source_status_ok else "BLOCKED",
                "evidence": str(audit_row["audit_decision"]),
                "remaining_obligation": "none for NGC5907 source-field endpoint eligibility",
            },
            {
                "gate_id": "AEG2_SOURCE_FROZEN_PROJECTION_PROTOCOL",
                "gate_status": "PASS" if freeze_ready and n_blocked == 0 else "BLOCKED",
                "evidence": str(freeze["projection_freeze_status"]),
                "remaining_obligation": "none; scoring must use this frozen protocol unchanged",
            },
            {
                "gate_id": "AEG3_FORMULA_FREEZE_BEFORE_SCORING",
                "gate_status": "PASS",
                "evidence": "formula/sign/amplitude/window are written in the freeze manifest before endpoint scoring",
                "remaining_obligation": "future endpoint runs must read this manifest, not infer formula from v_obs",
            },
            {
                "gate_id": "AEG4_ENDPOINT_BLIND_CONSTRUCTION",
                "gate_status": "PASS",
                "evidence": "construction inputs are source fields, direct kernel observables, and the predeclared TPG carrier",
                "remaining_obligation": "v_obs may be read only by the separate scoring script",
            },
            {
                "gate_id": "AEG5_NO_RETUNING_RULE",
                "gate_status": "PASS",
                "evidence": "posthoc_retuning_allowed=False; amplitude is gamma_proj=0.5*Pi_projection*h_over_r",
                "remaining_obligation": "changing sign, amplitude, carrier, or window after scoring demotes the row to diagnostic",
            },
        ]
    )
    gates["galaxy"] = "NGC5907"
    gates["endpoint_scores_allowed"] = bool(manifest["endpoint_scores_allowed"].iloc[0])
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
                "galaxy": "NGC5907",
                "accepted_readout_subfamily": "K_projection_dominated",
                "n_gates": len(gates),
                "n_pass": int(gates["gate_status"].eq("PASS").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "formula_id": str(manifest["formula_id"].iloc[0]),
                "gamma_projection": gamma_projection,
                "endpoint_scores_allowed": bool(manifest["endpoint_scores_allowed"].iloc[0]),
                "accepted_endpoint_freeze_status": (
                    "ACCEPTED_ENDPOINT_FREEZE_READY"
                    if bool(manifest["endpoint_scores_allowed"].iloc[0])
                    else "ACCEPTED_ENDPOINT_FREEZE_BLOCKED"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ngc5907_projection_accepted_endpoint_manifest.csv", index=False)
    gates.to_csv(DATA / "ngc5907_projection_accepted_endpoint_gate.csv", index=False)
    summary.to_csv(DATA / "ngc5907_projection_accepted_endpoint_summary.csv", index=False)

    report = [
        "# NGC5907 Projection Accepted-Endpoint Freeze Gate",
        "",
        "This gate is not a rotation score. It freezes the projection-dominated",
        "readout formula before endpoint scoring and records that the construction",
        "does not use observed rotation residuals.",
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
        "If the formula sign, amplitude rule, carrier, or radial window is changed",
        "after seeing endpoint scores, the row must be demoted back to diagnostic.",
        "",
    ]
    (REPORTS / "ngc5907_projection_accepted_endpoint_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
