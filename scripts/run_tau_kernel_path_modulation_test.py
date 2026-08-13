#!/usr/bin/env python3
"""Test whether foreground-path class modulates frozen Tau-kernel performance."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
N_PERMUTATIONS = 10000
SEED = 20260711


def main() -> None:
    scores = pd.read_csv(DATA / "s4g75_promoted_kernel_endpoint_scores.csv")
    atlas = pd.read_csv(DATA / "sparc_lightcone_disturbance_atlas_v02.csv")
    joined = scores.merge(
        atlas.drop(columns=["split"]), on="galaxy", validate="one_to_one"
    )
    joined["kernel_gain_vs_tpg"] = joined.rmse_tpg_v6 - joined.rmse_matched_family
    joined["kernel_gain_vs_wrong"] = joined.rmse_wrong_family_mean - joined.rmse_matched_family
    joined["path_disturbed"] = joined.path_disturbance_class.ne("P0")
    clean = joined.loc[~joined.path_disturbed]
    disturbed = joined.loc[joined.path_disturbed]

    observed = float(disturbed.kernel_gain_vs_tpg.mean() - clean.kernel_gain_vs_tpg.mean())
    rng = np.random.default_rng(SEED)
    labels = joined.path_disturbed.to_numpy()
    gains = joined.kernel_gain_vs_tpg.to_numpy()
    null = np.empty(N_PERMUTATIONS)
    for index in range(N_PERMUTATIONS):
        shuffled = rng.permutation(labels)
        null[index] = gains[shuffled].mean() - gains[~shuffled].mean()
    two_sided_p = float((1 + np.sum(np.abs(null) >= abs(observed))) / (N_PERMUTATIONS + 1))
    wins = joined.matched_beats_tpg_v6.astype(bool)
    table = [
        [int((wins & labels).sum()), int((~wins & labels).sum())],
        [int((wins & ~labels).sum()), int((~wins & ~labels).sum())],
    ]
    _, fisher_p = fisher_exact(table, alternative="two-sided")
    _, mw_p = mannwhitneyu(
        disturbed.kernel_gain_vs_tpg,
        clean.kernel_gain_vs_tpg,
        alternative="two-sided",
    )
    candidate = two_sided_p <= 0.05 and fisher_p <= 0.05
    payload = {
        "schema": "tau_kernel_path_modulation_test_v01",
        "status": (
            "RETROSPECTIVE_TAU_KERNEL_PATH_MODULATION_CANDIDATE"
            if candidate else "RETROSPECTIVE_TAU_KERNEL_PATH_MODULATION_NOT_DETECTED"
        ),
        "n_galaxies": len(joined),
        "n_path_clean_p0": len(clean),
        "n_path_disturbed_p1_p3": len(disturbed),
        "kernel_gain_definition": "rmse_tpg_v6 - rmse_matched_family; positive favors Tau kernel",
        "clean": {
            "mean_gain_vs_tpg": float(clean.kernel_gain_vs_tpg.mean()),
            "median_gain_vs_tpg": float(clean.kernel_gain_vs_tpg.median()),
            "matched_beats_tpg_fraction": float(clean.matched_beats_tpg_v6.mean()),
            "matched_beats_wrong_fraction": float(clean.matched_beats_wrong_mean.mean()),
            "median_gain_vs_wrong_kernel": float(clean.kernel_gain_vs_wrong.median()),
        },
        "path_disturbed": {
            "mean_gain_vs_tpg": float(disturbed.kernel_gain_vs_tpg.mean()),
            "median_gain_vs_tpg": float(disturbed.kernel_gain_vs_tpg.median()),
            "matched_beats_tpg_fraction": float(disturbed.matched_beats_tpg_v6.mean()),
            "matched_beats_wrong_fraction": float(disturbed.matched_beats_wrong_mean.mean()),
            "median_gain_vs_wrong_kernel": float(disturbed.kernel_gain_vs_wrong.median()),
        },
        "difference_disturbed_minus_clean_mean_gain": observed,
        "permutation": {"n": N_PERMUTATIONS, "seed": SEED, "two_sided_p": two_sided_p},
        "mann_whitney_two_sided_p": float(mw_p),
        "fisher_win_table": table,
        "fisher_two_sided_p": float(fisher_p),
        "path_modulation_candidate": candidate,
        "physical_channel_detected": False,
        "claim_boundary": (
            "retrospective kernel-performance stratification with seven non-P0 systems; "
            "SIMBAD path proxy incomplete and kernel endpoint is a stress test, not validation"
        ),
    }
    (DATA / "tau_kernel_path_modulation_test_v01.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    joined[["galaxy", "split", "formula_family", "path_disturbance_class",
            "source_disturbance_class", "observation_disturbance_class",
            "kernel_gain_vs_tpg", "kernel_gain_vs_wrong", "matched_beats_tpg_v6"]].to_csv(
        DATA / "tau_kernel_path_modulation_by_galaxy_v01.csv", index=False
    )
    print(payload["status"])


if __name__ == "__main__":
    main()
