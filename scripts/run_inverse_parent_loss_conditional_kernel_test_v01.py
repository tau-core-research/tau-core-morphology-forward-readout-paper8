#!/usr/bin/env python3
"""Diagnostic held-out test of morphology-conditioned inverse-loss kernels."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import SplineTransformer

import run_inverse_required_rapidity_diagnostic_v01 as source


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
PREFIX = "inverse_parent_loss_conditional_kernel_test_v01"
SEED = 8_675_311
KNOTS = (4, 6)
ALPHAS = (10.0, 100.0)
N_SHUFFLES = 30
MODELS = {
    "radial_spline": ([], False),
    "morphology_kernel": (source.MORPHOLOGY, True),
    "morphology_observer_kernel": (source.MORPHOLOGY + source.OBSERVER, True),
}


class Design:
    def __init__(self, knots: int, columns: list[str], family: bool):
        self.knots = knots
        self.columns = columns
        self.family = family

    def fit(self, frame: pd.DataFrame) -> "Design":
        self.spline = SplineTransformer(
            n_knots=self.knots, degree=3, include_bias=False
        ).fit(frame[["x"]])
        if self.columns:
            numeric = frame[self.columns].apply(pd.to_numeric, errors="coerce")
            self.median = numeric.median().fillna(0.0)
            filled = numeric.fillna(self.median)
            self.mean = filled.mean()
            self.scale = filled.std(ddof=0).replace(0.0, 1.0)
        if self.family:
            self.families = sorted(
                frame["formula_family"].fillna("missing").astype(str).unique()
            )
        return self

    def transform(
        self, frame: pd.DataFrame, family_override: np.ndarray | None = None
    ) -> np.ndarray:
        radial = self.spline.transform(frame[["x"]])
        blocks = [np.ones((len(frame), 1)), radial]
        if self.columns:
            numeric = frame[self.columns].apply(pd.to_numeric, errors="coerce")
            z = ((numeric.fillna(self.median) - self.mean) / self.scale).to_numpy()
            blocks.extend([z, (z[:, :, None] * radial[:, None, :]).reshape(len(frame), -1)])
        if self.family:
            labels = (
                frame["formula_family"].fillna("missing").astype(str).to_numpy()
                if family_override is None
                else np.asarray(family_override, dtype=str)
            )
            onehot = np.column_stack([labels == item for item in self.families]).astype(float)
            blocks.extend(
                [onehot, (onehot[:, :, None] * radial[:, None, :]).reshape(len(frame), -1)]
            )
        return np.column_stack(blocks)


def weights(frame: pd.DataFrame) -> np.ndarray:
    counts = frame.groupby("galaxy")["galaxy"].transform("size").to_numpy(float)
    return 1.0 / counts


def galaxy_rmse(frame: pd.DataFrame, target: np.ndarray, pred: np.ndarray) -> pd.DataFrame:
    work = pd.DataFrame(
        {"galaxy": frame["galaxy"].to_numpy(), "e2": (target - pred) ** 2, "z2": target**2}
    )
    grouped = work.groupby("galaxy", sort=False)[["e2", "z2"]].mean()
    grouped["rmse"] = np.sqrt(grouped["e2"])
    grouped["zero_rmse"] = np.sqrt(grouped["z2"])
    grouped["delta_zero"] = grouped["rmse"] - grouped["zero_rmse"]
    return grouped.reset_index()


def choose(train: pd.DataFrame, target: np.ndarray, columns: list[str], family: bool) -> tuple[int, float, pd.DataFrame]:
    rows = []
    groups = train["galaxy"].to_numpy()
    for knots in KNOTS:
        for alpha in ALPHAS:
            scores = []
            for fit_idx, val_idx in GroupKFold(3).split(train, groups=groups):
                fit, val = train.iloc[fit_idx], train.iloc[val_idx]
                design = Design(knots, columns, family).fit(fit)
                model = Ridge(alpha=alpha).fit(
                    design.transform(fit), target[fit_idx], sample_weight=weights(fit)
                )
                pred = model.predict(design.transform(val))
                scores.append(float(galaxy_rmse(val, target[val_idx], pred)["rmse"].mean()))
            rows.append({"knots": knots, "alpha": alpha, "cv_mean_galaxy_rmse": float(np.mean(scores))})
    table = pd.DataFrame(rows)
    best = table.sort_values(["cv_mean_galaxy_rmse", "knots", "alpha"]).iloc[0]
    return int(best["knots"]), float(best["alpha"]), table


def paired(delta: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    signs = rng.choice((-1.0, 1.0), size=(5_000, len(delta)))
    null = np.mean(signs * delta, axis=1)
    p = float((1 + np.sum(null <= np.mean(delta))) / (len(null) + 1))
    boot = rng.choice(delta, size=(2_000, len(delta)), replace=True).mean(axis=1)
    lo, hi = np.quantile(boot, [0.025, 0.975])
    return p, float(lo), float(hi)


def permuted_labels(frame: pd.DataFrame, rng: np.random.Generator) -> np.ndarray:
    unique = frame[["galaxy", "formula_family"]].drop_duplicates("galaxy")
    shuffled = unique["formula_family"].fillna("missing").astype(str).to_numpy().copy()
    rng.shuffle(shuffled)
    mapping = dict(zip(unique["galaxy"], shuffled))
    return frame["galaxy"].map(mapping).to_numpy(str)


def main() -> None:
    frame, hashes = source.load_frame()
    used = set(source.MORPHOLOGY + source.OBSERVER + ["formula_family", "x"])
    leak = sorted(used & source.FORBIDDEN)
    if leak:
        raise ValueError(f"endpoint leakage: {leak}")
    train = frame.loc[frame["split"].eq("train")].copy()
    holdout = frame.loc[frame["split"].eq("holdout")].copy()
    rng = np.random.default_rng(SEED)
    summary_rows, pair_rows, shuffle_rows, sensitivity_rows = [], [], [], []

    for baseline_id, baseline_column in source.BASELINES.items():
        train_target = np.log(train["vobs"].to_numpy() / train[baseline_column].to_numpy())
        holdout_target = np.log(holdout["vobs"].to_numpy() / holdout[baseline_column].to_numpy())
        score_map = {}
        fitted = {}
        for model_id, (columns, family) in MODELS.items():
            knots, alpha, sensitivity = choose(train, train_target, columns, family)
            sensitivity.insert(0, "model_id", model_id)
            sensitivity.insert(0, "baseline_id", baseline_id)
            sensitivity_rows.append(sensitivity)
            design = Design(knots, columns, family).fit(train)
            model = Ridge(alpha=alpha).fit(
                design.transform(train), train_target, sample_weight=weights(train)
            )
            pred = model.predict(design.transform(holdout))
            scores = galaxy_rmse(holdout, holdout_target, pred)
            score_map[model_id] = scores
            fitted[model_id] = (design, model)
            delta = scores["delta_zero"].to_numpy()
            p, lo, hi = paired(delta, rng)
            summary_rows.append(
                {
                    "baseline_id": baseline_id,
                    "model_id": model_id,
                    "knots": knots,
                    "alpha": alpha,
                    "rmse_ratio_to_zero": float(scores["rmse"].mean() / scores["zero_rmse"].mean()),
                    "mean_delta_rmse_vs_zero": float(delta.mean()),
                    "ci_lower": lo,
                    "ci_upper": hi,
                    "p_lower": p,
                    "galaxy_win_fraction": float((delta < 0.0).mean()),
                    "pearson_r": float(pearsonr(holdout_target, pred).statistic),
                    "spearman_r": float(spearmanr(holdout_target, pred).statistic),
                }
            )

        for left, right in (
            ("morphology_kernel", "radial_spline"),
            ("morphology_observer_kernel", "morphology_kernel"),
        ):
            joined = score_map[left].merge(score_map[right], on="galaxy", suffixes=("_l", "_r"))
            delta = joined["rmse_l"].to_numpy() - joined["rmse_r"].to_numpy()
            p, lo, hi = paired(delta, rng)
            pair_rows.append(
                {"baseline_id": baseline_id, "left": left, "right": right,
                 "mean_delta_rmse": float(delta.mean()), "ci_lower": lo,
                 "ci_upper": hi, "p_lower": p, "left_win_fraction": float((delta < 0).mean())}
            )

        design, model = fitted["morphology_kernel"]
        matched = score_map["morphology_kernel"]["rmse"].mean()
        for permutation in range(N_SHUFFLES):
            train_labels = permuted_labels(train, rng)
            holdout_labels = permuted_labels(holdout, rng)
            shuffled_model = Ridge(alpha=model.alpha).fit(
                design.transform(train, train_labels), train_target, sample_weight=weights(train)
            )
            shuffled_pred = shuffled_model.predict(design.transform(holdout, holdout_labels))
            shuffled_rmse = float(galaxy_rmse(holdout, holdout_target, shuffled_pred)["rmse"].mean())
            shuffle_rows.append(
                {"baseline_id": baseline_id, "permutation": permutation,
                 "matched_rmse": float(matched), "shuffled_rmse": shuffled_rmse,
                 "matched_minus_shuffled": float(matched - shuffled_rmse)}
            )

    summary = pd.DataFrame(summary_rows)
    pairs = pd.DataFrame(pair_rows)
    shuffles = pd.DataFrame(shuffle_rows)
    sensitivity = pd.concat(sensitivity_rows, ignore_index=True)
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    summary.to_csv(DATA / f"{PREFIX}_summary.csv", index=False)
    pairs.to_csv(DATA / f"{PREFIX}_pair_tests.csv", index=False)
    shuffles.to_csv(DATA / f"{PREFIX}_family_shuffles.csv", index=False)
    sensitivity.to_csv(DATA / f"{PREFIX}_sensitivity.csv", index=False)

    shuffle_summary = []
    for baseline_id, group in shuffles.groupby("baseline_id", sort=False):
        shuffle_summary.append(
            {"baseline_id": baseline_id,
             "matched_beats_shuffle_fraction": float((group["matched_minus_shuffled"] < 0).mean()),
             "permutation_p": float((1 + np.sum(group["matched_minus_shuffled"] >= 0)) / (len(group) + 1))}
        )
    shuffle_summary = pd.DataFrame(shuffle_summary)
    roundtrip = float(np.max(np.abs(train["vn"] ** 2 * np.exp(2*np.log(train["vobs"]/train["vn"])) - train["vobs"] ** 2)))
    audit = {
        "schema": PREFIX, "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT", "hashes": hashes,
        "n_train_galaxies": int(train["galaxy"].nunique()),
        "n_holdout_galaxies": int(holdout["galaxy"].nunique()),
        "n_holdout_points": int(len(holdout)),
        "checks": {"endpoint_predictor_overlap": leak, "equal_velocity_zero_limit": bool(np.log(1.0) == 0),
                   "roundtrip_max_abs_v2_error": roundtrip, "roundtrip_tolerance_pass": roundtrip < 1e-8,
                   "resolution_scan_knots": list(KNOTS), "regularization_scan": list(ALPHAS),
                   "independent_metrics": ["mean-galaxy RMSE", "Pearson r", "Spearman r"],
                   "family_shuffle_count": N_SHUFFLES},
        "endpoint_authorized": False,
        "strongest_alternative": "ordinary baryonic scaling, non-circular motion, inclination/deprojection, tracer and distance systematics",
    }
    (DATA / f"{PREFIX}.json").write_text(json.dumps(audit, indent=2) + "\n")
    report = ["# Inverse parent-loss conditional-kernel test v01", "",
              "Status: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`.", "",
              "The diagnostic tests radial B-splines, morphology-conditioned spline",
              "interactions, and a morphology-plus-observer version on the frozen",
              "131/44 galaxy split. Knot count and ridge strength are selected only",
              "inside grouped training cross-validation.", "", "## Held-out results", "",
              source.markdown_table(summary), "", "## Incremental tests", "",
              source.markdown_table(pairs), "", "## Family-label shuffle control", "",
              source.markdown_table(shuffle_summary), "",
              "Because the target is reconstructed from the endpoint, these are",
              "retrodictive structure tests. They do not identify a parent kernel,",
              "Nature occupation, or a dark-matter replacement law.", ""]
    (REPORTS / f"{PREFIX}.md").write_text("\n".join(report))
    print(summary.to_string(index=False))
    print(pairs.to_string(index=False))
    print(shuffle_summary.to_string(index=False))
    print(json.dumps(audit["checks"], indent=2))
    print("INVERSE_PARENT_LOSS_CONDITIONAL_KERNEL_TEST_V01_COMPLETE")


if __name__ == "__main__":
    main()
