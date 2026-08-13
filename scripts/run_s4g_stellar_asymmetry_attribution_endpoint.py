#!/usr/bin/env python3
"""Score the frozen two-band S4G stellar-asymmetry attribution endpoint."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
FREEZE_PATH = DATA / "s4g_stellar_asymmetry_attribution_freeze_v01.json"
SOURCE_PATH = DATA / "s4g_stellar_asymmetry_attribution_source_v01.csv"
ENDPOINT_PATH = DATA / "source_native_carrier_robustness_scores_by_galaxy.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transform(frame: pd.DataFrame, features: list[str], train_mask: np.ndarray) -> np.ndarray:
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
    x: np.ndarray, y: np.ndarray, train_mask: np.ndarray, test_mask: np.ndarray
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
    asymmetry_values: np.ndarray,
    n_folds: int,
) -> dict[str, object]:
    work = frame.copy()
    work["asymmetry_scored"] = asymmetry_values
    pred_baseline = np.full(len(work), np.nan)
    pred_augmented = np.full(len(work), np.nan)
    coefficients = []
    for fold in range(n_folds):
        test_mask = work["fold"].eq(fold).to_numpy()
        train_mask = ~test_mask
        x_base = transform(work, baseline_features, train_mask)
        x_asymmetry = transform(work, ["asymmetry_scored"], train_mask)
        pred_baseline[test_mask], _ = ridge_fit_predict(x_base, y, train_mask, test_mask)
        pred_augmented[test_mask], beta = ridge_fit_predict(
            np.column_stack([x_base, x_asymmetry]), y, train_mask, test_mask
        )
        coefficients.append(float(beta[-1]))
    mse_baseline = float(np.mean((y - pred_baseline) ** 2))
    mse_augmented = float(np.mean((y - pred_augmented) ** 2))
    return {
        "prediction_baseline": pred_baseline,
        "prediction_augmented": pred_augmented,
        "mse_baseline": mse_baseline,
        "mse_augmented": mse_augmented,
        "mse_reduction": mse_baseline - mse_augmented,
        "proportional_mse_reduction": (mse_baseline - mse_augmented) / mse_baseline,
        "asymmetry_coefficients": coefficients,
        "positive_asymmetry_coefficient_folds": sum(value > 0 for value in coefficients),
    }


def scalar_metrics(result: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in result.items() if not key.startswith("prediction_")}


def main() -> None:
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    if freeze["status"] != "SOURCE_ONLY_S4G_STELLAR_ASYMMETRY_FREEZE_READY":
        raise RuntimeError("S4G stellar-asymmetry source freeze is not ready")
    if not freeze["source_only"] or freeze["endpoint_access"]:
        raise RuntimeError("S4G stellar-asymmetry source/endpoint boundary failed")
    if sha256(SOURCE_PATH) != freeze["source_features_sha256"]:
        raise RuntimeError("S4G stellar-asymmetry frozen source hash mismatch")

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
            f"S4G asymmetry endpoint join changed sample: {len(joined)} != {freeze['n_rows']}"
        )

    baseline_features = freeze["baseline_features"]
    asymmetry_3p6 = joined["asymmetry_3p6"].astype(float).to_numpy()
    asymmetry_4p5 = joined["asymmetry_4p5"].astype(float).to_numpy()
    y_tpg = np.log(joined["rmse_tpg_v6"].astype(float).to_numpy())
    y_newtonian = np.log(joined["rmse_newtonian_baryonic"].astype(float).to_numpy())

    tpg_3p6 = oof_score(joined, y_tpg, baseline_features, asymmetry_3p6, freeze["n_folds"])
    tpg_4p5 = oof_score(joined, y_tpg, baseline_features, asymmetry_4p5, freeze["n_folds"])
    newtonian_3p6 = oof_score(
        joined, y_newtonian, baseline_features, asymmetry_3p6, freeze["n_folds"]
    )

    rng = np.random.default_rng(freeze["permutation_seed"])
    null_3p6 = np.empty(freeze["n_permutations"])
    null_4p5 = np.empty(freeze["n_permutations"])
    for index in range(freeze["n_permutations"]):
        permutation = rng.permutation(len(joined))
        null_3p6[index] = float(
            oof_score(
                joined, y_tpg, baseline_features, asymmetry_3p6[permutation], freeze["n_folds"]
            )["mse_reduction"]
        )
        null_4p5[index] = float(
            oof_score(
                joined, y_tpg, baseline_features, asymmetry_4p5[permutation], freeze["n_folds"]
            )["mse_reduction"]
        )

    observed_3p6 = float(tpg_3p6["mse_reduction"])
    observed_4p5 = float(tpg_4p5["mse_reduction"])
    p_3p6 = float((1 + np.sum(null_3p6 >= observed_3p6)) / (len(null_3p6) + 1))
    p_4p5 = float((1 + np.sum(null_4p5 >= observed_4p5)) / (len(null_4p5) + 1))
    q95_3p6 = float(np.quantile(null_3p6, 0.95))
    q95_4p5 = float(np.quantile(null_4p5, 0.95))

    gates = {
        "source_channel_correlation_ge_0p8": freeze["source_channel_concordance_gate"],
        "positive_tpg_oof_reduction_3p6": observed_3p6 > 0,
        "positive_tpg_oof_reduction_4p5": observed_4p5 > 0,
        "shuffle_p_le_0p05_3p6": p_3p6 <= 0.05,
        "shuffle_p_le_0p05_4p5": p_4p5 <= 0.05,
        "above_shuffle_q95_3p6": observed_3p6 > q95_3p6,
        "above_shuffle_q95_4p5": observed_4p5 > q95_4p5,
        "positive_coefficient_in_4_of_5_folds_3p6": int(
            tpg_3p6["positive_asymmetry_coefficient_folds"]
        ) >= 4,
        "positive_coefficient_in_4_of_5_folds_4p5": int(
            tpg_4p5["positive_asymmetry_coefficient_folds"]
        ) >= 4,
        "tpg_gain_exceeds_newtonian_control": float(tpg_3p6["proportional_mse_reduction"])
        > float(newtonian_3p6["proportional_mse_reduction"]),
    }
    status = (
        "RETROSPECTIVE_S4G_STELLAR_ASYMMETRY_SIGNAL_PASS"
        if all(gates.values())
        else "RETROSPECTIVE_S4G_STELLAR_ASYMMETRY_SIGNAL_FAIL"
    )

    predictions = joined[["galaxy", "fold", "asymmetry_3p6", "asymmetry_4p5"]].copy()
    predictions["log_tpg_target"] = y_tpg
    predictions["tpg_3p6_baseline_prediction"] = tpg_3p6["prediction_baseline"]
    predictions["tpg_3p6_augmented_prediction"] = tpg_3p6["prediction_augmented"]
    predictions["tpg_4p5_augmented_prediction"] = tpg_4p5["prediction_augmented"]
    predictions_path = DATA / "s4g_stellar_asymmetry_attribution_oof_v01.csv"
    predictions.to_csv(predictions_path, index=False)

    null_path = DATA / "s4g_stellar_asymmetry_attribution_null_v01.csv"
    pd.DataFrame(
        {
            "permutation": np.arange(len(null_3p6)),
            "tpg_mse_reduction_3p6": null_3p6,
            "tpg_mse_reduction_4p5": null_4p5,
        }
    ).to_csv(null_path, index=False)

    summary = {
        "schema": "s4g_stellar_asymmetry_attribution_endpoint_v01",
        "status": status,
        "claim_level": "retrospective_source_family_prevalidation",
        "n_rows": len(joined),
        "n_folds": freeze["n_folds"],
        "source_channel_correlation": freeze["source_channel_correlation"],
        "tpg_3p6_primary": scalar_metrics(tpg_3p6),
        "tpg_4p5_replication": scalar_metrics(tpg_4p5),
        "newtonian_3p6_control": scalar_metrics(newtonian_3p6),
        "shuffle": {
            "n": len(null_3p6),
            "p_3p6": p_3p6,
            "p_4p5": p_4p5,
            "q95_3p6": q95_3p6,
            "q95_4p5": q95_4p5,
        },
        "gates": gates,
        "freeze_sha256": sha256(FREEZE_PATH),
        "source_sha256": sha256(SOURCE_PATH),
        "endpoint_sha256": sha256(ENDPOINT_PATH),
        "claim_boundary": (
            "retrospective source-family prevalidation; a pass would establish only "
            "incremental stellar-asymmetry information after broad controls, not M_tau"
        ),
    }
    summary_path = DATA / "s4g_stellar_asymmetry_attribution_endpoint_v01.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    gate_lines = "\n".join(
        f"| `{name}` | {'PASS' if value else 'FAIL'} |" for name, value in gates.items()
    )
    report_path = REPORTS / "s4g_stellar_asymmetry_attribution_endpoint_v01.md"
    report_path.write_text(
        f"""# S4G Stellar Asymmetry Attribution Endpoint v0.1

**Status:** `{status}`

## Five-Fold Out-of-Fold Result

| target/coordinate | baseline MSE | augmented MSE | reduction | proportional reduction |
| --- | ---: | ---: | ---: | ---: |
| TPG-v6, 3.6 micron A | {tpg_3p6['mse_baseline']:.8f} | {tpg_3p6['mse_augmented']:.8f} | {observed_3p6:.8f} | {tpg_3p6['proportional_mse_reduction']:.3%} |
| TPG-v6, 4.5 micron A | {tpg_4p5['mse_baseline']:.8f} | {tpg_4p5['mse_augmented']:.8f} | {observed_4p5:.8f} | {tpg_4p5['proportional_mse_reduction']:.3%} |
| Newtonian control, 3.6 micron A | {newtonian_3p6['mse_baseline']:.8f} | {newtonian_3p6['mse_augmented']:.8f} | {newtonian_3p6['mse_reduction']:.8f} | {newtonian_3p6['proportional_mse_reduction']:.3%} |

## Null And Sign Checks

| quantity | 3.6 micron | 4.5 micron |
| --- | ---: | ---: |
| positive coefficient folds | {tpg_3p6['positive_asymmetry_coefficient_folds']}/5 | {tpg_4p5['positive_asymmetry_coefficient_folds']}/5 |
| paired-row shuffle p | {p_3p6:.6f} | {p_4p5:.6f} |
| shuffle 95th percentile | {q95_3p6:.8f} | {q95_4p5:.8f} |

## Promotion Gates

| gate | result |
| --- | --- |
{gate_lines}

The source coordinate, sign, broad structural controls, folds, model, metric,
null, and Newtonian control were frozen before this scorer opened the endpoint.

## Claim Boundary

This is retrospective source-family prevalidation. Even a pass would establish
only incremental stellar-asymmetry information, not unique morphological-body
attribution, physical channel descent, or proof of `M_tau`.
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
