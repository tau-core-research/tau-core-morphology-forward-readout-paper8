#!/usr/bin/env python3
"""Build an NGC4088-specific filled warp closure-source mapping artifact.

This script injects the residual-blind `x_w` value from the channel-map
digitization/x_w conversion lane into the NGC4088 closure-source mapping shell.
It remains pre-endpoint because the kernel-to-velocity normalization and full
readout law are still open.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc4088_filled_warp_closure_mapping_not_endpoint"


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


def ramp_basis(x: float, x_warp: float, power: float) -> float:
    if x <= x_warp + 1.0e-12:
        return 0.0
    if x_warp >= 1.0:
        return 0.0
    return ((x - x_warp) / (1.0 - x_warp)) ** power


def build_mapping() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    prekernel = pd.read_csv(DATA / "s4g75_ngc4088_warp_prekernel_observables.csv")
    xw_audit = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    values = dict(zip(prekernel["observable"], prekernel["value"]))
    q_warp = float(values["qualitative_warp_asymmetry_score"])
    x_w = float(xw_audit["x_warp_onset"])
    x_w_unc = float(xw_audit["x_warp_uncertainty"])
    onset_kpc = float(xw_audit["combined_onset_kpc"])

    powers = [1.0, 2.0]
    x_values = [0.0, 0.1, 0.2, x_w, 0.4, 0.6, 0.8, 1.0]

    rule = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "mapping_name": "filled_dimensionless_outer_warp_asymmetry_ramp",
                "dimensionless_radius": "x := R / R_HI",
                "basis_formula": "C_warp(x; x_w, p) = q_warp * max(0, (x - x_w)/(1 - x_w))^p",
                "known_source_strength_q_warp": q_warp,
                "filled_x_warp_onset": x_w,
                "filled_x_warp_uncertainty": x_w_unc,
                "filled_onset_kpc": onset_kpc,
                "filled_onset_source": "channel-map digitization response + x_w conversion audit",
                "allowed_turn_on_powers": "1.0;2.0",
                "mapping_status": "FILLED_SOURCE_BASIS_PROFILE_NORMALIZATION_OPEN",
                "accepted_for_mapping_rule": bool(xw_audit["accepted_for_mapping_rule"]),
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    rows = []
    for power in powers:
        for x in x_values:
            rows.append(
                {
                    "galaxy": "NGC4088",
                    "x_R_over_RHI": x,
                    "filled_x_warp_onset": x_w,
                    "x_warp_uncertainty": x_w_unc,
                    "turn_on_power_control": power,
                    "q_warp": q_warp,
                    "filled_basis_value": q_warp * ramp_basis(x, x_w, power),
                    "profile_status": "FILLED_SOURCE_BASIS_NOT_ENDPOINT",
                    "accepted_for_mapping_rule": bool(xw_audit["accepted_for_mapping_rule"]),
                    "endpoint_scores_allowed": False,
                    "endpoint_scores_computed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    profile = pd.DataFrame(rows)

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "filled_x_warp_onset": x_w,
                "filled_x_warp_uncertainty": x_w_unc,
                "filled_onset_kpc": onset_kpc,
                "n_profile_rows": len(profile),
                "mapping_status": "FILLED_SOURCE_BASIS_PROFILE_NORMALIZATION_OPEN",
                "accepted_for_mapping_rule": bool(xw_audit["accepted_for_mapping_rule"]),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return rule, profile, summary


def write_report(rule: pd.DataFrame, profile: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# NGC4088 Filled Warp Closure Mapping",
        "",
        "This report injects the residual-blind NGC4088 `x_w` estimate into the",
        "warp closure-source mapping shell. It is still not an endpoint kernel or",
        "velocity prediction.",
        "",
        "## Verdict",
        "",
        "NGC4088 now has a filled source-side onset control for the closure-source",
        "lane. The remaining blocker is not the onset any more; it is the",
        "kernel-to-velocity normalization and final readout law.",
        "",
        "## Filled Mapping Rule",
        "",
        markdown_table(rule),
        "",
        "## Filled Profile Grid",
        "",
        markdown_table(profile),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "This artifact only fills the source-side onset control in the mapping",
        "shell. It does not authorize endpoint scoring, baseline comparison, or a",
        "matched-family validation claim.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_filled_warp_closure_mapping.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    rule, profile, summary = build_mapping()
    rule.to_csv(DATA / "s4g75_ngc4088_filled_warp_closure_mapping.csv", index=False)
    profile.to_csv(DATA / "s4g75_ngc4088_filled_warp_closure_profile.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_filled_warp_closure_summary.csv", index=False)
    write_report(rule, profile, summary)
    print("PAPER8_NGC4088_FILLED_WARP_CLOSURE_MAPPING_COMPLETE")


if __name__ == "__main__":
    main()
