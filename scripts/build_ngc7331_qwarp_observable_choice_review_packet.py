#!/usr/bin/env python3
"""Build the NGC7331 q_warp observable-choice independent review packet.

The packet freezes what an independent reviewer may use to decide whether the
B2 q_warp source-strength carrier should be the centroid observable, the
outer-envelope observable, or an explicit interval. It does not perform that
review, freeze a formula, or score an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_qwarp_observable_choice_review_packet_not_endpoint"


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

    choice_summary = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_summary.csv").iloc[0]
    q_candidates = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_candidates.csv")
    first_pass = pd.read_csv(DATA / "ngc7331_things_qwarp_first_pass_summary.csv").iloc[0]
    sensitivity = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_sensitivity_summary.csv").iloc[0]
    mom1 = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_summary.csv").iloc[0]
    mom1_response = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_response.csv").iloc[0]

    q_centroid = float(choice_summary["q_centroid_mid"])
    q_envelope = float(choice_summary["q_envelope_mid"])

    packet = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "packet_id": "N7331_QWARP_OBSERVABLE_CHOICE_REVIEW_PACKET_V1",
                "review_status": "REVIEW_PACKET_READY_RESPONSE_PENDING",
                "allowed_source_inputs": (
                    "ngc7331_things_qwarp_first_pass_measurements.csv;"
                    "ngc7331_things_qwarp_measurement_sensitivity.csv;"
                    "ngc7331_things_mom1_sign_cross_measurements.csv;"
                    "ngc7331_qwarp_observable_choice_candidates.csv"
                ),
                "forbidden_inputs": (
                    "vobs;rotation_residual;endpoint_score;baseline_rmse;"
                    "wrong_family_rank;best_fit_family;required_S_tau_diagnostic"
                ),
                "q_centroid_mid": q_centroid,
                "q_envelope_mid": q_envelope,
                "q_envelope_to_centroid_ratio": float(
                    choice_summary["q_envelope_to_centroid_ratio"]
                ),
                "mom1_context_status": str(mom1["mom1_sign_cross_status"]),
                "epsilon_cross_candidate_bound": float(mom1["epsilon_cross_candidate_bound"]),
                "accepted_review_outcomes": (
                    "ACCEPT_CENTROID;ACCEPT_ENVELOPE;CARRY_INTERVAL;REJECT_Q_FREEZE"
                ),
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    review_options = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "review_option": "ACCEPT_CENTROID",
                "q_value_or_interval": f"{q_centroid:.12g}",
                "required_justification": (
                    "reviewer accepts that B2 q_warp should measure mean outer-ridge "
                    "centroid displacement rather than envelope support"
                ),
                "formula_freeze_effect": "q_warp_numeric_candidate_available_sign_epsilon_still_required",
            },
            {
                "galaxy": GALAXY,
                "review_option": "ACCEPT_ENVELOPE",
                "q_value_or_interval": f"{q_envelope:.12g}",
                "required_justification": (
                    "reviewer accepts that B2 q_warp should measure outer-envelope "
                    "support, not only centroid shift"
                ),
                "formula_freeze_effect": "q_warp_numeric_candidate_available_sign_epsilon_still_required",
            },
            {
                "galaxy": GALAXY,
                "review_option": "CARRY_INTERVAL",
                "q_value_or_interval": f"[{q_centroid:.12g}, {q_envelope:.12g}]",
                "required_justification": (
                    "reviewer decides both source-native observables are admissible "
                    "and the exact-transfer formula must carry q uncertainty"
                ),
                "formula_freeze_effect": "q_interval_available_sign_epsilon_still_required",
            },
            {
                "galaxy": GALAXY,
                "review_option": "REJECT_Q_FREEZE",
                "q_value_or_interval": "not_applicable",
                "required_justification": (
                    "reviewer finds neither observable sufficiently tied to B2 source "
                    "strength without additional source-native data or theorem"
                ),
                "formula_freeze_effect": "q_warp_remains_blocked",
            },
        ]
    )
    review_options["endpoint_scores_allowed"] = False
    review_options["uses_vobs_or_residual"] = False
    review_options["claim_boundary"] = CLAIM_BOUNDARY

    response_template = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "packet_id": "N7331_QWARP_OBSERVABLE_CHOICE_REVIEW_PACKET_V1",
                "reviewer_or_method_id": "PENDING_INDEPENDENT_REVIEW",
                "review_decision": "PENDING_INDEPENDENT_REVIEW",
                "accepted_q_warp_value": "PENDING_INDEPENDENT_REVIEW",
                "accepted_q_warp_interval": "PENDING_INDEPENDENT_REVIEW",
                "sign_convention_decision": "PENDING_INDEPENDENT_REVIEW",
                "epsilon_cross_decision": "PENDING_INDEPENDENT_REVIEW",
                "review_rationale": "PENDING_INDEPENDENT_REVIEW",
                "source_inputs_used": "PENDING_INDEPENDENT_REVIEW",
                "forbidden_inputs_used": "PENDING_INDEPENDENT_REVIEW",
                "formula_freeze_allowed_after_review": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_QPACK1_PACKET_SCOPE",
                "gate_status": "PASS",
                "evidence": "review packet declares allowed outcomes and forbidden inputs",
                "remaining_obligation": "fill independent review response",
            },
            {
                "gate_id": "N7331_QPACK2_SOURCE_INPUTS",
                "gate_status": "PASS",
                "evidence": (
                    f"first_pass={first_pass['qwarp_first_pass_status']}; "
                    f"sensitivity={sensitivity['sensitivity_status']}"
                ),
                "remaining_obligation": "reviewer must cite which source-side rows are used",
            },
            {
                "gate_id": "N7331_QPACK3_MOM1_CONTEXT",
                "gate_status": "PASS_CONTEXT",
                "evidence": (
                    f"receding={mom1_response['receding_side_consensus']}; "
                    f"f_PA={float(mom1_response['f_pa_max']):.6g}"
                ),
                "remaining_obligation": "sign convention still requires explicit review decision",
            },
            {
                "gate_id": "N7331_QPACK4_RESPONSE",
                "gate_status": "BLOCKED_RESPONSE_PENDING",
                "evidence": "response template is empty",
                "remaining_obligation": "independent reviewer must select option or reject freeze",
            },
            {
                "gate_id": "N7331_QPACK5_FORMULA_FREEZE",
                "gate_status": "BLOCKED",
                "evidence": "packet creation alone cannot freeze q, sign, or epsilon",
                "remaining_obligation": "valid response plus sign/epsilon handling required",
            },
            {
                "gate_id": "N7331_QPACK6_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "packet forbids vobs/residual/scores/ranks as review inputs",
                "remaining_obligation": "none at packet level",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "review_packet_status": "NGC7331_QWARP_OBSERVABLE_CHOICE_REVIEW_PACKET_READY_RESPONSE_PENDING",
                "n_review_options": int(len(review_options)),
                "q_centroid_mid": q_centroid,
                "q_envelope_mid": q_envelope,
                "response_pending": True,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "fill independent review response, then run acceptance/intake gate"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    packet.to_csv(DATA / "ngc7331_qwarp_observable_choice_review_packet.csv", index=False)
    review_options.to_csv(DATA / "ngc7331_qwarp_observable_choice_review_options.csv", index=False)
    response_template.to_csv(
        DATA / "ngc7331_qwarp_observable_choice_review_response_template.csv", index=False
    )
    gates.to_csv(DATA / "ngc7331_qwarp_observable_choice_review_packet_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_qwarp_observable_choice_review_packet_summary.csv", index=False)

    report = [
        "# NGC7331 q_warp Observable-Choice Review Packet",
        "",
        "Status: `NGC7331_QWARP_OBSERVABLE_CHOICE_REVIEW_PACKET_READY_RESPONSE_PENDING`.",
        "",
        "This packet freezes the residual-blind review choices for deciding which",
        "source-native q_warp observable, if any, can enter the exact-transfer B2",
        "formula-freeze route. It does not perform the review and does not score an endpoint.",
        "",
        "## Packet",
        "",
        markdown_table(packet),
        "",
        "## Review options",
        "",
        markdown_table(review_options),
        "",
        "## Response template",
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
    ]
    (REPORTS / "ngc7331_qwarp_observable_choice_review_packet.md").write_text(
        "\n".join(report), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
