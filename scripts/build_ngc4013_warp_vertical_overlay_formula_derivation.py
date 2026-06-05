#!/usr/bin/env python3
"""Derive an NGC4013 warp/vertical-overlay formula shell.

This is a derivation/freeze-skeleton, not an endpoint score. The formula is
built from residual-blind source fields after the compact lane has been rejected:
warp onset, edge-disk vertical thickness, extended vertical component, and
rotational-lag context.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_warp_vertical_overlay_formula_derivation_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    source = pd.read_csv(DATA / "ngc4013_compact_overlay_source_summary.csv").iloc[0]
    preflight = pd.read_csv(DATA / "ngc4013_warp_overlay_preflight_summary.csv").iloc[0]

    r_warp = float(preflight["warp_onset_kpc"])
    h_over_rs = float(source["s4g_edge_disk_h_over_r"])
    z_ec_kpc = float(source["extended_component_scaleheight_kpc"])
    f_ec = float(source["extended_component_mass_fraction"])
    h_hi_central = float(preflight["central_hi_scaleheight_kpc"])
    rs_proxy = h_hi_central / float(preflight["central_h_over_rs_proxy"])

    # Dimensionless source-side overlay strength. This is not a fitted amplitude:
    # it is a conservative first-order projection/vertical-overlay coefficient
    # assembled from already acquired source observables. The 1/2 factor keeps
    # the first-order attenuation convention aligned with the NGC5907 projection
    # endpoint shell.
    gamma_z = 0.5 * h_over_rs
    gamma_ec = 0.5 * f_ec
    gamma_overlay_upper = min(0.95, gamma_z + gamma_ec)

    manifest = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "formula_id": "NGC4013_WARP_VERTICAL_OVERLAY_V1",
                "readout_subfamily": "K_warp_vertical_overlay_candidate",
                "carrier": "v_TPG",
                "solved_response_formula": (
                    "v_wvo^2(R)=v_TPG^2(R)*(1-Gamma_wvo*K_wvo(R))"
                ),
                "kernel_formula": (
                    "K_wvo(R)=W_warp(R;R_w,R_o)*[omega_z*K_z(R)+omega_EC*K_EC(R)+omega_lag*K_lag(R)]"
                ),
                "warp_window": "W_warp=smoothstep((R-R_w)/(R_o-R_w))",
                "vertical_kernel": "K_z(R)=1/(1+R/R_s)",
                "extended_component_kernel": "K_EC(R)=1/(1+R/z_EC)",
                "lag_kernel": "K_lag(R)=normalized lag-shallowing profile; source map still required",
                "sign_rule": "attenuation_not_added_gravity",
                "amplitude_rule": "Gamma_wvo <= 0.5*h_over_Rs + 0.5*f_EC until lag map is frozen",
                "r_warp_kpc": r_warp,
                "r_outer_kpc": "",
                "h_over_rs": h_over_rs,
                "z_ec_kpc": z_ec_kpc,
                "f_ec": f_ec,
                "rs_proxy_kpc": rs_proxy,
                "gamma_z": gamma_z,
                "gamma_ec": gamma_ec,
                "gamma_overlay_upper": gamma_overlay_upper,
                "uses_vobs_or_residual_in_derivation": False,
                "formula_frozen_for_endpoint": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    derivation_steps = pd.DataFrame(
        [
            {
                "step_id": "D1_COMPACT_REJECTION",
                "status": "DERIVED_FROM_SOURCE_AUDIT",
                "statement": "S4G has no bulge B component for NGC4013; compact endpoint is not source-supported.",
                "formula_consequence": "replace K_compact_finite by K_warp_vertical_overlay_candidate",
            },
            {
                "step_id": "D2_CARRIER_CHOICE",
                "status": "DEFINITION",
                "statement": "Use v_TPG as the already available solved-response carrier for overlay attenuation.",
                "formula_consequence": "v_wvo^2 = v_TPG^2(1 - overlay attenuation)",
            },
            {
                "step_id": "D3_SIGN_RULE",
                "status": "ASSUMPTION_WITH_SOURCE_MOTIVATION",
                "statement": "Edge-on warp/vertical/lag overlay is treated as apparent overread/projection contamination.",
                "formula_consequence": "attenuation sign, not added-gravity sign",
            },
            {
                "step_id": "D4_WARP_WINDOW",
                "status": "FORMULA_CONDITIONAL",
                "statement": "The source gives warp onset near 10 kpc but not a fully accepted outer window.",
                "formula_consequence": "W_warp=smoothstep((R-R_w)/(R_o-R_w)); R_o remains a freeze blocker",
            },
            {
                "step_id": "D5_VERTICAL_OVERLAY_STRENGTH",
                "status": "SOURCE_DERIVED_BOUND",
                "statement": "S4G edge-disk h/R and Comeron extended-component mass fraction set a conservative first-order bound.",
                "formula_consequence": "Gamma_wvo <= 0.5*h/Rs + 0.5*f_EC",
            },
            {
                "step_id": "D6_LAG_KERNEL",
                "status": "BLOCKED_SOURCE_MAP_REQUIRED",
                "statement": "Rotational lag context is present, but a normalized radial lag map is not yet frozen.",
                "formula_consequence": "K_lag is symbolic until lag-to-kernel mapping is accepted",
            },
            {
                "step_id": "D7_ENDPOINT_STATUS",
                "status": "ENDPOINT_BLOCKED",
                "statement": "No endpoint score is allowed until R_o and K_lag are frozen without vobs.",
                "formula_consequence": "formula shell derived; endpoint formula not frozen",
            },
        ]
    )
    derivation_steps["galaxy"] = "NGC4013"
    derivation_steps["endpoint_scores_allowed"] = False
    derivation_steps["claim_boundary"] = CLAIM_BOUNDARY
    derivation_steps = derivation_steps[
        [
            "galaxy",
            "step_id",
            "status",
            "statement",
            "formula_consequence",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    blockers = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "blocker_id": "B1_OUTER_WARP_WINDOW",
                "required_input": "accepted outer warp/projection support radius R_o",
                "why_required": "without R_o, W_warp cannot be endpoint-frozen",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "blocker_id": "B2_LAG_TO_KERNEL_MAP",
                "required_input": "accepted normalized radial lag-shallowing profile K_lag(R)",
                "why_required": "lag context cannot become a numerical kernel without a source-side map",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "blocker_id": "B3_WEIGHT_RULE",
                "required_input": "residual-blind omega_z, omega_EC, omega_lag weighting rule",
                "why_required": "component weights cannot be selected by endpoint residuals",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "formula_id": "NGC4013_WARP_VERTICAL_OVERLAY_V1",
                "r_warp_kpc": r_warp,
                "h_over_rs": h_over_rs,
                "z_ec_kpc": z_ec_kpc,
                "f_ec": f_ec,
                "gamma_overlay_upper": gamma_overlay_upper,
                "n_derivation_steps": len(derivation_steps),
                "n_endpoint_blockers": len(blockers),
                "derivation_status": "FORMULA_SHELL_DERIVED_ENDPOINT_FREEZE_BLOCKED",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ngc4013_warp_vertical_overlay_formula_manifest.csv", index=False)
    derivation_steps.to_csv(
        DATA / "ngc4013_warp_vertical_overlay_formula_derivation_steps.csv", index=False
    )
    blockers.to_csv(DATA / "ngc4013_warp_vertical_overlay_formula_blockers.csv", index=False)
    summary.to_csv(DATA / "ngc4013_warp_vertical_overlay_formula_summary.csv", index=False)

    report = [
        "# NGC4013 Warp/Vertical-Overlay Formula Derivation",
        "",
        "This report derives a source-side formula shell for NGC4013 after the",
        "compact endpoint lane is rejected. It does not score the rotation curve.",
        "",
        "## Formula",
        "",
        "The derived shell is",
        "",
        "`v_wvo^2(R)=v_TPG^2(R)*(1-Gamma_wvo*K_wvo(R))`,",
        "",
        "with",
        "",
        "`K_wvo(R)=W_warp(R;R_w,R_o)*[omega_z*K_z(R)+omega_EC*K_EC(R)+omega_lag*K_lag(R)]`.",
        "",
        "The current source-derived upper coefficient is",
        f"`Gamma_wvo <= {gamma_overlay_upper:.6g}`.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Derivation Steps",
        "",
        markdown_table(derivation_steps),
        "",
        "## Endpoint Blockers",
        "",
        markdown_table(blockers),
        "",
        "## Claim Boundary",
        "",
        "This is a formula derivation shell. The endpoint remains blocked until the",
        "outer warp window, lag-to-kernel map, and component weighting rule are",
        "frozen without using observed rotation residuals.",
        "",
    ]
    (REPORTS / "ngc4013_warp_vertical_overlay_formula_derivation.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
