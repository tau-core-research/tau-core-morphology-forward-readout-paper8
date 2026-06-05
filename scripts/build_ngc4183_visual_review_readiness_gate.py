#!/usr/bin/env python3
"""Gate whether the NGC4183 tilted-ring review packet is visually review-ready."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_visual_review_readiness_gate_not_endpoint"
GALAXY = "NGC4183"


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

    packet = pd.read_csv(DATA / "ngc4183_tilted_ring_independent_review_summary.csv").iloc[0]
    response = pd.read_csv(DATA / "ngc4183_tilted_ring_review_response_summary.csv").iloc[0]
    visual_sources = pd.read_csv(
        DATA / "ngc4183_tilted_ring_independent_review_visual_sources.csv"
    )

    visual_sources["exists"] = visual_sources["path"].map(lambda p: Path(str(p)).exists())
    all_visual_sources_present = bool(visual_sources["exists"].all())
    response_received = bool(response["response_received"])

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_VRR_G1_PACKET_EXISTS",
                "gate_status": "PASS",
                "evidence": str(packet["review_packet_status"]),
                "freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none",
            },
            {
                "gate_id": "N4183_VRR_G2_VISUAL_SOURCES",
                "gate_status": "PASS" if all_visual_sources_present else "BLOCKED",
                "evidence": f"{int(visual_sources['exists'].sum())}/{len(visual_sources)} visual sources present",
                "freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none" if all_visual_sources_present else "render missing page/crop sources",
            },
            {
                "gate_id": "N4183_VRR_G3_RESPONSE_RECEIVED",
                "gate_status": "PASS" if response_received else "BLOCKED",
                "evidence": str(response["review_response_intake_status"]),
                "freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": (
                    "none at visual-packet level; see review-response intake for acceptance/freeze state"
                    if response_received
                    else "independent reviewer response still required"
                ),
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    review_ready = all_visual_sources_present
    freeze_allowed = False
    summary = pd.DataFrame(
        [
            {
                "visual_review_readiness_status": (
                    "NGC4183_VISUAL_REVIEW_PACKET_READY_RESPONSE_REQUIRED"
                    if review_ready and not response_received
                    else "NGC4183_VISUAL_REVIEW_PACKET_READY_RESPONSE_RECEIVED"
                    if review_ready and response_received
                    else "NGC4183_VISUAL_REVIEW_PACKET_BLOCKED_MISSING_SOURCES"
                ),
                "galaxy": GALAXY,
                "n_visual_sources": len(visual_sources),
                "n_visual_sources_present": int(visual_sources["exists"].sum()),
                "visual_review_packet_ready": review_ready,
                "review_response_received": response_received,
                "formula_freeze_allowed": freeze_allowed,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "fill_independent_review_response" if not response_received else "review_response_intake",
            }
        ]
    )

    visual_sources.to_csv(DATA / "ngc4183_visual_review_readiness_sources.csv", index=False)
    gates.to_csv(DATA / "ngc4183_visual_review_readiness_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_visual_review_readiness_summary.csv", index=False)

    report = f"""# NGC4183 Visual Review Readiness Gate

Status: `{summary.iloc[0]["visual_review_readiness_status"]}`

This gate checks whether the NGC4183 tilted-ring review packet has enough visual
source material for an independent reviewer.  It does not accept the review and
does not authorize formula freeze.

## Summary

{markdown_table(summary)}

## Visual Sources

{markdown_table(visual_sources)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Interpretation

The visual review packet is ready if all rendered/cropped source images exist.
If a response has already been received, this gate remains informational only
and the real state moves downstream to review-response intake, freeze, and any
later accepted-control scoring. For NGC4183 that downstream lane has now
already run to a narrow accepted null-control interval endpoint, so this visual
packet remains as audit-trail support rather than as a live blocker.
"""
    (REPORTS / "ngc4183_visual_review_readiness_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
