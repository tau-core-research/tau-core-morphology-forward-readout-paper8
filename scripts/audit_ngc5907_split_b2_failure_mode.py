#!/usr/bin/env python3
"""Audit why the NGC5907 split-B2 unit-load holdout fails.

This diagnostic preserves the negative result from the caveated split-B2
endpoint score. It does not tune a replacement formula.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC5907"
CLAIM_BOUNDARY = "ngc5907_split_b2_failure_mode_audit_not_formula_tuning"


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


def rmse(values: pd.Series) -> float:
    return float(np.sqrt(np.mean(values.astype(float) ** 2)))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    points = pd.read_csv(
        DATA / "ngc5907_split_b2_unit_load_caveated_holdout_endpoint_points.csv"
    )
    summary = pd.read_csv(
        DATA / "ngc5907_split_b2_unit_load_caveated_holdout_endpoint_summary.csv"
    ).iloc[0]
    manifest = pd.read_csv(
        DATA / "ngc5907_split_b2_unit_load_formula_freeze_manifest.csv"
    ).iloc[0]

    r_outer = float(manifest["r_outer_kpc"])
    x_w = float(manifest["x_w_formula_freeze"])
    r_start = r_outer * x_w

    residual_cols = {
        "split_b2": "v_split_b2_unit_load_km_s",
        "projection": "v_projection_accepted",
        "mixed_projection": "v_mixed_population",
        "tpg_v6": "v_v6",
        "mond": "v_mond",
        "newtonian": "vn",
    }
    for label, column in residual_cols.items():
        points[f"resid_{label}_km_s"] = points[column].astype(float) - points["vobs"].astype(float)

    points["radial_zone"] = np.select(
        [
            points["r"].astype(float) < r_start,
            (points["r"].astype(float) >= r_start)
            & (points["r"].astype(float) <= r_outer),
            points["r"].astype(float) > r_outer,
        ],
        ["inner_inactive_ramp", "source_warp_window", "beyond_source_window"],
        default="unclassified",
    )

    zone_rows = []
    for zone, group in points.groupby("radial_zone", sort=False):
        row = {
            "galaxy": GALAXY,
            "radial_zone": zone,
            "n_points": len(group),
            "r_min_kpc": float(group["r"].min()),
            "r_max_kpc": float(group["r"].max()),
            "mean_kernel_ramp": float(group["kernel_ramp"].mean()),
            "split_b2_rmse_km_s": rmse(group["resid_split_b2_km_s"]),
            "projection_rmse_km_s": rmse(group["resid_projection_km_s"]),
            "tpg_v6_rmse_km_s": rmse(group["resid_tpg_v6_km_s"]),
            "newtonian_rmse_km_s": rmse(group["resid_newtonian_km_s"]),
            "split_b2_mean_bias_km_s": float(group["resid_split_b2_km_s"].mean()),
        }
        zone_rows.append(row)
    zones = pd.DataFrame(zone_rows)
    zones["claim_boundary"] = CLAIM_BOUNDARY

    failure_modes = pd.DataFrame(
        [
            {
                "failure_mode": "INNER_CARRIER_UNDERPREDICTION",
                "evidence": (
                    "For R<R_warp_start the ramp is zero, so split-B2 reduces to "
                    "the Newtonian carrier; NGC5907 requires a strong non-Newtonian/"
                    "projection-like carrier already in this region."
                ),
                "affected_zone": "inner_inactive_ramp",
                "formula_implication": (
                    "standalone Newtonian+added split-B2 is the wrong readout class"
                ),
                "not_a_tuning_instruction": True,
            },
            {
                "failure_mode": "OUTER_ADDED_READOUT_OVERBOOST",
                "evidence": (
                    "Beyond the source optical warp window the linear ramp continues "
                    "above unity and the added velocity-squared term overshoots."
                ),
                "affected_zone": "beyond_source_window",
                "formula_implication": (
                    "NGC5907 prefers bounded projection/attenuation behavior, not an "
                    "unbounded added warp-history ramp"
                ),
                "not_a_tuning_instruction": True,
            },
            {
                "failure_mode": "MORPHOLOGY_LANE_MISMATCH",
                "evidence": (
                    "Existing projection and TPG-like baselines remain strong while "
                    "split-B2 added readout fails."
                ),
                "affected_zone": "global",
                "formula_implication": (
                    "NGC5907 supports projection-dominated readout classification over "
                    "split-B2 added-readout transfer"
                ),
                "not_a_tuning_instruction": True,
            },
        ]
    )
    failure_modes["galaxy"] = GALAXY
    failure_modes["claim_boundary"] = CLAIM_BOUNDARY

    audit_summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "failure_audit_status": (
                    "NGC5907_SPLIT_B2_NEGATIVE_RESULT_FAILURE_MODE_AUDIT_COMPLETE"
                ),
                "split_b2_rmse_km_s": float(summary["split_b2_rmse_km_s"]),
                "best_baseline_model": str(summary["best_baseline_model"]),
                "best_baseline_rmse_km_s": float(summary["best_baseline_rmse_km_s"]),
                "best_existing_tau_context_model": str(
                    summary["best_existing_tau_context_model"]
                ),
                "best_existing_tau_context_rmse_km_s": float(
                    summary["best_existing_tau_context_rmse_km_s"]
                ),
                "primary_interpretation": (
                    "negative holdout: split-B2 added-readout does not transfer to "
                    "NGC5907; projection/TPG-like lane remains favored"
                ),
                "formula_tuned": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    points.to_csv(DATA / "ngc5907_split_b2_failure_mode_points.csv", index=False)
    zones.to_csv(DATA / "ngc5907_split_b2_failure_mode_zones.csv", index=False)
    failure_modes.to_csv(DATA / "ngc5907_split_b2_failure_modes.csv", index=False)
    audit_summary.to_csv(DATA / "ngc5907_split_b2_failure_mode_summary.csv", index=False)

    report = f"""# NGC5907 Split-B2 Failure Mode Audit

Status: `{audit_summary.iloc[0]['failure_audit_status']}`

This audit preserves the negative split-B2 result. It does not tune a new
formula.

## Summary

{markdown_table(audit_summary)}

## Radial Zones

{markdown_table(zones)}

## Failure Modes

{markdown_table(failure_modes)}

## Interpretation

The failed split-B2 holdout is informative. NGC5907 already needs a strong
projection/TGP-like carrier in the inner region where the split-B2 ramp is
inactive. In the outer region the added ramp overboosts. This points away from
an added warp-history readout and toward a bounded projection/attenuation
readout for this galaxy.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    (REPORTS / "ngc5907_split_b2_failure_mode_audit.md").write_text(
        report, encoding="utf-8"
    )

    print(audit_summary.to_string(index=False))
    print(zones.to_string(index=False))


if __name__ == "__main__":
    main()
