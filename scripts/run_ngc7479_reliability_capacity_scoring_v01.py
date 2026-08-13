#!/usr/bin/env python3
"""Score the frozen source-reliability and finite-capacity response."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ngc7479_reliability_capacity_scoring_v01.md"
G = 4.30091e-6
RBAR_KPC = 10.2
GALAXIES = ["NGC 613", "NGC 4303", "NGC 4579", "NGC 5248", "NGC 7479"]


def response(points: pd.DataFrame, x_eval: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    q = points[points.point_origin.eq("vector_marker")].sort_values("physical_r_over_abar")
    x = q.physical_r_over_abar.to_numpy(float)
    delta = q.physical_delta.to_numpy(float)
    sigma = 0.5 * (
        q.physical_delta_error_minus.to_numpy(float)
        + q.physical_delta_error_plus.to_numpy(float)
    )
    reliability = delta**2 / np.maximum(delta**2 + sigma**2, 1.0e-15)
    density = reliability * delta**2
    x_nodes = np.concatenate(([0.0], x))
    density_nodes = np.concatenate(([0.0], density))
    cumulative = np.concatenate((
        [0.0],
        np.cumsum(np.diff(x_nodes) * (density_nodes[1:] + density_nodes[:-1]) / 2.0),
    ))
    q_eval = np.interp(x_eval, x_nodes, cumulative, left=0.0, right=cumulative[-1])
    return q_eval / (1.0 + q_eval), reliability


def rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def main() -> None:
    freeze = json.loads((DATA / "ngc7479_reliability_capacity_response_freeze_v01.json").read_text())
    endpoint = pd.read_csv(DATA / "ngc7479_hi_rotation_endpoint_v01.csv")
    stellar = pd.read_csv(DATA / "ngc7479_stellar_velocity_field_v01.csv")
    gas = pd.read_csv(DATA / "ngc7479_hi_radial_proxy_v01.csv")
    morph = pd.read_csv(DATA / "coming_vector_marker_centers_v01.csv")
    radius = endpoint.radius_kpc_at_source_distance.to_numpy(float)
    x_eval = radius / RBAR_KPC
    observed = endpoint.vrot_hi_km_s.to_numpy(float)
    vstar = stellar.vstar_total_primary_km_s.to_numpy(float)
    responses, reliability_summary = {}, {}
    for galaxy in GALAXIES:
        responses[galaxy], rho = response(morph[morph.galaxy.eq(galaxy)], x_eval)
        reliability_summary[galaxy] = {
            "mean": float(np.mean(rho)), "min": float(np.min(rho)), "max": float(np.max(rho))
        }
    detail_rows, summary_rows = [], []
    for floor, gas_floor in gas.groupby("grayscale_floor"):
        enclosed = np.interp(radius, gas_floor.radius_kpc, gas_floor.gas_enclosed_mass_msun_with_helium)
        vgas = np.sqrt(G * enclosed / radius)
        vbar = np.sqrt(vstar**2 + vgas**2)
        predictions = {g: vbar * np.sqrt(1.0 + responses[g]) for g in GALAXIES}
        matched_rmse = rmse(observed, predictions["NGC 7479"])
        wrong = {g: rmse(observed, predictions[g]) for g in GALAXIES if g != "NGC 7479"}
        summary_rows.append({
            "grayscale_floor": floor,
            "rmse_newton_baryonic": rmse(observed, vbar),
            "rmse_matched_ngc7479": matched_rmse,
            "rmse_wrong_family_mean": float(np.mean(list(wrong.values()))),
            "rmse_wrong_family_best": float(min(wrong.values())),
            "best_wrong_galaxy": min(wrong, key=wrong.get),
            "matched_beats_newton": matched_rmse < rmse(observed, vbar),
            "matched_beats_wrong_mean": matched_rmse < np.mean(list(wrong.values())),
            "matched_beats_best_wrong": matched_rmse < min(wrong.values()),
        })
        for i, r in enumerate(radius):
            detail_rows.append({
                "grayscale_floor": floor, "radius_kpc": r, "radius_over_bar": x_eval[i],
                "vobs_hi_km_s": observed[i], "vbar_km_s": vbar[i],
                "matched_capacity_response": responses["NGC 7479"][i],
                "vpred_matched_km_s": predictions["NGC 7479"][i],
            })
    detail = pd.DataFrame(detail_rows)
    summary = pd.DataFrame(summary_rows)
    detail.to_csv(DATA / "ngc7479_reliability_capacity_scoring_points_v01.csv", index=False)
    summary.to_csv(DATA / "ngc7479_reliability_capacity_scoring_summary_v01.csv", index=False)
    result = {
        "schema": "tau_core_ngc7479_reliability_capacity_scoring_v01",
        "status": "POST_OPEN_RELIABILITY_CAPACITY_DIAGNOSTIC_COMPLETE",
        "freeze_status": freeze["status"], "fitted_parameters": 0,
        "n_endpoint_points": len(endpoint), "n_gas_sensitivities": len(summary),
        "source_reliability": reliability_summary,
        "all_matched_beat_newton": bool(summary.matched_beats_newton.all()),
        "all_matched_beat_wrong_mean": bool(summary.matched_beats_wrong_mean.all()),
        "all_matched_beat_best_wrong": bool(summary.matched_beats_best_wrong.all()),
        "rmse_ranges": {
            "newton": [float(summary.rmse_newton_baryonic.min()), float(summary.rmse_newton_baryonic.max())],
            "matched": [float(summary.rmse_matched_ngc7479.min()), float(summary.rmse_matched_ngc7479.max())],
            "wrong_mean": [float(summary.rmse_wrong_family_mean.min()), float(summary.rmse_wrong_family_mean.max())],
            "best_wrong": [float(summary.rmse_wrong_family_best.min()), float(summary.rmse_wrong_family_best.max())]
        },
        "prospective": False, "strict_physical_score_allowed": False,
        "tau_morphology_detected": False, "channel_detected": False,
        "claim_boundary": freeze["claim_boundary"]
    }
    (DATA / "ngc7479_reliability_capacity_scoring_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC7479 reliability-capacity scoring v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The zero-fit post-open diagnostic weights each source marker by `rho=Delta^2/(Delta^2+sigma^2)`, accumulates `rho Delta^2`, and applies the finite map `C=Q/(1+Q)`. "
        f"RMSE ranges are Newton `{result['rmse_ranges']['newton']}`, matched `{result['rmse_ranges']['matched']}`, wrong mean `{result['rmse_ranges']['wrong_mean']}`, and best wrong `{result['rmse_ranges']['best_wrong']}` km/s.\n\n"
        "This does not derive a physical capacity law and is not prospective for NGC7479.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
