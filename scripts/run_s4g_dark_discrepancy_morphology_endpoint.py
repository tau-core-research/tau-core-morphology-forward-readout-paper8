#!/usr/bin/env python3
"""Test whether source-frozen S4G morphology predicts outer mass discrepancy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TAU_ROOT = ROOT.parent
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
FREEZE_PATH = DATA / "s4g_dark_discrepancy_morphology_freeze_v01.json"
TARGET_PATH = TAU_ROOT / (
    "tau-core-theory/source_material/tau_core_foundations/numerical_checks/"
    "tau_core_galactic_clock_channel_reparameterization_v01_galaxies.csv"
)
SUMMARY_PATH = DATA / "s4g_dark_discrepancy_morphology_endpoint_v01.json"
N_PERMUTATIONS = 2000
RNG_SEED = 20260711


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix(frame: pd.DataFrame, columns: list[str], train: np.ndarray) -> np.ndarray:
    values = frame[columns].astype(float).to_numpy(copy=True)
    medians = np.nanmedian(values[train], axis=0)
    medians = np.where(np.isfinite(medians), medians, 0.0)
    missing = np.where(np.isnan(values))
    values[missing] = medians[missing[1]]
    means = values[train].mean(axis=0)
    scales = values[train].std(axis=0)
    scales = np.where(scales > 1e-12, scales, 1.0)
    return (values - means) / scales


def predict(x: np.ndarray, y: np.ndarray, train: np.ndarray, test: np.ndarray) -> np.ndarray:
    x_train = np.column_stack([np.ones(train.sum()), x[train]])
    x_test = np.column_stack([np.ones(test.sum()), x[test]])
    penalty = np.eye(x_train.shape[1])
    penalty[0, 0] = 0.0
    beta = np.linalg.solve(x_train.T @ x_train + penalty, x_train.T @ y[train])
    return x_test @ beta


def mse(actual: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.mean((actual - predicted) ** 2))


def main() -> None:
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    if freeze["status"] != "SOURCE_ONLY_DARK_DISCREPANCY_MORPHOLOGY_FREEZE_READY":
        raise RuntimeError("Dark-discrepancy morphology freeze is not ready")
    source_path = ROOT / freeze["source_features_path"]
    if sha256(source_path) != freeze["source_features_sha256"]:
        raise RuntimeError("Frozen source feature hash mismatch")

    source = pd.read_csv(source_path)
    target = pd.read_csv(TARGET_PATH)[
        ["galaxy", "outer3_required_clock_factor_median"]
    ].copy()
    target = target.loc[target["outer3_required_clock_factor_median"].gt(0)]
    joined = source.merge(target, on="galaxy", how="inner", validate="one_to_one")
    joined = joined.sort_values("galaxy").reset_index(drop=True)
    train = joined["split"].eq("train").to_numpy()
    test = joined["split"].eq("holdout").to_numpy()
    x_base = matrix(joined, freeze["baseline_features"], train)
    x_morph = matrix(joined, freeze["morphology_features"], train)
    factor = joined["outer3_required_clock_factor_median"].astype(float).to_numpy()
    y = -2.0 * np.log(factor)

    base_prediction = predict(x_base, y, train, test)
    augmented_prediction = predict(np.column_stack([x_base, x_morph]), y, train, test)
    baseline_mse = mse(y[test], base_prediction)
    augmented_mse = mse(y[test], augmented_prediction)
    observed = baseline_mse - augmented_mse

    rng = np.random.default_rng(RNG_SEED)
    row_null = np.empty(N_PERMUTATIONS)
    column_null = np.empty(N_PERMUTATIONS)
    for index in range(N_PERMUTATIONS):
        permuted = x_morph[rng.permutation(len(joined))]
        row_null[index] = baseline_mse - mse(
            y[test], predict(np.column_stack([x_base, permuted]), y, train, test)
        )
        independent = np.empty_like(x_morph)
        for column in range(x_morph.shape[1]):
            independent[:, column] = x_morph[rng.permutation(len(joined)), column]
        column_null[index] = baseline_mse - mse(
            y[test], predict(np.column_stack([x_base, independent]), y, train, test)
        )

    row_p = float((1 + np.sum(row_null >= observed)) / (N_PERMUTATIONS + 1))
    column_p = float((1 + np.sum(column_null >= observed)) / (N_PERMUTATIONS + 1))
    row_q95 = float(np.quantile(row_null, 0.95))
    column_q95 = float(np.quantile(column_null, 0.95))
    gates = {
        "positive_holdout_mse_reduction": observed > 0,
        "row_shuffle_p_le_0p05": row_p <= 0.05,
        "column_shuffle_p_le_0p05": column_p <= 0.05,
        "above_row_shuffle_q95": observed > row_q95,
        "above_column_shuffle_q95": observed > column_q95,
    }
    passed = all(gates.values())

    holdout = joined.loc[test, ["galaxy", "split"]].copy()
    holdout["log_outer3_mass_discrepancy"] = y[test]
    holdout["baseline_prediction"] = base_prediction
    holdout["baseline_plus_morphology_prediction"] = augmented_prediction
    holdout.to_csv(DATA / "s4g_dark_discrepancy_morphology_holdout_v01.csv", index=False)
    pd.DataFrame({
        "permutation": np.arange(N_PERMUTATIONS),
        "row_shuffle_mse_reduction": row_null,
        "column_shuffle_mse_reduction": column_null,
    }).to_csv(DATA / "s4g_dark_discrepancy_morphology_nulls_v01.csv", index=False)

    status = (
        "RETROSPECTIVE_S4G_DARK_DISCREPANCY_MORPHOLOGY_SIGNAL_PASS"
        if passed else "RETROSPECTIVE_S4G_DARK_DISCREPANCY_MORPHOLOGY_SIGNAL_FAIL"
    )
    summary = {
        "schema": "s4g_dark_discrepancy_morphology_endpoint_v01",
        "status": status,
        "claim_level": "retrospective_locked_prevalidation",
        "n_rows": len(joined),
        "n_train": int(train.sum()),
        "n_holdout": int(test.sum()),
        "target": "log_outer3_mass_discrepancy",
        "baseline_mse": baseline_mse,
        "baseline_plus_morphology_mse": augmented_mse,
        "mse_reduction": observed,
        "proportional_mse_reduction": observed / baseline_mse,
        "nulls": {"n": N_PERMUTATIONS, "rng_seed": RNG_SEED, "row_p": row_p,
                  "row_q95": row_q95, "column_p": column_p, "column_q95": column_q95},
        "gates": gates,
        "freeze_sha256": sha256(FREEZE_PATH),
        "source_sha256": sha256(source_path),
        "target_sha256": sha256(TARGET_PATH),
        "morphology_information_candidate": passed,
        "channel_origin_identified": False,
        "claim_boundary": (
            "retrospective locked 4D inverse test; even a pass is incremental source-"
            "morphology information about outer discrepancy, not M_tau or channel proof"
        ),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "s4g_dark_discrepancy_morphology_endpoint_v01.md").write_text(
        f"""# S4G Dark-Discrepancy Morphology Endpoint v0.1

**Status:** `{status}`

The frozen holdout contains {int(test.sum())} galaxies ({len(joined)} total).
Baseline MSE is `{baseline_mse:.8f}` and baseline-plus-morphology MSE is
`{augmented_mse:.8f}`, giving a reduction of `{observed:.8f}`
(`{observed / baseline_mse:.2%}`). Row-shuffle `p={row_p:.6f}` and independent
column-shuffle `p={column_p:.6f}`.

This is a retrospective locked 4D inverse test. It does not derive the
morphological body, identify an observer-time or quantum channel, or exclude
dark matter.
""", encoding="utf-8")
    print(status)
    print(SUMMARY_PATH)


if __name__ == "__main__":
    main()
