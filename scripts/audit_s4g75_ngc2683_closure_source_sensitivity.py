#!/usr/bin/env python3
"""Audit NGC2683 closure-source prototype sensitivity.

This audit varies only residual-blind prototype knobs around the first
flare-closure source rule: locality width and ring-offset strength.  It keeps
the train-derived amplitude policy fixed and does not authorize endpoint
promotion.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc2683_closure_source_sensitivity_not_validation"
GALAXY = "NGC2683"
FAMILY = "K_thick_flared"

LOCALITY_MULTIPLIERS = [0.5, 1.0, 1.5, 2.0]
RING_STRENGTHS = [0.0, 0.5, 1.0]
POST22_POLICY = "post22_linear_taper_to_inner_height"

INTEGRATE = getattr(np, "trapezoid", np.trapz)

sys.path.insert(0, str(ROOT / "scripts"))
import run_s4g75_ngc2683_flare_closure_source_prototype as proto  # noqa: E402
import run_s4g75_promoted_kernel_endpoint_stress_test as promoted  # noqa: E402
import run_source_native_readout_formula_endpoint as src  # noqa: E402


def rmse(sub: pd.DataFrame, pred_col: str) -> float:
    return float(((sub[pred_col] - sub["vobs"]).pow(2).mean()) ** 0.5)


def closure_profile_with_strength(
    grid: np.ndarray,
    post22_policy: str,
    ring_strength: float,
    r_outer: float,
) -> np.ndarray:
    height = proto.source_flare_height(grid, post22_policy, r_outer)
    safe_h = np.maximum(height, 1.0e-6)
    log_h = np.log(safe_h)
    log_r = np.log(np.maximum(grid, 1.0e-4))
    dlogh_dlogr = np.gradient(log_h, log_r)
    source = np.maximum(dlogh_dlogr, 0.0)
    if ring_strength > 0:
        ring_width = 1.5
        ring = ring_strength * (proto.RING_VERTICAL_OFFSET_KPC / proto.H_MAX_KPC) * np.exp(
            -0.5 * ((grid - proto.R_SAT_END_KPC) / ring_width) ** 2
        )
        source = source + ring
    max_value = float(np.max(source))
    if max_value > 0:
        source = source / max_value
    return source


def nonlocal_kernel_with_strength(
    radii: np.ndarray,
    scale_radius: float,
    locality_width_kpc: float,
    ring_strength: float,
) -> np.ndarray:
    r_outer = float(np.max(radii))
    grid = np.linspace(0.0, r_outer, 768)
    source = closure_profile_with_strength(grid, POST22_POLICY, ring_strength, r_outer)
    disk_weight = np.exp(-grid / max(scale_radius, 1.0e-6))
    values = []
    for radius in radii:
        locality = np.exp(-0.5 * ((grid - radius) / max(locality_width_kpc, 1.0e-6)) ** 2)
        weight = disk_weight * locality
        den = INTEGRATE(weight, grid)
        averaged = float(INTEGRATE(weight * source, grid) / den) if den > 0 else 0.0
        values.append(scale_radius * averaged)
    return np.asarray(values, dtype=float)


def build_sensitivity() -> tuple[pd.DataFrame, pd.DataFrame]:
    points, _labels = src.load_points()
    base_points = promoted.apply_promoted_observables(points)
    scalar_kernel_points = src.add_bridge_formula_kernels(base_points)
    amplitudes = src.fit_amplitudes(scalar_kernel_points)
    scalar_scored = src.add_predictions(scalar_kernel_points, amplitudes)
    scalar_ngc = scalar_scored.loc[scalar_scored["galaxy"] == GALAXY].copy()
    scalar_rmse = rmse(scalar_ngc, f"v_{FAMILY}")
    beta = float(
        amplitudes.loc[
            amplitudes["formula_family"] == FAMILY,
            "beta_delta_v2_amplitude",
        ].iloc[0]
    )
    scale_radius = float(scalar_ngc["scale_radius_proxy_kpc"].iloc[0])
    radii = scalar_ngc["r"].to_numpy()
    rows = []
    points_rows = []
    for locality_multiplier in LOCALITY_MULTIPLIERS:
        locality_width = locality_multiplier * scale_radius
        for ring_strength in RING_STRENGTHS:
            scored = scalar_scored.copy()
            mask = scored["galaxy"] == GALAXY
            closure_kernel = nonlocal_kernel_with_strength(
                radii,
                scale_radius=scale_radius,
                locality_width_kpc=locality_width,
                ring_strength=ring_strength,
            )
            scored.loc[mask, f"kernel_{FAMILY}"] = closure_kernel
            scored = src.add_predictions(scored, amplitudes)
            sub = scored.loc[scored["galaxy"] == GALAXY].copy()
            candidate_rmse = rmse(sub, f"v_{FAMILY}")
            rows.append(
                {
                    "galaxy": GALAXY,
                    "post22_policy": POST22_POLICY,
                    "locality_multiplier": locality_multiplier,
                    "locality_width_kpc": locality_width,
                    "ring_strength": ring_strength,
                    "beta_delta_v2_amplitude": beta,
                    "scalar_rmse_K_thick_flared": scalar_rmse,
                    "closure_source_rmse_K_thick_flared": candidate_rmse,
                    "closure_source_minus_scalar_rmse": candidate_rmse - scalar_rmse,
                    "closure_kernel_min": float(np.min(closure_kernel)),
                    "closure_kernel_median": float(np.median(closure_kernel)),
                    "closure_kernel_max": float(np.max(closure_kernel)),
                    "accepted_endpoint_ready": False,
                    "endpoint_scores_allowed": False,
                    "endpoint_scores_computed": True,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            for radius, kernel in zip(radii, closure_kernel):
                points_rows.append(
                    {
                        "galaxy": GALAXY,
                        "radius_kpc": radius,
                        "locality_multiplier": locality_multiplier,
                        "ring_strength": ring_strength,
                        "closure_kernel_K_thick_flared": kernel,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    sensitivity = pd.DataFrame(rows)
    point_kernels = pd.DataFrame(points_rows)
    return sensitivity, point_kernels


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


def write_report(sensitivity: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    improved = sensitivity.loc[sensitivity["closure_source_minus_scalar_rmse"] < 0]
    best = sensitivity.sort_values("closure_source_minus_scalar_rmse").iloc[0]
    lines = [
        "# NGC2683 Closure-Source Sensitivity Audit",
        "",
        "This audit varies only residual-blind prototype knobs: locality width and "
        "ring-offset strength. It is not accepted validation.",
        "",
        "## Verdict",
        "",
        f"Grid points checked: {len(sensitivity)}.",
        f"Grid points improving over scalar thick/flared: {len(improved)}.",
        f"Best delta RMSE: {best['closure_source_minus_scalar_rmse']:.6g}.",
        f"Best locality multiplier: {best['locality_multiplier']:.6g}.",
        f"Best ring strength: {best['ring_strength']:.6g}.",
        "",
        "## Sensitivity Table",
        "",
        markdown_table(sensitivity),
        "",
        "## Claim Boundary",
        "",
        "This grid is a formula-development sensitivity map. The best row is not "
        "selected as an endpoint model, because the grid itself is a prototype "
        "design audit and not a predeclared population protocol.",
        "",
    ]
    (REPORTS / "s4g75_ngc2683_closure_source_sensitivity.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    sensitivity, point_kernels = build_sensitivity()
    sensitivity.to_csv(DATA / "s4g75_ngc2683_closure_source_sensitivity.csv", index=False)
    point_kernels.to_csv(DATA / "s4g75_ngc2683_closure_source_sensitivity_points.csv", index=False)
    write_report(sensitivity)
    print(f"wrote {DATA / 's4g75_ngc2683_closure_source_sensitivity.csv'}")
    print(f"wrote {DATA / 's4g75_ngc2683_closure_source_sensitivity_points.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc2683_closure_source_sensitivity.md'}")


if __name__ == "__main__":
    main()
