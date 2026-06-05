#!/usr/bin/env python3
"""Review the NGC4088 H4 interaction-context source-history component.

This artifact fills the previously missing H4 source-history component from a
literature source already included in the reproducibility package. It is
residual-blind: it does not inspect observed rotation residuals or endpoint
scores. In this repository, "history" means morphology-carried source history,
not a separate fundamental Tau-side object.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_h4_interaction_context_review_not_endpoint"


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


def build_review() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    evidence = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "evidence_id": "H4_E1_GLOBAL_DISTORTION_CONTEXT",
                "source": "Verheijen & Sancisi 2001 Ursa Major HI data paper, Sec. 7.3",
                "source_locator": "local text lines near section 7.3",
                "evidence_summary": "NGC4088 is identified as a system with strong optical and kinematic distortion.",
                "component_support": 1.0,
                "forbidden_inputs_used": False,
            },
            {
                "galaxy": GALAXY,
                "evidence_id": "H4_E2_NGC4088_NOTE_ASYMMETRIC_WARP",
                "source": "Verheijen & Sancisi 2001 NGC4088 observing-results note",
                "source_locator": "local text NGC4088 note",
                "evidence_summary": "The NGC4088 note reports a strongly distorted disk, strong PV asymmetry, asymmetric warp, and asymmetric PA change.",
                "component_support": 1.0,
                "forbidden_inputs_used": False,
            },
            {
                "galaxy": GALAXY,
                "evidence_id": "H4_E3_COMPANION_CONTEXT",
                "source": "Verheijen & Sancisi 2001 NGC4085/NGC4088 notes",
                "source_locator": "local text NGC4085 and NGC4088 notes",
                "evidence_summary": "NGC4085 is listed 10 arcmin from NGC4088, and NGC4088 is described as a strongly disturbed nearby system.",
                "component_support": 1.0,
                "forbidden_inputs_used": False,
            },
        ]
    )
    h4_value = float(evidence["component_support"].mean())
    h4_uncertainty = 0.15
    review = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "component_id": "H4_INTERACTION_CONTEXT",
                "component_symbol": "h_env",
                "reviewed_component_value": h4_value,
                "review_uncertainty": h4_uncertainty,
                "review_status": "ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND",
                "review_basis": "residual-blind literature review of NGC4088 distortion, asymmetric warp, and companion/context evidence",
                "review_caveat": "source-history proxy only; not endpoint validation and not a claim of a unique dynamical cause",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    gates = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "gate_id": "H4_1_SOURCE_PRESENT",
                "gate_status": "PASS",
                "evidence": "local Ursa Major HI literature text includes NGC4088 distortion/asymmetry/context statements",
                "remaining_obligation": "preserve source citation in later manifest",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "H4_2_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "review does not read endpoint residuals or observed velocity scores",
                "remaining_obligation": "keep H4 fixed before endpoint scoring",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "H4_3_SOURCE_HISTORY_INTERPRETATION",
                "gate_status": "PASS",
                "evidence": "history is morphology-carried interaction/warp/asymmetry context, not a new fundamental object",
                "remaining_obligation": "avoid treating h_env as an endpoint-fitted parameter",
            },
            {
                "galaxy": GALAXY,
                "gate_id": "H4_4_NUMERIC_BOUND_USE",
                "gate_status": "PASS",
                "evidence": f"h_env={h4_value:.6g} with source-review uncertainty {h4_uncertainty:.6g}",
                "remaining_obligation": "carry uncertainty in epsilon_cross interpretation",
            },
        ]
    )
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "review_id": "NGC4088_H4_INTERACTION_CONTEXT_SOURCE_REVIEW",
                "accepted_h4_interaction_context": h4_value,
                "accepted_h4_uncertainty": h4_uncertainty,
                "n_evidence_rows": len(evidence),
                "n_pass": int((gates["gate_status"] == "PASS").sum()),
                "n_blocked": int((gates["gate_status"] == "BLOCKED").sum()),
                "h4_review_status": "H4_INTERACTION_CONTEXT_ACCEPTED_SOURCE_REVIEWED",
                "source_history_caveat_status": "H4_CAVEAT_RESOLVED_FOR_PROTOCOL_BOUND",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return evidence, review, gates, summary


def write_report(
    evidence: pd.DataFrame,
    review: pd.DataFrame,
    gates: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 H4 Interaction-Context Review",
        "",
        "This residual-blind source review fills the previously missing H4",
        "interaction/context component for the NGC4088 source-history proxy.",
        "Here, source history means morphology-carried evidence of previous or",
        "ongoing disturbance; it is not a new fundamental Tau object.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Evidence",
        "",
        markdown_table(evidence),
        "",
        "## Review",
        "",
        markdown_table(review),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The accepted H4 value authorizes only a residual-blind protocol input",
        "for source-bound calculations. It is not endpoint validation and does",
        "not identify a unique physical interaction history.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_h4_interaction_context_review.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    evidence, review, gates, summary = build_review()
    evidence.to_csv(DATA / "s4g75_ngc4088_h4_interaction_context_evidence.csv", index=False)
    review.to_csv(DATA / "s4g75_ngc4088_h4_interaction_context_review.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_h4_interaction_context_review_gate.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_h4_interaction_context_review_summary.csv",
        index=False,
    )
    write_report(evidence, review, gates, summary)
    print("PAPER8_NGC4088_H4_INTERACTION_CONTEXT_REVIEW_COMPLETE")


if __name__ == "__main__":
    main()
