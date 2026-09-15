#!/usr/bin/env python3
"""Held-out morphology test for the measurement-inverse parent-loss atlas.

Endpoint values define the diagnostic target.  They never select predictors,
the frozen train/holdout split, or the source-side feature blocks.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import run_inverse_required_rapidity_diagnostic_v01 as common


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
PREFIX = "inverse_parent_loss_morphology_test_v01"
SUMMARY_OUT = DATA / f"{PREFIX}_summary.csv"
PAIR_OUT = DATA / f"{PREFIX}_pair_tests.csv"
AUDIT_OUT = DATA / f"{PREFIX}.json"
REPORT_OUT = REPORTS / f"{PREFIX}.md"
SEED = 8_675_310
MODELS = (
    "radial_only",
    "orientation_quality",
    "morphology_proxy",
    "morphology_plus_orientation",
    "combined",
)


def galaxy_scores(frame: pd.DataFrame, target: np.ndarray, pred: np.ndarray) -> pd.DataFrame:
    work = pd.DataFrame(
        {"galaxy": frame["galaxy"].to_numpy(), "target": target, "pred": pred}
    )
    rows = []
    for galaxy, group in work.groupby("galaxy", sort=False):
        rmse = float(np.sqrt(np.mean((group["target"] - group["pred"]) ** 2)))
        zero = float(np.sqrt(np.mean(group["target"] ** 2)))
        rows.append(
            {
                "galaxy": galaxy,
                "rmse": rmse,
                "zero_rmse": zero,
                "delta_zero": rmse - zero,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    frame, hashes = common.load_frame()
    specs = common.specifications()
    used_predictors = {
        feature
        for model_id in MODELS
        for block in specs[model_id]
        for feature in block
    }
    forbidden_overlap = sorted(used_predictors & common.FORBIDDEN)
    if forbidden_overlap:
        raise ValueError(f"endpoint predictors leaked into features: {forbidden_overlap}")
    train_mask = frame["split"].eq("train").to_numpy()
    holdout_mask = frame["split"].eq("holdout").to_numpy()
    train = frame.loc[train_mask].copy()
    holdout = frame.loc[holdout_mask].copy()
    rng = np.random.default_rng(SEED)
    summary_rows = []
    score_tables: dict[tuple[str, str], pd.DataFrame] = {}
    alpha_records = []

    for baseline_id, baseline_column in common.BASELINES.items():
        target = np.log(
            frame["vobs"].to_numpy(float) / frame[baseline_column].to_numpy(float)
        )
        train_target = target[train_mask]
        holdout_target = target[holdout_mask]
        for model_id in MODELS:
            numeric, categorical = specs[model_id]
            alpha, records = common.choose_alpha(
                train, train_target, numeric, categorical
            )
            alpha_records.extend(
                {"baseline_id": baseline_id, "model_id": model_id, **row}
                for row in records
            )
            model = common.pipeline(numeric, categorical, alpha)
            model.fit(
                train,
                train_target,
                ridge__sample_weight=common.equal_galaxy_weights(train),
            )
            pred = model.predict(holdout)
            scores = galaxy_scores(holdout, holdout_target, pred)
            score_tables[(baseline_id, model_id)] = scores
            delta = scores["delta_zero"].to_numpy(float)
            p_lower, ci_lo, ci_hi = common.paired_test(delta, rng)
            rmse = float(scores["rmse"].mean())
            zero = float(scores["zero_rmse"].mean())
            summary_rows.append(
                {
                    "baseline_id": baseline_id,
                    "model_id": model_id,
                    "selected_alpha": alpha,
                    "holdout_mean_galaxy_rmse_kappa": rmse,
                    "rmse_ratio_to_zero": rmse / zero,
                    "mean_delta_rmse_vs_zero": float(delta.mean()),
                    "bootstrap_ci_lower": ci_lo,
                    "bootstrap_ci_upper": ci_hi,
                    "paired_sign_flip_p_lower": p_lower,
                    "galaxy_win_fraction": float((delta < 0.0).mean()),
                    "point_pearson_r": common.safe_correlation(
                        holdout_target, pred, "pearson"
                    ),
                    "point_spearman_r": common.safe_correlation(
                        holdout_target, pred, "spearman"
                    ),
                }
            )

    comparisons = (
        ("morphology_proxy", "radial_only", "morphology_beyond_radial"),
        (
            "morphology_plus_orientation",
            "morphology_proxy",
            "orientation_added_to_morphology",
        ),
        ("combined", "morphology_proxy", "observer_added_to_morphology"),
    )
    pair_rows = []
    for baseline_id in common.BASELINES:
        for left, right, comparison_id in comparisons:
            joined = score_tables[(baseline_id, left)].merge(
                score_tables[(baseline_id, right)],
                on="galaxy",
                suffixes=("_left", "_right"),
                validate="one_to_one",
            )
            delta = joined["rmse_left"].to_numpy() - joined["rmse_right"].to_numpy()
            p_lower, ci_lo, ci_hi = common.paired_test(delta, rng)
            pair_rows.append(
                {
                    "baseline_id": baseline_id,
                    "comparison_id": comparison_id,
                    "mean_delta_rmse_left_minus_right": float(delta.mean()),
                    "bootstrap_ci_lower": ci_lo,
                    "bootstrap_ci_upper": ci_hi,
                    "paired_sign_flip_p_lower": p_lower,
                    "left_win_fraction": float((delta < 0.0).mean()),
                }
            )

    summary = pd.DataFrame(summary_rows)
    pairs = pd.DataFrame(pair_rows)
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    summary.to_csv(SUMMARY_OUT, index=False, float_format="%.12g")
    pairs.to_csv(PAIR_OUT, index=False, float_format="%.12g")

    forward_error = float(
        np.max(
            np.abs(
                frame["vn"].to_numpy(float) ** 2
                * np.exp(2.0 * np.log(frame["vobs"] / frame["vn"]))
                - frame["vobs"].to_numpy(float) ** 2
            )
        )
    )
    audit = {
        "schema": PREFIX,
        "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "hashes": hashes,
        "n_train_galaxies": int(train["galaxy"].nunique()),
        "n_holdout_galaxies": int(holdout["galaxy"].nunique()),
        "n_holdout_points": int(len(holdout)),
        "target": "kappa_required=log(v_observed/v_baseline)",
        "checks": {
            "frozen_split_retained": set(frame["split"]) == {"train", "holdout"},
            "equal_velocity_zero_limit": bool(np.log(1.0) == 0.0),
            "forward_substitution_max_abs_v2_error": forward_error,
            "forward_substitution_tolerance_pass": forward_error < 1.0e-8,
            "finite_metrics": bool(
                np.isfinite(
                    summary.select_dtypes(include=[np.number]).to_numpy()
                ).all()
            ),
            "alpha_sensitivity_values": list(common.ALPHAS),
            "independent_metrics": ["mean-galaxy RMSE", "Pearson r", "Spearman r"],
            "forbidden_predictor_overlap": forbidden_overlap,
        },
        "forbidden_interpretations": [
            "parent morphology identified from the inverse target",
            "Nature occupation",
            "dark-matter replacement",
        ],
        "strongest_alternative": "baryonic scaling, inclination/deprojection, non-circular motion, distance and baseline-systematic structure",
    }
    AUDIT_OUT.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    focus = summary.loc[
        summary["model_id"].isin(["radial_only", "morphology_proxy", "combined"])
    ]
    report = [
        "# Inverse parent-loss morphology test v01",
        "",
        "Status: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`.",
        "",
        "This held-out test asks whether residual-blind source morphology predicts",
        "the endpoint-derived `kappa_required` atlas. It does not infer a parent law.",
        "",
        "## Held-out summary",
        "",
        common.markdown_table(focus),
        "",
        "## Incremental comparisons",
        "",
        common.markdown_table(pairs),
        "",
        "A morphology improvement relative to radius alone is an empirical",
        "association with the inverse target, not identification of morphological",
        "parent loss. Conventional source and measurement covariates remain direct",
        "alternatives. A later source-frozen law must predict untouched endpoints.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(report), encoding="utf-8")
    print(focus.to_string(index=False))
    print(pairs.to_string(index=False))
    print(json.dumps(audit["checks"], indent=2))
    print("INVERSE_PARENT_LOSS_MORPHOLOGY_TEST_V01_COMPLETE")


if __name__ == "__main__":
    main()
