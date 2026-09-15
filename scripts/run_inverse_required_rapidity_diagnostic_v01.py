#!/usr/bin/env python3
"""Held-out inverse required-rapidity diagnostic for the frozen SPARC packet.

The endpoint is intentionally used to reconstruct a terminal-equivalent target.
Nothing produced here is a physical Tau kernel or an endpoint promotion.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "figures"
PAPER_FIGURES = ROOT / "paper8_submission_source" / "figures"
TPG_POINTS = Path(
    "/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1/"
    "tau_rotation_curve_frozen_proxy_runner_v0_points.csv"
)

PREFIX = "inverse_required_rapidity_diagnostic_v01"
POINTS_OUT = DATA / f"{PREFIX}_points.csv"
GALAXY_OUT = DATA / f"{PREFIX}_galaxy_scores.csv"
SUMMARY_OUT = DATA / f"{PREFIX}_summary.csv"
PAIR_OUT = DATA / f"{PREFIX}_model_pair_tests.csv"
ALPHA_OUT = DATA / f"{PREFIX}_alpha_sensitivity.csv"
AUDIT_OUT = DATA / f"{PREFIX}_audit.json"
REPORT_OUT = REPORTS / f"{PREFIX}.md"
FIGURE_OUT = FIGURES / f"fig_{PREFIX}.png"
PAPER_FIGURE_OUT = PAPER_FIGURES / FIGURE_OUT.name

C_KMS = 299_792.458
C_CONTROL_KMS = 300_000.0
ALPHAS = (0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)
N_SIGN_FLIPS = 50_000
N_BOOTSTRAPS = 10_000
SEED = 8_675_309

BASELINES = {
    "newtonian_baryonic": "vn",
    "tpg_v6": "v_v6",
    "mond_fixed": "v_mond",
}
RADIAL = ["x", "x2", "x3"]
DISTANCE = ["log_distance_mpc", "distance_frac_error"]
ORIENTATION_QUALITY = ["Inc_deg", "e_Inc_deg", "Q"]
OBSERVER = DISTANCE + ORIENTATION_QUALITY
MORPHOLOGY = [
    "T",
    "log_rdisk_kpc",
    "SBdisk_Lsun_pc2",
    "log_mhi",
    "log_rhi_kpc",
    "gas_frac",
    "bulge_frac",
    "total_gas_fraction",
    "log_sbdisk",
    "log_sb_peak",
    "manifest_confidence",
    "scale_radius_proxy_kpc",
    "thickness_h_over_rs_proxy",
]
FORBIDDEN = {
    "vobs",
    "resid_v6",
    "resid_mond",
    "resid_tau_proxy",
    "required_S_tau",
    "q_required",
    "u_required_kms",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_frame() -> tuple[pd.DataFrame, dict[str, str]]:
    master_path = DATA / "external_sparc_master_table.csv"
    labels_path = DATA / "source_native_readout_formula_labels.csv"
    for path in (TPG_POINTS, master_path, labels_path):
        if not path.exists():
            raise FileNotFoundError(path)
    points = pd.read_csv(TPG_POINTS)
    master = pd.read_csv(master_path).rename(columns={"Galaxy": "galaxy"})
    labels = pd.read_csv(labels_path)[
        [
            "galaxy",
            "formula_family",
            "manifest_confidence",
            "distance_frac_error",
            "scale_radius_proxy_kpc",
            "thickness_h_over_rs_proxy",
        ]
    ]
    frame = points.merge(master, on="galaxy", how="left", validate="many_to_one")
    frame = frame.merge(labels, on="galaxy", how="left", validate="many_to_one")
    frame["rmax_kpc"] = frame.groupby("galaxy")["r"].transform("max")
    frame["x"] = frame["r"] / frame["rmax_kpc"].replace(0.0, np.nan)
    frame["x2"] = frame["x"] ** 2
    frame["x3"] = frame["x"] ** 3
    frame["log_distance_mpc"] = np.log1p(frame["D_Mpc"].clip(lower=0.0))
    frame["distance_frac_error"] = (
        frame["e_D_Mpc"] / frame["D_Mpc"].replace(0.0, np.nan)
    ).fillna(frame["distance_frac_error"])
    frame["log_rdisk_kpc"] = np.log1p(frame["Rdisk_kpc"].clip(lower=0.0))
    frame["log_mhi"] = np.log1p(frame["MHI_1e9Msun"].clip(lower=0.0))
    frame["log_rhi_kpc"] = np.log1p(frame["RHI_kpc"].clip(lower=0.0))
    for column in OBSERVER + MORPHOLOGY:
        frame[f"x__{column}"] = frame["x"] * frame[column]
        frame[f"x2__{column}"] = frame["x2"] * frame[column]
    required = {"galaxy", "split", "r", "vobs", "vn", "v_v6", "v_mond", "errv"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    if set(frame["split"].unique()) != {"train", "holdout"}:
        raise ValueError("the frozen train/holdout split is missing")
    if frame[["vobs", "vn", "v_v6", "v_mond", "r"]].isna().any().any():
        raise ValueError("required endpoint values contain missing entries")
    return frame, {
        "tpg_points_sha256": sha256(TPG_POINTS),
        "sparc_master_sha256": sha256(master_path),
        "formula_labels_sha256": sha256(labels_path),
    }


def expanded(features: list[str]) -> list[str]:
    return (
        features
        + [f"x__{column}" for column in features]
        + [f"x2__{column}" for column in features]
    )


def specifications() -> dict[str, tuple[list[str], list[str]]]:
    return {
        "radial_only": (RADIAL, []),
        "distance_context": (RADIAL + expanded(DISTANCE), []),
        "orientation_quality": (RADIAL + expanded(ORIENTATION_QUALITY), []),
        "observer_geometry": (RADIAL + expanded(OBSERVER), []),
        "morphology_proxy": (RADIAL + expanded(MORPHOLOGY), ["formula_family"]),
        "morphology_plus_distance": (
            RADIAL + expanded(MORPHOLOGY) + expanded(DISTANCE),
            ["formula_family"],
        ),
        "morphology_plus_orientation": (
            RADIAL + expanded(MORPHOLOGY) + expanded(ORIENTATION_QUALITY),
            ["formula_family"],
        ),
        "combined": (
            RADIAL + expanded(OBSERVER) + expanded(MORPHOLOGY),
            ["formula_family"],
        ),
    }


def pipeline(numeric: list[str], categorical: list[str], alpha: float) -> Pipeline:
    transformers = []
    if numeric:
        transformers.append(
            (
                "numeric",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                numeric,
            )
        )
    if categorical:
        transformers.append(
            (
                "categorical",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        (
                            "encode",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=True),
                        ),
                    ]
                ),
                categorical,
            )
        )
    return Pipeline(
        [
            ("preprocess", ColumnTransformer(transformers)),
            ("ridge", Ridge(alpha=alpha)),
        ]
    )


def equal_galaxy_weights(frame: pd.DataFrame) -> np.ndarray:
    counts = frame.groupby("galaxy")["galaxy"].transform("size").to_numpy(float)
    return 1.0 / counts


def mean_galaxy_rmse(
    frame: pd.DataFrame, target: np.ndarray, prediction: np.ndarray
) -> float:
    work = pd.DataFrame(
        {
            "galaxy": frame["galaxy"].to_numpy(),
            "e2": (target - prediction) ** 2,
        }
    )
    return float(np.sqrt(work.groupby("galaxy")["e2"].mean()).mean())


def choose_alpha(
    train: pd.DataFrame,
    target: np.ndarray,
    numeric: list[str],
    categorical: list[str],
) -> tuple[float, list[dict[str, float]]]:
    splitter = GroupKFold(n_splits=5)
    groups = train["galaxy"].to_numpy()
    rows = []
    for alpha in ALPHAS:
        fold_scores = []
        for fold, (fit_index, valid_index) in enumerate(
            splitter.split(train, groups=groups), start=1
        ):
            fit = train.iloc[fit_index]
            valid = train.iloc[valid_index]
            model = pipeline(numeric, categorical, alpha)
            model.fit(
                fit,
                target[fit_index],
                ridge__sample_weight=equal_galaxy_weights(fit),
            )
            score = mean_galaxy_rmse(
                valid, target[valid_index], model.predict(valid)
            )
            fold_scores.append(score)
            rows.append({"alpha": alpha, "fold": fold, "cv_rmse_kms": score})
        rows.append(
            {
                "alpha": alpha,
                "fold": 0,
                "cv_rmse_kms": float(np.mean(fold_scores)),
            }
        )
    mean_rows = [row for row in rows if row["fold"] == 0]
    selected = min(mean_rows, key=lambda row: row["cv_rmse_kms"])
    return float(selected["alpha"]), rows


def paired_test(
    differences: np.ndarray, rng: np.random.Generator
) -> tuple[float, float, float]:
    values = np.asarray(differences, dtype=float)
    observed = float(np.mean(values))
    signs = rng.choice((-1.0, 1.0), size=(N_SIGN_FLIPS, len(values)))
    null = np.mean(signs * values[None, :], axis=1)
    p_lower = float((1 + np.sum(null <= observed)) / (N_SIGN_FLIPS + 1))
    bootstrap = rng.choice(values, size=(N_BOOTSTRAPS, len(values)), replace=True)
    lower, upper = np.quantile(np.mean(bootstrap, axis=1), [0.025, 0.975])
    return p_lower, float(lower), float(upper)


def galaxy_score_table(
    holdout: pd.DataFrame,
    target: np.ndarray,
    prediction: np.ndarray,
    baseline_id: str,
    model_id: str,
) -> pd.DataFrame:
    work = pd.DataFrame(
        {
            "galaxy": holdout["galaxy"].to_numpy(),
            "target": target,
            "prediction": prediction,
        }
    )
    rows = []
    for galaxy, subset in work.groupby("galaxy"):
        rmse_model = float(
            np.sqrt(np.mean((subset["target"] - subset["prediction"]) ** 2))
        )
        rmse_zero = float(np.sqrt(np.mean(subset["target"] ** 2)))
        rows.append(
            {
                "baseline_id": baseline_id,
                "model_id": model_id,
                "galaxy": galaxy,
                "n_points": int(len(subset)),
                "rmse_model_kms": rmse_model,
                "rmse_zero_kms": rmse_zero,
                "delta_rmse_model_minus_zero_kms": rmse_model - rmse_zero,
                "model_beats_zero": rmse_model < rmse_zero,
                "mean_required_u_kms": float(subset["target"].mean()),
                "mean_predicted_u_kms": float(subset["prediction"].mean()),
            }
        )
    return pd.DataFrame(rows)


def safe_correlation(
    target: np.ndarray, prediction: np.ndarray, method: str
) -> float:
    if np.std(target) == 0.0 or np.std(prediction) == 0.0:
        return float("nan")
    if method == "pearson":
        return float(pearsonr(target, prediction).statistic)
    return float(spearmanr(target, prediction).statistic)


def markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in frame.iterrows():
        values = []
        for column in columns:
            value = row[column]
            values.append(f"{value:.6g}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def draw_figure(points: pd.DataFrame, summary: pd.DataFrame) -> None:
    figure, axes = plt.subplots(2, 3, figsize=(13, 7.2), constrained_layout=True)
    order = ["radial_only", "observer_geometry", "morphology_proxy", "combined"]
    for column, baseline_id in enumerate(BASELINES):
        subset = points.loc[
            (points["baseline_id"] == baseline_id)
            & (points["model_id"] == "combined")
            & (points["split"] == "holdout")
        ]
        ax = axes[0, column]
        ax.scatter(
            subset["u_required_kms"],
            subset["u_predicted_kms"],
            s=8,
            alpha=0.35,
            edgecolors="none",
        )
        joined = np.r_[
            subset["u_required_kms"].to_numpy(),
            subset["u_predicted_kms"].to_numpy(),
        ]
        limits = np.quantile(joined, [0.01, 0.99])
        ax.plot(limits, limits, color="black", linestyle="--", linewidth=1)
        ax.set_xlim(limits)
        ax.set_ylim(limits)
        ax.set_title(baseline_id.replace("_", " "))
        ax.set_xlabel("required equivalent rapidity c q_req [km/s]")
        if column == 0:
            ax.set_ylabel("held-out prediction [km/s]")

        ax = axes[1, column]
        metric = (
            summary.loc[summary["baseline_id"] == baseline_id]
            .set_index("model_id")
            .loc[order]
        )
        ax.bar(
            range(4),
            metric["rmse_ratio_to_zero"],
            color=["#777777", "#4C78A8", "#F58518", "#54A24B"],
        )
        ax.axhline(1.0, color="black", linestyle="--", linewidth=1)
        ax.set_xticks(range(4), ["radial", "observer", "morph.", "combined"], rotation=20)
        ax.set_ylabel("mean-galaxy RMSE / zero-channel RMSE")
        ax.set_ylim(0, max(1.1, float(metric["rmse_ratio_to_zero"].max()) * 1.08))
    figure.suptitle(
        "Inverse required-rapidity diagnostic: held-out prediction, not a physical kernel"
    )
    FIGURE_OUT.parent.mkdir(parents=True, exist_ok=True)
    PAPER_FIGURE_OUT.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_OUT, dpi=180)
    figure.savefig(PAPER_FIGURE_OUT, dpi=180)
    plt.close(figure)


def main() -> None:
    frame, hashes = load_frame()
    specs = specifications()
    used = {
        feature
        for numeric, categorical in specs.values()
        for feature in numeric + categorical
    }
    forbidden_overlap = sorted(used & FORBIDDEN)
    if forbidden_overlap:
        raise ValueError(f"endpoint predictors leaked into features: {forbidden_overlap}")

    train_mask = frame["split"].eq("train").to_numpy()
    holdout_mask = frame["split"].eq("holdout").to_numpy()
    train = frame.loc[train_mask].copy()
    holdout = frame.loc[holdout_mask].copy()
    rng = np.random.default_rng(SEED)

    points_frames = []
    galaxy_frames = []
    summary_rows = []
    alpha_rows = []
    exact_linear_errors = {}
    c_control_errors = {}

    for baseline_id, baseline_column in BASELINES.items():
        observed_beta = frame["vobs"].to_numpy(float) / C_KMS
        baseline_beta = frame[baseline_column].to_numpy(float) / C_KMS
        q_required = np.arctanh(observed_beta) - np.arctanh(baseline_beta)
        u_required = C_KMS * q_required
        linear = frame["vobs"].to_numpy(float) - frame[baseline_column].to_numpy(float)
        exact_linear_errors[baseline_id] = float(np.max(np.abs(u_required - linear)))
        q_control = np.arctanh(frame["vobs"].to_numpy(float) / C_CONTROL_KMS)
        q_control -= np.arctanh(frame[baseline_column].to_numpy(float) / C_CONTROL_KMS)
        c_control_errors[baseline_id] = float(
            np.max(np.abs(u_required - C_CONTROL_KMS * q_control))
        )
        train_target = u_required[train_mask]
        holdout_target = u_required[holdout_mask]

        for model_id, (numeric, categorical) in specs.items():
            selected_alpha, alpha_records = choose_alpha(
                train, train_target, numeric, categorical
            )
            for record in alpha_records:
                alpha_rows.append(
                    {"baseline_id": baseline_id, "model_id": model_id, **record}
                )
            model = pipeline(numeric, categorical, selected_alpha)
            model.fit(
                train,
                train_target,
                ridge__sample_weight=equal_galaxy_weights(train),
            )
            prediction = model.predict(frame)
            holdout_prediction = prediction[holdout_mask]
            scores = galaxy_score_table(
                holdout,
                holdout_target,
                holdout_prediction,
                baseline_id,
                model_id,
            )
            galaxy_frames.append(scores)
            delta = scores["delta_rmse_model_minus_zero_kms"].to_numpy()
            p_lower, ci_lower, ci_upper = paired_test(delta, rng)
            rmse_model = float(scores["rmse_model_kms"].mean())
            rmse_zero = float(scores["rmse_zero_kms"].mean())
            cv_score = next(
                record["cv_rmse_kms"]
                for record in alpha_records
                if record["fold"] == 0 and record["alpha"] == selected_alpha
            )
            summary_rows.append(
                {
                    "baseline_id": baseline_id,
                    "model_id": model_id,
                    "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
                    "n_train_galaxies": int(train["galaxy"].nunique()),
                    "n_holdout_galaxies": int(holdout["galaxy"].nunique()),
                    "n_holdout_points": int(len(holdout)),
                    "selected_alpha": selected_alpha,
                    "train_group_cv_mean_galaxy_rmse_kms": cv_score,
                    "holdout_mean_galaxy_rmse_model_kms": rmse_model,
                    "holdout_mean_galaxy_rmse_zero_kms": rmse_zero,
                    "rmse_ratio_to_zero": rmse_model / rmse_zero,
                    "mean_delta_rmse_model_minus_zero_kms": float(np.mean(delta)),
                    "delta_rmse_bootstrap_ci_lower_kms": ci_lower,
                    "delta_rmse_bootstrap_ci_upper_kms": ci_upper,
                    "paired_sign_flip_p_lower": p_lower,
                    "holdout_galaxy_win_fraction": float(
                        scores["model_beats_zero"].mean()
                    ),
                    "holdout_point_pearson_r": safe_correlation(
                        holdout_target, holdout_prediction, "pearson"
                    ),
                    "holdout_point_spearman_r": safe_correlation(
                        holdout_target, holdout_prediction, "spearman"
                    ),
                }
            )
            points_frames.append(
                pd.DataFrame(
                    {
                        "baseline_id": baseline_id,
                        "model_id": model_id,
                        "galaxy": frame["galaxy"],
                        "split": frame["split"],
                        "r_kpc": frame["r"],
                        "x_r_over_rmax": frame["x"],
                        "v_observed_kms": frame["vobs"],
                        "v_baseline_kms": frame[baseline_column],
                        "q_required": q_required,
                        "u_required_kms": u_required,
                        "u_predicted_kms": prediction,
                    }
                )
            )

    points = pd.concat(points_frames, ignore_index=True)
    galaxies = pd.concat(galaxy_frames, ignore_index=True)
    summary = pd.DataFrame(summary_rows)
    alpha_sensitivity = pd.DataFrame(alpha_rows)

    comparisons = [
        ("distance_context", "radial_only", "distance_beyond_radial"),
        ("orientation_quality", "radial_only", "orientation_beyond_radial"),
        ("observer_geometry", "radial_only", "observer_beyond_radial"),
        ("morphology_proxy", "radial_only", "morphology_beyond_radial"),
        (
            "morphology_plus_distance",
            "morphology_proxy",
            "distance_added_to_morphology",
        ),
        (
            "morphology_plus_orientation",
            "morphology_proxy",
            "orientation_added_to_morphology",
        ),
        ("combined", "morphology_proxy", "observer_added_to_morphology"),
        (
            "combined",
            "morphology_plus_orientation",
            "distance_added_after_orientation_and_morphology",
        ),
        (
            "combined",
            "morphology_plus_distance",
            "orientation_added_after_distance_and_morphology",
        ),
        ("combined", "observer_geometry", "morphology_added_to_observer"),
    ]
    pair_rows = []
    for baseline_id in BASELINES:
        subset = galaxies.loc[galaxies["baseline_id"] == baseline_id]
        for left, right, comparison_id in comparisons:
            left_rows = subset.loc[
                subset["model_id"] == left, ["galaxy", "rmse_model_kms"]
            ].rename(columns={"rmse_model_kms": "left_rmse"})
            right_rows = subset.loc[
                subset["model_id"] == right, ["galaxy", "rmse_model_kms"]
            ].rename(columns={"rmse_model_kms": "right_rmse"})
            joined = left_rows.merge(right_rows, on="galaxy", validate="one_to_one")
            delta = joined["left_rmse"].to_numpy() - joined["right_rmse"].to_numpy()
            p_lower, ci_lower, ci_upper = paired_test(delta, rng)
            pair_rows.append(
                {
                    "baseline_id": baseline_id,
                    "comparison_id": comparison_id,
                    "left_model": left,
                    "right_model": right,
                    "mean_delta_rmse_left_minus_right_kms": float(np.mean(delta)),
                    "bootstrap_ci_lower_kms": ci_lower,
                    "bootstrap_ci_upper_kms": ci_upper,
                    "paired_sign_flip_p_lower": p_lower,
                    "left_beats_right_galaxy_fraction": float(np.mean(delta < 0.0)),
                }
            )
    pair_tests = pd.DataFrame(pair_rows)

    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    point_index = [
        "baseline_id",
        "galaxy",
        "split",
        "r_kpc",
        "x_r_over_rmax",
        "v_observed_kms",
        "v_baseline_kms",
        "q_required",
        "u_required_kms",
    ]
    points_compact = (
        points.pivot_table(
            index=point_index,
            columns="model_id",
            values="u_predicted_kms",
            aggfunc="first",
        )
        .reset_index()
        .rename_axis(columns=None)
    )
    points_compact = points_compact.rename(
        columns={
            model_id: f"u_predicted_{model_id}_kms" for model_id in specs
        }
    )
    points_compact.to_csv(POINTS_OUT, index=False, float_format="%.12g")
    galaxies.to_csv(GALAXY_OUT, index=False, float_format="%.12g")
    summary.to_csv(SUMMARY_OUT, index=False, float_format="%.12g")
    pair_tests.to_csv(PAIR_OUT, index=False, float_format="%.12g")
    alpha_sensitivity.to_csv(ALPHA_OUT, index=False, float_format="%.12g")
    draw_figure(points, summary)

    def headline(baseline_id: str) -> dict[str, float]:
        row = summary.loc[
            (summary["baseline_id"] == baseline_id)
            & (summary["model_id"] == "combined")
        ].iloc[0]
        return {
            "rmse_ratio_to_zero": float(row["rmse_ratio_to_zero"]),
            "mean_delta_rmse_kms": float(
                row["mean_delta_rmse_model_minus_zero_kms"]
            ),
            "paired_sign_flip_p_lower": float(row["paired_sign_flip_p_lower"]),
            "holdout_point_pearson_r": float(row["holdout_point_pearson_r"]),
        }

    audit = {
        "schema": "tau_core_inverse_required_rapidity_diagnostic_v01",
        "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "formula": {
            "q_required": "atanh(v_observed/c)-atanh(v_baseline/c)",
            "u_required_kms": "c*q_required",
            "interpretation": (
                "terminal-equivalent inverse rapidity, not a physical Tau source kernel"
            ),
        },
        "frozen_packet": {
            "n_points": int(len(frame)),
            "n_galaxies": int(frame["galaxy"].nunique()),
            "n_train_galaxies": int(train["galaxy"].nunique()),
            "n_holdout_galaxies": int(holdout["galaxy"].nunique()),
            **hashes,
        },
        "predictor_policy": {
            "forbidden_overlap": forbidden_overlap,
            "holdout_used_for_tuning": False,
            "alpha_selection": "five-fold grouped CV on training galaxies only",
            "formula_family_status": (
                "residual-blind proxy, not externally promoted physical morphology"
            ),
            "distance_status": (
                "geometric proxy, not a measured instrument or parent-loss kernel"
            ),
        },
        "known_limit_and_numerics": {
            "equal_velocity_gives_zero_exactly": math.isclose(
                math.atanh(100.0 / C_KMS) - math.atanh(100.0 / C_KMS),
                0.0,
                abs_tol=0.0,
            ),
            "maximum_exact_minus_linear_kms": exact_linear_errors,
            "maximum_change_using_c_300000_kms": c_control_errors,
        },
        "headline_combined": {
            baseline_id: headline(baseline_id) for baseline_id in BASELINES
        },
        "observer_added_to_morphology": pair_tests.loc[
            pair_tests["comparison_id"] == "observer_added_to_morphology"
        ].to_dict(orient="records"),
        "strongest_alternatives": [
            "conventional baryonic scaling and the mass-discrepancy relation",
            "distance, beam, inclination, calibration and deprojection systematics",
            "smooth structure already absorbed by the TPG/v6 and MOND baselines",
        ],
        "claim_boundary": {
            "endpoint_allowed": False,
            "not_derived": [
                "physical q_tau(R)",
                "source-owned D_O(R)",
                "stable Q_OS",
                "body-versus-observer attribution",
                "distance-dependent parent loss",
                "Nature occupation",
                "dark-matter replacement law",
            ],
        },
    }
    AUDIT_OUT.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    display = summary[
        [
            "baseline_id",
            "model_id",
            "holdout_mean_galaxy_rmse_model_kms",
            "holdout_mean_galaxy_rmse_zero_kms",
            "rmse_ratio_to_zero",
            "mean_delta_rmse_model_minus_zero_kms",
            "delta_rmse_bootstrap_ci_lower_kms",
            "delta_rmse_bootstrap_ci_upper_kms",
            "paired_sign_flip_p_lower",
            "holdout_galaxy_win_fraction",
            "holdout_point_pearson_r",
        ]
    ]
    observer_display = pair_tests.loc[
        pair_tests["comparison_id"].isin(
            [
                "distance_added_to_morphology",
                "orientation_added_to_morphology",
                "observer_added_to_morphology",
                "distance_added_after_orientation_and_morphology",
            ]
        )
    ]
    report = [
        "# Inverse Required-Rapidity Diagnostic v0.1",
        "",
        "**Status:** DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "",
        "## Question and identity",
        "",
        "The observed endpoint is used deliberately to reconstruct the",
        "terminal-equivalent rapidity required relative to each baseline:",
        "",
        "$$",
        "q_{\\rm req}(R)=\\operatorname{artanh}[v_{\\rm obs}(R)/c]",
        "-\\operatorname{artanh}[v_{\\rm base}(R)/c],",
        "\\qquad u_{\\rm req}=c q_{\\rm req}.",
        "$$",
        "",
        "This is an exact inverse identity for the declared rapidity shell. It",
        "does not identify the physical source of the discrepancy.",
        "",
        "## Frozen protocol",
        "",
        f"- Galaxies: {frame['galaxy'].nunique()}; points: {len(frame)}.",
        f"- Training galaxies: {train['galaxy'].nunique()}; untouched holdout: {holdout['galaxy'].nunique()}.",
        "- Baselines: Newtonian baryonic, frozen TPG/v6 and fixed MOND.",
        "- Ridge strength: grouped cross-validation on training galaxies only.",
        "- Every galaxy has equal total training weight.",
        "- Endpoint values and residuals are forbidden predictors.",
        "- Morphology families are available-data proxies, not promoted labels.",
        "- Distance is geometric context, not a measured path-loss kernel.",
        "",
        "## Holdout results",
        "",
        markdown_table(display),
        "",
        "A ratio below one improves on the zero-additional-rapidity control.",
        "Randomization and bootstrap intervals use the 44 holdout galaxies.",
        "",
        "## Observer geometry added to morphology",
        "",
        markdown_table(observer_display),
        "",
        "## Interpretation",
        "",
        "The Newton-relative inverse target is substantially predictable, but",
        "ordinary baryonic scaling and the established mass-discrepancy relation",
        "are the stronger explanation. After TPG/v6 or MOND, the combined model",
        "shows only small holdout improvement and weak pointwise correlation.",
        "Observer-geometry proxies do not add a robust component beyond morphology.",
        "",
        "The informative result is therefore mostly negative: the current broad",
        "source and distance descriptors do not recover a stable universal",
        "post-TPG/MOND rapidity profile on unseen galaxies.",
        "",
        "## Claim boundary",
        "",
        "This result cannot separate body morphology, observer access, calibration,",
        "beam/deprojection systematics or baseline misspecification. It derives no",
        "physical Tau kernel, permits no endpoint promotion and supplies no",
        "dark-matter replacement law.",
        "",
        f"![Inverse rapidity diagnostic](../figures/{FIGURE_OUT.name})",
        "",
    ]
    REPORT_OUT.write_text("\n".join(report), encoding="utf-8")
    print(display.to_string(index=False))
    print(observer_display.to_string(index=False))
    print("INVERSE_REQUIRED_RAPIDITY_DIAGNOSTIC_V01_COMPLETE")


if __name__ == "__main__":
    main()
