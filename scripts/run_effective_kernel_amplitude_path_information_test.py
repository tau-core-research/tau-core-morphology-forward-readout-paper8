#!/usr/bin/env python3
"""Test path information in galaxy-specific effective Tau-kernel amplitudes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
N_PERMUTATIONS = 2000
SEED = 20260711
sys.path.insert(0, str(ROOT / "scripts"))
import run_s4g75_promoted_kernel_endpoint_stress_test as promoted  # noqa: E402
import run_source_native_readout_formula_endpoint as source  # noqa: E402


def standardize(x, train):
    x = x.astype(float, copy=True)
    med = np.nanmedian(x[train], axis=0)
    med = np.where(np.isfinite(med), med, 0)
    missing = np.where(~np.isfinite(x)); x[missing] = med[missing[1]]
    mean = x[train].mean(axis=0); scale = x[train].std(axis=0)
    return (x - mean) / np.where(scale > 1e-12, scale, 1)


def oof(x, y, folds):
    prediction = np.empty(len(y))
    for fold in sorted(np.unique(folds)):
        test = folds == fold; train = ~test
        z = standardize(x, train)
        a = np.column_stack([np.ones(train.sum()), z[train]])
        b = np.column_stack([np.ones(test.sum()), z[test]])
        penalty = np.eye(a.shape[1]); penalty[0, 0] = 0
        beta = np.linalg.solve(a.T @ a + penalty, a.T @ y[train])
        prediction[test] = b @ beta
    return prediction


def main() -> None:
    points, _ = source.load_points()
    points = promoted.apply_promoted_observables(points)
    points = source.add_bridge_formula_kernels(points)
    beta_rows = []
    for galaxy, sub in points.groupby("galaxy"):
        family = sub.formula_family.iloc[0]
        kernel = sub[f"kernel_{family}"].to_numpy(float)
        target = (sub.vobs**2 - sub.v_v6**2).to_numpy(float)
        beta_rows.append({
            "galaxy": galaxy, "formula_family": family,
            "effective_beta": float(kernel @ target / (kernel @ kernel)),
            "kernel_rms": float(np.sqrt(np.mean(kernel**2))),
            "carrier_v2_rms": float(np.sqrt(np.mean(sub.v_v6.to_numpy(float)**4))),
            "n_points": len(sub),
        })
    betas = pd.DataFrame(beta_rows)
    betas["signed_fractional_kernel_load"] = (
        betas.effective_beta * betas.kernel_rms / betas.carrier_v2_rms
    )
    features = pd.read_csv(DATA / "s4g_stellar_asymmetry_attribution_source_v01.csv")
    atlas = pd.read_csv(DATA / "sparc_lightcone_disturbance_atlas_v02.csv")[[
        "galaxy", "source_disturbance_class", "observation_disturbance_class",
        "path_disturbance_class", "foreground_candidate_count",
        "foreground_inverse_angle_weight",
    ]]
    joined = features.merge(atlas, on="galaxy", validate="one_to_one").merge(
        betas, on="galaxy", validate="one_to_one"
    ).sort_values("galaxy").reset_index(drop=True)
    numeric = ["sparc_t_type", "log_distance_mpc", "inclination_deg", "log_l36",
               "log_reff_kpc", "log_sbeff", "log_rdisk_kpc", "log_sbdisk", "log_mhi",
               "log_rhi_kpc", "asymmetry_3p6", "asymmetry_4p5"]
    base = joined[numeric].to_numpy(float)
    dummies = pd.get_dummies(joined[["formula_family", "source_disturbance_class",
                                     "observation_disturbance_class"]], dtype=float).to_numpy()
    base = np.column_stack([base, dummies])
    path = np.column_stack([joined.foreground_candidate_count.to_numpy(float),
                            np.log1p(joined.foreground_inverse_angle_weight.to_numpy(float))])
    y = joined.effective_beta.to_numpy(float)
    scale = float(np.median(np.abs(y))) or 1.0
    y = y / scale
    folds = joined.fold.to_numpy(int)
    pred_base = oof(base, y, folds)
    pred_path = oof(np.column_stack([base, path]), y, folds)
    mse_base = float(np.mean((y - pred_base)**2)); mse_path = float(np.mean((y - pred_path)**2))
    observed = mse_base - mse_path
    rng = np.random.default_rng(SEED); null = np.empty(N_PERMUTATIONS)
    for index in range(N_PERMUTATIONS):
        shuffled = path[rng.permutation(len(path))]
        pred = oof(np.column_stack([base, shuffled]), y, folds)
        null[index] = mse_base - float(np.mean((y - pred)**2))
    p = float((1 + np.sum(null >= observed)) / (N_PERMUTATIONS + 1))
    q95 = float(np.quantile(null, 0.95))
    candidate = observed > 0 and p <= 0.05 and observed > q95
    payload = {
        "schema": "effective_kernel_amplitude_path_information_test_v01",
        "status": "RETROSPECTIVE_EFFECTIVE_BETA_PATH_INFORMATION_PASS" if candidate else
                  "RETROSPECTIVE_EFFECTIVE_BETA_PATH_INFORMATION_FAIL",
        "n_galaxies": len(joined), "n_folds": len(np.unique(folds)),
        "target": "galaxy-specific effective beta for fixed matched Tau kernel shape",
        "normalization": "beta divided by population median absolute beta",
        "baseline_oof_mse": mse_base, "baseline_plus_path_oof_mse": mse_path,
        "mse_reduction": observed, "proportional_mse_reduction": observed / mse_base,
        "shuffle": {"n": N_PERMUTATIONS, "seed": SEED, "p": p, "q95": q95},
        "path_information_candidate": candidate, "physical_channel_detected": False,
        "claim_boundary": (
            "retrospective endpoint-derived beta attribution; path proxy incomplete and beta "
            "combines body mismatch, calibration, tracer transfer and any channel response"
        ),
    }
    (DATA / "effective_kernel_amplitude_path_information_test_v01.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    joined[["galaxy", "fold", "formula_family", "effective_beta",
            "kernel_rms", "carrier_v2_rms", "signed_fractional_kernel_load",
            "path_disturbance_class", "source_disturbance_class",
            "observation_disturbance_class"]].to_csv(
        DATA / "effective_kernel_amplitude_path_by_galaxy_v01.csv", index=False
    )
    print(payload["status"])


if __name__ == "__main__":
    main()
