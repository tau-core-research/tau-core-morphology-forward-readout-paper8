#!/usr/bin/env python3
"""Run the frozen UNGC Theta1 environment attribution endpoint."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
FREEZE_PATH = DATA / "ungc_theta1_environment_attribution_freeze_v01.json"
SOURCE_PATH = DATA / "ungc_theta1_environment_attribution_source_v01.csv"
ENDPOINT_PATH = DATA / "source_native_carrier_robustness_scores_by_galaxy.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transform(
    frame: pd.DataFrame,
    features: list[str],
    train_mask: np.ndarray,
) -> np.ndarray:
    matrix = frame[features].astype(float).to_numpy(copy=True)
    medians = np.nanmedian(matrix[train_mask], axis=0)
    medians = np.where(np.isfinite(medians), medians, 0.0)
    missing = np.where(np.isnan(matrix))
    matrix[missing] = medians[missing[1]]
    means = matrix[train_mask].mean(axis=0)
    scales = matrix[train_mask].std(axis=0)
    scales = np.where(scales > 1e-12, scales, 1.0)
    return (matrix - means) / scales


def ridge_fit_predict(
    x: np.ndarray,
    y: np.ndarray,
    train_mask: np.ndarray,
    test_mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    x_train = np.column_stack([np.ones(train_mask.sum()), x[train_mask]])
    x_test = np.column_stack([np.ones(test_mask.sum()), x[test_mask]])
    penalty = np.eye(x_train.shape[1])
    penalty[0, 0] = 0.0
    beta = np.linalg.solve(x_train.T @ x_train + penalty, x_train.T @ y[train_mask])
    return x_test @ beta, beta


def oof_score(
    frame: pd.DataFrame,
    y: np.ndarray,
    baseline_features: list[str],
    environment_values: np.ndarray,
    n_folds: int,
) -> dict[str, object]:
    work = frame.copy()
    work["theta1_scored"] = environment_values
    pred_baseline = np.full(len(work), np.nan)
    pred_augmented = np.full(len(work), np.nan)
    theta_coefficients = []
    for fold in range(n_folds):
        test_mask = work["fold"].eq(fold).to_numpy()
        train_mask = ~test_mask
        x_base = transform(work, baseline_features, train_mask)
        x_theta = transform(work, ["theta1_scored"], train_mask)
        pred_baseline[test_mask], _ = ridge_fit_predict(
            x_base, y, train_mask, test_mask
        )
        pred_augmented[test_mask], beta = ridge_fit_predict(
            np.column_stack([x_base, x_theta]), y, train_mask, test_mask
        )
        theta_coefficients.append(float(beta[-1]))
    mse_baseline = float(np.mean((y - pred_baseline) ** 2))
    mse_augmented = float(np.mean((y - pred_augmented) ** 2))
    return {
        "prediction_baseline": pred_baseline,
        "prediction_augmented": pred_augmented,
        "mse_baseline": mse_baseline,
        "mse_augmented": mse_augmented,
        "mse_reduction": mse_baseline - mse_augmented,
        "proportional_mse_reduction": (mse_baseline - mse_augmented)
        / mse_baseline,
        "theta_coefficients": theta_coefficients,
        "positive_theta_coefficient_folds": sum(
            coefficient > 0 for coefficient in theta_coefficients
        ),
    }


def main() -> None:
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    if freeze["status"] != "SOURCE_ONLY_THETA1_ENVIRONMENT_FREEZE_READY":
        raise RuntimeError("Theta1 source freeze is not ready")
    if not freeze["source_only"] or freeze["endpoint_access"]:
        raise RuntimeError("Theta1 source/endpoint boundary failed")
    if sha256(SOURCE_PATH) != freeze["source_features_sha256"]:
        raise RuntimeError("Theta1 frozen source hash mismatch")

    source = pd.read_csv(SOURCE_PATH)
    endpoint = pd.read_csv(ENDPOINT_PATH)
    endpoint = endpoint.loc[
        endpoint["carrier_id"].eq("tpg_v6"),
        ["galaxy", "rmse_tpg_v6", "rmse_newtonian_baryonic"],
    ].copy()
    joined = source.merge(endpoint, on="galaxy", how="inner", validate="one_to_one")
    joined = joined.sort_values("galaxy").reset_index(drop=True)
    if len(joined) != freeze["n_rows"]:
        raise RuntimeError(
            f"Theta1 endpoint join changed sample: {len(joined)} != {freeze['n_rows']}"
        )

    baseline_features = freeze["baseline_features"] + freeze[
        "baseline_missingness_features"
    ]
    theta1 = joined["theta1"].astype(float).to_numpy()
    y_tpg = np.log(joined["rmse_tpg_v6"].astype(float).to_numpy())
    y_newtonian = np.log(
        joined["rmse_newtonian_baryonic"].astype(float).to_numpy()
    )
    tpg = oof_score(joined, y_tpg, baseline_features, theta1, freeze["n_folds"])
    newtonian = oof_score(
        joined, y_newtonian, baseline_features, theta1, freeze["n_folds"]
    )

    rng = np.random.default_rng(freeze["permutation_seed"])
    null = np.empty(freeze["n_permutations"])
    for index in range(freeze["n_permutations"]):
        permuted = theta1[rng.permutation(len(theta1))]
        null[index] = float(
            oof_score(
                joined,
                y_tpg,
                baseline_features,
                permuted,
                freeze["n_folds"],
            )["mse_reduction"]
        )
    observed = float(tpg["mse_reduction"])
    shuffle_p = float((1 + np.sum(null >= observed)) / (len(null) + 1))
    shuffle_q95 = float(np.quantile(null, 0.95))

    gates = {
        "positive_tpg_oof_mse_reduction": observed > 0,
        "theta1_shuffle_p_le_0p05": shuffle_p <= 0.05,
        "above_theta1_shuffle_q95": observed > shuffle_q95,
        "positive_theta1_coefficient_in_4_of_5_folds": int(
            tpg["positive_theta_coefficient_folds"]
        )
        >= 4,
        "tpg_gain_exceeds_newtonian_control": float(
            tpg["proportional_mse_reduction"]
        )
        > float(newtonian["proportional_mse_reduction"]),
    }
    status = (
        "RETROSPECTIVE_UNGC_THETA1_ENVIRONMENT_SIGNAL_PASS"
        if all(gates.values())
        else "RETROSPECTIVE_UNGC_THETA1_ENVIRONMENT_SIGNAL_FAIL"
    )

    predictions = joined[["galaxy", "fold", "theta1"]].copy()
    predictions["log_tpg_target"] = y_tpg
    predictions["tpg_baseline_prediction"] = tpg["prediction_baseline"]
    predictions["tpg_augmented_prediction"] = tpg["prediction_augmented"]
    predictions["log_newtonian_target"] = y_newtonian
    predictions["newtonian_baseline_prediction"] = newtonian[
        "prediction_baseline"
    ]
    predictions["newtonian_augmented_prediction"] = newtonian[
        "prediction_augmented"
    ]
    predictions_path = DATA / "ungc_theta1_environment_attribution_oof_v01.csv"
    predictions.to_csv(predictions_path, index=False)

    null_path = DATA / "ungc_theta1_environment_attribution_null_v01.csv"
    pd.DataFrame(
        {"permutation": np.arange(len(null)), "tpg_mse_reduction": null}
    ).to_csv(null_path, index=False)

    summary = {
        "schema": "ungc_theta1_environment_attribution_endpoint_v01",
        "status": status,
        "claim_level": "retrospective_source_family_prevalidation",
        "n_rows": len(joined),
        "n_folds": freeze["n_folds"],
        "tpg_target": {
            key: value
            for key, value in tpg.items()
            if not key.startswith("prediction_")
        },
        "newtonian_control": {
            key: value
            for key, value in newtonian.items()
            if not key.startswith("prediction_")
        },
        "shuffle": {
            "n": len(null),
            "p": shuffle_p,
            "q95": shuffle_q95,
            "median": float(np.median(null)),
        },
        "gates": gates,
        "freeze_sha256": sha256(FREEZE_PATH),
        "source_sha256": sha256(SOURCE_PATH),
        "endpoint_sha256": sha256(ENDPOINT_PATH),
        "claim_boundary": (
            "retrospective source-family prevalidation only; even a pass would "
            "remain compatible with ordinary tidal astrophysics and would not "
            "prove M_tau or shared-parent channel descent"
        ),
    }
    summary_path = DATA / "ungc_theta1_environment_attribution_endpoint_v01.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "ungc_theta1_environment_attribution_endpoint_v01.md"
    gate_lines = "\n".join(
        f"| `{name}` | {'PASS' if value else 'FAIL'} |" for name, value in gates.items()
    )
    report_path.write_text(
        f"""# UNGC Theta1 Environment Attribution Endpoint v0.1

**Status:** `{status}`

## Five-Fold Out-of-Fold Result

| target | baseline MSE | augmented MSE | reduction | proportional reduction |
| --- | ---: | ---: | ---: | ---: |
| TPG-v6 residual | {tpg['mse_baseline']:.8f} | {tpg['mse_augmented']:.8f} | {tpg['mse_reduction']:.8f} | {tpg['proportional_mse_reduction']:.3%} |
| Newtonian residual control | {newtonian['mse_baseline']:.8f} | {newtonian['mse_augmented']:.8f} | {newtonian['mse_reduction']:.8f} | {newtonian['proportional_mse_reduction']:.3%} |

## Frozen Sign And Null

| quantity | value |
| --- | ---: |
| positive Theta1 coefficient folds | {tpg['positive_theta_coefficient_folds']}/5 |
| standardized fold coefficients | `{tpg['theta_coefficients']}` |
| shuffle p | {shuffle_p:.6f} |
| shuffle 95th percentile | {shuffle_q95:.8f} |
| observed MSE reduction | {observed:.8f} |

## Promotion Gates

| gate | result |
| --- | --- |
{gate_lines}

The catalog, crossmatch, hypothesis, sign, folds, baseline, model, metric, and
controls were frozen before this scorer opened the endpoint. The scorer
verified the source-feature hash.

## Claim Boundary

This is retrospective source-family prevalidation. Even a positive result
would remain compatible with ordinary tidal astrophysics and would not prove
`M_tau`, physical channel descent, or shared-parent covariance.
""",
        encoding="utf-8",
    )
    print(status)
    print(summary_path)
    print(report_path)
    print(predictions_path)
    print(null_path)


if __name__ == "__main__":
    main()
