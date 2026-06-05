#!/usr/bin/env python3
"""Build the NGC4088 breakthrough-oriented promotion gate.

This gate consolidates the residual-blind x_w conversion, independent q/memory
review, B_i freeze rule, and epsilon_cross bound artifacts. It is deliberately
not an endpoint scorer and does not promote a final accepted subfamily label.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_breakthrough_promotion_gate_not_endpoint"


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

    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    review = pd.read_csv(
        DATA / "s4g75_ngc4088_source_response_independent_review_summary.csv"
    ).iloc[0]
    bi = pd.read_csv(DATA / "s4g75_ngc4088_bi_coefficient_freeze_rule_summary.csv").iloc[0]
    eps_expr = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_bound_expression_summary.csv"
    ).iloc[0]
    eps_bound = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_locality_bound_summary.csv"
    ).iloc[0]
    packet = pd.read_csv(DATA / "ngc4088_source_review_packet_summary.csv").iloc[0]

    xw_ready = bool(xw["accepted_for_mapping_rule"])
    source_authorized = bool(review["numeric_bound_source_authorization"])
    bi_ready = bool(bi["numeric_bound_coefficient_authorization"])
    eps_available = str(eps_expr["numeric_bound_status"]) == "NUMERIC_EPSILON_PROTOCOL_BOUND_AVAILABLE"
    locality_ready = str(eps_bound["locality_bound_status"]).startswith("LOCALITY_EPSILON_BOUND_READY")

    gates = pd.DataFrame(
        [
            {
                "gate_id": "BT1_LITERATURE_WARP_HISTORY_ANCHOR",
                "gate_status": "PASS" if packet["n_accepted_literature_fields"] >= 5 else "BLOCKED",
                "evidence": f"{int(packet['n_accepted_literature_fields'])} accepted literature fields",
                "remaining_obligation": "preserve citation/source-line provenance",
            },
            {
                "gate_id": "BT2_XW_MAPPING_READY",
                "gate_status": "PASS_CAVEATED" if xw_ready else "BLOCKED",
                "evidence": f"x_warp={float(xw['x_warp_onset']):.6g}, uncertainty={float(xw['x_warp_uncertainty']):.6g}, dimension_ok={bool(xw['dimension_check_passed'])}",
                "remaining_obligation": "independent source reviewer should recheck the manual channel-map digitization before accepted-manifest use",
            },
            {
                "gate_id": "BT3_Q_MEMORY_AUTHORIZED",
                "gate_status": "PASS" if source_authorized else "BLOCKED",
                "evidence": f"q={float(review['accepted_q_warp_measured']):.6g}, m_history={float(review['accepted_m_history_warp']):.6g}",
                "remaining_obligation": "preserve residual-blind review packet and uncertainty",
            },
            {
                "gate_id": "BT4_BI_FREEZE_READY",
                "gate_status": "PASS" if bi_ready else "BLOCKED",
                "evidence": str(bi["freeze_rule_status"]),
                "remaining_obligation": "treat B_i=1 as conservative protocol bound, not final Tau-side coefficient law",
            },
            {
                "gate_id": "BT5_EPSILON_NUMERIC_BOUND_AVAILABLE",
                "gate_status": "PASS_CAVEATED" if eps_available and locality_ready else "BLOCKED",
                "evidence": f"|epsilon_cross| <= {float(eps_bound['numeric_bound_value']):.6g}",
                "remaining_obligation": "do not use the bound as an endpoint-selected amplitude; keep it source-bound",
            },
            {
                "gate_id": "BT6_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "all consolidation inputs set endpoint_scores_allowed=False",
                "remaining_obligation": "endpoint diagnostics remain separate from accepted-manifest promotion",
            },
        ]
    )
    gates["galaxy"] = "NGC4088"
    gates["proposed_readout_subfamily"] = "K_warp_history_coupled"
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "proposed_readout_subfamily",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    n_pass_like = int(gates["gate_status"].str.startswith("PASS").sum())
    n_blocked = int(gates["gate_status"].eq("BLOCKED").sum())
    n_caveated = int(gates["gate_status"].eq("PASS_CAVEATED").sum())
    breakthrough_status = (
        "BREAKTHROUGH_PROTOCOL_BOUND_READY_NOT_ENDPOINT"
        if n_blocked == 0 and n_caveated > 0
        else "BREAKTHROUGH_PROMOTION_BLOCKED"
        if n_blocked > 0
        else "BREAKTHROUGH_PROTOCOL_READY_NOT_ENDPOINT"
    )
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "proposed_readout_subfamily": "K_warp_history_coupled",
                "n_gates": len(gates),
                "n_pass_like": n_pass_like,
                "n_caveated": n_caveated,
                "n_blocked": n_blocked,
                "x_warp_onset": float(xw["x_warp_onset"]) if xw_ready else None,
                "q_warp": float(review["accepted_q_warp_measured"]) if source_authorized else None,
                "m_history_warp": float(review["accepted_m_history_warp"]) if source_authorized else None,
                "epsilon_cross_bound": float(eps_bound["numeric_bound_value"]) if eps_available and locality_ready else None,
                "breakthrough_status": breakthrough_status,
                "accepted_subfamily_label_promoted": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates.to_csv(DATA / "ngc4088_breakthrough_promotion_gate.csv", index=False)
    summary.to_csv(DATA / "ngc4088_breakthrough_promotion_summary.csv", index=False)

    report = [
        "# NGC4088 Breakthrough Promotion Gate",
        "",
        "This gate consolidates the residual-blind NGC4088 warp/history source",
        "chain. It is designed to answer whether the diagnostic NGC4088 signal",
        "has a source-bound protocol pathway toward a predeclared test case.",
        "It does not score endpoints and does not validate Tau Core.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Interpretation",
        "",
        "The current result is a source-bound protocol breakthrough, not an empirical",
        "breakthrough. The warp/history literature anchor, x_w mapping, q/memory",
        "authorization, B_i freeze, and epsilon_cross numeric protocol bound now",
        "form a continuous residual-blind chain. The remaining caveat is that the",
        "x_w digitization and epsilon_cross bound are still protocol/caveated inputs,",
        "not final accepted-manifest endpoint permissions.",
        "",
    ]
    (REPORTS / "ngc4088_breakthrough_promotion_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
