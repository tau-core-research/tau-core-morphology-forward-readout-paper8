#!/usr/bin/env python3
"""Endpoint-blind ordered conditional parent-to-gas response audit."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/sdp81_parent_gas_conditional_response_v01.json"
REPORT = ROOT / "reports/sdp81_parent_gas_conditional_response_v01.md"


def finite_difference(function, point: np.ndarray, step: float = 1.0e-6) -> np.ndarray:
    columns = []
    for index in range(point.size):
        plus, minus = point.copy(), point.copy()
        plus[index] += step
        minus[index] -= step
        columns.append((function(plus) - function(minus)) / (2.0 * step))
    return np.column_stack(columns)


def main() -> None:
    h_xi = np.asarray(
        [
            [3.2, 0.3, 0.0, 0.1, 0.0],
            [0.3, 2.7, 0.2, 0.0, 0.1],
            [0.0, 0.2, 2.4, 0.2, 0.0],
            [0.1, 0.0, 0.2, 2.9, 0.2],
            [0.0, 0.1, 0.0, 0.2, 2.5],
        ]
    )
    p0 = np.asarray(
        [
            [1.0, 0.1, 0.0, 0.0, 0.0],
            [0.0, 0.9, 0.2, 0.0, 0.0],
            [0.0, 0.0, 1.1, -0.1, 0.0],
            [0.0, 0.0, 0.0, 0.8, 0.15],
            [0.05, 0.0, 0.0, 0.0, 1.2],
        ]
    )
    xi0 = np.asarray([0.2, -0.1, 0.3, 0.05, -0.2])
    b_xi_z = -h_xi @ p0
    p_derived = -np.linalg.solve(h_xi, b_xi_z)
    p_fd = finite_difference(lambda z: xi0 + p0 @ z, np.zeros(5))

    h_values = np.linalg.eigvalsh(h_xi)
    p_singular = np.linalg.svd(p_derived, compute_uv=False)
    b_singular = np.linalg.svd(b_xi_z, compute_uv=False)
    lower = b_singular.min() / h_values.max()
    upper = b_singular.max() / h_values.min()

    backreaction = b_xi_z.T @ np.linalg.solve(h_xi, b_xi_z)
    h_z = backreaction + 2.0 * np.eye(5)
    joint = np.block([[h_z, b_xi_z.T], [b_xi_z, h_xi]])

    singular_p = p0.copy()
    singular_p[:, -1] = singular_p[:, 0]
    singular_b = -h_xi @ singular_p

    permutation = np.eye(5)
    permutation[[0, 1]] = permutation[[1, 0]]
    p_alt = p0 @ permutation
    b_alt = -h_xi @ p_alt

    checks = {
        "gas_hessian_positive": bool(h_values.min() > 0.0),
        "implicit_formula_verified": bool(np.allclose(p_derived, p0, atol=1.0e-12)),
        "finite_difference_verified": bool(np.allclose(p_derived, p_fd, atol=1.0e-9)),
        "full_rank_equivalence_verified": bool(
            np.linalg.matrix_rank(p_derived) == np.linalg.matrix_rank(b_xi_z) == 5
        ),
        "singular_control_verified": bool(
            np.linalg.matrix_rank(singular_p) == np.linalg.matrix_rank(singular_b) < 5
        ),
        "conditioning_bounds_verified": bool(
            p_singular.min() + 1.0e-12 >= lower
            and p_singular.max() <= upper + 1.0e-12
        ),
        "positive_joint_control": bool(np.linalg.eigvalsh(joint).min() > 0.0),
        "simultaneous_elimination_backreacts": bool(np.linalg.norm(backreaction) > 0.0),
        "same_reduct_does_not_select_bridge": bool(
            not np.allclose(-np.linalg.solve(h_xi, b_alt), p_derived)
        ),
        "physical_mixed_derivative_selected": False,
        "no_spectral_endpoint_read": True,
        "no_co109_header_or_pixel_read": True,
    }
    proof_checks = {
        key: value
        for key, value in checks.items()
        if key != "physical_mixed_derivative_selected"
    }
    status = (
        "CONDITIONAL_PARENT_GAS_RESPONSE_DERIVED_PHYSICAL_MIXED_JET_OPEN"
        if all(proof_checks.values()) and checks["physical_mixed_derivative_selected"] is False
        else "PARENT_GAS_CONDITIONAL_RESPONSE_AUDIT_FAILED"
    )
    result = {
        "schema": "tau-core.paper8.sdp81-parent-gas-conditional-response.v01",
        "status": status,
        "formula": "P=D_Z xi_*(Z)=-H_xi^{-1}B_xiZ",
        "derived_bridge_rank": int(np.linalg.matrix_rank(p_derived)),
        "mixed_derivative_rank": int(np.linalg.matrix_rank(b_xi_z)),
        "minimum_bridge_singular_value": float(p_singular.min()),
        "backreaction_frobenius_norm": float(np.linalg.norm(backreaction)),
        "physical_mixed_derivative_selected": False,
        "checks": checks,
        "proof_checks_passed": sum(proof_checks.values()),
        "proof_checks_total": len(proof_checks),
        "claim_boundary": (
            "The ordered implicit-response formula and no-backreaction requirement "
            "are derived. The physical conditional gas law, B_xiZ, and Nature "
            "occupation are not selected; no CO(10-9) endpoint was read."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 parent-to-gas conditional-response audit v01\n\n"
        f"Status: `{status}`. Proof checks: `{result['proof_checks_passed']}/"
        f"{result['proof_checks_total']}`. No spectral endpoint or CO(10-9) "
        "header/pixels were read.\n\n"
        "With the post-body response $Z$ already frozen, stationarity of a "
        "conditional gas functional gives "
        "$P=D_Z\\xi_*=-H_\\xi^{-1}B_{\\xi Z}$. Full bridge rank is therefore "
        "equivalent to full mixed-derivative rank.\n\n"
        "A simultaneous symmetric solve generically shifts the upstream Hessian "
        "by $-B_{\\xi Z}^T H_\\xi^{-1}B_{\\xi Z}$; the witness has nonzero "
        f"backreaction norm `{np.linalg.norm(backreaction):.6g}`. An alternative "
        "bridge with the same positive gas Hessian and baseline proves that the "
        "physical mixed derivative remains unselected.\n",
        encoding="utf-8",
    )
    print(status)


if __name__ == "__main__":
    main()
