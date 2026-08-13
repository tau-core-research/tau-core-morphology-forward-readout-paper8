#!/usr/bin/env python3
"""Fit the frozen source-feature body amplitude law and score fixed holdout galaxies."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

import run_source_native_readout_formula_endpoint as source


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/body_amplitude_law_score_v01.md"
FAMILIES = source.FORMULA_FAMILIES


def ridge_fit(x, y, weights, alpha):
    root_w = np.sqrt(weights)[:, None]
    xw, yw = x * root_w, y * root_w[:, 0]
    penalty = np.eye(x.shape[1]) * alpha
    penalty[: len(FAMILIES), : len(FAMILIES)] = 0.0
    return np.linalg.pinv(xw.T @ xw + penalty) @ (xw.T @ yw)


def rmse(frame, column):
    return float(np.sqrt(np.mean((frame[column] - frame.vobs) ** 2)))


def main() -> None:
    freeze = json.loads((DATA / "body_amplitude_law_freeze_v01.json").read_text())
    assert freeze["uses_vobs_or_residual"] is False
    points, labels = source.load_points()
    points = source.add_bridge_formula_kernels(points)
    galaxy = (
        points.groupby("galaxy", as_index=False)
        .agg(
            total_gas_fraction=("total_gas_fraction", "mean"),
            mean_log_sbdisk=("log_sbdisk", "mean"),
            mean_bulge=("bulge_frac", "mean"),
            scale_radius_proxy_kpc=("scale_radius_proxy_kpc", "first"),
            tail_cutoff_radius_proxy_kpc=("tail_cutoff_radius_proxy_kpc", "first"),
        )
    )
    galaxy["log_scale_radius_proxy_kpc"] = np.log(galaxy.scale_radius_proxy_kpc.clip(1e-6))
    galaxy["log_tail_to_scale_ratio"] = np.log(
        (galaxy.tail_cutoff_radius_proxy_kpc / galaxy.scale_radius_proxy_kpc).clip(1e-6)
    )
    raw_features = freeze["source_features"]
    train_names = set(points.loc[points.split.eq("train"), "galaxy"])
    means = galaxy[galaxy.galaxy.isin(train_names)][raw_features].mean()
    scales = galaxy[galaxy.galaxy.isin(train_names)][raw_features].std(ddof=0).replace(0, 1)
    for feature in raw_features:
        galaxy[f"z_{feature}"] = (galaxy[feature] - means[feature]) / scales[feature]
    zcols = [f"z_{feature}" for feature in raw_features]
    points = points.merge(galaxy[["galaxy"] + zcols], on="galaxy", validate="many_to_one")

    def design(frame, candidate_family=None):
        family = frame.formula_family if candidate_family is None else pd.Series(
            candidate_family, index=frame.index
        )
        kernel = np.array([
            frame.loc[i, f"kernel_{f}"] for i, f in zip(frame.index, family)
        ])
        onehot = np.column_stack([(family == f).to_numpy(float) for f in FAMILIES])
        return kernel[:, None] * np.column_stack([onehot, frame[zcols].to_numpy()])

    train = points[points.split.eq("train")].copy().reset_index(drop=True)
    target = (train.vobs**2 - train.vn**2).to_numpy()
    weights = (1.0 / train.groupby("galaxy").galaxy.transform("size")).to_numpy()
    groups = train.galaxy.to_numpy()
    x = design(train)
    cv_rows = []
    splitter = GroupKFold(n_splits=5)
    for alpha in freeze["ridge_alpha_grid"]:
        galaxy_errors = []
        for fit_idx, val_idx in splitter.split(x, target, groups):
            coef = ridge_fit(x[fit_idx], target[fit_idx], weights[fit_idx], alpha)
            residual = x[val_idx] @ coef - target[val_idx]
            val = pd.DataFrame({"galaxy": groups[val_idx], "sq": residual**2})
            galaxy_errors.extend(val.groupby("galaxy").sq.mean().tolist())
        cv_rows.append({"alpha": alpha, "galaxy_balanced_cv_mse": float(np.mean(galaxy_errors))})
    selected_alpha = min(cv_rows, key=lambda row: row["galaxy_balanced_cv_mse"])["alpha"]
    coef = ridge_fit(x, target, weights, selected_alpha)

    scored = points.copy().reset_index(drop=True)
    for family in FAMILIES:
        correction = design(scored, family) @ coef
        scored[f"v_amp_{family}"] = np.sqrt(np.maximum(scored.vn**2 + correction, 0.0))
    rows = []
    for name, sub in scored.groupby("galaxy"):
        matched_family = sub.formula_family.iloc[0]
        fs = {family: rmse(sub, f"v_amp_{family}") for family in FAMILIES}
        matched = fs[matched_family]
        wrong = np.mean([value for family, value in fs.items() if family != matched_family])
        rows.append({
            "galaxy": name, "split": sub.split.iloc[0], "formula_family": matched_family,
            "n_points": len(sub), "rmse_matched": matched, "rmse_wrong_mean": wrong,
            "rmse_newton": rmse(sub, "vn"), "rmse_tpg_v6": rmse(sub, "v_v6"),
            "rmse_mond": rmse(sub, "v_mond"),
            "matched_minus_wrong": matched-wrong,
            "matched_minus_newton": matched-rmse(sub,"vn"),
            "matched_minus_tpg_v6": matched-rmse(sub,"v_v6"),
            "matched_minus_mond": matched-rmse(sub,"v_mond"),
            **{f"rmse_{family}": value for family, value in fs.items()},
        })
    scores = pd.DataFrame(rows).sort_values(["split", "galaxy"])
    holdout = scores[scores.split.eq("holdout")]
    def summary(column):
        values = holdout[column]
        return {"win_fraction": float((values < 0).mean()), "mean_delta_km_s": float(values.mean())}
    baseline = json.loads((DATA / "body_only_newtonian_kernel_score_v01.json").read_text())
    result = {
        "schema": "tau-core.paper8.body-amplitude-law-score.v01",
        "status": "SOURCE_FEATURE_BODY_AMPLITUDE_LAW_HOLDOUT_SCORED",
        "selected_ridge_alpha_train_cv": selected_alpha,
        "train_cv": cv_rows,
        "coefficients": {
            **{f"family_intercept_{family}": float(coef[i]) for i, family in enumerate(FAMILIES)},
            **{feature: float(coef[len(FAMILIES)+i]) for i, feature in enumerate(raw_features)},
        },
        "n_holdout_galaxies": len(holdout), "n_holdout_points": int(holdout.n_points.sum()),
        "matched_vs_wrong": summary("matched_minus_wrong"),
        "matched_vs_newton": summary("matched_minus_newton"),
        "matched_vs_tpg_v6": summary("matched_minus_tpg_v6"),
        "matched_vs_mond": summary("matched_minus_mond"),
        "change_vs_constant_family_body_model": {
            "tpg_win_fraction": summary("matched_minus_tpg_v6")["win_fraction"] - baseline["matched_vs_tpg_v6"]["win_fraction"],
            "mond_win_fraction": summary("matched_minus_mond")["win_fraction"] - baseline["matched_vs_mond"]["win_fraction"],
            "tpg_mean_delta_km_s": summary("matched_minus_tpg_v6")["mean_delta_km_s"] - baseline["matched_vs_tpg_v6"]["mean_delta_km_s"],
            "mond_mean_delta_km_s": summary("matched_minus_mond")["mean_delta_km_s"] - baseline["matched_vs_mond"]["mean_delta_km_s"],
        },
        "claim_boundary": (
            "retrospective source-feature amplitude-law diagnostic with train-only grouped CV; "
            "not prospective, not a parent derivation, and no channel/Tau validation"
        ),
    }
    (DATA / "body_amplitude_law_score_v01.json").write_text(json.dumps(result, indent=2)+"\n")
    scores.to_csv(DATA / "body_amplitude_law_scores_by_galaxy_v01.csv", index=False)
    REPORT.write_text(
        "# Source-feature body amplitude-law score v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"Train-grouped CV selected ridge alpha `{selected_alpha}`. On `{len(holdout)}` "
        f"holdout galaxies, the source-feature amplitude law beats wrong-family, Newton, "
        f"TPG/v6, and MOND in `{result['matched_vs_wrong']['win_fraction']:.3f}`, "
        f"`{result['matched_vs_newton']['win_fraction']:.3f}`, "
        f"`{result['matched_vs_tpg_v6']['win_fraction']:.3f}`, and "
        f"`{result['matched_vs_mond']['win_fraction']:.3f}`. Mean matched-minus-TPG and "
        f"matched-minus-MOND RMSE are `{result['matched_vs_tpg_v6']['mean_delta_km_s']:.3f}` "
        f"and `{result['matched_vs_mond']['mean_delta_km_s']:.3f} km/s`. This tests whether "
        "source morphology can predict response amplitude; it is not a first-principles law.\n"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
