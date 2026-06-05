#!/usr/bin/env python3
"""Prototype a flare/warp closure-source kernel for NGC2683.

The H(R)-aware damping prototype showed that injecting the flare profile into
the old thick/flared damping family is insufficient.  This diagnostic treats
the radial flare structure as a separate source term: the readout kernel is
driven by where the source-native flare profile changes, rather than by local
thickness alone.  It is a formula-development preflight, not validation.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc2683_flare_closure_source_prototype_not_validation"
GALAXY = "NGC2683"
FAMILY = "K_thick_flared"

R_START_KPC = 9.0
H_START_KPC = 0.5
R_MAX_KPC = 15.0
H_MAX_KPC = 4.0
R_SAT_END_KPC = 22.0
RING_VERTICAL_OFFSET_KPC = 1.3

POST22_POLICIES = [
    "post22_hold_plateau_upper",
    "post22_linear_taper_to_inner_height",
]
CLOSURE_POLICIES = [
    "flare_gradient_source",
    "flare_gradient_plus_ring_offset_source",
]

INTEGRATE = getattr(np, "trapezoid", np.trapz)

sys.path.insert(0, str(ROOT / "scripts"))
import run_s4g75_promoted_kernel_endpoint_stress_test as promoted  # noqa: E402
import run_source_native_readout_formula_endpoint as src  # noqa: E402


def rmse(sub: pd.DataFrame, pred_col: str) -> float:
    return float(((sub[pred_col] - sub["vobs"]).pow(2).mean()) ** 0.5)


def source_flare_height(radius_kpc: np.ndarray, policy: str, r_outer: float) -> np.ndarray:
    radius = np.asarray(radius_kpc, dtype=float)
    scale = (R_MAX_KPC - R_START_KPC) / np.log(H_MAX_KPC / H_START_KPC)
    height = np.full_like(radius, H_START_KPC, dtype=float)
    rise = (radius >= R_START_KPC) & (radius <= R_MAX_KPC)
    height[rise] = H_START_KPC * np.exp((radius[rise] - R_START_KPC) / scale)
    plateau = (radius > R_MAX_KPC) & (radius <= R_SAT_END_KPC)
    height[plateau] = H_MAX_KPC
    post = radius > R_SAT_END_KPC
    if policy == "post22_hold_plateau_upper":
        height[post] = H_MAX_KPC
    elif policy == "post22_linear_taper_to_inner_height":
        denom = max(r_outer - R_SAT_END_KPC, 1.0e-6)
        frac = np.clip((radius[post] - R_SAT_END_KPC) / denom, 0.0, 1.0)
        height[post] = H_MAX_KPC + frac * (H_START_KPC - H_MAX_KPC)
    else:
        raise ValueError(f"unknown post-22 policy: {policy}")
    return height


def closure_profile(
    grid: np.ndarray,
    post22_policy: str,
    closure_policy: str,
    r_outer: float,
) -> np.ndarray:
    height = source_flare_height(grid, post22_policy, r_outer)
    safe_h = np.maximum(height, 1.0e-6)
    log_h = np.log(safe_h)
    log_r = np.log(np.maximum(grid, 1.0e-4))
    dlogh_dlogr = np.gradient(log_h, log_r)
    flare_source = np.maximum(dlogh_dlogr, 0.0)
    if closure_policy == "flare_gradient_source":
        source = flare_source
    elif closure_policy == "flare_gradient_plus_ring_offset_source":
        ring_width = 1.5
        ring = (RING_VERTICAL_OFFSET_KPC / H_MAX_KPC) * np.exp(
            -0.5 * ((grid - R_SAT_END_KPC) / ring_width) ** 2
        )
        source = flare_source + ring
    else:
        raise ValueError(f"unknown closure policy: {closure_policy}")
    max_value = float(np.max(source))
    if max_value > 0:
        source = source / max_value
    return source


def nonlocal_closure_kernel(
    radii: np.ndarray,
    scale_radius: float,
    post22_policy: str,
    closure_policy: str,
    locality_width_kpc: float,
) -> np.ndarray:
    r_outer = float(np.max(radii))
    grid = np.linspace(0.0, r_outer, 768)
    source = closure_profile(grid, post22_policy, closure_policy, r_outer)
    disk_weight = np.exp(-grid / max(scale_radius, 1.0e-6))
    values = []
    for radius in radii:
        locality = np.exp(-0.5 * ((grid - radius) / max(locality_width_kpc, 1.0e-6)) ** 2)
        weight = disk_weight * locality
        den = INTEGRATE(weight, grid)
        averaged = float(INTEGRATE(weight * source, grid) / den) if den > 0 else 0.0
        # Scale by Rs to keep dimensions close to the existing thick/flared
        # kernel shell. This is a prototype normalization, not a final law.
        values.append(scale_radius * averaged)
    return np.asarray(values, dtype=float)


def build_prototype() -> tuple[pd.DataFrame, pd.DataFrame]:
    points, _labels = src.load_points()
    base_points = promoted.apply_promoted_observables(points)
    scalar_kernel_points = src.add_bridge_formula_kernels(base_points)
    amplitudes = src.fit_amplitudes(scalar_kernel_points)
    scalar_scored = src.add_predictions(scalar_kernel_points, amplitudes)
    scalar_ngc = scalar_scored.loc[scalar_scored["galaxy"] == GALAXY].copy()
    beta = float(
        amplitudes.loc[
            amplitudes["formula_family"] == FAMILY,
            "beta_delta_v2_amplitude",
        ].iloc[0]
    )
    scale_radius = float(scalar_ngc["scale_radius_proxy_kpc"].iloc[0])
    radii = scalar_ngc["r"].to_numpy()
    locality_width = scale_radius
    rows = []
    summaries = []

    for post22_policy in POST22_POLICIES:
        for closure_policy in CLOSURE_POLICIES:
            scored = scalar_scored.copy()
            mask = scored["galaxy"] == GALAXY
            closure_kernel = nonlocal_closure_kernel(
                radii,
                scale_radius=scale_radius,
                post22_policy=post22_policy,
                closure_policy=closure_policy,
                locality_width_kpc=locality_width,
            )
            scored.loc[mask, f"kernel_{FAMILY}"] = closure_kernel
            scored = src.add_predictions(scored, amplitudes)
            prototype_ngc = scored.loc[scored["galaxy"] == GALAXY].copy()
            compare = scalar_ngc[
                [
                    "galaxy",
                    "r",
                    "vobs",
                    "v_v6",
                    "v_mond",
                    f"kernel_{FAMILY}",
                    f"v_{FAMILY}",
                ]
            ].rename(
                columns={
                    f"kernel_{FAMILY}": "scalar_kernel_K_thick_flared",
                    f"v_{FAMILY}": "scalar_v_K_thick_flared",
                }
            )
            compare = compare.merge(
                prototype_ngc[
                    [
                        "r",
                        f"kernel_{FAMILY}",
                        f"v_{FAMILY}",
                    ]
                ].rename(
                    columns={
                        f"kernel_{FAMILY}": "closure_source_kernel_K_thick_flared",
                        f"v_{FAMILY}": "closure_source_v_K_thick_flared",
                    }
                ),
                on="r",
                how="left",
                validate="one_to_one",
            )
            compare["post22_policy"] = post22_policy
            compare["closure_policy"] = closure_policy
            compare["locality_width_kpc"] = locality_width
            compare["closure_minus_scalar_kernel"] = (
                compare["closure_source_kernel_K_thick_flared"]
                - compare["scalar_kernel_K_thick_flared"]
            )
            compare["closure_minus_scalar_v"] = (
                compare["closure_source_v_K_thick_flared"]
                - compare["scalar_v_K_thick_flared"]
            )
            compare["accepted_endpoint_ready"] = False
            compare["endpoint_scores_allowed"] = False
            compare["endpoint_scores_computed"] = True
            compare["claim_boundary"] = CLAIM_BOUNDARY
            rows.append(compare)
            summaries.append(
                {
                    "galaxy": GALAXY,
                    "post22_policy": post22_policy,
                    "closure_policy": closure_policy,
                    "n_points": int(len(compare)),
                    "locality_width_kpc": locality_width,
                    "beta_delta_v2_amplitude": beta,
                    "scalar_rmse_K_thick_flared": rmse(compare, "scalar_v_K_thick_flared"),
                    "closure_source_rmse_K_thick_flared": rmse(
                        compare,
                        "closure_source_v_K_thick_flared",
                    ),
                    "closure_source_minus_scalar_rmse": rmse(
                        compare,
                        "closure_source_v_K_thick_flared",
                    )
                    - rmse(compare, "scalar_v_K_thick_flared"),
                    "rmse_tpg_v6": rmse(compare, "v_v6"),
                    "rmse_mond": rmse(compare, "v_mond"),
                    "closure_kernel_min": float(np.min(closure_kernel)),
                    "closure_kernel_median": float(np.median(closure_kernel)),
                    "closure_kernel_max": float(np.max(closure_kernel)),
                    "accepted_endpoint_ready": False,
                    "endpoint_scores_allowed": False,
                    "endpoint_scores_computed": True,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return pd.concat(rows, ignore_index=True), pd.DataFrame(summaries)


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


def write_report(points: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC2683 Flare Closure-Source Kernel Prototype",
        "",
        "This diagnostic treats radial flare structure as a separate closure "
        "source. It is not accepted validation.",
        "",
        "## Prototype Rule",
        "",
        "The source profile is the positive radial gradient of log H(R), optionally "
        "plus a localized ring-offset source near the saturation/outer-ring "
        "region. A nonlocal source-weighted average is evaluated at each rotation "
        "radius with locality width fixed to the S4G/SPARC disk scale.",
        "",
        "## Verdict",
        "",
        markdown_table(summary),
        "",
        "## Point-Level Comparison",
        "",
        markdown_table(
            points[
                [
                    "post22_policy",
                    "closure_policy",
                    "r",
                    "scalar_kernel_K_thick_flared",
                    "closure_source_kernel_K_thick_flared",
                    "scalar_v_K_thick_flared",
                    "closure_source_v_K_thick_flared",
                    "closure_minus_scalar_v",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This is a formula-development preflight. The closure-source policies are "
        "explicit prototype rules and are not source-validated endpoint laws. "
        "Stress scores do not authorize label or endpoint promotion.",
        "",
    ]
    (REPORTS / "s4g75_ngc2683_flare_closure_source_prototype.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    points, summary = build_prototype()
    points.to_csv(DATA / "s4g75_ngc2683_flare_closure_source_prototype_points.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc2683_flare_closure_source_prototype_summary.csv", index=False)
    write_report(points, summary)
    print(f"wrote {DATA / 's4g75_ngc2683_flare_closure_source_prototype_points.csv'}")
    print(f"wrote {DATA / 's4g75_ngc2683_flare_closure_source_prototype_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc2683_flare_closure_source_prototype.md'}")


if __name__ == "__main__":
    main()
