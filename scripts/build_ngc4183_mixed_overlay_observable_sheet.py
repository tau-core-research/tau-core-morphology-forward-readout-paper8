#!/usr/bin/env python3
"""Build a residual-blind NGC4183 mixed-overlay observable sheet.

The sheet promotes reviewed source-native geometry fields into dimensionless
observable candidates for a later formula-freeze gate.  It still does not choose
or score an endpoint formula.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_mixed_overlay_observable_sheet_not_endpoint"
GALAXY = "NGC4183"


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


def arcmin_to_kpc(theta_arcmin: float, distance_mpc: float) -> float:
    return theta_arcmin * distance_mpc * 1000.0 * math.pi / (180.0 * 60.0)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    sparc_row = sparc.loc[sparc["Galaxy"].eq(GALAXY)].iloc[0]
    audit_summary = pd.read_csv(DATA / "ngc4183_mixed_overlay_source_audit_summary.csv").iloc[0]
    audit_fields = pd.read_csv(DATA / "ngc4183_mixed_overlay_source_audit_fields.csv")

    distance_mpc = float(sparc_row["D_Mpc"])
    rdisk_kpc = float(sparc_row["Rdisk_kpc"])
    rhi_sparc_kpc = float(sparc_row["RHI_kpc"])
    inc_sparc_deg = float(sparc_row["Inc_deg"])
    hi_diameter_arcmin = 6.1
    hi_inclination_deg = 83.0
    hi_position_angle_deg = 347.0
    rhi_source_kpc = arcmin_to_kpc(hi_diameter_arcmin, distance_mpc) / 2.0
    rhi_relative_difference = abs(rhi_source_kpc - rhi_sparc_kpc) / rhi_sparc_kpc

    p_edge = math.sin(math.radians(hi_inclination_deg)) ** 2
    x_scale = rdisk_kpc / rhi_source_kpc
    x_hi_extent = rhi_source_kpc / rdisk_kpc

    observables = pd.DataFrame(
        [
            {
                "observable_id": "R_HI_source_native_kpc",
                "value": rhi_source_kpc,
                "unit": "kpc",
                "source_basis": "HI diameter 6.1 arcmin at SPARC D=18.0 Mpc",
                "source_id": "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "status": "ACCEPTED_NUMERIC_CAVEATED_REVIEWED",
                "freeze_candidate": True,
                "notes": "Independent H I support radius proxy; consistent with SPARC RHI.",
            },
            {
                "observable_id": "R_HI_source_vs_SPARC_relative_difference",
                "value": rhi_relative_difference,
                "unit": "dimensionless",
                "source_basis": "source-native R_HI compared to SPARC RHI",
                "source_id": "SPARC_MASTER+VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "status": "CONSISTENCY_CHECK_PASS",
                "freeze_candidate": False,
                "notes": "Agreement below 1%; supports using RHI as denominator.",
            },
            {
                "observable_id": "projection_edge_on_strength_p_edge",
                "value": p_edge,
                "unit": "dimensionless",
                "source_basis": "sin^2(i_HI), i_HI=83 deg",
                "source_id": "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "status": "ACCEPTED_NUMERIC_CAVEATED_REVIEWED",
                "freeze_candidate": True,
                "notes": "High-inclination projection observable; not a residual fit.",
            },
            {
                "observable_id": "disk_scale_fraction_x_scale",
                "value": x_scale,
                "unit": "dimensionless",
                "source_basis": "Rdisk/R_HI_source",
                "source_id": "SPARC_MASTER+VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "status": "ACCEPTED_NUMERIC_RESIDUAL_BLIND",
                "freeze_candidate": True,
                "notes": "Scale placement observable for smooth disk carrier.",
            },
            {
                "observable_id": "hi_extent_in_disk_scales",
                "value": x_hi_extent,
                "unit": "dimensionless",
                "source_basis": "R_HI_source/Rdisk",
                "source_id": "SPARC_MASTER+VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "status": "ACCEPTED_NUMERIC_RESIDUAL_BLIND",
                "freeze_candidate": True,
                "notes": "Extended support observable; large value favors outer-overlay review.",
            },
            {
                "observable_id": "outer_warp_flag",
                "value": 1.0,
                "unit": "dimensionless flag",
                "source_basis": "source note: slightly warped in the outer regions",
                "source_id": "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "status": "ACCEPTED_CONTEXT_CAVEATED",
                "freeze_candidate": False,
                "notes": "Qualitative source support; no numeric warp onset/amplitude yet.",
            },
            {
                "observable_id": "hi_position_angle_deg",
                "value": hi_position_angle_deg,
                "unit": "deg",
                "source_basis": "total H I map position angle",
                "source_id": "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "status": "ACCEPTED_NUMERIC_CAVEATED_REVIEWED",
                "freeze_candidate": True,
                "notes": "Orientation field; formula use requires a declared projection kernel.",
            },
            {
                "observable_id": "warp_onset_or_amplitude",
                "value": pd.NA,
                "unit": "dimensionless_or_kpc",
                "source_basis": "not available in current reviewed sources",
                "source_id": "PENDING",
                "status": "BLOCKED_NUMERIC_FIELD_MISSING",
                "freeze_candidate": False,
                "notes": "Prevents a source-native warp ramp freeze.",
            },
            {
                "observable_id": "bar_core_history_overlay",
                "value": pd.NA,
                "unit": "mixed",
                "source_basis": "not available in current reviewed sources",
                "source_id": "PENDING",
                "status": "BLOCKED_REQUIRED_FIELD_MISSING",
                "freeze_candidate": False,
                "notes": "Current worklist readout name requires this review before label promotion.",
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_OBS_G1_SOURCE_AUDIT_INPUT",
                "gate_status": "PASS",
                "evidence": str(audit_summary["source_audit_status"]),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "observable sheet only; no scoring",
            },
            {
                "gate_id": "N4183_OBS_G2_RHI_DENOMINATOR",
                "gate_status": "PASS_CAVEATED",
                "evidence": f"source-native RHI={rhi_source_kpc:.3f} kpc vs SPARC RHI={rhi_sparc_kpc:.3f} kpc",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "choose formula lane before using denominator",
            },
            {
                "gate_id": "N4183_OBS_G3_PROJECTION_OBSERVABLE",
                "gate_status": "PASS_CAVEATED",
                "evidence": f"HI inclination={hi_inclination_deg:.1f} deg gives p_edge={p_edge:.3f}",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "derive projection kernel and coefficient rule",
            },
            {
                "gate_id": "N4183_OBS_G4_WARP_NUMERIC_KERNEL",
                "gate_status": "BLOCKED",
                "evidence": "outer warp is qualitative only; no onset/amplitude frozen",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "acquire source-native warp onset/amplitude or use a projection-only lane",
            },
            {
                "gate_id": "N4183_OBS_G5_LABEL_PROMOTION",
                "gate_status": "BLOCKED",
                "evidence": "bar/core/history overlay field remains missing for current proposed label",
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "remaining_obligation": "either acquire missing fields or narrow label to projection/outer-warp caveated lane",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "observable_sheet_status": "NGC4183_MIXED_OVERLAY_OBSERVABLE_SHEET_PARTIAL_PASS_LABEL_AND_FORMULA_BLOCKED",
                "galaxy": GALAXY,
                "n_observables": len(observables),
                "n_freeze_candidates": int(observables["freeze_candidate"].sum()),
                "rhi_source_kpc": rhi_source_kpc,
                "rhi_sparc_kpc": rhi_sparc_kpc,
                "rhi_relative_difference": rhi_relative_difference,
                "projection_edge_on_strength_p_edge": p_edge,
                "has_numeric_warp_kernel": False,
                "has_bar_core_history_overlay": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "narrow_or_promote_label_then_derive_projection_or_outer_warp_formula_shell",
            }
        ]
    )

    observables.to_csv(DATA / "ngc4183_mixed_overlay_observable_sheet.csv", index=False)
    gates.to_csv(DATA / "ngc4183_mixed_overlay_observable_sheet_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_mixed_overlay_observable_sheet_summary.csv", index=False)

    source_fields = audit_fields[["field_id", "value", "unit", "field_status", "freeze_usable"]]
    report = f"""# NGC4183 Mixed-Overlay Observable Sheet

Status: `{summary.iloc[0]["observable_sheet_status"]}`

This sheet turns residual-blind NGC4183 source information into candidate
observables for a later readout formula.  It is not an endpoint score and does
not read observed velocity residuals.

## Summary

{markdown_table(summary)}

## Observables

{markdown_table(observables)}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Source Fields Used

{markdown_table(source_fields)}

## Dimensional/Limit Notes

- `R_HI_source_native_kpc`, `Rdisk`, and `Vflat` carry physical units and can
  only enter a future formula through a dimensionally checked shell.
- `p_edge = sin^2(i_HI)` and `Rdisk/R_HI` are dimensionless.
- The zero-overlay/no-warp limit must recover the chosen carrier before any
  endpoint scoring.

## Verdict

NGC4183 now has a partial residual-blind observable sheet: H I support radius,
high-inclination projection strength, disk-scale fraction, and qualitative outer
warp context.  It is still blocked for formula freeze because the current
mixed-overlay label requires either numeric warp/onset amplitude or a narrowed
projection-dominated label with an independently justified coefficient rule.
"""
    (REPORTS / "ngc4183_mixed_overlay_observable_sheet.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
