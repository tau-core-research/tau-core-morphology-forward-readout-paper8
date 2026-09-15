#!/usr/bin/env python3
"""Post-open identifiability audit for a future velocity-zero-point-safe terminal.

This script deliberately does not repair or rescore the frozen NGC4062
confirmatory endpoint.  It uses that opened endpoint only to diagnose the
linear algebra that a future, independently frozen terminal must satisfy.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/ngc4062_velocity_zero_point_orthogonalization_v01.md"
ENDPOINT = DATA / "ngc4062_halogas_confirmatory_endpoint_v01.json"


def stable_rank(array: np.ndarray, relative_tolerance: float = 1.0e-10) -> int:
    singular = np.linalg.svd(array, compute_uv=False)
    if singular.size == 0 or singular[0] == 0:
        return 0
    return int(np.sum(singular > relative_tolerance * singular[0]))


def weighted_nuisance_projector(nuisance: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    inverse = np.linalg.pinv(covariance)
    gram = nuisance.T @ inverse @ nuisance
    return np.eye(nuisance.shape[0]) - nuisance @ np.linalg.pinv(gram) @ nuisance.T @ inverse


def max_abs(array: np.ndarray) -> float:
    return float(np.max(np.abs(array)))


def main() -> None:
    endpoint = json.loads(ENDPOINT.read_text(encoding="utf-8"))
    if endpoint["status"] != "NGC4062_CONFIRMATORY_ENDPOINT_FAIL":
        raise RuntimeError("This post-open audit is tied to the preserved failed endpoint")

    primary_velocity = 769.0
    alternate_velocity = 758.0
    velocity_step = alternate_velocity - primary_velocity
    common_template = np.ones((2, 1))
    resolutions: dict[str, dict[str, object]] = {}

    for resolution in ("HR", "LR"):
        output = endpoint["outputs"][resolution]
        delta = np.asarray(output["delta_odd_by_radius_km_s"], dtype=float)
        covariance = np.asarray(output["covariance_km2_s2"], dtype=float)
        alternate = next(
            row for row in output["nuisance_variants"]
            if row["variant"] == "ghasp_systemic_758"
        )
        alternate_delta = np.asarray(alternate["delta_odd_by_radius_km_s"], dtype=float)

        # This secant is endpoint-informed and therefore diagnostic only.  A
        # future confirmatory terminal must source or calibrate its nuisance
        # tangent before its endpoint values are opened.
        nuisance = ((alternate_delta - delta) / velocity_step).reshape(-1, 1)
        inverse = np.linalg.pinv(covariance)
        projection = weighted_nuisance_projector(nuisance, covariance)
        projected_covariance = projection @ covariance @ projection.T
        projected_delta = projection @ delta
        statistic = float(delta @ inverse @ projection @ delta)
        degrees_of_freedom = stable_rank(projection)
        total_common_information = float((common_template.T @ inverse @ common_template).item())
        retained_common_information = float(
            (common_template.T @ inverse @ projection @ common_template).item()
        )
        information_fraction = retained_common_information / total_common_information
        invariance_errors = [
            max_abs(projection @ (delta + nuisance[:, 0] * shift) - projected_delta)
            for shift in (-100.0, -13.0, 0.0, 7.0, 100.0)
        ]
        augmented_rank = stable_rank(np.column_stack((nuisance, common_template)))
        resolutions[resolution] = {
            "post_open_secant_nuisance_tangent_dimensionless": nuisance[:, 0].tolist(),
            "nuisance_rank": stable_rank(nuisance),
            "projector_rank": degrees_of_freedom,
            "augmented_nuisance_common_template_rank": augmented_rank,
            "projector": projection.tolist(),
            "projected_delta_km_s": projected_delta.tolist(),
            "projected_covariance_km2_s2": projected_covariance.tolist(),
            "annihilation_max_abs": max_abs(projection @ nuisance),
            "idempotence_max_abs": max_abs(projection @ projection - projection),
            "weighted_self_adjoint_max_abs": max_abs(projection.T @ inverse - inverse @ projection),
            "zero_point_shift_invariance_max_abs_km_s": max(invariance_errors),
            "common_template_information_fraction_retained": information_fraction,
            "post_open_projected_zero_statistic": statistic,
            "post_open_projected_zero_dof": degrees_of_freedom,
            "post_open_projected_zero_p": float(chi2.sf(statistic, degrees_of_freedom)),
        }

    identity = np.eye(2)
    exact_common_nuisance = np.ones((2, 1))
    exact_projection = weighted_nuisance_projector(exact_common_nuisance, identity)
    exact_counterexample_information = float(
        (common_template.T @ exact_projection @ common_template).item()
    )
    operator_checks_pass = all(
        row["nuisance_rank"] == 1
        and row["projector_rank"] == 1
        and row["annihilation_max_abs"] < 1.0e-12
        and row["idempotence_max_abs"] < 1.0e-12
        and row["weighted_self_adjoint_max_abs"] < 1.0e-12
        and row["zero_point_shift_invariance_max_abs_km_s"] < 1.0e-10
        for row in resolutions.values()
    )
    result = {
        "schema": "ngc4062_velocity_zero_point_orthogonalization_v01",
        "status": "POST_OPEN_ORTHOGONALIZATION_DERIVED_FUTURE_FREEZE_REQUIRED",
        "input_endpoint_status": endpoint["status"],
        "analysis_role": "post-open identifiability and operator-design audit only",
        "endpoint_rescored": False,
        "confirmatory_status_changed": False,
        "velocity_step_km_s": velocity_step,
        "equation": "P_perp = I - G (G^T C^-1 G)^+ G^T C^-1",
        "units": {
            "d": "km/s",
            "C": "(km/s)^2",
            "G_dd_dvsys": "dimensionless",
            "P_perp": "dimensionless",
            "quadratic_statistic": "dimensionless",
        },
        "resolutions": resolutions,
        "exact_common_mode_counterexample": {
            "nuisance_tangent": [1.0, 1.0],
            "common_signal_template": [1.0, 1.0],
            "projected_common_information": exact_counterexample_information,
            "conclusion": "A common signal is unidentifiable when it is collinear with the velocity-zero-point nuisance.",
        },
        "operator_checks_pass": operator_checks_pass,
        "derived_results": {
            "nuisance_shifts_are_annihilated": True,
            "one_of_two_radial_degrees_of_freedom_is_removed": True,
            "current_common_mean_is_nearly_erased": True,
            "future_target_requires_rank_increment": "rank([G,s]) = rank(G) + 1",
        },
        "future_freeze_requirements": [
            "derive or calibrate G without opening the future endpoint contrast",
            "use a linear or otherwise differentiably calibrated radial estimator",
            "freeze the covariance, nuisance span, target template, rank tolerance, and minimum information rule",
            "open an independent survey/sample; do not reuse NGC4062 as confirmation",
        ],
        "first_questionable_step": (
            "The NGC4062 secant tangent uses two already opened systemic-velocity reductions and is not source-owned; "
            "it cannot define a confirmatory terminal."
        ),
        "claim_boundary": (
            "The covariance-weighted nuisance projection is an algebraic result and the NGC4062 numbers are post-open "
            "diagnostics.  They do not repair the failed endpoint, select a physical q_R, establish parent morphology "
            "or Nature occupation, or support a dark-matter replacement claim."
        ),
    }
    if not operator_checks_pass or exact_counterexample_information > 1.0e-12:
        raise RuntimeError("Velocity-zero-point projection audit failed")

    output = DATA / "ngc4062_velocity_zero_point_orthogonalization_v01.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    hr = resolutions["HR"]
    lr = resolutions["LR"]
    REPORT.write_text(
        "# NGC4062 velocity-zero-point orthogonalization audit v0.1\n\n"
        f"**Status:** `{result['status']}`\n\n"
        "For a future radial contrast vector $d$, covariance $C$, and a source-frozen "
        "velocity-zero-point tangent matrix $G$, the covariance-weighted residual maker is\n\n"
        "```text\nP_perp = I - G (G^T C^-1 G)^+ G^T C^-1.\n```\n\n"
        "It obeys $P_\\perp G=0$, $P_\\perp^2=P_\\perp$, and covariance-weighted "
        "self-adjointness. Consequently $P_\\perp(d+G\\eta)=P_\\perp d$: an additive "
        "systemic-velocity nuisance cannot create the projected signal. With two rings and one "
        "nuisance direction, however, only one radial degree of freedom remains.\n\n"
        "The opened 769-to-758 km/s secants are diagnostic only. They retain just "
        f"`{hr['common_template_information_fraction_retained']:.6g}` (HR) and "
        f"`{lr['common_template_information_fraction_retained']:.6g}` (LR) of the covariance-weighted "
        "information in a constant radial signal. The projected post-open zero tests also remain "
        f"non-significant (HR $p={hr['post_open_projected_zero_p']:.3f}$; "
        f"LR $p={lr['post_open_projected_zero_p']:.3f}$), but these are not new confirmatory scores.\n\n"
        "The decisive counterexample is exact: if the desired signal template and the nuisance "
        "tangent are both $(1,1)^T$, projection removes the entire signal. A future terminal is "
        "identifiable only if `rank([G,s]) = rank(G) + 1`, with a predeclared minimum retained-information "
        "rule. Because the present weighted-median tangent was estimated from opened reductions, the "
        "physical/source-owned $G$ is still missing. NGC4062 remains a failed, calibration-limited endpoint.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
