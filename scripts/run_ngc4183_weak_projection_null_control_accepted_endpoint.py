#!/usr/bin/env python3
"""Run the accepted NGC4183 weak-projection/null-control interval endpoint.

This is an interval-control endpoint, not a point-fit endpoint. It reads the
frozen NGC4183 null-control formula unchanged, constructs a source-frozen
interval around the exponential-disk carrier, and reads observed velocities
only in the scoring block.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_weak_projection_null_control_accepted_endpoint_preliminary_control"
GALAXY = "NGC4183"
FORMULA_ID = "N4183_WEAK_PROJECTION_NULL_CONTROL_BOUND"

sys.path.insert(0, str(ROOT / "scripts"))
import run_mixed_readout_population_endpoint as endpoint  # noqa: E402


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


def baseline_interval_rows(points: pd.DataFrame) -> list[dict[str, object]]:
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
            (pred >= points["v_null_control_interval_min_km_s"])
            & (pred <= points["v_null_control_interval_max_km_s"])
        )
        rows.append(
            {
                "galaxy": GALAXY,
                "model_id": model_id,
                "model_role": "baseline_point_curve",
                "n_points": len(points),
                "rmse_km_s": rmse(residual),
                "mae_km_s": float(np.mean(np.abs(residual))),
                "fraction_inside_null_control_interval": float(inside.mean()),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    accepted = pd.read_csv(DATA / "ngc4183_accepted_null_control_summary.csv").iloc[0]
    manifest = pd.read_csv(DATA / "ngc4183_null_control_formula_freeze_manifest.csv").iloc[0]
    grid = pd.read_csv(DATA / "ngc4183_null_control_formula_freeze_grid.csv")

    if not bool(accepted["accepted_control_allowed"]):
        raise RuntimeError("NGC4183 accepted null-control gate is not score-eligible")
    if str(manifest["formula_id"]) != FORMULA_ID:
        raise RuntimeError("Unexpected NGC4183 null-control formula id")
    if not bool(manifest["formula_freeze_allowed"]):
        raise RuntimeError("NGC4183 null-control formula is not frozen")

    points = endpoint.build_generic_predictions()
    sub = points.loc[points["galaxy"].eq(GALAXY)].sort_values("r").reset_index(drop=True).copy()
    ratio_min = float(grid["v2_ratio_min"].min())
    ratio_max = float(grid["v2_ratio_max"].max())
    rhi_kpc = float(
        pd.read_csv(DATA / "ngc4183_tilted_ring_orientation_profile_summary.csv").iloc[0]["rhi_kpc"]
    )
    gamma_bound = float(manifest["gamma_bound"])
    velocity_fraction = float(manifest["max_velocity_fractional_change"])

    carrier = sub["v_K_exponential_disk"].astype(float)
    interval_min = carrier * np.sqrt(ratio_min)
    interval_max = carrier * np.sqrt(ratio_max)
    interval_mid = 0.5 * (interval_min + interval_max)

    joined = sub[
        ["galaxy", "r", "vobs", "errv", "vn", "v_v6", "v_mond", "v_K_exponential_disk"]
    ].copy()
    joined["x_R_over_RHI"] = joined["r"].astype(float) / rhi_kpc
    joined["v2_ratio_min"] = ratio_min
    joined["v2_ratio_max"] = ratio_max
    joined["v_null_control_interval_min_km_s"] = interval_min
    joined["v_null_control_interval_max_km_s"] = interval_max
    joined["v_null_control_interval_midpoint_km_s"] = interval_mid
    joined["null_control_formula_id"] = FORMULA_ID

    distance = interval_distance(
        joined["vobs"],
        joined["v_null_control_interval_min_km_s"],
        joined["v_null_control_interval_max_km_s"],
    )
    inside = distance == 0.0
    joined["null_control_interval_distance_km_s"] = distance
    joined["inside_null_control_interval"] = inside
    joined["construction_used_vobs"] = False
    joined["scoring_used_vobs"] = True
    joined["endpoint_scores_allowed"] = True
    joined["point_selected_from_residual"] = False
    joined["claim_boundary"] = CLAIM_BOUNDARY

    scores = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "model_id": FORMULA_ID,
                "model_role": "accepted_null_control_interval_readout",
                "n_points": len(joined),
                "coverage_fraction": float(inside.mean()),
                "interval_distance_rmse_km_s": rmse(distance),
                "interval_midpoint_rmse_km_s": rmse(
                    joined["v_null_control_interval_midpoint_km_s"] - joined["vobs"]
                ),
                "gamma_bound": gamma_bound,
                "max_velocity_fractional_change": velocity_fraction,
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    baseline_scores = pd.DataFrame(baseline_interval_rows(joined))

    summary = pd.DataFrame(
        [
            {
                "endpoint_status": "NGC4183_ACCEPTED_NULL_CONTROL_INTERVAL_ENDPOINT_COMPLETE",
                "galaxy": GALAXY,
                "formula_id": FORMULA_ID,
                "n_points": len(joined),
                "coverage_fraction": float(inside.mean()),
                "interval_distance_rmse_km_s": rmse(distance),
                "interval_midpoint_rmse_km_s": rmse(
                    joined["v_null_control_interval_midpoint_km_s"] - joined["vobs"]
                ),
                "best_baseline_rmse_km_s": float(baseline_scores["rmse_km_s"].min()),
                "best_baseline_model": str(
                    baseline_scores.sort_values("rmse_km_s")["model_id"].iloc[0]
                ),
                "best_baseline_inside_interval_fraction": float(
                    baseline_scores.sort_values("rmse_km_s")[
                        "fraction_inside_null_control_interval"
                    ].iloc[0]
                ),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_scores_allowed": True,
                "point_selected_from_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "claim_status": (
                    "accepted null-control interval endpoint only; not a point-fit "
                    "endpoint and not population validation"
                ),
            }
        ]
    )

    joined.to_csv(
        DATA / "ngc4183_weak_projection_null_control_accepted_endpoint_points.csv",
        index=False,
    )
    scores.to_csv(
        DATA / "ngc4183_weak_projection_null_control_accepted_endpoint_scores.csv",
        index=False,
    )
    baseline_scores.to_csv(
        DATA / "ngc4183_weak_projection_null_control_accepted_endpoint_baselines.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ngc4183_weak_projection_null_control_accepted_endpoint_summary.csv",
        index=False,
    )

    report = [
        "# NGC4183 Weak-Projection Null-Control Accepted Endpoint",
        "",
        "This endpoint is scored as a frozen interval-control branch, not as a",
        "single fitted point curve. It reads observed velocities only after the",
        "accepted null-control gate and frozen formula manifest have passed.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interval Score",
        "",
        markdown_table(scores),
        "",
        "## Baseline Context",
        "",
        markdown_table(baseline_scores),
        "",
        "## Claim Boundary",
        "",
        "The branch preserves the frozen null-control interval unchanged. It does",
        "not select a residual-tuned point coefficient inside the interval. The",
        "endpoint result is therefore an accepted single-galaxy interval-control",
        "readout, not a point-fit validation and not population validation.",
        "",
    ]
    (REPORTS / "ngc4183_weak_projection_null_control_accepted_endpoint.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
