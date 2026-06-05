#!/usr/bin/env python3
"""Build a residual-blind morphological-history proxy protocol for NGC4088.

The generic morphology-history layer is partly inverse and therefore cannot
serve as accepted source evidence.  This protocol defines a source-native
NGC4088 warp/asymmetry history proxy lane for bounding epsilon_cross.
"Memory" in existing identifiers means morphology-carried source history, not
a separate fundamental object.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_memory_history_proxy_protocol_not_endpoint"


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


def build_protocol() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    source_search = pd.read_csv(DATA / "s4g75_vertical_source_search_audit.csv")
    ngc4088_sources = source_search[source_search["galaxy"] == GALAXY]
    has_whisp = bool(
        ngc4088_sources["source_status"]
        .astype(str)
        .str.contains("WHISP_WARP_ASYMMETRY_SOURCE_READY", regex=False)
        .any()
    )

    protocol = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "protocol_id": "NGC4088_WARP_MEMORY_HISTORY_SOURCE_PROXY_PROTOCOL",
                "proxy_definition": (
                    "m_history_warp = weighted_source_score("
                    "warp_persistence, HI_lopsidedness, outer_disk_asymmetry, interaction_context)"
                ),
                "allowed_sources": "WHISP/HI morphology; channel-map persistence; outer-disk asymmetry; residual-blind environment notes",
                "forbidden_inputs": "vobs; rotation residuals; rotation-inferred family; endpoint-selected model",
                "current_status": "PROTOCOL_READY_RESPONSE_EMPTY",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    components = pd.DataFrame(
        [
            {
                "component_id": "H1_WARP_PERSISTENCE",
                "component_symbol": "h_warp_persist",
                "description": "warp/asymmetry appears across multiple adjacent channel-map panels or HI contours",
                "current_value": None,
                "availability_status": "MEASUREMENT_REQUIRED",
            },
            {
                "component_id": "H2_HI_LOPSIDEDNESS",
                "component_symbol": "h_lopsided_hi",
                "description": "side-to-side HI morphology imbalance independent of rotation residuals",
                "current_value": None,
                "availability_status": "MEASUREMENT_REQUIRED",
            },
            {
                "component_id": "H3_OUTER_DISK_ASYMMETRY",
                "component_symbol": "h_outer_asym",
                "description": "outer-disk non-axisymmetric asymmetry visible in source morphology",
                "current_value": None,
                "availability_status": "MEASUREMENT_REQUIRED",
            },
            {
                "component_id": "H4_INTERACTION_CONTEXT",
                "component_symbol": "h_env",
                "description": "residual-blind environmental or interaction context from literature/source registry",
                "current_value": None,
                "availability_status": "SOURCE_REVIEW_REQUIRED",
            },
        ]
    )
    components["galaxy"] = GALAXY
    components["claim_boundary"] = CLAIM_BOUNDARY
    components = components[
        [
            "galaxy",
            "component_id",
            "component_symbol",
            "description",
            "current_value",
            "availability_status",
            "claim_boundary",
        ]
    ]

    response_template = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "response_id": "NGC4088_MEMORY_HISTORY_PROXY_RESPONSE_V1",
                "m_history_warp": None,
                "m_history_uncertainty": None,
                "n_components_measured": 0,
                "n_components_required": len(components),
                "source_ready_whisp": has_whisp,
                "response_status": "MEASUREMENT_EMPTY",
                "uses_rotation_inferred_proxy": False,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "H1_PROTOCOL_DEFINED",
                "gate_status": "PASS",
                "evidence": "morphological-history proxy components are declared",
                "remaining_obligation": "none at protocol-definition level",
            },
            {
                "gate_id": "H2_SOURCE_LANE_AVAILABLE",
                "gate_status": "PASS" if has_whisp else "BLOCKED",
                "evidence": "WHISP warp/asymmetry source lane is available" if has_whisp else "WHISP source lane missing",
                "remaining_obligation": "none at source-lane level" if has_whisp else "acquire source lane",
            },
            {
                "gate_id": "H3_INVERSE_PROXY_EXCLUDED",
                "gate_status": "PASS",
                "evidence": "protocol forbids rotation-inferred family and endpoint residuals",
                "remaining_obligation": "keep generic inverse morphology-history proxy separate",
            },
            {
                "gate_id": "H4_COMPONENT_MEASUREMENTS_FILLED",
                "gate_status": "BLOCKED",
                "evidence": "m_history components are empty",
                "remaining_obligation": "perform residual-blind source review/measurement",
            },
            {
                "gate_id": "H5_INDEPENDENT_REVIEW",
                "gate_status": "BLOCKED",
                "evidence": "no independent morphological-history review exists",
                "remaining_obligation": "independent reviewer must verify m_history_warp",
            },
            {
                "gate_id": "H6_EPSILON_BOUND_CONNECTION",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "m_history_warp would supply the B_mem f_mem term in the epsilon_cross bound",
                "remaining_obligation": "derive/predeclare B_mem coefficient",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    status_counts = gates["gate_status"].value_counts().to_dict()
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "protocol_id": protocol["protocol_id"].iloc[0],
                "n_components": len(components),
                "n_components_measured": 0,
                "source_ready_whisp": has_whisp,
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "memory_proxy_status": "MEMORY_PROTOCOL_READY_MEASUREMENT_BLOCKED",
                "epsilon_cross_impact": "UNBLOCKS_MEMORY_COMPONENT_AFTER_MEASUREMENT_AND_REVIEW",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return protocol, components, response_template, gates, summary


def write_report(
    protocol: pd.DataFrame,
    components: pd.DataFrame,
    response_template: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Morphological-History Proxy Protocol",
        "",
        "This protocol defines a residual-blind morphological-history proxy",
        "lane for NGC4088 warp/asymmetry. It explicitly excludes the generic",
        "rotation-inferred proxy. In this context, memory means only",
        "morphology-carried source history.",
        "",
        "## Protocol",
        "",
        markdown_table(protocol),
        "",
        "## Components",
        "",
        markdown_table(components),
        "",
        "## Response Template",
        "",
        markdown_table(response_template),
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
        "m_history_warp remains empty until residual-blind source measurement and",
        "independent review are completed.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_memory_history_proxy_protocol.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    protocol, components, response, gates, summary = build_protocol()
    protocol.to_csv(DATA / "s4g75_ngc4088_memory_history_proxy_protocol.csv", index=False)
    components.to_csv(DATA / "s4g75_ngc4088_memory_history_proxy_components.csv", index=False)
    response.to_csv(DATA / "s4g75_ngc4088_memory_history_proxy_response_template.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_memory_history_proxy_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_memory_history_proxy_summary.csv", index=False)
    write_report(protocol, components, response, gates, summary)
    print("PAPER8_NGC4088_MEMORY_HISTORY_PROXY_PROTOCOL_COMPLETE")


if __name__ == "__main__":
    main()
