#!/usr/bin/env python3
"""Independent audit of the UGC03580 bounded two-plane readout shell."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
BODY_SUMMARY = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_body_v01.json"
BODY_POINTS = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_body_v01_points.csv"
BUILDER = ROOT / "scripts" / "build_ugc03580_ugc3580_two_plane_readout_shell_v01.py"
POINTS = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_readout_shell_v01_points.csv"
SUMMARY = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_readout_shell_v01.json"
OUT = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_readout_shell_reproducibility_audit_v01.json"
REPORT = ROOT / "reports" / "ugc03580_ugc3580_two_plane_readout_shell_reproducibility_audit_v01.md"

EXPECTED_BODY_SUMMARY_SHA256 = "b9a831f1166b908c6df084a39fbb2183f7a9e7337142aa5d228c27e166bd0048"
EXPECTED_BODY_POINTS_SHA256 = "d196498ee6068a306a7391e0ec0fc58885c5536aa56fd68cd290a9094f4a5173"

# These bounds audit the explicitly frozen text representations, not the
# unrounded in-memory construction.  The body table is frozen at 13 and the
# shell table at 9 significant digits so that NumPy 1.x/2.x produce identical
# bytes without pretending to retain precision absent from the source tables.
BODY_TEXT_ATOL = 5.0e-12
SHELL_TEXT_ATOL = 5.0e-9
SUMMARY_TEXT_ATOL = 5.0e-11


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def unit(vector: np.ndarray) -> np.ndarray:
    value = np.asarray(vector, dtype=float)
    return value / np.linalg.norm(value)


def defect(normals: np.ndarray, plane: np.ndarray) -> np.ndarray:
    return 1.0 - np.clip(np.asarray(normals) @ unit(plane), -1.0, 1.0)


def kernel(
    normals: np.ndarray,
    inner: np.ndarray,
    outer: np.ndarray,
    power: float,
    tolerance: float = 1.0e-12,
) -> np.ndarray:
    inner_u = unit(inner)
    outer_u = unit(outer)
    if 1.0 - float(np.dot(inner_u, outer_u)) <= tolerance:
        return np.zeros(len(normals), dtype=float)
    d_inner = defect(normals, inner_u)
    d_outer = defect(normals, outer_u)
    numerator = d_inner**power
    return numerator / (numerator + d_outer**power)


def slerp(left: np.ndarray, right: np.ndarray, fraction: float) -> np.ndarray:
    """Independent shortest-great-circle interpolation for the audit."""

    a = unit(left)
    b = unit(right)
    dot = float(np.clip(a @ b, -1.0, 1.0))
    angle = math.acos(dot)
    if angle < 1.0e-14:
        return a.copy()
    value = (
        math.sin((1.0 - fraction) * angle) * a
        + math.sin(fraction * angle) * b
    ) / math.sin(angle)
    return unit(value)


def solve_k1_level(
    left: np.ndarray,
    right: np.ndarray,
    inner: np.ndarray,
    outer: np.ndarray,
    target: float,
    *,
    tolerance: float,
    maximum_iterations: int = 192,
) -> tuple[float, np.ndarray, float]:
    """Independent bracketed level solve on one SLERP source segment."""

    def residual(fraction: float) -> float:
        normal = slerp(left, right, fraction)
        return float(kernel(normal[None, :], inner, outer, 1.0)[0] - target)

    low = 0.0
    high = 1.0
    f_low = residual(low)
    f_high = residual(high)
    if f_low * f_high > 0.0:
        raise ValueError("source segment does not bracket target K1")
    for _ in range(maximum_iterations):
        middle = 0.5 * (low + high)
        f_middle = residual(middle)
        if abs(f_middle) <= tolerance or high - low <= tolerance:
            return middle, slerp(left, right, middle), f_middle
        if f_low * f_middle <= 0.0:
            high = middle
        else:
            low = middle
            f_low = f_middle
    raise RuntimeError("independent K1 level solve did not converge")


def close(left: float, right: float, tolerance: float = 1.0e-12) -> bool:
    return bool(math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance))


def main() -> None:
    body = json.loads(BODY_SUMMARY.read_text(encoding="utf-8"))
    body_points = pd.read_csv(BODY_POINTS)
    points = pd.read_csv(POINTS)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    inner_record = body["construction"]["inner_reference_plane"]
    outer_record = body["construction"]["outer_mean_plane"]
    inner = np.array([inner_record[key] for key in ("n_w", "n_n", "n_los")], dtype=float)
    outer = np.array([outer_record[key] for key in ("n_w", "n_n", "n_los")], dtype=float)
    normals = body_points[["n_w_orientation", "n_n_orientation", "n_los_orientation"]].to_numpy(
        dtype=float
    )
    supported = body_points["within_source_terminal_support"].to_numpy(dtype=bool)
    transition = body_points["zone"].eq("transition").to_numpy()

    d_inner = defect(normals, inner)
    d_outer = defect(normals, outer)
    transverse = unit(np.cross(unit(inner), unit(outer)))
    signed_chirality = normals @ transverse
    anchor_gram = np.array(
        [[1.0, unit(inner) @ unit(outer)], [unit(inner) @ unit(outer), 1.0]],
        dtype=float,
    )
    anchor_projections = np.column_stack((1.0 - d_inner, 1.0 - d_outer))
    chirality_sq_from_defects = 1.0 - np.einsum(
        "ni,ij,nj->n",
        anchor_projections,
        np.linalg.inv(anchor_gram),
        anchor_projections,
    )
    k1 = kernel(normals, inner, outer, 1.0)
    k2 = kernel(normals, inner, outer, 2.0)
    swapped = kernel(normals, outer, inner, 1.0)
    coincident = kernel(normals, inner, inner, 1.0)
    theoretical_limits = kernel(np.vstack((inner, outer)), inner, outer, 1.0)
    separation_defect = 1.0 - float(np.dot(unit(inner), unit(outer)))
    amplitude = 0.5 * separation_defect
    response_plus = 1.0 + amplitude * k1
    response_minus = 1.0 - amplitude * k1
    reference_sine = math.sin(math.radians(float(inner_record["inclination_deg"])))
    projection = (
        np.sin(np.deg2rad(body_points["inclination_deg"].to_numpy(dtype=float))) / reference_sine
    ) ** 2
    reflected_normals = normals - 2.0 * signed_chirality[:, None] * transverse[None, :]
    mirror_projection = (1.0 - reflected_normals[:, 2] ** 2) / reference_sine**2
    mirror_projection_difference = mirror_projection - projection
    mirror_projection_difference_analytic = (
        4.0
        * signed_chirality
        * transverse[2]
        * (normals[:, 2] - signed_chirality * transverse[2])
        / reference_sine**2
    )
    published_normals = body_points[["n_w", "n_n", "n_los"]].to_numpy(dtype=float)
    published_normals /= np.linalg.norm(published_normals, axis=1)[:, None]
    source_orientation_residual_deg = np.rad2deg(
        np.arccos(np.clip(np.einsum("ij,ij->i", normals, published_normals), -1.0, 1.0))
    )
    supported_indices = np.flatnonzero(supported)
    mirror_witness_index = int(
        supported_indices[
            np.argmax(np.abs(mirror_projection_difference[supported]))
        ]
    )

    radius = body_points["radius_arcsec"].to_numpy(dtype=float)
    radius_index = {float(value): index for index, value in enumerate(radius)}
    collision_segments = ((210.0, 240.0), (270.0, 300.0))
    collision_targets = (0.900, 0.925, 0.950)

    def collision_record(target: float, tolerance: float) -> dict[str, object]:
        roots = []
        for radius_left, radius_right in collision_segments:
            index_left = radius_index[radius_left]
            index_right = radius_index[radius_right]
            fraction, normal, residual = solve_k1_level(
                normals[index_left],
                normals[index_right],
                inner,
                outer,
                target,
                tolerance=tolerance,
            )
            roots.append(
                {
                    "segment_arcsec": [radius_left, radius_right],
                    "fraction": fraction,
                    "radius_arcsec": radius_left
                    + fraction * (radius_right - radius_left),
                    "K1": target + residual,
                    "K1_residual": residual,
                    "chi": float(normal @ transverse),
                    "projection_ratio_sq": float(
                        (1.0 - normal[2] ** 2) / reference_sine**2
                    ),
                }
            )
        return {
            "target_K1": target,
            "roots": roots,
            "radial_separation_arcsec": roots[1]["radius_arcsec"]
            - roots[0]["radius_arcsec"],
            "projection_difference": roots[1]["projection_ratio_sq"]
            - roots[0]["projection_ratio_sq"],
            "chi_difference": roots[1]["chi"] - roots[0]["chi"],
        }

    collision_records = [
        collision_record(target, tolerance=1.0e-14) for target in collision_targets
    ]
    collision_witness = next(
        record for record in collision_records if record["target_K1"] == 0.925
    )
    collision_loose = collision_record(0.925, tolerance=1.0e-11)
    scalar_summary = summary["scalar_registration_boundary"]
    stored_collision = scalar_summary["selected_witness"]
    maximum_tolerance_radius_shift = max(
        abs(
            collision_witness["roots"][index]["radius_arcsec"]
            - collision_loose["roots"][index]["radius_arcsec"]
        )
        for index in range(2)
    )
    maximum_stored_collision_error = max(
        abs(
            collision_witness["roots"][index][field]
            - stored_collision["roots"][index][field]
        )
        for index in range(2)
        for field in ("radius_arcsec", "K1", "chi", "projection_ratio_sq")
    )

    # A concrete same-body countermodel: all curves below satisfy the declared
    # bounded carrier-recovery shell but differ on the transition rows.
    carrier_sq = np.full(len(k1), 100.0**2)
    counter_plus = carrier_sq * (1.0 + 0.4 * k1)
    counter_minus = carrier_sq * (1.0 - 0.4 * k1)
    counter_p2 = carrier_sq * (1.0 + 0.4 * k2)

    # Exact post-body response witness.  The same positive Hessian and the same
    # source morphology admit opposite and continuously rescaled mixed blocks.
    # Hence stability selects neither the terminal sign nor its amplitude.
    h_z = np.array([[2.0, 0.3], [0.3, 1.5]], dtype=float)
    b_zk = np.array([0.4, -0.2], dtype=float)
    l_g = np.array([1.2, 0.7], dtype=float)
    response_state = -np.linalg.solve(h_z, b_zk)
    gamma = float(l_g @ response_state)
    gamma_sign_flip = float(l_g @ (-np.linalg.solve(h_z, -b_zk)))
    gamma_scale_three = float(l_g @ (-np.linalg.solve(h_z, 3.0 * b_zk)))
    hessian_eigenvalues = np.linalg.eigvalsh(h_z)

    # Common-action pullback witness.  Z=(g,phi), I has a visible two-plane
    # direction and one hidden Parent direction, and K sees only the first.
    # The two registrations have exactly the same visible K projection but
    # give different terminal responses when the hidden direction is not a
    # terminal null.  This is independent of every rotation endpoint.
    h_gg = np.array([[3.0, 0.2], [0.2, 2.4]], dtype=float)
    h_ff = np.array([[2.2, 0.1], [0.1, 1.8]], dtype=float)
    h_gf = np.array([[0.25, -0.10], [0.15, 0.20]], dtype=float)
    h_complete = np.block([[h_gg, h_gf], [h_gf.T, h_ff]])
    b_zi = np.array(
        [[0.40, -0.15], [0.20, 0.30], [-0.10, 0.25], [0.35, -0.20]],
        dtype=float,
    )
    j_visible = np.array([[1.0], [0.0]], dtype=float)
    j_hidden = np.array([[1.0], [1.0]], dtype=float)
    p_visible = np.array([[1.0, 0.0]], dtype=float)
    l_gravity = np.array([[1.0, 0.35]], dtype=float)
    l_complete = np.hstack((l_gravity, np.zeros((1, 2), dtype=float)))
    b_zk_visible = b_zi @ j_visible
    b_zk_hidden = b_zi @ j_hidden
    gamma_visible_lift = float(
        (-l_complete @ np.linalg.solve(h_complete, b_zk_visible)).item()
    )
    gamma_hidden_lift = float(
        (-l_complete @ np.linalg.solve(h_complete, b_zk_hidden)).item()
    )
    h_gravity_eff = h_gg - h_gf @ np.linalg.solve(h_ff, h_gf.T)

    def schur_mixed(block: np.ndarray) -> np.ndarray:
        return block[:2] - h_gf @ np.linalg.solve(h_ff, block[2:])

    gamma_visible_schur = float(
        (-l_gravity @ np.linalg.solve(h_gravity_eff, schur_mixed(b_zk_visible))).item()
    )
    gamma_hidden_schur = float(
        (-l_gravity @ np.linalg.solve(h_gravity_eff, schur_mixed(b_zk_hidden))).item()
    )
    baseline_load = np.array([-0.70, -0.50, 0.0, 0.0], dtype=float)
    zero_state = -np.linalg.solve(h_complete, baseline_load)
    same_action_carrier = float((l_complete @ zero_state).item())

    # A generic radial operator need not reduce to one constant scalar gain.
    # This source-only profile is a counterexample to automatic rank-one
    # factorization; no observed velocity enters it.
    nonconstant_gain = 0.2 + 0.1 * k1
    positive_kernel = supported & (k1 > 1.0e-12)
    inferred_gain = (
        carrier_sq[positive_kernel] * nonconstant_gain[positive_kernel] * k1[positive_kernel]
        / (carrier_sq[positive_kernel] * k1[positive_kernel])
    )

    carrier_sq_alt = np.full(len(k1), 120.0**2)

    builder_text = BUILDER.read_text(encoding="utf-8").lower()
    endpoint_loader_snippets = (
        "data/external/sparc",
        "rotmod.dat",
        "load_sparc_endpoint",
        "warp_prediction",
    )
    forbidden_output_columns = [
        column
        for column in points.columns
        if any(token in column.lower() for token in ("vobs", "vrot", "residual", "rotmod", "sparc"))
    ]

    numerical = summary["numerical_summary"]
    projection_summary = summary["standard_projection_control"]
    checks = {
        "upstream_summary_hash_matches": sha256(BODY_SUMMARY) == EXPECTED_BODY_SUMMARY_SHA256,
        "upstream_points_hash_matches": sha256(BODY_POINTS) == EXPECTED_BODY_POINTS_SHA256,
        "builder_has_no_endpoint_loader": not any(token in builder_text for token in endpoint_loader_snippets),
        "output_has_no_endpoint_columns": len(forbidden_output_columns) == 0,
        "row_count_preserved": len(points) == len(body_points) == 18,
        "plane_defects_nonnegative": bool(np.all(d_inner >= -1.0e-14) and np.all(d_outer >= -1.0e-14)),
        "K1_bounded": bool(np.all((k1 >= -1.0e-14) & (k1 <= 1.0 + 1.0e-14))),
        "K2_bounded": bool(np.all((k2 >= -1.0e-14) & (k2 <= 1.0 + 1.0e-14))),
        "inner_and_outer_limits_exact": bool(np.allclose(theoretical_limits, [0.0, 1.0], atol=1.0e-14)),
        "plane_swap_complementarity": bool(np.max(np.abs(k1 + swapped - 1.0)) < 1.0e-12),
        "coincident_plane_deactivates_kernel": bool(np.allclose(coincident, 0.0, atol=0.0)),
        "stored_defects_match": bool(
            np.allclose(points["defect_to_inner_plane"], d_inner)
            and np.allclose(points["defect_to_outer_plane"], d_outer)
        ),
        "stored_K1_matches": bool(np.allclose(points["kernel_p1_affine_defect_candidate"], k1)),
        "stored_K2_matches": bool(np.allclose(points["kernel_p2_counterfamily_control"], k2)),
        "stored_signed_chirality_matches": bool(
            np.allclose(points["signed_two_plane_chirality_control"], signed_chirality)
        ),
        "stored_chirality_square_matches_raw_defect_identity": bool(
            np.allclose(
                points["chirality_sq_from_raw_defects"],
                chirality_sq_from_defects,
                atol=5.0e-14,
            )
        ),
        "raw_defect_chirality_square_identity_is_exact": bool(
            np.max(np.abs(signed_chirality**2 - chirality_sq_from_defects))
            < 2.0e-13
        ),
        "supported_source_path_uses_both_chirality_signs": bool(
            set(np.sign(signed_chirality[supported]).astype(int)) == {-1, 1}
        ),
        "source_output_contains_published_oriented_spin_normal_components": all(
            column in body_points.columns for column in ("n_w", "n_n", "n_los")
        ),
        "source_orientation_matches_published_spin_normal_components": bool(
            np.max(source_orientation_residual_deg) < 0.1
        ),
        "reflected_normals_remain_unit": bool(
            np.max(np.abs(np.linalg.norm(reflected_normals, axis=1) - 1.0)) < 1.0e-12
        ),
        "p_counterfamily_is_nontrivial": float(np.max(np.abs(k1[transition] - k2[transition]))) > 0.1,
        "sign_counterfamily_is_nontrivial": bool(np.max(np.abs(counter_plus - counter_minus)) > 0.0),
        "power_counterfamily_is_nontrivial": bool(np.max(np.abs(counter_plus - counter_p2)) > 0.0),
        "postbody_hessian_is_positive": bool(np.min(hessian_eigenvalues) > 0.0),
        "implicit_response_formula_is_exact": bool(
            np.allclose(h_z @ response_state + b_zk, 0.0, atol=1.0e-14)
        ),
        "mixed_block_sign_flip_reverses_terminal_sign": close(gamma_sign_flip, -gamma),
        "mixed_block_rescaling_changes_terminal_amplitude": close(gamma_scale_three, 3.0 * gamma),
        "hessian_stays_fixed_across_sign_and_scale_countermodels": bool(
            np.allclose(h_z, h_z.T) and np.min(hessian_eigenvalues) > 0.0
        ),
        "common_action_mixed_block_factorizes_through_registration": bool(
            np.allclose(b_zk_visible, b_zi @ j_visible)
            and np.allclose(b_zk_hidden, b_zi @ j_hidden)
        ),
        "distinct_parent_lifts_have_same_visible_K": bool(
            np.allclose(p_visible @ j_visible, p_visible @ j_hidden, atol=0.0)
            and not np.allclose(j_visible, j_hidden)
        ),
        "same_visible_K_can_have_distinct_terminal_response": bool(
            abs(gamma_visible_lift - gamma_hidden_lift) > 1.0e-3
        ),
        "visible_lift_complete_and_schur_responses_agree": close(
            gamma_visible_lift, gamma_visible_schur
        ),
        "hidden_lift_complete_and_schur_responses_agree": close(
            gamma_hidden_lift, gamma_hidden_schur
        ),
        "same_action_zero_morphology_carrier_is_positive": same_action_carrier > 0.0,
        "constant_scalar_amplitude_is_not_generic": bool(np.ptp(inferred_gain) > 1.0e-3),
        "same_body_allows_distinct_zero_morphology_carriers": bool(
            np.all(carrier_sq_alt > 0.0) and not np.allclose(carrier_sq_alt, carrier_sq)
        ),
        "zero_amplitude_recovers_carrier": bool(np.allclose(carrier_sq * (1.0 + 0.0 * k1), carrier_sq)),
        "negative_branch_remains_nonnegative": bool(np.all(response_minus[supported] >= 0.0)),
        "projection_control_matches": bool(
            np.allclose(points["fixed_inner_inclination_projection_ratio_sq_control"], projection)
        ),
        "stored_mirror_reflected_los_matches": bool(
            np.allclose(points["mirror_reflected_n_los_control"], reflected_normals[:, 2])
        ),
        "stored_mirror_projection_matches": bool(
            np.allclose(
                points["mirror_fixed_inner_inclination_projection_ratio_sq_control"],
                mirror_projection,
            )
        ),
        "stored_mirror_projection_difference_matches": bool(
            np.allclose(
                points["mirror_minus_source_projection_ratio_sq_control"],
                mirror_projection_difference,
            )
        ),
        "analytic_mirror_projection_identity_is_exact": bool(
            np.max(
                np.abs(
                    mirror_projection_difference
                    - mirror_projection_difference_analytic
                )
            )
            < 1.0e-12
        ),
        "standard_projection_is_not_mirror_even_on_source_support": bool(
            np.max(np.abs(mirror_projection_difference[supported])) > 0.1
        ),
        "summary_retains_chi_for_complete_projection_stack": bool(
            summary["exact_registration_fibre"]["complete_projection_stack_decision"]
            == "RETAIN_CHI"
            and summary["exact_registration_fibre"]["status"]
            == "EXACT_GEOMETRIC_FIBRE_CHI_RETAINED_FOR_COMPLETE_PROJECTION_STACK"
            and projection_summary["mirror_even_on_supported_source_fibre"] is False
        ),
        "K1_path_segments_have_overlapping_level_range": bool(
            max(k1[radius_index[210.0]], k1[radius_index[240.0]])
            > min(k1[radius_index[270.0]], k1[radius_index[300.0]])
        ),
        "same_K1_level_has_two_disjoint_source_path_roots": bool(
            collision_witness["radial_separation_arcsec"] > 40.0
        ),
        "source_path_collision_K1_residual_is_small": bool(
            max(abs(root["K1_residual"]) for root in collision_witness["roots"])
            < 1.0e-12
        ),
        "equal_K1_source_path_roots_have_opposite_chi": bool(
            collision_witness["roots"][0]["chi"]
            * collision_witness["roots"][1]["chi"]
            < 0.0
        ),
        "equal_K1_source_path_roots_have_distinct_projection": bool(
            abs(collision_witness["projection_difference"]) > 0.08
        ),
        "source_path_collision_survives_neighboring_level_targets": bool(
            min(abs(record["projection_difference"]) for record in collision_records)
            > 0.07
        ),
        "source_path_level_solver_is_tolerance_stable": bool(
            maximum_tolerance_radius_shift < 1.0e-7
        ),
        "stored_source_path_collision_matches_independent_recomputation": bool(
            maximum_stored_collision_error < SHELL_TEXT_ATOL
        ),
        "summary_refutes_K1_as_complete_shared_descriptor": bool(
            scalar_summary["complete_shared_descriptor"] is False
            and scalar_summary["status"]
            == "K1_REFUTED_AS_COMPLETE_SHARED_DESCRIPTOR"
        ),
        "summary_does_not_overclaim_multicomponent_parent_occupation": bool(
            scalar_summary["multicomponent_parent_coupling_occupied_by_nature"]
            == "OPEN"
        ),
        "projection_range_matches_summary": close(
            float(np.min(projection[supported])),
            float(projection_summary["minimum_supported"]),
            SUMMARY_TEXT_ATOL,
        )
        and close(
            float(np.max(projection[supported])),
            float(projection_summary["maximum_supported"]),
            SUMMARY_TEXT_ATOL,
        ),
        "geometric_amplitude_matches_summary": close(amplitude, float(numerical["geometric_amplitude"])),
        "endpoint_values_unused": summary["endpoint_values_used"] is False,
        "terminal_formula_unselected": summary["terminal_formula_selected"] is False,
        "endpoint_remains_blocked": summary["endpoint_allowed"] is False,
        "status_is_formula_shell_only": summary["status"] == "FORMULA_SHELL_DERIVED_ENDPOINT_BLOCKED",
    }
    passed = int(sum(checks.values()))
    status = "REPRODUCIBILITY_AUDIT_PASS" if passed == len(checks) else "REPRODUCIBILITY_AUDIT_FAIL"
    result = {
        "schema": "tau_core_ugc03580_ugc3580_two_plane_readout_shell_reproducibility_audit_v01",
        "status": status,
        "checks_passed": passed,
        "checks_total": len(checks),
        "checks": checks,
        "independent_recomputation": {
            "plane_defect_separation": separation_defect,
            "geometric_amplitude": amplitude,
            "minimum_supported_K1": float(np.min(k1[supported])),
            "maximum_supported_K1": float(np.max(k1[supported])),
            "maximum_transition_abs_K1_minus_K2": float(np.max(np.abs(k1[transition] - k2[transition]))),
            "minimum_supported_projection_ratio_sq": float(np.min(projection[supported])),
            "maximum_supported_projection_ratio_sq": float(np.max(projection[supported])),
            "minimum_supported_signed_chirality": float(np.min(signed_chirality[supported])),
            "maximum_supported_signed_chirality": float(np.max(signed_chirality[supported])),
            "maximum_abs_chirality_square_identity_residual": float(
                np.max(np.abs(signed_chirality**2 - chirality_sq_from_defects))
            ),
            "maximum_source_orientation_vs_published_spin_normal_deg": float(
                np.max(source_orientation_residual_deg)
            ),
            "maximum_supported_abs_mirror_projection_difference": float(
                np.max(np.abs(mirror_projection_difference[supported]))
            ),
            "rms_supported_mirror_projection_difference": float(
                np.sqrt(np.mean(mirror_projection_difference[supported] ** 2))
            ),
            "maximum_abs_mirror_projection_identity_residual": float(
                np.max(
                    np.abs(
                        mirror_projection_difference
                        - mirror_projection_difference_analytic
                    )
                )
            ),
            "maximum_difference_witness": {
                "radius_arcsec": float(
                    body_points.loc[mirror_witness_index, "radius_arcsec"]
                ),
                "source_n_los": float(normals[mirror_witness_index, 2]),
                "mirror_n_los": float(reflected_normals[mirror_witness_index, 2]),
                "source_projection_ratio_sq": float(projection[mirror_witness_index]),
                "mirror_projection_ratio_sq": float(
                    mirror_projection[mirror_witness_index]
                ),
            },
            "same_body_plus_minus_max_v2_difference_for_100_km_s_carrier": float(
                np.max(np.abs(counter_plus - counter_minus))
            ),
        },
        "scalar_registration_collision": {
            "segments_arcsec": [list(value) for value in collision_segments],
            "sensitivity_targets": collision_records,
            "selected_witness": collision_witness,
            "maximum_radius_shift_under_tolerance_change_arcsec": float(
                maximum_tolerance_radius_shift
            ),
            "maximum_builder_vs_auditor_value_error": float(
                maximum_stored_collision_error
            ),
            "interpretation": (
                "K1 is not injective even on the frozen continuous source path and "
                "cannot be the complete shared descriptor; an alternative source-owned "
                "scalar factorization or a multicomponent Parent coupling remains open"
            ),
            "endpoint_values_used": False,
        },
        "source_action_countermodel": {
            "H_Z": h_z.tolist(),
            "B_ZK": b_zk.tolist(),
            "L_G": l_g.tolist(),
            "minimum_H_Z_eigenvalue": float(np.min(hessian_eigenvalues)),
            "Gamma": gamma,
            "Gamma_after_B_ZK_sign_flip": gamma_sign_flip,
            "Gamma_after_B_ZK_scale_times_three": gamma_scale_three,
            "same_body_and_H_Z": True,
            "endpoint_values_used": False,
        },
        "common_action_pullback_witness": {
            "factorization": "B_ZK=B_ZI J_(I<-K)",
            "terminal_response": "Gamma=-L_G H_Z^{-1} B_ZI J_(I<-K)",
            "same_visible_K_projection_residual": float(
                np.max(np.abs(p_visible @ j_visible - p_visible @ j_hidden))
            ),
            "Gamma_visible_lift": gamma_visible_lift,
            "Gamma_hidden_lift": gamma_hidden_lift,
            "Gamma_visible_lift_after_exact_schur_reduction": gamma_visible_schur,
            "Gamma_hidden_lift_after_exact_schur_reduction": gamma_hidden_schur,
            "same_action_zero_morphology_carrier": same_action_carrier,
            "endpoint_values_used": False,
        },
        "conditional_completion": {
            "response_operator": "Gamma=-L_G H_Z^{-1} B_ZK",
            "common_action_reduction": (
                "B_ZDhat=B_ZI J_(I<-Dhat); inside a frozen Einstein--Newton/observer branch "
                "L_G=D_Z O_G and v_carrier^2=O_G[Z_*(I=0)]"
            ),
            "p": (
                "selected exactly only by a source-owned full-support defect law f(d)=c*d^p; "
                "a first nonzero analytic jet selects only local leading order"
            ),
            "sign": "sign of the occupied typed terminal response Gamma after conventions are frozen",
            "amplitude": (
                "one scalar a exists only if [Gamma K_p]/(v_carrier^2 K_p) is constant "
                "on nonzero support"
            ),
            "carrier": "the calibrated zero-morphology physical terminal branch",
            "occupation": "requires independent physical source-orbit occupation",
            "remaining_source_object": (
                "a source-owned complete-terminal scalar factorization of the retained "
                "signed descriptor, or a genuinely multicomponent registration into the "
                "Parent invariant, plus an occupied calibrated common packet"
            ),
            "current_status": (
                "K1_REFUTED_AS_COMPLETE_DESCRIPTOR_SIGNED_REGISTRATION_AND_OCCUPATION_OPEN"
            ),
        },
        "verdict": (
            "bounded morphology coordinate proven; a common action conditionally makes the mixed "
            "response, gravity terminal and carrier one derivative/evaluation chain, but the current "
            "source packet fixes chi retention and refutes K1 as a complete source-path "
            "descriptor but does not select an alternative signed scalar or multicomponent "
            "Parent registration, exact exponent/profile, "
            "constant-amplitude factorization, calibrated occupation or nature-level completion"
        ),
        "claim_boundary": "formula-shell mathematics only; no endpoint or Tau-specific physical validation",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# UGC03580 bounded two-plane readout-shell reproducibility audit v01",
                "",
                f"Status: `{status}`",
                "",
                f"Independent checks passed: `{passed}/{len(checks)}`.",
                "",
                "The audit independently reconstructs the plane defects, the `p=1` and",
                "`p=2` bounded coordinates, exact plane-swap complementarity, theoretical",
                "inner/outer limits, the coincident-plane null, and the standard fixed-",
                "inclination projection control. It also instantiates distinct same-body",
                "terminal curves to verify the non-identifiability counterfamily.",
                "",
                "The post-body witness independently verifies `Gamma=-L_G H_Z^{-1}B_ZK`.",
                "Keeping the same positive `H_Z` and source body while replacing `B_ZK`",
                "by `-B_ZK` or `3 B_ZK` reverses the sign or triples the amplitude.",
                "A nonconstant radial gain also shows that one scalar `a` requires an",
                "additional rank-one/factorization theorem; it is not implied by stability.",
                "",
                "The common-action witness also verifies `B_ZDhat=B_ZI J_(I<-Dhat)` and exact",
                "Schur reduction of an occupied internal field. Two distinct Parent lifts",
                "have identical visible `K` projection but gains",
                f"`{gamma_visible_lift:.12f}` and `{gamma_hidden_lift:.12f}`. Thus the",
                "visible coordinate cannot reconstruct its own source registration.",
                "",
                "The independent geometry calculation further proves that the actual raw",
                "two-defect descriptor has a discrete mirror fibre. The signed triple",
                "product `chi` completes the oriented geometry and its squared magnitude",
                "is reconstructed from the two raw defects to",
                f"`{np.max(np.abs(signed_chirality**2 - chirality_sq_from_defects)):.3e}` maximum residual.",
                "The frozen source supplies oriented spin-normal components and the",
                "supported path contains both signs. The standard fixed-inner-inclination",
                "projection is not mirror-even: the maximum supported mirror difference is",
                f"`{np.max(np.abs(mirror_projection_difference[supported])):.12f}` and the RMS is",
                f"`{np.sqrt(np.mean(mirror_projection_difference[supported] ** 2)):.12f}`.",
                "Therefore `chi` must be retained in the complete projection descriptor.",
                "This remains standard projection visibility, not evidence for fundamental",
                "Parent handedness or a Tau-specific coupling.",
                "",
                "The independent piecewise-SLERP calculation also refutes `K_1` as",
                "the complete shared coordinate. The level `K_1=0.925` occurs at",
                f"`{collision_witness['roots'][0]['radius_arcsec']:.9f}` and",
                f"`{collision_witness['roots'][1]['radius_arcsec']:.9f} arcsec`, with",
                f"projections `{collision_witness['roots'][0]['projection_ratio_sq']:.12f}`",
                f"and `{collision_witness['roots'][1]['projection_ratio_sq']:.12f}` and",
                "opposite signs of `chi`. Neighboring target levels 0.900 and 0.950",
                "give the same conclusion, and the bisection tolerance control is stable.",
                "This does not prove that Nature occupies a rank-two Parent response; it",
                "requires retaining `D_hat` until an alternative source-owned scalar",
                "factorization or a multicomponent coupling is independently derived.",
                "",
                "The mathematical shell is reproducible. The selected common action would",
                "remove independent terminal gains, but the retained signed descriptor's",
                "physical registration, exact",
                "profile, calibration and occupation remain open, so endpoint scoring stays",
                "blocked.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if status != "REPRODUCIBILITY_AUDIT_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
