#!/usr/bin/env python3
"""Build a residual-blind NGC4088 warp/asymmetry closure-source mapping shell.

The mapping is deliberately pre-endpoint.  It defines a dimensionless radial
closure-source basis from source-native warp/asymmetry observables, but it does
not infer the warp-onset radius or amplitude from rotation residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc4088_warp_closure_mapping_rule_not_endpoint"


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


def ramp_basis(x: float, x_warp: float, power: float) -> float:
    if x <= x_warp:
        return 0.0
    if x_warp >= 1.0:
        return 0.0
    return ((x - x_warp) / (1.0 - x_warp)) ** power


def build_mapping() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    prekernel = pd.read_csv(DATA / "s4g75_ngc4088_warp_prekernel_observables.csv")
    values = dict(zip(prekernel["observable"], prekernel["value"]))
    q_warp = float(values["qualitative_warp_asymmetry_score"])
    r_hi_over_rdisk = float(values["R_HI_over_SPARC_Rdisk"])
    r_hi_over_rs4g = float(values["R_HI_over_S4G_scale_radius"])
    rule = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "mapping_name": "dimensionless_outer_warp_asymmetry_ramp",
                "dimensionless_radius": "x := R / R_HI",
                "basis_formula": "C_warp(x; x_w, p) = q_warp * max(0, (x - x_w)/(1 - x_w))^p",
                "source_strength": "q_warp := qualitative_warp_asymmetry_score",
                "known_source_strength": q_warp,
                "known_scale_R_HI_over_Rdisk": r_hi_over_rdisk,
                "known_scale_R_HI_over_Rs4g": r_hi_over_rs4g,
                "free_source_required": "x_w := warp_onset_radius / R_HI",
                "shape_control": "p >= 1 controls how gradually the source turns on",
                "dimensional_status": "DIMENSIONLESS_BASIS_ONLY",
                "known_limit_inner": "C_warp = 0 for x <= x_w",
                "known_limit_outer": "C_warp = q_warp at x = 1 when q_warp is fixed",
                "missing_for_endpoint": (
                    "source-native x_w; radial PA/theta profile; amplitude/readout "
                    "normalization; residual-blind kernel-to-velocity map"
                ),
                "mapping_status": "FORMULA_DEVELOPMENT_SHELL_PROFILE_ONSET_BLOCKED",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    grid_rows = []
    x_values = [0.0, 0.25, 0.5, 0.75, 1.0]
    onset_grid = [0.5, 0.7, 0.85]
    powers = [1.0, 2.0]
    for x_warp in onset_grid:
        for power in powers:
            for x in x_values:
                grid_rows.append(
                    {
                        "galaxy": "NGC4088",
                        "x_R_over_RHI": x,
                        "x_warp_onset_control": x_warp,
                        "turn_on_power_control": power,
                        "q_warp": q_warp,
                        "basis_value": q_warp * ramp_basis(x, x_warp, power),
                        "grid_status": "SENSITIVITY_BASIS_NOT_ENDPOINT",
                        "uses_vobs_or_residual": False,
                        "endpoint_scores_allowed": False,
                        "endpoint_scores_computed": False,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    grid = pd.DataFrame(grid_rows)
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "mapping_status": "FORMULA_DEVELOPMENT_SHELL_PROFILE_ONSET_BLOCKED",
                "n_basis_grid_rows": len(grid),
                "known_source_strength_q_warp": q_warp,
                "known_scale_R_HI_over_Rdisk": r_hi_over_rdisk,
                "known_scale_R_HI_over_Rs4g": r_hi_over_rs4g,
                "required_source_native_onset": "warp_onset_radius_or_PA_profile",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return rule, grid, summary


def write_report(rule: pd.DataFrame, grid: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Warp Closure Mapping Rule",
        "",
        "This report defines a residual-blind mapping shell from NGC4088 "
        "warp/asymmetry evidence into a dimensionless closure-source basis. It "
        "does not create an endpoint kernel.",
        "",
        "## Verdict",
        "",
        "The bridge can now express the NGC4088 warp/asymmetry lane as a concrete "
        "dimensionless source basis, but the onset and radial profile are still "
        "source-missing. The formula is therefore a development shell, not a "
        "validated 4D readout.",
        "",
        "## Mapping Rule",
        "",
        markdown_table(
            rule[
                [
                    "mapping_name",
                    "dimensionless_radius",
                    "basis_formula",
                    "known_source_strength",
                    "free_source_required",
                    "dimensional_status",
                    "mapping_status",
                    "endpoint_scores_allowed",
                ]
            ]
        ),
        "",
        "## Sensitivity Basis Grid",
        "",
        markdown_table(grid.head(18)),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "The onset controls in the grid are sensitivity controls, not fitted "
        "parameters and not accepted source measurements. Endpoint use requires "
        "a source-native warp-onset or PA/theta profile and a fixed readout map.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_warp_closure_mapping_rule.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    rule, grid, summary = build_mapping()
    rule.to_csv(DATA / "s4g75_ngc4088_warp_closure_mapping_rule.csv", index=False)
    grid.to_csv(DATA / "s4g75_ngc4088_warp_closure_basis_grid.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_warp_closure_mapping_summary.csv", index=False)
    write_report(rule, grid, summary)
    print(f"wrote {DATA / 's4g75_ngc4088_warp_closure_mapping_rule.csv'}")
    print(f"wrote {DATA / 's4g75_ngc4088_warp_closure_basis_grid.csv'}")
    print(f"wrote {DATA / 's4g75_ngc4088_warp_closure_mapping_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_ngc4088_warp_closure_mapping_rule.md'}")


if __name__ == "__main__":
    main()
