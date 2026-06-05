#!/usr/bin/env python3
"""Build the NGC5907 mixed accepted-endpoint gate.

This promotes the already frozen NGC5907 exponential-disk + projection mixed
formula to score-eligible endpoint status without reading endpoint residuals.
The prior projection endpoint is explicitly not used as mixed-readout evidence.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_not_score"


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

    freeze_manifest = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_manifest.csv"
    ).iloc[0]
    freeze_summary = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_summary.csv"
    ).iloc[0]
    freeze_gate = pd.read_csv(DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_gate.csv")

    source_rule_ready = bool(freeze_summary["source_rule_candidate"])
    freeze_ready = (
        str(freeze_summary["formula_freeze_status"])
        == "MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING"
    )
    endpoint_blind = not bool(freeze_summary["uses_vobs_or_residual_in_construction"])
    previous_projection_not_evidence = not bool(
        freeze_summary["previous_projection_endpoint_used_as_mixed_evidence"]
    )
    no_blocked = int(freeze_summary["n_blocked"]) == 0
    formula_frozen = bool(freeze_manifest["formula_frozen_before_mixed_scoring"])
    score_allowed = bool(
        source_rule_ready
        and freeze_ready
        and endpoint_blind
        and previous_projection_not_evidence
        and no_blocked
        and formula_frozen
    )

    manifest = freeze_manifest.copy()
    manifest["accepted_endpoint_formula_id"] = manifest["formula_id"]
    manifest["formula_frozen_before_endpoint_scoring"] = True
    manifest["endpoint_scores_allowed"] = score_allowed
    manifest["posthoc_retuning_allowed"] = False
    manifest["accepted_endpoint_freeze_status"] = (
        "ACCEPTED_MIXED_ENDPOINT_FREEZE_READY"
        if score_allowed
        else "ACCEPTED_MIXED_ENDPOINT_FREEZE_BLOCKED"
    )
    manifest["claim_boundary"] = CLAIM_BOUNDARY
    manifest = manifest.to_frame().T

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N5907_MAEG1_SOURCE_RULE_READY",
                "gate_status": "PASS" if source_rule_ready else "BLOCKED",
                "evidence": str(freeze_manifest["mixed_readout_candidate"]),
                "remaining_obligation": "none for this single-galaxy mixed endpoint gate",
            },
            {
                "gate_id": "N5907_MAEG2_FORMULA_FROZEN_BEFORE_SCORING",
                "gate_status": "PASS" if freeze_ready and formula_frozen else "BLOCKED",
                "evidence": str(freeze_summary["formula_freeze_status"]),
                "remaining_obligation": "scoring script must read this manifest unchanged",
            },
            {
                "gate_id": "N5907_MAEG3_ENDPOINT_BLIND_CONSTRUCTION",
                "gate_status": "PASS" if endpoint_blind else "BLOCKED",
                "evidence": "freeze construction uses source queue and frozen projection manifest only",
                "remaining_obligation": "vobs may enter only in the separate endpoint scoring script",
            },
            {
                "gate_id": "N5907_MAEG4_PRIOR_PROJECTION_NOT_MIXED_EVIDENCE",
                "gate_status": "PASS_CAVEATED" if previous_projection_not_evidence else "BLOCKED",
                "evidence": "previous_projection_endpoint_used_as_mixed_evidence=False",
                "remaining_obligation": (
                    "preserve this caveat: prior projection endpoint is control context, "
                    "not mixed-label evidence"
                ),
            },
            {
                "gate_id": "N5907_MAEG5_NO_BLOCKED_FREEZE_GATES",
                "gate_status": "PASS" if no_blocked else "BLOCKED",
                "evidence": f"n_blocked={int(freeze_summary['n_blocked'])}",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "N5907_MAEG6_NO_RETUNING_RULE",
                "gate_status": "PASS",
                "evidence": "posthoc_retuning_allowed=False; sign, carrier, kernel, amplitude, and window are frozen",
                "remaining_obligation": "any post-score formula change demotes this row to diagnostic",
            },
        ]
    )
    gates["galaxy"] = "NGC5907"
    gates["formula_id"] = str(freeze_manifest["formula_id"])
    gates["endpoint_scores_allowed"] = score_allowed
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "formula_id",
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
                "formula_id": str(freeze_manifest["formula_id"]),
                "accepted_endpoint_freeze_status": (
                    "ACCEPTED_MIXED_ENDPOINT_FREEZE_READY"
                    if score_allowed
                    else "ACCEPTED_MIXED_ENDPOINT_FREEZE_BLOCKED"
                ),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "source_rule_candidate": source_rule_ready,
                "formula_frozen_before_endpoint_scoring": formula_frozen,
                "previous_projection_endpoint_used_as_mixed_evidence": False,
                "endpoint_scores_allowed": score_allowed,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_manifest.csv",
        index=False,
    )
    gates.to_csv(DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_gate.csv", index=False)
    summary.to_csv(
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_gate_summary.csv",
        index=False,
    )

    report = [
        "# NGC5907 Exponential-Disk + Projection Mixed Accepted Endpoint Gate",
        "",
        "This gate promotes the frozen NGC5907 mixed readout protocol to a",
        "single-galaxy accepted endpoint gate. It does not score the curve.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Frozen Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Formula-Freeze Gate Input",
        "",
        markdown_table(freeze_gate),
        "",
        "## Claim Boundary",
        "",
        "The earlier NGC5907 projection endpoint is not counted as evidence for",
        "the mixed readout label. It is control context only. Endpoint scoring",
        "must be run by a separate script that reads this accepted manifest",
        "unchanged.",
        "",
    ]
    (REPORTS / "ngc5907_expdisk_projection_mixed_accepted_endpoint_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
