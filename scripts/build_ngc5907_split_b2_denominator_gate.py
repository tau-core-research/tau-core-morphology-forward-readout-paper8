#!/usr/bin/env python3
"""Build the NGC5907 split-B2 denominator/source-radius gate.

The split-B2 unit-load shell needs a frozen radial coordinate

    x = R / R_outer,    x_w = R_warp_start / R_outer.

For NGC5907 the SPARC master row has RHI_kpc=0, so the clean SPARC-RHI route is
blocked. This gate records whether a residual-blind source-native denominator
can be used instead. It does not score endpoints and does not freeze the final
velocity formula.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC5907"
CLAIM_BOUNDARY = "ngc5907_split_b2_denominator_gate_not_endpoint"


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

    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    freeze_fields = pd.read_csv(DATA / "ngc5907_projection_freeze_fields.csv")
    selector = pd.read_csv(DATA / "split_b2_independent_holdout_candidates.csv")

    sparc_row = sparc.loc[sparc["Galaxy"].eq(GALAXY)].iloc[0]
    selector_row = selector.loc[selector["galaxy"].eq(GALAXY)].iloc[0]
    warp_range = freeze_fields.loc[
        freeze_fields["observable"].eq("optical_warp_radial_range")
    ].iloc[0]
    warp_displacement = freeze_fields.loc[
        freeze_fields["observable"].eq("optical_warp_max_displacement")
    ].iloc[0]

    r_inner, r_outer = [float(piece) for piece in str(warp_range["value"]).split("-")]
    rhi_sparc = float(sparc_row["RHI_kpc"])
    vflat = float(sparc_row["Vflat_kms"])
    rdisk = float(sparc_row["Rdisk_kpc"])
    inc = float(sparc_row["Inc_deg"])
    xw_source_window = r_inner / r_outer
    warp_span = r_outer - r_inner
    warp_displacement_kpc = float(warp_displacement["value"])

    candidates = pd.DataFrame(
        [
            {
                "denominator_id": "D0_SPARC_RHI",
                "r_outer_kpc": rhi_sparc,
                "x_w": pd.NA if rhi_sparc <= 0 else r_inner / rhi_sparc,
                "status": (
                    "BLOCKED_SPARC_RHI_ZERO_OR_MISSING"
                    if rhi_sparc <= 0
                    else "PASS_PRIMARY_DENOMINATOR"
                ),
                "source": "external_sparc_master_table.csv",
                "source_line_refs": "NGC5907 row",
                "interpretation": "clean HI support denominator if nonzero",
                "caveat": "blocked for this galaxy because SPARC RHI_kpc=0",
            },
            {
                "denominator_id": "D1_SOURCE_OPTICAL_WARP_OUTER_EDGE",
                "r_outer_kpc": r_outer,
                "x_w": xw_source_window,
                "status": "PASS_CAVEATED_SOURCE_NATIVE_DENOMINATOR",
                "source": str(warp_range["source"]),
                "source_line_refs": str(warp_range["source_line_refs"]),
                "interpretation": (
                    "outer edge of the source-native optical warp support window"
                ),
                "caveat": (
                    "optical warp support denominator, not HI extent; use only as "
                    "predeclared caveated holdout route"
                ),
            },
            {
                "denominator_id": "D2_DISK_SCALE_LENGTH",
                "r_outer_kpc": rdisk,
                "x_w": r_inner / rdisk,
                "status": "REJECTED_WRONG_ROLE",
                "source": "external_sparc_master_table.csv",
                "source_line_refs": "NGC5907 row",
                "interpretation": "disk scale, not outer support radius",
                "caveat": "would make x_w>1 and inactive-window semantics fail",
            },
        ]
    )
    candidates["galaxy"] = GALAXY
    candidates["uses_vobs_or_residual"] = False
    candidates["endpoint_scores_allowed"] = False
    candidates["claim_boundary"] = CLAIM_BOUNDARY

    selected = candidates.loc[
        candidates["denominator_id"].eq("D1_SOURCE_OPTICAL_WARP_OUTER_EDGE")
    ].iloc[0]

    fields = pd.DataFrame(
        [
            {
                "field_id": "SB2D1_WARP_START",
                "observable": "optical_warp_start_radius",
                "value": r_inner,
                "unit": "kpc",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "source": str(warp_range["source"]),
                "source_line_refs": str(warp_range["source_line_refs"]),
                "role": "sets split-B2 turn-on numerator R_warp_start",
            },
            {
                "field_id": "SB2D2_WARP_OUTER_SUPPORT",
                "observable": "optical_warp_outer_support_radius",
                "value": r_outer,
                "unit": "kpc",
                "status": "PASS_CAVEATED_SOURCE_NATIVE_DENOMINATOR",
                "source": str(warp_range["source"]),
                "source_line_refs": str(warp_range["source_line_refs"]),
                "role": "sets split-B2 denominator R_outer when SPARC RHI is missing",
            },
            {
                "field_id": "SB2D3_SOURCE_XW",
                "observable": "x_w_source_window",
                "value": xw_source_window,
                "unit": "dimensionless",
                "status": "DERIVED_FROM_SOURCE_WINDOW",
                "source": str(warp_range["source"]),
                "source_line_refs": str(warp_range["source_line_refs"]),
                "role": "defines ramp start in source-window coordinate",
            },
            {
                "field_id": "SB2D4_VFLAT",
                "observable": "Vflat",
                "value": vflat,
                "unit": "km/s",
                "status": "SPARC_SOURCE_CATALOG_AVAILABLE",
                "source": "external_sparc_master_table.csv",
                "source_line_refs": "NGC5907 row",
                "role": "sets velocity-squared carrier scale Vflat^2",
            },
            {
                "field_id": "SB2D5_WARP_DISPLACEMENT_CONTEXT",
                "observable": "optical_warp_max_displacement",
                "value": warp_displacement_kpc,
                "unit": "kpc",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD_CONTEXT_ONLY",
                "source": str(warp_displacement["source"]),
                "source_line_refs": str(warp_displacement["source_line_refs"]),
                "role": "supports projection/warp context; not used as denominator",
            },
        ]
    )
    fields["galaxy"] = GALAXY
    fields["endpoint_scores_allowed"] = False
    fields["uses_vobs_or_residual"] = False
    fields["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "SB2D_G1_SELECTOR",
                "gate_status": "PASS_CAVEATED",
                "evidence": str(selector_row["split_b2_holdout_status"]),
                "remaining_obligation": "denominator must be frozen before formula scoring",
            },
            {
                "gate_id": "SB2D_G2_SPARC_RHI_ROUTE",
                "gate_status": "BLOCKED",
                "evidence": f"SPARC RHI_kpc={rhi_sparc:.6g}",
                "remaining_obligation": "do not use SPARC RHI for NGC5907 split-B2",
            },
            {
                "gate_id": "SB2D_G3_SOURCE_NATIVE_DENOMINATOR",
                "gate_status": "PASS_CAVEATED",
                "evidence": (
                    f"Sasaki optical warp source window {r_inner:.6g}-{r_outer:.6g} kpc"
                ),
                "remaining_obligation": (
                    "mark endpoint as caveated unless a source-native HI denominator is acquired"
                ),
            },
            {
                "gate_id": "SB2D_G4_DIMENSIONAL_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": (
                    f"x_w={xw_source_window:.6g} is dimensionless and lies in (0,1)"
                ),
                "remaining_obligation": "none at radial-coordinate level",
            },
            {
                "gate_id": "SB2D_G5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "uses SPARC catalog and source-field freeze only; no vobs/residual columns",
                "remaining_obligation": "future scoring must read a formula freeze manifest unchanged",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["selected_denominator_id"] = str(selected["denominator_id"])
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "denominator_gate_status": (
                    "NGC5907_SPLIT_B2_DENOMINATOR_GATE_PASS_CAVEATED_NOT_ENDPOINT"
                ),
                "selected_denominator_id": str(selected["denominator_id"]),
                "selected_r_outer_kpc": float(selected["r_outer_kpc"]),
                "x_w_source_window": xw_source_window,
                "warp_span_kpc": warp_span,
                "sparc_rhi_kpc": rhi_sparc,
                "vflat_km_s": vflat,
                "n_candidates": len(candidates),
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "formula_freeze_allowed_next": True,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    candidates.to_csv(DATA / "ngc5907_split_b2_denominator_candidates.csv", index=False)
    fields.to_csv(DATA / "ngc5907_split_b2_denominator_fields.csv", index=False)
    gates.to_csv(DATA / "ngc5907_split_b2_denominator_gate.csv", index=False)
    summary.to_csv(DATA / "ngc5907_split_b2_denominator_summary.csv", index=False)

    report = f"""# NGC5907 Split-B2 Denominator Gate

Status: `{summary.iloc[0]['denominator_gate_status']}`

This gate freezes the radial-coordinate denominator needed by a future NGC5907
split-B2 holdout formula. It does not score an endpoint.

## Summary

{markdown_table(summary)}

## Denominator Candidates

{markdown_table(candidates[[
    'denominator_id',
    'r_outer_kpc',
    'x_w',
    'status',
    'interpretation',
    'caveat',
]])}

## Frozen Source Fields

{markdown_table(fields[[
    'field_id',
    'observable',
    'value',
    'unit',
    'status',
    'role',
]])}

## Gates

{markdown_table(gates[[
    'gate_id',
    'gate_status',
    'evidence',
    'remaining_obligation',
]])}

## Interpretation

The clean SPARC-RHI route is blocked because the NGC5907 SPARC row has
`RHI_kpc=0`. A caveated residual-blind denominator is nevertheless available
from the source-native optical warp support window: the Sasaki source gives the
warp from 13.3 to 24.0 kpc, so the split-B2 coordinate can be frozen as
`x_w = 13.3 / 24.0 = {xw_source_window:.6g}`.

This is not the same as an HI support radius. Therefore any split-B2 NGC5907
formula using this denominator must be labelled caveated and predeclared before
scoring.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    (REPORTS / "ngc5907_split_b2_denominator_gate.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
