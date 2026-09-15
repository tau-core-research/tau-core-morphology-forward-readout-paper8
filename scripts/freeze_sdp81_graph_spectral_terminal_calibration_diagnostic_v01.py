#!/usr/bin/env python3
"""Freeze a canonical ordered-channel spectral calibration diagnostic.

The six declared spectral channels define a path graph.  Its centered
Laplacian has simple spectrum, so its eigenvectors fix terminal modes up to
sign.  This removes the arbitrary ordering of Helmert columns.  It does not,
however, derive which source stiffness belongs to which graph frequency:
monotone and reverse assignments are both retained as conditional candidates.
No endpoint data are read by this freeze step.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

from freeze_sdp81_4d_corridor_proxy_diagnostic_v01 import (
    exp_symmetric,
    ordered_channel_generator,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
BASE = DATA / "sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json"
OUT = DATA / "sdp81_graph_spectral_terminal_calibration_diagnostic_freeze_v01.json"
REPORT = ROOT / "reports/sdp81_graph_spectral_terminal_calibration_diagnostic_freeze_v01.md"

WR_T19_SOURCE = (
    "source_material/tau_core_foundations/numerical_checks/"
    "tau_core_wr_t19_fixed_seed_body_channel_transmission_audit_v01_summary.json"
)
WR_T19_SHA256 = "713202b771d8dfa20a2cfb4be3af39444b81fa1fb50ef7fee7f3f70342a74e15"
WR_T19_STIFFNESSES = np.asarray([1.25, 1.5, 2.0, 2.5, 3.0], dtype=float)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_graph_modes() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return Helmert basis, reduced Laplacian, eigenvalues and signed modes."""
    helmert, laplacian = ordered_channel_generator(6)
    eigenvalues, rotation = np.linalg.eigh(laplacian)
    channel_modes = helmert @ rotation
    # The sign is immaterial to a diagonal self-adjoint transfer, but freezing
    # it makes the calibration artifact byte-stable and independently testable.
    for column in range(channel_modes.shape[1]):
        support = np.flatnonzero(np.abs(channel_modes[:, column]) > 1e-12)
        if channel_modes[support[0], column] < 0.0:
            channel_modes[:, column] *= -1.0
            rotation[:, column] *= -1.0
    return helmert, laplacian, eigenvalues, rotation


def compile_transfers(depths: list[float], generator: np.ndarray) -> list[list[list[float]]]:
    return [exp_symmetric(-depth * generator).tolist() for depth in depths]


def build_freeze(base: dict) -> dict:
    helmert, laplacian, eigenvalues, rotation = canonical_graph_modes()
    stored_basis = np.asarray(base["terminal_calibration"]["centered_log_channel_basis"])
    if not np.allclose(helmert, stored_basis):
        raise ValueError("the frozen terminal Helmert basis changed")

    depths = [float(item["proxy_depth"]) for item in base["compiled_paths"]]
    spectrum = WR_T19_STIFFNESSES / float(WR_T19_STIFFNESSES.max())
    monotone = rotation @ np.diag(0.5 * spectrum) @ rotation.T
    reverse = rotation @ np.diag(0.5 * spectrum[::-1]) @ rotation.T
    isotropic = np.eye(5) * (0.5 * float(np.mean(spectrum)))
    candidates = {
        "wr_t19_graph_monotone_half": {
            "role": "conditional_monotone_spectral_locality_candidate",
            "generator": monotone.tolist(),
            "transfers": compile_transfers(depths, monotone),
            "assignment": "increasing stiffness with increasing path-graph frequency",
        },
        "wr_t19_graph_reverse_half": {
            "role": "adversarial_assignment_control",
            "generator": reverse.tolist(),
            "transfers": compile_transfers(depths, reverse),
            "assignment": "decreasing stiffness with increasing path-graph frequency",
        },
        "isotropic_mean_half": {
            "role": "mode_blind_control",
            "generator": isotropic.tolist(),
            "transfers": compile_transfers(depths, isotropic),
            "assignment": "mean stiffness on every centered mode",
        },
    }
    mode_assignment_ensemble = []
    for permutation in itertools.permutations(range(5)):
        assigned = spectrum[list(permutation)]
        generator = rotation @ np.diag(0.5 * assigned) @ rotation.T
        mode_assignment_ensemble.append(
            {
                "assignment_id": "perm_" + "".join(str(index) for index in permutation),
                "permutation": list(permutation),
                "normalized_stiffness_by_increasing_graph_frequency": assigned.tolist(),
                "generator": generator.tolist(),
                "transfers": compile_transfers(depths, generator),
            }
        )
    commutators = {
        name: float(
            np.linalg.norm(np.asarray(item["generator"]) @ laplacian - laplacian @ np.asarray(item["generator"]))
        )
        for name, item in candidates.items()
    }
    theoretical = np.asarray(
        [(2.0 - 2.0 * np.cos(k * np.pi / 6.0)) / (2.0 + 2.0 * np.cos(np.pi / 6.0)) for k in range(1, 6)]
    )
    checks = {
        "base_proxy_is_nonphysical": base["physical_endpoint_authorized"] is False,
        "no_endpoint_read_during_freeze": True,
        "graph_spectrum_is_simple": bool(np.all(np.diff(eigenvalues) > 1e-12)),
        "graph_spectrum_matches_path_p6": bool(np.allclose(eigenvalues, theoretical)),
        "canonical_modes_are_orthonormal": bool(np.allclose(rotation.T @ rotation, np.eye(5))),
        "canonical_modes_diagonalize_laplacian": bool(
            np.allclose(rotation.T @ laplacian @ rotation, np.diag(eigenvalues))
        ),
        "all_candidates_commute_with_laplacian": max(commutators.values()) < 1e-12,
        "all_five_factorial_assignments_frozen": len(mode_assignment_ensemble) == 120,
        "all_transfers_are_positive_contractions": all(
            np.linalg.eigvalsh(np.asarray(transfer)).min() > 0.0
            and np.linalg.svd(np.asarray(transfer), compute_uv=False).max() < 1.0
            for item in candidates.values()
            for transfer in item["transfers"]
        ),
        "physical_endpoint_remains_unauthorized": True,
    }
    return {
        "schema": "tau-core.paper8.sdp81-graph-spectral-terminal-calibration-freeze.v01",
        "status": "CANONICAL_GRAPH_BASIS_FROZEN_ASSIGNMENT_OPEN_DIAGNOSTIC_ONLY",
        "scientific_role": (
            "retrospective discrimination of source-stiffness assignments after a "
            "canonical ordered-channel basis construction; not terminal calibration"
        ),
        "inputs": {
            "base_proxy": str(BASE.relative_to(ROOT)),
            "base_proxy_sha256": sha256(BASE),
            "spectral_or_velocity_endpoint_read": False,
        },
        "source_provenance": {
            "wr_t19_path": WR_T19_SOURCE,
            "wr_t19_sha256": WR_T19_SHA256,
            "wr_t19_stiffnesses": WR_T19_STIFFNESSES.tolist(),
        },
        "conditional_lemma": {
            "name": "PATHCAL-1",
            "statement": (
                "For the declared P6 ordered-channel graph, the centered normalized "
                "Laplacian has five simple eigenvalues. Every self-adjoint operator "
                "commuting with it is diagonal in its graph eigenbasis."
            ),
            "proved_here": True,
            "non_implication": (
                "Commutation fixes eigenvectors, not the assignment of five supplied "
                "stiffness eigenvalues; all permutations still commute."
            ),
        },
        "additional_assumptions": {
            "ordered_nearest_neighbor_channel_graph": (
                "declared terminal proxy; physical parent ownership not derived"
            ),
            "self_adjoint_commuting_terminal_operator": (
                "conditional candidate assumption; not derived"
            ),
            "monotone_stiffness_in_graph_frequency": (
                "tested candidate assumption; not derived and not supported by this score"
            ),
        },
        "path_ids": [item["path_id"] for item in base["compiled_paths"]],
        "proxy_depths": depths,
        "depth_boundary": (
            "depth remains the normalized conventional 4D Fermat proxy and is not "
            "identified with parent morphological distance"
        ),
        "helmert_basis": helmert.tolist(),
        "normalized_path_graph_laplacian": laplacian.tolist(),
        "canonical_graph_eigenvalues": eigenvalues.tolist(),
        "helmert_to_canonical_rotation": rotation.tolist(),
        "canonical_channel_modes": (helmert @ rotation).tolist(),
        "commutator_norms": commutators,
        "candidates": candidates,
        "mode_assignment_ensemble": mode_assignment_ensemble,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "diagnostic_run_allowed": all(checks.values()),
        "physical_endpoint_authorized": False,
        "retrospective_only": True,
        "claim_boundary": (
            "PATHCAL-1 removes arbitrary Helmert-column ordering under a declared P6 "
            "terminal graph, but neither derives that graph from the parent package "
            "nor selects a monotone stiffness assignment. The retrospective score "
            "cannot establish terminal calibration, parent depth, physical realization, "
            "or nonzero Nature occupation."
        ),
    }


def main() -> None:
    result = build_freeze(json.loads(BASE.read_text(encoding="utf-8")))
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 graph-spectral terminal-calibration freeze v01\n\n"
        f"Status: `{result['status']}`; checks: "
        f"`{result['checks_passed']}/{result['checks_total']}`.\n\n"
        "`PATHCAL-1` canonically diagonalizes the declared ordered-channel graph. "
        "Monotone, reverse, and isotropic source-stiffness assignments are frozen "
        "before endpoint scoring. No endpoint is read here.\n\n"
        f"{result['claim_boundary']}\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
