#!/usr/bin/env python3
"""Build the NGC7331 q_warp observable-choice review gate.

This gate synthesizes the THINGS centroid q_warp, envelope q_warp, and MOM1
sign/cross-term review into a formula-freeze decision. It remains residual
blind and endpoint blocked: it reads only source-side derived packets.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_qwarp_observable_choice_review_gate_not_endpoint"


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
    return str(value).strip().lower() == "true"


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    first_pass = pd.read_csv(DATA / "ngc7331_things_qwarp_first_pass_summary.csv").iloc[0]
    sensitivity = pd.read_csv(DATA / "ngc7331_things_qwarp_measurement_sensitivity_summary.csv").iloc[0]
    mom1 = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_summary.csv").iloc[0]
    mom1_response = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_response.csv").iloc[0]

    q_centroid_mid = 0.5 * (
        float(sensitivity["q_centroid_mean_min"])
        + float(sensitivity["q_centroid_mean_max"])
    )
    q_envelope_mid = 0.5 * (
        float(sensitivity["q_envelope_p80_mean_min"])
        + float(sensitivity["q_envelope_p80_mean_max"])
    )
    q_ratio = q_envelope_mid / max(q_centroid_mid, 1.0e-12)
    q_choice_gap_fraction = abs(q_envelope_mid - q_centroid_mid) / max(q_envelope_mid, 1.0e-12)

    candidates = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "candidate_observable": "CENTROID_RIDGE_SHIFT",
                "q_warp_candidate": q_centroid_mid,
                "source_status": "STABLE_FIRST_PASS_REVIEW_REQUIRED",
                "physical_readout_interpretation": "mean outer ridge displacement relative to inner reference",
                "risk": "may undercount symmetric outer warp/envelope support",
                "formula_freeze_recommendation": "DO_NOT_FREEZE_WITHOUT_REVIEW",
            },
            {
                "galaxy": GALAXY,
                "candidate_observable": "OUTER_ENVELOPE_P80_SUPPORT",
                "q_warp_candidate": q_envelope_mid,
                "source_status": "STABLE_FIRST_PASS_REVIEW_REQUIRED",
                "physical_readout_interpretation": "outer envelope support away from inner reference",
                "risk": "may overcount broad envelope thickness as warp strength",
                "formula_freeze_recommendation": "DO_NOT_FREEZE_WITHOUT_REVIEW",
            },
        ]
    )
    candidates["endpoint_scores_allowed"] = False
    candidates["uses_vobs_or_residual"] = False
    candidates["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_QCHOICE1_SOURCE_NATIVE_Q_EXISTS",
                "gate_status": "PASS_REVIEW_INPUT_AVAILABLE",
                "evidence": (
                    f"centroid_mid={q_centroid_mid:.6g}; envelope_mid={q_envelope_mid:.6g}"
                ),
                "remaining_obligation": "none for existence of q candidates",
            },
            {
                "gate_id": "N7331_QCHOICE2_OBSERVABLE_UNIQUENESS",
                "gate_status": "BLOCKED_OBSERVABLE_CHOICE_NOT_UNIQUE",
                "evidence": f"envelope/centroid ratio={q_ratio:.6g}",
                "remaining_obligation": "independent review must select centroid, envelope, or carry an interval",
            },
            {
                "gate_id": "N7331_QCHOICE3_MOM1_CONTEXT",
                "gate_status": "PASS_REVIEW_INPUT_AVAILABLE",
                "evidence": (
                    "MOM1 receding side consensus="
                    f"{mom1_response['receding_side_consensus']}; "
                    f"f_PA_max={float(mom1_response['f_pa_max']):.6g}"
                ),
                "remaining_obligation": "map source orientation to B2 sign convention",
            },
            {
                "gate_id": "N7331_QCHOICE4_EPSILON_INTERVAL",
                "gate_status": "BLOCKED_INTERVAL_NOT_ACCEPTED",
                "evidence": (
                    f"candidate epsilon_cross bound={float(mom1['epsilon_cross_candidate_bound']):.6g}; "
                    f"q choice gap fraction={q_choice_gap_fraction:.6g}"
                ),
                "remaining_obligation": "accept/carry epsilon interval after q observable decision",
            },
            {
                "gate_id": "N7331_QCHOICE5_FORMULA_FREEZE",
                "gate_status": "BLOCKED",
                "evidence": "q observable not selected, sign not frozen, epsilon interval not accepted",
                "remaining_obligation": "close review decisions before exact-transfer formula freeze",
            },
            {
                "gate_id": "N7331_QCHOICE6_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "gate reads only source-side derived packets, not rotation scores",
                "remaining_obligation": "none at endpoint-blindness level",
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

    formula_freeze_allowed = False
    endpoint_scores_allowed = False
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "observable_choice_status": "NGC7331_QWARP_OBSERVABLE_CHOICE_REVIEW_GATE_BUILT_FREEZE_BLOCKED",
                "q_centroid_mid": q_centroid_mid,
                "q_envelope_mid": q_envelope_mid,
                "q_envelope_to_centroid_ratio": q_ratio,
                "q_choice_gap_fraction": q_choice_gap_fraction,
                "mom1_context_available": True,
                "sigma_warp_sign_ready": bool_value(mom1["sigma_warp_sign_ready"]),
                "epsilon_cross_bound_ready": bool_value(mom1["epsilon_cross_bound_ready"]),
                "formula_freeze_allowed": formula_freeze_allowed,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "independent review must select q_warp observable and sign/epsilon handling"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    candidates.to_csv(DATA / "ngc7331_qwarp_observable_choice_candidates.csv", index=False)
    gates.to_csv(DATA / "ngc7331_qwarp_observable_choice_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_qwarp_observable_choice_summary.csv", index=False)

    report = [
        "# NGC7331 q_warp Observable-Choice Review Gate",
        "",
        "Status: `NGC7331_QWARP_OBSERVABLE_CHOICE_REVIEW_GATE_BUILT_FREEZE_BLOCKED`.",
        "",
        "This gate synthesizes THINGS q_warp first-pass measurements, threshold",
        "sensitivity, and MOM1 sign/cross-term context. It does not select an",
        "observable, does not freeze a formula, and does not score an endpoint.",
        "",
        "## Candidate observables",
        "",
        markdown_table(candidates),
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
    (REPORTS / "ngc7331_qwarp_observable_choice_review_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
