#!/usr/bin/env python3
"""Endpoint-blind audit of the G4D coframe mediator compiler for SDP.81."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/sdp81_g4d_coframe_parent_gas_mediator_compiler_v01.json"
REPORT = ROOT / "reports/sdp81_g4d_coframe_parent_gas_mediator_compiler_v01.md"
TOL = 1.0e-10
SYM = tuple((i, j) for i in range(4) for j in range(i, 4))


def rank(value: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(value, tol=TOL))


def metric_vector(value: np.ndarray) -> np.ndarray:
    return np.asarray([value[i, j] for i, j in SYM])


def sym_exp(value: np.ndarray) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(value)
    return eigenvectors @ np.diag(np.exp(eigenvalues)) @ eigenvectors.T


def coframe(generator: np.ndarray) -> np.ndarray:
    strain = np.asarray(
        [
            [generator[4], generator[5], generator[6]],
            [generator[5], generator[7], generator[8]],
            [generator[6], generator[8], generator[9]],
        ]
    )
    spatial = sym_exp(strain)
    result = np.zeros((4, 4))
    result[0, 0] = np.exp(generator[0])
    result[1:, 0] = spatial @ generator[1:4]
    result[1:, 1:] = spatial
    return result


def main() -> None:
    rng = np.random.default_rng(81104)
    eta = np.diag([-1.0, 1.0, 1.0, 1.0])

    full_columns = []
    for i in range(4):
        for j in range(4):
            matrix = np.zeros((4, 4))
            matrix[i, j] = 1.0
            full_columns.append(metric_vector(matrix.T @ eta + eta @ matrix))
    j_full = np.column_stack(full_columns)

    active = []
    matrix = np.zeros((4, 4))
    matrix[0, 0] = 1.0
    active.append(matrix.reshape(-1))
    for i in range(1, 4):
        matrix = np.zeros((4, 4))
        matrix[i, 0] = 1.0
        active.append(matrix.reshape(-1))
    for i in range(1, 4):
        for j in range(i, 4):
            matrix = np.zeros((4, 4))
            matrix[i, j] = matrix[j, i] = 1.0
            active.append(matrix.reshape(-1))
    j_metric = j_full @ np.column_stack(active)

    lorentz = []
    for i in range(1, 4):
        matrix = np.zeros((4, 4))
        matrix[0, i] = matrix[i, 0] = 1.0
        lorentz.append(matrix.reshape(-1))
    for i, j in ((1, 2), (1, 3), (2, 3)):
        matrix = np.zeros((4, 4))
        matrix[i, j], matrix[j, i] = 1.0, -1.0
        lorentz.append(matrix.reshape(-1))
    lorentz = np.column_stack(lorentz)

    d_c = rng.normal(size=(14, 10))
    d_a = rng.normal(size=(14, 5))
    d_m = rng.normal(size=(8, 10))
    # Ordered conditional source row for the formerly free registration.
    r_a = rng.normal(size=(12, 5))
    r_z = rng.normal(size=(12, 5))
    d_access = rng.normal(size=(4, 5))
    w_za = np.diag(np.linspace(0.7, 1.8, 12))
    k_a = r_a.T @ w_za @ r_a + d_access.T @ d_access
    b_az = r_a.T @ w_za @ r_z
    i_za = -np.linalg.solve(k_a, b_az)
    l_c = d_c.T @ d_c + d_m.T @ d_m
    d_z_c = -np.linalg.solve(l_c, d_c.T @ d_a @ i_za)
    d_z_h = j_metric @ d_z_c

    gas_seed = rng.normal(size=(5, 5))
    h_gas = gas_seed.T @ gas_seed + np.eye(5)
    b_gas_h = rng.normal(size=(5, 10))
    p = -np.linalg.solve(h_gas, b_gas_h @ d_z_h)

    i_alt = i_za @ np.diag([1.3, 0.8, 1.1, 0.9, 1.2])
    h_alt = j_metric @ (-np.linalg.solve(l_c, d_c.T @ d_a @ i_alt))
    b_alt = b_gas_h.copy()
    b_alt[0, 0] += 0.4
    p_alt = -np.linalg.solve(h_gas, b_alt @ d_z_h)

    # Conditional finite difference and an ordered-versus-symmetric control.
    r_0 = rng.normal(size=12)
    direction = rng.normal(size=5)
    step = 1.0e-6
    a_plus = -np.linalg.solve(k_a, r_a.T @ w_za @ (r_0 + r_z @ (step * direction)))
    a_minus = -np.linalg.solve(k_a, r_a.T @ w_za @ (r_0 - r_z @ (step * direction)))
    finite_access = (a_plus - a_minus) / (2.0 * step)
    schur = b_az.T @ np.linalg.solve(k_a, b_az)
    h_z = schur + 2.0 * np.eye(5)
    load_z = rng.normal(size=5)
    load_a = rng.normal(size=5)
    ordered = np.block([[h_z, np.zeros((5, 5))], [b_az, k_a]])
    symmetric = np.block([[h_z, b_az.T], [b_az, k_a]])
    z_frozen = np.linalg.solve(h_z, load_z)
    z_ordered = np.linalg.solve(ordered, np.concatenate([load_z, load_a]))[:5]
    z_symmetric = np.linalg.solve(symmetric, np.concatenate([load_z, load_a]))[:5]

    # The current concrete AORS access-star row has only four independent
    # root-minus-reference differences and annihilates the raw common mode.
    d_a_star = np.column_stack((-np.ones(4), np.eye(4)))
    d_c_star = rng.normal(size=(4, 10))
    t_star = d_c_star.T @ d_a_star
    d_z_h_star = j_metric @ (-np.linalg.solve(l_c, t_star))
    u_svd, _, vh_svd = np.linalg.svd(t_star, full_matrices=True)
    missing_terminal_row = vh_svd[-1]
    missing_coframe_leg = u_svd[:, -1]
    t_star_plus_one = t_star + np.outer(missing_coframe_leg, missing_terminal_row)
    t_star_redundant = t_star + np.outer(t_star[:, 0], missing_terminal_row)

    # Natural completion candidate: the normalized AORS common null covector
    # paired with the gauge-invariant coframe log-volume differential.
    q_access_common = np.ones(5) / np.sqrt(5.0)
    q_volume = np.asarray([1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0])
    q_volume_full = np.zeros(16)
    q_volume_full[[0, 5, 10, 15]] = 1.0
    q_volume_from_metric = np.asarray(
        [-0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.5, 0.0, 0.5]
    )
    volume_direction = rng.normal(size=10)
    logdet_plus = np.linalg.slogdet(coframe(step * volume_direction))[1]
    logdet_minus = np.linalg.slogdet(coframe(-step * volume_direction))[1]
    finite_volume = (logdet_plus - logdet_minus) / (2.0 * step)
    volume_shared_jet = np.outer(q_volume, q_access_common)
    t_star_plus_volume = t_star + volume_shared_jet
    coframe_image = u_svd[:, : rank(t_star)]
    q_volume_redundant = coframe_image @ (coframe_image.T @ q_volume)
    t_star_volume_coframe_redundant = t_star + np.outer(
        q_volume_redundant, q_access_common
    )
    t_star_volume_access_redundant = t_star + np.outer(q_volume, vh_svd[0])
    k_volume, k_access = 1.7, 0.9
    gamma_bound = np.sqrt(k_volume * k_access)
    h_scalar_zero = np.asarray([[k_volume, 0.0], [0.0, k_access]])
    h_scalar_plus = np.asarray(
        [[k_volume, 0.4 * gamma_bound], [0.4 * gamma_bound, k_access]]
    )
    h_scalar_minus = np.asarray(
        [[k_volume, -0.4 * gamma_bound], [-0.4 * gamma_bound, k_access]]
    )
    h_scalar_saturated = np.asarray(
        [[k_volume, gamma_bound], [gamma_bound, k_access]]
    )
    h_scalar_overcoupled = np.asarray(
        [[k_volume, 1.1 * gamma_bound], [1.1 * gamma_bound, k_access]]
    )
    k_volume_response, gamma_response = 0.7, -0.35
    l_volume = l_c + k_volume_response * np.outer(q_volume, q_volume)
    response_star = -np.linalg.solve(l_c, t_star)
    response_volume = -np.linalg.solve(
        l_volume, t_star + gamma_response * volume_shared_jet
    )
    l0_inv_u = np.linalg.solve(l_c, q_volume)
    scalar_s = float(q_volume @ l0_inv_u)
    response_delta_formula = np.outer(
        l0_inv_u,
        (
            k_volume_response * (q_volume @ np.linalg.solve(l_c, t_star))
            - gamma_response * q_access_common
        )
        / (1.0 + k_volume_response * scalar_s),
    )
    response_delta = response_volume - response_star
    metric_response_delta = j_metric @ response_delta
    gas_response_delta = -np.linalg.solve(h_gas, b_gas_h @ metric_response_delta)
    metric_volume_leg = j_metric @ l0_inv_u
    metric_projector_null = np.eye(10) - np.outer(
        metric_volume_leg, metric_volume_leg
    ) / float(metric_volume_leg @ metric_volume_leg)
    b_gas_null = metric_projector_null[:5]
    gas_null_delta = -np.linalg.solve(h_gas, b_gas_null @ metric_response_delta)
    desired_cancel_row = (gamma_response / k_volume_response) * q_access_common
    t_cancel = np.outer(l_c @ q_volume / float(q_volume @ q_volume), desired_cancel_row)
    cancel_base = -np.linalg.solve(l_c, t_cancel)
    cancel_full = -np.linalg.solve(
        l_volume, t_cancel + gamma_response * volume_shared_jet
    )
    r_volume = rng.normal(size=6)
    r_access_common = rng.normal(size=6)
    lambda_action = 2.3
    k_volume_relation = lambda_action * float(r_volume @ r_volume)
    k_access_relation = lambda_action * float(r_access_common @ r_access_common)
    gamma_relation = lambda_action * float(r_volume @ r_access_common)
    rho_relation = gamma_relation / np.sqrt(k_volume_relation * k_access_relation)
    lambda_action_alt = 4.2 * lambda_action
    rho_relation_alt = (
        lambda_action_alt * float(r_volume @ r_access_common)
        / np.sqrt(
            lambda_action_alt
            * float(r_volume @ r_volume)
            * lambda_action_alt
            * float(r_access_common @ r_access_common)
        )
    )
    r_access_orthogonal = r_access_common - r_volume * float(
        r_volume @ r_access_common
    ) / float(r_volume @ r_volume)
    gamma_orthogonal = lambda_action * float(r_volume @ r_access_orthogonal)
    gamma_antiparallel = -lambda_action * float(r_volume @ r_volume)
    rho_antiparallel = gamma_antiparallel / k_volume_relation
    compatibility_volume = rng.normal(size=4)
    k_volume_full = k_volume_relation + lambda_action * float(
        compatibility_volume @ compatibility_volume
    )
    rho_with_compatibility = gamma_relation / np.sqrt(
        k_volume_full * k_access_relation
    )

    # Standard matter-volume and line-transfer terminal checks.  A conformal
    # coframe variation couples to the stress-energy trace, but Paper 8's
    # centered-log terminal removes a uniform spectral gain.  If a fixed-source
    # line has I_j=S_j(1-exp(-tau_j)) and tau_j -> exp(zeta)tau_j, its response
    # is g(tau_j)=tau_j/expm1(tau_j), which survives only through opacity shape.
    energy_density = 5.0
    cold_trace = -energy_density + 3.0 * (0.02 * energy_density)
    radiation_trace = -energy_density + 3.0 * energy_density / 3.0
    conformal_parameter = 0.013
    conformal_metric_variation = 2.0 * conformal_parameter * eta
    conformal_q_volume = 0.5 * np.trace(eta @ conformal_metric_variation)
    channel_count = 6
    centered_projector = np.eye(channel_count) - np.ones(
        (channel_count, channel_count)
    ) / channel_count
    optical_depth_equal = np.full(channel_count, 0.7)
    optical_depth_shape = np.asarray([0.08, 0.2, 0.45, 0.9, 1.7, 3.2])
    opacity_response_equal = optical_depth_equal / np.expm1(optical_depth_equal)
    opacity_response_shape = optical_depth_shape / np.expm1(optical_depth_shape)
    opacity_grid = np.logspace(-5, 2, 2000)
    opacity_response_grid = opacity_grid / np.expm1(opacity_grid)
    zeta_step = 1.0e-6

    def log_line_intensity(zeta: float, tau: np.ndarray) -> np.ndarray:
        return np.log(-np.expm1(-np.exp(zeta) * tau))

    opacity_response_fd = (
        log_line_intensity(zeta_step, optical_depth_shape)
        - log_line_intensity(-zeta_step, optical_depth_shape)
    ) / (2.0 * zeta_step)

    checks = {
        "full_coframe_metric_map_has_rank_ten": rank(j_full) == 10,
        "full_coframe_metric_map_has_six_null_directions": 16 - rank(j_full) == 6,
        "explicit_lorentz_generators_are_null": bool(
            rank(lorentz) == 6 and np.linalg.norm(j_full @ lorentz) < TOL
        ),
        "metric_active_chart_is_injective": rank(j_metric) == 10,
        "ordered_coframe_hessian_is_positive": bool(np.linalg.eigvalsh(l_c).min() > 0.0),
        "paper8_registration_witness_has_rank_five": rank(i_za) == 5,
        "coframe_and_metric_witnesses_transmit_five_modes": rank(d_z_c) == rank(d_z_h) == 5,
        "composed_parent_gas_witness_has_rank_five": rank(p) == 5,
        "same_g4d_blocks_different_registration_changes_metric_bridge": bool(
            np.linalg.norm(h_alt - d_z_h) > 1.0e-6
        ),
        "same_metric_bridge_different_gas_response_changes_final_bridge": bool(
            np.linalg.norm(p_alt - p) > 1.0e-6
        ),
        "zero_gas_metric_response_is_exact_null_control": bool(
            np.allclose(-np.linalg.solve(h_gas, np.zeros((5, 10)) @ d_z_h), 0.0)
        ),
        "ordered_source_row_derives_registration": bool(
            np.allclose(finite_access, i_za @ direction, atol=2.0e-9)
        ),
        "ordered_access_preserves_Z_while_symmetric_solve_backreacts": bool(
            np.allclose(z_ordered, z_frozen, atol=TOL)
            and np.linalg.norm(z_symmetric - z_frozen) > 1.0e-6
            and np.linalg.norm(schur) > 1.0e-6
        ),
        "current_aors_access_star_has_rank_four": rank(d_a_star) == 4,
        "current_aors_access_star_annihilates_common_mode": bool(
            np.allclose(d_a_star @ np.ones(5), 0.0, atol=TOL)
        ),
        "invertible_registration_cannot_raise_aors_transmission_above_four": bool(
            rank(d_z_h_star) <= 4
        ),
        "coframe_capacity_does_not_remove_access_bottleneck": bool(
            rank(j_metric) == 10 and rank(d_z_h_star) == 4
        ),
        "one_independent_scalar_shared_row_closes_exact_rank_deficit": bool(
            rank(t_star) == 4 and rank(t_star_plus_one) == 5
        ),
        "redundant_scalar_shared_row_does_not_close_rank_deficit": bool(
            rank(t_star_redundant) == 4
        ),
        "rank_one_enrichment_adds_at_most_one_mode": bool(
            rank(t_star_plus_one) - rank(t_star) <= 1
        ),
        "coframe_log_volume_differential_matches_finite_difference": bool(
            np.isclose(finite_volume, q_volume @ volume_direction, atol=2.0e-9)
        ),
        "coframe_log_volume_is_half_metric_trace": bool(
            np.allclose(q_volume_from_metric @ j_metric, q_volume, atol=TOL)
        ),
        "coframe_log_volume_annihilates_lorentz_gauge": bool(
            np.allclose(q_volume_full @ lorentz, 0.0, atol=TOL)
        ),
        "natural_common_volume_mixed_jet_has_rank_one": rank(volume_shared_jet) == 1,
        "natural_common_volume_lane_closes_witness_rank_deficit": bool(
            rank(t_star) == 4 and rank(t_star_plus_volume) == 5
        ),
        "zero_common_volume_coupling_leaves_rank_four": rank(t_star) == 4,
        "coframe_redundant_volume_leg_leaves_rank_four": bool(
            rank(t_star_volume_coframe_redundant) == 4
        ),
        "access_redundant_volume_leg_leaves_rank_four": bool(
            rank(t_star_volume_access_redundant) == 4
        ),
        "positive_scalar_sector_allows_zero_mixed_coupling": bool(
            np.linalg.eigvalsh(h_scalar_zero).min() > 0.0
        ),
        "positive_scalar_sector_allows_both_mixed_coupling_signs": bool(
            np.linalg.eigvalsh(h_scalar_plus).min() > 0.0
            and np.linalg.eigvalsh(h_scalar_minus).min() > 0.0
        ),
        "positive_scalar_sector_imposes_cauchy_bound": bool(
            np.linalg.eigvalsh(h_scalar_overcoupled).min() < 0.0
        ),
        "perfect_square_saturates_scalar_cauchy_bound": bool(
            np.isclose(np.linalg.det(h_scalar_saturated), 0.0, atol=TOL)
        ),
        "saturated_scalar_sector_is_rank_one": rank(h_scalar_saturated) == 1,
        "diagonal_susceptibilities_do_not_select_mixed_orientation": bool(
            np.allclose(np.diag(h_scalar_plus), np.diag(h_scalar_minus))
            and not np.allclose(h_scalar_plus, h_scalar_minus)
        ),
        "common_volume_ordered_response_matches_sherman_morrison_formula": bool(
            np.allclose(response_delta, response_delta_formula, atol=TOL)
        ),
        "common_volume_increment_has_rank_one": rank(response_delta) == 1,
        "metricized_common_volume_increment_has_rank_one": rank(metric_response_delta) == 1,
        "generic_gas_terminal_receives_rank_one_increment": rank(gas_response_delta) == 1,
        "terminal_annihilation_can_hide_nonzero_common_volume_increment": bool(
            np.linalg.norm(response_delta) > 0.0
            and np.allclose(gas_null_delta, 0.0, atol=TOL)
        ),
        "self_and_mixed_row_contributions_can_cancel_exactly": bool(
            gamma_response != 0.0 and np.allclose(cancel_full, cancel_base, atol=TOL)
        ),
        "common_relation_row_generates_positive_scalar_gram_block": bool(
            np.linalg.eigvalsh(
                np.asarray(
                    [
                        [k_volume_relation, gamma_relation],
                        [gamma_relation, k_access_relation],
                    ]
                )
            ).min()
            >= -TOL
        ),
        "relation_correlation_obeys_cauchy_bound": bool(
            abs(rho_relation) <= 1.0 + TOL
        ),
        "relation_correlation_is_common_action_scale_invariant": bool(
            np.isclose(rho_relation, rho_relation_alt, atol=TOL)
        ),
        "relation_orthogonality_is_exact_zero_activation_control": bool(
            np.isclose(gamma_orthogonal, 0.0, atol=TOL)
        ),
        "relation_orientation_reversal_flips_and_saturates_coupling": bool(
            gamma_antiparallel < 0.0 and np.isclose(rho_antiparallel, -1.0, atol=TOL)
        ),
        "extra_coframe_compatibility_weakens_normalized_cross_correlation": bool(
            abs(rho_with_compatibility) < abs(rho_relation)
        ),
        "cold_massive_matter_has_nonzero_stress_trace": bool(
            not np.isclose(cold_trace, 0.0, atol=TOL)
        ),
        "classical_radiation_is_trace_free_control": bool(
            np.isclose(radiation_trace, 0.0, atol=TOL)
        ),
        "coframe_volume_is_four_times_conformal_parameter": bool(
            np.isclose(conformal_q_volume, 4.0 * conformal_parameter, atol=TOL)
        ),
        "centered_terminal_annihilates_uniform_gain": bool(
            np.allclose(centered_projector @ np.ones(channel_count), 0.0, atol=TOL)
        ),
        "opacity_response_matches_finite_difference": bool(
            np.allclose(opacity_response_fd, opacity_response_shape, atol=2.0e-9)
        ),
        "positive_opacity_response_is_strictly_decreasing": bool(
            np.all(opacity_response_grid > 0.0)
            and np.all(np.diff(opacity_response_grid) < 0.0)
        ),
        "equal_opacity_is_centered_terminal_null": bool(
            np.allclose(centered_projector @ opacity_response_equal, 0.0, atol=TOL)
        ),
        "nonuniform_opacity_survives_centered_terminal": bool(
            np.linalg.norm(centered_projector @ opacity_response_shape) > 1.0e-3
        ),
        "no_co109_header_or_pixel_read": True,
        "no_physical_registration_self_asserted": True,
    }
    status = (
        "OPACITY_SHAPE_SURVIVAL_DERIVED_SOURCE_PROFILE_OPEN"
        if all(checks.values())
        else "SDP81_G4D_COFRAME_MEDIATOR_COMPILER_AUDIT_FAILED"
    )
    result = {
        "schema": "tau-core.paper8.sdp81-g4d-coframe-parent-gas-mediator-compiler.v01",
        "status": status,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "coframe_metric_rank": rank(j_metric),
        "coframe_metric_gauge_nullity": 16 - rank(j_full),
        "D_Z_metric_rank": rank(d_z_h),
        "parent_gas_bridge_rank": rank(p),
        "B_AZ_rank": rank(b_az),
        "I_ZA_rank": rank(i_za),
        "schur_backreaction_norm": float(np.linalg.norm(schur)),
        "current_AORS_D_A_rank": rank(d_a_star),
        "current_AORS_D_Z_metric_rank": rank(d_z_h_star),
        "minimal_independent_scalar_enrichment_rank": rank(t_star_plus_one),
        "natural_common_volume_enrichment_rank": rank(t_star_plus_volume),
        "common_volume_response_increment_rank": rank(response_delta),
        "common_volume_metric_increment_rank": rank(metric_response_delta),
        "common_volume_gas_increment_rank": rank(gas_response_delta),
        "source_relation_correlation": float(rho_relation),
        "physical_g4d_packet_occupied": False,
        "physical_I_ZA_owned": False,
        "physical_gas_metric_response_owned": False,
        "standard_cold_matter_volume_coupling_nonzero": True,
        "conditional_opacity_shape_terminal_survival_derived": True,
        "physical_channel_opacity_profile_owned": False,
        "endpoint_authorized": False,
        "claim_boundary": (
            "The AORS common null and coframe log-volume select a natural rank-one "
            "completion. In a one-row source packet its coefficient is the weighted "
            "Gram pairing of the volume and common-access relation images. Standard "
            "massive matter couples to volume through its stress trace. A centered "
            "spectral terminal sees the induced opacity response only when its "
            "channel profile is nonuniform and independently source-owned."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 G4D coframe parent--gas mediator compiler audit v01\n\n"
        f"Status: `{status}`. Checks: `{result['checks_passed']}/"
        f"{result['checks_total']}`. No CO(10-9) header or pixel was read.\n\n"
        "The access registration is $I_{ZA}=-K_A^{-1}R_A^*W_{ZA}R_Z$. "
        "The ordered compiler is $D_Zc_*=-L_C^{-1}D_C^*W_RD_AI_{ZA}$, "
        "$D_Zh=J_{\\rm met}D_Zc_*$, and "
        "$P=-H_\\xi^{-1}B_{\\xi h}D_Zh$. The coframe/metric chart has ten "
        "physical directions and the full coframe map has six Lorentz-gauge "
        "nulls. A rank-five witness exists.\n\n"
        "The finite difference verifies the conditional source-row derivative. "
        "The lower-triangular solve preserves frozen $Z$, whereas a symmetric "
        "solve generates a nonzero Schur backreaction. The common relation row "
        "and $B_{\\xi h}$ are not physically supplied by the current SDP.81 "
        "packet. The current AORS access star has rank four. One nonredundant "
        "scalar shared access--coframe row is algebraically minimal and sufficient "
        "to restore rank five; a redundant row fails. The natural candidate pairs "
        "the normalized AORS common mode with $D\\log|\\det D_O|$, equivalently half "
        "the mixed metric trace. A positive scalar Hessian only implies "
        "$|\\gamma_{\\rm cm}|\\leq\\sqrt{k_Vk_A}$ and admits zero and both signs. "
        "The finite witness closes, but its coefficient, physical transversality "
        "and Nature occupation remain open, so endpoint "
        "authorization remains false. The exact ordered response includes the "
        "correlated coframe self-Hessian and is rank at most one through a generic "
        "linear gas terminal; exact cancellation or a terminal null can hide it.\n\n"
        "In one common source row, $\\gamma_{\\rm cm}=\\Lambda_A"
        "\\langle D_Ce_V,D_Ae_A\\rangle_W$. Its normalized value is the weighted "
        "relation-space cosine, so activation is exactly nonzero nonorthogonality "
        "and the common action scale cancels. Those relation images remain "
        "physically unoccupied in the current packet.\n\n"
        "For $T_{\\mu\\nu}=-(2/\\sqrt{-g})\\,\\delta S_m/\\delta g^{\\mu\\nu}$, "
        "a conformal coframe variation gives "
        "$\\delta S_m=\\int\\sqrt{-g}\\,\\varphi T^\\mu{}_{\\mu}$ and "
        "$q_V=4\\varphi$. Cold massive matter is nonzero while classical "
        "radiation is a trace-free control. A uniform gain is nevertheless null "
        "after spectral centering. For fixed source function and "
        "$\\tau_j\\mapsto e^\\zeta\\tau_j$, the surviving response is "
        "$\\tau_j/(e^{\\tau_j}-1)$; unequal opacities survive, equal opacity does "
        "not. The channel-wise physical opacity profile is still unsourced.\n",
        encoding="utf-8",
    )
    print(status)


if __name__ == "__main__":
    main()
