#!/usr/bin/env python3
"""Audit robustness of the preliminary path/effective-beta information signal."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
N = 2000
SEED = 20260712
sys.path.insert(0, str(ROOT / "scripts"))
from run_effective_kernel_amplitude_path_information_test import oof  # noqa: E402


def score(base, path, y, folds, rng):
    pred_base = oof(base, y, folds)
    pred_path = oof(np.column_stack([base, path]), y, folds)
    mse_base = float(np.mean((y - pred_base) ** 2))
    mse_path = float(np.mean((y - pred_path) ** 2))
    observed = mse_base - mse_path
    null = np.empty(N)
    for index in range(N):
        shuffled = path[rng.permutation(len(path))]
        prediction = oof(np.column_stack([base, shuffled]), y, folds)
        null[index] = mse_base - float(np.mean((y - prediction) ** 2))
    return {
        "n": len(y), "mse_reduction": observed,
        "proportional_mse_reduction": observed / mse_base,
        "shuffle_p": float((1 + np.sum(null >= observed)) / (N + 1)),
        "null_q95": float(np.quantile(null, 0.95)),
    }


def main() -> None:
    betas = pd.read_csv(DATA / "effective_kernel_amplitude_path_by_galaxy_v01.csv")
    features = pd.read_csv(DATA / "s4g_stellar_asymmetry_attribution_source_v01.csv")
    atlas = pd.read_csv(DATA / "sparc_lightcone_disturbance_atlas_v02.csv")[[
        "galaxy", "source_disturbance_class", "observation_disturbance_class",
        "foreground_candidate_count", "foreground_inverse_angle_weight",
    ]]
    joined = features.merge(atlas, on="galaxy", validate="one_to_one").merge(
        betas[["galaxy", "formula_family", "effective_beta", "signed_fractional_kernel_load"]],
        on="galaxy", validate="one_to_one"
    ).sort_values("galaxy").reset_index(drop=True)
    numeric = ["sparc_t_type", "log_distance_mpc", "inclination_deg", "log_l36",
               "log_reff_kpc", "log_sbeff", "log_rdisk_kpc", "log_sbdisk", "log_mhi",
               "log_rhi_kpc", "asymmetry_3p6", "asymmetry_4p5"]
    base_num = joined[numeric].to_numpy(float)
    dummies = pd.get_dummies(joined[["formula_family", "source_disturbance_class",
                                     "observation_disturbance_class"]], dtype=float).to_numpy()
    base = np.column_stack([base_num, dummies])
    path = np.column_stack([joined.foreground_candidate_count.to_numpy(float),
                            np.log1p(joined.foreground_inverse_angle_weight.to_numpy(float))])
    raw = joined.effective_beta.to_numpy(float)
    median = float(np.median(np.abs(raw))) or 1
    q05, q95 = np.quantile(raw, [0.05, 0.95])
    variants = {
        "raw_scaled": (np.ones(len(joined), dtype=bool), raw / median),
        "signed_log": (np.ones(len(joined), dtype=bool), np.sign(raw) * np.log1p(np.abs(raw) / median)),
        "winsor_5_95": (np.ones(len(joined), dtype=bool), np.clip(raw, q05, q95) / median),
        "exclude_compact_family": (joined.formula_family.ne("K_compact_finite").to_numpy(), raw / median),
        "scale_invariant_fractional_kernel_load": (
            np.ones(len(joined), dtype=bool),
            joined.signed_fractional_kernel_load.to_numpy(float),
        ),
    }
    results = {}
    for offset, (name, (mask, target)) in enumerate(variants.items()):
        results[name] = score(base[mask], path[mask], target[mask], joined.fold.to_numpy(int)[mask],
                              np.random.default_rng(SEED + offset))
    robust = all(result["mse_reduction"] > 0 and result["shuffle_p"] <= 0.05
                 for result in results.values())
    payload = {
        "schema": "effective_kernel_amplitude_path_robustness_v01",
        "status": "EFFECTIVE_BETA_PATH_SIGNAL_ROBUST" if robust else
                  "EFFECTIVE_BETA_PATH_SIGNAL_NOT_ROBUST_TO_TARGET_SCALE_AND_FAMILY",
        "variants": results,
        "all_variants_positive_and_p_le_0p05": robust,
        "path_information_candidate_promoted": robust,
        "physical_channel_detected": False,
        "claim_boundary": "retrospective robustness audit; heterogeneous path proxy and endpoint-derived beta",
    }
    (DATA / "effective_kernel_amplitude_path_robustness_v01.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["status"])


if __name__ == "__main__":
    main()
