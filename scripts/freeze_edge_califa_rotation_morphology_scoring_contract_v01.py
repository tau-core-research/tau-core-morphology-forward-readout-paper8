#!/usr/bin/env python3
"""Freeze and algebraically audit the unopened EDGE--CALIFA endpoint score."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import block_diag


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
PREREG = DATA / "edge_califa_rotation_morphology_preregistration_v03.json"
PREFLIGHT = DATA / "edge_califa_rotation_morphology_source_preflight_v02.json"
MATRICES = DATA / "edge_califa_rotation_morphology_source_matrices_v02.npz"
OUTPUT = DATA / "edge_califa_rotation_morphology_scoring_contract_v01.json"
HASH = DATA / "edge_califa_rotation_morphology_scoring_contract_v01.sha256"
REPORT = ROOT / "reports/edge_califa_rotation_morphology_scoring_contract_v01.md"

N_ZONES = 5
N_MODES = 4
N_SECTORS = 6
RELATIVE_SVD_TOLERANCE = 1.0e-10


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_rank(array: np.ndarray) -> int:
    singular = np.linalg.svd(array, compute_uv=False)
    if singular.size == 0 or singular[0] == 0:
        return 0
    return int(np.sum(singular > RELATIVE_SVD_TOLERANCE * singular[0]))


def fit_modes(design: np.ndarray, values: np.ndarray, variance: np.ndarray) -> np.ndarray:
    if stable_rank(design) != design.shape[1]:
        raise ValueError("Terminal harmonic design is rank deficient")
    if np.any(~np.isfinite(variance)) or np.any(variance <= 0):
        raise ValueError("Terminal variance is non-positive or non-finite")
    weight = 1.0 / variance
    normal = design.T @ (weight[:, None] * design)
    rhs = design.T @ (weight * values)
    coefficient = np.linalg.pinv(normal, rcond=RELATIVE_SVD_TOLERANCE) @ rhs
    if not np.all(np.isfinite(coefficient)):
        raise FloatingPointError("Terminal harmonic coefficient is non-finite")
    return coefficient


def sector_jackknife_block(
    design: np.ndarray, values: np.ndarray, variance: np.ndarray, sectors: np.ndarray
) -> np.ndarray:
    if set(np.unique(sectors)) != set(range(N_SECTORS)):
        raise ValueError("Every frozen macrosector must be occupied")
    estimates = []
    for omitted in range(N_SECTORS):
        keep = sectors != omitted
        estimates.append(fit_modes(design[keep], values[keep], variance[keep]))
    estimates = np.asarray(estimates)
    mean = estimates.mean(axis=0)
    covariance = (N_SECTORS - 1) / N_SECTORS * (estimates - mean).T @ (estimates - mean)
    retained = covariance[np.ix_([1, 2, 3, 4], [1, 2, 3, 4])]
    if stable_rank(retained) != N_MODES:
        raise ValueError("Retained sector-jackknife covariance is not rank four")
    if np.min(np.linalg.eigvalsh(retained)) <= 0:
        raise ValueError("Retained sector-jackknife covariance is not positive definite")
    return retained


def assemble_covariance(blocks: list[np.ndarray]) -> np.ndarray:
    if len(blocks) != N_ZONES:
        raise ValueError("Exactly five terminal covariance blocks are required")
    covariance = block_diag(*blocks)
    if covariance.shape != (20, 20) or stable_rank(covariance) != 20:
        raise ValueError("Assembled terminal covariance is not full rank")
    if not np.all(np.isfinite(covariance)) or not np.allclose(covariance, covariance.T):
        raise ValueError("Assembled terminal covariance is invalid")
    if np.min(np.linalg.eigvalsh(covariance)) <= 0:
        raise ValueError("Assembled terminal covariance is not positive definite")
    return covariance


def weighted_projection(source: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    inverse = np.linalg.inv(covariance)
    gram = source.T @ inverse @ source
    projection = np.eye(source.shape[0]) - source @ np.linalg.pinv(
        gram, rcond=RELATIVE_SVD_TOLERANCE
    ) @ source.T @ inverse
    if not np.all(np.isfinite(projection)):
        raise FloatingPointError("Covariance-weighted projection is non-finite")
    return projection


def score(source: np.ndarray, covariance: np.ndarray, terminal: np.ndarray) -> dict[str, Any]:
    if stable_rank(source) not in (8, 16):
        raise ValueError("Score source has an unexpected rank")
    projection = weighted_projection(source, covariance)
    innovation = projection @ terminal
    projected_covariance = projection @ covariance @ projection.T
    dof = stable_rank(projected_covariance)
    q_value = float(
        innovation
        @ np.linalg.pinv(projected_covariance, rcond=RELATIVE_SVD_TOLERANCE)
        @ innovation
    )
    if not np.isfinite(q_value) or q_value < -1.0e-8:
        raise FloatingPointError("Projection score is invalid")
    return {
        "q": max(0.0, q_value),
        "source_rank": stable_rank(source),
        "projection_rank": stable_rank(projection),
        "projected_covariance_rank": dof,
        "annihilation_max_abs": float(np.max(np.abs(projection @ source))),
    }


def radial_reverse(body: np.ndarray) -> np.ndarray:
    return body.reshape(N_ZONES, N_MODES, body.shape[1])[::-1].reshape(body.shape)


def phase_rotate_pi_over_2(body: np.ndarray) -> np.ndarray:
    rotated = body.reshape(N_ZONES, N_MODES, body.shape[1]).copy()
    for offset in (0, 2):
        real = rotated[:, offset, :].copy()
        imaginary = rotated[:, offset + 1, :].copy()
        rotated[:, offset, :] = -imaginary
        rotated[:, offset + 1, :] = real
    return rotated.reshape(body.shape)


def studentized_mean(values: np.ndarray) -> float:
    mean = float(np.mean(values))
    scale = float(np.std(values, ddof=1) / np.sqrt(values.size))
    if scale == 0:
        return float(np.sign(mean) * np.inf) if mean != 0 else 0.0
    return mean / scale


def exact_shared_sign_tests(differences: np.ndarray) -> dict[str, Any]:
    """Exact one-sided primary and shared-sign studentized max-T control tests."""
    if differences.ndim != 2 or differences.shape[1] != 3:
        raise ValueError("Expected N by three control-difference matrix")
    n_galaxies = differences.shape[0]
    if n_galaxies < 6:
        raise ValueError("The frozen exact test requires at least six galaxies")
    primary_values = differences.mean(axis=1)
    observed_primary = float(np.mean(primary_values))
    observed_t = np.array([studentized_mean(differences[:, j]) for j in range(3)])
    primary_null = []
    max_t_null = []
    for sign_tuple in itertools.product((-1.0, 1.0), repeat=n_galaxies):
        signs = np.asarray(sign_tuple)
        signed = signs[:, None] * differences
        primary_null.append(float(np.mean(signs * primary_values)))
        max_t_null.append(max(studentized_mean(signed[:, j]) for j in range(3)))
    primary_null = np.asarray(primary_null)
    max_t_null = np.asarray(max_t_null)
    tolerance = 1.0e-12
    primary_p = float(np.mean(primary_null >= observed_primary - tolerance))
    adjusted = [float(np.mean(max_t_null >= value - tolerance)) for value in observed_t]
    return {
        "n_galaxies": n_galaxies,
        "n_exact_sign_vectors": int(2**n_galaxies),
        "observed_primary_mean_d": observed_primary,
        "primary_exact_one_sided_p": primary_p,
        "control_studentized_statistics": observed_t.tolist(),
        "control_max_t_adjusted_p": adjusted,
        "median_primary_d": float(np.median(primary_values)),
        "positive_primary_count": int(np.sum(primary_values > 0)),
    }


def synthetic_covariance_audit() -> dict[str, Any]:
    rng = np.random.default_rng(20260830)
    blocks = []
    for zone in range(N_ZONES):
        sectors = np.repeat(np.arange(N_SECTORS), 10)
        angle = 2 * np.pi * (sectors + rng.uniform(0.05, 0.95, sectors.size)) / N_SECTORS - np.pi
        design = np.column_stack(
            [np.ones(angle.size), np.cos(angle), np.sin(angle), np.cos(2 * angle), np.sin(2 * angle)]
        )
        variance = rng.uniform(0.5, 2.0, angle.size)
        truth = np.array([0.2, 1.0, -0.6, 0.4, -0.3]) * (zone + 1)
        values = design @ truth + rng.normal(scale=np.sqrt(variance))
        blocks.append(sector_jackknife_block(design, values, variance, sectors))
    covariance = assemble_covariance(blocks)
    source = rng.normal(size=(20, 16))
    while stable_rank(source) != 16:
        source = rng.normal(size=(20, 16))
    terminal = source @ rng.normal(size=16)
    projected = score(source, covariance, terminal)
    return {
        "zone_covariance_ranks": [stable_rank(block) for block in blocks],
        "assembled_covariance_rank": stable_rank(covariance),
        "minimum_eigenvalue": float(np.min(np.linalg.eigvalsh(covariance))),
        "pure_source_q": projected["q"],
        "projected_rank": projected["projected_covariance_rank"],
        "all_gates_pass": bool(
            all(stable_rank(block) == 4 for block in blocks)
            and stable_rank(covariance) == 20
            and projected["projected_covariance_rank"] == 4
            and projected["q"] < 1.0e-8
        ),
    }


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    if prereg["endpoint_opened"] or preflight["velocity_terminal_values_opened"]:
        raise RuntimeError("Scoring contract must be frozen before endpoint opening")
    names = list(preflight["confirmatory_untouched"])
    if len(names) < 6:
        raise RuntimeError("Insufficient frozen confirmatory cohort")
    packet = np.load(MATRICES)
    rank_rows = []
    for index, name in enumerate(names):
        standard = packet[f"{name}__standard"]
        body = packet[f"{name}__body"]
        cross_name = names[(index + 1) % len(names)]
        controls = {
            "correct": np.column_stack([standard, body]),
            "radial_reversal": np.column_stack([standard, radial_reverse(body)]),
            "phase_rotation_pi_over_2": np.column_stack([standard, phase_rotate_pi_over_2(body)]),
            "cross_galaxy": np.column_stack([standard, packet[f"{cross_name}__body"]]),
        }
        row = {"galaxy": name, "cross_galaxy_body": cross_name}
        row.update({f"{label}_rank": stable_rank(matrix) for label, matrix in controls.items()})
        row["all_equal_rank_16"] = all(stable_rank(matrix) == 16 for matrix in controls.values())
        rank_rows.append(row)
    covariance_audit = synthetic_covariance_audit()
    all_pass = covariance_audit["all_gates_pass"] and all(row["all_equal_rank_16"] for row in rank_rows)
    if not all_pass:
        raise RuntimeError("The unopened scoring contract failed its algebraic audit")

    result = {
        "schema": "edge_califa_rotation_morphology_scoring_contract_v01",
        "status": "UNOPENED_ENDPOINT_SCORING_CONTRACT_FROZEN_AND_AUDITED",
        "preregistration_sha256": sha256(PREREG),
        "source_preflight_sha256": sha256(PREFLIGHT),
        "source_matrices_sha256": sha256(MATRICES),
        "confirmatory_galaxies": names,
        "source_control_rank_audit": rank_rows,
        "synthetic_covariance_audit": covariance_audit,
        "terminal_vector": "five zones times {m1_cos,m1_sin,m2_cos,m2_sin}",
        "score": "Q(S)=y^T P(S)^T [P(S) Sigma P(S)^T]^+ P(S)y",
        "per_galaxy_controls": ["radial_reversal", "phase_rotation_pi_over_2", "cross_galaxy"],
        "per_galaxy_primary": "D_g=mean(Q_control,g)-Q_correct,g",
        "primary_inference": "exact one-sided shared-sign permutation over all 2^N sign vectors",
        "control_inference": "shared-sign studentized max-T, one-sided and exact over all 2^N sign vectors",
        "thresholds": {
            "primary_p_less_than": 0.01,
            "median_d_positive": True,
            "strictly_more_than_fraction_positive": 0.60,
            "every_control_max_t_adjusted_p_less_than": 0.05,
        },
        "no_post_open_regularization": True,
        "terminal_values_opened": False,
        "claim_boundary": (
            "a pass is external source-developed morphology-alignment prevalidation beyond the "
            "declared nuisance span and controls, not a Tau-specific or beyond-standard discovery"
        ),
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    HASH.write_text(f"{digest}  data/derived/{OUTPUT.name}\n", encoding="utf-8")
    REPORT.write_text(
        "# EDGE--CALIFA rotation-morphology scoring contract v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "All seven correct and equal-rank control constructions have rank 16. The frozen "
        "six-sector covariance and rank-four projection algebra pass deterministic synthetic "
        "tests. The exact shared-sign primary and max-T procedures are now fixed. No CO or "
        "Halpha terminal velocity value was opened.\n",
        encoding="utf-8",
    )
    print(result["status"], digest)


if __name__ == "__main__":
    main()
