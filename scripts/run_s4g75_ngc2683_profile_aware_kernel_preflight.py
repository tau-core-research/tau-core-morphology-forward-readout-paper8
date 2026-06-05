#!/usr/bin/env python3
"""Run a profile-aware thick/flared kernel preflight for NGC2683.

This diagnostic compares the current scalar h/Rs thick/flared shell with a
source-native flare-profile shell for NGC2683.  It is not an accepted endpoint:
the profile-to-kernel rule is still under development and the post-22 kpc
source profile is not uniquely specified.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc2683_profile_aware_kernel_preflight_not_validation"
GALAXY = "NGC2683"
FAMILY = "K_thick_flared"

sys.path.insert(0, str(ROOT / "scripts"))
import run_s4g75_promoted_kernel_endpoint_stress_test as promoted  # noqa: E402
import run_source_native_readout_formula_endpoint as src  # noqa: E402


def rmse(sub: pd.DataFrame, pred_col: str) -> float:
    return float(((sub[pred_col] - sub["vobs"]).pow(2).mean()) ** 0.5)


def build_profile_points() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    points, _labels = src.load_points()
    base_points = promoted.apply_promoted_observables(points)
    scalar_kernel_points = src.add_bridge_formula_kernels(base_points)
    amplitudes = src.fit_amplitudes(scalar_kernel_points)
    scalar_scored = src.add_predictions(scalar_kernel_points, amplitudes)

    mapping = pd.read_csv(DATA / "s4g75_ngc2683_flare_profile_mapping_gate.csv")[
        ["radius_kpc", "flare_h_over_rs_profile", "mapping_status", "mapping_region"]
    ].rename(columns={"radius_kpc": "r"})

    profile_points = base_points.copy()
    profile_points = profile_points.merge(mapping, on="r", how="left", validate="many_to_one")
    mask = (profile_points["galaxy"] == GALAXY) & (
        profile_points["mapping_status"] == "PROFILE_MAPPED"
    )
    profile_points.loc[mask, "thickness_h_over_rs_proxy"] = profile_points.loc[
        mask, "flare_h_over_rs_profile"
    ]
    profile_kernel_points = src.add_bridge_formula_kernels(profile_points)
    profile_scored = src.add_predictions(profile_kernel_points, amplitudes)

    unclipped_points = base_points.copy()
    unclipped_points = unclipped_points.merge(mapping, on="r", how="left", validate="many_to_one")
    unclipped_kernel_points = src.add_bridge_formula_kernels(unclipped_points)
    mask = (unclipped_kernel_points["galaxy"] == GALAXY) & (
        unclipped_kernel_points["mapping_status"] == "PROFILE_MAPPED"
    )
    x = (
        unclipped_kernel_points.loc[mask, "r"]
        / unclipped_kernel_points.loc[mask, "scale_radius_proxy_kpc"]
    ).to_numpy()
    h_unclipped = unclipped_kernel_points.loc[mask, "flare_h_over_rs_profile"].to_numpy()
    r_s = unclipped_kernel_points.loc[mask, "scale_radius_proxy_kpc"].to_numpy()
    unclipped_kernel_points.loc[mask, f"kernel_{FAMILY}"] = (
        r_s * src.thick_damped_shape(x, h_unclipped)
    )
    unclipped_scored = src.add_predictions(unclipped_kernel_points, amplitudes)
    return scalar_scored, profile_scored, unclipped_scored, amplitudes


def build_preflight() -> tuple[pd.DataFrame, pd.DataFrame]:
    scalar_scored, profile_scored, unclipped_scored, amplitudes = build_profile_points()
    scalar_ngc = scalar_scored.loc[scalar_scored["galaxy"] == GALAXY].copy()
    profile_ngc = profile_scored.loc[profile_scored["galaxy"] == GALAXY].copy()
    unclipped_ngc = unclipped_scored.loc[unclipped_scored["galaxy"] == GALAXY].copy()

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
        profile_ngc[
            [
                "r",
                "flare_h_over_rs_profile",
                "mapping_status",
                "mapping_region",
                "thickness_h_over_rs_proxy",
                f"kernel_{FAMILY}",
                f"v_{FAMILY}",
            ]
        ].rename(
            columns={
                "thickness_h_over_rs_proxy": "profile_policy_h_over_rs",
                f"kernel_{FAMILY}": "profile_kernel_K_thick_flared",
                f"v_{FAMILY}": "profile_v_K_thick_flared",
            }
        ),
        on="r",
        how="left",
        validate="one_to_one",
    )
    compare = compare.merge(
        unclipped_ngc[
            [
                "r",
                f"kernel_{FAMILY}",
                f"v_{FAMILY}",
            ]
        ].rename(
            columns={
                f"kernel_{FAMILY}": "unclipped_profile_kernel_K_thick_flared",
                f"v_{FAMILY}": "unclipped_profile_v_K_thick_flared",
            }
        ),
        on="r",
        how="left",
        validate="one_to_one",
    )
    compare["profile_minus_scalar_kernel"] = (
        compare["profile_kernel_K_thick_flared"] - compare["scalar_kernel_K_thick_flared"]
    )
    compare["scalar_effective_h_over_rs_clipped"] = compare["scalar_h_over_rs"].clip(
        lower=0.05,
        upper=0.75,
    )
    compare["profile_effective_h_over_rs_clipped"] = compare["profile_policy_h_over_rs"].clip(
        lower=0.05,
        upper=0.75,
    )
    compare["profile_h_over_rs_exceeds_current_clip"] = compare[
        "profile_policy_h_over_rs"
    ] > 0.75
    compare["profile_minus_scalar_v"] = (
        compare["profile_v_K_thick_flared"] - compare["scalar_v_K_thick_flared"]
    )
    compare["unclipped_profile_minus_scalar_kernel"] = (
        compare["unclipped_profile_kernel_K_thick_flared"]
        - compare["scalar_kernel_K_thick_flared"]
    )
    compare["unclipped_profile_minus_scalar_v"] = (
        compare["unclipped_profile_v_K_thick_flared"]
        - compare["scalar_v_K_thick_flared"]
    )
    compare["claim_boundary"] = CLAIM_BOUNDARY
    compare["accepted_endpoint_ready"] = False
    compare["endpoint_scores_allowed"] = False
    compare["endpoint_scores_computed"] = True

    mapped = compare.loc[compare["mapping_status"] == "PROFILE_MAPPED"]
    rows = []
    for policy, sub in [
        ("mapped_only_source_profile_policy", mapped),
        ("hybrid_profile_mapped_scalar_unmapped_policy", compare),
    ]:
        rows.append(
            {
                "galaxy": GALAXY,
                "policy": policy,
                "n_points": int(len(sub)),
                "n_profile_mapped_points": int((sub["mapping_status"] == "PROFILE_MAPPED").sum()),
                "n_unmapped_points": int(
                    (sub["mapping_status"] == "MAPPING_REQUIRED_AFTER_22_KPC").sum()
                ),
                "beta_delta_v2_amplitude": float(
                    amplitudes.loc[
                        amplitudes["formula_family"] == FAMILY,
                        "beta_delta_v2_amplitude",
                    ].iloc[0]
                ),
                "scalar_rmse_K_thick_flared": rmse(sub, "scalar_v_K_thick_flared"),
                "profile_rmse_K_thick_flared": rmse(sub, "profile_v_K_thick_flared"),
                "unclipped_profile_rmse_K_thick_flared": rmse(
                    sub,
                    "unclipped_profile_v_K_thick_flared",
                ),
                "profile_minus_scalar_rmse": rmse(sub, "profile_v_K_thick_flared")
                - rmse(sub, "scalar_v_K_thick_flared"),
                "unclipped_profile_minus_scalar_rmse": rmse(
                    sub,
                    "unclipped_profile_v_K_thick_flared",
                )
                - rmse(sub, "scalar_v_K_thick_flared"),
                "n_profile_points_exceeding_current_clip": int(
                    sub["profile_h_over_rs_exceeds_current_clip"].sum()
                ),
                "scalar_rmse_tpg_v6": rmse(sub, "v_v6"),
                "scalar_rmse_mond": rmse(sub, "v_mond"),
                "accepted_endpoint_ready": False,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    summary = pd.DataFrame(rows)
    return compare, summary


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


def write_report(compare: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC2683 Profile-Aware Thick/Flared Kernel Preflight",
        "",
        "This diagnostic compares the current scalar h/Rs thick/flared shell with "
        "a source-native flare-profile shell for NGC2683. It is not accepted "
        "validation.",
        "",
        "## Verdict",
        "",
        markdown_table(summary),
        "",
        "A positive profile-minus-scalar RMSE means the current naive profile "
        "insertion worsens the stress score. That is a useful failure signal: "
        "the direct flare profile should feed a profile-aware readout kernel, "
        "not simply a pointwise scalar substitution.",
        "",
        "## Point-Level Comparison",
        "",
        markdown_table(
            compare[
                [
                    "r",
                    "mapping_status",
                    "scalar_h_over_rs",
                    "profile_policy_h_over_rs",
                    "profile_effective_h_over_rs_clipped",
                    "profile_h_over_rs_exceeds_current_clip",
                    "scalar_kernel_K_thick_flared",
                    "profile_kernel_K_thick_flared",
                    "unclipped_profile_kernel_K_thick_flared",
                    "scalar_v_K_thick_flared",
                    "profile_v_K_thick_flared",
                    "unclipped_profile_v_K_thick_flared",
                    "profile_minus_scalar_v",
                    "unclipped_profile_minus_scalar_v",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This preflight computes stress RMSEs for kernel development only. It does "
        "not create an accepted endpoint row and does not resolve the post-22 kpc "
        "source-profile ambiguity.",
        "",
    ]
    (REPORTS / "s4g75_ngc2683_profile_aware_kernel_preflight.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    compare, summary = build_preflight()
    compare.to_csv(DATA / "s4g75_ngc2683_profile_aware_kernel_preflight_points.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc2683_profile_aware_kernel_preflight_summary.csv", index=False)
    write_report(compare, summary)
    print(f"wrote {DATA / 's4g75_ngc2683_profile_aware_kernel_preflight_points.csv'}")
    print(f"wrote {DATA / 's4g75_ngc2683_profile_aware_kernel_preflight_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc2683_profile_aware_kernel_preflight.md'}")


if __name__ == "__main__":
    main()
