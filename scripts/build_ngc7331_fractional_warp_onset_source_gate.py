#!/usr/bin/env python3
"""Build a source-only NGC7331 fractional warp-onset gate.

This gate tightens the NGC7331 outer-warp caveat without changing the already
scored V1 endpoint.  Bosma's NED-hosted 21 cm discussion gives both a Holmberg
major-axis size and a fractional warp-onset statement.  We convert that source
statement into an approximate kpc onset using the SPARC distance, but mark any
formula update as replay-required because the accepted NGC7331 mixed endpoint
has already been scored with the broad Rdisk-to-RHI V1 window.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc7331_fractional_warp_onset_source_gate_not_endpoint"


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
    caveat = pd.read_csv(DATA / "ngc7331_outer_warp_vertical_caveat_summary.csv").iloc[0]
    row = sparc.loc[sparc["Galaxy"].eq("NGC7331")].iloc[0]

    distance_mpc = float(row["D_Mpc"])
    rdisk_kpc = float(row["Rdisk_kpc"])
    rhi_kpc = float(row["RHI_kpc"])
    holmberg_major_diameter_arcmin = 13.5
    holmberg_radius_arcmin = holmberg_major_diameter_arcmin / 2.0
    fractional_onset_in_holmberg_radius = 0.5
    onset_arcmin = fractional_onset_in_holmberg_radius * holmberg_radius_arcmin
    kpc_per_arcmin = distance_mpc * 1000.0 * 3.141592653589793 / (180.0 * 60.0)
    onset_kpc = onset_arcmin * kpc_per_arcmin
    onset_over_rdisk = onset_kpc / rdisk_kpc
    onset_over_rhi = onset_kpc / rhi_kpc

    fields = pd.DataFrame(
        [
            {
                "field_id": "N7331_FW1_HOLMBERG_SIZE",
                "observable": "holmberg_major_axis_size",
                "value": holmberg_major_diameter_arcmin,
                "unit": "arcmin",
                "status": "ACCEPTED_SOURCE_NUMERIC_FIELD",
                "source": "https://ned.ipac.caltech.edu/level5/March05/Bosma/Bosma4_7.html",
                "source_line_refs": "lines 5-6",
                "role": "sets Holmberg-system angular major-axis size for fractional onset conversion",
            },
            {
                "field_id": "N7331_FW2_FRACTIONAL_WARP_ONSET",
                "observable": "warp_onset_fraction_of_holmberg_radius",
                "value": fractional_onset_in_holmberg_radius,
                "unit": "dimensionless",
                "status": "ACCEPTED_SOURCE_FRACTIONAL_FIELD",
                "source": "https://ned.ipac.caltech.edu/level5/March05/Bosma/Bosma4_7.html",
                "source_line_refs": "lines 80-84",
                "role": "source-anchors the outer-warp onset fraction without using rotation residuals",
            },
            {
                "field_id": "N7331_FW3_APPROX_ONSET_KPC",
                "observable": "approx_warp_onset_radius",
                "value": onset_kpc,
                "unit": "kpc",
                "status": "DERIVED_FROM_BOSMA_FRACTION_AND_SPARC_DISTANCE",
                "source": "Bosma Holmberg fraction + SPARC distance",
                "source_line_refs": "Bosma lines 5-6 and 80-84; SPARC D_Mpc",
                "role": "candidate V2 outer-window inner radius; not applied to the already scored V1 endpoint",
            },
        ]
    )
    fields["uses_vobs_or_residual"] = False
    fields["endpoint_scores_allowed"] = False
    fields["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_FW_G1_SOURCE_STATEMENT_PRESENT",
                "gate_status": "PASS",
                "evidence": "Bosma/NED states NGC7331 warp starts at 0.5 times the Holmberg radius",
                "remaining_obligation": "none at source-statement level",
            },
            {
                "gate_id": "N7331_FW_G2_KPC_CONVERSION_AVAILABLE",
                "gate_status": "PASS_CAVEATED",
                "evidence": f"0.5*R_Ho={onset_arcmin:.3f} arcmin; SPARC D={distance_mpc:.3f} Mpc gives R_onset={onset_kpc:.3f} kpc",
                "remaining_obligation": "conversion depends on pairing the Bosma Holmberg size with the SPARC distance",
            },
            {
                "gate_id": "N7331_FW_G3_ENDPOINT_PROTOCOL_BOUNDARY",
                "gate_status": "BLOCKED_REPLAY_REQUIRED",
                "evidence": "accepted NGC7331 V1 endpoint was already scored with broad Rdisk-to-RHI window",
                "remaining_obligation": "use this onset only in a predeclared V2 replay/holdout or future endpoint",
            },
        ]
    )
    gates["galaxy"] = "NGC7331"
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC7331",
                "source_gate_status": "FRACTIONAL_WARP_ONSET_SOURCE_READY_REPLAY_REQUIRED",
                "previous_outer_warp_numeric_onset_available": bool(
                    caveat["outer_warp_numeric_onset_available"]
                ),
                "fractional_warp_onset_available": True,
                "approx_warp_onset_arcmin": onset_arcmin,
                "approx_warp_onset_kpc": onset_kpc,
                "approx_warp_onset_over_Rdisk": onset_over_rdisk,
                "approx_warp_onset_over_RHI": onset_over_rhi,
                "v1_broad_window_inner_kpc": rdisk_kpc,
                "v1_broad_window_outer_kpc": rhi_kpc,
                "candidate_v2_window_inner_kpc": onset_kpc,
                "candidate_v2_window_outer_kpc": rhi_kpc,
                "formula_update_allowed_for_current_endpoint": False,
                "replay_or_holdout_required": True,
                "uses_vobs_or_residual_in_construction": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    fields.to_csv(DATA / "ngc7331_fractional_warp_onset_source_fields.csv", index=False)
    gates.to_csv(DATA / "ngc7331_fractional_warp_onset_source_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_fractional_warp_onset_source_summary.csv", index=False)

    report = [
        "# NGC7331 Fractional Warp-Onset Source Gate",
        "",
        "This source-only gate tightens the NGC7331 outer-warp caveat without",
        "changing the already scored V1 mixed endpoint. It records a source",
        "fractional onset statement and an approximate kpc conversion, but any",
        "formula update is replay/holdout-only.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source Fields",
        "",
        markdown_table(fields),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "This gate is not an endpoint score and not a post-hoc improvement of the",
        "accepted NGC7331 V1 result. The candidate V2 window may be used only in",
        "a predeclared replay/holdout lane or a future source-selected case.",
        "",
    ]
    (REPORTS / "ngc7331_fractional_warp_onset_source_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
