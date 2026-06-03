#!/usr/bin/env python3
"""Gate P0 visual-review responses before accepted-manifest promotion.

This gate is downstream of the visual-review response intake validator.  It
does not promote labels by itself and does not compute endpoint scores; it only
decides whether the P0 review responses may enter an independent accepted
morphology-manifest audit.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_response_to_manifest_promotion_gate_not_endpoint"

PROMOTION_REQUIREMENTS = [
    {
        "gate": "response_intake_complete",
        "decision_rule": "all P0 response rows pass the response intake validator",
    },
    {
        "gate": "forbidden_inputs_absent",
        "decision_rule": "no endpoint-derived forbidden input is present in review responses",
    },
    {
        "gate": "review_confidence_present",
        "decision_rule": "review confidence is supplied for every P0 row",
    },
    {
        "gate": "family_recommendation_present",
        "decision_rule": "residual-blind family recommendation is supplied for every P0 row",
    },
    {
        "gate": "history_memory_judgment_present",
        "decision_rule": "morphological memory/history proxy judgment is supplied for every P0 row",
    },
]


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def evaluate_gate(gate: str, validation: pd.DataFrame) -> tuple[str, int]:
    if gate == "response_intake_complete":
        blocked = validation[
            validation["validation_status"]
            != "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
        ]
        return ("PASS" if blocked.empty else "BLOCKED", len(blocked))
    if gate == "forbidden_inputs_absent":
        blocked = validation[validation["forbidden_input_detected"]]
        return ("PASS" if blocked.empty else "BLOCKED", len(blocked))
    if gate == "review_confidence_present":
        blocked = validation[
            validation["missing_required_fields"].str.contains("review_confidence")
        ]
        return ("PASS" if blocked.empty else "BLOCKED", len(blocked))
    if gate == "family_recommendation_present":
        blocked = validation[
            validation["missing_required_fields"].str.contains(
                "residual_blind_family_recommendation"
            )
        ]
        return ("PASS" if blocked.empty else "BLOCKED", len(blocked))
    if gate == "history_memory_judgment_present":
        blocked = validation[
            validation["missing_required_fields"].str.contains(
                "morphological_memory_history_proxy_judgment"
            )
        ]
        return ("PASS" if blocked.empty else "BLOCKED", len(blocked))
    raise ValueError(f"Unknown gate: {gate}")


def build_gates(validation: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for requirement in PROMOTION_REQUIREMENTS:
        status, blocked_rows = evaluate_gate(requirement["gate"], validation)
        rows.append(
            {
                "gate": requirement["gate"],
                "gate_status": status,
                "blocked_rows": blocked_rows,
                "decision_rule": requirement["decision_rule"],
                "accepted_manifest_audit_entry_allowed": status == "PASS",
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def write_report(gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    decision = summary["promotion_gate_decision"].iloc[0]
    if decision == "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT":
        verdict = [
            "The current package passes this P0 response gate. The responses may",
            "enter an independent accepted-manifest audit lane, but this still",
            "does not create full endpoint labels or endpoint scores.",
        ]
    else:
        verdict = [
            "The current package is correctly blocked because the P0 response intake",
            "is still pending. This is a review-readiness blocker, not a negative",
            "empirical result.",
            "This blocked promotion gate is not a negative empirical result.",
        ]
    lines = [
        "# P0 Response-to-Manifest Promotion Gate",
        "",
        "This gate decides whether completed P0 visual-review responses may enter",
        "an independent accepted morphology-manifest audit. It does not promote",
        "labels, does not create accepted morphology rows, and does not compute",
        "endpoint scores.",
        "",
        "This gate does not promote labels and does not compute endpoint scores.",
        "",
        "This promotion gate is not an endpoint score.",
        "",
        "## Verdict",
        "",
        f"Promotion gate decision: `{decision}`.",
        "",
        *verdict,
        "",
        "## Gate Status",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "A PASS here would only allow the responses to enter an independent",
        "accepted-manifest audit. It would not run a frozen endpoint, compare",
        "against MOND/RAR/TGP/Newtonian baselines, or validate Tau Core.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_response_to_manifest_promotion_gate.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    validation = pd.read_csv(DATA / "p0_visual_review_response_validation.csv")
    gates = build_gates(validation)
    blocked = gates[gates["gate_status"] == "BLOCKED"]
    decision = (
        "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
        if blocked.empty
        else "BLOCKED_RESPONSE_REVIEW_NOT_PROMOTABLE"
    )
    summary = pd.DataFrame(
        [
            {
                "promotion_gate_decision": decision,
                "n_gates": len(gates),
                "n_blocked_gates": len(blocked),
                "n_blocked_rows_total": int(blocked["blocked_rows"].sum()),
                "accepted_manifest_audit_entry_allowed": blocked.empty,
                "accepted_labels_created": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    gates.to_csv(DATA / "p0_response_to_manifest_promotion_gates.csv", index=False)
    summary.to_csv(DATA / "p0_response_to_manifest_promotion_summary.csv", index=False)
    write_report(gates, summary)
    print("PAPER8_P0_RESPONSE_TO_MANIFEST_PROMOTION_GATE_COMPLETE")


if __name__ == "__main__":
    main()
