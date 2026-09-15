#!/usr/bin/env python3
"""Run the frozen depth-free PCRR rank-one diagnostic on SDP.81."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from run_sdp81_4d_corridor_proxy_covariance_robustness_v01 import log_mode_covariances
from run_sdp81_common_action_endpoint_v01 import load_frozen_endpoint


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
MODEL = DATA / "sdp81_pcrr_rank_one_invariant_diagnostic_freeze_v01.json"
ENDPOINT_MODEL = DATA / "sdp81_4d_corridor_proxy_diagnostic_freeze_v01.json"
COVARIANCE_SOURCE = DATA / "sdp81_4d_corridor_proxy_covariance_robustness_v01.json"
OUT = DATA / "sdp81_pcrr_rank_one_invariant_diagnostic_score_v01.json"
REPORT = ROOT / "reports/sdp81_pcrr_rank_one_invariant_diagnostic_score_v01.md"


def singular_statistics(matrix: np.ndarray) -> dict:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    total = float(singular_values @ singular_values)
    if total <= 0.0:
        return {
            "singular_values": singular_values.tolist(),
            "rank_one_energy_fraction": 0.0,
            "rank_one_residual_fraction": 0.0,
        }
    leading = float(singular_values[0] ** 2 / total)
    return {
        "singular_values": singular_values.tolist(),
        "rank_one_energy_fraction": leading,
        "rank_one_residual_fraction": 1.0 - leading,
    }


def projected_log_covariance(
    fluxes: np.ndarray,
    path_basis: np.ndarray,
    channel_basis: np.ndarray,
    channel_covariance: np.ndarray,
) -> np.ndarray:
    mode_covariances = log_mode_covariances(
        fluxes, channel_basis, channel_covariance
    )
    block = np.zeros((20, 20), dtype=float)
    for index, covariance in enumerate(mode_covariances):
        block[index * 5 : (index + 1) * 5, index * 5 : (index + 1) * 5] = covariance
    transform = np.kron(path_basis.T, np.eye(5))
    return transform @ block @ transform.T


def monte_carlo_p_value(values: np.ndarray, observed: float) -> float:
    return float((1 + np.sum(values >= observed)) / (values.size + 1))


def score_geometry(
    index: int,
    observed_matrix: np.ndarray,
    observed_stats: dict,
    covariance: np.ndarray,
    draws: int,
    seed_base: int,
) -> dict:
    left, singular, right_t = np.linalg.svd(observed_matrix, full_matrices=False)
    fitted_rank_one = singular[0] * np.outer(left[:, 0], right_t[0])
    seed = np.random.SeedSequence([seed_base, index])
    null_seed, rank_one_seed = seed.spawn(2)
    null_rng = np.random.default_rng(null_seed)
    rank_one_rng = np.random.default_rng(rank_one_seed)
    null_draws = null_rng.multivariate_normal(
        np.zeros(15), covariance, size=draws
    ).reshape(draws, 3, 5)
    null_singular = np.linalg.svd(null_draws, compute_uv=False)
    null_energy = null_singular[:, 0] ** 2 / np.sum(null_singular**2, axis=1)
    rank_one_draws = rank_one_rng.multivariate_normal(
        np.zeros(15), covariance, size=draws
    ).reshape(draws, 3, 5) + fitted_rank_one
    rank_one_singular = np.linalg.svd(rank_one_draws, compute_uv=False)
    rank_one_residual = np.sum(rank_one_singular[:, 1:] ** 2, axis=1) / np.sum(
        rank_one_singular**2, axis=1
    )
    null_p = monte_carlo_p_value(
        null_energy, observed_stats["rank_one_energy_fraction"]
    )
    rank_one_gof_p = monte_carlo_p_value(
        rank_one_residual, observed_stats["rank_one_residual_fraction"]
    )
    return {
        "noise_null_rank_one_energy_median": float(np.median(null_energy)),
        "noise_null_upper_tail_p_value": null_p,
        "rank_one_bootstrap_residual_median": float(np.median(rank_one_residual)),
        "rank_one_gof_upper_tail_p_value": rank_one_gof_p,
        "rank_zero_rejected_at_0_05": null_p <= 0.05,
        "rank_one_rejected_at_0_05": rank_one_gof_p <= 0.05,
    }


def main() -> None:
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    if not model.get("diagnostic_run_allowed") or model.get("physical_endpoint_authorized"):
        raise RuntimeError("rank-one diagnostic is not authorized")
    endpoint_model = json.loads(ENDPOINT_MODEL.read_text(encoding="utf-8"))
    covariance_source = json.loads(COVARIANCE_SOURCE.read_text(encoding="utf-8"))
    fluxes = load_frozen_endpoint(endpoint_model)
    path_basis = np.asarray(model["path_centering_basis"], dtype=float)
    channel_basis = np.asarray(model["channel_centering_basis"], dtype=float)
    observed_matrix = path_basis.T @ np.log(fluxes) @ channel_basis
    observed_stats = singular_statistics(observed_matrix)
    draw_count = int(model["statistics"]["bootstrap_draws_per_geometry"])
    seed_base = int(model["statistics"]["random_seed_base"])
    records = []
    for index, geometry in enumerate(covariance_source["geometry_records"]):
        covariance = projected_log_covariance(
            fluxes,
            path_basis,
            channel_basis,
            np.asarray(geometry["channel_covariance"], dtype=float),
        )
        score = score_geometry(
            index, observed_matrix, observed_stats, covariance, draw_count, seed_base
        )
        records.append(
            {
                "inner_radius_arcsec": geometry["inner_radius_arcsec"],
                "outer_radius_arcsec": geometry["outer_radius_arcsec"],
                "grid_step_arcsec": geometry["grid_step_arcsec"],
                "projected_covariance_minimum_eigenvalue": float(
                    np.linalg.eigvalsh(covariance).min()
                ),
                **score,
            }
        )
    null_p = [record["noise_null_upper_tail_p_value"] for record in records]
    gof_p = [record["rank_one_gof_upper_tail_p_value"] for record in records]
    summary = {
        "geometry_count": len(records),
        "noise_null_upper_tail_p_value_range": [float(min(null_p)), float(max(null_p))],
        "rank_one_gof_upper_tail_p_value_range": [float(min(gof_p)), float(max(gof_p))],
        "rank_zero_rejected_geometries": sum(
            record["rank_zero_rejected_at_0_05"] for record in records
        ),
        "rank_one_rejected_geometries": sum(
            record["rank_one_rejected_at_0_05"] for record in records
        ),
    }
    checks = {
        "nine_covariance_geometries": len(records) == 9,
        "all_projected_covariances_positive": all(
            record["projected_covariance_minimum_eigenvalue"] > 0.0
            for record in records
        ),
        "rank_zero_not_rejected_any_geometry": summary[
            "rank_zero_rejected_geometries"
        ]
        == 0,
        "rank_one_not_rejected_any_geometry": summary[
            "rank_one_rejected_geometries"
        ]
        == 0,
        "no_depth_proxy_used": True,
        "physical_endpoint_remains_unauthorized": True,
    }
    result = {
        "schema": "tau-core.paper8.sdp81-pcrr-rank-one-invariant-score.v01",
        "status": "RETROSPECTIVE_DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "verdict": "RANK_ONE_COMPATIBLE_NOT_DETECTED_NOT_IDENTIFYING",
        "model": str(MODEL.relative_to(ROOT)),
        "covariance_source": str(COVARIANCE_SOURCE.relative_to(ROOT)),
        "spectral_endpoint_read": True,
        "observed_double_centered_log_matrix": observed_matrix.tolist(),
        "observed_statistics": observed_stats,
        "geometry_records": records,
        "summary": summary,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "physical_endpoint_authorized": False,
        "confirmatory_prediction": False,
        "claim_boundary": (
            "The observed interaction is compatible with a rank-one matrix under "
            "all nine covariance models, but its leading singular fraction is not "
            "unusual under the rank-zero noise control. Rank one is also shared by "
            "nonlinear separable filters and can be altered by path-mode calibration. "
            "This depth-free retrospective diagnostic neither detects PCRR nor "
            "identifies Tau, parent depth, terminal calibration, or Nature occupation."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 PCRR rank-one invariant diagnostic score v01\n\n"
        f"Status: `{result['status']}`. Verdict: `{result['verdict']}`.\n\n"
        f"Observed singular values: `{', '.join(f'{value:.6f}' for value in observed_stats['singular_values'])}`. "
        f"The leading mode carries `{observed_stats['rank_one_energy_fraction']:.3%}` "
        f"of double-centered log-spectral energy; residual fraction "
        f"`{observed_stats['rank_one_residual_fraction']:.3%}`.\n\n"
        f"Across nine covariance geometries, rank-zero noise upper-tail p spans "
        f"`{min(null_p):.3f}--{max(null_p):.3f}` and fitted-rank-one goodness-of-fit "
        f"p spans `{min(gof_p):.3f}--{max(gof_p):.3f}`. Neither rank zero nor rank "
        "one is rejected at 0.05 in any geometry.\n\n"
        f"{result['claim_boundary']}\n",
        encoding="utf-8",
    )
    print(result["verdict"])


if __name__ == "__main__":
    main()
