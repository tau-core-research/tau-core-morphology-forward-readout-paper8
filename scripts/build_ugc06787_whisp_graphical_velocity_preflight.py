#!/usr/bin/env python3
"""Digitize the frozen WHISP UGC06787 60-arcsec velocity panel coarsely."""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
SOURCE = ROOT / "data" / "external" / "literature" / "ugc06787_whisp_hi_route" / "whisp_ugc06787_overview.gif"

# Frozen from the source overview before any endpoint access.
PANEL_BOX = (537, 542, 701, 694)
SYSTEMIC_VELOCITY_KM_S = 1176.0
PALETTE = [
    ("red", (252, 2, 4), 1425.0),
    ("orange", (252, 178, 4), 1375.0),
    ("yellow", (252, 252, 4), 1325.0),
    ("bright_green", (5, 245, 5), 1275.0),
    ("dark_green", (4, 146, 4), 1225.0),
    ("light_blue", (92, 166, 236), 1175.0),
    ("blue", (4, 2, 205), 1125.0),
    ("purple", (124, 2, 156), 1075.0),
]
QUANTIZATION_HALF_WIDTH_KM_S = 25.0


def velocity_side(value: float) -> str:
    if abs(value - SYSTEMIC_VELOCITY_KM_S) <= QUANTIZATION_HALF_WIDTH_KM_S:
        return "systemic_ambiguous"
    return "receding" if value > SYSTEMIC_VELOCITY_KM_S else "approaching"


def main() -> None:
    source = json.loads((DATA / "ugc06787_whisp_hi_source_v01.json").read_text())
    if not source["graphical_velocity_field_acquired"]:
        raise RuntimeError("frozen WHISP graphical source is unavailable")

    image = Image.open(SOURCE).convert("RGB")
    panel = image.crop(PANEL_BOX)
    panel_path = DATA / "ugc06787_whisp_60arcsec_velocity_panel_v01.png"
    panel.save(panel_path)

    palette_by_rgb = {rgb: (name, velocity) for name, rgb, velocity in PALETTE}
    raw_pixels: dict[tuple[int, int], tuple[str, float, tuple[int, int, int]]] = {}
    for y in range(panel.height):
        for x in range(panel.width):
            rgb = panel.getpixel((x, y))
            if rgb not in palette_by_rgb:
                continue
            name, velocity = palette_by_rgb[rgb]
            raw_pixels[(x, y)] = (name, velocity, rgb)

    unseen = set(raw_pixels)
    components: list[set[tuple[int, int]]] = []
    while unseen:
        start = unseen.pop()
        component = {start}
        frontier = [start]
        while frontier:
            x, y = frontier.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    neighbor = (x + dx, y + dy)
                    if neighbor in unseen:
                        unseen.remove(neighbor)
                        component.add(neighbor)
                        frontier.append(neighbor)
        components.append(component)
    components.sort(key=len, reverse=True)
    galaxy_component = components[0]

    rows = []
    for x, y in sorted(galaxy_component, key=lambda item: (item[1], item[0])):
        name, velocity, _ = raw_pixels[(x, y)]
        rows.append(
                {
                    "panel_x": x,
                    "panel_y": y,
                    "source_x": x + PANEL_BOX[0],
                    "source_y": y + PANEL_BOX[1],
                    "palette_class": name,
                    "velocity_bin_center_km_s": velocity,
                    "velocity_quantization_half_width_km_s": QUANTIZATION_HALF_WIDTH_KM_S,
                    "systemic_relation": velocity_side(velocity),
                    "endpoint_access": False,
                }
            )

    if not rows:
        raise RuntimeError("no exact WHISP palette pixels found")
    pixel_path = DATA / "ugc06787_whisp_60arcsec_velocity_pixels_v01.csv"
    with pixel_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(row["systemic_relation"] for row in rows)
    class_counts = Counter(row["palette_class"] for row in rows)
    centroids = {}
    for side in ("approaching", "receding", "systemic_ambiguous"):
        side_rows = [row for row in rows if row["systemic_relation"] == side]
        centroids[side] = {
            "n_pixels": len(side_rows),
            "panel_x_mean": sum(int(row["panel_x"]) for row in side_rows) / len(side_rows),
            "panel_y_mean": sum(int(row["panel_y"]) for row in side_rows) / len(side_rows),
        }
    separation = math.dist(
        (centroids["approaching"]["panel_x_mean"], centroids["approaching"]["panel_y_mean"]),
        (centroids["receding"]["panel_x_mean"], centroids["receding"]["panel_y_mean"]),
    )
    result = {
        "schema": "ugc06787_whisp_graphical_velocity_preflight_v01",
        "status": "WHISP_UGC06787_60ARCSEC_GRAPHICAL_VELOCITY_DIGITIZED_WORLD_TRANSPORT_OPEN",
        "panel_box_source_pixels": list(PANEL_BOX),
        "panel_size_pixels": [panel.width, panel.height],
        "systemic_velocity_km_s": SYSTEMIC_VELOCITY_KM_S,
        "palette_bin_centers_km_s": {name: velocity for name, _, velocity in PALETTE},
        "quantization_half_width_km_s": QUANTIZATION_HALF_WIDTH_KM_S,
        "exact_palette_pixels": len(rows),
        "raw_exact_palette_pixels": len(raw_pixels),
        "connected_component_sizes": [len(component) for component in components[:10]],
        "largest_component_policy": "retain only the largest 8-connected exact-palette component to remove the plotted beam marker and isolated graphical pixels",
        "side_counts": dict(counts),
        "palette_counts": dict(class_counts),
        "side_centroids": centroids,
        "approaching_receding_centroid_separation_pixels": separation,
        "both_hi_velocity_sides_present": counts["approaching"] > 0 and counts["receding"] > 0,
        "world_coordinate_transport_ready": False,
        "halpha_common_radial_transport_ready": False,
        "physical_a_row_constructed": False,
        "endpoint_access": False,
        "claim_boundary": "coarse exact-palette graphical digitization only; bin centers inferred from the printed legend with +/-25 km/s quantization; no WCS/FITS, beam covariance, H I-Halpha radial map, or physical channel test",
    }
    (DATA / "ugc06787_whisp_graphical_velocity_preflight_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    (REPORTS / "ugc06787_whisp_graphical_velocity_preflight_v01.md").write_text(
        f"""# UGC06787 WHISP Graphical Velocity Preflight v0.1

**Status:** `{result['status']}`

The frozen 60 arcsec intensity-weighted velocity panel was cropped at source
pixel box `{PANEL_BOX}`. Only exact printed palette colors in the largest
8-connected component were retained; this removes the separate plotted beam
marker and isolated graphical pixels. The
legend is represented by 50 km/s bins with `+/-25 km/s` graphical
quantization; anti-aliased pixels and black background are excluded.

| quantity | value |
| --- | ---: |
| exact palette pixels | {len(rows)} |
| approaching pixels | {counts['approaching']} |
| receding pixels | {counts['receding']} |
| systemic-ambiguous pixels | {counts['systemic_ambiguous']} |
| approaching/receding centroid separation | {separation:.3f} pixels |

Both H I velocity sides are present in the graphical product. The GHASP-SPARC
packet currently contains only approaching-side Halpha rows, so a symmetric
H I-Halpha parity comparison remains blocked.

This preflight does not supply WCS, a calibrated FITS velocity field, beam
covariance, or common H I-Halpha radial coordinates. It cannot be promoted to
a physical `A_p` row. The next admissible step is source-side world-coordinate
calibration of the panel axes or direct cube/FITS acquisition.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
