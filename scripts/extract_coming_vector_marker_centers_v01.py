#!/usr/bin/env python3
"""Extract green Delta marker centers from checksum-frozen COMING EPS figures."""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "external" / "literature" / "coming_bar_harmonics"
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "coming_vector_marker_centers_v01.md"
GREEN = "rgb(0%, 50.193787%, 0%)"
TARGETS = {
    # y ranges select panels; bottom is the Delta=0 right-axis coordinate.
    "NGC 613": ("PLOTS1.eps", 190.0, 350.0, 13, 338.218750, 471.511719),
    "NGC 4303": ("PLOTS3.eps", 680.0, 792.0, 13, 765.753906, 382.738281),
    "NGC 4579": ("PLOTS4.eps", 0.0, 180.0, 11, 124.300781, 408.726562),
    "NGC 5248": ("PLOTS4.eps", 190.0, 350.0, 9, 338.218750, 388.542969),
    "NGC 7479": ("PLOTS5.eps", 680.0, 792.0, 10, 765.753906, 452.597656),
}
DELTA_AXIS_HEIGHT_PT = 148.855469
RIGHT_PANEL_X_ZERO_PT = 304.589844


def path_center(path: ET.Element) -> tuple[float, float]:
    values = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", path.attrib["d"])]
    xs, ys = values[0::2], values[1::2]
    # pdftocairo preserves the author coordinates with this page transform.
    return sum(xs) / len(xs) * 0.1, 792.0 - sum(ys) / len(ys) * 0.1


def green_vertical_segments(root: ET.Element) -> list[tuple[float, float, float]]:
    segments = []
    pattern = re.compile(r"([ML])\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)")
    for element in root.iter():
        if element.attrib.get("stroke") != GREEN or not element.attrib.get("d"):
            continue
        points = [(cmd, float(x) * 0.1, 792.0 - float(y) * 0.1) for cmd, x, y in pattern.findall(element.attrib["d"])]
        for (cmd0, x0, y0), (cmd1, x1, y1) in zip(points, points[1:]):
            if cmd0 == "M" and cmd1 == "L" and abs(x0 - x1) < 1e-5 and abs(y0 - y1) > 1.0:
                segments.append((x0, min(y0, y1), max(y0, y1)))
    return segments


def extract_svg(eps: Path, svg: Path) -> None:
    pdf = svg.with_suffix(".pdf")
    subprocess.run(["ps2pdf", str(eps), str(pdf)], check=True)
    subprocess.run(["pdftocairo", "-svg", str(pdf), str(svg)], check=True)


def main() -> None:
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        converted: dict[str, Path] = {}
        for galaxy, (filename, y_min, y_max, expected, delta_zero_y, bar_x) in TARGETS.items():
            if filename not in converted:
                svg = tmp_path / filename.replace(".eps", ".svg")
                extract_svg(SOURCE / filename, svg)
                converted[filename] = svg
            root = ET.parse(converted[filename]).getroot()
            verticals = green_vertical_segments(root)
            centers = []
            for element in root.iter():
                if element.attrib.get("fill") == GREEN and element.attrib.get("d"):
                    x, y = path_center(element)
                    if y_min <= y <= y_max and 300.0 <= x <= 512.0:
                        centers.append((x, y))
            centers.sort()
            if len(centers) != expected:
                raise RuntimeError(f"{galaxy}: expected {expected} markers, found {len(centers)}")
            source_points = [(x, y, "vector_marker") for x, y in centers]
            if galaxy == "NGC 4579":
                source_points.insert(0, (319.417969, float("nan"), "source_text_clipped_marker"))
            for index, (x, y, point_origin) in enumerate(source_points, start=1):
                if point_origin == "source_text_clipped_marker":
                    delta = 2.9
                    calibration_status = "source_text_override_clipped_outlier"
                    error_minus = error_plus = None
                    y_top = y_bottom = None
                else:
                    delta = (delta_zero_y - y) / DELTA_AXIS_HEIGHT_PT
                    calibration_status = "vector_linear_axis_0_to_1"
                    matching = [segment for segment in verticals if abs(segment[0] - x) <= 0.02]
                    if len(matching) != 1:
                        raise RuntimeError(f"{galaxy} marker {index}: expected one vertical error bar, found {len(matching)}")
                    _, y_top, y_bottom = matching[0]
                    delta_high = (delta_zero_y - y_top) / DELTA_AXIS_HEIGHT_PT
                    delta_low = (delta_zero_y - y_bottom) / DELTA_AXIS_HEIGHT_PT
                    error_minus = max(0.0, delta - delta_low)
                    error_plus = max(0.0, delta_high - delta)
                r_over_abar = (x - RIGHT_PANEL_X_ZERO_PT) / (bar_x - RIGHT_PANEL_X_ZERO_PT)
                rows.append(
                    {
                        "galaxy": galaxy,
                        "source_figure": filename,
                        "marker_index_radial_order": index,
                        "vector_x_pt": round(x, 6),
                        "vector_y_pt": None if point_origin == "source_text_clipped_marker" else round(y, 6),
                        "delta_axis_calibrated": True,
                        "physical_delta": round(delta, 6),
                        "physical_delta_error_minus": None if error_minus is None else round(error_minus, 6),
                        "physical_delta_error_plus": None if error_plus is None else round(error_plus, 6),
                        "vector_error_y_top_pt": None if y_top is None else round(y_top, 6),
                        "vector_error_y_bottom_pt": None if y_bottom is None else round(y_bottom, 6),
                        "physical_r_over_abar": round(r_over_abar, 6),
                        "delta_calibration_status": calibration_status,
                        "point_origin": point_origin,
                        "uses_dark_discrepancy_endpoint": False,
                    }
                )
    frame = pd.DataFrame(rows)
    frame.to_csv(DATA / "coming_vector_marker_centers_v01.csv", index=False)
    counts = frame.groupby("galaxy").size().to_dict()
    payload = {
        "schema": "tau_core_coming_vector_marker_centers_v01",
        "status": "DELTA_RADIAL_PROFILES_AND_VISIBLE_ERRORS_EXTRACTED_OUTLIER_ERROR_OPEN",
        "n_galaxies": len(counts),
        "n_markers": len(frame),
        "marker_counts": counts,
        "marker_count_gate_pass": counts == {
            g: spec[3] + (1 if g == "NGC 4579" else 0) for g, spec in TARGETS.items()
        },
        "delta_axis_calibrated": True,
        "ngc4579_clipped_outlier_restored_as_separate_point": True,
        "physical_delta_amplitudes_frozen": True,
        "radial_r_over_abar_calibrated": True,
        "central_value_profiles_frozen": True,
        "n_points_with_vector_errors": int(frame.physical_delta_error_minus.notna().sum()),
        "physical_profiles_frozen": False,
        "uses_dark_discrepancy_endpoint": False,
        "endpoint_scoring_allowed": False,
        "next_gate": "complete reverse-render residual validation and decide the clipped outlier uncertainty policy",
        "claim_boundary": "source Delta(R/a_bar) profiles with vector errors except the clipped NGC4579 outlier; endpoint remains closed",
    }
    (DATA / "coming_vector_marker_centers_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = [
        "# COMING vector marker centers v01",
        "",
        f"Status: `{payload['status']}`",
        "",
        f"Extracted `{len(frame)}` green `Delta` marker centers from five source panels. Marker-count gates pass for every galaxy: `{counts}`.",
        "",
        "The common linear `Delta=0..1` transform, source-marked `a_bar` lines, and vector error bars are applied. NGC4579's fully clipped innermost point is restored as a separate `Delta=2.9` row at the radial coordinate retained by its clipped error-bar segment; its uncertainty remains unavailable. Full-page rendering also corrected the initial NGC613 row assignment. Endpoint scoring is prohibited.",
        "",
    ]
    REPORT.write_text("\n".join(lines))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
