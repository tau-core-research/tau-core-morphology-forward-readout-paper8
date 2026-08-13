#!/usr/bin/env python3
"""Digitize the prefrozen NGC4579 Halpha PV model line with reverse-render QA."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
IMAGE = DATA / "ngc4579_halpha_pv_render" / "page43_300dpi.png"
REPORT = ROOT / "reports" / "ngc4579_halpha_pv_endpoint_v01.md"
FREEZE = DATA / "ngc4579_halpha_pv_extraction_freeze_v01.json"
X_LEFT, X_RIGHT = 519, 2080
Y_TOP, Y_BOTTOM = 2650, 2851
OFFSET_MIN, OFFSET_MAX = -100.0, 100.0
VELOCITY_TOP, VELOCITY_BOTTOM = 1750.0, 1250.0
VSYS = 1507.6
INCLINATION_DEG = 38.7
DISTANCE_MPC = 16.5
BAR_RADIUS_KPC = 3.62
CURVE_CLIPPED_AFTER_OFFSET_ARCSEC = 20.0


def trace_curve(rgb: np.ndarray) -> np.ndarray:
    strip = rgb[Y_TOP + 4:Y_BOTTOM - 4, X_LEFT + 4:X_RIGHT - 4].astype(float)
    maximum = strip.max(axis=2)
    chroma = strip.max(axis=2) - strip.min(axis=2)
    cost = 5.0 * maximum / 255.0 + 8.0 * chroma / 255.0
    height, width = cost.shape
    # The source curve enters near 1325 km/s at the left edge.
    start = int(round((VELOCITY_TOP - 1325.0) / (VELOCITY_TOP - VELOCITY_BOTTOM) * (Y_BOTTOM - Y_TOP))) - 4
    dp = np.full((height, width), np.inf)
    back = np.zeros((height, width), dtype=np.int16)
    dp[:, 0] = cost[:, 0] + 0.08 * (np.arange(height) - start) ** 2
    for x in range(1, width):
        for y in range(height):
            lo, hi = max(0, y - 4), min(height, y + 5)
            candidates = dp[lo:hi, x - 1] + 0.18 * np.abs(np.arange(lo, hi) - y)
            j = int(np.argmin(candidates))
            dp[y, x] = cost[y, x] + candidates[j]
            back[y, x] = lo + j
    end_expected = int(round((VELOCITY_TOP - 1710.0) / (VELOCITY_TOP - VELOCITY_BOTTOM) * (Y_BOTTOM - Y_TOP))) - 4
    endpoint_cost = dp[:, -1] + 0.08 * (np.arange(height) - end_expected) ** 2
    trace = np.zeros(width, dtype=int)
    trace[-1] = int(np.argmin(endpoint_cost))
    for x in range(width - 1, 0, -1):
        trace[x - 1] = back[trace[x], x]
    return trace + Y_TOP + 4


def main() -> None:
    freeze = json.loads(FREEZE.read_text())
    image = Image.open(IMAGE).convert("RGB")
    rgb = np.asarray(image)
    trace = trace_curve(rgb)
    x_trace = np.arange(X_LEFT + 4, X_RIGHT - 4)
    offsets = np.arange(-95.0, 95.0001, 5.0)
    x_sample = X_LEFT + (offsets - OFFSET_MIN) / (OFFSET_MAX - OFFSET_MIN) * (X_RIGHT - X_LEFT)
    y_sample = np.interp(x_sample, x_trace, trace)
    vlos = VELOCITY_TOP + (y_sample - Y_TOP) / (Y_BOTTOM - Y_TOP) * (VELOCITY_BOTTOM - VELOCITY_TOP)
    radius_kpc = np.abs(offsets) * DISTANCE_MPC * 1e3 / 206265.0
    vrot = np.abs(vlos - VSYS) / np.sin(np.deg2rad(INCLINATION_DEG))
    published_curve_visible = offsets <= CURVE_CLIPPED_AFTER_OFFSET_ARCSEC
    vlos = np.where(published_curve_visible, vlos, np.nan)
    vrot = np.where(published_curve_visible, vrot, np.nan)
    side = np.where(offsets < 0.0, "approaching", "receding")
    out = pd.DataFrame({
        "offset_arcsec": offsets, "side": side, "radius_kpc": radius_kpc,
        "vlos_model_km_s": vlos, "vrot_deprojected_km_s": vrot,
        "published_model_curve_visible": published_curve_visible,
        "post_bar_primary": radius_kpc >= BAR_RADIUS_KPC,
        "source_pixel_x": x_sample, "source_pixel_y": y_sample,
    })
    out.to_csv(DATA / "ngc4579_halpha_pv_endpoint_v01.csv", index=False)

    overlay = image.copy()
    draw = ImageDraw.Draw(overlay)
    for x, y in zip(x_trace[::3], trace[::3]):
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(255, 0, 255))
    for x, y in zip(x_sample, y_sample):
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), outline=(255, 255, 0), width=2)
    overlay.save(DATA / "ngc4579_halpha_pv_reverse_render_v01.png")

    primary = out[out.post_bar_primary & out.published_model_curve_visible]
    side_counts = primary.side.value_counts().to_dict()
    both_sides_pass = all(side_counts.get(side, 0) >= 3 for side in ("approaching", "receding"))
    result = {
        "schema": "tau_core_ngc4579_halpha_pv_endpoint_v01",
        "status": "GRAPHICAL_HALPHA_PV_ENDPOINT_INELIGIBLE_SOURCE_CURVE_CLIPPED",
        "freeze_status": freeze["status"], "n_all_samples": len(out),
        "n_post_bar_samples": len(primary),
        "post_bar_side_counts": side_counts,
        "post_bar_radius_range_kpc": [float(primary.radius_kpc.min()), float(primary.radius_kpc.max())],
        "post_bar_vrot_range_km_s": [float(primary.vrot_deprojected_km_s.min()), float(primary.vrot_deprojected_km_s.max())],
        "endpoint_values_opened": True,
        "reverse_render_visual_acceptance": False,
        "source_curve_clipped_after_offset_arcsec": CURVE_CLIPPED_AFTER_OFFSET_ARCSEC,
        "both_sides_quality_gate_pass": both_sides_pass,
        "combined_baryonic_field_ready": True,
        "scoring_allowed": False,
        "claim_boundary": "ineligible graphical endpoint: the published model curve exits the panel before the receding post-bar domain; no score is permitted"
    }
    (DATA / "ngc4579_halpha_pv_endpoint_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC4579 Halpha PV endpoint v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The source model curve exits through the upper panel boundary near `+{CURVE_CLIPPED_AFTER_OFFSET_ARCSEC:.0f}` arcsec. "
        f"Only `{side_counts.get('approaching', 0)}` approaching and `{side_counts.get('receding', 0)}` receding visible post-bar samples remain. "
        "The prefrozen both-sides quality gate therefore fails and scoring is forbidden. The apparent lower-right trace is colored PV emission, not the black source-model curve.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
