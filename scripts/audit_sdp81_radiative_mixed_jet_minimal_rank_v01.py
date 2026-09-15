#!/usr/bin/env python3
"""Endpoint-blind minimal-rank audit for the SDP.81 radiative terminal."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/sdp81_radiative_mixed_jet_minimal_rank_v01.json"
REPORT = ROOT / "reports/sdp81_radiative_mixed_jet_minimal_rank_v01.md"


def helmert(count: int) -> np.ndarray:
    basis = np.zeros((count, count - 1))
    for column in range(count - 1):
        scale = np.sqrt((column + 1) * (column + 2))
        basis[: column + 1, column] = 1.0 / scale
        basis[column + 1, column] = -(column + 1) / scale
    return basis


def slab(u: np.ndarray, xi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ln_eta, ln_contrast, ln_tau, center, ln_width = xi
    amplitude = np.exp(ln_eta + ln_contrast)
    tau0, width = np.exp(ln_tau), np.exp(ln_width)
    delta = u - center
    profile = np.exp(-0.5 * (delta / width) ** 2)
    depth = tau0 * profile
    flux = amplitude * (1.0 - np.exp(-depth))
    response = amplitude * np.exp(-depth) * depth
    derivative = np.column_stack(
        [
            flux,
            flux,
            response,
            response * delta / width**2,
            response * delta**2 / width**2,
        ]
    )
    return flux, derivative


def mixture(u: np.ndarray, xi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    rho, center1, center2, ln_width1, ln_width2 = xi
    width1, width2 = np.exp(ln_width1), np.exp(ln_width2)
    delta1, delta2 = u - center1, u - center2
    part1 = np.exp(-0.5 * (delta1 / width1) ** 2)
    part2 = np.exp(rho) * np.exp(-0.5 * (delta2 / width2) ** 2)
    flux = part1 + part2
    derivative = np.column_stack(
        [
            part2,
            part1 * delta1 / width1**2,
            part2 * delta2 / width2**2,
            part1 * delta1**2 / width1**2,
            part2 * delta2**2 / width2**2,
        ]
    )
    return flux, derivative


def centered_jacobian(flux: np.ndarray, derivative: np.ndarray, basis: np.ndarray) -> np.ndarray:
    return basis.T @ np.diag(1.0 / flux) @ derivative


def finite_difference(function, point: np.ndarray) -> np.ndarray:
    step = 1.0e-6
    columns = []
    for index in range(len(point)):
        plus, minus = point.copy(), point.copy()
        plus[index] += step
        minus[index] -= step
        columns.append((function(plus) - function(minus)) / (2.0 * step))
    return np.column_stack(columns)


def main() -> None:
    u = np.linspace(-2.5, 2.5, 6)
    basis = helmert(6)
    slab_point = np.asarray([0.1, -0.2, np.log(2.0), 0.2, np.log(0.9)])
    slab_flux, slab_derivative = slab(u, slab_point)
    slab_j = centered_jacobian(slab_flux, slab_derivative, basis)
    slab_fd = finite_difference(lambda x: basis.T @ np.log(slab(u, x)[0]), slab_point)

    thin_point = slab_point.copy()
    thin_point[2] = np.log(1.0e-7)
    thin_flux, thin_derivative = slab(u, thin_point)
    thin_j = centered_jacobian(thin_flux, thin_derivative, basis)

    mix_point = np.asarray([0.2, -0.9, 0.8, np.log(0.65), np.log(0.9)])
    mix_flux, mix_derivative = mixture(u, mix_point)
    mix_j = centered_jacobian(mix_flux, mix_derivative, basis)
    mix_fd = finite_difference(lambda x: basis.T @ np.log(mixture(u, x)[0]), mix_point)
    mix_singular = np.linalg.svd(mix_j, compute_uv=False)

    degenerate = np.asarray([0.2, 0.1, 0.1, np.log(0.8), np.log(0.8)])
    deg_flux, deg_derivative = mixture(u, degenerate)
    deg_j = centered_jacobian(deg_flux, deg_derivative, basis)

    bridge = np.asarray(
        [
            [1.0, 0.1, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.2, 0.0, 0.0],
            [0.0, 0.0, 1.0, -0.1, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.15],
            [0.05, 0.0, 0.0, 0.0, 1.0],
        ]
    )
    chain = mix_j @ bridge
    chain_fd = finite_difference(
        lambda z: basis.T @ np.log(mixture(u, mix_point + bridge @ z)[0]),
        np.zeros(5),
    )

    # Two-transition opacity identifiability control.  The published intrinsic
    # brightness-luminosity ratio r_87/54=0.30 supplies two positive line
    # intensities only.  If the two source functions are not independently
    # fixed, every positive pair of optical depths reproduces the same data via
    # S_j=I_j/(1-exp(-tau_j)), while the volume/column response
    # d log I_j / d zeta = tau_j/expm1(tau_j) changes.
    published_line_intensity = np.asarray([1.0, 0.30])
    tau_family_a = np.asarray([0.10, 0.20])
    tau_family_b = np.asarray([1.00, 3.00])

    def matching_source_function(tau: np.ndarray) -> np.ndarray:
        return published_line_intensity / (-np.expm1(-tau))

    source_function_a = matching_source_function(tau_family_a)
    source_function_b = matching_source_function(tau_family_b)
    reproduced_a = source_function_a * (-np.expm1(-tau_family_a))
    reproduced_b = source_function_b * (-np.expm1(-tau_family_b))
    opacity_response_a = tau_family_a / np.expm1(tau_family_a)
    opacity_response_b = tau_family_b / np.expm1(tau_family_b)
    two_line_center = np.eye(2) - np.ones((2, 2)) / 2.0

    slab_rank = int(np.linalg.matrix_rank(slab_j, tol=1.0e-10))
    thin_rank = int(np.linalg.matrix_rank(thin_j, tol=1.0e-6))
    mix_rank = int(np.linalg.matrix_rank(mix_j, tol=1.0e-10))
    degenerate_rank = int(np.linalg.matrix_rank(deg_j, tol=1.0e-10))
    checks = {
        "basis_orthonormal_and_centered": bool(
            np.allclose(basis.T @ basis, np.eye(5), atol=1.0e-12)
            and np.allclose(basis.T @ np.ones(6), 0.0, atol=1.0e-12)
        ),
        "slab_derivative_verified": bool(np.allclose(slab_j, slab_fd, atol=1.0e-8, rtol=1.0e-7)),
        "slab_rank_at_most_three": slab_rank <= 3,
        "thin_slab_rank_at_most_two": thin_rank <= 2,
        "mixture_derivative_verified": bool(np.allclose(mix_j, mix_fd, atol=1.0e-8, rtol=1.0e-7)),
        "distinct_two_component_rank_five": mix_rank == 5,
        "coincident_component_rank_loss": degenerate_rank < 5,
        "chain_rule_verified": bool(np.allclose(chain, chain_fd, atol=1.0e-8, rtol=1.0e-7)),
        "distinct_opacity_families_reproduce_same_two_line_ratio": bool(
            np.allclose(reproduced_a, published_line_intensity, atol=1.0e-12)
            and np.allclose(reproduced_b, published_line_intensity, atol=1.0e-12)
            and not np.allclose(tau_family_a, tau_family_b)
        ),
        "same_two_line_data_allow_distinct_centered_volume_responses": bool(
            not np.allclose(
                two_line_center @ opacity_response_a,
                two_line_center @ opacity_response_b,
            )
        ),
        "two_line_ratio_alone_does_not_identify_channel_opacity": True,
        "no_spectral_endpoint_read": True,
        "no_co109_header_or_pixel_read": True,
    }
    result = {
        "schema": "tau-core.paper8.sdp81-radiative-mixed-jet-minimal-rank.v01",
        "status": (
            "RADIATIVE_BASIS_EXISTS_TWO_LINE_OPACITY_PROFILE_UNIDENTIFIED"
            if all(checks.values())
            else "RADIATIVE_MIXED_JET_RANK_AUDIT_FAILED"
        ),
        "formula": "D_Z S=(D_xi S)P, P=D_Z xi",
        "uniform_slab_centered_log_rank": slab_rank,
        "optically_thin_uniform_slab_rank": thin_rank,
        "two_component_centered_log_rank": mix_rank,
        "two_component_minimum_singular_value": float(mix_singular.min()),
        "coincident_component_control_rank": degenerate_rank,
        "published_intrinsic_CO87_to_CO54_luminosity_ratio": 0.30,
        "published_ratio_uncertainty": 0.04,
        "two_line_opacity_profile_identified": False,
        "additional_source_closure_required": (
            "independent channel-wise source function/excitation or optical-depth "
            "constraint, including beam filling and differential magnification"
        ),
        "witness_bridge_determinant": float(np.linalg.det(bridge)),
        "physical_parent_to_gas_bridge_selected": False,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "claim_boundary": (
            "A local radiative rank theorem and nonempty completion witness; not "
            "a CO(10-9) calibration, parent-gas bridge, Nature occupation, or endpoint score. "
            "The published CO(8-7)/CO(5-4) ratio alone does not identify opacity."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 radiative mixed-jet minimal-rank audit v01\n\n"
        f"Status: `{result['status']}`. Checks: `{result['checks_passed']}/"
        f"{result['checks_total']}`. No spectral endpoint or CO(10-9) header/pixels were read.\n\n"
        f"Uniform-slab centered-log rank: `{slab_rank}`; optically thin limit: "
        f"`{thin_rank}`. Distinct two-component rank: `{mix_rank}`, minimum singular "
        f"value `{mix_singular.min():.6g}`. Coincident-component control rank: "
        f"`{degenerate_rank}`.\n\n"
        "The standard radiative block can be full rank, but the physical "
        "parent/body-mode to gas-state bridge $P=D_Z\\xi$ remains unselected.\n\n"
        "The published intrinsic $r_{8-7/5-4}=0.30\\pm0.04$ does not close the "
        "opacity profile. For any positive $\\tau_j$, choosing "
        "$S_j=I_j/(1-e^{-\\tau_j})$ reproduces the same two line intensities, "
        "while $\\partial_\\zeta\\log I_j=\\tau_j/(e^{\\tau_j}-1)$ changes. "
        "Two explicit positive counterfamilies verify this non-identifiability. "
        "A channel-wise excitation/source-function or independent opacity "
        "constraint is therefore required before a source-frozen score.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
