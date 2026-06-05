#!/usr/bin/env python3
"""Review source evidence for NGC7331 exact B2 transfer fields.

This gate consumes residual-blind source context already present in the
package and records which of the q_warp, sigma_warp, and epsilon_cross packets
can be promoted. It deliberately does not fill numeric endpoint inputs when the
source evidence is only qualitative or sign-ambiguous.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_b2_exact_transfer_source_evidence_review_not_endpoint"
BOSMA_URL = "https://ned.ipac.caltech.edu/level5/March05/Bosma/Bosma4_7.html"
PATRA_URL = "https://academic.oup.com/mnras/article/478/4/4931/5045978"


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

    packet_summary = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_source_packet_summary.csv"
    ).iloc[0]
    onset_summary = pd.read_csv(DATA / "ngc7331_fractional_warp_onset_source_summary.csv").iloc[0]
    caveat_summary = pd.read_csv(DATA / "ngc7331_outer_warp_vertical_caveat_summary.csv").iloc[0]
    caveat_fields = pd.read_csv(DATA / "ngc7331_outer_warp_vertical_caveat_fields.csv")

    inclination = caveat_fields.loc[
        caveat_fields["observable"].eq("inclination_review_range"), "value"
    ].iloc[0]
    warp_caveat = caveat_fields.loc[
        caveat_fields["observable"].eq("possible_outer_warp_caveat"), "value"
    ].iloc[0]

    evidence = pd.DataFrame(
        [
            {
                "evidence_id": "N7331_B2_EV1_HI_COMPLEX_WARP",
                "supports_field": "q_warp;sigma_warp;epsilon_cross_inputs",
                "evidence_status": "ACCEPTED_CONTEXT_NOT_NUMERIC",
                "source": BOSMA_URL,
                "source_summary": (
                    "21 cm review reports an extended H I disk with complex warp; "
                    "the optical disk and very outer H I warp can deviate in opposite directions"
                ),
                "usable_now": True,
                "numeric_value": pd.NA,
                "why_not_final_input": "context supports a warp lane but does not by itself fix warp strength or sign",
            },
            {
                "evidence_id": "N7331_B2_EV2_FRACTIONAL_ONSET",
                "supports_field": "q_warp",
                "evidence_status": "ACCEPTED_NUMERIC_ONSET_NOT_AMPLITUDE",
                "source": BOSMA_URL,
                "source_summary": (
                    "fractional outer-warp onset has been converted into a replay-only "
                    f"x_w={float(onset_summary['approx_warp_onset_over_RHI']):.6g}"
                ),
                "usable_now": True,
                "numeric_value": float(onset_summary["approx_warp_onset_over_RHI"]),
                "why_not_final_input": "x_w is not q_warp; it fixes onset scale, not warp strength",
            },
            {
                "evidence_id": "N7331_B2_EV3_VERTICAL_OUTER_CONTEXT",
                "supports_field": "sigma_warp;epsilon_cross_inputs",
                "evidence_status": "ACCEPTED_CONTEXT_SIGN_AMBIGUOUS",
                "source": PATRA_URL,
                "source_summary": (
                    "vertical/thickness study records inclination context and possible "
                    f"outer-warp emission caveat ({warp_caveat})"
                ),
                "usable_now": True,
                "numeric_value": pd.NA,
                "why_not_final_input": "possible outer emission/warp context does not freeze added-readout vs attenuation sign",
            },
            {
                "evidence_id": "N7331_B2_EV4_INCLINATION_PROJECTION_CONTEXT",
                "supports_field": "epsilon_cross_inputs",
                "evidence_status": "ACCEPTED_NUMERIC_CONTEXT_NOT_BOUND",
                "source": PATRA_URL,
                "source_summary": f"inclination review range/adopted value is available: {inclination}",
                "usable_now": True,
                "numeric_value": pd.NA,
                "why_not_final_input": "projection context is one component, not a closed epsilon_cross bound",
            },
        ]
    )
    evidence["galaxy"] = GALAXY
    evidence["endpoint_scores_allowed"] = False
    evidence["uses_vobs_or_residual"] = False
    evidence["claim_boundary"] = CLAIM_BOUNDARY
    evidence = evidence[
        [
            "galaxy",
            "evidence_id",
            "supports_field",
            "evidence_status",
            "source",
            "source_summary",
            "usable_now",
            "numeric_value",
            "why_not_final_input",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    decisions = pd.DataFrame(
        [
            {
                "required_b2_field": "q_warp",
                "review_decision": "CONTEXT_READY_NUMERIC_Q_WARP_BLOCKED",
                "accepted_value": pd.NA,
                "decision_basis": "complex H I warp context plus x_w onset exists, but no source-native warp-strength amplitude is measured",
                "next_required_action": "digitize or acquire H I warp amplitude/asymmetry map and compute bounded q_warp",
            },
            {
                "required_b2_field": "sigma_warp",
                "review_decision": "SIGN_RULE_BLOCKED_COMPLEX_WARP",
                "accepted_value": pd.NA,
                "decision_basis": "Bosma-style complex warp and Patra outer-emission caveat make added-readout vs attenuation sign nontrivial",
                "next_required_action": "freeze sign convention from source-side orientation/readout geometry",
            },
            {
                "required_b2_field": "epsilon_cross_inputs",
                "review_decision": "BOUND_BLOCKED_CROSS_TERMS_LIKELY_RELEVANT",
                "accepted_value": pd.NA,
                "decision_basis": "complex multi-zone warp/projection context means cross terms cannot be assumed zero",
                "next_required_action": "build residual-blind orientation, side-asymmetry, history/context, and locality bound",
            },
        ]
    )
    decisions["galaxy"] = GALAXY
    decisions["endpoint_scores_allowed"] = False
    decisions["uses_vobs_or_residual"] = False
    decisions["claim_boundary"] = CLAIM_BOUNDARY
    decisions = decisions[
        [
            "galaxy",
            "required_b2_field",
            "review_decision",
            "accepted_value",
            "decision_basis",
            "next_required_action",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_B2ER1_SOURCE_CONTEXT_AVAILABLE",
                "gate_status": "PASS",
                "evidence": "Bosma H I warp context and Patra vertical/projection context are available",
                "remaining_obligation": "none at context availability level",
            },
            {
                "gate_id": "N7331_B2ER2_Q_WARP_PROMOTION",
                "gate_status": "BLOCKED_NUMERIC_AMPLITUDE_MISSING",
                "evidence": "x_w exists but q_warp amplitude/asymmetry does not",
                "remaining_obligation": "source-native H I map digitization or literature amplitude bound",
            },
            {
                "gate_id": "N7331_B2ER3_SIGMA_PROMOTION",
                "gate_status": "BLOCKED_SIGN_AMBIGUOUS",
                "evidence": "complex warp has opposite inner/outer directional context",
                "remaining_obligation": "source-side sign/orientation review",
            },
            {
                "gate_id": "N7331_B2ER4_EPSILON_PROMOTION",
                "gate_status": "BLOCKED_BOUND_MISSING",
                "evidence": "cross terms are plausibly relevant but not bounded",
                "remaining_obligation": "orientation/asymmetry/history/locality bound packet",
            },
            {
                "gate_id": "N7331_B2ER5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "review uses source/literature context and previous source gates, not vobs residuals",
                "remaining_obligation": "endpoint scoring remains blocked until formula freeze",
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
                "source_evidence_review_status": "NGC7331_SOURCE_EVIDENCE_REVIEW_BUILT_EXACT_TRANSFER_STILL_BLOCKED",
                "packet_status": str(packet_summary["source_packet_status"]),
                "n_evidence_rows": len(evidence),
                "n_decisions": len(decisions),
                "n_gates": len(gates),
                "n_pass": int(gates["gate_status"].eq("PASS").sum()),
                "n_blocked": int(gates["gate_status"].str.startswith("BLOCKED").sum()),
                "q_warp_promoted": False,
                "sigma_warp_promoted": False,
                "epsilon_cross_promoted": False,
                "complex_warp_context_confirmed": True,
                "cross_terms_must_be_carried_or_bounded": True,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "population_claim_allowed": False,
                "next_required_action": "acquire or digitize source-native H I warp amplitude/asymmetry for q_warp and sign review",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    evidence.to_csv(DATA / "ngc7331_b2_exact_transfer_source_evidence.csv", index=False)
    decisions.to_csv(DATA / "ngc7331_b2_exact_transfer_source_evidence_decisions.csv", index=False)
    gates.to_csv(DATA / "ngc7331_b2_exact_transfer_source_evidence_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_b2_exact_transfer_source_evidence_summary.csv", index=False)

    report = [
        "# NGC7331 B2 Exact Transfer Source Evidence Review",
        "",
        "This review consumes residual-blind source context for NGC7331 and asks",
        "whether the exact B2 transfer packet can be promoted. It cannot yet:",
        "the evidence confirms a real complex warp context, but does not supply",
        "a numeric q_warp, an unambiguous sigma_warp sign, or a closed",
        "epsilon_cross bound.",
        "",
        "## Evidence",
        "",
        markdown_table(evidence),
        "",
        "## Decisions",
        "",
        markdown_table(decisions),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "The review strengthens NGC7331 as an exact-transfer upgrade target by",
        "confirming that the missing fields are physically relevant, not arbitrary.",
        "It also prevents overclaiming: because the warp is complex, the sign and",
        "cross-term layers cannot be silently inherited from NGC4088.",
        "",
    ]
    (REPORTS / "ngc7331_b2_exact_transfer_source_evidence_review.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
