#!/usr/bin/env python3
"""Re-evaluate UGC08490 side compatibility with interpolation covariance."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ugc08490_oriented_channel_covariance_audit_v02.md"
C_KM_S = 299792.458


def interpolation_matrix(source_x: np.ndarray, target_x: np.ndarray) -> np.ndarray:
    weights = np.zeros((len(target_x), len(source_x)))
    for i, x in enumerate(target_x):
        hi = int(np.searchsorted(source_x, x, side="right"))
        hi = min(max(hi, 1), len(source_x) - 1)
        lo = hi - 1
        fraction = (x - source_x[lo]) / (source_x[hi] - source_x[lo])
        weights[i, lo] = 1.0 - fraction
        weights[i, hi] = fraction
    return weights


def dq_dv(vobs: np.ndarray, vbar: np.ndarray) -> np.ndarray:
    step = 1.0e-3
    def q(v: np.ndarray) -> np.ndarray:
        bo, bb = v / C_KM_S, vbar / C_KM_S
        return np.arctanh((bo - bb) / (1.0 - bo * bb))
    return (q(vobs + step) - q(vobs - step)) / (2.0 * step)


def main() -> None:
    first = json.loads((DATA / "ugc08490_oriented_channel_compatibility_v01.json").read_text())
    points = pd.read_csv(DATA / "ugc08490_oriented_channel_compatibility_points_v01.csv")
    sides = pd.read_csv(DATA / "ghasp_full_federation_side_points_v01.csv")
    sides = sides[sides.ghasp_key.eq("UGC8490") & sides.velocity_km_s.gt(0)].copy()
    radius = points.radius_kpc.to_numpy(float)
    covariance = np.zeros((len(radius), len(radius)))
    side_diagnostics = {}
    for label, code in (("approaching", "a"), ("receding", "r")):
        source = sides[sides.side.eq(code)].sort_values("radius_kpc")
        x = source.radius_kpc.to_numpy(float)
        sigma_v = source.velocity_error_km_s.to_numpy(float)
        weights = interpolation_matrix(x, radius)
        covariance_v = weights @ np.diag(sigma_v**2) @ weights.T
        derivative = dq_dv(
            points[f"v_{label}_km_s"].to_numpy(float),
            points.vbar_km_s.to_numpy(float),
        )
        covariance_q = np.diag(derivative) @ covariance_v @ np.diag(derivative)
        covariance += covariance_q
        side_diagnostics[label] = {
            "n_source_points": len(source),
            "interpolation_matrix_rank": int(np.linalg.matrix_rank(weights)),
            "covariance_rank": int(np.linalg.matrix_rank(covariance_q)),
            "max_off_diagonal_correlation": float(np.max(np.abs(
                covariance_q / np.sqrt(np.outer(np.diag(covariance_q), np.diag(covariance_q)))
                - np.eye(len(radius))
            ))),
        }
    difference = points.q_approaching.to_numpy(float) - points.q_receding.to_numpy(float)
    inverse = np.linalg.pinv(covariance, rcond=1.0e-12)
    rank = int(np.linalg.matrix_rank(covariance))
    chi2 = float(difference @ inverse @ difference)
    leave_one_out = []
    for omitted in range(len(radius)):
        keep = np.arange(len(radius)) != omitted
        cov_keep = covariance[np.ix_(keep, keep)]
        diff_keep = difference[keep]
        rank_keep = int(np.linalg.matrix_rank(cov_keep))
        chi2_keep = float(diff_keep @ np.linalg.pinv(cov_keep, rcond=1.0e-12) @ diff_keep)
        leave_one_out.append({
            "omitted_radius_kpc": float(radius[omitted]),
            "chi2_per_effective_dof": chi2_keep / rank_keep,
        })
    one = np.ones(len(radius))
    mean = float((one @ inverse @ difference) / (one @ inverse @ one))
    mean_error = float(np.sqrt(1.0 / (one @ inverse @ one)))
    result = {
        "schema": "tau_core_ugc08490_oriented_channel_covariance_audit_v02",
        "status": "INTERPOLATION_COVARIANCE_AWARE_COMPATIBILITY_AUDIT_COMPLETE",
        "first_pass_status": first["status"], "fitted_channel_parameters": 0,
        "n_common_radii": len(radius), "covariance_rank": rank,
        "side_diagnostics": side_diagnostics,
        "gls_side_compatibility": {
            "chi2": chi2, "effective_degrees_of_freedom": rank,
            "chi2_per_effective_dof": chi2 / rank,
            "weighted_mean_q_difference": mean,
            "weighted_mean_q_difference_error": mean_error,
            "weighted_mean_q_difference_z": mean / mean_error,
        },
        "leave_one_radius_out": {
            "minimum_chi2_per_effective_dof": float(min(x["chi2_per_effective_dof"] for x in leave_one_out)),
            "maximum_chi2_per_effective_dof": float(max(x["chi2_per_effective_dof"] for x in leave_one_out)),
            "best_omitted_radius_kpc": float(min(leave_one_out, key=lambda x: x["chi2_per_effective_dof"])["omitted_radius_kpc"]),
            "all_omissions": leave_one_out,
        },
        "common_reciprocal_load_compatible": bool(chi2 / rank <= 2.0),
        "baryonic_covariance_included": False,
        "inclination_covariance_included": False,
        "physical_channel_detected": False,
        "claim_boundary": "retrospective interpolation-covariance audit; remaining geometry and baryonic covariance are open, and common load remains halo-degenerate"
    }
    (DATA / "ugc08490_oriented_channel_covariance_audit_v02.json").write_text(json.dumps(result, indent=2) + "\n")
    pd.DataFrame(covariance).to_csv(DATA / "ugc08490_oriented_channel_difference_covariance_v02.csv", index=False)
    REPORT.write_text(
        "# UGC08490 oriented-channel covariance audit v02\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The exact linear-interpolation weight matrices give covariance rank `{rank}`. GLS side compatibility is "
        f"`chi2/dof={chi2 / rank:.3f}` and mean-difference `z={mean / mean_error:.3f}`. "
        f"Maximum off-diagonal correlations are `{side_diagnostics['approaching']['max_off_diagonal_correlation']:.3f}` and "
        f"`{side_diagnostics['receding']['max_off_diagonal_correlation']:.3f}`.\n\n"
        "No channel parameter is fitted. Geometry/baryonic covariance and dark-halo degeneracy remain open.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
