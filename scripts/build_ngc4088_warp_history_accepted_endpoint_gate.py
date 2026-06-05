#!/usr/bin/env python3
"""Promote the frozen NGC4088 warp/history formula to endpoint-score eligibility.

This gate does not score the rotation curve.  It checks that the formula was
frozen before scoring, that construction is endpoint-blind, and that the
remaining B1/B2/B3 caveats are explicit.  Scoring is performed only by the
separate run_ngc4088_warp_history_accepted_endpoint.py script.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_warp_history_accepted_endpoint_gate_not_score"


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

    freeze = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_summary.csv").iloc[0]
    manifest_in = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_manifest.csv").iloc[0]
    dashboard = pd.read_csv(DATA / "ngc4088_formula_freeze_readiness_summary.csv").iloc[0]

    formula_ready = bool_value(freeze["formula_frozen_before_endpoint_scoring"])
    dashboard_ready = str(dashboard["readiness_decision"]) == "FORMULA_FREEZE_READY_ENDPOINT_GATE_REQUIRED"
    endpoint_blind = not bool_value(freeze["uses_vobs_or_residual_in_construction"])
    caveats_declared = bool_value(freeze["b2_law_level_open"]) and bool_value(
        freeze["b3_law_level_open"]
    )
    allowed = formula_ready and dashboard_ready and endpoint_blind and caveats_declared

    manifest = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "accepted_readout_subfamily": "K_warp_history_caveated_protocol",
                "formula_id": str(manifest_in["formula_id"]),
                "source_formula_freeze_manifest": "ngc4088_warp_history_formula_freeze_manifest.csv",
                "source_kernel_grid": "ngc4088_warp_history_formula_freeze_kernel_grid.csv",
                "formula_text": str(manifest_in["formula_text"]),
                "kernel_text": str(manifest_in["kernel_text"]),
                "amplitude_rule": str(manifest_in["amplitude_rule"]),
                "baseline_carrier": str(manifest_in["carrier"]),
                "x_w_formula_freeze": float(manifest_in["x_w_formula_freeze"]),
                "q_warp": float(manifest_in["q_warp"]),
                "sigma_warp": float(manifest_in["sigma_warp"]),
                "vflat_km_s": float(manifest_in["vflat_km_s"]),
                "lambda_w_km2_s2": float(manifest_in["lambda_w_km2_s2"]),
                "turn_on_power_frozen": float(manifest_in["turn_on_power_frozen"]),
                "formula_frozen_before_endpoint_scoring": formula_ready,
                "uses_vobs_or_residual_in_construction": False,
                "posthoc_retuning_allowed": False,
                "endpoint_scores_allowed": allowed,
                "caveat_b1": str(manifest_in["x_w_provenance_caveat"]),
                "caveat_b2": "physical-normalization law is formula-conditional, not final Tau-side law",
                "caveat_b3": "scale uniqueness is protocol-level, not law-level uniqueness",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4088_AEG1_FORMULA_FROZEN",
                "gate_status": "PASS" if formula_ready else "BLOCKED",
                "evidence": str(freeze["formula_freeze_status"]),
                "remaining_obligation": "none for endpoint scoring; law-level caveats remain",
            },
            {
                "gate_id": "N4088_AEG2_DASHBOARD_READY",
                "gate_status": "PASS" if dashboard_ready else "BLOCKED",
                "evidence": str(dashboard["readiness_decision"]),
                "remaining_obligation": "none if dashboard says endpoint gate required",
            },
            {
                "gate_id": "N4088_AEG3_ENDPOINT_BLIND_CONSTRUCTION",
                "gate_status": "PASS" if endpoint_blind else "BLOCKED",
                "evidence": "frozen manifest/kernel grid do not use vobs or residuals",
                "remaining_obligation": "scoring script may read vobs only after this gate",
            },
            {
                "gate_id": "N4088_AEG4_CAVEATS_DECLARED",
                "gate_status": "PASS_CAVEATED" if caveats_declared else "BLOCKED",
                "evidence": "B1 graphical WHISP caveat, B2 law-level open, B3 law-level open",
                "remaining_obligation": "claim must remain preliminary single-galaxy control",
            },
            {
                "gate_id": "N4088_AEG5_NO_RETUNING_RULE",
                "gate_status": "PASS",
                "evidence": "posthoc_retuning_allowed=False; p=1 and lambda_w are frozen before scoring",
                "remaining_obligation": "changing p, sign, carrier, x_w, or lambda after scoring demotes the row to diagnostic",
            },
        ]
    )
    gates["galaxy"] = "NGC4088"
    gates["endpoint_scores_allowed"] = allowed
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
                "galaxy": "NGC4088",
                "accepted_readout_subfamily": "K_warp_history_caveated_protocol",
                "formula_id": str(manifest["formula_id"].iloc[0]),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "lambda_w_km2_s2": float(manifest["lambda_w_km2_s2"].iloc[0]),
                "endpoint_scores_allowed": allowed,
                "accepted_endpoint_freeze_status": (
                    "CAVEATED_ACCEPTED_ENDPOINT_FREEZE_READY"
                    if allowed
                    else "ACCEPTED_ENDPOINT_FREEZE_BLOCKED"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ngc4088_warp_history_accepted_endpoint_manifest.csv", index=False)
    gates.to_csv(DATA / "ngc4088_warp_history_accepted_endpoint_gate.csv", index=False)
    summary.to_csv(
        DATA / "ngc4088_warp_history_accepted_endpoint_gate_summary.csv", index=False
    )

    report = [
        "# NGC4088 Warp/History Accepted Endpoint Gate",
        "",
        "This gate promotes the frozen NGC4088 warp/history formula to caveated",
        "single-galaxy endpoint-score eligibility. It does not score the curve.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Accepted Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "This is a caveated accepted endpoint gate. The next scoring script must",
        "read the frozen formula unchanged. The result may be reported only as a",
        "single-galaxy preliminary control endpoint, not as empirical validation.",
        "",
    ]
    (REPORTS / "ngc4088_warp_history_accepted_endpoint_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
