#!/usr/bin/env python3
"""Run the NGC7331 exact B2 interval-control audit.

This is a post-freeze interval audit, not a point endpoint fit. It reads the
frozen NGC7331 exact B2 transfer interval manifest/grid unchanged, then scores
whether observed velocities fall inside or near the source-frozen interval.
No q_warp point is selected from residuals.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
FORMULA_ID = "NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1"
CLAIM_BOUNDARY = "ngc7331_b2_exact_transfer_interval_control_audit_not_point_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def rmse(values: pd.Series | np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    return float(np.sqrt(np.mean(np.square(arr))))


def interval_distance(obs: pd.Series, low: pd.Series, high: pd.Series) -> pd.Series:
    obs_arr = obs.astype(float)
    low_arr = low.astype(float)
    high_arr = high.astype(float)
    return np.where(obs_arr < low_arr, low_arr - obs_arr, np.where(obs_arr > high_arr, obs_arr - high_arr, 0.0))


def baseline_interval_rows(points: pd.DataFrame, interval_grid: pd.DataFrame) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for model_id, column in [
        ("NEWTONIAN_vn", "vn"),
        ("TPG_V6_v_v6", "v_v6"),
        ("MOND_v_mond", "v_mond"),
        ("EXPONENTIAL_DISK_CARRIER", "v_K_exponential_disk"),
    ]:
        pred = points[column].astype(float)
        residual = pred - points["vobs"].astype(float)
        inside = (
            (pred >= interval_grid["v_exact_b2_min_cross_caveated_km_s"])
            & (pred <= interval_grid["v_exact_b2_max_cross_caveated_km_s"])
        )
        rows.append(
            {
                "galaxy": GALAXY,
                "model_id": model_id,
                "model_role": "baseline_point_curve",
                "n_points": len(points),
                "rmse_km_s": rmse(residual),
                "mae_km_s": float(np.mean(np.abs(residual))),
                "fraction_inside_exact_b2_cross_caveated_interval": float(inside.mean()),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(DATA / "ngc7331_b2_exact_transfer_formula_freeze_manifest.csv").iloc[0]
    summary_in = pd.read_csv(DATA / "ngc7331_b2_exact_transfer_formula_freeze_summary.csv").iloc[0]
    grid = pd.read_csv(DATA / "ngc7331_b2_exact_transfer_formula_freeze_kernel_grid.csv")
    points = pd.read_csv(DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_points.csv")
    if str(manifest["formula_id"]) != FORMULA_ID:
        raise RuntimeError("Unexpected NGC7331 exact B2 freeze formula id")
    if not bool(summary_in["formula_frozen_before_endpoint_scoring"]):
        raise RuntimeError("Exact B2 interval formula is not frozen")
    if len(points) != len(grid):
        raise RuntimeError("Point/grid length mismatch")

    joined = points[["galaxy", "r", "vobs", "errv", "vn", "v_v6", "v_mond", "v_K_exponential_disk"]].copy()
    for column in [
        "x_R_over_RHI",
        "x_w_formula_freeze",
        "kernel_warp_history_min",
        "kernel_warp_history_max",
        "v_exact_b2_min_km_s",
        "v_exact_b2_max_km_s",
        "v_exact_b2_min_cross_caveated_km_s",
        "v_exact_b2_max_cross_caveated_km_s",
    ]:
        joined[column] = grid[column].to_numpy()

    exact_distance = interval_distance(
        joined["vobs"],
        joined["v_exact_b2_min_km_s"],
        joined["v_exact_b2_max_km_s"],
    )
    cross_distance = interval_distance(
        joined["vobs"],
        joined["v_exact_b2_min_cross_caveated_km_s"],
        joined["v_exact_b2_max_cross_caveated_km_s"],
    )
    exact_inside = exact_distance == 0.0
    cross_inside = cross_distance == 0.0
    midpoint = 0.5 * (
        joined["v_exact_b2_min_km_s"] + joined["v_exact_b2_max_km_s"]
    )
    cross_midpoint = 0.5 * (
        joined["v_exact_b2_min_cross_caveated_km_s"]
        + joined["v_exact_b2_max_cross_caveated_km_s"]
    )

    joined["exact_b2_interval_distance_km_s"] = exact_distance
    joined["exact_b2_cross_caveated_interval_distance_km_s"] = cross_distance
    joined["inside_exact_b2_interval"] = exact_inside
    joined["inside_exact_b2_cross_caveated_interval"] = cross_inside
    joined["v_exact_b2_interval_midpoint_km_s"] = midpoint
    joined["v_exact_b2_cross_caveated_midpoint_km_s"] = cross_midpoint
    joined["construction_used_vobs"] = False
    joined["scoring_used_vobs"] = True
    joined["endpoint_scores_allowed"] = True
    joined["point_q_selected_from_residual"] = False
    joined["claim_boundary"] = CLAIM_BOUNDARY

    scores = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "model_id": FORMULA_ID,
                "model_role": "source_frozen_interval_readout",
                "n_points": len(joined),
                "coverage_fraction": float(exact_inside.mean()),
                "coverage_fraction_cross_caveated": float(cross_inside.mean()),
                "interval_distance_rmse_km_s": rmse(exact_distance),
                "interval_distance_rmse_cross_caveated_km_s": rmse(cross_distance),
                "interval_midpoint_rmse_km_s": rmse(midpoint - joined["vobs"]),
                "interval_midpoint_rmse_cross_caveated_km_s": rmse(
                    cross_midpoint - joined["vobs"]
                ),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    baseline_scores = pd.DataFrame(baseline_interval_rows(joined, grid))

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": FORMULA_ID,
                "audit_status": "NGC7331_EXACT_B2_INTERVAL_CONTROL_AUDIT_COMPLETE_NOT_POINT_ENDPOINT",
                "n_points": len(joined),
                "coverage_fraction": float(exact_inside.mean()),
                "coverage_fraction_cross_caveated": float(cross_inside.mean()),
                "interval_distance_rmse_km_s": rmse(exact_distance),
                "interval_distance_rmse_cross_caveated_km_s": rmse(cross_distance),
                "best_baseline_rmse_km_s": float(baseline_scores["rmse_km_s"].min()),
                "best_baseline_model": str(
                    baseline_scores.sort_values("rmse_km_s")["model_id"].iloc[0]
                ),
                "best_baseline_inside_cross_caveated_interval_fraction": float(
                    baseline_scores.sort_values("rmse_km_s")[
                        "fraction_inside_exact_b2_cross_caveated_interval"
                    ].iloc[0]
                ),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_scores_allowed": True,
                "point_q_selected_from_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "claim_status": (
                    "interval-control audit only; not a point endpoint and not population validation"
                ),
            }
        ]
    )

    joined.to_csv(DATA / "ngc7331_b2_exact_transfer_interval_control_points.csv", index=False)
    scores.to_csv(DATA / "ngc7331_b2_exact_transfer_interval_control_scores.csv", index=False)
    baseline_scores.to_csv(
        DATA / "ngc7331_b2_exact_transfer_interval_control_baselines.csv", index=False
    )
    summary.to_csv(DATA / "ngc7331_b2_exact_transfer_interval_control_summary.csv", index=False)

    report = [
        "# NGC7331 B2 Exact Transfer Interval-Control Audit",
        "",
        "This audit scores the frozen interval readout as an interval, not as a",
        "single fitted point curve. It does not choose q_warp from residuals.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interval Scores",
        "",
        markdown_table(scores),
        "",
        "## Baseline Context",
        "",
        markdown_table(baseline_scores),
        "",
        "## Claim Boundary",
        "",
        "The audit reads observed velocities only after the formula freeze. Its",
        "primary metrics are interval coverage and distance-to-interval, not a",
        "post-hoc selected q_warp point. A future accepted endpoint may use this",
        "manifest only if it keeps the interval protocol unchanged or declares a",
        "new pre-frozen point-branch protocol before scoring.",
        "",
    ]
    (REPORTS / "ngc7331_b2_exact_transfer_interval_control_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
