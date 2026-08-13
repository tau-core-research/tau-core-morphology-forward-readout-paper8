#!/usr/bin/env python3
"""Ablate the ingredients that make the frozen TPG/v6 baseline effective."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

import run_source_native_readout_formula_endpoint as source


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/tpg_v6_motivation_ablation.md"
A0 = 1.2e-10
KPC_M = 3.085677581491367e19


def loading(points: pd.DataFrame) -> np.ndarray:
    acceleration = (points.vn.to_numpy() * 1000.0) ** 2 / (points.r.to_numpy() * KPC_M)
    return A0 / acceleration


def response(x: np.ndarray, family: str, gamma: float = 1.0, beta: float = 1.0) -> np.ndarray:
    t = np.power(x, beta)
    if family == "log":
        return np.log1p(t)
    if family == "linear":
        return t
    if family == "bounded":
        return t / (1.0 + t)
    if family == "generalized_dtl":
        if abs(gamma - 1.0) < 1.0e-12:
            return np.log1p(t)
        return (np.power(1.0 + t, 1.0 - gamma) - 1.0) / (1.0 - gamma)
    raise ValueError(family)


def fit_alpha(points: pd.DataFrame, shape: np.ndarray) -> float:
    train = points.split.eq("train").to_numpy()
    vn, vobs = points.vn.to_numpy(), points.vobs.to_numpy()

    def objective(alpha: float) -> float:
        pred = vn[train] * (1.0 + alpha * shape[train])
        return float(np.mean((pred - vobs[train]) ** 2))

    return float(minimize_scalar(objective, bounds=(0.0, 2.0), method="bounded").x)


def galaxy_summary(points: pd.DataFrame, prediction: np.ndarray, lane: str) -> dict:
    frame = points.copy()
    frame["prediction"] = prediction
    frame = frame[frame.split.eq(lane)]
    values = []
    for _, sub in frame.groupby("galaxy"):
        values.append(float(np.sqrt(np.mean((sub.prediction - sub.vobs) ** 2))))
    return {
        "n_galaxies": int(frame.galaxy.nunique()), "n_points": len(frame),
        "mean_galaxy_rmse_km_s": float(np.mean(values)),
        "median_galaxy_rmse_km_s": float(np.median(values)),
    }


def main() -> None:
    points, _ = source.load_points()
    x = loading(points)
    candidates = []
    fixed = [
        ("newton", np.zeros(len(points)), 0.0, "no low-acceleration response"),
        ("linear_fixed", response(x, "linear"), 0.360, "additive loading control"),
        ("bounded_fixed", response(x, "bounded"), 0.360, "saturating control"),
        ("log_fixed_0360", response(x, "log"), 0.360, "frozen TPG/v6"),
        ("log_cosmology_0366", response(x, "log"), 0.366, "2 a0/(c H0 Planck) candidate"),
    ]
    for name, shape, alpha, origin in fixed:
        candidates.append((name, shape, alpha, origin, False))
    for family in ["linear", "bounded", "log"]:
        shape = response(x, family)
        candidates.append((f"{family}_train_alpha", shape, fit_alpha(points, shape),
                           "alpha selected on historical train", True))

    grid = []
    for gamma in [0.75, 1.0, 1.25, 1.5]:
        for beta in [0.75, 1.0, 1.25]:
            shape = response(x, "generalized_dtl", gamma=gamma, beta=beta)
            alpha = fit_alpha(points, shape)
            prediction = points.vn.to_numpy() * (1.0 + alpha * shape)
            train_metric = galaxy_summary(points, prediction, "train")["mean_galaxy_rmse_km_s"]
            grid.append({"gamma": gamma, "beta": beta, "alpha": alpha,
                         "train_mean_galaxy_rmse_km_s": train_metric, "shape": shape})
    selected = min(grid, key=lambda row: row["train_mean_galaxy_rmse_km_s"])
    candidates.append((
        f"generalized_dtl_train_selected_g{selected['gamma']}_b{selected['beta']}",
        selected["shape"], selected["alpha"], "gamma beta and alpha selected on historical train", True,
    ))

    rows = []
    for name, shape, alpha, origin, train_selected in candidates:
        prediction = points.vn.to_numpy() * (1.0 + alpha * shape)
        train = galaxy_summary(points, prediction, "train")
        holdout = galaxy_summary(points, prediction, "holdout")
        rows.append({
            "candidate": name, "alpha": alpha, "origin": origin,
            "train_selected": train_selected,
            "train_mean_galaxy_rmse_km_s": train["mean_galaxy_rmse_km_s"],
            "holdout_mean_galaxy_rmse_km_s": holdout["mean_galaxy_rmse_km_s"],
            "holdout_median_galaxy_rmse_km_s": holdout["median_galaxy_rmse_km_s"],
        })
    table = pd.DataFrame(rows).sort_values("holdout_mean_galaxy_rmse_km_s")
    table.to_csv(DATA / "tpg_v6_motivation_ablation.csv", index=False)
    grid_out = pd.DataFrame([{k: v for k, v in row.items() if k != "shape"} for row in grid])
    grid_out.to_csv(DATA / "tpg_v6_generalized_dtl_train_grid.csv", index=False)

    by_name = table.set_index("candidate")
    canonical = by_name.loc["log_fixed_0360"]
    cosmology = by_name.loc["log_cosmology_0366"]
    log_fit = by_name.loc["log_train_alpha"]
    result = {
        "schema": "tpg_v6_motivation_ablation",
        "status": "TPG_V6_STRUCTURAL_MOTIVATION_ABLATION_COMPLETE",
        "canonical_formula": "v=vN[1+alpha log(1+a0/aN)]",
        "conditional_log_derivation": (
            "independent finite-capacity loadings compose multiplicatively while response adds; "
            "I(0)=0 and I'(0)=1 force I(x)=log(1+x)"
        ),
        "canonical_holdout_mean_galaxy_rmse_km_s": float(canonical.holdout_mean_galaxy_rmse_km_s),
        "cosmology_alpha_holdout_delta_km_s": float(
            cosmology.holdout_mean_galaxy_rmse_km_s - canonical.holdout_mean_galaxy_rmse_km_s
        ),
        "train_refit_alpha": float(log_fit.alpha),
        "train_refit_alpha_holdout_delta_km_s": float(
            log_fit.holdout_mean_galaxy_rmse_km_s - canonical.holdout_mean_galaxy_rmse_km_s
        ),
        "generalized_dtl_train_selected": {
            "gamma": selected["gamma"], "beta": selected["beta"], "alpha": selected["alpha"],
        },
        "a0_status": "empirical MOND scale; Tau-side compact-scale origin remains conditional",
        "alpha_status": "SPARC-calibrated operational constant; first-principles normalization open",
        "claim_boundary": "ablation of predictive ingredients, not a parent derivation or new validation",
    }
    (DATA / "tpg_v6_motivation_ablation.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# TPG/v6 motivation ablation\n\n"
        f"Status: `{result['status']}`\n\n"
        "The logarithm is conditionally forced by multiplicative finite-capacity loading and "
        "additive response. The acceleration ratio `a0/aN(R)` supplies a local, dimensionless "
        "activation coordinate and automatically turns the response off in the Newtonian limit.\n\n"
        f"Frozen TPG/v6 holdout mean galaxy RMSE is `{canonical.holdout_mean_galaxy_rmse_km_s:.3f} "
        f"km/s`. Replacing `alpha=0.360` by the cosmological candidate `0.366` changes this by "
        f"`{result['cosmology_alpha_holdout_delta_km_s']:+.3f} km/s`. Refitting alpha on train gives "
        f"`{result['train_refit_alpha']:.4f}` and changes holdout by "
        f"`{result['train_refit_alpha_holdout_delta_km_s']:+.3f} km/s`.\n\n"
        f"The generalized DTL train grid selects `gamma={selected['gamma']}`, "
        f"`beta={selected['beta']}`, `alpha={selected['alpha']:.4f}`. See the CSV artifacts for "
        "linear, bounded, logarithmic, and generalized controls.\n\n"
        "The test diagnoses where the empirical strength resides. It does not derive `a0`, the "
        "metric normalization, or the ordered-disk branch from the Tau parent.\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
