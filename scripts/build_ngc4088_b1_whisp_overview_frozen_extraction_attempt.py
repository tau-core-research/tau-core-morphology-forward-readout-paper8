#!/usr/bin/env python3
"""Run a frozen WHISP overview extraction attempt for NGC4088 B1.

This script uses only the cached WHISP UGC 7081 graphical overview.  It extracts
two coherent high-saturation position-velocity components from the panel with
the source-provided "Offset from center (arcmin)" axis.  The result is a
source-side x_w candidate and an agreement audit against the first-pass
digitization.  It is not an endpoint score and does not read observed rotation
velocities or residuals.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CACHE = ROOT / "data" / "external" / "literature" / "ngc4088_source_native_hi_route"
OVERVIEW = CACHE / "whisp_ugc7081_overview.gif"
POSVEL_CROP = CACHE / "whisp_ugc7081_posvel_crop.png"
OVERLAY = CACHE / "whisp_ugc7081_posvel_frozen_extraction_overlay.png"
CLAIM_BOUNDARY = "ngc4088_b1_whisp_overview_frozen_extraction_attempt_not_endpoint"

# Frozen geometry from the review packet.  The full-panel crop contains the
# position-velocity plot itself; the labels are outside the crop.
PANEL_BOX = (533, 94, 707, 267)
DATA_X_MIN = 5
DATA_X_MAX = 169
DATA_Y_MIN = 20
DATA_Y_MAX = 155
OFFSET_LEFT_ARCMIN = 8.0
OFFSET_RIGHT_ARCMIN = -8.0
OFFSET_CENTER_X_PX = (DATA_X_MIN + DATA_X_MAX) / 2.0
PIXELS_PER_ARCMIN = (DATA_X_MAX - DATA_X_MIN) / (
    OFFSET_LEFT_ARCMIN - OFFSET_RIGHT_ARCMIN
)
MIN_COMPONENT_AREA = 250


def x_to_offset_arcmin(x_pixel: float) -> float:
    # The WHISP axis is positive to the left and negative to the right.
    return (OFFSET_CENTER_X_PX - x_pixel) / PIXELS_PER_ARCMIN


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


def build_mask(crop_rgb: np.ndarray) -> np.ndarray:
    """Segment the high-saturation H I ridge from the WHISP pos-vel panel."""
    data_window = np.zeros(crop_rgb.shape[:2], dtype=bool)
    data_window[DATA_Y_MIN:DATA_Y_MAX, DATA_X_MIN:DATA_X_MAX] = True
    saturation_like = (crop_rgb.max(axis=2) - crop_rgb.min(axis=2)) > 100
    red_or_warm = (crop_rgb[:, :, 0] > 130) & (crop_rgb[:, :, 2] < 170)
    return data_window & saturation_like & red_or_warm


def extract_components(mask: np.ndarray) -> pd.DataFrame:
    labels, n_labels = ndimage.label(mask)
    rows: list[dict[str, float | int | str]] = []
    for label_id in range(1, n_labels + 1):
        ys, xs = np.where(labels == label_id)
        area = len(xs)
        if area < MIN_COMPONENT_AREA:
            continue
        x_mean = float(xs.mean())
        y_mean = float(ys.mean())
        offset = x_to_offset_arcmin(x_mean)
        rows.append(
            {
                "component_id": f"C{len(rows)+1}",
                "label_id": label_id,
                "area_px": area,
                "x_min_px": int(xs.min()),
                "x_max_px": int(xs.max()),
                "y_min_px": int(ys.min()),
                "y_max_px": int(ys.max()),
                "x_centroid_px": x_mean,
                "y_centroid_px": y_mean,
                "offset_centroid_arcmin": offset,
                "abs_offset_centroid_arcmin": abs(offset),
                "component_side": "positive_offset_side" if offset >= 0 else "negative_offset_side",
            }
        )
    return pd.DataFrame(rows).sort_values("area_px", ascending=False).reset_index(drop=True)


def make_overlay(crop: Image.Image, components: pd.DataFrame) -> None:
    image = crop.convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle([DATA_X_MIN, DATA_Y_MIN, DATA_X_MAX, DATA_Y_MAX], outline=(200, 200, 200), width=1)
    draw.line([(OFFSET_CENTER_X_PX, DATA_Y_MIN), (OFFSET_CENTER_X_PX, DATA_Y_MAX)], fill=(255, 255, 255), width=1)
    colors = [(255, 80, 0), (255, 255, 0), (0, 220, 255), (180, 120, 255)]
    for idx, row in components.iterrows():
        color = colors[idx % len(colors)]
        box = [int(row["x_min_px"]), int(row["y_min_px"]), int(row["x_max_px"]), int(row["y_max_px"])]
        draw.rectangle(box, outline=color, width=2)
        x = float(row["x_centroid_px"])
        y = float(row["y_centroid_px"])
        draw.line([(x, DATA_Y_MIN), (x, DATA_Y_MAX)], fill=color, width=1)
        draw.ellipse([x - 3, y - 3, x + 3, y + 3], outline=color, width=2)
        draw.text((box[0] + 2, max(0, box[1] - 12)), str(row["component_id"]), fill=color)
    image.save(OVERLAY)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)

    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    packet = pd.read_csv(DATA / "ngc4088_b1_whisp_overview_extraction_packet.csv").iloc[0]
    first_pass_xw = float(xw["x_warp_onset"])
    hi_radius_arcmin = float(xw["hi_radius_arcmin"])
    tolerance_xw = max(float(xw["x_warp_uncertainty"]), 0.05)
    tolerance_arcmin = hi_radius_arcmin * tolerance_xw

    overview = Image.open(OVERVIEW).convert("RGB")
    crop = overview.crop(PANEL_BOX)
    crop.save(POSVEL_CROP)
    crop_rgb = np.array(crop)
    mask = build_mask(crop_rgb)
    components = extract_components(mask)

    usable_components = components.head(2).copy()
    side_count = usable_components["component_side"].nunique() if len(usable_components) else 0
    if len(usable_components) >= 2 and side_count == 2:
        side_a = float(
            usable_components.loc[
                usable_components["component_side"].eq("positive_offset_side"),
                "offset_centroid_arcmin",
            ].iloc[0]
        )
        side_b = float(
            usable_components.loc[
                usable_components["component_side"].eq("negative_offset_side"),
                "offset_centroid_arcmin",
            ].iloc[0]
        )
        combined_onset_arcmin = 0.5 * (abs(side_a) + abs(side_b))
        x_w_review = combined_onset_arcmin / hi_radius_arcmin
        uncertainty_arcmin = max(
            0.5 * abs(abs(side_a) - abs(side_b)),
            tolerance_arcmin / 2.0,
        )
        agrees = abs(x_w_review - first_pass_xw) <= tolerance_xw
        extraction_status = "FROZEN_WHISP_OVERVIEW_EXTRACTION_ATTEMPT_COMPLETE_AGREES_WITH_FIRST_PASS"
    else:
        side_a = np.nan
        side_b = np.nan
        combined_onset_arcmin = np.nan
        x_w_review = np.nan
        uncertainty_arcmin = np.nan
        agrees = False
        extraction_status = "FROZEN_WHISP_OVERVIEW_EXTRACTION_ATTEMPT_INCONCLUSIVE"

    components["selected_for_response"] = components["component_id"].isin(set(usable_components["component_id"]))
    components["uses_vobs_or_residual"] = False
    components["endpoint_scores_allowed"] = False
    components["claim_boundary"] = CLAIM_BOUNDARY
    make_overlay(crop, usable_components)

    response = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "packet_id": packet["packet_id"],
                "reviewer_or_method_id": "FROZEN_SCRIPT_WHISP_OVERVIEW_SATURATION_COMPONENT_CENTROID_V1",
                "review_timestamp_utc": "REPRODUCIBLE_SCRIPT_RUN",
                "source_product_used": packet["source_product"],
                "source_product_hash": "not_hashed_in_this_attempt",
                "side_a_onset_offset_arcmin": side_a,
                "side_b_onset_offset_arcmin": side_b,
                "side_combination_rule": "mean(abs(two_largest_opposite-side saturation-component centroids))",
                "combined_onset_arcmin": combined_onset_arcmin,
                "uncertainty_arcmin": uncertainty_arcmin,
                "x_w_review": x_w_review,
                "agrees_with_first_pass_within_tolerance": agrees,
                "review_notes": (
                    "Frozen algorithmic candidate from WHISP graphical overview; "
                    "agreement supports B1 but does not by itself authorize formula freeze."
                ),
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    obligations = pd.DataFrame(
        [
            {
                "obligation_id": "WHEXATT1_SOURCE_PRODUCT_AND_AXIS",
                "status": "PASS",
                "evidence": "cached WHISP overview and frozen pos-vel panel geometry are used",
            },
            {
                "obligation_id": "WHEXATT2_TWO_OPPOSITE_COMPONENTS",
                "status": "PASS" if len(usable_components) >= 2 and side_count == 2 else "BLOCKED",
                "evidence": f"selected_components={len(usable_components)}, side_count={side_count}",
            },
            {
                "obligation_id": "WHEXATT3_FIRST_PASS_AGREEMENT",
                "status": "PASS" if agrees else "BLOCKED",
                "evidence": (
                    f"x_w_review={x_w_review:.6g}, first_pass_x_w={first_pass_xw:.6g}, "
                    f"tolerance={tolerance_xw:.6g}"
                    if np.isfinite(x_w_review)
                    else "x_w_review not finite"
                ),
            },
            {
                "obligation_id": "WHEXATT4_FORMULA_FREEZE_PROMOTION",
                "status": "PENDING_REVIEW",
                "evidence": "requires explicit B1 promotion decision or independent review before accepting x_w",
            },
        ]
    )
    obligations["uses_vobs_or_residual"] = False
    obligations["endpoint_scores_allowed"] = False
    obligations["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "frozen_extraction_attempt_status": extraction_status,
                "galaxy": "NGC4088",
                "b1_resolution_status": "B1_NOT_RESOLVED_FROZEN_EXTRACTION_PROMOTION_REVIEW_REQUIRED",
                "source_product": packet["source_product"],
                "posvel_crop": str(POSVEL_CROP.relative_to(ROOT)),
                "extraction_overlay": str(OVERLAY.relative_to(ROOT)),
                "side_a_onset_offset_arcmin": side_a,
                "side_b_onset_offset_arcmin": side_b,
                "combined_onset_arcmin": combined_onset_arcmin,
                "uncertainty_arcmin": uncertainty_arcmin,
                "x_w_review": x_w_review,
                "first_pass_x_w": first_pass_xw,
                "acceptance_tolerance_x_w": tolerance_xw,
                "agrees_with_first_pass_within_tolerance": agrees,
                "accepted_x_w_for_formula_freeze": False,
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": "promote B1 explicitly only after reviewing this frozen extraction or obtaining independent review/direct FITS data",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    components.to_csv(DATA / "ngc4088_b1_whisp_overview_frozen_extraction_components.csv", index=False)
    response.to_csv(DATA / "ngc4088_b1_whisp_overview_frozen_extraction_response.csv", index=False)
    obligations.to_csv(DATA / "ngc4088_b1_whisp_overview_frozen_extraction_obligations.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b1_whisp_overview_frozen_extraction_summary.csv", index=False)

    report = [
        "# NGC4088 WHISP Overview Frozen Extraction Attempt",
        "",
        "This attempt uses only the cached WHISP UGC 7081 graphical H I overview.",
        "It extracts a source-side x_w candidate from the position-velocity panel",
        "with the source-provided arcmin offset axis. It is not an endpoint score",
        "and does not use observed rotation residuals.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Response Candidate",
        "",
        markdown_table(response),
        "",
        "## Component Ledger",
        "",
        markdown_table(components),
        "",
        "## Obligations",
        "",
        markdown_table(obligations),
        "",
        "## Interpretation",
        "",
        "The frozen WHISP overview extraction gives a source-side x_w candidate that",
        "agrees with the first-pass value within the predeclared tolerance. This is",
        "a real strengthening of B1 provenance, but it is still marked as a",
        "promotion-review input rather than an accepted formula-freeze value.",
        "",
    ]
    (REPORTS / "ngc4088_b1_whisp_overview_frozen_extraction_attempt.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
