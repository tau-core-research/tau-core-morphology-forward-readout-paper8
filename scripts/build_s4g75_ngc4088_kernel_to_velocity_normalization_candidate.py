#!/usr/bin/env python3
"""Build an NGC4088-specific kernel-to-velocity normalization candidate.

This is a source-side/theory-conditional bridge artifact: it combines the
filled NGC4088 warp closure-source basis with a dimensionally explicit
delta-v-squared normalization candidate. It does not compare against Vobs,
does not fit amplitudes, and does not authorize endpoint scoring.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint"


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
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def build_candidate() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    filled = pd.read_csv(DATA / "s4g75_ngc4088_filled_warp_closure_profile.csv")
    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    prekernel = pd.read_csv(DATA / "s4g75_ngc4088_warp_prekernel_observables.csv")
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")

    values = dict(zip(prekernel["observable"], prekernel["value"]))
    sparc_row = sparc.loc[sparc["Galaxy"] == "NGC4088"].iloc[0]
    r_hi_kpc = float(values["R_HI_from_WHISP_diameter_kpc"])
    rdisk_kpc = float(sparc_row["Rdisk_kpc"])
    q_warp = float(values["qualitative_warp_asymmetry_score"])
    vflat = float(sparc_row["Vflat_kms"])
    vflat2 = vflat**2
    closure_fraction = float(xw["x_warp_onset"])
    onset_kpc = float(xw["combined_onset_kpc"])

    constants = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "constant_name": "sigma_warp_orientation",
                "constant_value": 1.0,
                "unit": "dimensionless",
                "role": "positive closure-source orientation",
                "proof_status": "THEORY_CONDITIONAL",
                "rationale": "warp/asymmetry closure-source lane is treated as a positive outer residual readout channel",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4088",
                "constant_name": "q_warp",
                "constant_value": q_warp,
                "unit": "dimensionless",
                "role": "source-side warp strength",
                "proof_status": "SOURCE_NATIVE_QUALITATIVE_GATE",
                "rationale": "qualitative source strength imported from the NGC4088 warp/asymmetry extraction gate",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4088",
                "constant_name": "c_warp_candidate",
                "constant_value": closure_fraction,
                "unit": "dimensionless",
                "role": "source-normalization candidate",
                "proof_status": "XW_FILLED_SOURCE_FRACTION",
                "rationale": "first compact normalization candidate uses the filled x_w fraction as a residual-blind onset/closure scale",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4088",
                "constant_name": "velocity_scale_candidate",
                "constant_value": vflat2,
                "unit": "km2_s2",
                "role": "dimensionful delta-v-squared scale",
                "proof_status": "SOURCE_CATALOG_SCALE_CANDIDATE",
                "rationale": "uses catalog flat-speed squared as a simple source-side scale carrier for candidate normalization only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4088",
                "constant_name": "onset_over_rdisk",
                "constant_value": onset_kpc / rdisk_kpc,
                "unit": "dimensionless",
                "role": "secondary scale check",
                "proof_status": "DERIVED_FROM_FILLED_ONSET",
                "rationale": "tracks whether the filled onset sits in the outer disk relative to SPARC Rdisk",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    profile_rows = []
    for power in sorted(filled["turn_on_power_control"].unique()):
        sub = filled.loc[filled["turn_on_power_control"] == power].copy()
        sub["normalization_prefactor_km2_s2"] = q_warp * closure_fraction * vflat2
        sub["delta_v2_warp_candidate"] = (
            sub["normalization_prefactor_km2_s2"] * sub["filled_basis_value"]
        )
        sub["radius_kpc_candidate"] = sub["x_R_over_RHI"] * r_hi_kpc
        sub["normalization_status"] = "THEORY_CONDITIONAL_FILLED_SOURCE_RULE"
        sub["accepted_for_endpoint"] = False
        sub["claim_boundary"] = CLAIM_BOUNDARY
        profile_rows.append(
            sub[
                [
                    "galaxy",
                    "x_R_over_RHI",
                    "radius_kpc_candidate",
                    "filled_x_warp_onset",
                    "x_warp_uncertainty",
                    "turn_on_power_control",
                    "filled_basis_value",
                    "normalization_prefactor_km2_s2",
                    "delta_v2_warp_candidate",
                    "normalization_status",
                    "accepted_for_endpoint",
                    "claim_boundary",
                ]
            ]
        )
    profile = pd.concat(profile_rows, ignore_index=True)

    summary = (
        profile.groupby("turn_on_power_control", as_index=False)
        .agg(
            n_profile_rows=("x_R_over_RHI", "count"),
            max_delta_v2_candidate=("delta_v2_warp_candidate", "max"),
            median_delta_v2_candidate=("delta_v2_warp_candidate", "median"),
        )
        .sort_values("turn_on_power_control")
    )
    summary["galaxy"] = "NGC4088"
    summary["filled_x_warp_onset"] = float(xw["x_warp_onset"])
    summary["r_hi_kpc"] = r_hi_kpc
    summary["vflat_km_s"] = vflat
    summary["normalization_status"] = "THEORY_CONDITIONAL_FILLED_SOURCE_RULE"
    summary["accepted_for_endpoint"] = False
    summary["claim_boundary"] = CLAIM_BOUNDARY
    summary = summary[
        [
            "galaxy",
            "turn_on_power_control",
            "n_profile_rows",
            "filled_x_warp_onset",
            "r_hi_kpc",
            "vflat_km_s",
            "max_delta_v2_candidate",
            "median_delta_v2_candidate",
            "normalization_status",
            "accepted_for_endpoint",
            "claim_boundary",
        ]
    ]

    return constants, profile, summary


def write_report(constants: pd.DataFrame, profile: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# NGC4088 Kernel-to-Velocity Normalization Candidate",
        "",
        "This report is the first NGC4088-specific candidate bridge from the",
        "filled closure-source basis to a delta-v-squared readout scale. It is not",
        "an endpoint score, fit, or validation result.",
        "",
        "## Verdict",
        "",
        "NGC4088 now has a theory-conditional kernel-to-velocity normalization",
        "candidate built on the filled source-side onset control. The remaining",
        "open issue is whether this normalization law is the right physical",
        "readout law, not whether a residual-blind onset exists.",
        "",
        "## Constants",
        "",
        markdown_table(constants),
        "",
        "## Candidate Profile",
        "",
        markdown_table(profile),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "This candidate is dimensionally explicit and source-filled, but it remains",
        "theory-conditional. It does not compare against observed velocity",
        "endpoints and does not authorize matched-family or baseline claims.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_kernel_to_velocity_normalization_candidate.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    constants, profile, summary = build_candidate()
    constants.to_csv(
        DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_constants.csv",
        index=False,
    )
    profile.to_csv(
        DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_profile.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_summary.csv",
        index=False,
    )
    write_report(constants, profile, summary)
    print("PAPER8_NGC4088_KERNEL_TO_VELOCITY_NORMALIZATION_CANDIDATE_COMPLETE")


if __name__ == "__main__":
    main()
