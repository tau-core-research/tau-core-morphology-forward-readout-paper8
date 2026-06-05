#!/usr/bin/env python3
"""Build the NGC4088 readout promotion gate.

This gate asks whether the NGC4088 source-filled warp/asymmetry readout lane can
be promoted from formula-development/preflight status to an endpoint-authorized
4D readout law.  It does not compute endpoint scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc4088_readout_promotion_gate_not_endpoint"


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


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame]:
    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    filled = pd.read_csv(DATA / "s4g75_ngc4088_filled_warp_closure_profile.csv")
    constants = pd.read_csv(DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_constants.csv")
    norm = pd.read_csv(DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_profile.csv")
    preflight = pd.read_csv(DATA / "s4g75_ngc4088_readout_preflight_profile.csv")

    p1 = norm.loc[norm["turn_on_power_control"] == 1.0].sort_values("x_R_over_RHI")
    p2 = norm.loc[norm["turn_on_power_control"] == 2.0].sort_values("x_R_over_RHI")
    basis_ok = (
        (filled["filled_basis_value"] >= -1.0e-12).all()
        and (filled["filled_basis_value"] <= filled["q_warp"] + 1.0e-12).all()
    )
    monotone_ok = (
        p1["delta_v2_warp_candidate"].diff().fillna(0.0).ge(-1.0e-12).all()
        and p2["delta_v2_warp_candidate"].diff().fillna(0.0).ge(-1.0e-12).all()
    )
    inner_zero_ok = (
        norm.loc[
            norm["x_R_over_RHI"] <= norm["filled_x_warp_onset"] + 1.0e-12,
            "delta_v2_warp_candidate",
        ]
        .le(1.0e-12)
        .all()
    )
    units_ok = {
        row["constant_name"]: row["unit"] for _, row in constants.iterrows()
    }["velocity_scale_candidate"] == "km2_s2"

    gates = pd.DataFrame(
        [
            {
                "gate_id": "SOURCE_ONSET_READY",
                "gate_status": "PASS" if bool(xw["accepted_for_mapping_rule"]) else "BLOCKED",
                "evidence": "x_w conversion audit accepted for mapping rule",
                "required_next_action": "independent digitization review before endpoint use",
                "endpoint_authorizing": False,
            },
            {
                "gate_id": "DIMENSIONAL_CARRIER_READY",
                "gate_status": "PASS" if units_ok else "BLOCKED",
                "evidence": "velocity scale is explicitly stored as km2_s2",
                "required_next_action": "derive why this carrier is the physical Tau-side readout scale",
                "endpoint_authorizing": False,
            },
            {
                "gate_id": "SOURCE_BASIS_SANITY",
                "gate_status": "PASS" if basis_ok and monotone_ok and inner_zero_ok else "BLOCKED",
                "evidence": "basis is zero before onset, nonnegative, bounded by q_warp, and monotone after onset",
                "required_next_action": "stress under uncertainty and independent digitization",
                "endpoint_authorizing": False,
            },
            {
                "gate_id": "RESIDUAL_BLIND_GENERATION",
                "gate_status": "PASS" if not preflight["uses_vobs_for_generation"].any() else "BLOCKED",
                "evidence": "candidate profile generation does not use observed velocity",
                "required_next_action": "keep observed columns contextual until a predeclared endpoint is launched",
                "endpoint_authorizing": False,
            },
            {
                "gate_id": "ENDPOINT_SCORE_GUARD",
                "gate_status": (
                    "PASS"
                    if not preflight["endpoint_scores_allowed"].any()
                    and not preflight["endpoint_scores_computed"].any()
                    else "BLOCKED"
                ),
                "evidence": "preflight profile exports no endpoint score",
                "required_next_action": "launch endpoint only through a separate frozen endpoint protocol",
                "endpoint_authorizing": False,
            },
            {
                "gate_id": "INDEPENDENT_DIGITIZATION_REVIEW",
                "gate_status": "BLOCKED",
                "evidence": "current x_w comes from a first-pass manual digitization response",
                "required_next_action": "obtain independent residual-blind review or frozen image-analysis repeat",
                "endpoint_authorizing": False,
            },
            {
                "gate_id": "PHYSICAL_NORMALIZATION_LAW",
                "gate_status": "BLOCKED",
                "evidence": "normalization prefactor is theory-conditional, not derived as final Tau-side law",
                "required_next_action": "derive or predeclare the accepted mapping from closure-source basis to delta v^2",
                "endpoint_authorizing": False,
            },
            {
                "gate_id": "POPULATION_GENERALIZATION",
                "gate_status": "BLOCKED",
                "evidence": "only NGC4088 has this source-filled warp/asymmetry lane",
                "required_next_action": "repeat on a predeclared source-rich sample before population claims",
                "endpoint_authorizing": False,
            },
        ]
    )
    gates["galaxy"] = "NGC4088"
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "required_next_action",
            "endpoint_authorizing",
            "claim_boundary",
        ]
    ]

    blocked = gates.loc[gates["gate_status"] == "BLOCKED"]
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "n_gates": len(gates),
                "n_passed_gates": int((gates["gate_status"] == "PASS").sum()),
                "n_blocked_gates": len(blocked),
                "blocked_gate_ids": ";".join(blocked["gate_id"]),
                "readout_promotion_decision": "PROMOTION_BLOCKED_PREFLIGHT_READY",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return gates, summary


def write_report(gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Readout Promotion Gate",
        "",
        "This gate separates a concrete source-filled preflight profile from an",
        "endpoint-authorized 4D readout law.",
        "",
        "## Verdict",
        "",
        "NGC4088 is preflight-ready but not promotion-ready. The onset, dimension,",
        "basis sanity, residual-blind generation, and endpoint-score guard pass.",
        "The open blockers are independent digitization review, physical",
        "normalization-law derivation, and population generalization.",
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "This promotion gate does not score the readout profile against observed",
        "velocities. It only states which preconditions are passed or blocked before",
        "a separate frozen endpoint protocol could be considered.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_readout_promotion_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    gates, summary = build_gate()
    gates.to_csv(DATA / "s4g75_ngc4088_readout_promotion_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_readout_promotion_summary.csv", index=False)
    write_report(gates, summary)
    print("PAPER8_NGC4088_READOUT_PROMOTION_GATE_COMPLETE")


if __name__ == "__main__":
    main()
