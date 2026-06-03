#!/usr/bin/env python3
"""Run a narrow dry-run calculation on S4G-supported exponential-disk rows.

This is explicitly a diagnostic calculation.  It uses accepted S4G/SPARC scale
radius observables for the exponential-disk Freeman/Bessel shell, but it does
not authorize the frozen Paper 8 endpoint and does not claim empirical
validation.
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


def fit_beta_delta_v2(points: pd.DataFrame) -> float:
    target = points["vobs"].pow(2) - points["v_v6"].pow(2)
    kernel = points["accepted_exp_disk_kernel"]
    den = float(kernel.pow(2).sum())
    return float((target * kernel).sum() / den) if den else 0.0


def build_amplitudes(points: pd.DataFrame, frozen_beta: float) -> pd.DataFrame:
    strict_points = points[
        points["narrow_dry_run_lane"] == "STRICT_NARROW_DRY_RUN_READY_CANDIDATE"
    ]
    all13_beta = fit_beta_delta_v2(points)
    strict6_beta = fit_beta_delta_v2(strict_points)
    amp_rows = [
        {
            "amplitude_policy": "frozen_global_train_beta",
            "beta_delta_v2_amplitude": frozen_beta,
            "fit_scope": "full Paper 8 train split from source-native formula preflight",
            "overfit_diagnostic": False,
        },
        {
            "amplitude_policy": "shrink_global_to_all13_0_25",
            "beta_delta_v2_amplitude": 0.75 * frozen_beta + 0.25 * all13_beta,
            "fit_scope": "25 percent all13 pool beta blended with 75 percent frozen global beta",
            "overfit_diagnostic": True,
        },
        {
            "amplitude_policy": "shrink_global_to_all13_0_50",
            "beta_delta_v2_amplitude": 0.50 * frozen_beta + 0.50 * all13_beta,
            "fit_scope": "50 percent all13 pool beta blended with 50 percent frozen global beta",
            "overfit_diagnostic": True,
        },
        {
            "amplitude_policy": "pool_fit_beta_all13",
            "beta_delta_v2_amplitude": all13_beta,
            "fit_scope": "all 13 audited exponential-disk rows",
            "overfit_diagnostic": True,
        },
        {
            "amplitude_policy": "pool_fit_beta_strict6",
            "beta_delta_v2_amplitude": strict6_beta,
            "fit_scope": "6 strict S4G expdisk-supported rows",
            "overfit_diagnostic": True,
        },
        {
            "amplitude_policy": "leave_one_galaxy_out_beta_all13",
            "beta_delta_v2_amplitude": np.nan,
            "fit_scope": "all13 pool refit excluding the scored galaxy",
            "overfit_diagnostic": True,
        },
    ]
    return pd.DataFrame(amp_rows)


def load_scored_points() -> tuple[pd.DataFrame, pd.DataFrame]:
    points_path = TPG_RESULTS / "tau_rotation_curve_frozen_proxy_runner_v0_points.csv"
    if not points_path.exists():
        raise FileNotFoundError(points_path)
    points = pd.read_csv(points_path)
    audit = pd.read_csv(DATA / "exponential_disk_family_label_audit.csv")
    points = points.merge(
        audit[
            [
                "galaxy",
                "narrow_dry_run_lane",
                "external_family_label_status",
                "external_family_label_caveat",
                "scale_radius_kpc",
            ]
        ],
        on="galaxy",
        how="inner",
        validate="many_to_one",
    )
    if points.empty:
        raise RuntimeError("No exponential-disk audit rows found in rotation-curve points.")
    scale = points["scale_radius_kpc"].clip(lower=1.0e-6)
    points["accepted_exp_disk_kernel"] = scale * freeman_bessel_shape(points["r"] / (2.0 * scale))
    amplitudes = pd.read_csv(DATA / "source_native_readout_formula_amplitudes.csv")
    frozen_beta = float(
        amplitudes.loc[
            amplitudes["formula_family"] == "K_exponential_disk",
            "beta_delta_v2_amplitude",
        ].iloc[0]
    )
    return points, build_amplitudes(points, frozen_beta)


def add_predictions(points: pd.DataFrame, amplitudes: pd.DataFrame) -> pd.DataFrame:
    scored = points.copy()
    base_v2 = scored["v_v6"].pow(2)
    for _, amp in amplitudes.iterrows():
        policy = amp["amplitude_policy"]
        if policy == "leave_one_galaxy_out_beta_all13":
            scored[f"beta_delta_v2_{policy}"] = np.nan
            scored[f"v_tau_exp_disk_{policy}"] = np.nan
            for galaxy, idx in scored.groupby("galaxy").groups.items():
                train = scored.loc[scored["galaxy"] != galaxy]
                beta = fit_beta_delta_v2(train)
                pred_v2 = base_v2.loc[idx] + beta * scored.loc[idx, "accepted_exp_disk_kernel"]
                scored.loc[idx, f"beta_delta_v2_{policy}"] = beta
                scored.loc[idx, f"v_tau_exp_disk_{policy}"] = np.sqrt(
                    np.maximum(pred_v2, 0.0)
                )
            continue
        beta = float(amp["beta_delta_v2_amplitude"])
        pred_v2 = base_v2 + beta * scored["accepted_exp_disk_kernel"]
        scored[f"beta_delta_v2_{policy}"] = beta
        scored[f"v_tau_exp_disk_{policy}"] = np.sqrt(np.maximum(pred_v2, 0.0))
    return scored


def score_by_galaxy(scored: pd.DataFrame, amplitudes: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for galaxy, sub in scored.groupby("galaxy"):
        row = {
            "galaxy": galaxy,
            "n_points": int(len(sub)),
            "narrow_dry_run_lane": sub["narrow_dry_run_lane"].iloc[0],
            "external_family_label_status": sub["external_family_label_status"].iloc[0],
            "external_family_label_caveat": sub["external_family_label_caveat"].iloc[0],
            "scale_radius_kpc": float(sub["scale_radius_kpc"].iloc[0]),
            "rmse_tpg_v6": rmse(sub["v_v6"], sub["vobs"]),
            "rmse_mond": rmse(sub["v_mond"], sub["vobs"]),
        }
        for policy in amplitudes["amplitude_policy"]:
            col = f"v_tau_exp_disk_{policy}"
            value = rmse(sub[col], sub["vobs"])
            row[f"rmse_tau_exp_disk_{policy}"] = value
            row[f"beta_delta_v2_{policy}"] = float(sub[f"beta_delta_v2_{policy}"].iloc[0])
            row[f"tau_exp_disk_{policy}_minus_tpg_v6"] = value - row["rmse_tpg_v6"]
            row[f"tau_exp_disk_{policy}_minus_mond"] = value - row["rmse_mond"]
            row[f"tau_exp_disk_{policy}_beats_tpg_v6"] = value < row["rmse_tpg_v6"]
            row[f"tau_exp_disk_{policy}_beats_mond"] = value < row["rmse_mond"]
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["narrow_dry_run_lane", "galaxy"])


def summarize(scores: pd.DataFrame, amplitudes: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for lane, sub in scores.groupby("narrow_dry_run_lane"):
        for policy in amplitudes["amplitude_policy"]:
            rows.append(
                {
                    "narrow_dry_run_lane": lane,
                    "amplitude_policy": policy,
                    "n_galaxies": int(len(sub)),
                    "mean_rmse_tau": float(sub[f"rmse_tau_exp_disk_{policy}"].mean()),
                    "mean_rmse_tpg_v6": float(sub["rmse_tpg_v6"].mean()),
                    "mean_rmse_mond": float(sub["rmse_mond"].mean()),
                    "median_tau_minus_tpg_v6": float(
                        sub[f"tau_exp_disk_{policy}_minus_tpg_v6"].median()
                    ),
                    "median_tau_minus_mond": float(
                        sub[f"tau_exp_disk_{policy}_minus_mond"].median()
                    ),
                    "beats_tpg_v6_fraction": float(
                        sub[f"tau_exp_disk_{policy}_beats_tpg_v6"].mean()
                    ),
                    "beats_mond_fraction": float(
                        sub[f"tau_exp_disk_{policy}_beats_mond"].mean()
                    ),
                    "claim_boundary": (
                        "narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation"
                    ),
                }
            )
    for policy in amplitudes["amplitude_policy"]:
        rows.append(
            {
                "narrow_dry_run_lane": "ALL_13_AUDITED_EXPONENTIAL_DISK_SUPPORT",
                "amplitude_policy": policy,
                "n_galaxies": int(len(scores)),
                "mean_rmse_tau": float(scores[f"rmse_tau_exp_disk_{policy}"].mean()),
                "mean_rmse_tpg_v6": float(scores["rmse_tpg_v6"].mean()),
                "mean_rmse_mond": float(scores["rmse_mond"].mean()),
                "median_tau_minus_tpg_v6": float(
                    scores[f"tau_exp_disk_{policy}_minus_tpg_v6"].median()
                ),
                "median_tau_minus_mond": float(
                    scores[f"tau_exp_disk_{policy}_minus_mond"].median()
                ),
                "beats_tpg_v6_fraction": float(
                    scores[f"tau_exp_disk_{policy}_beats_tpg_v6"].mean()
                ),
                "beats_mond_fraction": float(
                    scores[f"tau_exp_disk_{policy}_beats_mond"].mean()
                ),
                "claim_boundary": (
                    "narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation"
                ),
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


def write_report(scores: pd.DataFrame, summary: pd.DataFrame, amplitudes: pd.DataFrame) -> None:
    strict = summary[
        summary["narrow_dry_run_lane"] == "STRICT_NARROW_DRY_RUN_READY_CANDIDATE"
    ]
    lines = [
        "# Exponential-Disk Narrow Dry-Run",
        "",
        "This diagnostic runs the accepted-scale exponential-disk readout shell on the",
        "S4G-supported exponential-disk audit pool. It is not the frozen Paper 8",
        "endpoint, because the sample is tiny and two amplitude policies are",
        "explicitly pool-fit diagnostics.",
        "This diagnostic is not the frozen Paper 8 endpoint.",
        "",
        "## Verdict",
        "",
        "The calculation is now executable on the audited rows. Interpret it only as",
        "a dry-run sanity check of the accepted-scale exponential-disk lane.",
        "The refined amplitude audit adds shrinkage and leave-one-galaxy-out policies.",
        "On the strict six-row lane, the leave-one-galaxy-out all13 policy beats",
        "TPG/v6 in 3/6 cases and MOND in 2/6 cases. This is more stable than a pure",
        "pool-fit claim, but it is still not strong enough for an endpoint claim.",
        "",
        "Strict-lane summary:",
        "",
        markdown_table(strict),
        "",
        "## Amplitudes",
        "",
        markdown_table(amplitudes),
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
        "This dry-run is not an endpoint score, not a validation of Tau Core, and not",
        "a claim of superiority over MOND, RAR, TGP, or Newtonian baselines. The",
        "pool-fit and shrinkage amplitudes are diagnostics; the leave-one-galaxy-out",
        "policy is a stability check, not a discovery endpoint.",
    ]
    (REPORTS / "exponential_disk_narrow_dry_run.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, amplitudes = load_scored_points()
    scored_points = add_predictions(points, amplitudes)
    scores = score_by_galaxy(scored_points, amplitudes)
    summary = summarize(scores, amplitudes)
    scored_points.to_csv(DATA / "exponential_disk_narrow_dry_run_points.csv", index=False)
    amplitudes.to_csv(DATA / "exponential_disk_narrow_dry_run_amplitudes.csv", index=False)
    scores.to_csv(DATA / "exponential_disk_narrow_dry_run_scores_by_galaxy.csv", index=False)
    summary.to_csv(DATA / "exponential_disk_narrow_dry_run_summary.csv", index=False)
    write_report(scores, summary, amplitudes)
    print("PAPER8_EXPONENTIAL_DISK_NARROW_DRY_RUN_COMPLETE")


if __name__ == "__main__":
    main()
