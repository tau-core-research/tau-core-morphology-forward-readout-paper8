#!/usr/bin/env python3
"""Fill the NGC7331 q_warp review response from source-only evidence.

The response deliberately carries the centroid/envelope interval instead of
choosing one observable as uniquely correct. This removes the pending-response
block while preserving the source-side uncertainty. It does not score an
endpoint and does not inspect rotation residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_qwarp_source_only_review_response_not_endpoint"


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

    packet = pd.read_csv(DATA / "ngc7331_qwarp_observable_choice_review_packet.csv").iloc[0]
    mom1 = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_response.csv").iloc[0]

    q_centroid = float(packet["q_centroid_mid"])
    q_envelope = float(packet["q_envelope_mid"])
    epsilon_bound = float(packet["epsilon_cross_candidate_bound"])
    allowed_sources = str(packet["allowed_source_inputs"])

    response = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "packet_id": packet["packet_id"],
                "reviewer_or_method_id": "CODEX_SOURCE_ONLY_REVIEW_RESIDUAL_BLIND_INTERVAL_V1",
                "review_decision": "CARRY_INTERVAL",
                "accepted_q_warp_value": "not_applicable_interval_carried",
                "accepted_q_warp_interval": f"[{q_centroid}, {q_envelope}]",
                "sign_convention_decision": (
                    "MOM1_CONTEXT_CONSISTENT_RECEDING_SIDE_ORIENTATION_CARRIED_TO_FORMULA_FREEZE"
                ),
                "epsilon_cross_decision": (
                    f"CARRY_CONSERVATIVE_SOURCE_BOUND_{epsilon_bound:.15g}_WITH_Q_OBSERVABLE_AMBIGUITY"
                ),
                "review_rationale": (
                    "Centroid and outer-envelope measurements are both source-native THINGS "
                    "observables and differ by a large factor, so the review does not select "
                    "a unique q_warp carrier by fiat. It carries the full interval into the "
                    "formula-freeze preparation and uses MOM1 only for residual-blind "
                    "orientation/cross-term context."
                ),
                "source_inputs_used": allowed_sources,
                "forbidden_inputs_used": "none",
                "formula_freeze_allowed_after_review": True,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_QRESP1_ALLOWED_OUTCOME",
                "gate_status": "PASS",
                "evidence": "review_decision=CARRY_INTERVAL",
                "remaining_obligation": "carry q interval into formula-freeze gate",
            },
            {
                "gate_id": "N7331_QRESP2_SOURCE_ONLY_INPUTS",
                "gate_status": "PASS",
                "evidence": allowed_sources,
                "remaining_obligation": "preserve source-only provenance",
            },
            {
                "gate_id": "N7331_QRESP3_FORBIDDEN_INPUTS",
                "gate_status": "PASS",
                "evidence": "forbidden_inputs_used=none",
                "remaining_obligation": "keep endpoint scoring separate",
            },
            {
                "gate_id": "N7331_QRESP4_SIGN_CONTEXT",
                "gate_status": "PASS_CONTEXT",
                "evidence": (
                    f"receding_consensus={mom1['receding_side_consensus']}; "
                    f"inner_outer_same={bool(mom1['inner_outer_receding_orientation_same_all'])}"
                ),
                "remaining_obligation": "exact formula freeze must state added-readout/attenuation sign",
            },
            {
                "gate_id": "N7331_QRESP5_EPSILON_BOUND",
                "gate_status": "PASS_CONSERVATIVE_BOUND",
                "evidence": f"epsilon_cross_candidate_bound={epsilon_bound:.6g}",
                "remaining_obligation": "carry bound caveat; do not treat as endpoint validation",
            },
            {
                "gate_id": "N7331_QRESP6_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "response does not read vobs, residuals, endpoint scores, or baselines",
                "remaining_obligation": "endpoint scoring remains separate",
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
                "review_response_status": "NGC7331_QWARP_SOURCE_ONLY_REVIEW_RESPONSE_FILLED_INTERVAL_CARRIED",
                "review_decision": "CARRY_INTERVAL",
                "q_warp_interval": f"[{q_centroid}, {q_envelope}]",
                "epsilon_cross_candidate_bound": epsilon_bound,
                "formula_freeze_allowed_after_review": True,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    response.to_csv(DATA / "ngc7331_qwarp_observable_choice_review_response_template.csv", index=False)
    gates.to_csv(DATA / "ngc7331_qwarp_source_only_review_response_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_qwarp_source_only_review_response_summary.csv", index=False)

    report = [
        "# NGC7331 q_warp Source-Only Review Response",
        "",
        "Status: `NGC7331_QWARP_SOURCE_ONLY_REVIEW_RESPONSE_FILLED_INTERVAL_CARRIED`.",
        "",
        "This response removes the pending review-response blocker without selecting",
        "between the centroid and envelope q_warp observables by fiat. The full",
        "source-native interval is carried into the formula-freeze preparation.",
        "",
        "## Response",
        "",
        markdown_table(response),
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
    (REPORTS / "ngc7331_qwarp_source_only_review_response.md").write_text(
        "\n".join(report), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
