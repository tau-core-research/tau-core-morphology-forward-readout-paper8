#!/usr/bin/env python3
"""Run endpoint-blind diagnostic NGC7479 bar scoring with raster gas proxies."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORT = ROOT / "reports" / "ngc7479_diagnostic_bar_scoring_v01.md"
G = 4.30091e-6
RBAR_KPC = 10.2
GALAXIES = ["NGC 613", "NGC 4303", "NGC 4579", "NGC 5248", "NGC 7479"]


def profile(points: pd.DataFrame, radius_over_bar: np.ndarray) -> np.ndarray:
    q = points[points.point_origin.eq("vector_marker")].sort_values("physical_r_over_abar")
    x = q.physical_r_over_abar.to_numpy(float)
    y = q.physical_delta.to_numpy(float)
    return np.interp(radius_over_bar, x, y, left=0.0, right=0.0)


def rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def main() -> None:
    endpoint = pd.read_csv(DATA / "ngc7479_hi_rotation_endpoint_v01.csv")
    stellar = pd.read_csv(DATA / "ngc7479_stellar_velocity_field_v01.csv")
    gas = pd.read_csv(DATA / "ngc7479_hi_radial_proxy_v01.csv")
    morph = pd.read_csv(DATA / "coming_vector_marker_centers_v01.csv")
    radius = endpoint.radius_kpc_at_source_distance.to_numpy(float)
    observed = endpoint.vrot_hi_km_s.to_numpy(float)
    vstar = stellar.vstar_total_primary_km_s.to_numpy(float)
    rnorm = radius / RBAR_KPC
    rows = []
    summaries = []
    for floor, gas_floor in gas.groupby("grayscale_floor"):
        enclosed = np.interp(radius, gas_floor.radius_kpc, gas_floor.gas_enclosed_mass_msun_with_helium)
        vgas = np.sqrt(G * enclosed / radius)
        vbar = np.sqrt(vstar**2 + vgas**2)
        family_predictions = {}
        for galaxy in GALAXIES:
            delta = profile(morph[morph.galaxy.eq(galaxy)], rnorm)
            family_predictions[galaxy] = vbar * np.sqrt(1.0 + delta**2)
        matched = family_predictions["NGC 7479"]
        wrong_rmses = {g: rmse(observed, pred) for g, pred in family_predictions.items() if g != "NGC 7479"}
        summaries.append(
            {
                "grayscale_floor": floor,
                "rmse_newton_baryonic": rmse(observed, vbar),
                "rmse_matched_ngc7479": rmse(observed, matched),
                "rmse_wrong_family_mean": float(np.mean(list(wrong_rmses.values()))),
                "rmse_wrong_family_best": float(min(wrong_rmses.values())),
                "matched_beats_newton": rmse(observed, matched) < rmse(observed, vbar),
                "matched_beats_wrong_mean": rmse(observed, matched) < np.mean(list(wrong_rmses.values())),
                "matched_beats_best_wrong": rmse(observed, matched) < min(wrong_rmses.values()),
            }
        )
        delta_match = profile(morph[morph.galaxy.eq("NGC 7479")], rnorm)
        for i in range(len(radius)):
            rows.append(
                {
                    "grayscale_floor": floor,
                    "radius_kpc": radius[i],
                    "radius_over_bar": rnorm[i],
                    "vobs_hi_km_s": observed[i],
                    "vstar_km_s": vstar[i],
                    "vgas_spherical_proxy_km_s": vgas[i],
                    "vbar_km_s": vbar[i],
                    "delta_matched": delta_match[i],
                    "vpred_matched_km_s": matched[i],
                }
            )
    detail = pd.DataFrame(rows)
    summary = pd.DataFrame(summaries)
    detail.to_csv(DATA / "ngc7479_diagnostic_bar_scoring_points_v01.csv", index=False)
    summary.to_csv(DATA / "ngc7479_diagnostic_bar_scoring_summary_v01.csv", index=False)
    payload = {
        "schema": "tau_core_ngc7479_diagnostic_bar_scoring_v01",
        "status": "DIAGNOSTIC_ONLY_RASTER_GAS_PROXY_SCORE_COMPLETE",
        "formula": "v_pred^2 = v_bar^2 * (1 + Delta_source^2)",
        "fitted_parameters": 0,
        "uses_endpoint_to_select_morphology_scale_or_amplitude": False,
        "n_endpoint_points": len(endpoint),
        "n_gas_sensitivities": len(summary),
        "all_matched_beat_newton": bool(summary.matched_beats_newton.all()),
        "all_matched_beat_wrong_mean": bool(summary.matched_beats_wrong_mean.all()),
        "all_matched_beat_best_wrong": bool(summary.matched_beats_best_wrong.all()),
        "rmse_ranges": {
            "newton_baryonic": [float(summary.rmse_newton_baryonic.min()), float(summary.rmse_newton_baryonic.max())],
            "matched": [float(summary.rmse_matched_ngc7479.min()), float(summary.rmse_matched_ngc7479.max())],
            "wrong_mean": [float(summary.rmse_wrong_family_mean.min()), float(summary.rmse_wrong_family_mean.max())],
            "best_wrong": [float(summary.rmse_wrong_family_best.min()), float(summary.rmse_wrong_family_best.max())],
        },
        "strict_physical_score_allowed": False,
        "tau_morphology_detected": False,
        "channel_detected": False,
        "claim_boundary": "diagnostic scoring with publication-raster gas and spherical gas-force proxy; not endpoint validation",
    }
    (DATA / "ngc7479_diagnostic_bar_scoring_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    REPORT.write_text(
        "# NGC7479 diagnostic bar scoring v01\n\n"
        f"Status: `{payload['status']}`\n\n"
        "The zero-fit readout `v_pred^2=v_bar^2(1+Delta_source^2)` is scored against the independent ten-point H I endpoint under three raster-gas sensitivities and four wrong-family profiles. "
        f"RMSE ranges: Newton `{payload['rmse_ranges']['newton_baryonic']}`, matched `{payload['rmse_ranges']['matched']}`, wrong mean `{payload['rmse_ranges']['wrong_mean']}`, best wrong `{payload['rmse_ranges']['best_wrong']}` km/s.\n\n"
        "This is diagnostic only: the gas distribution comes from an unvalidated publication grayscale and its gravity uses a spherical enclosed-mass proxy. No Tau morphology or channel detection is claimed.\n"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
