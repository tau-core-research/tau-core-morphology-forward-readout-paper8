#!/usr/bin/env python3
"""Build robustness checks for the source-native readout formula result.

This script does not alter the endpoint labels.  It reads the same frozen
source-native formula artifacts and reports stress tests for the headline
matched-versus-wrong holdout fraction.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from run_source_native_readout_formula_endpoint import (  # noqa: E402
    FORMULA_FAMILIES,
    add_bridge_formula_kernels,
    add_predictions,
    fit_amplitudes,
    load_points,
    score_galaxies,
)

ROBUST_SEED = 271828
N_SHUFFLES_10K = 10_000
N_BOOTSTRAP = 10_000
N_ALT_SPLITS = 100
HOLDOUT_FRAC = 44 / 175


def finite_p(count: int, n: int) -> float:
    return float((1 + count) / (n + 1))


def shuffled_10k(galaxy_scores: pd.DataFrame) -> dict[str, float]:
    holdout = galaxy_scores.loc[galaxy_scores["split"] == "holdout"].reset_index(drop=True)
    rng = np.random.default_rng(ROBUST_SEED)
    labels = holdout["formula_family"].to_numpy()
    observed_beats = float(holdout["matched_beats_wrong_mean"].mean())
    observed_mean = float(holdout["matched_minus_wrong_mean"].mean())
    beats_stats = []
    mean_stats = []
    for _ in range(N_SHUFFLES_10K):
        shuffled = rng.permutation(labels)
        beats = []
        means = []
        for row_idx, family in enumerate(shuffled):
            scores = {
                candidate: float(holdout.loc[row_idx, f"rmse_{candidate}"])
                for candidate in FORMULA_FAMILIES
            }
            selected = scores[family]
            wrong = [value for candidate, value in scores.items() if candidate != family]
            wrong_mean = float(np.mean(wrong))
            beats.append(selected < wrong_mean)
            means.append(selected - wrong_mean)
        beats_stats.append(float(np.mean(beats)))
        mean_stats.append(float(np.mean(means)))
    beats_stats = np.asarray(beats_stats)
    mean_stats = np.asarray(mean_stats)
    return {
        "test": "10k shuffled-label null",
        "result": observed_beats,
        "p_value": finite_p(int((beats_stats >= observed_beats).sum()), N_SHUFFLES_10K),
        "detail": (
            f"seed={ROBUST_SEED}; observed mean-minus-wrong={observed_mean:.3f}; "
            f"null beats-wrong median={np.median(beats_stats):.3f}"
        ),
    }


def bootstrap_ci(galaxy_scores: pd.DataFrame) -> dict[str, float]:
    holdout = galaxy_scores.loc[galaxy_scores["split"] == "holdout"].reset_index(drop=True)
    rng = np.random.default_rng(ROBUST_SEED + 1)
    values = holdout["matched_beats_wrong_mean"].astype(float).to_numpy()
    stats = []
    n = len(values)
    for _ in range(N_BOOTSTRAP):
        idx = rng.integers(0, n, size=n)
        stats.append(float(values[idx].mean()))
    lo, hi = np.percentile(stats, [2.5, 97.5])
    return {
        "test": "Bootstrap CI",
        "result": float(values.mean()),
        "p_value": np.nan,
        "detail": f"seed={ROBUST_SEED + 1}; {N_BOOTSTRAP} galaxy bootstrap CI=[{lo:.3f},{hi:.3f}]",
    }


def weighted_rmse_by_galaxy(scored_points: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for galaxy, sub in scored_points.groupby("galaxy"):
        family = sub["formula_family"].iloc[0]
        err = sub["errv"].astype(float).clip(lower=1.0e-3)
        weights = 1.0 / np.square(err)
        family_scores = {}
        for candidate in FORMULA_FAMILIES:
            resid = sub[f"v_{candidate}"].astype(float) - sub["vobs"].astype(float)
            family_scores[candidate] = float(np.sqrt(np.average(np.square(resid), weights=weights)))
        selected = family_scores[family]
        wrong = [value for candidate, value in family_scores.items() if candidate != family]
        rows.append(
            {
                "galaxy": galaxy,
                "split": sub["split"].iloc[0],
                "formula_family": family,
                "weighted_matched_beats_wrong": selected < float(np.mean(wrong)),
                "weighted_matched_minus_wrong": selected - float(np.mean(wrong)),
            }
        )
    return pd.DataFrame(rows)


def error_weighted_summary(scored_points: pd.DataFrame) -> dict[str, float]:
    weighted = weighted_rmse_by_galaxy(scored_points)
    weighted.to_csv(DATA / "source_native_readout_formula_error_weighted_scores.csv", index=False)
    holdout = weighted.loc[weighted["split"] == "holdout"]
    return {
        "test": "Error-weighted RMSE",
        "result": float(holdout["weighted_matched_beats_wrong"].mean()),
        "p_value": np.nan,
        "detail": f"uses errv weights; mean weighted matched-minus-wrong={holdout['weighted_matched_minus_wrong'].mean():.3f}",
    }


def family_balanced(galaxy_scores: pd.DataFrame) -> dict[str, float]:
    holdout = galaxy_scores.loc[galaxy_scores["split"] == "holdout"]
    by_family = holdout.groupby("formula_family")["matched_beats_wrong_mean"].mean()
    return {
        "test": "Family-balanced score",
        "result": float(by_family.mean()),
        "p_value": np.nan,
        "detail": "; ".join(f"{family}={value:.3f}" for family, value in by_family.items()),
    }


def alternative_splits(points_with_kernels: pd.DataFrame) -> dict[str, float]:
    rng = np.random.default_rng(ROBUST_SEED + 2)
    galaxies = (
        points_with_kernels[["galaxy", "formula_family"]]
        .drop_duplicates()
        .sort_values("galaxy")
        .reset_index(drop=True)
    )
    stats = []
    for _ in range(N_ALT_SPLITS):
        holdout_galaxies = []
        for _, sub in galaxies.groupby("formula_family"):
            names = sub["galaxy"].to_numpy()
            n_hold = max(1, int(round(len(names) * HOLDOUT_FRAC)))
            holdout_galaxies.extend(rng.choice(names, size=n_hold, replace=False).tolist())
        alt = points_with_kernels.copy()
        alt["split"] = np.where(alt["galaxy"].isin(set(holdout_galaxies)), "holdout", "train")
        amps = fit_amplitudes(alt)
        scored = add_predictions(alt, amps)
        galaxy_scores, _, _ = score_galaxies(scored)
        hold = galaxy_scores.loc[galaxy_scores["split"] == "holdout"]
        stats.append(float(hold["matched_beats_wrong_mean"].mean()))
    stats = np.asarray(stats)
    return {
        "test": "Alternative split median",
        "result": float(np.median(stats)),
        "p_value": np.nan,
        "detail": (
            f"seed={ROBUST_SEED + 2}; {N_ALT_SPLITS} family-stratified splits; "
            f"central 90%=[{np.percentile(stats,5):.3f},{np.percentile(stats,95):.3f}]"
        ),
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    points, _ = load_points()
    points_with_kernels = add_bridge_formula_kernels(points)
    amplitudes = fit_amplitudes(points_with_kernels)
    scored_points = add_predictions(points_with_kernels, amplitudes)
    galaxy_scores, summary, _ = score_galaxies(scored_points)
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    rows = [
        {
            "test": "Original holdout",
            "result": float(holdout["matched_beats_wrong_fraction"]),
            "p_value": np.nan,
            "detail": (
                f"n_holdout={int(holdout['n_galaxies'])}; "
                f"mean matched-minus-wrong={holdout['mean_matched_minus_wrong']:.3f}"
            ),
        },
        shuffled_10k(galaxy_scores),
        bootstrap_ci(galaxy_scores),
        error_weighted_summary(scored_points),
        alternative_splits(points_with_kernels),
        family_balanced(galaxy_scores),
    ]
    out = pd.DataFrame(rows)
    out.to_csv(DATA / "source_native_readout_formula_robustness_summary.csv", index=False)
    print("SOURCE_NATIVE_READOUT_ROBUSTNESS_COMPLETE")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
