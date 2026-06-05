#!/usr/bin/env python3
"""Convert an accepted NGC4088 digitization response into an x_w audit.

This script is the first machine-readable conversion gate from the channel-map
digitization response into the dimensionless warp-onset control
`x_w = R_warp / R_HI`. It remains blocked until the response template is fully
filled and passes the frozen protocol checks.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc4088_xw_conversion_audit_not_endpoint"
PENDING = "DIGITIZATION_RESPONSE_PENDING"


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


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    response = pd.read_csv(DATA / "s4g75_ngc4088_channel_map_digitization_response_template.csv")
    validation = pd.read_csv(DATA / "s4g75_ngc4088_channel_map_digitization_response_validation.csv")
    gate = pd.read_csv(DATA / "s4g75_ngc4088_warp_asymmetry_extraction_gate.csv").iloc[0]
    prekernel = pd.read_csv(DATA / "s4g75_ngc4088_warp_prekernel_observables.csv")

    row = response.iloc[0]
    validation_row = validation.iloc[0]
    hi_diameter_arcmin = float(gate["source_native_hi_diameter_arcmin"])
    hi_radius_arcmin = hi_diameter_arcmin / 2.0
    r_hi_kpc = float(
        prekernel.loc[
            prekernel["observable"] == "R_HI_from_WHISP_diameter_kpc", "value"
        ].iloc[0]
    )

    required_fields = [
        "inner_disk_axis_pa_deg",
        "outer_ridge_axis_side_a_pa_deg",
        "outer_ridge_axis_side_b_pa_deg",
        "onset_radius_side_a_arcmin",
        "onset_radius_side_b_arcmin",
        "side_combination_rule_applied",
        "xw_combined_arcmin",
        "uncertainty_arcmin",
        "crosscheck_page77_consistency",
    ]
    missing = [field for field in required_fields if str(row[field]).strip() == PENDING]
    ready = (
        validation_row["validation_status"] == "READY_FOR_XW_CONVERSION_AUDIT"
        and not missing
    )

    if ready:
        onset_arcmin = float(row["xw_combined_arcmin"])
        uncertainty_arcmin = float(row["uncertainty_arcmin"])
        x_w = onset_arcmin / hi_radius_arcmin
        uncertainty_x_w = uncertainty_arcmin / hi_radius_arcmin
        onset_kpc = x_w * r_hi_kpc
        status = "XW_READY_FOR_MAPPING_RULE"
        dimension_ok = 0.0 < x_w < 1.0
    else:
        onset_arcmin = ""
        uncertainty_arcmin = ""
        x_w = ""
        uncertainty_x_w = ""
        onset_kpc = ""
        status = "BLOCKED_DIGITIZATION_RESPONSE_PENDING"
        dimension_ok = False

    audit = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "conversion_status": status,
                "digitization_validation_status": validation_row["validation_status"],
                "side_combination_rule_applied": row["side_combination_rule_applied"],
                "hi_diameter_arcmin": hi_diameter_arcmin,
                "hi_radius_arcmin": hi_radius_arcmin,
                "r_hi_kpc": r_hi_kpc,
                "combined_onset_arcmin": onset_arcmin,
                "combined_onset_kpc": onset_kpc,
                "x_warp_onset": x_w,
                "x_warp_uncertainty": uncertainty_x_w,
                "dimension_check_passed": dimension_ok,
                "crosscheck_page77_consistency": row["crosscheck_page77_consistency"],
                "accepted_for_mapping_rule": bool(ready and dimension_ok),
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "xw_conversion_decision": status,
                "n_missing_required_fields": len(missing),
                "accepted_for_mapping_rule": bool(ready and dimension_ok),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return audit, summary


def write_report(audit: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# NGC4088 x_w Conversion Audit",
        "",
        "This report is the first machine-readable conversion gate from the frozen",
        "channel-map digitization response into the dimensionless warp-onset",
        "control `x_w = R_warp / R_HI`.",
        "",
        "## Verdict",
        "",
        "The current package is correctly blocked until the digitization response",
        "template is filled and validated. No `x_w` value is accepted yet.",
        "",
        "## Audit",
        "",
        markdown_table(audit),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "A passing conversion audit would only make `x_w` available as an input to",
        "the residual-blind mapping-rule lane. It would still not authorize",
        "endpoint scoring or a validation claim.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_xw_conversion_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    audit, summary = build_audit()
    audit.to_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_xw_conversion_summary.csv", index=False)
    write_report(audit, summary)
    print("PAPER8_NGC4088_XW_CONVERSION_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
