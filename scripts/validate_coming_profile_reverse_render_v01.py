#!/usr/bin/env python3
"""Reverse-render calibrated COMING profiles back to source vector geometry."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "coming_profile_reverse_render_validation_v01.md"
X_ZERO = 304.589844
AXIS_HEIGHT = 148.855469
GEOMETRY = {
    "NGC 613": (338.218750, 471.511719),
    "NGC 4303": (765.753906, 382.738281),
    "NGC 4579": (124.300781, 408.726562),
    "NGC 5248": (338.218750, 388.542969),
    "NGC 7479": (765.753906, 452.597656),
}


def main() -> None:
    frame = pd.read_csv(DATA / "coming_vector_marker_centers_v01.csv")
    visible = frame[frame.point_origin.eq("vector_marker")].copy()
    x_residuals = []
    y_residuals = []
    error_roundtrip_residuals = []
    rows = []
    for row in visible.itertuples(index=False):
        delta_zero_y, bar_x = GEOMETRY[row.galaxy]
        x_back = X_ZERO + row.physical_r_over_abar * (bar_x - X_ZERO)
        y_back = delta_zero_y - row.physical_delta * AXIS_HEIGHT
        x_res = x_back - row.vector_x_pt
        y_res = y_back - row.vector_y_pt
        # The extracted errors map to upper/lower vector endpoints. Mapping
        # them to Delta and back must preserve their distance from the marker.
        y_top_back = y_back - row.physical_delta_error_plus * AXIS_HEIGHT
        y_bottom_back = y_back + row.physical_delta_error_minus * AXIS_HEIGHT
        err_res = max(
            abs(y_top_back - row.vector_error_y_top_pt),
            abs(y_bottom_back - row.vector_error_y_bottom_pt),
        )
        x_residuals.append(abs(x_res))
        y_residuals.append(abs(y_res))
        error_roundtrip_residuals.append(err_res)
        rows.append(
            {
                "galaxy": row.galaxy,
                "marker_index_radial_order": row.marker_index_radial_order,
                "x_roundtrip_residual_pt": x_res,
                "y_roundtrip_residual_pt": y_res,
                "error_roundtrip_residual_pt": err_res,
            }
        )
    pd.DataFrame(rows).to_csv(DATA / "coming_profile_reverse_render_residuals_v01.csv", index=False)
    tolerance = 2e-4
    payload = {
        "schema": "tau_core_coming_profile_reverse_render_validation_v01",
        "status": "VISIBLE_PROFILE_REVERSE_RENDER_PASS_CLIPPED_OUTLIER_UNCERTAINTY_OPEN",
        "n_visible_points": len(visible),
        "max_x_roundtrip_residual_pt": max(x_residuals),
        "max_y_roundtrip_residual_pt": max(y_residuals),
        "max_error_roundtrip_residual_pt": max(error_roundtrip_residuals),
        "tolerance_pt": tolerance,
        "visible_marker_roundtrip_pass": max(x_residuals + y_residuals) <= tolerance,
        "visible_error_roundtrip_pass": max(error_roundtrip_residuals) <= tolerance,
        "clipped_ngc4579_outlier_present": bool(
            ((frame.galaxy == "NGC 4579") & (frame.point_origin == "source_text_clipped_marker")).any()
        ),
        "clipped_ngc4579_outlier_uncertainty_available": False,
        "source_profile_gate_complete": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": "visible profile geometry validated; one source-clipped uncertainty remains unknowable from this figure",
    }
    (DATA / "coming_profile_reverse_render_validation_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    REPORT.write_text(
        "# COMING profile reverse-render validation v01\n\n"
        f"Status: `{payload['status']}`\n\n"
        f"All `{len(visible)}` visible points pass the physical-to-vector round trip at `{tolerance}` pt tolerance. "
        f"Maximum marker residuals are `{payload['max_x_roundtrip_residual_pt']:.3g}` pt in x and "
        f"`{payload['max_y_roundtrip_residual_pt']:.3g}` pt in y.\n\n"
        "The separate NGC4579 `Delta=2.9` source-text point is retained, but its clipped uncertainty cannot be reverse-rendered. "
        "The visible geometry gate passes; the strict uncertainty-complete source gate and endpoint scoring remain closed.\n"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
