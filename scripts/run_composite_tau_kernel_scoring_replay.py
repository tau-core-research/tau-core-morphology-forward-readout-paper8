#!/usr/bin/env python3
"""Score the frozen composite Tau kernel on the predeclared replay lanes."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import run_family_observable_quality_diagnostics as quality
import run_predeclared_quality_gate_diagnostics as gates


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/composite_tau_kernel_scoring_replay_v01.md"
SEED = 20260711
N_BOOTSTRAP = 20_000


def bootstrap_interval(values: np.ndarray, rng: np.random.Generator) -> list[float]:
    samples = np.empty(N_BOOTSTRAP)
    for index in range(N_BOOTSTRAP):
        draw = rng.integers(0, len(values), len(values))
        samples[index] = np.mean(values[draw])
    return np.quantile(samples, [0.025, 0.5, 0.975]).tolist()


def lane_summary(joined: pd.DataFrame, lane: str, expression: str, nulls: pd.DataFrame) -> dict:
    holdout = joined[joined.split.eq("holdout")]
    sub = holdout.loc[gates.apply_gate(holdout, expression)].copy()
    null = nulls[(nulls.split.eq("holdout")) & (nulls.quality_gate.eq(lane))].iloc[0]
    rng = np.random.default_rng(SEED + len(sub))
    delta_wrong = sub.matched_minus_wrong_mean.to_numpy()
    delta_tpg = sub.matched_minus_tpg_v6.to_numpy()
    delta_mond = sub.matched_minus_mond.to_numpy()
    return {
        "lane": lane,
        "n_galaxies": len(sub),
        "n_rotation_points": int(sub.n_points_scored.sum()),
        "mean_rmse_km_s": {
            "matched_tau": float(sub.rmse_matched_family.mean()),
            "wrong_family": float(sub.rmse_wrong_family_mean.mean()),
            "tpg_v6": float(sub.rmse_tpg_v6.mean()),
            "mond": float(sub.rmse_mond.mean()),
        },
        "win_fraction": {
            "wrong_family": float(sub.matched_beats_wrong_mean.mean()),
            "tpg_v6": float(sub.matched_beats_tpg_v6.mean()),
            "mond": float(sub.matched_beats_mond.mean()),
        },
        "mean_paired_rmse_delta_km_s": {
            "matched_minus_wrong": float(delta_wrong.mean()),
            "matched_minus_tpg_v6": float(delta_tpg.mean()),
            "matched_minus_mond": float(delta_mond.mean()),
        },
        "paired_bootstrap_mean_delta_95_interval_km_s": {
            "matched_minus_wrong": bootstrap_interval(delta_wrong, rng),
            "matched_minus_tpg_v6": bootstrap_interval(delta_tpg, rng),
            "matched_minus_mond": bootstrap_interval(delta_mond, rng),
        },
        "shuffled_family_null": {
            "p_beats_wrong_fraction": float(null.p_beats_wrong_fraction_at_least_as_good),
            "p_mean_matched_minus_wrong": float(null.p_mean_minus_wrong_at_least_as_good),
        },
    }


def main() -> None:
    joined = quality.load_joined()
    nulls = pd.read_csv(DATA / "quality_gate_shuffled_null_summary.csv")
    primary = lane_summary(joined, "no_low_inclination", gates.QUALITY_GATES["no_low_inclination"], nulls)
    full = lane_summary(joined, "all", gates.QUALITY_GATES["all"], nulls)
    secondary = lane_summary(
        joined, "no_large_distance_error", gates.QUALITY_GATES["no_large_distance_error"], nulls
    )
    p = primary
    result = {
        "schema": "composite_tau_kernel_scoring_replay_v01",
        "status": "PREDECLARED_REPLAY_POSITIVE_KERNEL_SPECIFICITY_NOT_PROSPECTIVE_ENDPOINT",
        "kernel_interpretation": (
            "effective composite morphology-channel carrier; time and quantum factors unresolved"
        ),
        "amplitude_policy": "train_selected_family_to_global_shrinkage_0_40",
        "primary_lane": primary, "full_support_lane": full, "baseline_secondary_lane": secondary,
        "verdicts": {
            "matched_kernel_family_specificity_signal": (
                p["win_fraction"]["wrong_family"] >= 0.8
                and p["shuffled_family_null"]["p_beats_wrong_fraction"] <= 0.05
                and p["shuffled_family_null"]["p_mean_matched_minus_wrong"] <= 0.05
            ),
            "majority_beats_tpg_v6": p["win_fraction"]["tpg_v6"] > 0.5,
            "majority_beats_mond": p["win_fraction"]["mond"] > 0.5,
            "mean_rmse_beats_tpg_v6": p["mean_paired_rmse_delta_km_s"]["matched_minus_tpg_v6"] < 0,
            "mean_rmse_beats_mond": p["mean_paired_rmse_delta_km_s"]["matched_minus_mond"] < 0,
            "universal_baseline_superiority": False,
            "time_operator_identified": False, "quantum_operator_identified": False,
            "physical_channel_origin_identified": False,
        },
        "replay_not_prospective_reason": (
            "the quality gate was selected as a protocol candidate after preparation-state holdout inspection"
        ),
        "endpoint_access": True,
        "claim_boundary": (
            "positive morphology-family-specific composite-kernel replay; not a new prospective endpoint, "
            "not universal superiority, and not identification of time or quantum channel origin"
        ),
    }
    (DATA / "composite_tau_kernel_scoring_replay_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    primary_rows = joined[
        joined.split.eq("holdout") & gates.apply_gate(joined, gates.QUALITY_GATES["no_low_inclination"])
    ].copy()
    primary_rows.to_csv(DATA / "composite_tau_kernel_scoring_replay_primary_v01.csv", index=False)
    REPORT.write_text(
        "# Composite Tau kernel scoring replay v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The primary no-low-inclination lane contains {p['n_galaxies']} galaxies and "
        f"{p['n_rotation_points']} rotation points. The matched kernel beats the wrong-family "
        f"mean in `{p['win_fraction']['wrong_family']:.3f}`, TPG/v6 in "
        f"`{p['win_fraction']['tpg_v6']:.3f}`, and MOND in "
        f"`{p['win_fraction']['mond']:.3f}` of galaxies. Shuffled-family p-values are "
        f"`{p['shuffled_family_null']['p_beats_wrong_fraction']:.4f}` and "
        f"`{p['shuffled_family_null']['p_mean_matched_minus_wrong']:.4f}`.\n\n"
        f"Mean paired matched-minus-TPG RMSE is "
        f"`{p['mean_paired_rmse_delta_km_s']['matched_minus_tpg_v6']:.3f} km/s`; "
        f"matched-minus-MOND is `{p['mean_paired_rmse_delta_km_s']['matched_minus_mond']:.3f} km/s`.\n\n"
        "This is a positive kernel-family-specificity replay. It is not a fresh prospective "
        "endpoint and does not separate morphology, time, quantum, or path operators.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
