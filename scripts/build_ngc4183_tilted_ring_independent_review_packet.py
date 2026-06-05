#!/usr/bin/env python3
"""Build an independent review packet for NGC4183 tilted-ring extraction."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
LIT = ROOT / "data" / "external" / "literature"
CLAIM_BOUNDARY = "ngc4183_tilted_ring_independent_review_packet_not_endpoint"
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


def source_excerpt() -> str:
    text_path = LIT / "2001_verheijen_sancisi_ursa_major_hi.txt"
    text = text_path.read_text(encoding="utf-8", errors="replace")
    start = text.find("N4183\n10")
    end = text.find("N4217", start)
    if start == -1 or end == -1:
        return "N4183 Table 4 OCR excerpt not found."
    excerpt = text[start:end]
    lines = [line.strip() for line in excerpt.splitlines() if line.strip()]
    return " / ".join(lines)


def load_or_initialize_response_template() -> pd.DataFrame:
    template_path = DATA / "ngc4183_tilted_ring_independent_review_response_template.csv"
    default = pd.DataFrame(
        [
            {
                "reviewer": "independent_reviewer",
                "date": "YYYY-MM-DD",
                "source_identity_decision": "",
                "radius_series_decision": "",
                "orientation_series_decision": "",
                "velocity_columns_decision": "",
                "upper_bound_conclusion_decision": "",
                "corrections": "",
                "review_verdict": "",
                "may_freeze_null_control_after_review": False,
            }
        ]
    )
    if not template_path.exists():
        return default
    existing = pd.read_csv(template_path)
    if existing.empty:
        return default
    for column in default.columns:
        if column not in existing.columns:
            existing[column] = default.iloc[0][column]
    return existing[default.columns]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    profile = pd.read_csv(DATA / "ngc4183_tilted_ring_orientation_profile.csv")
    profile_summary = pd.read_csv(
        DATA / "ngc4183_tilted_ring_orientation_profile_summary.csv"
    ).iloc[0]
    weak_summary = pd.read_csv(DATA / "ngc4183_weak_projection_control_summary.csv").iloc[0]
    visual_sources = pd.DataFrame(
        [
            {
                "visual_source_id": "N4183_TABLE4_FULL_PAGE",
                "path": str(
                    LIT
                    / "2001_verheijen_sancisi_pages/ngc4183_review/page-013.png"
                ),
                "role": "full rendered PDF page containing NGC4183 Table 4 rows",
                "review_use": "check context and column headers",
            },
            {
                "visual_source_id": "N4183_TABLE4_FULL_COLUMN_CROP",
                "path": str(
                    LIT
                    / "2001_verheijen_sancisi_pages/ngc4183_review/ngc4183_table4_full_column_crop.png"
                ),
                "role": "focused crop containing NGC4183 tilted-ring rows",
                "review_use": "primary visual transcription check",
            },
            {
                "visual_source_id": "N4183_OBSERVING_PARAMETERS_PAGE",
                "path": str(
                    LIT / "2001_verheijen_sancisi_pages/page_84-084.png"
                ),
                "role": "rendered page with NGC4183 H I parameters and warp note",
                "review_use": "check PA=347, i=83, H I diameter=6.1 arcmin, slight outer warp note",
            },
        ]
    )

    review_items = pd.DataFrame(
        [
            {
                "review_item": "source_identity",
                "field_or_range": "Verheijen & Sancisi 2001 / NGC4183 / Table 4",
                "current_value": "local PDF + OCR cache",
                "review_question": "Does the cited table block correspond to NGC4183 tilted-ring rows?",
                "required_response": "accept/reject/correct",
            },
            {
                "review_item": "radius_series",
                "field_or_range": "radius_arcsec",
                "current_value": f"{int(profile['radius_arcsec'].min())}..{int(profile['radius_arcsec'].max())} arcsec, n={len(profile)}",
                "review_question": "Are all radial rings transcribed correctly, including 229 and 241 arcsec rows?",
                "required_response": "accept/reject/correct",
            },
            {
                "review_item": "orientation_series",
                "field_or_range": "inclination_deg, pa_deg",
                "current_value": (
                    f"i={profile['inclination_deg'].min()}..{profile['inclination_deg'].max()} deg; "
                    f"PA={profile['pa_deg'].min()}..{profile['pa_deg'].max()} deg"
                ),
                "review_question": "Is the near-constant i=82 deg and PA=346..349 deg transcription correct?",
                "required_response": "accept/reject/correct",
            },
            {
                "review_item": "velocity_columns_not_endpoint",
                "field_or_range": "Vrot app/rec/ave",
                "current_value": "transcribed for source consistency only",
                "review_question": "Do not use Vrot columns for residual fitting; only confirm table transcription.",
                "required_response": "accept/reject/correct",
            },
            {
                "review_item": "upper_bound_conclusion",
                "field_or_range": "gamma_proj upper bound",
                "current_value": f"{float(weak_summary['gamma_projection_upper_bound']):.8f}",
                "review_question": "If orientation series is accepted, does the weak-control conclusion follow?",
                "required_response": "accept/reject/correct",
            },
        ]
    )

    response_template = load_or_initialize_response_template()

    response_received = bool(
        str(response_template.iloc[0].get("review_verdict", "")).strip()
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_REVIEW_G1_PACKET_CREATED",
                "gate_status": "PASS",
                "evidence": "profile, source excerpt, and response template written",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "independent response required",
            },
            {
                "gate_id": "N4183_REVIEW_G2_FREEZE_ALLOWED",
                "gate_status": "BLOCKED",
                "evidence": (
                    "independent review response is present but freeze remains separate"
                    if response_received
                    else "no independent review response yet"
                ),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": (
                    "review intake determines whether source-only acceptance or freeze authorization applies"
                    if response_received
                    else "reviewer must accept/correct OCR-derived profile"
                ),
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "review_packet_status": "NGC4183_TILTED_RING_REVIEW_PACKET_CREATED_FREEZE_BLOCKED",
                "galaxy": GALAXY,
                "profile_status": str(profile_summary["tilted_ring_profile_status"]),
                "weak_control_status": str(weak_summary["weak_control_preflight_status"]),
                "n_review_items": len(review_items),
                "review_response_received": response_received,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "review_response_intake" if response_received else "fill_independent_review_response",
            }
        ]
    )

    review_items.to_csv(DATA / "ngc4183_tilted_ring_independent_review_items.csv", index=False)
    visual_sources.to_csv(DATA / "ngc4183_tilted_ring_independent_review_visual_sources.csv", index=False)
    response_template.to_csv(
        DATA / "ngc4183_tilted_ring_independent_review_response_template.csv",
        index=False,
    )
    gates.to_csv(DATA / "ngc4183_tilted_ring_independent_review_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_tilted_ring_independent_review_summary.csv", index=False)

    report = f"""# NGC4183 Tilted-Ring Independent Review Packet

Status: `{summary.iloc[0]["review_packet_status"]}`

This packet is for independent source review.  It does not freeze a formula and
does not authorize endpoint scoring.

## Summary

{markdown_table(summary)}

## Review Items

{markdown_table(review_items)}

## Response Template

{markdown_table(response_template)}

## Visual Sources

{markdown_table(visual_sources)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Packet State

The packet preserves the latest response template if one has already been
filled. A filled source-review response does not by itself imply freeze
authorization.

## Source Pointers

- PDF: `{LIT / "2001_verheijen_sancisi_ursa_major_hi.pdf"}`
- OCR text: `{LIT / "2001_verheijen_sancisi_ursa_major_hi.txt"}`
- Full rendered table page: `{LIT / "2001_verheijen_sancisi_pages/ngc4183_review/page-013.png"}`
- NGC4183 table crop: `{LIT / "2001_verheijen_sancisi_pages/ngc4183_review/ngc4183_table4_full_column_crop.png"}`
- Observing-parameters page: `{LIT / "2001_verheijen_sancisi_pages/page_84-084.png"}`
- Extracted profile: `{DATA / "ngc4183_tilted_ring_orientation_profile.csv"}`

## OCR Excerpt To Review

> {source_excerpt()[:2400]}

## Current Derived Consequence

If the orientation transcription is accepted, the source-side projection
correction remains a weak/null-control case:

```text
max |Delta PA| = {float(profile_summary["max_abs_pa_drift_deg"]):.3f} deg
max |Delta i|  = {float(profile_summary["max_abs_inclination_drift_deg"]):.3f} deg
gamma_proj <= {float(weak_summary["gamma_projection_upper_bound"]):.8f}
|Delta v|/v <= {float(weak_summary["max_velocity_fractional_change"]):.8f}
```
"""
    (REPORTS / "ngc4183_tilted_ring_independent_review_packet.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
