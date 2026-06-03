#!/usr/bin/env python3
"""Audit exponential-disk dry-run failures and scale sensitivity."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import special


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
TPG_RESULTS = Path("/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1")
SCALE_MULTIPLIERS = [0.75, 1.0, 1.25]


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


def fit_beta(points: pd.DataFrame, kernel_col: str) -> float:
    target = points["vobs"].pow(2) - points["v_v6"].pow(2)
    kernel = points[kernel_col]
    den = float(kernel.pow(2).sum())
    return float((target * kernel).sum() / den) if den else 0.0


def load_points() -> pd.DataFrame:
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
    for multiplier in SCALE_MULTIPLIERS:
        scale = (points["scale_radius_kpc"] * multiplier).clip(lower=1.0e-6)
        points[f"kernel_scale_{multiplier:g}"] = scale * freeman_bessel_shape(
            points["r"] / (2.0 * scale)
        )
    return points


def score_multiplier(points: pd.DataFrame, multiplier: float) -> pd.DataFrame:
    kernel_col = f"kernel_scale_{multiplier:g}"
    rows = []
    for galaxy, sub in points.groupby("galaxy"):
        train = points[points["galaxy"] != galaxy]
        beta = fit_beta(train, kernel_col)
        pred_v2 = sub["v_v6"].pow(2) + beta * sub[kernel_col]
        pred = np.sqrt(np.maximum(pred_v2, 0.0))
        rmse_tau = rmse(pred, sub["vobs"])
        rmse_tpg = rmse(sub["v_v6"], sub["vobs"])
        rmse_mond = rmse(sub["v_mond"], sub["vobs"])
        rows.append(
            {
                "galaxy": galaxy,
                "scale_multiplier": multiplier,
                "narrow_dry_run_lane": sub["narrow_dry_run_lane"].iloc[0],
                "external_family_label_status": sub[
                    "external_family_label_status"
                ].iloc[0],
                "external_family_label_caveat": sub[
                    "external_family_label_caveat"
                ].iloc[0],
                "beta_leave_one_galaxy_out": beta,
                "rmse_tau": rmse_tau,
                "rmse_tpg_v6": rmse_tpg,
                "rmse_mond": rmse_mond,
                "tau_minus_tpg_v6": rmse_tau - rmse_tpg,
                "tau_minus_mond": rmse_tau - rmse_mond,
                "beats_tpg_v6": rmse_tau < rmse_tpg,
                "beats_mond": rmse_tau < rmse_mond,
                "claim_boundary": (
                    "scale_sensitivity_diagnostic_not_endpoint_not_validation"
                ),
            }
        )
    return pd.DataFrame(rows)


def classify_failure(row: pd.Series) -> str:
    if row["beats_tpg_v6"] and row["beats_mond"]:
        return "beats_both"
    if row["beats_tpg_v6"] and not row["beats_mond"]:
        return "beats_tpg_only"
    if row["beats_mond"] and not row["beats_tpg_v6"]:
        return "beats_mond_only"
    return "beats_neither"


def build_audits() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    points = load_points()
    scores = pd.concat(
        [score_multiplier(points, multiplier) for multiplier in SCALE_MULTIPLIERS],
        ignore_index=True,
    )
    scores["failure_class"] = scores.apply(classify_failure, axis=1)
    summary = (
        scores.groupby(["narrow_dry_run_lane", "scale_multiplier"], as_index=False)
        .agg(
            n_galaxies=("galaxy", "size"),
            mean_rmse_tau=("rmse_tau", "mean"),
            mean_rmse_tpg_v6=("rmse_tpg_v6", "mean"),
            mean_rmse_mond=("rmse_mond", "mean"),
            median_tau_minus_tpg_v6=("tau_minus_tpg_v6", "median"),
            median_tau_minus_mond=("tau_minus_mond", "median"),
            beats_tpg_v6_fraction=("beats_tpg_v6", "mean"),
            beats_mond_fraction=("beats_mond", "mean"),
        )
        .sort_values(["narrow_dry_run_lane", "scale_multiplier"])
    )
    best = (
        scores.sort_values(["galaxy", "rmse_tau"])
        .groupby("galaxy", as_index=False)
        .first()
        .sort_values(["narrow_dry_run_lane", "galaxy"])
    )
    return scores, summary, best


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(scores: pd.DataFrame, summary: pd.DataFrame, best: pd.DataFrame) -> None:
    strict_summary = summary[
        summary["narrow_dry_run_lane"] == "STRICT_NARROW_DRY_RUN_READY_CANDIDATE"
    ]
    failure_counts = (
        scores[scores["scale_multiplier"] == 1.0]
        .groupby(["narrow_dry_run_lane", "failure_class"], as_index=False)
        .size()
        .rename(columns={"size": "n_galaxies"})
    )
    lines = [
        "# Exponential-Disk Failure and Scale-Sensitivity Audit",
        "",
        "This audit varies only the accepted S4G/SPARC scale radius multiplier",
        "inside the exponential-disk Freeman/Bessel shell and uses a",
        "leave-one-galaxy-out amplitude policy. It does not launch the frozen",
        "endpoint.",
        "",
        "## Verdict",
        "",
        "The strict lane remains mixed under 0.75, 1.0, and 1.25 scale multipliers.",
        "This points to a readout-normalization or morphology-subtype issue rather",
        "than a simple single-scale correction.",
        "",
        "## Strict-Lane Scale Sensitivity",
        "",
        markdown_table(strict_summary),
        "",
        "## Failure Classes at Scale Multiplier 1.0",
        "",
        markdown_table(failure_counts),
        "",
        "## Best Multiplier Per Galaxy",
        "",
        markdown_table(
            best[
                [
                    "galaxy",
                    "narrow_dry_run_lane",
                    "scale_multiplier",
                    "failure_class",
                    "tau_minus_tpg_v6",
                    "tau_minus_mond",
                    "external_family_label_caveat",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This is a failure/sensitivity diagnostic, not an endpoint score and not a",
        "validation of Tau Core. The scale multipliers are diagnostic probes, not",
        "post-hoc selected formula parameters.",
    ]
    (REPORTS / "exponential_disk_failure_sensitivity_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    scores, summary, best = build_audits()
    scores.to_csv(DATA / "exponential_disk_failure_sensitivity_scores.csv", index=False)
    summary.to_csv(DATA / "exponential_disk_failure_sensitivity_summary.csv", index=False)
    best.to_csv(DATA / "exponential_disk_failure_sensitivity_best_by_galaxy.csv", index=False)
    write_report(scores, summary, best)
    print("PAPER8_EXPONENTIAL_DISK_FAILURE_SENSITIVITY_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
