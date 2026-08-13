#!/usr/bin/env python3
"""Test robust two-side H I support in the frozen NGC3726 WHISP overview."""

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
SOURCE = (
    ROOT
    / "data"
    / "external"
    / "literature"
    / "ngc3726_whisp_hi_route"
    / "whisp_ngc3726_overview.gif"
)

# Frozen from the source layout before any endpoint access.
PANEL_BOX = (537, 542, 701, 694)
PALETTE = {
    (252, 2, 4): ("red", "robust_receding"),
    (252, 190, 4): ("orange", "robust_receding"),
    (252, 252, 4): ("yellow", "robust_receding"),
    (5, 240, 6): ("bright_green", "systemic_ambiguous"),
    (4, 162, 5): ("dark_green", "systemic_ambiguous"),
    (116, 182, 243): ("light_blue", "robust_approaching"),
    (4, 2, 212): ("blue", "robust_approaching"),
    (140, 2, 172): ("purple", "robust_approaching"),
}


def main() -> None:
    source = json.loads((DATA / "ngc3726_whisp_hi_source_v01.json").read_text())
    if not source["graphical_velocity_field_acquired"]:
        raise RuntimeError("Frozen NGC3726 WHISP graphical source is unavailable")

    panel = Image.open(SOURCE).convert("RGB").crop(PANEL_BOX)
    panel_path = DATA / "ngc3726_whisp_60arcsec_velocity_panel_v01.png"
    panel.save(panel_path)
    raw = {
        (x, y): PALETTE[panel.getpixel((x, y))]
        for y in range(panel.height)
        for x in range(panel.width)
        if panel.getpixel((x, y)) in PALETTE
    }
    unseen = set(raw)
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
    galaxy = components[0]

    rows = []
    for x, y in sorted(galaxy, key=lambda item: (item[1], item[0])):
        palette_class, side_class = raw[(x, y)]
        rows.append(
            {
                "panel_x": x,
                "panel_y": y,
                "source_x": x + PANEL_BOX[0],
                "source_y": y + PANEL_BOX[1],
                "palette_class": palette_class,
                "robust_side_class": side_class,
                "endpoint_access": False,
            }
        )
    counts = Counter(row["robust_side_class"] for row in rows)
    centroids = {}
    for side in ("robust_approaching", "robust_receding"):
        selected = [row for row in rows if row["robust_side_class"] == side]
        centroids[side] = {
            "n_pixels": len(selected),
            "panel_x_mean": sum(int(row["panel_x"]) for row in selected) / len(selected),
            "panel_y_mean": sum(int(row["panel_y"]) for row in selected) / len(selected),
        }
    separation = math.dist(
        (centroids["robust_approaching"]["panel_x_mean"], centroids["robust_approaching"]["panel_y_mean"]),
        (centroids["robust_receding"]["panel_x_mean"], centroids["robust_receding"]["panel_y_mean"]),
    )
    with (DATA / "ngc3726_whisp_60arcsec_velocity_pixels_v01.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    candidate = next(
        row
        for row in csv.DictReader(
            (DATA / "ghasp_sparc_source_only_candidate_federation_v01.csv").open(
                newline="", encoding="utf-8"
            )
        )
        if row["galaxy"] == "NGC3726"
    )
    result = {
        "schema": "ngc3726_whisp_graphical_side_preflight_v01",
        "status": "NGC3726_HI_HALPHA_TWO_SIDE_SOURCE_SUPPORT_CONFIRMED_COMMON_TRANSPORT_OPEN",
        "panel_box_source_pixels": list(PANEL_BOX),
        "panel_size_pixels": [panel.width, panel.height],
        "raw_exact_palette_pixels": len(raw),
        "exact_palette_pixels_largest_component": len(rows),
        "connected_component_sizes": [len(component) for component in components[:10]],
        "side_counts": dict(counts),
        "side_centroids": centroids,
        "approaching_receding_centroid_separation_pixels": separation,
        "both_hi_velocity_sides_present": counts["robust_approaching"] > 0 and counts["robust_receding"] > 0,
        "halpha_approaching_points": int(candidate["n_approaching"]),
        "halpha_receding_points": int(candidate["n_receding"]),
        "both_halpha_sides_present": candidate["both_halpha_sides"] == "True",
        "selection_uses_vobs_or_residual": False,
        "world_coordinate_transport_ready": False,
        "beam_matched_hi_halpha_ready": False,
        "physical_a_row_constructed": False,
        "endpoint_access": False,
        "claim_boundary": "graphical robust-side support only; central green colors left ambiguous; no velocity calibration, WCS/FITS, common radial map, beam covariance, channel statistic, or endpoint result",
    }
    (DATA / "ngc3726_whisp_graphical_side_preflight_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    (REPORTS / "ngc3726_whisp_graphical_side_preflight_v01.md").write_text(
        f"""# NGC3726 WHISP Graphical Side Preflight v0.1

**Status:** `{result['status']}`

The frozen 60-arcsec WHISP intensity-weighted velocity panel was cropped at
source pixel box `{PANEL_BOX}`. Exact palette pixels in the largest
8-connected component were retained. Red/orange/yellow and
light-blue/blue/purple provide robust opposite-side classes; both green
classes are deliberately left systemic-ambiguous.

| source support | approaching | receding | ambiguous |
| --- | ---: | ---: | ---: |
| WHISP graphical pixels | {counts['robust_approaching']} | {counts['robust_receding']} | {counts['systemic_ambiguous']} |
| GHASP Halpha points | {candidate['n_approaching']} | {candidate['n_receding']} | n/a |

Both tracers therefore have two-side source support. This removes the
UGC06787 single-Halpha-side blocker, but it does not yet compare the tracers:
the graphical H I panel lacks formal WCS/FITS transport, beam matching, and
uncertainty covariance. No physical `A_p` row or endpoint result is created.
""",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
