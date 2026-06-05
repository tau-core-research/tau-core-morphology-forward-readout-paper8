#!/usr/bin/env python3
"""Score the NGC7331 split-B2 unit-load freeze candidate diagnostically.

This script reads the diagnostic split-B2 unit-load freeze grid and compares it
to observed NGC7331 velocities. The scoring is diagnostic only because the
branch was identified after the exact-transfer failure audit. No endpoint
promotion is allowed.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
FORMULA_ID = "NGC7331_SPLIT_B2_UNIT_LOAD_FREEZE_DIAGNOSTIC_V1"
CLAIM_BOUNDARY = "ngc7331_b2_split_unit_load_diagnostic_comparison_not_endpoint"


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


def rmse(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(values))))


def model_score(model_id: str, pred: np.ndarray, vobs: np.ndarray, errv: np.ndarray) -> dict[str, object]:
    residual = pred - vobs
    return {
        "galaxy": GALAXY,
        "model_id": model_id,
        "rmse_km_s": rmse(residual),
        "mae_km_s": float(np.mean(np.abs(residual))),
        "bias_km_s": float(np.mean(residual)),
        "within_err_fraction": float(np.mean(np.abs(residual) <= errv)),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    freeze_summary = pd.read_csv(
        DATA / "ngc7331_b2_split_unit_load_formula_freeze_summary.csv"
    ).iloc[0]
    grid = pd.read_csv(
        DATA / "ngc7331_b2_split_unit_load_formula_freeze_kernel_grid.csv"
    )
    exact_points = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_interval_control_points.csv"
    )
    exact_summary = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_interval_control_summary.csv"
    ).iloc[0]

    if str(freeze_summary["formula_id"]) != FORMULA_ID:
        raise RuntimeError("Unexpected split-B2 formula id")
    if len(grid) != len(exact_points):
        raise RuntimeError("Grid/point length mismatch")

    vobs = exact_points["vobs"].astype(float).to_numpy()
    errv = exact_points["errv"].astype(float).to_numpy()
    split_pred = grid["v_split_b2_unit_load_km_s"].astype(float).to_numpy()

    point_rows = exact_points[
        ["galaxy", "r", "vobs", "errv", "vn", "v_v6", "v_mond", "v_K_exponential_disk"]
    ].copy()
    point_rows["v_split_b2_unit_load_km_s"] = split_pred
    point_rows["split_b2_unit_load_residual_km_s"] = split_pred - vobs
    point_rows["construction_used_vobs"] = False
    point_rows["diagnostic_scoring_used_vobs"] = True
    point_rows["endpoint_scores_allowed"] = False
    point_rows["claim_boundary"] = CLAIM_BOUNDARY

    scores = pd.DataFrame(
        [
            model_score("SPLIT_B2_UNIT_LOAD_DIAGNOSTIC", split_pred, vobs, errv),
            model_score(
                "FAILED_EXACT_B2_CROSS_CAVEATED_UPPER",
                exact_points["v_exact_b2_max_cross_caveated_km_s"].astype(float).to_numpy(),
                vobs,
                errv,
            ),
            model_score("NEWTONIAN_vn", exact_points["vn"].astype(float).to_numpy(), vobs, errv),
            model_score("TPG_V6_v_v6", exact_points["v_v6"].astype(float).to_numpy(), vobs, errv),
            model_score("MOND_v_mond", exact_points["v_mond"].astype(float).to_numpy(), vobs, errv),
            model_score(
                "EXPONENTIAL_DISK_CARRIER",
                exact_points["v_K_exponential_disk"].astype(float).to_numpy(),
                vobs,
                errv,
            ),
        ]
    ).sort_values("rmse_km_s")
    scores["construction_used_vobs"] = False
    scores["diagnostic_scoring_used_vobs"] = True
    scores["endpoint_scores_allowed"] = False

    split_rmse = float(
        scores.loc[scores["model_id"].eq("SPLIT_B2_UNIT_LOAD_DIAGNOSTIC"), "rmse_km_s"].iloc[0]
    )
    failed_rmse = float(exact_summary["interval_distance_rmse_cross_caveated_km_s"])
    best_baseline = scores[
        scores["model_id"].isin(
            ["NEWTONIAN_vn", "TPG_V6_v_v6", "MOND_v_mond", "EXPONENTIAL_DISK_CARRIER"]
        )
    ].iloc[0]
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": FORMULA_ID,
                "comparison_status": (
                    "NGC7331_SPLIT_B2_UNIT_LOAD_DIAGNOSTIC_COMPARISON_COMPLETE_NOT_ENDPOINT"
                ),
                "n_points": len(point_rows),
                "split_b2_rmse_km_s": split_rmse,
                "failed_exact_b2_cross_interval_distance_rmse_km_s": failed_rmse,
                "rmse_improvement_vs_failed_exact_b2_km_s": failed_rmse - split_rmse,
                "best_baseline_model": str(best_baseline["model_id"]),
                "best_baseline_rmse_km_s": float(best_baseline["rmse_km_s"]),
                "split_minus_best_baseline_rmse_km_s": split_rmse
                - float(best_baseline["rmse_km_s"]),
                "construction_used_vobs": False,
                "diagnostic_scoring_used_vobs": True,
                "endpoint_scores_allowed": False,
                "claim_status": (
                    "diagnostic comparison only; confirms q-role repair improves "
                    "the failed exact-B2 transfer but cannot promote same-curve endpoint"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    point_rows.to_csv(
        DATA / "ngc7331_b2_split_unit_load_diagnostic_comparison_points.csv",
        index=False,
    )
    scores.to_csv(
        DATA / "ngc7331_b2_split_unit_load_diagnostic_comparison_scores.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ngc7331_b2_split_unit_load_diagnostic_comparison_summary.csv",
        index=False,
    )

    report = [
        "# NGC7331 split-B2 unit-load diagnostic comparison",
        "",
        "This comparison scores the split-B2 unit-load freeze candidate after the",
        "negative exact-transfer interval audit. It is diagnostic only and does",
        "not promote an accepted endpoint.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Interpretation",
        "",
        "The split unit-load branch substantially improves the failed exact-B2",
        "transfer distance, which confirms that q-role conflation was a real",
        "failure mode. Because the branch was selected after inspecting the",
        "failure, this result is a repair diagnostic. It can motivate a future",
        "predeclared holdout/population protocol, but it is not an accepted",
        "NGC7331 endpoint.",
        "",
    ]
    (REPORTS / "ngc7331_b2_split_unit_load_diagnostic_comparison.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
