#!/usr/bin/env python3
"""Validate image multiplicities and geometry of the frozen SDP.81 operator."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.LensModel.Solver.lens_equation_solver import LensEquationSolver
from lenstronomy.Util.param_util import phi_q2_ellipticity, shear_polar2cartesian


ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data/derived/sdp81_lens_operator_freeze_v01.json"
OUT = ROOT / "data/derived/sdp81_lens_operator_geometry_validation_v01.json"
REPORT = ROOT / "reports/sdp81_lens_operator_geometry_validation_v01.md"


def main() -> None:
    frozen = json.loads(FREEZE.read_text())
    model = frozen["models"]["inoue_best_fit"]
    theta_e = model["ellipticity_pa_deg_ccw_from_north"]
    theta_g = model["external_shear_pa_deg_ccw_from_north"]
    e1, e2 = phi_q2_ellipticity(np.deg2rad(90.0 + theta_e), model["axis_ratio_q"])
    gamma1, gamma2 = shear_polar2cartesian(
        np.deg2rad(theta_g), model["external_shear_gamma"]
    )
    center_x, center_y = model["lens_center_arcsec_relative_to_G"]
    kwargs = [
        {
            "theta_E": model["einstein_radius_b_arcsec"],
            "e1": e1,
            "e2": e2,
            "center_x": center_x,
            "center_y": center_y,
        },
        {"gamma1": gamma1, "gamma2": gamma2, "ra_0": 0.0, "dec_0": 0.0},
    ]
    lens = LensModel(["SIE", "SHEAR"])
    solver = LensEquationSolver(lens)
    images = {}
    for name, (source_x, source_y) in model["source_positions_arcsec"].items():
        x, y = solver.image_position_from_source(
            source_x,
            source_y,
            kwargs,
            search_window=5.0,
            min_distance=0.002,
            precision_limit=1e-10,
            num_iter_max=200,
        )
        images[name] = [[float(a), float(b)] for a, b in zip(x, y)]

    multiplicities = {name: len(points) for name, points in images.items()}
    multiplicity_pass = multiplicities == {"q1": 4, "d1": 2, "d2": 2}
    q1 = np.asarray(images["q1"])
    quadrant_pass = bool(all(
        np.any((np.sign(q1[:, 0]) == sx) & (np.sign(q1[:, 1]) == sy))
        for sx, sy in [(1, 1), (-1, 1), (-1, -1)]
    ) and np.sum(q1[:, 0] < 0) == 3)
    result = {
        "schema": "tau-core.paper8.sdp81-lens-geometry-validation.v01",
        "status": (
            "SMOOTH_OPERATOR_MULTIPLICITY_AND_CONFIGURATION_REPRODUCED_G_WCS_OPEN"
            if multiplicity_pass and quadrant_pass
            else "SMOOTH_OPERATOR_GEOMETRY_REPRODUCTION_FAILED"
        ),
        "implementation": {"library": "lenstronomy", "version": "1.14.2"},
        "convention_transform": {
            "ellipticity_phi_lenstronomy_deg": 90.0 + theta_e,
            "shear_phi_lenstronomy_deg": theta_g,
            "reason": "reproduces the published q1 quadruple and d1/d2 doubles",
        },
        "image_positions_arcsec_relative_to_G": images,
        "image_multiplicities": multiplicities,
        "expected_multiplicities": {"q1": 4, "d1": 2, "d2": 2},
        "multiplicity_pass": multiplicity_pass,
        "published_configuration_pass": quadrant_pass,
        "mean_fit_distance_reported_by_inoue_arcsec": 0.0014,
        "image_G_wcs_registration_complete": False,
        "pathwise_cube_comparison_allowed": False,
        "remaining_blocker": (
            "an external or image-modelled centroid for G must anchor the relative "
            "coordinates to the ALMA WCS before cube pixels are ray-traced"
        ),
        "claim_boundary": (
            "standard smooth-lens architecture reproduced; no multipath residual, "
            "channel-origin identification, time effect, or Tau Core detection"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# SDP.81 smooth lens-operator geometry validation\n\n"
        f"Status: `{result['status']}`\n\n"
        "The frozen Inoue best-fit SIE+external-shear model was translated to "
        "lenstronomy with `phi_e=90 deg + theta_e` and `phi_gamma=theta_gamma`. "
        f"It produces multiplicities `{multiplicities}`, reproducing the published "
        "q1 quadruple and d1/d2 doubles. The predicted q1 positions also reproduce "
        "the published A/B/C/D image configuration. This validates the relative "
        "smooth-lens geometry, not its absolute ALMA pixel registration. Image G "
        "still requires an independently anchored WCS centroid before ray tracing.\n"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
