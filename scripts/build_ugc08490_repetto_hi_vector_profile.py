#!/usr/bin/env python3
"""Extract UGC08490 observed H I rotation points from Repetto et al. figure 4."""

from __future__ import annotations

import json
from pathlib import Path

import fitz
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
FIGURE = ROOT / "data/external/literature/ugc08490_repetto2018_route/f4.pdf"
X_ZERO = 89.17333221435547
X_PER_2_KPC = 85.33333587646484
Y_ZERO = 490.04534912109375
Y_PER_20_KM_S = 82.2158203125
ARCSEC_PER_KPC = 43.9


def main() -> None:
    page = fitz.open(FIGURE)[0]
    drawings = page.get_drawings()
    points = []
    for drawing in drawings:
        rect = drawing["rect"]
        items = drawing["items"]
        if not (
            abs(rect.width - 7.0) < 0.01 and abs(rect.height - 7.0) < 0.01
            and items and items[0][0] == "c" and len(items) == 8
        ):
            continue
        x = (rect.x0 + rect.x1) / 2
        y = (rect.y0 + rect.y1) / 2
        if not (80 < x < 542 and y < 450):
            continue
        error_segments = []
        for candidate in drawings:
            line = candidate["rect"]
            if (
                line.width == 0 and abs(line.x0 - x) < 0.02
                and line.y0 <= y <= line.y1 and line.height > 3.5
            ):
                error_segments.append(line)
        error = None
        if error_segments:
            line = min(error_segments, key=lambda item: abs((item.y0 + item.y1) / 2 - y))
            error = line.height / 2 / (Y_PER_20_KM_S / 20)
        radius_kpc = (x - X_ZERO) / (X_PER_2_KPC / 2)
        points.append({
            "radius_kpc": radius_kpc, "radius_arcsec": radius_kpc * ARCSEC_PER_KPC,
            "hi_rotation_km_s": (Y_ZERO - y) / (Y_PER_20_KM_S / 20),
            "hi_error_km_s": error, "extraction": "vector_marker_and_errorbar_path",
            "endpoint_access": False,
        })
    frame = pd.DataFrame(points).sort_values("radius_kpc")
    frame.to_csv(DATA / "ugc08490_repetto_hi_vector_profile_v01.csv", index=False)
    result = {
        "schema": "ugc08490_repetto_hi_vector_profile_v01",
        "status": "UGC08490_PUBLISHED_VECTOR_HI_PROFILE_EXTRACTED",
        "n_points": len(frame), "radius_kpc_range": [float(frame.radius_kpc.min()), float(frame.radius_kpc.max())],
        "radius_arcsec_range": [float(frame.radius_arcsec.min()), float(frame.radius_arcsec.max())],
        "axis_calibration": {
            "x_zero_pdf": X_ZERO, "x_pdf_per_2_kpc": X_PER_2_KPC,
            "y_zero_pdf": Y_ZERO, "y_pdf_per_20_km_s": Y_PER_20_KM_S,
            "arcsec_per_kpc_from_printed_top_axis": ARCSEC_PER_KPC,
        },
        "source_native_numeric_table": False, "figure_derived_numeric_profile": True,
        "endpoint_access": False,
        "claim_boundary": "vector-figure extraction; values remain secondary to an author-supplied table",
    }
    (DATA / "ugc08490_repetto_hi_vector_profile_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"], len(frame))


if __name__ == "__main__":
    main()
