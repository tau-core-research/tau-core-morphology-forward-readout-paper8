#!/usr/bin/env python3
"""Run the first narrow matched-family accepted population endpoint.

This endpoint is restricted to the 13-row externally audited exponential-disk
lane. The amplitude is frozen from the global train-only source-native bridge
formula preflight; it is not refit on the accepted endpoint pool.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import special


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
TPG_RESULTS = Path("/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1")

CLAIM_BOUNDARY = (
    "narrow_accepted_exponential_disk_population_endpoint_preliminary_control"
)


def freeman_bessel_shape(y: pd.Series | np.ndarray) -> np.ndarray:
    values = np.asarray(y, dtype=float)
    clipped = np.clip(values, 1.0e-5, 80.0)
    combo = (
        special.iv(0, clipped) * special.kv(0, clipped)
        - special.iv(1, clipped) * special.kv(1, clipped)
    )
    shape = clipped * clipped * combo
    return np.nan_to_num(shape, nan=0.0, posinf=0.0, neginf=0.0)


def rmse(values: pd.Series, target: pd.Series) -> float:
    return float(np.sqrt(np.mean(np.square(values - target))))


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, float]:
    manifest = pd.read_csv(DATA / "narrow_accepted_exponential_disk_manifest.csv")
    points = pd.read_csv(
        TPG_RESULTS / "tau_rotation_curve_frozen_proxy_runner_v0_points.csv"
    )
    points = points.merge(
        manifest[
            [
                "galaxy",
                "accepted_population_support_tier",
                "accepted_population_caveat",
                "scale_radius_kpc",
            ]
        ],
        on="galaxy",
        how="inner",
        validate="many_to_one",
    )
    amplitudes = pd.read_csv(DATA / "source_native_readout_formula_amplitudes.csv")
    beta = float(
        amplitudes.loc[
            amplitudes["formula_family"] == "K_exponential_disk",
            "beta_delta_v2_amplitude",
        ].iloc[0]
    )
    return manifest, points, beta


def score_points(points: pd.DataFrame, beta: float) -> pd.DataFrame:
    out = points.copy()
    scale = out["scale_radius_kpc"].clip(lower=1.0e-6)
    out["accepted_exp_disk_kernel"] = scale * freeman_bessel_shape(out["r"] / (2.0 * scale))
    pred_v2 = out["v_v6"].pow(2) + beta * out["accepted_exp_disk_kernel"]
    out["v_tau_narrow_accepted_exp_disk"] = np.sqrt(np.maximum(pred_v2, 0.0))
    out["beta_delta_v2_amplitude"] = beta
    out["accepted_endpoint_claim_boundary"] = CLAIM_BOUNDARY
    return out


def score_by_galaxy(scored: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for galaxy, sub in scored.groupby("galaxy"):
        tau = rmse(sub["v_tau_narrow_accepted_exp_disk"], sub["vobs"])
        tpg = rmse(sub["v_v6"], sub["vobs"])
        mond = rmse(sub["v_mond"], sub["vobs"])
        rows.append(
            {
                "galaxy": galaxy,
                "support_tier": sub["accepted_population_support_tier"].iloc[0],
                "accepted_population_caveat": sub["accepted_population_caveat"].iloc[0],
                "n_points": int(len(sub)),
                "scale_radius_kpc": float(sub["scale_radius_kpc"].iloc[0]),
                "rmse_tau": tau,
                "rmse_tpg_v6": tpg,
                "rmse_mond": mond,
                "tau_minus_tpg_v6": tau - tpg,
                "tau_minus_mond": tau - mond,
                "tau_beats_tpg_v6": tau < tpg,
                "tau_beats_mond": tau < mond,
                "accepted_endpoint_status": "NARROW_ACCEPTED_MATCHED_FAMILY_RESULT",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows).sort_values(["support_tier", "galaxy"])


def build_summary(scores: pd.DataFrame, beta: float) -> pd.DataFrame:
    rows = []
    for tier, sub in scores.groupby("support_tier"):
        rows.append(
            {
                "accepted_population_lane": "NARROW_ACCEPTED_EXPONENTIAL_DISK_13",
                "support_tier": tier,
                "n_galaxies": int(len(sub)),
                "mean_rmse_tau": float(sub["rmse_tau"].mean()),
                "mean_rmse_tpg_v6": float(sub["rmse_tpg_v6"].mean()),
                "mean_rmse_mond": float(sub["rmse_mond"].mean()),
                "median_tau_minus_tpg_v6": float(sub["tau_minus_tpg_v6"].median()),
                "median_tau_minus_mond": float(sub["tau_minus_mond"].median()),
                "tau_beats_tpg_v6_fraction": float(sub["tau_beats_tpg_v6"].mean()),
                "tau_beats_mond_fraction": float(sub["tau_beats_mond"].mean()),
                "beta_delta_v2_amplitude": beta,
                "amplitude_policy": "frozen_global_train_beta",
                "accepted_endpoint_status": "NARROW_ACCEPTED_MATCHED_FAMILY_RESULT",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "accepted_population_lane": "NARROW_ACCEPTED_EXPONENTIAL_DISK_13",
            "support_tier": "ALL_13",
            "n_galaxies": int(len(scores)),
            "mean_rmse_tau": float(scores["rmse_tau"].mean()),
            "mean_rmse_tpg_v6": float(scores["rmse_tpg_v6"].mean()),
            "mean_rmse_mond": float(scores["rmse_mond"].mean()),
            "median_tau_minus_tpg_v6": float(scores["tau_minus_tpg_v6"].median()),
            "median_tau_minus_mond": float(scores["tau_minus_mond"].median()),
            "tau_beats_tpg_v6_fraction": float(scores["tau_beats_tpg_v6"].mean()),
            "tau_beats_mond_fraction": float(scores["tau_beats_mond"].mean()),
            "beta_delta_v2_amplitude": beta,
            "amplitude_policy": "frozen_global_train_beta",
            "accepted_endpoint_status": "NARROW_ACCEPTED_MATCHED_FAMILY_RESULT",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(summary: pd.DataFrame, scores: pd.DataFrame) -> None:
    overall = summary.loc[summary["support_tier"] == "ALL_13"].iloc[0]
    lines = [
        "# Narrow Accepted Exponential-Disk Population Endpoint",
        "",
        "This is the first population-level matched-family accepted endpoint lane in",
        "Paper 8. It is intentionally narrow: only the 13 externally audited",
        "exponential-disk rows are scored, using accepted scale radii and the",
        "frozen train-only exponential-disk amplitude from the source-native bridge",
        "formula preflight.",
        "",
        "## Verdict",
        "",
        "This lane is endpoint-complete in the narrow accepted sense, but it is not the full 175-row matched-family launch.",
        f"On all 13 accepted rows, mean Tau RMSE = {overall['mean_rmse_tau']:.6f},",
        f"mean TPG/v6 RMSE = {overall['mean_rmse_tpg_v6']:.6f},",
        f"mean MOND RMSE = {overall['mean_rmse_mond']:.6f}.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Galaxy Scores",
        "",
        markdown_table(scores),
        "",
        "## Claim Boundary",
        "",
        "This is a narrow accepted population endpoint, not the full accepted",
        "manifest launch, not a matched-family population validation across all",
        "families, and not a general claim that Tau Core replaces MOND, RAR, TPG,",
        "or Newtonian baselines.",
    ]
    (REPORTS / "narrow_accepted_exponential_disk_population_endpoint.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    _, points, beta = load_inputs()
    scored_points = score_points(points, beta)
    scores = score_by_galaxy(scored_points)
    summary = build_summary(scores, beta)
    scored_points.to_csv(
        DATA / "narrow_accepted_exponential_disk_population_endpoint_points.csv",
        index=False,
    )
    scores.to_csv(
        DATA / "narrow_accepted_exponential_disk_population_endpoint_scores.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "narrow_accepted_exponential_disk_population_endpoint_summary.csv",
        index=False,
    )
    write_report(summary, scores)
    print("PAPER8_NARROW_ACCEPTED_EXPONENTIAL_DISK_POPULATION_ENDPOINT_COMPLETE")


if __name__ == "__main__":
    main()
