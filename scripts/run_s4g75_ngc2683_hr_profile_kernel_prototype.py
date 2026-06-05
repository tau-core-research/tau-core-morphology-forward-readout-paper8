#!/usr/bin/env python3
"""Prototype an H(R)-aware thick/flared readout kernel for NGC2683.

The current executable thick/flared shell treats thickness as a local scalar
damping parameter.  This prototype keeps the same bridge-amplitude policy but
replaces local scalar damping with a residual-blind radial flare-profile
operator.  It is a kernel-development diagnostic, not an accepted endpoint.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
TPG_RESULTS = Path("/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1")
CLAIM_BOUNDARY = "s4g75_ngc2683_hr_profile_kernel_prototype_not_validation"
GALAXY = "NGC2683"
FAMILY = "K_thick_flared"

R_START_KPC = 9.0
H_START_KPC = 0.5
R_MAX_KPC = 15.0
H_MAX_KPC = 4.0
R_SAT_END_KPC = 22.0

POST22_POLICIES = [
    "post22_hold_plateau_upper",
    "post22_linear_taper_to_inner_height",
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
        raise ValueError(f"unknown policy: {policy}")
    return height


def nonlocal_h_over_rs(
    radii: np.ndarray,
    scale_radius: float,
    policy: str,
    locality_width_kpc: float,
) -> np.ndarray:
    r_outer = float(np.max(radii))
    grid = np.linspace(0.0, r_outer, 512)
    heights = source_flare_height(grid, policy, r_outer)
    source_weight = np.exp(-grid / max(scale_radius, 1.0e-6))
    values = []
    for radius in radii:
        locality = np.exp(-0.5 * ((grid - radius) / max(locality_width_kpc, 1.0e-6)) ** 2)
        weight = source_weight * locality
        den = INTEGRATE(weight, grid)
        mean_height = float(INTEGRATE(weight * heights, grid) / den) if den > 0 else H_START_KPC
        values.append(mean_height / scale_radius)
    return np.asarray(values, dtype=float)


def build_profile_kernel_points() -> tuple[pd.DataFrame, pd.DataFrame]:
    points, _labels = src.load_points()
    base_points = promoted.apply_promoted_observables(points)
    scalar_kernel_points = src.add_bridge_formula_kernels(base_points)
    amplitudes = src.fit_amplitudes(scalar_kernel_points)
    scalar_scored = src.add_predictions(scalar_kernel_points, amplitudes)
    scalar_ngc = scalar_scored.loc[scalar_scored["galaxy"] == GALAXY].copy()

    rows = []
    summaries = []
    beta = float(
        amplitudes.loc[
            amplitudes["formula_family"] == FAMILY,
            "beta_delta_v2_amplitude",
        ].iloc[0]
    )
    scale_radius = float(scalar_ngc["scale_radius_proxy_kpc"].iloc[0])
    radii = scalar_ngc["r"].to_numpy()
    # One source-native locality choice: the S4G/SPARC disk scale. This is not
    # fit to residuals and is kept fixed for the prototype.
    locality_width = scale_radius

    for policy in POST22_POLICIES:
        prototype = base_points.copy()
        mask = prototype["galaxy"] == GALAXY
        h_profile = nonlocal_h_over_rs(
            radii,
            scale_radius=scale_radius,
            policy=policy,
            locality_width_kpc=locality_width,
        )
        prototype.loc[mask, "thickness_h_over_rs_proxy"] = h_profile
        prototype_kernel_points = src.add_bridge_formula_kernels(prototype)
        x = (
            prototype_kernel_points.loc[mask, "r"]
            / prototype_kernel_points.loc[mask, "scale_radius_proxy_kpc"]
        ).to_numpy()
        r_s = prototype_kernel_points.loc[mask, "scale_radius_proxy_kpc"].to_numpy()
        prototype_kernel_points.loc[mask, f"kernel_{FAMILY}"] = (
            r_s * src.thick_damped_shape(x, h_profile)
        )
        scored = src.add_predictions(prototype_kernel_points, amplitudes)
        scored_ngc = scored.loc[scored["galaxy"] == GALAXY].copy()
        compare = scalar_ngc[
            [
                "galaxy",
                "r",
                "vobs",
                "v_v6",
                "v_mond",
                "thickness_h_over_rs_proxy",
                f"kernel_{FAMILY}",
                f"v_{FAMILY}",
            ]
        ].rename(
            columns={
                "thickness_h_over_rs_proxy": "scalar_h_over_rs",
                f"kernel_{FAMILY}": "scalar_kernel_K_thick_flared",
                f"v_{FAMILY}": "scalar_v_K_thick_flared",
            }
        )
        compare = compare.merge(
            scored_ngc[
                [
                    "r",
                    "thickness_h_over_rs_proxy",
                    f"kernel_{FAMILY}",
                    f"v_{FAMILY}",
                ]
            ].rename(
                columns={
                    "thickness_h_over_rs_proxy": "hr_profile_effective_h_over_rs",
                    f"kernel_{FAMILY}": "hr_profile_kernel_K_thick_flared",
                    f"v_{FAMILY}": "hr_profile_v_K_thick_flared",
                }
            ),
            on="r",
            how="left",
            validate="one_to_one",
        )
        compare["post22_policy"] = policy
        compare["locality_width_kpc"] = locality_width
        compare["hr_profile_minus_scalar_kernel"] = (
            compare["hr_profile_kernel_K_thick_flared"]
            - compare["scalar_kernel_K_thick_flared"]
        )
        compare["hr_profile_minus_scalar_v"] = (
            compare["hr_profile_v_K_thick_flared"]
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
                "post22_policy": policy,
                "n_points": int(len(compare)),
                "locality_width_kpc": locality_width,
                "beta_delta_v2_amplitude": beta,
                "scalar_rmse_K_thick_flared": rmse(compare, "scalar_v_K_thick_flared"),
                "hr_profile_rmse_K_thick_flared": rmse(compare, "hr_profile_v_K_thick_flared"),
                "hr_profile_minus_scalar_rmse": rmse(compare, "hr_profile_v_K_thick_flared")
                - rmse(compare, "scalar_v_K_thick_flared"),
                "rmse_tpg_v6": rmse(compare, "v_v6"),
                "rmse_mond": rmse(compare, "v_mond"),
                "h_over_rs_min": float(np.min(h_profile)),
                "h_over_rs_median": float(np.median(h_profile)),
                "h_over_rs_max": float(np.max(h_profile)),
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
        "# NGC2683 H(R)-Aware Thick/Flared Kernel Prototype",
        "",
        "This diagnostic replaces local scalar thickness with a residual-blind "
        "nonlocal radial flare-profile operator. It is not accepted validation.",
        "",
        "## Prototype Rule",
        "",
        "For each radius R, the effective h/Rs is computed as a source-weighted "
        "local average of H(R') over the NGC2683 flare profile, with locality "
        "width fixed to the S4G/SPARC disk scale. Two post-22 kpc closure "
        "policies bracket the source ambiguity.",
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
                    "r",
                    "scalar_h_over_rs",
                    "hr_profile_effective_h_over_rs",
                    "scalar_kernel_K_thick_flared",
                    "hr_profile_kernel_K_thick_flared",
                    "scalar_v_K_thick_flared",
                    "hr_profile_v_K_thick_flared",
                    "hr_profile_minus_scalar_v",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This is a profile-kernel development diagnostic. The post-22 kpc closure "
        "policies are explicit prototype brackets, not source-validated laws, and "
        "the stress scores do not authorize endpoint promotion.",
        "",
    ]
    (REPORTS / "s4g75_ngc2683_hr_profile_kernel_prototype.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    points, summary = build_profile_kernel_points()
    points.to_csv(DATA / "s4g75_ngc2683_hr_profile_kernel_prototype_points.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc2683_hr_profile_kernel_prototype_summary.csv", index=False)
    write_report(points, summary)
    print(f"wrote {DATA / 's4g75_ngc2683_hr_profile_kernel_prototype_points.csv'}")
    print(f"wrote {DATA / 's4g75_ngc2683_hr_profile_kernel_prototype_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc2683_hr_profile_kernel_prototype.md'}")


if __name__ == "__main__":
    main()
