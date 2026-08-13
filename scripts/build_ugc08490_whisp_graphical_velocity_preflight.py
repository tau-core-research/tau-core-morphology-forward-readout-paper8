#!/usr/bin/env python3
"""Digitize the frozen UGC08490 WHISP 60-arcsec velocity panel."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
SOURCE = ROOT / "data/external/literature/ugc08490_whisp_hi_route/whisp_ugc08490_overview.gif"
PANEL_BOX = (537, 542, 701, 694)
SYSTEMIC = 204.0
# Exact legend-color row centers; three printed labels freeze the linear scale.
LEGEND_ANCHORS = [(782.4603174603, 250.0), (821.4925373134, 200.0), (860.5, 150.0)]
PALETTE = [
    ("red", (252, 2, 4), 766.5), ("orange", (252, 190, 4), 782.4603174603),
    ("yellow", (252, 253, 4), 795.2253521127), ("bright_green", (4, 242, 4), 808.3455497382),
    ("dark_green", (6, 163, 9), 821.4925373134), ("light_blue", (116, 182, 244), 834.5024630542),
    ("blue", (4, 2, 212), 847.5), ("purple", (140, 2, 172), 860.5),
]


def main() -> None:
    source = json.loads((DATA / "ugc08490_whisp_hi_source_v01.json").read_text())
    if not source["graphical_velocity_field_acquired"]:
        raise RuntimeError("UGC08490 graphical source unavailable")
    slope, intercept = np.polyfit(
        [item[0] for item in LEGEND_ANCHORS], [item[1] for item in LEGEND_ANCHORS], 1
    )
    velocities = {rgb: (name, float(slope * row + intercept)) for name, rgb, row in PALETTE}
    centers = sorted(value for _, value in velocities.values())
    quantization = max(np.diff(centers)) / 2
    panel = Image.open(SOURCE).convert("RGB").crop(PANEL_BOX)
    panel.save(DATA / "ugc08490_whisp_60arcsec_velocity_panel_v01.png")
    pixels = {}
    for y in range(panel.height):
        for x in range(panel.width):
            rgb = panel.getpixel((x, y))
            if rgb in velocities:
                pixels[(x, y)] = velocities[rgb]
    unseen = set(pixels); components = []
    while unseen:
        start = unseen.pop(); component = {start}; frontier = [start]
        while frontier:
            x, y = frontier.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    neighbor = (x + dx, y + dy)
                    if neighbor in unseen:
                        unseen.remove(neighbor); component.add(neighbor); frontier.append(neighbor)
        components.append(component)
    components.sort(key=len, reverse=True)
    rows = []
    for x, y in sorted(components[0], key=lambda point: (point[1], point[0])):
        name, velocity = pixels[(x, y)]
        relation = "systemic_ambiguous" if abs(velocity - SYSTEMIC) <= quantization else (
            "receding" if velocity > SYSTEMIC else "approaching"
        )
        rows.append({
            "panel_x": x, "panel_y": y, "source_x": x + PANEL_BOX[0],
            "source_y": y + PANEL_BOX[1], "palette_class": name,
            "velocity_bin_center_km_s": velocity,
            "velocity_quantization_half_width_km_s": quantization,
            "systemic_relation": relation, "endpoint_access": False,
        })
    frame = pd.DataFrame(rows)
    frame.to_csv(DATA / "ugc08490_whisp_60arcsec_velocity_pixels_v01.csv", index=False)
    counts = Counter(frame.systemic_relation)
    result = {
        "schema": "ugc08490_whisp_graphical_velocity_preflight_v01",
        "status": "WHISP_UGC08490_60ARCSEC_VELOCITY_DIGITIZED_AXIS_TRANSPORT_OPEN",
        "panel_box_source_pixels": list(PANEL_BOX), "panel_size_pixels": list(panel.size),
        "systemic_velocity_km_s": SYSTEMIC, "legend_anchors": LEGEND_ANCHORS,
        "legend_velocity_per_source_y_pixel": float(slope),
        "palette_bin_centers_km_s": {name: velocity for _, (name, velocity) in velocities.items()},
        "quantization_half_width_km_s": float(quantization),
        "largest_component_pixels": len(frame),
        "connected_component_sizes": [len(component) for component in components[:10]],
        "side_counts": dict(counts),
        "both_hi_velocity_sides_present": counts["approaching"] > 0 and counts["receding"] > 0,
        "printed_axis_transport_ready": False, "common_hi_halpha_radii_ready": False,
        "kernel_measurement_allowed": False, "endpoint_access": False,
        "claim_boundary": (
            "exact-palette graphical preflight with printed-legend calibration; formal WCS, "
            "center, beam covariance and common tracer radii remain open"
        ),
    }
    (DATA / "ugc08490_whisp_graphical_velocity_preflight_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
