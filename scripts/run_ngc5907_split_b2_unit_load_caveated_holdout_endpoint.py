#!/usr/bin/env python3
"""Score the caveated NGC5907 split-B2 unit-load holdout formula.

The formula was frozen by
`build_ngc5907_split_b2_unit_load_formula_freeze_gate.py` before this scoring
script reads observed velocities. This endpoint remains caveated because the
radial denominator is the optical warp support radius rather than SPARC RHI.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC5907"
CLAIM_BOUNDARY = "ngc5907_split_b2_unit_load_caveated_holdout_preliminary_control"


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


def score_model(df: pd.DataFrame, model_id: str, column: str, role: str) -> dict[str, object]:
    residual = df[column].astype(float) - df["vobs"].astype(float)
    return {
        "galaxy": GALAXY,
        "model_id": model_id,
        "model_role": role,
        "n_points": len(df),
        "rmse_km_s": float(np.sqrt(np.mean(residual**2))),
        "mae_km_s": float(np.mean(np.abs(residual))),
        "bias_km_s": float(np.mean(residual)),
        "within_error_fraction": float(
            np.mean(np.abs(residual) <= df["errv"].astype(float))
        ),
        "construction_used_vobs": False,
        "scoring_used_vobs": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(
        DATA / "ngc5907_split_b2_unit_load_formula_freeze_manifest.csv"
    ).iloc[0]
    freeze_summary = pd.read_csv(
        DATA / "ngc5907_split_b2_unit_load_formula_freeze_summary.csv"
    ).iloc[0]
    kernel = pd.read_csv(
        DATA / "ngc5907_split_b2_unit_load_formula_freeze_kernel_grid.csv"
    )
    observed = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_points.csv",
        usecols=[
            "r",
            "vobs",
            "errv",
            "vn",
            "v_v6",
            "v_mond",
            "v_K_exponential_disk",
            "v_mixed_population",
        ],
    )
    projection = pd.read_csv(
        DATA / "ngc5907_projection_accepted_endpoint_points.csv",
        usecols=["r", "v_projection_accepted"],
    )

    if bool(manifest["uses_vobs_or_residual_in_construction"]):
        raise RuntimeError("frozen manifest is not endpoint-blind")
    if not bool(freeze_summary["future_separate_scoring_gate_required"]):
        raise RuntimeError("freeze summary does not require separate scoring gate")

    points = observed.merge(
        kernel[
            [
                "r_kpc",
                "kernel_ramp",
                "delta_v2_split_km2_s2",
                "v_split_b2_unit_load_km_s",
            ]
        ],
        left_on="r",
        right_on="r_kpc",
        how="inner",
        validate="one_to_one",
    ).merge(projection, on="r", how="left", validate="one_to_one")

    points["galaxy"] = GALAXY
    points["formula_id"] = str(manifest["formula_id"])
    points["endpoint_scores_allowed"] = True
    points["construction_used_vobs"] = False
    points["scoring_used_vobs"] = True
    points["claim_boundary"] = CLAIM_BOUNDARY

    models = [
        ("TAU_NGC5907_SPLIT_B2_UNIT_LOAD_CAVEATED", "v_split_b2_unit_load_km_s", "matched_split_b2_holdout_readout"),
        ("TAU_NGC5907_EXPDISK_PROJECTION_MIXED_ACCEPTED", "v_mixed_population", "existing_matched_mixed_readout_context"),
        ("TAU_NGC5907_PROJECTION_ACCEPTED", "v_projection_accepted", "existing_projection_readout_context"),
        ("TPG_V6_v_v6", "v_v6", "baseline"),
        ("MOND_v_mond", "v_mond", "baseline"),
        ("EXPONENTIAL_DISK_CARRIER", "v_K_exponential_disk", "baseline"),
        ("NEWTONIAN_vn", "vn", "baseline"),
    ]
    scores = pd.DataFrame([score_model(points, *model) for model in models])
    scores = scores.sort_values("rmse_km_s").reset_index(drop=True)

    split_rmse = float(
        scores.loc[
            scores["model_id"].eq("TAU_NGC5907_SPLIT_B2_UNIT_LOAD_CAVEATED"),
            "rmse_km_s",
        ].iloc[0]
    )
    best_baseline = scores.loc[scores["model_role"].eq("baseline")].iloc[0]
    best_existing_tau = scores.loc[
        scores["model_role"].str.contains("existing_", regex=False)
    ].iloc[0]

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": str(manifest["formula_id"]),
                "endpoint_status": (
                    "CAVEATED_SPLIT_B2_HOLDOUT_PRELIMINARY_CONTROL_SCORED"
                ),
                "n_points": len(points),
                "split_b2_rmse_km_s": split_rmse,
                "best_baseline_model": str(best_baseline["model_id"]),
                "best_baseline_rmse_km_s": float(best_baseline["rmse_km_s"]),
                "split_minus_best_baseline_rmse_km_s": split_rmse
                - float(best_baseline["rmse_km_s"]),
                "best_existing_tau_context_model": str(best_existing_tau["model_id"]),
                "best_existing_tau_context_rmse_km_s": float(best_existing_tau["rmse_km_s"]),
                "split_minus_best_existing_tau_context_rmse_km_s": split_rmse
                - float(best_existing_tau["rmse_km_s"]),
                "denominator_caveat": str(manifest["denominator_caveat"]),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_scores_allowed": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    points.to_csv(
        DATA / "ngc5907_split_b2_unit_load_caveated_holdout_endpoint_points.csv",
        index=False,
    )
    scores.to_csv(
        DATA / "ngc5907_split_b2_unit_load_caveated_holdout_endpoint_scores.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ngc5907_split_b2_unit_load_caveated_holdout_endpoint_summary.csv",
        index=False,
    )

    report = f"""# NGC5907 Split-B2 Unit-Load Caveated Holdout Endpoint

Status: `{summary.iloc[0]['endpoint_status']}`

This scoring script reads the frozen split-B2 manifest and kernel grid
unchanged. It reads observed velocities only for endpoint scoring.

## Summary

{markdown_table(summary)}

## Scores

{markdown_table(scores)}

## Interpretation

The split-B2 unit-load candidate is scored as a caveated preliminary control
because its denominator is the optical warp support radius, not SPARC/HI RHI.
It is therefore a useful independent-galaxy stress test of the NGC7331
split-B2 repair, but not yet a clean population endpoint.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    (
        REPORTS
        / "ngc5907_split_b2_unit_load_caveated_holdout_endpoint.md"
    ).write_text(report, encoding="utf-8")

    print(summary.to_string(index=False))
    print(scores[["model_id", "model_role", "rmse_km_s"]].to_string(index=False))


if __name__ == "__main__":
    main()
