#!/usr/bin/env python3
"""Audit the NGC7331 exact B2 q-placement failure mode.

This is a diagnostic ablation only. It reads the already frozen NGC7331 exact
B2 interval manifest and the post-freeze scoring points, then compares several
q-placement variants after the negative interval-control result. The variants
are not endpoint candidates because they are inspected after seeing the
NGC7331 failure.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_formula_freeze_manifest.csv"
    ).iloc[0]
    points = pd.read_csv(
        DATA / "ngc7331_b2_exact_transfer_interval_control_points.csv"
    )

    q_max = float(manifest["q_warp_max"])
    x_w = float(manifest["x_w_formula_freeze"])
    vflat = float(manifest["vflat_km_s"])
    epsilon_cross = float(manifest["epsilon_cross_bound"])

    x = points["x_R_over_RHI"].astype(float).to_numpy()
    ramp = np.maximum(0.0, (x - x_w) / (1.0 - x_w))
    active = ramp > 0.0
    vobs = points["vobs"].astype(float).to_numpy()
    errv = points["errv"].astype(float).to_numpy()
    vn = points["vn"].astype(float).to_numpy()
    required_delta_v2 = vobs**2 - vn**2
    source_scale = x_w * vflat**2

    carriers = {
        "NEWTONIAN_vn": points["vn"].astype(float).to_numpy(),
        "EXPONENTIAL_DISK_CARRIER": points["v_K_exponential_disk"].astype(float).to_numpy(),
        "TPG_V6_v_v6": points["v_v6"].astype(float).to_numpy(),
        "MOND_v_mond": points["v_mond"].astype(float).to_numpy(),
    }
    amplitude_variants = {
        "lambda_q_xw_vflat2": q_max * source_scale,
        "lambda_xw_vflat2": source_scale,
        "lambda_q_xw_vflat2_cross_high": q_max * source_scale * (1.0 + epsilon_cross),
        "lambda_xw_vflat2_cross_high": source_scale * (1.0 + epsilon_cross),
    }
    kernel_variants = {
        "kernel_q_ramp": q_max * ramp,
        "kernel_ramp": ramp,
    }

    rows: list[dict[str, object]] = []
    for carrier_id, carrier in carriers.items():
        for amplitude_id, amplitude in amplitude_variants.items():
            for kernel_id, kernel in kernel_variants.items():
                for sign_id, sign in [("plus_added_readout", 1.0), ("minus_attenuation", -1.0)]:
                    delta_v2 = sign * amplitude * kernel
                    pred = np.sqrt(np.maximum(carrier**2 + delta_v2, 0.0))
                    residual = pred - vobs
                    rows.append(
                        {
                            "galaxy": GALAXY,
                            "diagnostic_variant_id": (
                                f"{carrier_id}__{amplitude_id}__{kernel_id}__{sign_id}"
                            ),
                            "carrier_id": carrier_id,
                            "amplitude_id": amplitude_id,
                            "kernel_id": kernel_id,
                            "sign_id": sign_id,
                            "q_power_effective": (
                                2
                                if amplitude_id.startswith("lambda_q_")
                                and kernel_id == "kernel_q_ramp"
                                else 1
                                if amplitude_id.startswith("lambda_q_")
                                or kernel_id == "kernel_q_ramp"
                                else 0
                            ),
                            "amplitude_km2_s2": amplitude,
                            "rmse_km_s": rmse(residual),
                            "mae_km_s": float(np.mean(np.abs(residual))),
                            "inner_rmse_km_s": rmse(residual[~active]),
                            "outer_rmse_km_s": rmse(residual[active]),
                            "within_err_fraction": float(np.mean(np.abs(residual) <= errv)),
                            "last_radius_prediction_km_s": float(pred[-1]),
                            "construction_used_vobs": False,
                            "diagnostic_scoring_used_vobs": True,
                            "endpoint_scores_allowed": False,
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )

    scores = pd.DataFrame(rows).sort_values("rmse_km_s")

    required_rows: list[dict[str, object]] = []
    for kernel_id, kernel in {
        "current_kernel_q_ramp": q_max * ramp,
        "ramp_only": ramp,
    }.items():
        valid_kernel = kernel[active]
        required_lambda = required_delta_v2[active] / valid_kernel
        required_rows.append(
            {
                "galaxy": GALAXY,
                "kernel_id": kernel_id,
                "required_lambda_median_km2_s2": float(np.median(required_lambda)),
                "required_lambda_p25_km2_s2": float(np.percentile(required_lambda, 25)),
                "required_lambda_p75_km2_s2": float(np.percentile(required_lambda, 75)),
                "required_lambda_min_km2_s2": float(np.min(required_lambda)),
                "required_lambda_max_km2_s2": float(np.max(required_lambda)),
                "required_lambda_cv": float(
                    np.std(required_lambda) / np.mean(required_lambda)
                ),
                "source_lambda_qmax_km2_s2": q_max * source_scale,
                "source_scale_xw_vflat2_km2_s2": source_scale,
                "construction_used_vobs": False,
                "diagnostic_scoring_used_vobs": True,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    required = pd.DataFrame(required_rows)
    current = scores[
        (scores["carrier_id"] == "NEWTONIAN_vn")
        & (scores["amplitude_id"] == "lambda_q_xw_vflat2")
        & (scores["kernel_id"] == "kernel_q_ramp")
        & (scores["sign_id"] == "plus_added_readout")
    ].iloc[0]
    no_q_unit = scores[
        (scores["carrier_id"] == "NEWTONIAN_vn")
        & (scores["amplitude_id"] == "lambda_xw_vflat2")
        & (scores["kernel_id"] == "kernel_ramp")
        & (scores["sign_id"] == "plus_added_readout")
    ].iloc[0]
    exp_baseline = scores[
        (scores["carrier_id"] == "EXPONENTIAL_DISK_CARRIER")
        & (scores["amplitude_id"] == "lambda_q_xw_vflat2")
        & (scores["kernel_id"] == "kernel_q_ramp")
        & (scores["sign_id"] == "plus_added_readout")
    ].iloc[0]

    q_double_required = np.sqrt(
        np.maximum(required_delta_v2[active] / (source_scale * ramp[active]), 0.0)
    )
    q_single_required = np.maximum(
        required_delta_v2[active] / (source_scale * ramp[active]), 0.0
    )
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "audit_status": "NGC7331_B2_Q_PLACEMENT_ABLATION_DIAGNOSTIC_COMPLETE_NOT_ENDPOINT",
                "n_points": len(points),
                "n_outer_active_points": int(active.sum()),
                "source_q_warp_max": q_max,
                "current_effective_q_power": 2,
                "current_rmse_km_s": float(current["rmse_km_s"]),
                "current_outer_rmse_km_s": float(current["outer_rmse_km_s"]),
                "best_diagnostic_variant": str(scores.iloc[0]["diagnostic_variant_id"]),
                "best_diagnostic_rmse_km_s": float(scores.iloc[0]["rmse_km_s"]),
                "no_q_unit_newtonian_ramp_rmse_km_s": float(no_q_unit["rmse_km_s"]),
                "no_q_unit_newtonian_ramp_outer_rmse_km_s": float(
                    no_q_unit["outer_rmse_km_s"]
                ),
                "diagnostic_exponential_carrier_rmse_km_s": float(
                    exp_baseline["rmse_km_s"]
                ),
                "required_q_double_median": float(np.median(q_double_required)),
                "required_q_single_median": float(np.median(q_single_required)),
                "required_q_double_to_source_qmax_median_ratio": float(
                    np.median(q_double_required) / q_max
                ),
                "failure_mode": (
                    "q_warp is effectively squared by the transferred protocol; "
                    "NGC4088 had q_warp=1 so the issue was hidden, but NGC7331 "
                    "has q_warp<1 and the outer correction is suppressed"
                ),
                "claim_status": (
                    "diagnostic ablation only; variants inspected after negative "
                    "interval-control audit and cannot be used as endpoints"
                ),
                "construction_used_vobs": False,
                "diagnostic_scoring_used_vobs": True,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    scores.to_csv(DATA / "ngc7331_b2_q_placement_ablation_scores.csv", index=False)
    required.to_csv(
        DATA / "ngc7331_b2_q_placement_required_amplitude_audit.csv", index=False
    )
    summary.to_csv(DATA / "ngc7331_b2_q_placement_ablation_summary.csv", index=False)

    report = [
        "# NGC7331 B2 q-placement ablation audit",
        "",
        "This is a diagnostic hiba-audit, not a new endpoint. It was run after",
        "the negative exact B2 interval-control result to localize the failure",
        "mode of the transferred NGC4088 B2 shell.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Top diagnostic variants",
        "",
        markdown_table(scores.head(12)),
        "",
        "## Required amplitude audit",
        "",
        markdown_table(required),
        "",
        "## Interpretation",
        "",
        "The transferred exact B2 protocol places `q_warp` both in `lambda_w` and",
        "in `C_warp`, so the outer correction scales effectively as `q_warp^2`.",
        "That was invisible in NGC4088 because its frozen protocol used",
        "`q_warp=1`. It becomes a serious suppression in NGC7331, where the",
        "source-side interval has `q_warp < 1`. The diagnostic no-q unit-ramp",
        "variant is not an endpoint, but its improved RMSE localizes the failure",
        "to the q-placement/source-load law rather than to the ramp shape alone.",
        "",
    ]
    (REPORTS / "ngc7331_b2_q_placement_ablation_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
