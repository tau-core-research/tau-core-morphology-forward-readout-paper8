#!/usr/bin/env python3
"""Freeze and audit the unopened PHANGS radial body-projection score."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import block_diag
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
MATRICES = DATA / "phangs_radial_body_projection_development_terminal_edge_matrices_v01.npz"
PREREGISTRATION = DATA / "phangs_radial_body_projection_preregistration_v01.json"
IDENTIFIABILITY = DATA / "phangs_radial_body_projection_holdout_identifiability_v01.json"
REPORT = ROOT / "reports/phangs_radial_body_projection_scoring_contract_v01.md"

RELATIVE_SVD_TOLERANCE = 1.0e-10
N_ZONES = 5
N_MODES = 4
N_SECTORS = 12
GLOBAL_ALPHA = 0.01
INDIVIDUAL_ALPHA = 0.05
MIN_INDIVIDUAL_DETECTIONS = 3


def stable_rank(array: np.ndarray) -> int:
    singular = np.linalg.svd(array, compute_uv=False)
    if singular.size == 0 or singular[0] == 0:
        return 0
    return int(np.sum(singular > RELATIVE_SVD_TOLERANCE * singular[0]))


def fit_modes(design: np.ndarray, values: np.ndarray, variance: np.ndarray) -> np.ndarray:
    if stable_rank(design) != design.shape[1] or np.any(variance <= 0):
        raise ValueError("Mode fit failed its rank or positive-variance gate")
    weight = 1.0 / variance
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        normal = design.T @ (weight[:, None] * design)
        right_hand_side = design.T @ (weight * values)
        coefficient = np.linalg.pinv(normal, rcond=RELATIVE_SVD_TOLERANCE) @ right_hand_side
    if not np.all(np.isfinite(coefficient)):
        raise FloatingPointError("Mode coefficient is non-finite")
    return coefficient


def sector_jackknife_block(
    design: np.ndarray, values: np.ndarray, variance: np.ndarray, sectors: np.ndarray
) -> np.ndarray:
    if set(np.unique(sectors)) != set(range(N_SECTORS)):
        raise ValueError("All 12 frozen azimuth sectors must be occupied")
    estimates = []
    for omitted in range(N_SECTORS):
        keep = sectors != omitted
        estimates.append(fit_modes(design[keep], values[keep], variance[keep]))
    estimates = np.asarray(estimates)
    mean = estimates.mean(axis=0)
    covariance = (N_SECTORS - 1) / N_SECTORS * (estimates - mean).T @ (estimates - mean)
    retained = covariance[np.ix_([1, 2, 3, 4], [1, 2, 3, 4])]
    if stable_rank(retained) != N_MODES:
        raise ValueError("Retained sector-jackknife covariance block is rank deficient")
    return retained


def assemble_decision_covariance(blocks: list[np.ndarray]) -> np.ndarray:
    if len(blocks) != N_ZONES:
        raise ValueError("Exactly five covariance blocks are required")
    covariance = block_diag(*blocks)
    if (
        covariance.shape != (20, 20)
        or not np.all(np.isfinite(covariance))
        or not np.allclose(covariance, covariance.T, atol=1.0e-12)
        or stable_rank(covariance) != 20
        or np.min(np.linalg.eigvalsh(covariance)) <= 0
    ):
        raise ValueError("Assembled decision covariance failed its frozen gates")
    return covariance


def weighted_projection(source: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    inverse = np.linalg.inv(covariance)
    # Accelerate-backed NumPy can retain benign FP flags across finite matmuls.
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        gram = source.T @ inverse @ source
        projection = np.eye(source.shape[0]) - source @ np.linalg.pinv(
            gram, rcond=RELATIVE_SVD_TOLERANCE
        ) @ source.T @ inverse
    if not np.all(np.isfinite(projection)):
        raise FloatingPointError("Weighted projection is non-finite")
    return projection


def score(source: np.ndarray, covariance: np.ndarray, terminal: np.ndarray) -> dict[str, Any]:
    projection = weighted_projection(source, covariance)
    innovation = projection @ terminal
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        projected_covariance = projection @ covariance @ projection.T
    if not np.all(np.isfinite(projected_covariance)):
        raise FloatingPointError("Projected covariance is non-finite")
    dof = stable_rank(projected_covariance)
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        q_value = float(
            innovation
            @ np.linalg.pinv(projected_covariance, rcond=RELATIVE_SVD_TOLERANCE)
            @ innovation
        )
    if not np.isfinite(q_value):
        raise FloatingPointError("Projected Q is non-finite")
    return {
        "q": q_value,
        "dof": dof,
        "p_chi_square_approximation": float(chi2.sf(q_value, dof)),
        "projection_rank": stable_rank(projection),
        "projected_covariance_rank": dof,
        "innovation_norm": float(np.linalg.norm(innovation)),
    }


def radial_reverse(source: np.ndarray) -> np.ndarray:
    return source.reshape(N_ZONES, N_MODES, source.shape[1])[::-1].reshape(source.shape)


def phase_rotate_pi_over_2(source: np.ndarray) -> np.ndarray:
    rotated = source.reshape(N_ZONES, N_MODES, source.shape[1]).copy()
    for offset in (0, 2):
        real = rotated[:, offset, :].copy()
        imaginary = rotated[:, offset + 1, :].copy()
        rotated[:, offset, :] = -imaginary
        rotated[:, offset + 1, :] = real
    return rotated.reshape(source.shape)


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    q_value = float(sum(row["q"] for row in rows))
    dof = int(sum(row["dof"] for row in rows))
    individual_passes = int(
        sum(row["p_chi_square_approximation"] < INDIVIDUAL_ALPHA for row in rows)
    )
    p_value = float(chi2.sf(q_value, dof))
    return {
        "q": q_value,
        "dof": dof,
        "p_chi_square_approximation": p_value,
        "individual_p_below_0_05": individual_passes,
        "primary_and_replication_thresholds_pass": bool(
            p_value < GLOBAL_ALPHA and individual_passes >= MIN_INDIVIDUAL_DETECTIONS
        ),
    }


def synthetic_covariance(galaxy: str) -> np.ndarray:
    seed = int.from_bytes(galaxy.encode("ascii"), "little") % (2**32)
    rng = np.random.default_rng(seed)
    blocks = []
    for _ in range(N_ZONES):
        factor = rng.normal(size=(N_MODES, N_MODES))
        blocks.append(factor @ factor.T + 0.5 * np.eye(N_MODES))
    return block_diag(*blocks)


def audit_jackknife_assembly() -> dict[str, Any]:
    rng = np.random.default_rng(20260720)
    blocks = []
    for zone in range(N_ZONES):
        sectors = np.repeat(np.arange(N_SECTORS), 6)
        angle = 2.0 * np.pi * (sectors + rng.uniform(0.1, 0.9, sectors.size)) / N_SECTORS - np.pi
        design = np.column_stack(
            [np.ones(angle.size), np.cos(angle), np.sin(angle), np.cos(2 * angle), np.sin(2 * angle)]
        )
        truth = np.array([0.5, 1.0, -0.7, 0.4, -0.2]) * (zone + 1)
        variance = rng.uniform(0.5, 2.0, angle.size)
        values = design @ truth + rng.normal(scale=np.sqrt(variance))
        blocks.append(sector_jackknife_block(design, values, variance, sectors))
    covariance = assemble_decision_covariance(blocks)
    return {
        "zone_block_ranks": [stable_rank(block) for block in blocks],
        "assembled_rank": stable_rank(covariance),
        "minimum_eigenvalue": float(np.min(np.linalg.eigvalsh(covariance))),
        "all_gates_pass": bool(
            all(stable_rank(block) == N_MODES for block in blocks)
            and stable_rank(covariance) == 20
            and np.min(np.linalg.eigvalsh(covariance)) > 0
        ),
    }


def main() -> None:
    preregistration = json.loads(PREREGISTRATION.read_text(encoding="utf-8"))
    identifiability = json.loads(IDENTIFIABILITY.read_text(encoding="utf-8"))
    if preregistration["endpoint_opened"] or identifiability["endpoint_score_computed"]:
        raise RuntimeError("The scoring contract must be frozen before endpoint opening")
    if not identifiability["derived_results"]["projection_q_can_test_body_orthogonal_innovation"]:
        raise RuntimeError("The finite identifiability audit does not authorize the one-shot Q test")

    matrices = np.load(MATRICES)
    jackknife_audit = audit_jackknife_assembly()
    synthetic_checks: dict[str, Any] = {}
    all_pass = jackknife_audit["all_gates_pass"]
    for galaxy in matrices.files:
        source = matrices[galaxy]
        covariance = synthetic_covariance(galaxy)
        beta = np.arange(1.0, source.shape[1] + 1.0)
        pure_body = source @ beta
        body_score = score(source, covariance, pure_body)
        reverse_score = score(radial_reverse(source), covariance, pure_body)
        phase_score = score(phase_rotate_pi_over_2(source), covariance, pure_body)
        stellar_only_score = score(source[:, :4], covariance, pure_body)
        co_only_score = score(source[:, 4:], covariance, pure_body)

        projection = weighted_projection(source, covariance)
        candidate = projection @ np.linspace(-1.0, 1.0, source.shape[0])
        if np.linalg.norm(candidate) < 1.0e-8:
            candidate = projection @ np.eye(source.shape[0])[:, 0]
        transverse_score = score(source, covariance, pure_body + candidate)
        checks = {
            "covariance_rank_20": bool(stable_rank(covariance) == 20),
            "pure_body_q_zero": bool(abs(body_score["q"]) < 1.0e-10),
            "projected_dof_12": bool(body_score["dof"] == 12),
            "transverse_q_positive": bool(transverse_score["q"] > 1.0e-8),
            "radial_control_computable": bool(np.isfinite(reverse_score["q"])),
            "phase_control_computable": bool(np.isfinite(phase_score["q"])),
            "stellar_ablation_computable": bool(np.isfinite(stellar_only_score["q"])),
            "co_ablation_computable": bool(np.isfinite(co_only_score["q"])),
        }
        all_pass = all_pass and all(checks.values())
        synthetic_checks[galaxy] = {
            "checks": checks,
            "pure_body": body_score,
            "transverse_injection": transverse_score,
            "radial_reversal_pure_body_q": reverse_score["q"],
            "phase_rotation_pure_body_q": phase_score["q"],
            "stellar_only_pure_body_q": stellar_only_score["q"],
            "co_only_pure_body_q": co_only_score["q"],
        }

    decision_truth_table = {
        "global_and_three_individual": bool(0.009 < GLOBAL_ALPHA and 3 >= MIN_INDIVIDUAL_DETECTIONS),
        "global_without_replication": bool(0.009 < GLOBAL_ALPHA and 2 >= MIN_INDIVIDUAL_DETECTIONS),
        "replication_without_global": bool(0.02 < GLOBAL_ALPHA and 4 >= MIN_INDIVIDUAL_DETECTIONS),
    }
    all_pass = all_pass and decision_truth_table == {
        "global_and_three_individual": True,
        "global_without_replication": False,
        "replication_without_global": False,
    }

    result = {
        "schema": "phangs_radial_body_projection_scoring_contract_v01",
        "status": "ONE_SHOT_BODY_ORTHOGONAL_Q_SCORING_CONTRACT_FROZEN_UNOPENED",
        "terminal_construction": {
            "quality_cuts": {
                "maximum_velocity_error_km_s": 10.0,
                "minimum_halpha_flux_snr": 5.0,
                "maximum_absolute_halpha_velocity_km_s": 450.0,
                "beam_independent_sampling": "integer CO-beam pixel stride in both image axes",
            },
            "zero_point": "median(CO-Halpha) on the beam-independent common-quality support",
            "contrast": "CO velocity - frozen zero point - beam-matched Halpha velocity",
            "pixel_variance": "CO velocity error squared + Halpha velocity error squared",
            "radial_edges": "five quantile zones of radius on the same common-quality support",
            "angular_fit": "weighted least squares in {m0,m1_cos,m1_sin,m2_cos,m2_sin}",
            "terminal_vector": "zone-major {m1_cos,m1_sin,m2_cos,m2_sin}; m0 excluded; dimension 20",
        },
        "decision_covariance": {
            "construction": "block diagonal of five per-zone 4-by-4 m1/m2 leave-one-azimuth-sector jackknife covariance blocks",
            "azimuth_sectors": N_SECTORS,
            "jackknife_formula": "(J-1)/J sum_j (theta_j-theta_bar)(theta_j-theta_bar)^T",
            "required_zone_gates": [
                "all 12 sectors occupied",
                "every leave-one-sector five-mode design has rank 5",
                "each retained 4-by-4 covariance block has stable rank 4",
                "the assembled 20-by-20 covariance is finite, symmetric, and positive definite",
            ],
            "cross_zone_covariance": "set to zero in the decision statistic by the frozen block construction",
            "inference_boundary": "chi-square p-values are approximations because 12-sector jackknife blocks are not a complete spatial covariance model",
            "regularization": "forbidden after opening; a failed covariance gate makes that galaxy non-identifiable",
        },
        "projection_and_score": {
            "projection": "P=I-S(S^T Sigma^-1 S)^+S^T Sigma^-1",
            "innovation": "z=P y",
            "projected_covariance": "C=P Sigma P^T",
            "statistic": "Q=z^T C^+ z",
            "degrees_of_freedom": "stable rank(C)",
            "relative_svd_tolerance": RELATIVE_SVD_TOLERANCE,
            "per_galaxy_p": "chi2.sf(Q, dof)",
            "global_statistic": "sum_g Q_g with dof=sum_g dof_g",
        },
        "decision_rule": {
            "global_p_below": GLOBAL_ALPHA,
            "individual_p_below": INDIVIDUAL_ALPHA,
            "minimum_individual_detections_of_four": MIN_INDIVIDUAL_DETECTIONS,
            "both_conditions_required": True,
        },
        "controls": {
            "radial_reversal": "reverse the five source-profile zones before constructing S",
            "phase_rotation": "rotate every complex m1 and m2 source profile by pi/2 at fixed amplitude",
            "geometric_control_pass": "Q_correct is strictly below Q_control globally and in at least 3 of 4 individual galaxies, separately for each geometric control",
            "stellar_ablation": "repeat with the four CO columns only; report, not a detection gate",
            "co_ablation": "repeat with the four stellar columns only; report, not a detection gate",
        },
        "hard_stop_gates": [
            "confirmatory cohort must remain exactly NGC1300, NGC1385, NGC1512, NGC5068",
            "every acquired source and terminal hash must match its pre-open manifest",
            "source matrix and projection ranks must be 8 and 12 respectively",
            "every decision-covariance zone gate must pass without repair",
            "no formula, threshold, source column, radial zone, or galaxy replacement may change after opening",
        ],
        "promotion_boundary": {
            "one_shot_q_can_detect_body_orthogonal_tracer_structure": True,
            "grouped_body_increment_available": False,
            "reason": identifiability["minimal_corrected_statement"],
            "positive_q_does_not_identify": [
                "observer channel",
                "time readout",
                "quantum readout",
                "Tau-parent mechanism",
                "dark sector",
            ],
        },
        "synthetic_audit": synthetic_checks,
        "jackknife_assembly_audit": jackknife_audit,
        "decision_truth_table": decision_truth_table,
        "all_synthetic_checks_pass": all_pass,
        "velocity_contrast_used": False,
        "terminal_coefficients_used": False,
        "confirmatory_galaxies_opened": [],
        "endpoint_score_computed": False,
        "claim_boundary": (
            "pre-open executable scoring contract and synthetic numerical audit; not an empirical "
            "body-orthogonal mode, channel, time, quantum, Tau, or dark-sector result"
        ),
    }
    output = DATA / "phangs_radial_body_projection_scoring_contract_v01.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# PHANGS radial body-projection scoring contract v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The pre-open contract now fixes the common-support terminal vector, five block-sector-"
        "jackknife covariance matrices, covariance-weighted projection, individual and aggregate "
        "`Q`, stable-rank tolerance, thresholds, controls, and hard-stop gates. The chi-square "
        "calibration is explicitly approximate because the sector jackknife is not a complete "
        "spatial covariance. No contrast, coefficient, confirmatory field, or endpoint score was "
        "opened.\n\n"
        "A positive one-shot result would mean that the differential tracer field contains structure "
        "outside the declared radial body span and survives the frozen source-geometry controls. It "
        "would not identify a channel component or its time, quantum, Tau, or dark-sector origin. "
        "The grouped body-increment promotion clause remains unavailable under the proved finite "
        "identifiability no-go.\n",
        encoding="utf-8",
    )
    print(result["status"], all_pass)
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
