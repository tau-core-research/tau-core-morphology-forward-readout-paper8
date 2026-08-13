#!/usr/bin/env python3
"""Score a frozen cumulative source-morphology response for NGC7479."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ngc7479_cumulative_morphology_scoring_v01.md"
G = 4.30091e-6
RBAR_KPC = 10.2
GALAXIES = ["NGC 613", "NGC 4303", "NGC 4579", "NGC 5248", "NGC 7479"]


def cumulative_response(points: pd.DataFrame, x_eval: np.ndarray) -> np.ndarray:
    q = points[points.point_origin.eq("vector_marker")].sort_values("physical_r_over_abar")
    x = q.physical_r_over_abar.to_numpy(float)
    delta = q.physical_delta.to_numpy(float)
    x_nodes = np.concatenate(([0.0], x))
    density = np.concatenate(([0.0], delta**2))
    cumulative = np.concatenate(([0.0], np.cumsum(np.diff(x_nodes) * (density[1:] + density[:-1]) / 2.0)))
    return np.interp(x_eval, x_nodes, cumulative, left=0.0, right=cumulative[-1])


def rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def main() -> None:
    freeze = json.loads((DATA / "ngc7479_cumulative_morphology_response_freeze_v01.json").read_text())
    endpoint = pd.read_csv(DATA / "ngc7479_hi_rotation_endpoint_v01.csv")
    stellar = pd.read_csv(DATA / "ngc7479_stellar_velocity_field_v01.csv")
    gas = pd.read_csv(DATA / "ngc7479_hi_radial_proxy_v01.csv")
    morph = pd.read_csv(DATA / "coming_vector_marker_centers_v01.csv")
    radius = endpoint.radius_kpc_at_source_distance.to_numpy(float)
    x_eval = radius / RBAR_KPC
    observed = endpoint.vrot_hi_km_s.to_numpy(float)
    vstar = stellar.vstar_total_primary_km_s.to_numpy(float)
    details, summaries = [], []
    for floor, gas_floor in gas.groupby("grayscale_floor"):
        enclosed = np.interp(radius, gas_floor.radius_kpc, gas_floor.gas_enclosed_mass_msun_with_helium)
        vgas = np.sqrt(G * enclosed / radius)
        vbar = np.sqrt(vstar**2 + vgas**2)
        predictions, responses = {}, {}
        for galaxy in GALAXIES:
            response = cumulative_response(morph[morph.galaxy.eq(galaxy)], x_eval)
            responses[galaxy] = response
            predictions[galaxy] = vbar * np.sqrt(1.0 + response)
        matched_rmse = rmse(observed, predictions["NGC 7479"])
        wrong = {g: rmse(observed, predictions[g]) for g in GALAXIES if g != "NGC 7479"}
        summaries.append({
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
        for i in range(len(radius)):
            details.append({
                "grayscale_floor": floor, "radius_kpc": radius[i], "radius_over_bar": x_eval[i],
                "vobs_hi_km_s": observed[i], "vbar_km_s": vbar[i],
                "cumulative_response_matched": responses["NGC 7479"][i],
                "vpred_matched_km_s": predictions["NGC 7479"][i],
            })
    detail = pd.DataFrame(details)
    summary = pd.DataFrame(summaries)
    detail.to_csv(DATA / "ngc7479_cumulative_morphology_scoring_points_v01.csv", index=False)
    summary.to_csv(DATA / "ngc7479_cumulative_morphology_scoring_summary_v01.csv", index=False)
    result = {
        "schema": "tau_core_ngc7479_cumulative_morphology_scoring_v01",
        "status": "POST_OPEN_DIAGNOSTIC_CUMULATIVE_SCORE_COMPLETE",
        "freeze_status": freeze["status"], "fitted_parameters": 0,
        "n_endpoint_points": len(endpoint), "n_gas_sensitivities": len(summary),
        "all_matched_beat_newton": bool(summary.matched_beats_newton.all()),
        "all_matched_beat_wrong_mean": bool(summary.matched_beats_wrong_mean.all()),
        "all_matched_beat_best_wrong": bool(summary.matched_beats_best_wrong.all()),
        "rmse_ranges": {
            "newton": [float(summary.rmse_newton_baryonic.min()), float(summary.rmse_newton_baryonic.max())],
            "matched": [float(summary.rmse_matched_ngc7479.min()), float(summary.rmse_matched_ngc7479.max())],
            "wrong_mean": [float(summary.rmse_wrong_family_mean.min()), float(summary.rmse_wrong_family_mean.max())],
            "best_wrong": [float(summary.rmse_wrong_family_best.min()), float(summary.rmse_wrong_family_best.max())],
        },
        "prospective": False,
        "strict_physical_score_allowed": False,
        "tau_morphology_detected": False,
        "channel_detected": False,
        "claim_boundary": "post-open diagnostic with raster gas and spherical gas gravity; no physical attribution"
    }
    (DATA / "ngc7479_cumulative_morphology_scoring_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC7479 cumulative morphology scoring v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The frozen zero-fit response accumulates the source profile as `Q(x)=integral_0^x Delta(s)^2 ds` and scores `v_pred^2=v_bar^2(1+Q)`. "
        f"RMSE ranges are Newton `{result['rmse_ranges']['newton']}`, matched `{result['rmse_ranges']['matched']}`, wrong mean `{result['rmse_ranges']['wrong_mean']}`, and best wrong `{result['rmse_ranges']['best_wrong']}` km/s.\n\n"
        "This is post-open diagnostic evidence only. The endpoint predates the formula, and the gas field remains raster/spherical-proxy grade.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
