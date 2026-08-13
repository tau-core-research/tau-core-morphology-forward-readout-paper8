#!/usr/bin/env python3
"""Score the frozen S4G optical morphology attribution endpoint."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TAU_ROOT = ROOT.parent
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
FREEZE_PATH = DATA / "s4g_optical_morphology_attribution_freeze_v02.json"
SOURCE_PATH = DATA / "s4g_optical_morphology_attribution_source_features_v02.csv"
ENDPOINT_PATH = DATA / "source_native_carrier_robustness_scores_by_galaxy.csv"
RNG_SEED = 20260710
N_PERMUTATIONS = 1000


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_matrix(
    frame: pd.DataFrame, features: list[str], train_mask: np.ndarray
) -> np.ndarray:
    matrix = frame[features].astype(float).to_numpy(copy=True)
    train = matrix[train_mask]
    medians = np.nanmedian(train, axis=0)
    medians = np.where(np.isfinite(medians), medians, 0.0)
    missing = np.where(np.isnan(matrix))
    matrix[missing] = medians[missing[1]]
    means = matrix[train_mask].mean(axis=0)
    scales = matrix[train_mask].std(axis=0)
    scales = np.where(scales > 1e-12, scales, 1.0)
    return (matrix - means) / scales


def ridge_predict(
    x: np.ndarray, y: np.ndarray, train_mask: np.ndarray, test_mask: np.ndarray
) -> np.ndarray:
    x_train = np.column_stack([np.ones(train_mask.sum()), x[train_mask]])
    x_test = np.column_stack([np.ones(test_mask.sum()), x[test_mask]])
    penalty = np.eye(x_train.shape[1])
    penalty[0, 0] = 0.0
    beta = np.linalg.solve(x_train.T @ x_train + penalty, x_train.T @ y[train_mask])
    return x_test @ beta


def mse(y: np.ndarray, prediction: np.ndarray) -> float:
    return float(np.mean((y - prediction) ** 2))


def score_target(
    y: np.ndarray,
    x_base: np.ndarray,
    x_morph: np.ndarray,
    train_mask: np.ndarray,
    test_mask: np.ndarray,
) -> dict[str, float | np.ndarray]:
    pred_base = ridge_predict(x_base, y, train_mask, test_mask)
    pred_aug = ridge_predict(
        np.column_stack([x_base, x_morph]), y, train_mask, test_mask
    )
    y_test = y[test_mask]
    mse_base = mse(y_test, pred_base)
    mse_aug = mse(y_test, pred_aug)
    return {
        "prediction_baseline": pred_base,
        "prediction_augmented": pred_aug,
        "mse_baseline": mse_base,
        "mse_augmented": mse_aug,
        "mse_reduction": mse_base - mse_aug,
        "proportional_mse_reduction": (mse_base - mse_aug) / mse_base,
    }


def main() -> None:
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    if freeze["status"] != "SOURCE_ONLY_RETROSPECTIVE_LOCK_V02_READY":
        raise RuntimeError("Source freeze is not ready")
    if not freeze["source_only"] or freeze["endpoint_access"]:
        raise RuntimeError("Source freeze endpoint boundary failed")
    if sha256(SOURCE_PATH) != freeze["output_sha256"]:
        raise RuntimeError("Frozen source feature hash mismatch")
    if freeze["model"] != "ridge_linear_fixed_lambda_1":
        raise RuntimeError("Unexpected frozen model")

    source = pd.read_csv(SOURCE_PATH)
    endpoint = pd.read_csv(ENDPOINT_PATH)
    endpoint = endpoint.loc[
        endpoint["carrier_id"].eq("tpg_v6"),
        ["galaxy", "rmse_tpg_v6", "rmse_newtonian_baryonic"],
    ].copy()
    required_targets = ["rmse_tpg_v6", "rmse_newtonian_baryonic"]
    if any(target not in endpoint.columns for target in required_targets):
        raise RuntimeError("Required frozen endpoint target missing")
    joined = source.merge(
        endpoint,
        on="galaxy",
        how="inner",
        validate="one_to_one",
    ).sort_values("galaxy").reset_index(drop=True)
    if len(joined) != freeze["n_rows"]:
        raise RuntimeError(
            f"Endpoint join changed frozen sample: {len(joined)} != {freeze['n_rows']}"
        )

    train_mask = joined["split"].eq("train").to_numpy()
    test_mask = joined["split"].eq("holdout").to_numpy()
    baseline_features = freeze["baseline_features"] + freeze[
        "baseline_missingness_features"
    ]
    morphology_features = freeze["morphology_features"] + freeze[
        "morphology_missingness_features"
    ]
    x_base = prepare_matrix(joined, baseline_features, train_mask)
    x_morph = prepare_matrix(joined, morphology_features, train_mask)

    y_projection = np.log(joined["rmse_tpg_v6"].astype(float).to_numpy())
    y_newtonian = np.log(
        joined["rmse_newtonian_baryonic"].astype(float).to_numpy()
    )
    projection = score_target(
        y_projection, x_base, x_morph, train_mask, test_mask
    )
    newtonian = score_target(
        y_newtonian, x_base, x_morph, train_mask, test_mask
    )

    rng = np.random.default_rng(RNG_SEED)
    row_null = np.empty(N_PERMUTATIONS)
    column_null = np.empty(N_PERMUTATIONS)
    baseline_projection_mse = float(projection["mse_baseline"])
    for index in range(N_PERMUTATIONS):
        row_permutation = rng.permutation(len(joined))
        row_prediction = ridge_predict(
            np.column_stack([x_base, x_morph[row_permutation]]),
            y_projection,
            train_mask,
            test_mask,
        )
        row_null[index] = baseline_projection_mse - mse(
            y_projection[test_mask], row_prediction
        )

        column_permuted = np.empty_like(x_morph)
        for column in range(x_morph.shape[1]):
            column_permuted[:, column] = x_morph[
                rng.permutation(len(joined)), column
            ]
        column_prediction = ridge_predict(
            np.column_stack([x_base, column_permuted]),
            y_projection,
            train_mask,
            test_mask,
        )
        column_null[index] = baseline_projection_mse - mse(
            y_projection[test_mask], column_prediction
        )

    observed = float(projection["mse_reduction"])
    row_p = float((1 + np.sum(row_null >= observed)) / (N_PERMUTATIONS + 1))
    column_p = float(
        (1 + np.sum(column_null >= observed)) / (N_PERMUTATIONS + 1)
    )
    row_q95 = float(np.quantile(row_null, 0.95))
    column_q95 = float(np.quantile(column_null, 0.95))

    gates = {
        "positive_projection_holdout_reduction": observed > 0,
        "row_shuffle_p_le_0p05": row_p <= 0.05,
        "column_shuffle_p_le_0p05": column_p <= 0.05,
        "above_row_shuffle_q95": observed > row_q95,
        "above_column_shuffle_q95": observed > column_q95,
        "projection_gain_exceeds_newtonian_control": float(
            projection["proportional_mse_reduction"]
        )
        > float(newtonian["proportional_mse_reduction"]),
    }
    passed = all(gates.values())
    status = (
        "RETROSPECTIVE_S4G_OPTICAL_MORPHOLOGY_INCREMENTAL_SIGNAL_PASS"
        if passed
        else "RETROSPECTIVE_S4G_OPTICAL_MORPHOLOGY_INCREMENTAL_SIGNAL_FAIL"
    )

    holdout = joined.loc[test_mask, ["galaxy", "split"]].copy()
    holdout["log_projection_target"] = y_projection[test_mask]
    holdout["projection_baseline_prediction"] = projection["prediction_baseline"]
    holdout["projection_augmented_prediction"] = projection["prediction_augmented"]
    holdout["log_newtonian_target"] = y_newtonian[test_mask]
    holdout["newtonian_baseline_prediction"] = newtonian["prediction_baseline"]
    holdout["newtonian_augmented_prediction"] = newtonian["prediction_augmented"]
    holdout_path = DATA / "s4g_optical_morphology_attribution_holdout_v02.csv"
    holdout.to_csv(holdout_path, index=False)

    nulls = pd.DataFrame(
        {
            "permutation": np.arange(N_PERMUTATIONS),
            "row_shuffle_mse_reduction": row_null,
            "column_shuffle_mse_reduction": column_null,
        }
    )
    null_path = DATA / "s4g_optical_morphology_attribution_nulls_v02.csv"
    nulls.to_csv(null_path, index=False)

    summary = {
        "schema": "s4g_optical_morphology_attribution_endpoint_v02",
        "status": status,
        "claim_level": "retrospective_locked_prevalidation",
        "n_rows": len(joined),
        "n_train": int(train_mask.sum()),
        "n_holdout": int(test_mask.sum()),
        "projection_target": {
            "mse_baseline": float(projection["mse_baseline"]),
            "mse_augmented": float(projection["mse_augmented"]),
            "mse_reduction": observed,
            "proportional_mse_reduction": float(
                projection["proportional_mse_reduction"]
            ),
        },
        "newtonian_control_target": {
            "mse_baseline": float(newtonian["mse_baseline"]),
            "mse_augmented": float(newtonian["mse_augmented"]),
            "mse_reduction": float(newtonian["mse_reduction"]),
            "proportional_mse_reduction": float(
                newtonian["proportional_mse_reduction"]
            ),
        },
        "nulls": {
            "n_permutations": N_PERMUTATIONS,
            "rng_seed": RNG_SEED,
            "row_shuffle_p": row_p,
            "row_shuffle_q95": row_q95,
            "column_shuffle_p": column_p,
            "column_shuffle_q95": column_q95,
        },
        "gates": gates,
        "source_freeze_sha256": sha256(FREEZE_PATH),
        "source_features_sha256": sha256(SOURCE_PATH),
        "endpoint_sha256": sha256(ENDPOINT_PATH),
        "claim_boundary": (
            "retrospective locked SPARC/S4G prevalidation only; not independent "
            "external replication, physical channel descent, lensing covariance, "
            "or M_tau attribution"
        ),
    }
    summary_path = DATA / "s4g_optical_morphology_attribution_endpoint_v02.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    report_path = REPORTS / "s4g_optical_morphology_attribution_endpoint_v02.md"
    gate_lines = "\n".join(
        f"| `{name}` | {'PASS' if value else 'FAIL'} |" for name, value in gates.items()
    )
    report_path.write_text(
        f"""# S4G Optical Morphology Attribution Endpoint v0.2

**Status:** `{status}`

## Frozen Holdout Result

| target | baseline MSE | augmented MSE | reduction | proportional reduction |
| --- | ---: | ---: | ---: | ---: |
| projection residual | {projection['mse_baseline']:.8f} | {projection['mse_augmented']:.8f} | {observed:.8f} | {projection['proportional_mse_reduction']:.3%} |
| Newtonian control residual | {newtonian['mse_baseline']:.8f} | {newtonian['mse_augmented']:.8f} | {newtonian['mse_reduction']:.8f} | {newtonian['proportional_mse_reduction']:.3%} |

## Null Controls

| control | p | 95th percentile reduction |
| --- | ---: | ---: |
| morphology row shuffle | {row_p:.6f} | {row_q95:.8f} |
| independent morphology column shuffle | {column_p:.6f} | {column_q95:.8f} |

## Promotion Gates

| gate | result |
| --- | --- |
{gate_lines}

The source manifest, feature list, deterministic split, model, metrics,
controls, and promotion rule were frozen by a separate source-only script.
The scorer verified the frozen feature hash before opening the endpoint.

## Claim Boundary

This is a retrospective locked SPARC/S4G prevalidation test. It is not an
independent external replication, physical `M_tau` channel derivation,
dynamics-lensing shared-parent result, or morphological-body attribution.
""",
        encoding="utf-8",
    )
    print(status)
    print(summary_path)
    print(report_path)
    print(holdout_path)
    print(null_path)


if __name__ == "__main__":
    main()
