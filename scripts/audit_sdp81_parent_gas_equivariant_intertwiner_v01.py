#!/usr/bin/env python3
"""Endpoint-blind audit of symmetry constraints on the parent--gas bridge."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/sdp81_parent_gas_equivariant_intertwiner_v01.json"
REPORT = ROOT / "reports/sdp81_parent_gas_equivariant_intertwiner_v01.md"


def helmert(count: int) -> np.ndarray:
    basis = np.zeros((count, count - 1))
    for column in range(count - 1):
        scale = np.sqrt((column + 1) * (column + 2))
        basis[: column + 1, column] = 1.0 / scale
        basis[column + 1, column] = -(column + 1) / scale
    return basis


def permutation_matrix(permutation: tuple[int, ...]) -> np.ndarray:
    matrix = np.zeros((len(permutation), len(permutation)))
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def commutant_nullity(actions: list[np.ndarray]) -> int:
    size = actions[0].shape[0]
    constraints = [
        np.kron(action.T, np.eye(size)) - np.kron(np.eye(size), action)
        for action in actions
    ]
    return size * size - int(
        np.linalg.matrix_rank(np.vstack(constraints), tol=1.0e-10)
    )


def radiative_rank(u: np.ndarray, xi: np.ndarray, basis: np.ndarray) -> int:
    rho, center1, center2, log_width1, log_width2 = xi
    width1, width2 = np.exp(log_width1), np.exp(log_width2)
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
    return int(
        np.linalg.matrix_rank(basis.T @ np.diag(1.0 / flux) @ derivative, tol=1.0e-10)
    )


def swap_state(xi: np.ndarray) -> np.ndarray:
    rho, center1, center2, log_width1, log_width2 = xi
    return np.asarray([-rho, center2, center1, log_width2, log_width1])


def main() -> None:
    basis = helmert(6)
    reversal = basis.T @ permutation_matrix(tuple(reversed(range(6)))) @ basis
    reflection_values = np.linalg.eigvalsh(reversal)
    plus = int(np.sum(reflection_values > 0.0))
    minus = int(np.sum(reflection_values < 0.0))
    z2_dimension = commutant_nullity([reversal])

    adjacency = np.zeros((6, 6))
    for index in range(5):
        adjacency[index, index + 1] = adjacency[index + 1, index] = 1.0
    laplacian = basis.T @ (np.diag(adjacency.sum(axis=1)) - adjacency) @ basis

    s6_generators = []
    graph_commutators = []
    for index in range(5):
        permutation = list(range(6))
        permutation[index], permutation[index + 1] = permutation[index + 1], permutation[index]
        generator = basis.T @ permutation_matrix(tuple(permutation)) @ basis
        s6_generators.append(generator)
        graph_commutators.append(np.linalg.norm(generator @ laplacian - laplacian @ generator))
    s6_dimension = commutant_nullity(s6_generators)

    second_z2_bridge = np.eye(5) + 0.3 * reversal
    trivial_gas_rank = int(
        np.linalg.matrix_rank(0.5 * (np.eye(5) + reversal), tol=1.0e-10)
    )

    generic = np.asarray([0.2, -0.9, 0.8, np.log(0.65), np.log(0.9)])
    fixed = np.asarray([0.0, 0.1, 0.1, np.log(0.8), np.log(0.8)])
    generic_swap_distance = float(np.linalg.norm(swap_state(generic) - generic))
    fixed_rank = radiative_rank(np.linspace(-2.5, 2.5, 6), fixed, basis)

    checks = {
        "basis_orthonormal": bool(np.allclose(basis.T @ basis, np.eye(5))),
        "reflection_is_involution": bool(np.allclose(reversal @ reversal, np.eye(5))),
        "p6_reflection_is_graph_symmetry": bool(
            np.linalg.norm(reversal @ laplacian - laplacian @ reversal) < 1.0e-12
        ),
        "reflection_split_is_two_plus_three": plus == 2 and minus == 3,
        "reflection_commutant_dimension_is_thirteen": z2_dimension == 13,
        "multiple_full_rank_reflection_intertwiners_exist": bool(
            np.linalg.matrix_rank(second_z2_bridge) == 5
            and not np.allclose(second_z2_bridge, np.eye(5))
            and np.allclose(second_z2_bridge @ reversal, reversal @ second_z2_bridge)
        ),
        "standard_s6_commutant_dimension_is_one": s6_dimension == 1,
        "standard_s6_is_not_p6_graph_symmetry": bool(max(graph_commutators) > 1.0e-6),
        "s6_scalar_scale_remains_free": bool(
            all(
                np.allclose((0.7 * np.eye(5)) @ g, g @ (0.7 * np.eye(5)))
                and np.allclose((1.4 * np.eye(5)) @ g, g @ (1.4 * np.eye(5)))
                for g in s6_generators
            )
        ),
        "trivial_gas_reflection_has_rank_at_most_two": trivial_gas_rank == 2,
        "generic_two_component_baseline_not_swap_fixed": bool(generic_swap_distance > 0.0),
        "swap_fixed_baseline_radiative_rank_below_five": fixed_rank < 5,
        "no_spectral_endpoint_read": True,
        "no_co109_header_or_pixel_read": True,
    }
    status = (
        "SYMMETRY_INTERTWINER_SHAPE_DERIVED_CURRENT_SYMMETRIES_NONSELECTING"
        if all(checks.values())
        else "PARENT_GAS_EQUIVARIANT_INTERTWINER_AUDIT_FAILED"
    )
    result = {
        "schema": "tau-core.paper8.sdp81-parent-gas-equivariant-intertwiner.v01",
        "status": status,
        "formula": "P rho_Z(g)=rho_xi(g)P",
        "p6_reflection_parity_multiplicities": [plus, minus],
        "p6_reflection_intertwiner_dimension": z2_dimension,
        "hypothetical_s6_commutant_dimension": s6_dimension,
        "two_component_swap_fixed_radiative_rank": fixed_rank,
        "physical_common_representation_owned": False,
        "physical_susceptibility_anchor_owned": False,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "claim_boundary": (
            "Current terminal-graph and component-label symmetries do not select "
            "the physical parent-to-gas bridge or authorize the CO(10-9) endpoint."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 parent--gas equivariant-intertwiner audit v01\n\n"
        f"Status: `{status}`. Checks: `{result['checks_passed']}/"
        f"{result['checks_total']}`. No spectral endpoint or CO(10-9) header/pixels "
        "were read.\n\n"
        "A common source-owned symmetry would require "
        "$P\\rho_Z(g)=\\rho_\\xi(g)P$. The actual ordered $P_6$ reflection has "
        f"centered parity split `{plus}+{minus}` and a `{z2_dimension}`-dimensional "
        "intertwiner space, so it does not select the bridge. A hypothetical "
        f"standard $S_6$ action leaves a `{s6_dimension}`-dimensional scalar "
        "commutant, but is neither a symmetry of the ordered graph nor a sourced "
        "gas representation, and its scale remains free.\n\n"
        "Generic distinct gas components are not fixed by label exchange; its "
        f"fixed locus has radiative rank `{fixed_rank}`. The physical common "
        "representation/intertwiner and nonzero susceptibility anchor remain open.\n",
        encoding="utf-8",
    )
    print(status)


if __name__ == "__main__":
    main()
