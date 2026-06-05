#!/usr/bin/env python3
"""Build a residual-blind WHISP overview extraction review packet for NGC4088.

The WHISP UGC 7081 overview is not a FITS/source-coordinate cube, but it is a
source-provenance H I overview with an arcmin offset axis in the position-
velocity panel and sky-coordinate axes in the map panels.  This packet turns
that cached source into a reviewable B1 extraction task.  It does not accept
x_w and does not score an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CACHE = ROOT / "data" / "external" / "literature" / "ngc4088_source_native_hi_route"
OVERVIEW = CACHE / "whisp_ugc7081_overview.gif"
OVERLAY = CACHE / "whisp_ugc7081_overview_extraction_overlay.png"
CLAIM_BOUNDARY = "ngc4088_b1_whisp_overview_extraction_review_not_endpoint"


PANELS = [
    {
        "panel_id": "P1_OPTICAL_SKY",
        "panel_role": "context_only",
        "x0": 90,
        "y0": 93,
        "x1": 267,
        "y1": 267,
        "review_use": "optical orientation/context; not sufficient for x_w",
    },
    {
        "panel_id": "P3_POSITION_VELOCITY_MAJOR_AXIS",
        "panel_role": "primary_arcmin_onset_candidate",
        "x0": 533,
        "y0": 94,
        "x1": 707,
        "y1": 267,
        "review_use": "direct arcmin offset axis along major axis; candidate source for side onsets",
    },
    {
        "panel_id": "P5_TOTAL_HI_30_ARCSEC",
        "panel_role": "hi_morphology_cross_check",
        "x0": 313,
        "y0": 319,
        "x1": 487,
        "y1": 493,
        "review_use": "30 arcsec total HI morphology and sky-coordinate cross-check",
    },
    {
        "panel_id": "P6_TOTAL_HI_60_ARCSEC",
        "panel_role": "hi_morphology_cross_check",
        "x0": 533,
        "y0": 319,
        "x1": 707,
        "y1": 493,
        "review_use": "60 arcsec total HI morphology and sky-coordinate cross-check",
    },
    {
        "panel_id": "P8_IWM_VELOCITY_30_ARCSEC",
        "panel_role": "velocity_field_cross_check",
        "x0": 313,
        "y0": 533,
        "x1": 487,
        "y1": 705,
        "review_use": "30 arcsec velocity-field orientation/asymmetry cross-check",
    },
    {
        "panel_id": "P9_IWM_VELOCITY_60_ARCSEC",
        "panel_role": "velocity_field_cross_check",
        "x0": 533,
        "y0": 533,
        "x1": 707,
        "y1": 705,
        "review_use": "60 arcsec velocity-field orientation/asymmetry cross-check",
    },
]


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def make_overlay(panels: pd.DataFrame) -> None:
    image = Image.open(OVERVIEW).convert("RGB")
    draw = ImageDraw.Draw(image)
    colors = {
        "primary_arcmin_onset_candidate": (255, 80, 0),
        "hi_morphology_cross_check": (0, 170, 255),
        "velocity_field_cross_check": (100, 220, 80),
        "context_only": (180, 180, 180),
    }
    for _, row in panels.iterrows():
        color = colors.get(row["panel_role"], (255, 255, 0))
        box = [int(row["x0"]), int(row["y0"]), int(row["x1"]), int(row["y1"])]
        draw.rectangle(box, outline=color, width=3)
        draw.text((box[0] + 4, box[1] + 4), row["panel_id"], fill=color)
    image.save(OVERLAY)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)

    acquisition = pd.read_csv(DATA / "ngc4088_b1_original_hi_data_acquisition_summary.csv").iloc[0]
    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    hi_radius_arcmin = float(xw["hi_radius_arcmin"])
    first_pass_xw = float(xw["x_warp_onset"])
    tolerance_xw = max(float(xw["x_warp_uncertainty"]), 0.05)
    tolerance_arcmin = hi_radius_arcmin * tolerance_xw

    overview_exists = OVERVIEW.exists()
    panels = pd.DataFrame(PANELS)
    panels["overview_image"] = str(OVERVIEW.relative_to(ROOT))
    panels["uses_vobs_or_residual"] = False
    panels["endpoint_scores_allowed"] = False
    panels["claim_boundary"] = CLAIM_BOUNDARY
    if overview_exists:
        make_overlay(panels)

    packet = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "packet_id": "NGC4088_WHISP_OVERVIEW_ARCMIN_EXTRACTION_REVIEW_PACKET_V1",
                "source_product": str(OVERVIEW.relative_to(ROOT)),
                "source_product_status": (
                    "WHISP_GRAPHICAL_OVERVIEW_CACHED_REVIEW_READY"
                    if overview_exists
                    else "WHISP_GRAPHICAL_OVERVIEW_MISSING"
                ),
                "primary_panel": "P3_POSITION_VELOCITY_MAJOR_AXIS",
                "primary_axis": "Offset from center (arcmin)",
                "hi_radius_arcmin": hi_radius_arcmin,
                "first_pass_x_w": first_pass_xw,
                "acceptance_tolerance_x_w": tolerance_xw,
                "acceptance_tolerance_arcmin": tolerance_arcmin,
                "forbidden_inputs": "vobs;rotation_residual;endpoint_score;fit_rank;required_S_tau_diagnostic",
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    response_template = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "packet_id": packet.iloc[0]["packet_id"],
                "reviewer_or_method_id": "PENDING_WHISP_OVERVIEW_REVIEW",
                "review_timestamp_utc": "PENDING_WHISP_OVERVIEW_REVIEW",
                "source_product_used": str(OVERVIEW.relative_to(ROOT)),
                "source_product_hash": "PENDING_OPTIONAL_HASH",
                "side_a_onset_offset_arcmin": "PENDING_WHISP_OVERVIEW_REVIEW",
                "side_b_onset_offset_arcmin": "PENDING_WHISP_OVERVIEW_REVIEW",
                "side_combination_rule": "mean(abs(side_a), abs(side_b)) unless one side is explicitly flagged unusable",
                "combined_onset_arcmin": "PENDING_WHISP_OVERVIEW_REVIEW",
                "uncertainty_arcmin": "PENDING_WHISP_OVERVIEW_REVIEW",
                "x_w_review": "PENDING_WHISP_OVERVIEW_REVIEW",
                "agrees_with_first_pass_within_tolerance": "PENDING_WHISP_OVERVIEW_REVIEW",
                "review_notes": "PENDING_WHISP_OVERVIEW_REVIEW",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    obligations = pd.DataFrame(
        [
            {
                "obligation_id": "WHEX1_SOURCE_PRODUCT_CACHED",
                "status": "PASS" if overview_exists else "BLOCKED",
                "requirement": "WHISP UGC7081 overview GIF is cached with provenance",
                "acceptance_condition": "source_product_status=WHISP_GRAPHICAL_OVERVIEW_CACHED_REVIEW_READY",
            },
            {
                "obligation_id": "WHEX2_ARCMIN_AXIS_PRESENT",
                "status": "PASS" if overview_exists else "BLOCKED",
                "requirement": "position-velocity panel has Offset from center (arcmin) axis",
                "acceptance_condition": "reviewer uses P3 axis rather than endpoint residuals",
            },
            {
                "obligation_id": "WHEX3_RESPONSE_FILLED",
                "status": "PENDING",
                "requirement": "reviewer fills side-A/side-B onset offsets and uncertainty",
                "acceptance_condition": "numeric arcmin offsets and uncertainty present",
            },
            {
                "obligation_id": "WHEX4_TOLERANCE_OR_INTERVAL",
                "status": "PENDING",
                "requirement": "x_w review agrees with first pass or freezes an uncertainty interval",
                "acceptance_condition": (
                    f"|x_w_review - {first_pass_xw:.6g}| <= {tolerance_xw:.6g}, "
                    "or source-side interval is frozen before formula use"
                ),
            },
            {
                "obligation_id": "WHEX5_INDEPENDENT_OR_FROZEN_METHOD",
                "status": "PENDING",
                "requirement": "measurement is performed by independent reviewer or frozen image script",
                "acceptance_condition": "reviewer_or_method_id is not the first-pass digitizer",
            },
        ]
    )
    obligations["uses_vobs_or_residual"] = False
    obligations["endpoint_scores_allowed"] = False
    obligations["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "whisp_overview_extraction_status": (
                    "WHISP_OVERVIEW_EXTRACTION_PACKET_READY_RESPONSE_PENDING"
                    if overview_exists
                    else "WHISP_OVERVIEW_EXTRACTION_PACKET_BLOCKED_SOURCE_MISSING"
                ),
                "galaxy": "NGC4088",
                "b1_resolution_status": "B1_NOT_RESOLVED_WHISP_OVERVIEW_REVIEW_PENDING",
                "whisp_graphical_overview_cached": overview_exists,
                "original_hi_data_audit_status": acquisition["original_hi_data_audit_status"],
                "n_review_panels": len(panels),
                "n_pending_obligations": int(obligations["status"].eq("PENDING").sum()),
                "accepted_x_w_for_formula_freeze": False,
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": "fill the WHISP overview extraction response or obtain direct FITS/source-coordinate H I data",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    panels.to_csv(DATA / "ngc4088_b1_whisp_overview_extraction_panels.csv", index=False)
    packet.to_csv(DATA / "ngc4088_b1_whisp_overview_extraction_packet.csv", index=False)
    response_template.to_csv(
        DATA / "ngc4088_b1_whisp_overview_extraction_response_template.csv", index=False
    )
    obligations.to_csv(DATA / "ngc4088_b1_whisp_overview_extraction_obligations.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b1_whisp_overview_extraction_summary.csv", index=False)

    report = [
        "# NGC4088 WHISP Overview Extraction Review Packet",
        "",
        "This packet turns the cached WHISP UGC 7081 graphical H I overview into a",
        "residual-blind B1 review task. It is not a formula freeze and not an",
        "endpoint score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Packet",
        "",
        markdown_table(packet),
        "",
        "## Review Panels",
        "",
        markdown_table(panels[["panel_id", "panel_role", "review_use", "overview_image"]]),
        "",
        "## Obligations",
        "",
        markdown_table(obligations),
        "",
        "## Response Template",
        "",
        markdown_table(response_template),
        "",
        "## Interpretation",
        "",
        "The WHISP overview gives a stronger source-provenance route than the printed",
        "paper crop because the position-velocity panel includes an arcmin offset",
        "axis. B1 still remains open: the packet must be filled by an independent",
        "reviewer or frozen extraction method, and the resulting x_w must either",
        "agree with the first-pass value within tolerance or produce a frozen",
        "source-side uncertainty interval before formula use.",
        "",
    ]
    (REPORTS / "ngc4088_b1_whisp_overview_extraction_review_packet.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
