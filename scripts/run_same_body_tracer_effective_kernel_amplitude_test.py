#!/usr/bin/env python3
"""Fit amplitude-only effective Tau kernels to same-body H I and Halpha tracers."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
sys.path.insert(0, str(ROOT / "scripts"))
import run_s4g75_promoted_kernel_endpoint_stress_test as promoted  # noqa: E402
import run_source_native_readout_formula_endpoint as source  # noqa: E402


def beta_fit(kernel: np.ndarray, carrier: np.ndarray, velocity: np.ndarray) -> float:
    target = velocity**2 - carrier**2
    return float(kernel @ target / (kernel @ kernel))


def fit_summary(kernel, carrier, velocity):
    beta = beta_fit(kernel, carrier, velocity)
    prediction = np.sqrt(np.maximum(carrier**2 + beta * kernel, 0))
    loo = []
    for index in range(len(kernel)):
        keep = np.arange(len(kernel)) != index
        loo.append(beta_fit(kernel[keep], carrier[keep], velocity[keep]))
    loo = np.asarray(loo)
    jackknife_se = float(np.sqrt((len(loo) - 1) / len(loo) * np.sum((loo - loo.mean()) ** 2)))
    return {
        "beta_delta_v2_amplitude": beta,
        "jackknife_se": jackknife_se,
        "jackknife_min": float(loo.min()),
        "jackknife_max": float(loo.max()),
        "rmse_km_s": float(np.sqrt(np.mean((velocity - prediction) ** 2))),
    }


def kernel_profile(galaxy: str, radii_kpc: np.ndarray):
    points, _ = source.load_points()
    points = promoted.apply_promoted_observables(points)
    points = source.add_bridge_formula_kernels(points)
    sub = points.loc[points.galaxy.eq(galaxy)].sort_values("r")
    family = sub.formula_family.iloc[0]
    return (
        family,
        np.interp(radii_kpc, sub.r, sub[f"kernel_{family}"]),
        np.interp(radii_kpc, sub.r, sub.v_v6),
    )


def difference(a, b):
    delta = a["beta_delta_v2_amplitude"] - b["beta_delta_v2_amplitude"]
    sigma = math.hypot(a["jackknife_se"], b["jackknife_se"])
    return {"delta_beta": delta, "combined_jackknife_sigma": sigma,
            "absolute_z": abs(delta) / sigma if sigma > 0 else None}


def one_parameter_loo(delta_v2: np.ndarray, basis: np.ndarray) -> dict[str, float]:
    predictions = np.empty(len(delta_v2))
    for index in range(len(delta_v2)):
        keep = np.arange(len(delta_v2)) != index
        coefficient = float(basis[keep] @ delta_v2[keep] / (basis[keep] @ basis[keep]))
        predictions[index] = coefficient * basis[index]
    return {"loo_rmse_v2": float(np.sqrt(np.mean((delta_v2 - predictions) ** 2)))}


def carrier_plus_kernel_loo(delta_v2, carrier_basis, kernel_basis):
    design = np.column_stack([carrier_basis, kernel_basis])
    predictions = np.empty(len(delta_v2))
    kernel_coefficients = []
    for index in range(len(delta_v2)):
        keep = np.arange(len(delta_v2)) != index
        coefficient = np.linalg.lstsq(design[keep], delta_v2[keep], rcond=None)[0]
        predictions[index] = design[index] @ coefficient
        kernel_coefficients.append(float(coefficient[1]))
    scaled = design / np.linalg.norm(design, axis=0)
    condition = float(np.linalg.cond(scaled))
    return {
        "loo_rmse_v2": float(np.sqrt(np.mean((delta_v2 - predictions) ** 2))),
        "normalized_design_condition_number": condition,
        "loo_kernel_coefficient_min": min(kernel_coefficients),
        "loo_kernel_coefficient_max": max(kernel_coefficients),
        "loo_kernel_coefficient_same_sign": (
            min(kernel_coefficients) > 0 or max(kernel_coefficients) < 0
        ),
    }


def shape_controls(kernel, carrier, hi, ha):
    delta = ha**2 - hi**2
    controls = {
        "tau_kernel": one_parameter_loo(delta, kernel),
        "constant_delta_v2": one_parameter_loo(delta, np.ones_like(kernel)),
        "multiplicative_carrier_v2": one_parameter_loo(delta, carrier**2),
    }
    winner = min(controls, key=lambda name: controls[name]["loo_rmse_v2"])
    profiled = carrier_plus_kernel_loo(delta, carrier**2, kernel)
    carrier_rmse = controls["multiplicative_carrier_v2"]["loo_rmse_v2"]
    profiled["improvement_over_carrier_only"] = carrier_rmse - profiled["loo_rmse_v2"]
    profiled["proportional_improvement_over_carrier_only"] = (
        (carrier_rmse - profiled["loo_rmse_v2"]) / carrier_rmse
    )
    profiled["kernel_after_scale_candidate"] = (
        profiled["improvement_over_carrier_only"] > 0
        and profiled["loo_kernel_coefficient_same_sign"]
        and profiled["normalized_design_condition_number"] < 30
    )
    return {"models": controls, "best_one_parameter_shape": winner,
            "tau_kernel_shape_wins": winner == "tau_kernel",
            "carrier_plus_tau_kernel": profiled}


def main() -> None:
    results = {}

    g = "NGC3726"
    rows = pd.read_csv(DATA / "ngc3726_hi_halpha_channel_preflight_v01.csv").sort_values("radius_arcsec")
    distance = 18.0
    radii = rows.radius_arcsec.to_numpy() * distance * 1000 / 206265
    family, kernel, carrier = kernel_profile(g, radii)
    hi = 0.5 * (rows.hi_approaching_vrot_km_s.to_numpy() + rows.hi_receding_vrot_km_s.to_numpy())
    ha = 0.5 * (rows.halpha_approaching_vrot_km_s.to_numpy() + rows.halpha_receding_vrot_km_s.to_numpy())
    hi_fit = fit_summary(kernel, carrier, hi)
    ha_fit = fit_summary(kernel, carrier, ha)
    results[g] = {
        "formula_family": family, "n_common_radii": len(radii),
        "radius_kpc_min": float(radii.min()), "radius_kpc_max": float(radii.max()),
        "hi": hi_fit, "halpha": ha_fit, "halpha_minus_hi": difference(ha_fit, hi_fit),
        "shape_controls": shape_controls(kernel, carrier, hi, ha),
    }

    g = "NGC4559"
    rows = pd.read_csv(DATA / "ngc4559_halogas_hi_halpha_replication_v01.csv")
    geometry = json.loads((DATA / "ngc4559_halogas_extraction_freeze_v01.json").read_text())["source_geometry"]
    distance = 9.0
    radii_arcsec = np.sort(rows.radius_arcsec.unique())
    radii = radii_arcsec * distance * 1000 / 206265
    family, kernel, carrier = kernel_profile(g, radii)
    ha_i = math.radians(float(geometry["ghasp"]["kinematic_inclination_deg"]))
    hi_i = math.radians(float(geometry["hi"]["inclination_deg"]))
    variants = {}
    for resolution in ("HR", "LR"):
        sub = rows.loc[rows.resolution.eq(resolution)].sort_values("radius_arcsec")
        hi = 0.5 * (
            sub.hi_approaching_u_los_km_s.to_numpy() + sub.hi_receding_u_los_km_s.to_numpy()
        ) / math.sin(hi_i)
        ha = 0.5 * (
            sub.halpha_approaching_vrot_km_s.to_numpy() + sub.halpha_receding_vrot_km_s.to_numpy()
        )
        hi_fit = fit_summary(kernel, carrier, hi)
        ha_fit = fit_summary(kernel, carrier, ha)
        variants[resolution] = {
            "hi": hi_fit, "halpha": ha_fit,
            "halpha_minus_hi": difference(ha_fit, hi_fit),
            "projection_check_halpha_sin_i": math.sin(ha_i),
            "shape_controls": shape_controls(kernel, carrier, hi, ha),
        }
    results[g] = {
        "formula_family": family, "n_common_radii": len(radii),
        "radius_kpc_min": float(radii.min()), "radius_kpc_max": float(radii.max()),
        "resolutions": variants,
        "hi_resolution_beta_difference": (
            variants["HR"]["hi"]["beta_delta_v2_amplitude"]
            - variants["LR"]["hi"]["beta_delta_v2_amplitude"]
        ),
    }

    z_values = [
        results["NGC3726"]["halpha_minus_hi"]["absolute_z"],
        results["NGC4559"]["resolutions"]["HR"]["halpha_minus_hi"]["absolute_z"],
        results["NGC4559"]["resolutions"]["LR"]["halpha_minus_hi"]["absolute_z"],
    ]
    candidate = all(value is not None and value >= 2 for value in z_values)
    kernel_shape_wins = all([
        results["NGC3726"]["shape_controls"]["tau_kernel_shape_wins"],
        results["NGC4559"]["resolutions"]["HR"]["shape_controls"]["tau_kernel_shape_wins"],
        results["NGC4559"]["resolutions"]["LR"]["shape_controls"]["tau_kernel_shape_wins"],
    ])
    after_scale_candidate = all([
        results["NGC3726"]["shape_controls"]["carrier_plus_tau_kernel"]["kernel_after_scale_candidate"],
        results["NGC4559"]["resolutions"]["HR"]["shape_controls"]["carrier_plus_tau_kernel"]["kernel_after_scale_candidate"],
        results["NGC4559"]["resolutions"]["LR"]["shape_controls"]["carrier_plus_tau_kernel"]["kernel_after_scale_candidate"],
    ])
    embedded_candidate = candidate and kernel_shape_wins
    payload = {
        "schema": "same_body_tracer_effective_kernel_amplitude_test_v01",
        "status": (
            "DIAGNOSTIC_KERNEL_EMBEDDED_TRACER_CHANNEL_CANDIDATE"
            if embedded_candidate else
            "DIAGNOSTIC_TRACER_AMPLITUDE_DIFFERENCE_NOT_KERNEL_SPECIFIC"
            if candidate else "DIAGNOSTIC_TRACER_KERNEL_AMPLITUDE_DIFFERENCE_NOT_REPLICATED"
        ),
        "model": "fixed source kernel shape and TPG carrier; one beta per tracer",
        "galaxies": results,
        "two_sigma_difference_in_all_galaxy_resolution_tests": candidate,
        "tau_kernel_shape_wins_all_equal_parameter_controls": kernel_shape_wins,
        "kernel_embedded_channel_information_candidate": embedded_candidate,
        "kernel_after_multiplicative_scale_candidate_all_tests": after_scale_candidate,
        "physical_channel_detected": False,
        "limitations": [
            "jackknife captures radial leverage but not full velocity covariance",
            "only amplitude is varied; radial dilation and onset shift are fixed",
            "H I and Halpha line formation, pressure support, beam and geometry remain conventional alternatives",
            "small two-galaxy diagnostic",
        ],
        "claim_boundary": (
            "same-body tracer effective-kernel amplitude diagnostic; a difference is not a "
            "physical observer-channel detection without full covariance and independent replication"
        ),
    }
    (DATA / "same_body_tracer_effective_kernel_amplitude_test_v01.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["status"])


if __name__ == "__main__":
    main()
