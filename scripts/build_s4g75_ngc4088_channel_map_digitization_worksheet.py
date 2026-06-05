#!/usr/bin/env python3
"""Build a frozen NGC4088 channel-map digitization worksheet.

The worksheet turns the rendered N4088 channel-map panel into panel-level
measurement targets.  It does not infer the warp onset and does not use
rotation residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
LITERATURE = ROOT / "data" / "external" / "literature"
PAGE_DIR = LITERATURE / "2001_verheijen_sancisi_pages"
ROI = PAGE_DIR / "ngc4088_page_76_channel_maps_roi.png"
OVERLAY = PAGE_DIR / "ngc4088_page_76_channel_maps_roi_worksheet_overlay.png"
CLAIM_BOUNDARY = "s4g75_ngc4088_channel_map_digitization_worksheet_not_endpoint"


VELOCITIES = [
    [568, 585, 601, 618],
    [634, 651, 667, 684],
    [701, 717, 734, 750],
    [767, 783, 800, 817],
    [833, 850, 866, 883],
    [899, 916, 933, None],
]

# Pixel coordinates in the ROI crop.  These are frozen worksheet coordinates,
# not measured physical quantities.
GRID_LEFT = 0
GRID_TOP = 22
CELL_WIDTH = 171
CELL_HEIGHT = 157


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


def panel_rows() -> pd.DataFrame:
    rows = []
    for r, velocities in enumerate(VELOCITIES, start=1):
        for c, velocity in enumerate(velocities, start=1):
            x0 = GRID_LEFT + (c - 1) * CELL_WIDTH
            y0 = GRID_TOP + (r - 1) * CELL_HEIGHT
            x1 = x0 + CELL_WIDTH
            y1 = y0 + CELL_HEIGHT
            valid = velocity is not None
            rows.append(
                {
                    "galaxy": "NGC4088",
                    "panel_id": f"r{r}c{c}",
                    "row": r,
                    "col": c,
                    "channel_velocity_kms": velocity if valid else "",
                    "roi_x0_px": x0,
                    "roi_y0_px": y0,
                    "roi_x1_px": x1,
                    "roi_y1_px": y1,
                    "panel_status": "MEASUREMENT_TARGET" if valid else "NON_TARGET_EDGE_PANEL",
                    "measurement_inner_axis_px": "",
                    "measurement_outer_ridge_axis_px": "",
                    "measurement_onset_radius_arcmin": "",
                    "measurement_uncertainty_arcmin": "",
                    "side_label": "",
                    "uses_vobs_or_residual": False,
                    "x_warp_onset_available": False,
                    "endpoint_scores_allowed": False,
                    "endpoint_scores_computed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def build_overlay(panels: pd.DataFrame) -> None:
    im = Image.open(ROI).convert("RGB")
    draw = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("Arial.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    for _, row in panels.iterrows():
        color = (220, 40, 40) if row["panel_status"] == "MEASUREMENT_TARGET" else (140, 140, 140)
        box = (row["roi_x0_px"], row["roi_y0_px"], row["roi_x1_px"], row["roi_y1_px"])
        draw.rectangle(box, outline=color, width=2)
        label = f"{row['panel_id']} {row['channel_velocity_kms']}"
        draw.text((row["roi_x0_px"] + 5, row["roi_y0_px"] + 5), label, fill=color, font=font)
    im.save(OVERLAY)


def build_outputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    panels = panel_rows()
    build_overlay(panels)
    measurement_targets = panels.loc[panels["panel_status"] == "MEASUREMENT_TARGET"]
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "roi_png": str(ROI.relative_to(ROOT)),
                "overlay_png": str(OVERLAY.relative_to(ROOT)),
                "n_panel_rows": len(panels),
                "n_measurement_targets": len(measurement_targets),
                "n_empty_measurement_fields": int(
                    measurement_targets[
                        [
                            "measurement_inner_axis_px",
                            "measurement_outer_ridge_axis_px",
                            "measurement_onset_radius_arcmin",
                            "measurement_uncertainty_arcmin",
                        ]
                    ]
                    .eq("")
                    .sum()
                    .sum()
                ),
                "worksheet_status": "PANEL_WORKSHEET_READY_MEASUREMENTS_EMPTY",
                "x_warp_onset_available": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return panels, summary


def write_report(panels: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Channel-Map Digitization Worksheet",
        "",
        "This worksheet freezes panel coordinates for the N4088 channel-map "
        "digitization target. It does not measure the warp onset.",
        "",
        "## Verdict",
        "",
        "The channel-map ROI has been split into panel-level measurement targets. "
        "All measurement fields remain empty; `x_w` is still unavailable.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Panel Targets",
        "",
        markdown_table(
            panels[
                [
                    "panel_id",
                    "channel_velocity_kms",
                    "roi_x0_px",
                    "roi_y0_px",
                    "roi_x1_px",
                    "roi_y1_px",
                    "panel_status",
                    "x_warp_onset_available",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "Panel boxes are digitization scaffolding, not source measurements. A "
        "human or frozen image-analysis protocol must fill the measurement fields "
        "before any `x_w` candidate can be computed.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_channel_map_digitization_worksheet.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    panels, summary = build_outputs()
    panels.to_csv(DATA / "s4g75_ngc4088_channel_map_digitization_worksheet.csv", index=False)
    summary.to_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_worksheet_summary.csv",
        index=False,
    )
    write_report(panels, summary)
    print(f"wrote {DATA / 's4g75_ngc4088_channel_map_digitization_worksheet.csv'}")
    print(f"wrote {DATA / 's4g75_ngc4088_channel_map_digitization_worksheet_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc4088_channel_map_digitization_worksheet.md'}")
    print(f"wrote {OVERLAY}")


if __name__ == "__main__":
    main()
