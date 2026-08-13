#!/usr/bin/env python3
"""Replay the prefrozen modal-capacity operator on the numeric SINGS Halpha curve."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
SOURCE = ROOT / "data" / "external" / "literature" / "ngc4579_sings_halpha" / "ngc4579.dat"
REPORT = ROOT / "reports" / "ngc4579_sings_halpha_modal_capacity_replay_v01.md"
DISTANCE_MPC = 16.5
BAR_RADIUS_KPC = 3.62
GALAXIES = ["NGC 613", "NGC 4303", "NGC 4579", "NGC 5248", "NGC 7479"]


def basis(u: np.ndarray) -> np.ndarray:
    return np.column_stack((np.ones_like(u), u, 0.5 * (3.0 * u**2 - 1.0)))


def modal_response(points: pd.DataFrame, x_eval: np.ndarray) -> tuple[np.ndarray, dict]:
    q = points[points.point_origin.eq("vector_marker")].sort_values("physical_r_over_abar")
    x = q.physical_r_over_abar.to_numpy(float)
    y = q.physical_delta.to_numpy(float)
    sigma = 0.5 * (
        q.physical_delta_error_minus.to_numpy(float)
        + q.physical_delta_error_plus.to_numpy(float)
    )
    sigma = np.maximum(sigma, 1.0e-6)
    xmax = float(x[-1])
    design = basis(2.0 * x / xmax - 1.0)
    precision = np.diag(1.0 / sigma**2)
    covariance = np.linalg.inv(design.T @ precision @ design)
    coefficients = covariance @ design.T @ precision @ y
    variances = np.diag(covariance)
    capacities = coefficients**2 / np.maximum(coefficients**2 + variances, 1.0e-15)
    transmitted = basis(np.concatenate(([-1.0], 2.0 * x / xmax - 1.0))) @ (
        np.sqrt(capacities) * coefficients
    )
    density = transmitted**2
    x_nodes = np.concatenate(([0.0], x))
    total_capacity = float(np.mean(capacities))
    response = np.zeros_like(x_nodes)
    for i in range(1, len(x_nodes)):
        dx = x_nodes[i] - x_nodes[i - 1]
        density_mid = 0.5 * (density[i - 1] + density[i])
        if total_capacity > 0.0:
            response[i] = total_capacity - (total_capacity - response[i - 1]) * np.exp(
                -density_mid * dx / total_capacity
            )
    return np.interp(x_eval, x_nodes, response, left=0.0, right=response[-1]), {
        "coefficients": coefficients.tolist(),
        "coefficient_standard_errors": np.sqrt(variances).tolist(),
        "modal_capacities": capacities.tolist(),
        "total_capacity": total_capacity,
        "support_xmax": xmax,
    }


def rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def reduced_chi2(observed: np.ndarray, predicted: np.ndarray, error: np.ndarray) -> float:
    return float(np.mean(((observed - predicted) / error) ** 2))


def main() -> None:
    freeze = json.loads((DATA / "ngc4579_halpha_prospective_replication_freeze_v01.json").read_text())
    numeric_freeze = json.loads((DATA / "ngc4579_sings_halpha_rotation_extraction_freeze_v01.json").read_text())
    source = pd.read_csv(
        SOURCE, comment=";", sep=r"\s+",
        names=["radius_arcsec", "vobs_halpha_km_s", "side_error_km_s", "gipsy_error_km_s", "final_error_km_s"],
    )
    source["radius_kpc"] = source.radius_arcsec * DISTANCE_MPC * 1e3 / 206265.0
    source["post_bar_primary"] = source.radius_kpc >= BAR_RADIUS_KPC
    source["source_sides_individually_available"] = False
    source["side_disagreement_retained_in_final_error"] = True
    source.to_csv(DATA / "ngc4579_sings_halpha_rotation_endpoint_v01.csv", index=False)

    endpoint = source[source.post_bar_primary].copy()
    baryonic = pd.read_csv(DATA / "ngc4579_combined_baryonic_field_v01.csv")
    morphology = pd.read_csv(DATA / "coming_vector_marker_centers_v01.csv")
    radius = endpoint.radius_kpc.to_numpy(float)
    observed = endpoint.vobs_halpha_km_s.to_numpy(float)
    error = endpoint.final_error_km_s.to_numpy(float)
    x_eval = radius / BAR_RADIUS_KPC

    responses, modes = {}, {}
    for galaxy in GALAXIES:
        responses[galaxy], modes[galaxy] = modal_response(
            morphology[morphology.galaxy.eq(galaxy)], x_eval
        )

    velocity_columns = [c for c in baryonic.columns if c.startswith("vbar_alpha")]
    summaries, details = [], []
    for column in velocity_columns:
        vbar = np.interp(radius, baryonic.radius_kpc, baryonic[column])
        predictions = {g: vbar * np.sqrt(1.0 + responses[g]) for g in GALAXIES}
        matched = predictions["NGC 4579"]
        wrong_rmse = {g: rmse(observed, predictions[g]) for g in GALAXIES if g != "NGC 4579"}
        wrong_chi2 = {
            g: reduced_chi2(observed, predictions[g], error)
            for g in GALAXIES if g != "NGC 4579"
        }
        summaries.append({
            "baryonic_sensitivity": column,
            "rmse_newton_baryonic": rmse(observed, vbar),
            "rmse_matched_ngc4579": rmse(observed, matched),
            "rmse_wrong_family_mean": float(np.mean(list(wrong_rmse.values()))),
            "rmse_wrong_family_best": float(min(wrong_rmse.values())),
            "best_wrong_galaxy": min(wrong_rmse, key=wrong_rmse.get),
            "reduced_chi2_newton_baryonic": reduced_chi2(observed, vbar, error),
            "reduced_chi2_matched_ngc4579": reduced_chi2(observed, matched, error),
            "reduced_chi2_wrong_family_mean": float(np.mean(list(wrong_chi2.values()))),
            "matched_beats_newton": rmse(observed, matched) < rmse(observed, vbar),
            "matched_beats_wrong_mean": rmse(observed, matched) < np.mean(list(wrong_rmse.values())),
            "matched_beats_best_wrong": rmse(observed, matched) < min(wrong_rmse.values()),
        })
        for i, r in enumerate(radius):
            details.append({
                "baryonic_sensitivity": column, "radius_kpc": r,
                "radius_over_bar": x_eval[i], "vobs_halpha_km_s": observed[i],
                "final_error_km_s": error[i], "vbar_km_s": vbar[i],
                "matched_modal_response": responses["NGC 4579"][i],
                "vpred_matched_km_s": matched[i],
            })

    summary = pd.DataFrame(summaries)
    pd.DataFrame(details).to_csv(DATA / "ngc4579_sings_halpha_modal_capacity_points_v01.csv", index=False)
    summary.to_csv(DATA / "ngc4579_sings_halpha_modal_capacity_summary_v01.csv", index=False)
    ranges = lambda column: [float(summary[column].min()), float(summary[column].max())]
    result = {
        "schema": "tau_core_ngc4579_sings_halpha_modal_capacity_replay_v01",
        "status": "PROSPECTIVE_PREFROZEN_OPERATOR_REPLAY_CAVEATED_SOURCE_SIDE_AVERAGED",
        "target_freeze_status": freeze["status"],
        "numeric_route_freeze_status": numeric_freeze["status"],
        "source_sha256": "a0bc3ab76e5c55b1653132a03cce325cc33598eefa45afa266829104c86ffb04",
        "fitted_endpoint_parameters": 0,
        "n_source_points": int(len(source)), "n_post_bar_points": int(len(endpoint)),
        "post_bar_radius_range_kpc": [float(radius.min()), float(radius.max())],
        "source_sides_individually_available": False,
        "side_disagreement_retained_in_source_final_error": True,
        "source_mode_diagnostics": modes, "n_baryonic_sensitivities": int(len(summary)),
        "all_matched_beat_newton": bool(summary.matched_beats_newton.all()),
        "all_matched_beat_wrong_mean": bool(summary.matched_beats_wrong_mean.all()),
        "all_matched_beat_best_wrong": bool(summary.matched_beats_best_wrong.all()),
        "rmse_ranges_km_s": {
            "newton": ranges("rmse_newton_baryonic"),
            "matched": ranges("rmse_matched_ngc4579"),
            "wrong_mean": ranges("rmse_wrong_family_mean"),
            "best_wrong": ranges("rmse_wrong_family_best"),
        },
        "tau_morphology_detected": False, "physical_channel_detected": False,
        "claim_boundary": "independent-Halpha zero-fit operator replay with source-averaged sides; diagnostic evidence only, not a physical channel detection or Tau Core proof"
    }
    (DATA / "ngc4579_sings_halpha_modal_capacity_replay_v01.json").write_text(json.dumps(result, indent=2) + "\n")
    REPORT.write_text(
        "# NGC4579 SINGS Halpha modal-capacity replay v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The archived author table supplies `{len(source)}` numeric Halpha rotation points and `{len(endpoint)}` post-bar points. "
        "It preserves side disagreement as `side_error`/`final_error`, but does not publish the two side curves separately. "
        f"Across nine endpoint-blind baryonic sensitivities, RMSE ranges are Newton `{result['rmse_ranges_km_s']['newton']}`, "
        f"matched `{result['rmse_ranges_km_s']['matched']}`, wrong-family mean `{result['rmse_ranges_km_s']['wrong_mean']}`, "
        f"and best wrong `{result['rmse_ranges_km_s']['best_wrong']}` km/s.\n\n"
        "No endpoint parameter was fitted. This replay does not identify a physical channel.\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
