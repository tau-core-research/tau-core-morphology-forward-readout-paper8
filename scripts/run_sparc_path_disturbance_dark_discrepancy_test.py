#!/usr/bin/env python3
"""Test incremental foreground-path information about outer mass discrepancy."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TAU_ROOT = ROOT.parent
DATA = ROOT / "data/derived"
TARGET = TAU_ROOT / (
    "tau-core-theory/source_material/tau_core_foundations/numerical_checks/"
    "tau_core_galactic_clock_channel_reparameterization_v01_galaxies.csv"
)
N_PERMUTATIONS = 2000
SEED = 20260711


def standardize(values: np.ndarray, train: np.ndarray) -> np.ndarray:
    values = values.astype(float, copy=True)
    med = np.nanmedian(values[train], axis=0)
    med = np.where(np.isfinite(med), med, 0.0)
    missing = np.where(~np.isfinite(values))
    values[missing] = med[missing[1]]
    mean = values[train].mean(axis=0)
    scale = values[train].std(axis=0)
    return (values - mean) / np.where(scale > 1e-12, scale, 1.0)


def fold_prediction(x: np.ndarray, y: np.ndarray, folds: np.ndarray) -> np.ndarray:
    result = np.empty(len(y))
    for fold in sorted(np.unique(folds)):
        test = folds == fold
        train = ~test
        z = standardize(x, train)
        a = np.column_stack([np.ones(train.sum()), z[train]])
        b = np.column_stack([np.ones(test.sum()), z[test]])
        penalty = np.eye(a.shape[1]); penalty[0, 0] = 0
        beta = np.linalg.solve(a.T @ a + penalty, a.T @ y[train])
        result[test] = b @ beta
    return result


def main() -> None:
    features = pd.read_csv(DATA / "s4g_stellar_asymmetry_attribution_source_v01.csv")
    atlas = pd.read_csv(DATA / "sparc_lightcone_disturbance_atlas_v02.csv")
    target = pd.read_csv(TARGET)[["galaxy", "outer3_required_clock_factor_median"]]
    joined = features.merge(
        atlas[["galaxy", "source_disturbance_class", "observation_disturbance_class",
               "foreground_candidate_count", "foreground_inverse_angle_weight",
               "background_redshift_control_count", "stellar_crowding_control_count"]],
        on="galaxy", validate="one_to_one",
    ).merge(target, on="galaxy", validate="one_to_one")
    joined = joined.loc[joined.outer3_required_clock_factor_median.gt(0)].sort_values("galaxy").reset_index(drop=True)
    baseline_columns = [
        "sparc_t_type", "log_distance_mpc", "inclination_deg", "log_l36",
        "log_reff_kpc", "log_sbeff", "log_rdisk_kpc", "log_sbdisk", "log_mhi",
        "log_rhi_kpc", "asymmetry_3p6", "asymmetry_4p5",
        "background_redshift_control_count", "stellar_crowding_control_count",
    ]
    baseline = joined[baseline_columns].to_numpy(float)
    class_dummies = pd.get_dummies(
        joined[["source_disturbance_class", "observation_disturbance_class"]],
        dtype=float,
    ).to_numpy()
    baseline = np.column_stack([baseline, class_dummies])
    path = np.column_stack([
        joined.foreground_candidate_count.to_numpy(float),
        np.log1p(joined.foreground_inverse_angle_weight.to_numpy(float)),
    ])
    y = -2 * np.log(joined.outer3_required_clock_factor_median.to_numpy(float))
    folds = joined.fold.to_numpy(int)
    pred_base = fold_prediction(baseline, y, folds)
    pred_path = fold_prediction(np.column_stack([baseline, path]), y, folds)
    mse_base = float(np.mean((y - pred_base) ** 2))
    mse_path = float(np.mean((y - pred_path) ** 2))
    observed = mse_base - mse_path
    rng = np.random.default_rng(SEED)
    null = np.empty(N_PERMUTATIONS)
    for index in range(N_PERMUTATIONS):
        shuffled = path[rng.permutation(len(path))]
        prediction = fold_prediction(np.column_stack([baseline, shuffled]), y, folds)
        null[index] = mse_base - float(np.mean((y - prediction) ** 2))
    p_value = float((1 + np.sum(null >= observed)) / (N_PERMUTATIONS + 1))
    q95 = float(np.quantile(null, 0.95))
    candidate = observed > 0 and p_value <= 0.05 and observed > q95
    payload = {
        "schema": "sparc_path_disturbance_dark_discrepancy_test_v01",
        "status": (
            "RETROSPECTIVE_PATH_PROXY_INCREMENTAL_SIGNAL_PASS_PRELIMINARY"
            if candidate else "RETROSPECTIVE_PATH_PROXY_INCREMENTAL_SIGNAL_FAIL"
        ),
        "n_galaxies": len(joined),
        "n_folds": len(np.unique(folds)),
        "target": "log_outer3_mass_discrepancy",
        "baseline_oof_mse": mse_base,
        "baseline_plus_path_oof_mse": mse_path,
        "mse_reduction": observed,
        "proportional_mse_reduction": observed / mse_base,
        "shuffle": {"n": N_PERMUTATIONS, "seed": SEED, "p": p_value, "q95": q95},
        "path_features": ["foreground_candidate_count", "log1p_foreground_inverse_angle_weight"],
        "controls": baseline_columns + ["source_disturbance_class", "observation_disturbance_class"],
        "path_information_candidate": candidate,
        "physical_channel_detected": False,
        "claim_boundary": (
            "retrospective heterogeneous-SIMBAD proxy test; even a pass is incremental catalogue "
            "path information, not a complete lightcone integral or physical channel detection"
        ),
    }
    (DATA / "sparc_path_disturbance_dark_discrepancy_test_v01.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    pd.DataFrame({
        "galaxy": joined.galaxy, "fold": folds, "log_outer3_mass_discrepancy": y,
        "baseline_prediction": pred_base, "baseline_plus_path_prediction": pred_path,
    }).to_csv(DATA / "sparc_path_disturbance_dark_discrepancy_oof_v01.csv", index=False)
    print(payload["status"])


if __name__ == "__main__":
    main()
