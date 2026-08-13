#!/usr/bin/env python3
"""Run the OSCC-1 water-filled capacity audit and corrected channel score."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import run_little_things_lightcone_capacity_score as old_capacity
import run_theory_completed_scale_tail_kernel_v02 as v02


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/little_things_oscc_capacity_scoring_v02.md"
BUDGET_FACTORS = (0.5, 1.0, 2.0)


def water_fill(gains: np.ndarray, budget: float) -> tuple[np.ndarray, float]:
    """Allocate a finite source budget across real Gaussian channel modes."""
    gains = np.asarray(gains, dtype=float)
    allocation = np.zeros_like(gains)
    positive = gains > 1.0e-14
    if budget <= 0.0 or not positive.any():
        return allocation, 0.0
    floors = 1.0 / gains[positive] ** 2
    low = float(floors.min())
    high = float(floors.max() + budget)
    for _ in range(200):
        level = 0.5 * (low + high)
        used = np.maximum(level - floors, 0.0).sum()
        if used > budget:
            high = level
        else:
            low = level
    level = 0.5 * (low + high)
    allocation[positive] = np.maximum(level - floors, 0.0)
    allocation *= budget / allocation.sum()
    return allocation, level


def rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def reduced_chi2(observed: np.ndarray, predicted: np.ndarray, error: np.ndarray) -> float:
    return float(np.mean(((observed - predicted) / error) ** 2))


def summarize(frame: pd.DataFrame) -> dict:
    dtpg = frame.rmse_oscc_v02 - frame.rmse_tpg_v6
    dv02 = frame.rmse_oscc_v02 - frame.rmse_v02
    return {
        "n_galaxies": int(len(frame)),
        "n_points": int(frame.n_points.sum()),
        "mean_rmse_km_s": {
            "oscc_v02": float(frame.rmse_oscc_v02.mean()),
            "v02": float(frame.rmse_v02.mean()),
            "tpg_v6": float(frame.rmse_tpg_v6.mean()),
            "mond": float(frame.rmse_mond.mean()),
        },
        "mean_paired_delta_km_s": {
            "oscc_minus_tpg": float(dtpg.mean()),
            "oscc_minus_v02": float(dv02.mean()),
        },
        "win_fraction": {
            "tpg_v6": float((dtpg < 0).mean()),
            "v02": float((dv02 < 0).mean()),
            "mond": float((frame.rmse_oscc_v02 < frame.rmse_mond).mean()),
        },
        "mean_reduced_chi2": {
            "oscc_v02": float(frame.chi2_oscc_v02.mean()),
            "v02": float(frame.chi2_v02.mean()),
            "tpg_v6": float(frame.chi2_tpg_v6.mean()),
        },
        "capacity_bits_per_profile_use": {
            "mean": float(frame.capacity_bits.mean()),
            "median": float(frame.capacity_bits.median()),
            "min": float(frame.capacity_bits.min()),
            "max": float(frame.capacity_bits.max()),
        },
        "water_filled_modes": {
            "mean": float(frame.active_modes.mean()),
            "min": int(frame.active_modes.min()),
            "max": int(frame.active_modes.max()),
        },
    }


def main() -> None:
    theory = json.loads(
        (DATA / "theory_completed_scale_tail_kernel_v02.json").read_text(encoding="utf-8")
    )
    eta = float(theory["eta"])
    points = pd.read_csv(DATA / "little_things_prospective_kernel_scored_points_v01.csv")
    audit = pd.read_csv(DATA / "little_things_baryonic_vector_extraction_audit_v01.csv")
    catalog = pd.read_csv(DATA / "little_things_prospective_scoring_freeze_v01.csv")
    allowed = set(audit.loc[audit.status.eq("pass"), "galaxy"])
    points = points[points.galaxy.isin(allowed) & points.prospective_name_freeze].copy()
    points = v02.add_channel_shape(points)
    points = points.merge(
        catalog[["galaxy", "distance_mpc", "hi_beam_fwhm_kpc"]],
        on="galaxy", how="left", validate="many_to_one",
    )
    points["v_v02"] = points.v_tpg_v6 * np.exp(0.5 * eta * points.phi_tail_bounded)
    if points[["hi_beam_fwhm_kpc", "velocity_error_km_s"]].isna().any().any():
        raise RuntimeError("OSCC-1 inputs contain missing beam or noise values")

    capacity_rows = []
    score_rows = []
    for galaxy, indices in points.groupby("galaxy", sort=True).groups.items():
        sub = points.loc[indices].sort_values("r")
        beam = old_capacity.gaussian_measurement_operator(
            sub.r.to_numpy(), float(sub.hi_beam_fwhm_kpc.iloc[0])
        )
        raw_correction = (sub.v_v02 - sub.v_tpg_v6).to_numpy()
        transported_correction = beam @ raw_correction
        prediction = sub.v_tpg_v6.to_numpy() + transported_correction
        full_smoothed = beam @ sub.v_v02.to_numpy()
        points.loc[sub.index, "v_oscc_v02"] = prediction
        points.loc[sub.index, "v_oscc_full_smoothing_control"] = full_smoothed

        # C_eff = beam times the exact local derivative dv_v02/dphi.
        derivative = 0.5 * eta * sub.v_v02.to_numpy()
        channel = beam @ np.diag(derivative)
        noise_inv_sqrt = np.diag(1.0 / sub.velocity_error_km_s.to_numpy())
        # G=I/n makes x^T G x the radial mean-square morphology load.
        source_cost_inv_sqrt = np.sqrt(len(sub)) * np.eye(len(sub))
        whitened = noise_inv_sqrt @ channel @ source_cost_inv_sqrt
        gains = np.linalg.svd(whitened, compute_uv=False)
        base_budget = float(np.mean(sub.phi_tail_bounded.to_numpy() ** 2))
        for factor in BUDGET_FACTORS:
            budget = factor * base_budget
            allocation, water_level = water_fill(gains, budget)
            capacity = float(0.5 * np.log2(1.0 + gains ** 2 * allocation).sum())
            capacity_rows.append({
                "galaxy": galaxy,
                "budget_factor": factor,
                "source_budget": budget,
                "capacity_bits_per_profile_use": capacity,
                "active_modes": int((allocation > 0).sum()),
                "sampled_modes": len(sub),
                "water_level": water_level,
                "max_whitened_gain": float(gains.max()),
                "min_whitened_gain": float(gains.min()),
            })

        observed = sub.velocity_km_s.to_numpy()
        error = sub.velocity_error_km_s.to_numpy()
        score_rows.append({
            "galaxy": galaxy,
            "inclination_deg": float(sub.inclination_deg.iloc[0]),
            "distance_mpc": float(sub.distance_mpc.iloc[0]),
            "hi_beam_fwhm_kpc": float(sub.hi_beam_fwhm_kpc.iloc[0]),
            "n_points": len(sub),
            "rmse_oscc_v02": rmse(observed, prediction),
            "rmse_v02": rmse(observed, sub.v_v02.to_numpy()),
            "rmse_tpg_v6": rmse(observed, sub.v_tpg_v6.to_numpy()),
            "rmse_mond": rmse(observed, sub.v_mond.to_numpy()),
            "rmse_full_smoothing_control": rmse(observed, full_smoothed),
            "chi2_oscc_v02": reduced_chi2(observed, prediction, error),
            "chi2_v02": reduced_chi2(observed, sub.v_v02.to_numpy(), error),
            "chi2_tpg_v6": reduced_chi2(observed, sub.v_tpg_v6.to_numpy(), error),
        })

    capacities = pd.DataFrame(capacity_rows)
    scores = pd.DataFrame(score_rows)
    nominal_capacity = capacities[capacities.budget_factor.eq(1.0)][
        ["galaxy", "capacity_bits_per_profile_use", "active_modes"]
    ].rename(columns={"capacity_bits_per_profile_use": "capacity_bits"})
    scores = scores.merge(nominal_capacity, on="galaxy", validate="one_to_one")
    primary = scores[scores.inclination_deg >= 40].copy()
    budget_sensitivity = {}
    for factor in BUDGET_FACTORS:
        sub = capacities[
            capacities.budget_factor.eq(factor) & capacities.galaxy.isin(primary.galaxy)
        ]
        budget_sensitivity[str(factor)] = {
            "mean_capacity_bits_per_profile_use": float(sub.capacity_bits_per_profile_use.mean()),
            "mean_active_modes": float(sub.active_modes.mean()),
        }

    result = {
        "schema": "little_things_oscc_capacity_scoring_v02",
        "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "law": "OSCC-1 classical real linear-Gaussian water-filled capacity",
        "scored_formula": "v_oscc=v_TPG+W_beam(v_v02-v_TPG)",
        "capacity_operator": "H=N^{-1/2} W_beam diag(dv_v02/dphi) G^{-1/2}",
        "noise_covariance": "diagonal published velocity_error_km_s squared; correlations unavailable",
        "source_cost": "G=I/n, so P=mean(phi_tail_bounded^2)",
        "eta": eta,
        "eta_refit": False,
        "little_things_opened_before_formula": True,
        "primary": summarize(primary),
        "budget_sensitivity": budget_sensitivity,
        "full_smoothing_control_mean_rmse_km_s": float(primary.rmse_full_smoothing_control.mean()),
        "capacity_modifies_prediction_directly": False,
        "physical_parent_cost_metric_derived": False,
        "correlated_path_noise_available": False,
        "time_operator_identified": False,
        "quantum_operator_identified": False,
        "claim_boundary": "OSCC-1-consistent opened-sample diagnostic using diagonal published errors and an operational source-cost convention; not a physical parent-capacity measurement or prospective endpoint",
    }
    points.to_csv(DATA / "little_things_oscc_capacity_scored_points_v02.csv", index=False)
    scores.to_csv(DATA / "little_things_oscc_capacity_scores_by_galaxy_v02.csv", index=False)
    capacities.to_csv(DATA / "little_things_oscc_capacity_modes_v02.csv", index=False)
    (DATA / "little_things_oscc_capacity_scoring_v02.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    p = result["primary"]
    REPORT.write_text(
        "# LITTLE THINGS OSCC-1 capacity scoring v02\n\n"
        f"Status: `{result['status']}`\n\n"
        "The score transports only the frozen v02-minus-TPG correction through the source-native "
        "H I beam. Capacity is computed separately from the noise-whitened local Jacobian with "
        "water filling; it is not reused as an attenuation factor.\n\n"
        f"On the 14-galaxy primary lane, mean RMSE is `{p['mean_rmse_km_s']['oscc_v02']:.3f} "
        f"km/s`, versus `{p['mean_rmse_km_s']['v02']:.3f}` for raw v02 and "
        f"`{p['mean_rmse_km_s']['tpg_v6']:.3f}` for TPG. Mean OSCC-minus-TPG is "
        f"`{p['mean_paired_delta_km_s']['oscc_minus_tpg']:+.3f} km/s`; mean OSCC-minus-v02 "
        f"is `{p['mean_paired_delta_km_s']['oscc_minus_v02']:+.3f} km/s`. The nominal operational "
        f"capacity is `{p['capacity_bits_per_profile_use']['mean']:.3f}` bits per profile use on "
        f"average, with `{p['water_filled_modes']['mean']:.2f}` active modes.\n\n"
        "The numerical capacity depends on the declared `G=I/n` source-cost convention and a "
        "diagonal noise approximation. It is not yet a parent-derived physical capacity.\n",
        encoding="utf-8",
    )
    print(result["status"], json.dumps(result["primary"], sort_keys=True))


if __name__ == "__main__":
    main()
