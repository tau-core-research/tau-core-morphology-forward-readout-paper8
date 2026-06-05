#!/usr/bin/env python3
"""Build the NGC7331 caveated mixed accepted-endpoint gate."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_gate_not_score"


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
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_manifest.csv"
    ).iloc[0]
    freeze_summary = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_summary.csv"
    ).iloc[0]
    freeze_gate = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_gate.csv"
    )

    source_rule_ready = bool(freeze_summary["source_rule_candidate"])
    freeze_ready = (
        str(freeze_summary["formula_freeze_status"])
        == "CAVEATED_MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING"
    )
    endpoint_blind = not bool(freeze_summary["uses_vobs_or_residual_in_construction"])
    broad_window_caveat_attached = not bool(freeze_summary["outer_warp_numeric_onset_available"])
    no_blocked = int(freeze_summary["n_blocked"]) == 0
    formula_frozen = bool(freeze_manifest["formula_frozen_before_mixed_scoring"])
    score_allowed = bool(
        source_rule_ready and freeze_ready and endpoint_blind and no_blocked and formula_frozen
    )

    manifest = freeze_manifest.copy()
    manifest["accepted_endpoint_formula_id"] = manifest["formula_id"]
    manifest["formula_frozen_before_endpoint_scoring"] = True
    manifest["endpoint_scores_allowed"] = score_allowed
    manifest["posthoc_retuning_allowed"] = False
    manifest["outer_warp_numeric_onset_available"] = False
    manifest["broad_outer_window_caveat_attached"] = broad_window_caveat_attached
    manifest["accepted_endpoint_freeze_status"] = (
        "CAVEATED_ACCEPTED_MIXED_ENDPOINT_FREEZE_READY"
        if score_allowed
        else "CAVEATED_ACCEPTED_MIXED_ENDPOINT_FREEZE_BLOCKED"
    )
    manifest["claim_boundary"] = CLAIM_BOUNDARY
    manifest = manifest.to_frame().T

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_MAEG1_SOURCE_RULE_READY",
                "gate_status": "PASS_CAVEATED" if source_rule_ready else "BLOCKED",
                "evidence": str(freeze_manifest["mixed_readout_candidate"]),
                "remaining_obligation": "source rule is caveated by broad outer-window status",
            },
            {
                "gate_id": "N7331_MAEG2_FORMULA_FROZEN_BEFORE_SCORING",
                "gate_status": "PASS" if freeze_ready and formula_frozen else "BLOCKED",
                "evidence": str(freeze_summary["formula_freeze_status"]),
                "remaining_obligation": "scoring script must read this manifest unchanged",
            },
            {
                "gate_id": "N7331_MAEG3_ENDPOINT_BLIND_CONSTRUCTION",
                "gate_status": "PASS" if endpoint_blind else "BLOCKED",
                "evidence": "freeze construction uses caveat summary, source queue, and SPARC scale metadata only",
                "remaining_obligation": "vobs may enter only in the separate endpoint scoring script",
            },
            {
                "gate_id": "N7331_MAEG4_BROAD_WINDOW_CAVEAT_ATTACHED",
                "gate_status": "PASS_CAVEATED" if broad_window_caveat_attached else "PASS",
                "evidence": "outer_warp_numeric_onset_available=False; broad Rdisk-to-RHI window remains attached",
                "remaining_obligation": "a future numeric HI/projection warp-onset extraction should replace the broad window",
            },
            {
                "gate_id": "N7331_MAEG5_NO_BLOCKED_FREEZE_GATES",
                "gate_status": "PASS" if no_blocked else "BLOCKED",
                "evidence": f"n_blocked={int(freeze_summary['n_blocked'])}",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "N7331_MAEG6_NO_RETUNING_RULE",
                "gate_status": "PASS",
                "evidence": "posthoc_retuning_allowed=False; sign, carrier, kernel, amplitude, and window are frozen",
                "remaining_obligation": "any post-score formula change demotes this row to diagnostic",
            },
        ]
    )
    gates["galaxy"] = "NGC7331"
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
                "galaxy": "NGC7331",
                "formula_id": str(freeze_manifest["formula_id"]),
                "accepted_endpoint_freeze_status": (
                    "CAVEATED_ACCEPTED_MIXED_ENDPOINT_FREEZE_READY"
                    if score_allowed
                    else "CAVEATED_ACCEPTED_MIXED_ENDPOINT_FREEZE_BLOCKED"
                ),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "source_rule_candidate": source_rule_ready,
                "formula_frozen_before_endpoint_scoring": formula_frozen,
                "outer_warp_numeric_onset_available": False,
                "broad_outer_window_caveat_attached": broad_window_caveat_attached,
                "endpoint_scores_allowed": score_allowed,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_manifest.csv",
        index=False,
    )
    gates.to_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_gate.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_gate_summary.csv",
        index=False,
    )

    report = [
        "# NGC7331 Exponential-Disk + Vertical/Outer-Warp Mixed Accepted Endpoint Gate",
        "",
        "This gate promotes the frozen NGC7331 mixed readout protocol to a",
        "caveated single-galaxy accepted endpoint gate. It does not score the",
        "curve and it preserves the broad outer-window caveat.",
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
        "The missing numeric outer-warp onset is not repaired here. This is an",
        "accepted caveated endpoint gate only because the caveat is explicit and",
        "the formula is frozen before scoring.",
        "",
    ]
    (
        REPORTS
        / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_gate.md"
    ).write_text("\n".join(report), encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
