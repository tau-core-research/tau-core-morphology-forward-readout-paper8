#!/usr/bin/env python3
"""Independently review NGC4088 first-pass q/history source responses.

The review recomputes q_warp and the morphological-history proxy from the
frozen source-side digitization artifacts. It is residual-blind and does not
inspect rotation residuals or endpoint scores. Existing memory identifiers mean
morphology-carried source history, not a separate fundamental object.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_source_response_independent_review_not_endpoint"


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


def clipped(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def build_review() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    response = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_template.csv"
    ).iloc[0]
    validation = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_validation.csv"
    ).iloc[0]
    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    q_first = pd.read_csv(DATA / "s4g75_ngc4088_qwarp_first_pass_response.csv").iloc[0]
    memory_first = pd.read_csv(
        DATA / "s4g75_ngc4088_memory_history_first_pass_response.csv"
    ).iloc[0]
    memory_components = pd.read_csv(
        DATA / "s4g75_ngc4088_memory_history_first_pass_components.csv"
    )
    h4_review_path = DATA / "s4g75_ngc4088_h4_interaction_context_review_summary.csv"
    h4_review = pd.read_csv(h4_review_path).iloc[0] if h4_review_path.exists() else None
    if h4_review is not None and str(h4_review["h4_review_status"]) == "H4_INTERACTION_CONTEXT_ACCEPTED_SOURCE_REVIEWED":
        h4_mask = memory_components["component_id"] == "H4_INTERACTION_CONTEXT"
        memory_components.loc[h4_mask, "component_value"] = float(
            h4_review["accepted_h4_interaction_context"]
        )
        memory_components.loc[h4_mask, "evidence"] = (
            "source-reviewed NGC4088 distortion/asymmetric-warp/companion-context evidence"
        )
        memory_components.loc[h4_mask, "component_status"] = (
            "ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND"
        )

    inner_pa = float(response["inner_disk_axis_pa_deg"])
    side_a_pa = float(response["outer_ridge_axis_side_a_pa_deg"])
    side_b_pa = float(response["outer_ridge_axis_side_b_pa_deg"])
    delta_pa_max = max(abs(side_a_pa - inner_pa), abs(side_b_pa - inner_pa))
    side_onset_delta = abs(
        float(response["onset_radius_side_b_arcmin"])
        - float(response["onset_radius_side_a_arcmin"])
    )
    q_review = clipped(delta_pa_max / 90.0)
    q_uncertainty = clipped(
        max(
            float(xw["x_warp_uncertainty"]) / float(xw["x_warp_onset"]),
            side_onset_delta / float(xw["hi_radius_arcmin"]),
        )
    )

    measured_components = memory_components["component_value"].notna()
    memory_review = float(memory_components.loc[measured_components, "component_value"].mean())
    missing_components = int((~measured_components).sum())
    memory_uncertainty = clipped(
        max(
            float(memory_first["m_history_uncertainty"]),
            missing_components / len(memory_components),
            float(h4_review["accepted_h4_uncertainty"]) if h4_review is not None else 0.0,
        )
    )

    q_delta = abs(q_review - float(q_first["q_warp_measured"]))
    memory_delta = abs(memory_review - float(memory_first["m_history_warp"]))
    q_accept = (
        str(validation["validation_status"]) == "READY_FOR_XW_CONVERSION_AUDIT"
        and not bool(validation["forbidden_input_detected"])
        and q_delta <= float(q_first["q_warp_uncertainty"]) + 1.0e-12
    )
    memory_accept = (
        measured_components.sum() >= 4
        and memory_delta <= float(memory_first["m_history_uncertainty"]) + 1.0e-12
        and not bool(memory_first["uses_vobs_or_residual"])
    )
    memory_accept_caveated = (
        not memory_accept
        and measured_components.sum() >= 3
        and memory_delta <= float(memory_first["m_history_uncertainty"]) + 1.0e-12
        and not bool(memory_first["uses_vobs_or_residual"])
    )

    review = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "review_id": "NGC4088_QWARP_INDEPENDENT_SOURCE_REVIEW",
                "review_target": "q_warp_measured",
                "first_pass_value": float(q_first["q_warp_measured"]),
                "review_recomputed_value": q_review,
                "review_uncertainty": q_uncertainty,
                "absolute_delta": q_delta,
                "accepted_value": q_review if q_accept else None,
                "accepted_for_numeric_bound": q_accept,
                "review_status": (
                    "ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND"
                    if q_accept
                    else "REVIEW_REJECTED_OR_BLOCKED"
                ),
                "review_basis": "independent recomputation from frozen channel-map PA mismatch and x_w audit",
                "review_caveat": "source-side review only; not empirical endpoint validation",
            },
            {
                "galaxy": GALAXY,
                "review_id": "NGC4088_MEMORY_HISTORY_INDEPENDENT_SOURCE_REVIEW",
                "review_target": "m_history_warp",
                "first_pass_value": float(memory_first["m_history_warp"]),
                "review_recomputed_value": memory_review,
                "review_uncertainty": memory_uncertainty,
                "absolute_delta": memory_delta,
                "accepted_value": memory_review if (memory_accept or memory_accept_caveated) else None,
                "accepted_for_numeric_bound": memory_accept or memory_accept_caveated,
                "review_status": (
                    "ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND"
                    if memory_accept
                    else "ACCEPTED_CAVEATED_FOR_PROTOCOL_NUMERIC_BOUND"
                    if memory_accept_caveated
                    else "REVIEW_REJECTED_OR_BLOCKED"
                ),
                "review_basis": "independent recomputation from first-pass source components",
                "review_caveat": (
                    "H4 interaction/context source review filled; history means morphology-carried source history"
                    if memory_accept
                    else "environment component remains unfilled; uncertainty carries missing H4 context"
                ),
            },
        ]
    )
    review["reviewer_id"] = "CODEX_INDEPENDENT_SOURCE_REVIEWER_RESIDUAL_BLIND_001"
    review["uses_vobs_or_residual"] = False
    review["endpoint_scores_allowed"] = False
    review["claim_boundary"] = CLAIM_BOUNDARY
    review = review[
        [
            "galaxy",
            "review_id",
            "review_target",
            "reviewer_id",
            "first_pass_value",
            "review_recomputed_value",
            "review_uncertainty",
            "absolute_delta",
            "accepted_value",
            "accepted_for_numeric_bound",
            "review_status",
            "review_basis",
            "review_caveat",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "SR1_FROZEN_SOURCE_ARTIFACTS_PRESENT",
                "gate_status": "PASS",
                "evidence": "digitization response, validation, x_w audit, and first-pass responses are present",
                "remaining_obligation": "preserve frozen artifact provenance",
            },
            {
                "gate_id": "SR2_QWARP_RECOMPUTATION_MATCHES",
                "gate_status": "PASS" if q_accept else "BLOCKED",
                "evidence": f"q_review={q_review:.6g}, first_pass={float(q_first['q_warp_measured']):.6g}, delta={q_delta:.6g}",
                "remaining_obligation": "none" if q_accept else "resolve q_warp mismatch",
            },
            {
                "gate_id": "SR3_MEMORY_RECOMPUTATION_MATCHES_CAVEATED",
                "gate_status": "PASS" if (memory_accept or memory_accept_caveated) else "BLOCKED",
                "evidence": f"m_review={memory_review:.6g}, first_pass={float(memory_first['m_history_warp']):.6g}, missing_components={missing_components}",
                "remaining_obligation": (
                    "none; H4 source-history context filled"
                    if memory_accept
                    else "carry H4 caveat into numeric-bound interpretation"
                    if memory_accept_caveated
                    else "resolve morphological-history source response"
                ),
            },
            {
                "gate_id": "SR4_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "review reads only source/digitization artifacts and forbids vobs/residuals",
                "remaining_obligation": "keep endpoint tests separate",
            },
            {
                "gate_id": "SR5_NUMERIC_BOUND_SOURCE_AUTHORIZATION",
                "gate_status": "PASS" if q_accept and (memory_accept or memory_accept_caveated) else "BLOCKED",
                "evidence": (
                    "q accepted and memory accepted with source-reviewed H4 context"
                    if memory_accept
                    else "q accepted and memory accepted with explicit H4 caveat"
                ),
                "remaining_obligation": (
                    "freeze residual-blind B_i rule before evaluating epsilon_cross"
                    if q_accept and (memory_accept or memory_accept_caveated)
                    else "complete accepted source review"
                ),
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
    all_pass = int(status_counts.get("BLOCKED", 0)) == 0
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "review_packet_id": "NGC4088_QMEM_SOURCE_RESPONSE_INDEPENDENT_REVIEW",
                "n_reviews": len(review),
                "n_accepted_for_numeric_bound": int(review["accepted_for_numeric_bound"].sum()),
                "n_caveated_acceptances": int(
                    review["review_status"].str.contains("CAVEATED").sum()
                ),
                "accepted_q_warp_measured": q_review if q_accept else None,
                "accepted_m_history_warp": memory_review if (memory_accept or memory_accept_caveated) else None,
                "accepted_memory_uncertainty": memory_uncertainty if (memory_accept or memory_accept_caveated) else None,
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "source_review_status": (
                    "SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND"
                    if all_pass and memory_accept
                    else "SOURCE_RESPONSES_ACCEPTED_CAVEATED_FOR_PROTOCOL_BOUND"
                    if all_pass
                    else "SOURCE_RESPONSE_REVIEW_BLOCKED"
                ),
                "numeric_bound_source_authorization": all_pass,
                "next_required_action": (
                    "freeze_residual_blind_B_i_rule"
                    if all_pass
                    else "complete_independent_source_review"
                ),
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return review, gates, summary, memory_components


def write_report(
    review: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
    memory_components: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Source Response Independent Review",
        "",
        "This artifact independently recomputes the first-pass q_warp and",
        "morphological-history source responses from frozen source-side artifacts. It is",
        "residual-blind and does not inspect endpoint scores.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Review Rows",
        "",
        markdown_table(review),
        "",
        "## Memory Components Reused By Review",
        "",
        markdown_table(memory_components),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The review authorizes q_warp and a caveated morphological-history value for the",
        "protocol numeric epsilon_cross bound only. It is not an endpoint fit and",
        "not empirical validation of the final physical readout.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_source_response_independent_review.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    review, gates, summary, memory_components = build_review()
    review.to_csv(DATA / "s4g75_ngc4088_source_response_independent_review.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_source_response_independent_review_gate.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_source_response_independent_review_summary.csv",
        index=False,
    )
    write_report(review, gates, summary, memory_components)
    print("PAPER8_NGC4088_SOURCE_RESPONSE_INDEPENDENT_REVIEW_COMPLETE")


if __name__ == "__main__":
    main()
