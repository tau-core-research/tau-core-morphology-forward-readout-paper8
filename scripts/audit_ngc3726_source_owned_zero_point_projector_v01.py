#!/usr/bin/env python3
"""Audit a source-derived systemic-velocity nuisance projector on NGC3726.

NGC3726 was already opened as a development/preflight diagnostic.  This audit
therefore tests the operator and identifiability only; it is not a prospective
endpoint or a Tau-specific score.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/ngc3726_source_owned_zero_point_projector_v01.md"
PREFLIGHT_JSON = DATA / "ngc3726_hi_halpha_channel_preflight_v01.json"
PREFLIGHT_CSV = DATA / "ngc3726_hi_halpha_channel_preflight_v01.csv"


def stable_rank(array: np.ndarray, relative_tolerance: float = 1.0e-10) -> int:
    singular = np.linalg.svd(array, compute_uv=False)
    if singular.size == 0 or singular[0] == 0:
        return 0
    return int(np.sum(singular > relative_tolerance * singular[0]))


def max_abs(array: np.ndarray) -> float:
    return float(np.max(np.abs(array)))


def main() -> None:
    preflight = json.loads(PREFLIGHT_JSON.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(PREFLIGHT_CSV.open(newline="", encoding="utf-8")))
    if preflight["status"] != "NGC3726_TWO_TRACER_ODD_CONTRAST_NULL_NOT_REJECTED_PATTERN_DIAGNOSTIC":
        raise RuntimeError("Unexpected NGC3726 development input status")

    delta = np.asarray([float(row["delta_odd_los_km_s"]) for row in rows])
    covariance = (
        np.asarray(preflight["covariance_components"]["halpha_odd"], dtype=float)
        + np.asarray(preflight["covariance_components"]["hi_odd"], dtype=float)
        + np.asarray(preflight["covariance_components"]["cross_tracer"], dtype=float)
    )
    inverse = np.linalg.inv(covariance)
    n_radii = len(delta)

    # For u_r=(v_los,r-v_sys) and u_a=(v_sys-v_los,a), the side-odd
    # quantity O=u_r-u_a has dO/dv_sys=-2.  Hence
    # d(O_Halpha-O_HI)/d(vsys_Halpha,vsys_HI)=(-2,+2) at every radius.
    nuisance = np.column_stack((-2.0 * np.ones(n_radii), 2.0 * np.ones(n_radii)))
    nuisance_gram = nuisance.T @ inverse @ nuisance
    projection = (
        np.eye(n_radii)
        - nuisance @ np.linalg.pinv(nuisance_gram) @ nuisance.T @ inverse
    )
    projected = projection @ delta
    projected_covariance = projection @ covariance @ projection.T
    statistic = float(delta @ inverse @ projection @ delta)
    degrees_of_freedom = stable_rank(projection)
    p_value = float(chi2.sf(statistic, degrees_of_freedom))
    shifts = (
        np.asarray([-30.0, 0.0]),
        np.asarray([0.0, 17.0]),
        np.asarray([11.0, -9.0]),
    )
    invariance_error = max(
        max_abs(projection @ (delta + nuisance @ eta) - projected)
        for eta in shifts
    )
    constant = np.ones((n_radii, 1))
    constant_information_after_projection = float(
        (constant.T @ inverse @ projection @ constant).item()
    )
    checks = {
        "nuisance_rank_is_one": stable_rank(nuisance) == 1,
        "projector_rank_is_five": degrees_of_freedom == 5,
        "nuisance_annihilated": max_abs(projection @ nuisance) < 1.0e-12,
        "projector_idempotent": max_abs(projection @ projection - projection) < 1.0e-12,
        "weighted_self_adjoint": max_abs(projection.T @ inverse - inverse @ projection) < 1.0e-12,
        "finite_shift_invariant": invariance_error < 1.0e-10,
        "constant_radial_mode_annihilated": abs(constant_information_after_projection) < 1.0e-12,
        "matches_previous_constant_residual_statistic": abs(
            statistic - float(preflight["primary_odd_contrast"]["chi2_constant"])
        ) < 1.0e-10,
    }
    if not all(checks.values()):
        raise RuntimeError(f"NGC3726 zero-point projector audit failed: {checks}")

    result = {
        "schema": "ngc3726_source_owned_zero_point_projector_v01",
        "status": "SOURCE_DERIVED_ZERO_POINT_PROJECTOR_PASS_OPENED_SHAPE_NULL_NOT_REJECTED",
        "galaxy": "NGC3726",
        "analysis_role": "operator validation on an already opened independent-survey development case",
        "confirmatory_endpoint": False,
        "endpoint_rescored": False,
        "n_common_radii": n_radii,
        "nuisance_parameters": ["delta_vsys_halpha_km_s", "delta_vsys_hi_km_s"],
        "nuisance_tangent": nuisance.tolist(),
        "nuisance_rank": stable_rank(nuisance),
        "projector_rank": degrees_of_freedom,
        "projector": projection.tolist(),
        "projected_delta_odd_los_km_s": projected.tolist(),
        "projected_covariance_km2_s2": projected_covariance.tolist(),
        "shape_zero_statistic": statistic,
        "shape_zero_dof": degrees_of_freedom,
        "shape_zero_p": p_value,
        "operator_checks": checks,
        "operator_checks_pass": all(checks.values()),
        "derivation": {
            "side_convention": "u_r=v_los,r-v_sys and u_a=v_sys-v_los,a after line-of-sight transport",
            "single_tracer_derivative": "d(u_r-u_a)/d(v_sys)=-2",
            "cross_tracer_derivatives": "d Delta_O/d(vsys_Halpha,vsys_HI)=(-2,+2)",
            "rank_result": "the two zero points span one common radial nuisance direction",
            "projector": "P_perp=I-G(G^T C^-1 G)^+G^T C^-1",
        },
        "units": {
            "delta": "km/s",
            "nuisance_parameters": "km/s",
            "nuisance_tangent": "dimensionless",
            "covariance": "(km/s)^2",
            "projector": "dimensionless",
            "statistic": "dimensionless",
        },
        "assumptions": [
            "each published side curve uses one radius-independent systemic velocity",
            "approaching and receding side signs follow the frozen common convention",
            "the line-of-sight transport is linear in the side velocities",
            "the recorded covariance is adequate; missing beam, center, PA, radial, and phase-dependent terms remain limitations",
        ],
        "derived_result": (
            "six radii minus one common zero-point nuisance direction leave five shape degrees of freedom; "
            "the opened shape-only zero test is not rejected"
        ),
        "interpretation": (
            "The source-derived operator solves the constant velocity-zero-point degeneracy for radial shape tests, "
            "but it deliberately cannot test a constant radial signal and supplies no morphology-specific target template."
        ),
        "next_finite_action": (
            "freeze the same operator plus an independently source-derived nonconstant morphology template on a new, unopened survey/sample"
        ),
        "claim_boundary": (
            "standard kinematic nuisance projection and a preserved null development result; not a Tau detection, "
            "physical q_R, parent-morphology attribution, Nature occupation, or dark-matter replacement result"
        ),
    }
    output = DATA / "ngc3726_source_owned_zero_point_projector_v01.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# NGC3726 source-owned velocity-zero-point projector v0.1\n\n"
        f"**Status:** `{result['status']}`\n\n"
        "For each tracer, a fixed systemic-velocity shift changes the receding-minus-approaching "
        "line-of-sight odd contrast with derivative `-2`. The two independent tracer zero points "
        "therefore generate columns `(-2,+2)` repeated at every radius. Those columns are "
        "collinear and span one common radial nuisance mode.\n\n"
        "The covariance-weighted projector passes annihilation, idempotence, weighted self-adjointness, "
        "finite-shift invariance, and constant-mode controls. Six common radii leave five radial shape "
        f"degrees of freedom. The already opened shape-only statistic is `chi2={statistic:.4f}` for "
        f"`5` degrees of freedom (`p={p_value:.4f}`), so zero remains unrejected.\n\n"
        "This improves the method, not the empirical status. It removes any radius-independent relative "
        "velocity-zero-point offset exactly, but it also removes every constant radial signal. No "
        "morphology-specific nonconstant template is supplied, and missing beam/center/PA/radial covariance "
        "remains. Because NGC3726 was opened before this audit, it is an independent-survey development "
        "control rather than a new confirmatory endpoint.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
