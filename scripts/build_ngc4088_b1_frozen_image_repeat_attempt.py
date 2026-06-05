#!/usr/bin/env python3
"""Run a frozen image-analysis repeat attempt for NGC4088 B1.

This script is deliberately conservative.  It uses only the frozen page-76
channel-map ROI and worksheet grid to extract panel-level dark-contour geometry.
It does not read the rotation curve, endpoint residuals, fit ranks, or any
required-S_tau diagnostic.  Because the channel-map panel lacks a robust
machine-readable source-native radial calibration and the printed contours mix
labels/noise with source structure, this repeat attempt is allowed to support
the B1 review packet but not to close B1 by itself.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
PAGE_DIR = ROOT / "data" / "external" / "literature" / "2001_verheijen_sancisi_pages"
ROI = PAGE_DIR / "ngc4088_page_76_channel_maps_roi.png"
OVERLAY = PAGE_DIR / "ngc4088_page_76_frozen_image_repeat_overlay.png"
CLAIM_BOUNDARY = "ngc4088_b1_frozen_image_repeat_attempt_not_endpoint"

GRAY_THRESHOLD = 150
PANEL_MARGIN_PX = 8
PANEL_TOP_LABEL_EXCLUSION_PX = 34
MIN_COMPONENT_AREA_PX = 25


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


def pca_component(points_yx: np.ndarray) -> tuple[float, float, float, float]:
    centroid_yx = points_yx.mean(axis=0)
    centered = points_yx - centroid_yx
    cov = centered.T @ centered / max(len(points_yx) - 1, 1)
    vals, vecs = np.linalg.eigh(cov)
    order = np.argsort(vals)[::-1]
    vals = vals[order]
    vec = vecs[:, order[0]]
    angle_deg = float(np.degrees(np.arctan2(vec[0], vec[1])) % 180.0)
    elongation = float(np.sqrt(max(vals[0], 1.0e-12) / max(vals[1], 1.0e-12)))
    return float(centroid_yx[1]), float(centroid_yx[0]), angle_deg, elongation


def angular_abs_delta(a_deg: float, b_deg: float) -> float:
    delta = abs((a_deg - b_deg + 90.0) % 180.0 - 90.0)
    return float(delta)


def analyze_panels() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    worksheet = pd.read_csv(DATA / "s4g75_ngc4088_channel_map_digitization_worksheet.csv")
    raw = Image.open(ROI).convert("L")
    image = np.asarray(raw)

    rows = []
    for _, panel in worksheet.iterrows():
        if panel["panel_status"] != "MEASUREMENT_TARGET":
            continue
        x0 = int(panel["roi_x0_px"]) + PANEL_MARGIN_PX
        y0 = int(panel["roi_y0_px"]) + PANEL_TOP_LABEL_EXCLUSION_PX
        x1 = int(panel["roi_x1_px"]) - PANEL_MARGIN_PX
        y1 = int(panel["roi_y1_px"]) - PANEL_MARGIN_PX
        crop = image[y0:y1, x0:x1]
        dark = crop < GRAY_THRESHOLD
        labels, n_components = ndimage.label(dark)
        objects = ndimage.find_objects(labels)
        components = []
        for label_id, slc in enumerate(objects, start=1):
            if slc is None:
                continue
            component_points = np.argwhere(labels[slc] == label_id)
            area = int(len(component_points))
            if area < MIN_COMPONENT_AREA_PX:
                continue
            component_points[:, 0] += slc[0].start
            component_points[:, 1] += slc[1].start
            cx_local, cy_local, angle, elongation = pca_component(component_points)
            components.append(
                {
                    "area_px": area,
                    "cx_px": cx_local + x0,
                    "cy_px": cy_local + y0,
                    "axis_angle_deg_image": angle,
                    "elongation": elongation,
                }
            )
        if components:
            best = sorted(
                components,
                key=lambda item: (item["area_px"], item["elongation"]),
                reverse=True,
            )[0]
            extraction_status = "COMPONENT_EXTRACTED"
        else:
            best = {
                "area_px": 0,
                "cx_px": np.nan,
                "cy_px": np.nan,
                "axis_angle_deg_image": np.nan,
                "elongation": np.nan,
            }
            extraction_status = "NO_STABLE_COMPONENT"
        rows.append(
            {
                "galaxy": "NGC4088",
                "panel_id": panel["panel_id"],
                "row": int(panel["row"]),
                "col": int(panel["col"]),
                "channel_velocity_kms": float(panel["channel_velocity_kms"]),
                "n_raw_dark_components": int(n_components),
                "n_components_after_area_filter": len(components),
                "largest_component_area_px": best["area_px"],
                "component_centroid_x_px": best["cx_px"],
                "component_centroid_y_px": best["cy_px"],
                "axis_angle_deg_image": best["axis_angle_deg_image"],
                "elongation": best["elongation"],
                "extraction_status": extraction_status,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    panel_geometry = pd.DataFrame(rows)
    good = panel_geometry[
        panel_geometry["extraction_status"].eq("COMPONENT_EXTRACTED")
        & panel_geometry["elongation"].ge(1.2)
    ].copy()
    central = good[good["row"].isin([3, 4])]
    if len(central) >= 2:
        central_axis = float(np.median(central["axis_angle_deg_image"]))
    elif len(good):
        central_axis = float(np.median(good["axis_angle_deg_image"]))
    else:
        central_axis = np.nan
    if np.isfinite(central_axis):
        panel_geometry["angle_delta_from_central_deg"] = panel_geometry[
            "axis_angle_deg_image"
        ].map(
            lambda value: angular_abs_delta(float(value), central_axis)
            if pd.notna(value)
            else np.nan
        )
    else:
        panel_geometry["angle_delta_from_central_deg"] = np.nan

    candidate = panel_geometry[
        panel_geometry["angle_delta_from_central_deg"].ge(35.0)
        & panel_geometry["row"].isin([1, 2, 5, 6])
    ].copy()
    if len(candidate):
        repeat_signal_status = "WARP_LIKE_PA_DEPARTURE_DETECTED"
    else:
        repeat_signal_status = "NO_STABLE_WARP_ONSET_FROM_IMAGE_REPEAT"

    obligations = pd.DataFrame(
        [
            {
                "obligation_id": "B1R1_COMPONENT_SELECTION_STABILITY",
                "obligation_status": "PARTIAL",
                "current_evidence": f"{len(good)} panels have extracted elongated dark-contour components",
                "why_not_resolved": "printed labels, contour noise, and panel blending can still affect the selected component",
            },
            {
                "obligation_id": "B1R2_SOURCE_NATIVE_RADIAL_CALIBRATION",
                "obligation_status": "OPEN",
                "current_evidence": "panel grid and HI diameter are frozen, but per-panel source-native radius ticks are not machine-calibrated",
                "why_not_resolved": "cannot convert image-component departure to an accepted arcmin onset without reviewer/radial calibration",
            },
            {
                "obligation_id": "B1R3_INDEPENDENT_ACCEPTANCE",
                "obligation_status": "OPEN",
                "current_evidence": "automated repeat attempt is generated by the package, not an independent reviewer",
                "why_not_resolved": "B1 requires independent review response or an accepted frozen repeat with source-native calibration",
            },
        ]
    )
    obligations["endpoint_scores_allowed"] = False
    obligations["uses_vobs_or_residual"] = False
    obligations["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "repeat_attempt_status": "FROZEN_IMAGE_REPEAT_ATTEMPT_COMPLETE_INCONCLUSIVE",
                "b1_resolution_status": "B1_NOT_RESOLVED_IMAGE_REPEAT_INCONCLUSIVE",
                "roi_png": str(ROI.relative_to(ROOT)),
                "overlay_png": str(OVERLAY.relative_to(ROOT)),
                "gray_threshold": GRAY_THRESHOLD,
                "min_component_area_px": MIN_COMPONENT_AREA_PX,
                "n_panels_analyzed": len(panel_geometry),
                "n_elongated_components": len(good),
                "central_axis_angle_deg_image": central_axis,
                "repeat_signal_status": repeat_signal_status,
                "accepted_x_w_from_repeat_available": False,
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "complete independent reviewer response or add source-native radial "
                    "calibration before accepting an x_w repeat"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return panel_geometry, obligations, summary


def build_overlay(panel_geometry: pd.DataFrame) -> None:
    im = Image.open(ROI).convert("RGB")
    draw = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("Arial.ttf", 12)
    except OSError:
        font = ImageFont.load_default()
    for _, row in panel_geometry.iterrows():
        if pd.isna(row["component_centroid_x_px"]):
            continue
        cx = float(row["component_centroid_x_px"])
        cy = float(row["component_centroid_y_px"])
        angle = float(row["axis_angle_deg_image"])
        length = 36.0
        dx = np.cos(np.radians(angle)) * length / 2.0
        dy = np.sin(np.radians(angle)) * length / 2.0
        color = (20, 100, 220)
        if pd.notna(row["angle_delta_from_central_deg"]) and row[
            "angle_delta_from_central_deg"
        ] >= 35.0:
            color = (220, 120, 20)
        draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=color)
        draw.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=color, width=2)
        draw.text((cx + 5, cy + 5), str(row["panel_id"]), fill=color, font=font)
    im.save(OVERLAY)


def write_report(
    panel_geometry: pd.DataFrame, obligations: pd.DataFrame, summary: pd.DataFrame
) -> None:
    lines = [
        "# NGC4088 B1 Frozen Image-Analysis Repeat Attempt",
        "",
        "This is a residual-blind automated repeat attempt for the NGC4088 `x_w`",
        "digitization gate. It uses only the frozen page-76 channel-map ROI and",
        "the frozen worksheet grid. It does not read observed rotation residuals,",
        "endpoint scores, fit ranks, or required-S_tau diagnostics.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Obligations",
        "",
        markdown_table(obligations),
        "",
        "## Panel Geometry",
        "",
        markdown_table(
            panel_geometry[
                [
                    "panel_id",
                    "channel_velocity_kms",
                    "largest_component_area_px",
                    "axis_angle_deg_image",
                    "elongation",
                    "angle_delta_from_central_deg",
                    "extraction_status",
                ]
            ]
        ),
        "",
        "## Interpretation",
        "",
        "The repeat can provide a reproducible source-image diagnostic, but it is",
        "not strong enough to accept a new `x_w` value. The blocking reason is",
        "specific rather than conceptual: the printed channel-map crop needs either",
        "an independent reviewer measurement or a stronger source-native radial",
        "calibration before the image repeat can close B1.",
        "",
    ]
    (REPORTS / "ngc4088_b1_frozen_image_repeat_attempt.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    panel_geometry, obligations, summary = analyze_panels()
    build_overlay(panel_geometry)
    panel_geometry.to_csv(DATA / "ngc4088_b1_frozen_image_repeat_panel_geometry.csv", index=False)
    obligations.to_csv(DATA / "ngc4088_b1_frozen_image_repeat_obligations.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b1_frozen_image_repeat_summary.csv", index=False)
    write_report(panel_geometry, obligations, summary)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
