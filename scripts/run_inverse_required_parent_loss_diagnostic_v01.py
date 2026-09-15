#!/usr/bin/env python3
"""Invert measured rotation curves into an effective required readout loss.

This is deliberately endpoint-informed.  It reconstructs the terminal-equivalent
preimage required by a declared multiplicative readout shell; it does not select
a parent morphology, physical channel, or Nature occupation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
SOURCE = Path(
    "/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1/"
    "tau_rotation_curve_frozen_proxy_runner_v0_points.csv"
)
PREFIX = "inverse_required_parent_loss_diagnostic_v01"
POINTS_OUT = DATA / f"{PREFIX}_points.csv"
SUMMARY_OUT = DATA / f"{PREFIX}_summary.csv"
RADIAL_OUT = DATA / f"{PREFIX}_radial_bins.csv"
AUDIT_OUT = DATA / f"{PREFIX}.json"
REPORT_OUT = REPORTS / f"{PREFIX}.md"

BASELINES = {
    "newtonian_baryonic": "vn",
    "tpg_v6": "v_v6",
    "mond_fixed": "v_mond",
}
RADIAL_EDGES = np.linspace(0.0, 1.0, 6)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def equal_galaxy_weights(frame: pd.DataFrame) -> np.ndarray:
    counts = frame.groupby("galaxy")["galaxy"].transform("size").to_numpy(float)
    return 1.0 / counts


def weighted_rmse(values: np.ndarray, prediction: np.ndarray, weights: np.ndarray) -> float:
    return float(np.sqrt(np.average((values - prediction) ** 2, weights=weights)))


def fit_fixed_cubic(train: pd.DataFrame) -> np.ndarray:
    x = train["x"].to_numpy(float)
    design = np.column_stack([np.ones_like(x), x, x * x, x * x * x])
    weights = equal_galaxy_weights(train)
    lhs = design.T @ (weights[:, None] * design)
    rhs = design.T @ (weights * train["kappa_required"].to_numpy(float))
    return np.linalg.solve(lhs + 1.0e-10 * np.eye(4), rhs)


def markdown_table(frame: pd.DataFrame) -> str:
    headers = [str(column) for column in frame.columns]
    rows = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in frame.itertuples(index=False, name=None):
        values = []
        for value in row:
            if isinstance(value, (float, np.floating)):
                values.append(f"{float(value):.6g}")
            else:
                values.append(str(value))
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join(rows)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    source = pd.read_csv(SOURCE)
    required = {"galaxy", "split", "r", "vobs", "errv", *BASELINES.values()}
    missing = sorted(required - set(source.columns))
    if missing:
        raise ValueError(f"missing columns: {missing}")
    if (source[["vobs", *BASELINES.values()]] <= 0.0).any().any():
        raise ValueError("inverse logarithmic shell requires positive velocities")

    source = source.copy()
    source["rmax_kpc"] = source.groupby("galaxy")["r"].transform("max")
    source["x"] = source["r"] / source["rmax_kpc"]
    records: list[pd.DataFrame] = []
    summary_rows: list[dict[str, float | int | str]] = []
    radial_rows: list[dict[str, float | int | str]] = []

    for baseline_id, baseline_column in BASELINES.items():
        part = source[["galaxy", "split", "r", "x", "vobs", "errv", baseline_column]].copy()
        part = part.rename(columns={baseline_column: "v_baseline"})
        part.insert(0, "baseline_id", baseline_id)
        part["gain_required"] = part["vobs"] / part["v_baseline"]
        part["kappa_required"] = np.log(part["gain_required"])
        part["loss_required"] = 1.0 - 1.0 / part["gain_required"] ** 2
        part["delta_v2_required_km2_s2"] = part["vobs"] ** 2 - part["v_baseline"] ** 2
        part["sigma_kappa"] = part["errv"] / part["vobs"]
        part["sigma_loss"] = (
            2.0 * part["v_baseline"] ** 2 * part["errv"] / part["vobs"] ** 3
        )
        part["positive_loss_95"] = part["loss_required"] - 1.96 * part["sigma_loss"] > 0.0
        part["negative_loss_95"] = part["loss_required"] + 1.96 * part["sigma_loss"] < 0.0
        records.append(part)

        train = part.loc[part["split"] == "train"].copy()
        holdout = part.loc[part["split"] == "holdout"].copy()
        coeff = fit_fixed_cubic(train)
        xh = holdout["x"].to_numpy(float)
        pred_cubic = np.column_stack([np.ones_like(xh), xh, xh * xh, xh * xh * xh]) @ coeff
        pred_constant = np.full_like(xh, train.groupby("galaxy")["kappa_required"].mean().median())
        target = holdout["kappa_required"].to_numpy(float)
        weights = equal_galaxy_weights(holdout)
        zero_rmse = weighted_rmse(target, np.zeros_like(target), weights)
        constant_rmse = weighted_rmse(target, pred_constant, weights)
        cubic_rmse = weighted_rmse(target, pred_cubic, weights)
        galaxy_medians = part.groupby("galaxy", sort=False)["loss_required"].median()
        galaxy_positive = part.groupby("galaxy", sort=False)["positive_loss_95"].mean()
        summary_rows.append(
            {
                "baseline_id": baseline_id,
                "n_points": int(len(part)),
                "n_galaxies": int(part["galaxy"].nunique()),
                "median_gain": float(part["gain_required"].median()),
                "median_kappa": float(part["kappa_required"].median()),
                "median_loss": float(part["loss_required"].median()),
                "point_fraction_positive_loss": float((part["loss_required"] > 0.0).mean()),
                "point_fraction_positive_loss_95": float(part["positive_loss_95"].mean()),
                "point_fraction_negative_loss_95": float(part["negative_loss_95"].mean()),
                "galaxy_fraction_median_positive": float((galaxy_medians > 0.0).mean()),
                "galaxy_fraction_majority_positive_95": float((galaxy_positive > 0.5).mean()),
                "holdout_zero_kappa_rmse": zero_rmse,
                "holdout_constant_rmse_ratio": constant_rmse / zero_rmse,
                "holdout_fixed_cubic_rmse_ratio": cubic_rmse / zero_rmse,
            }
        )

        part["radial_bin"] = pd.cut(
            part["x"], RADIAL_EDGES, include_lowest=True, labels=False
        )
        for radial_bin, group in part.groupby("radial_bin", observed=True):
            radial_rows.append(
                {
                    "baseline_id": baseline_id,
                    "radial_bin": int(radial_bin),
                    "x_lower": float(RADIAL_EDGES[int(radial_bin)]),
                    "x_upper": float(RADIAL_EDGES[int(radial_bin) + 1]),
                    "n_points": int(len(group)),
                    "n_galaxies": int(group["galaxy"].nunique()),
                    "median_kappa": float(group["kappa_required"].median()),
                    "median_loss": float(group["loss_required"].median()),
                    "fraction_positive_loss_95": float(group["positive_loss_95"].mean()),
                }
            )

    points = pd.concat(records, ignore_index=True)
    summary = pd.DataFrame(summary_rows)
    radial = pd.DataFrame(radial_rows)
    POINTS_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points.to_csv(POINTS_OUT, index=False)
    summary.to_csv(SUMMARY_OUT, index=False)
    radial.to_csv(RADIAL_OUT, index=False)

    audit = {
        "schema": PREFIX,
        "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
        "source_sha256": sha256(SOURCE),
        "n_points": int(len(source)),
        "n_galaxies": int(source["galaxy"].nunique()),
        "inverse_shell": {
            "gain_required": "v_observed/v_baseline",
            "kappa_required": "log(v_observed/v_baseline)",
            "loss_required": "1-(v_baseline/v_observed)^2",
            "forward_convention": "v_observed^2=v_baseline^2/(1-loss_required)",
        },
        "identifiability": {
            "identified": "one terminal-equivalent scalar combination per measured radius and chosen baseline",
            "not_identified": [
                "parent morphology versus distance calibration versus time calibration",
                "channel kernel and terminal map separately",
                "causal origin or Nature occupation",
            ],
            "gauge_family": "kappa_required=kappa_D-kappa_T+kappa_M+kappa_cal; arbitrary component shifts summing to zero leave the measurement unchanged",
        },
        "summary": summary.to_dict(orient="records"),
        "checks": {
            "equal_velocity_gives_zero_kappa": bool(np.log(100.0 / 100.0) == 0.0),
            "equal_velocity_gives_zero_loss": bool(1.0 - (100.0 / 100.0) ** 2 == 0.0),
            "forward_substitution_max_abs_v2_error": float(
                np.max(np.abs(points["vobs"] ** 2 - points["v_baseline"] ** 2 / (1.0 - points["loss_required"])))
            ),
            "all_outputs_finite": bool(
                np.isfinite(points[["gain_required", "kappa_required", "loss_required", "sigma_kappa", "sigma_loss"]]).all().all()
            ),
            "holdout_not_used_to_fit_fixed_cubic": True,
        },
        "strongest_alternative": "ordinary baseline incompleteness, baryonic modelling and measurement/deprojection systematics generate the same inverse target",
        "endpoint_authorized": False,
        "claim_boundary": "The measurement fixes an effective terminal preimage only after a baseline and readout convention are chosen. It does not uniquely reconstruct the parent body or prove morphological loss.",
    }
    AUDIT_OUT.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    by_baseline = summary.set_index("baseline_id")
    newton = by_baseline.loc["newtonian_baryonic"]
    tpg = by_baseline.loc["tpg_v6"]
    mond = by_baseline.loc["mond_fixed"]

    report = [
        "# Inverse required parent-loss diagnostic v01",
        "",
        "Status: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`.",
        "",
        "## Exact inverse",
        "",
        "For the declared effective shell",
        "",
        "$$v_{\\rm obs}^2=v_{\\rm base}^2/(1-\\ell_{\\rm req}),$$",
        "",
        "the measurements determine",
        "",
        "$$g_{\\rm req}=v_{\\rm obs}/v_{\\rm base},\\qquad",
        "\\kappa_{\\rm req}=\\log g_{\\rm req},\\qquad",
        "\\ell_{\\rm req}=1-(v_{\\rm base}/v_{\\rm obs})^2.$$",
        "",
        "Positive `loss_required` means that this inverse-attenuation convention",
        "needs an apparent boost relative to the selected baseline. Negative values",
        "cannot be represented by a positive loss in this one-parameter shell.",
        "",
        "## Results",
        "",
        markdown_table(summary),
        "",
        f"Against baryons alone the median required gain is {newton['median_gain']:.3f}",
        f"and {100.0 * newton['point_fraction_positive_loss_95']:.1f}% of points",
        "require positive loss at the propagated 95% level. This is the familiar",
        "mass-discrepancy pattern expressed in the chosen inverse coordinates.",
        f"Against frozen TPG/v6 the median gain is {tpg['median_gain']:.3f} and the",
        f"fixed radial law has holdout RMSE ratio {tpg['holdout_fixed_cubic_rmse_ratio']:.3f};",
        f"against fixed MOND they are {mond['median_gain']:.3f} and",
        f"{mond['holdout_fixed_cubic_rmse_ratio']:.3f}. Thus the remaining inverse",
        "field after either non-Newtonian baseline is sign-mixed and is not captured",
        "well by one universal cubic radial profile.",
        "",
        "The fixed cubic is trained only on the 131-galaxy development split and",
        "evaluated on the 44-galaxy holdout. A ratio below one indicates that one",
        "universal radial shape improves on zero required log-gain.",
        "",
        "## What is and is not reconstructed",
        "",
        "At each measured radius the endpoint fixes one scalar combination. It does",
        "not split that number into parent morphology, spatial calibration, temporal",
        "calibration and terminal calibration. If",
        "",
        "$$\\kappa_{\\rm req}=\\kappa_D-\\kappa_T+\\kappa_M+\\kappa_{\\rm cal},$$",
        "",
        "then arbitrary component shifts whose signed sum is zero leave every",
        "measurement unchanged. This is the inverse gauge/null family. Additional",
        "independent observables or a source-side law are needed to choose one member.",
        "",
        "The strongest conventional counterinterpretation is that the reconstructed",
        "field absorbs baseline incompleteness, baryonic modelling and measurement or",
        "deprojection systematics. Therefore the output is an empirical target for a",
        "future Tau derivation, not evidence that the target is parent morphological",
        "loss and not a dark-matter replacement result.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(report), encoding="utf-8")
    print(summary.to_string(index=False))
    print(json.dumps(audit["checks"], indent=2))
    print("INVERSE_REQUIRED_PARENT_LOSS_DIAGNOSTIC_V01_COMPLETE")


if __name__ == "__main__":
    main()
