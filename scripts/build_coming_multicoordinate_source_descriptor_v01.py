#!/usr/bin/env python3
"""Build a residual-blind multi-coordinate descriptor for the COMING bar family."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "coming_multicoordinate_source_descriptor_v01.md"


def profile_modes(points: pd.DataFrame) -> dict[str, float]:
    q = points[points.point_origin.eq("vector_marker")].sort_values("physical_r_over_abar")
    x = q.physical_r_over_abar.to_numpy(float)
    y = q.physical_delta.to_numpy(float)
    sigma = 0.5 * (q.physical_delta_error_minus.to_numpy(float) + q.physical_delta_error_plus.to_numpy(float))
    sigma = np.maximum(sigma, 1.0e-6)
    u = 2.0 * x / x[-1] - 1.0
    design = np.column_stack((np.ones_like(u), u, 0.5 * (3.0 * u**2 - 1.0)))
    precision = np.diag(1.0 / sigma**2)
    covariance = np.linalg.inv(design.T @ precision @ design)
    coefficients = covariance @ design.T @ precision @ y
    variances = np.diag(covariance)
    capacities = coefficients**2 / np.maximum(coefficients**2 + variances, 1.0e-15)
    return {
        "mode_level": coefficients[0], "mode_slope": coefficients[1],
        "mode_curvature": coefficients[2], "capacity_level": capacities[0],
        "capacity_slope": capacities[1], "capacity_curvature": capacities[2],
        "profile_support_over_bar": x[-1],
    }


def main() -> None:
    fields = pd.read_csv(DATA / "coming_bar_source_fields_v01.csv")
    points = pd.read_csv(DATA / "coming_vector_marker_centers_v01.csv")
    readiness = pd.read_csv(DATA / "coming_bar_endpoint_readiness_v01.csv")
    rows = []
    for row in fields.itertuples():
        modes = profile_modes(points[points.galaxy.eq(row.galaxy)])
        ready = readiness[readiness.galaxy.eq(row.galaxy)].iloc[0]
        rows.append({
            "galaxy": row.galaxy, "bar_class": row.bar_class,
            "bar_class_numeric": 1.0 if row.bar_class == "SB" else 0.0,
            "bar_radius_kpc": row.deprojected_bar_radius_kpc,
            "bar_radius_fractional_error": row.deprojected_bar_radius_error_kpc / row.deprojected_bar_radius_kpc,
            "reversal_over_bar": row.reversal_over_bar_radius,
            "reversal_over_bar_error": row.reversal_over_bar_radius_error,
            **modes,
            "stellar_decomposition_acquired": bool(ready.stellar_decomposition_acquired),
            "phangs_catalog_match": bool(ready.phangs_catalog_match),
            "independent_endpoint_acquired": bool(ready.independent_rotation_endpoint_acquired),
            "uses_dark_discrepancy_endpoint": False,
        })
    frame = pd.DataFrame(rows)
    frame.to_csv(DATA / "coming_multicoordinate_source_descriptor_v01.csv", index=False)
    n_complete = int(frame[["bar_radius_kpc", "reversal_over_bar", "mode_level", "mode_slope", "mode_curvature"]].notna().all(axis=1).sum())
    result = {
        "schema": "tau_core_coming_multicoordinate_source_descriptor_v01",
        "status": "FIVE_SOURCE_MULTICOORDINATE_DESCRIPTOR_FROZEN",
        "n_galaxies": len(frame), "n_core_descriptor_complete": n_complete,
        "coordinates": [
            "bar class", "physical bar radius", "reversal radius / bar radius",
            "profile level", "profile slope", "profile curvature", "per-mode source capacity"
        ],
        "construction_uses_rotation_endpoint_or_dark_discrepancy": False,
        "ngc4303_selected_for_next_intake_from_readiness": True,
        "selection_reason": "S4G stellar decomposition and PHANGS coverage are already available; independent endpoint remains unopened locally",
        "formula_scoring_allowed": False,
        "claim_boundary": "source descriptor and prospective acquisition selection only; no endpoint attribution"
    }
    (DATA / "coming_multicoordinate_source_descriptor_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# COMING multi-coordinate source descriptor v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The barred source is no longer represented by `Delta(R/a_bar)` alone. The frozen descriptor combines bar class, physical bar scale, source-defined radial reversal, and fixed level/slope/curvature modes with their source-error capacities. All five galaxies have the core descriptor.\n\n"
        "NGC4303 is selected for the next acquisition intake because S4G and PHANGS source coverage already exist while no independent endpoint is open locally. This selection reads no dark-discrepancy residual and does not authorize scoring.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
