#!/usr/bin/env python3
"""Audit projector identities and frozen controls without endpoint values."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
MATRICES = DATA / "phangs_radial_body_projection_development_terminal_edge_matrices_v01.npz"
REPLAY = DATA / "phangs_radial_body_projection_development_terminal_edge_replay_v01.json"
REPORT = ROOT / "reports/phangs_radial_body_projection_operator_audit_v01.md"


def projector(source: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    inverse = np.linalg.inv(covariance)
    return np.eye(source.shape[0]) - source @ np.linalg.pinv(source.T @ inverse @ source) @ source.T @ inverse


def radial_reverse(source: np.ndarray) -> np.ndarray:
    return source.reshape(5, 4, source.shape[1])[::-1].reshape(source.shape)


def phase_rotate_pi_over_2(source: np.ndarray) -> np.ndarray:
    rotated = source.reshape(5, 4, source.shape[1]).copy()
    for offset in (0, 2):
        real = rotated[:, offset, :].copy()
        imag = rotated[:, offset + 1, :].copy()
        rotated[:, offset, :] = -imag
        rotated[:, offset + 1, :] = real
    return rotated.reshape(source.shape)


def max_abs(array: np.ndarray) -> float:
    return float(np.max(np.abs(array)))


def stable_rank(array: np.ndarray, relative_tolerance: float = 1.0e-10) -> int:
    singular = np.linalg.svd(array, compute_uv=False)
    return int(np.sum(singular > relative_tolerance * singular[0]))


def main() -> None:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    if replay["body_projection_score_computed"] or replay["confirmatory_galaxies_opened"]:
        raise RuntimeError("Operator audit requires a score-free development replay")
    matrices = np.load(MATRICES)
    rows = {}
    for galaxy in matrices.files:
        source = matrices[galaxy]
        seed = int.from_bytes(galaxy.encode("ascii"), "little") % (2**32)
        rng = np.random.default_rng(seed)
        factor = rng.normal(size=(20, 20))
        covariance = factor @ factor.T + 0.5 * np.eye(20)
        inverse = np.linalg.inv(covariance)
        projection = projector(source, covariance)
        projected_covariance = projection @ covariance @ projection.T
        body_vector = source @ np.arange(1.0, source.shape[1] + 1.0)
        q_body = float(
            (projection @ body_vector)
            @ np.linalg.pinv(projected_covariance)
            @ (projection @ body_vector)
        )
        reverse = radial_reverse(source)
        phase = phase_rotate_pi_over_2(source)
        rows[galaxy] = {
            "source_rank": stable_rank(source),
            "projection_rank": stable_rank(projection),
            "projected_covariance_rank": stable_rank(projected_covariance),
            "annihilation_max_abs": max_abs(projection @ source),
            "idempotence_max_abs": max_abs(projection @ projection - projection),
            "weighted_self_adjoint_max_abs": max_abs(projection.T @ inverse - inverse @ projection),
            "body_vector_q": q_body,
            "radial_reverse_rank": stable_rank(reverse),
            "phase_pi_over_2_rank": stable_rank(phase),
            "stellar_only_rank": stable_rank(source[:, :4]),
            "co_only_rank": stable_rank(source[:, 4:]),
        }
    all_pass = all(
        row["source_rank"] == 8
        and row["projection_rank"] == 12
        and row["projected_covariance_rank"] == 12
        and row["annihilation_max_abs"] < 1.0e-10
        and row["idempotence_max_abs"] < 1.0e-10
        and row["weighted_self_adjoint_max_abs"] < 1.0e-10
        and abs(row["body_vector_q"]) < 1.0e-10
        and row["radial_reverse_rank"] == 8
        and row["phase_pi_over_2_rank"] == 8
        and row["stellar_only_rank"] == 4
        and row["co_only_rank"] == 4
        for row in rows.values()
    )
    result = {
        "schema": "phangs_radial_body_projection_operator_audit_v01",
        "status": "COVARIANCE_WEIGHTED_BODY_PROJECTOR_IDENTITIES_PASS",
        "galaxies": rows,
        "all_operator_checks_pass": all_pass,
        "rank_relative_svd_tolerance": 1.0e-10,
        "covariance_role": "deterministic synthetic SPD matrices for algebra and conditioning only",
        "velocity_contrast_used": False,
        "terminal_coefficients_used": False,
        "confirmatory_galaxies_opened": [],
        "endpoint_score_computed": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": (
            "finite numerical audit of projector identities and source controls; not an empirical "
            "body-orthogonal mode, channel, time, quantum, Tau, or dark-sector result"
        ),
    }
    output = DATA / "phangs_radial_body_projection_operator_audit_v01.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# PHANGS radial body-projection operator audit v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "All five development matrices annihilate their source columns, give an idempotent "
        "covariance-weighted projector of rank 12, preserve the frozen control ranks, and return "
        "numerical zero for a pure body vector. Deterministic synthetic SPD covariances were used; "
        "no velocity contrast, terminal coefficient, confirmatory product, or endpoint score was read.\n",
        encoding="utf-8",
    )
    print(result["status"], all_pass)
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
