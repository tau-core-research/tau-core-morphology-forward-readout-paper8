#!/usr/bin/env python3
"""Diagnose whether B2 q_warp should be split into shape and load roles.

This is a post-failure theory/numerical audit. It does not create an endpoint.
It asks whether the NGC7331 exact-transfer failure is better described as a
wrong ramp shape or as a conflation of two source-side roles:

    q_shape: how strongly the radial kernel is spatially gated;
    mu_load: how strongly the source loads the velocity-squared carrier.

NGC4088 used q_warp=1, so q_shape and mu_load were observationally degenerate
in the frozen single-galaxy protocol. NGC7331 breaks that degeneracy.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint"


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

    q_shape = float(manifest["q_warp_max"])
    x_w = float(manifest["x_w_formula_freeze"])
    vflat = float(manifest["vflat_km_s"])
    source_scale = x_w * vflat**2
    x = points["x_R_over_RHI"].astype(float).to_numpy()
    ramp = np.maximum(0.0, (x - x_w) / (1.0 - x_w))
    active = ramp > 0
    vobs = points["vobs"].astype(float).to_numpy()
    vn = points["vn"].astype(float).to_numpy()
    required_delta_v2 = vobs**2 - vn**2

    # Existing protocol: q_shape and mu_load are identified.
    current_delta_v2 = q_shape * source_scale * (q_shape * ramp)
    current_pred = np.sqrt(np.maximum(vn**2 + current_delta_v2, 0.0))

    # Split-role diagnostic: q_shape governs the kernel only if explicitly used;
    # mu_load is a separate source-load coefficient. The following mu estimates
    # are descriptive diagnostics computed after the failed interval audit.
    required_mu_with_ramp_kernel = required_delta_v2[active] / (
        source_scale * ramp[active]
    )
    required_mu_with_q_kernel = required_delta_v2[active] / (
        source_scale * q_shape * ramp[active]
    )

    role_rows = pd.DataFrame(
        [
            {
                "role_id": "current_identified_role",
                "formula": "Delta v^2 = q_warp^2 x_w Vflat^2 ramp",
                "q_shape_factor": q_shape,
                "mu_load_factor": q_shape,
                "effective_q_power": 2,
                "interpretation": (
                    "NGC4088-degenerate convention; suppresses NGC7331 because q_warp<1"
                ),
                "status": "DIAGNOSTIC_FAILURE_MODE",
            },
            {
                "role_id": "shape_only_q_role",
                "formula": "Delta v^2 = mu_load x_w Vflat^2 q_shape ramp",
                "q_shape_factor": q_shape,
                "mu_load_factor": float(np.median(required_mu_with_q_kernel)),
                "effective_q_power": 1,
                "interpretation": (
                    "keeps q_warp as spatial source strength; requires separate load coefficient"
                ),
                "status": "POST_FAILURE_DIAGNOSTIC_ONLY",
            },
            {
                "role_id": "load_not_shape_q_role",
                "formula": "Delta v^2 = mu_load x_w Vflat^2 ramp",
                "q_shape_factor": 1.0,
                "mu_load_factor": float(np.median(required_mu_with_ramp_kernel)),
                "effective_q_power": 0,
                "interpretation": (
                    "treats THINGS q_warp as not the B2 radial kernel amplitude"
                ),
                "status": "POST_FAILURE_DIAGNOSTIC_ONLY",
            },
        ]
    )
    role_rows["galaxy"] = GALAXY
    role_rows["construction_used_vobs"] = False
    role_rows["diagnostic_scoring_used_vobs"] = True
    role_rows["endpoint_scores_allowed"] = False
    role_rows["claim_boundary"] = CLAIM_BOUNDARY

    diagnostic_rows: list[dict[str, object]] = []
    for role_id, kernel, mu_load in [
        ("current_identified_role", q_shape * ramp, q_shape),
        ("shape_only_q_role_median_mu", q_shape * ramp, np.median(required_mu_with_q_kernel)),
        ("load_not_shape_q_role_median_mu", ramp, np.median(required_mu_with_ramp_kernel)),
        ("unit_load_unit_shape_reference", ramp, 1.0),
    ]:
        delta_v2 = mu_load * source_scale * kernel
        pred = np.sqrt(np.maximum(vn**2 + delta_v2, 0.0))
        residual = pred - vobs
        diagnostic_rows.append(
            {
                "galaxy": GALAXY,
                "role_id": role_id,
                "mu_load_used": float(mu_load),
                "kernel_uses_q_shape": bool(role_id in {
                    "current_identified_role",
                    "shape_only_q_role_median_mu",
                }),
                "rmse_km_s": rmse(residual),
                "outer_rmse_km_s": rmse(residual[active]),
                "inner_rmse_km_s": rmse(residual[~active]),
                "last_radius_prediction_km_s": float(pred[-1]),
                "construction_used_vobs": False,
                "diagnostic_scoring_used_vobs": True,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    diagnostics = pd.DataFrame(diagnostic_rows).sort_values("rmse_km_s")
    required = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "quantity": "required_mu_load_if_kernel_is_ramp",
                "median": float(np.median(required_mu_with_ramp_kernel)),
                "p25": float(np.percentile(required_mu_with_ramp_kernel, 25)),
                "p75": float(np.percentile(required_mu_with_ramp_kernel, 75)),
                "min": float(np.min(required_mu_with_ramp_kernel)),
                "max": float(np.max(required_mu_with_ramp_kernel)),
                "source_q_shape_max": q_shape,
                "median_to_source_q_shape_ratio": float(
                    np.median(required_mu_with_ramp_kernel) / q_shape
                ),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": GALAXY,
                "quantity": "required_mu_load_if_kernel_is_q_shape_ramp",
                "median": float(np.median(required_mu_with_q_kernel)),
                "p25": float(np.percentile(required_mu_with_q_kernel, 25)),
                "p75": float(np.percentile(required_mu_with_q_kernel, 75)),
                "min": float(np.min(required_mu_with_q_kernel)),
                "max": float(np.max(required_mu_with_q_kernel)),
                "source_q_shape_max": q_shape,
                "median_to_source_q_shape_ratio": float(
                    np.median(required_mu_with_q_kernel) / q_shape
                ),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "audit_status": "NGC7331_B2_Q_ROLE_SEPARATION_DIAGNOSTIC_COMPLETE_NOT_ENDPOINT",
                "current_formula": "Delta v^2 = q_warp^2 x_w Vflat^2 ramp",
                "recommended_theory_fix": (
                    "split q_warp into q_shape and mu_load before any future freeze"
                ),
                "source_q_shape_max": q_shape,
                "current_rmse_km_s": float(rmse(current_pred - vobs)),
                "unit_load_unit_shape_reference_rmse_km_s": float(
                    diagnostics.loc[
                        diagnostics["role_id"].eq("unit_load_unit_shape_reference"),
                        "rmse_km_s",
                    ].iloc[0]
                ),
                "required_mu_load_if_ramp_kernel_median": float(
                    np.median(required_mu_with_ramp_kernel)
                ),
                "required_mu_load_if_q_kernel_median": float(
                    np.median(required_mu_with_q_kernel)
                ),
                "claim_status": (
                    "diagnostic-only formula-role separation; no endpoint promotion"
                ),
                "construction_used_vobs": False,
                "diagnostic_scoring_used_vobs": True,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    role_rows.to_csv(DATA / "ngc7331_b2_q_role_separation_roles.csv", index=False)
    diagnostics.to_csv(
        DATA / "ngc7331_b2_q_role_separation_diagnostics.csv", index=False
    )
    required.to_csv(
        DATA / "ngc7331_b2_q_role_separation_required_mu.csv", index=False
    )
    summary.to_csv(DATA / "ngc7331_b2_q_role_separation_summary.csv", index=False)

    report = [
        "# NGC7331 B2 q-role separation diagnostic",
        "",
        "This diagnostic follows the failed NGC7331 exact B2 interval-control",
        "audit. It is not an endpoint and does not promote a new formula.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Role split",
        "",
        markdown_table(role_rows),
        "",
        "## Diagnostic scores",
        "",
        markdown_table(diagnostics),
        "",
        "## Required source-load coefficient",
        "",
        markdown_table(required),
        "",
        "## Verdict",
        "",
        "The B2 transfer should not identify the radial kernel strength and the",
        "source-load amplitude by default. NGC4088 could not expose this because",
        "`q_warp=1`; NGC7331 does expose it because the source q interval is well",
        "below one. The next theory task is to derive a Tau-side `mu_load` or",
        "other source-load coefficient independently of the observed rotation",
        "residuals, while keeping `q_shape` as a source morphology/kernel handle.",
        "",
    ]
    (REPORTS / "ngc7331_b2_q_role_separation_diagnostic.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
