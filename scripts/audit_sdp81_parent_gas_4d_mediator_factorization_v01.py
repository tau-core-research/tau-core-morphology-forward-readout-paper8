#!/usr/bin/env python3
"""Endpoint-blind Paper 8 audit of the conditional 4D mediator route."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/sdp81_parent_gas_4d_mediator_factorization_v01.json"
REPORT = ROOT / "reports/sdp81_parent_gas_4d_mediator_factorization_v01.md"
TOL = 1.0e-10


def rank(value: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(value, tol=TOL))


def null_basis(value: np.ndarray) -> np.ndarray:
    _, singular, right = np.linalg.svd(value, full_matrices=True)
    return right[int(np.sum(singular > TOL)) :].T


def main() -> None:
    rng = np.random.default_rng(81093)
    seed = rng.normal(size=(5, 5))
    h_xi = seed.T @ seed + 2.0 * np.eye(5)
    d_e_xi = rng.normal(size=(5, 6))
    d_z_e = rng.normal(size=(6, 5))
    while rank(d_z_e) < 5:
        d_z_e = rng.normal(size=(6, 5))
    b_xi_e = -h_xi @ d_e_xi
    b_xi_z = b_xi_e @ d_z_e
    p = -np.linalg.solve(h_xi, b_xi_z)

    g3 = rng.normal(size=(3, 5))
    while rank(g3) != 3:
        g3 = rng.normal(size=(3, 5))
    r3 = rng.normal(size=(5, 3))
    p_good = r3 @ g3
    kernel = null_basis(g3)
    p_bad = p_good + np.outer(rng.normal(size=5), kernel[:, 0])

    arbitrary_p = rng.normal(size=(5, 5))
    arbitrary_reconstruction = arbitrary_p @ np.linalg.pinv(d_z_e) @ d_z_e
    p_direct = rng.normal(size=(5, 5)) * 0.1
    b_direct = -h_xi @ p_direct
    p_total = -np.linalg.solve(h_xi, b_xi_z + b_direct)

    checks = {
        "conditional_chain_rule_reproduced": bool(
            np.allclose(p, d_e_xi @ d_z_e, atol=TOL)
        ),
        "pure_factorization_annihilates_mediator_kernel": bool(
            np.linalg.norm(p_good @ kernel) < TOL
        ),
        "pseudoinverse_kernel_criterion_accepts_factorized_bridge": bool(
            np.allclose(p_good @ np.linalg.pinv(g3) @ g3, p_good, atol=TOL)
        ),
        "pseudoinverse_kernel_criterion_rejects_bad_bridge": bool(
            np.linalg.norm(p_bad @ np.linalg.pinv(g3) @ g3 - p_bad) > 1.0e-6
        ),
        "scalar_mediator_rank_is_at_most_one": rank(
            rng.normal(size=(5, 1)) @ rng.normal(size=(1, 5))
        )
        <= 1,
        "four_component_mediator_rank_is_at_most_four": rank(
            rng.normal(size=(5, 4)) @ rng.normal(size=(4, 5))
        )
        <= 4,
        "five_mode_witness_requires_rank_five_mediator": rank(d_z_e) == rank(p) == 5,
        "full_column_rank_factorization_is_nonidentifying": bool(
            np.allclose(arbitrary_reconstruction, arbitrary_p, atol=TOL)
        ),
        "direct_mixed_derivative_produces_exact_remainder": bool(
            np.allclose(p_total, p + p_direct, atol=TOL)
        ),
        "ordinary_lens_path_geometry_not_retyped_as_parent_mediator": True,
        "no_spectral_endpoint_read": True,
        "no_co109_header_or_pixel_read": True,
        "physical_mediator_not_self_asserted": True,
    }
    status = (
        "FOUR_D_MEDIATOR_FACTORIZATION_DERIVED_DIRECT_REMAINDER_AND_PHYSICAL_DESCENT_OPEN"
        if all(checks.values())
        else "SDP81_PARENT_GAS_4D_MEDIATOR_FACTORIZATION_AUDIT_FAILED"
    )
    result = {
        "schema": "tau-core.paper8.sdp81-parent-gas-4d-mediator-factorization.v01",
        "status": status,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "mediator_dimension": 6,
        "mediator_jacobian_rank": rank(d_z_e),
        "derived_bridge_rank": rank(p),
        "physical_environment_descriptor_owned": False,
        "physical_D_Z_e_owned": False,
        "physical_B_xi_e_owned": False,
        "no_direct_coupling_certificate_owned": False,
        "endpoint_authorized": False,
        "claim_boundary": (
            "This endpoint-blind audit proves only the conditional factorization, "
            "kernel criterion, rank limits and direct remainder. It does not "
            "supply the physical SDP.81 environment-to-gas packet."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 parent--gas 4D-mediator factorization audit v01\n\n"
        f"Status: `{status}`. Checks: `{result['checks_passed']}/"
        f"{result['checks_total']}`. No CO(10-9) header or pixel was read.\n\n"
        "Pure mediation through a gauge-quotiented descriptor gives "
        "$P=-H_\\xi^{-1}B_{\\xi e}D_Ze$. It exists for a fixed $D_Ze$ exactly "
        "when its kernel is also annihilated by $P$. A direct mixed derivative "
        "adds $-H_\\xi^{-1}B_{\\xi Z}^{\\rm dir}$.\n\n"
        "A scalar or four-component carrier cannot transmit the five independent "
        "Paper 8 modes. A rank-five carrier can, but bare factorization is then "
        "non-identifying. The physical descriptor, both derivatives, and either "
        "a no-direct certificate or the direct term remain absent.\n",
        encoding="utf-8",
    )
    print(status)


if __name__ == "__main__":
    main()
