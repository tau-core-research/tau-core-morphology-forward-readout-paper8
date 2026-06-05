#!/usr/bin/env python3
"""Acquire NGC4013 compact/overlay source evidence.

This source-acquisition pass intentionally preserves negative evidence. The
S4G Pipeline 4 decomposition row for NGC4013 contains an edge-disk component and
a nuclear PSF, but no Sersic bulge component with an effective radius. Together
with the Comeron et al. vertical-decomposition paper, this pressures the row
away from a compact endpoint lane and toward a warp/vertical-overlay lane.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_compact_overlay_source_acquisition_not_endpoint"


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

    s4g = pd.read_csv(DATA / "external_s4g_table7.csv")
    rows = s4g.loc[s4g["Name"] == "NGC4013"].copy()
    if rows.empty:
        raise RuntimeError("NGC4013 missing from external_s4g_table7.csv")

    z = rows.loc[rows["C"].astype(str).str.upper() == "Z"].iloc[0]
    n = rows.loc[rows["C"].astype(str).str.upper() == "N"].iloc[0]
    has_bulge = bool((rows["C"].astype(str).str.upper() == "B").any())
    kpc_per_arcsec = 18.0 * 1000.0 / 206265.0
    hr_kpc = float(z["hr2"]) * kpc_per_arcsec
    hz_kpc = float(z["hz2"]) * kpc_per_arcsec
    h_over_r = float(z["hz2"]) / float(z["hr2"])

    acquired = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "source_id": "S4G_PIPELINE4_TABLE7_LOCAL",
                "source_file": "data/derived/external_s4g_table7.csv",
                "source_line_refs": "Seq=1004; components C=Z,N",
                "observable": "s4g_component_decomposition",
                "extracted_value": "Z edgedisk + N nuclear_psf; no B bulge component",
                "numeric_value": "",
                "unit": "categorical",
                "acquisition_status": "ACQUIRED_NEGATIVE_COMPACT_EVIDENCE",
                "compact_lane_impact": "NO_S4G_BULGE_RE; compact support radius not acquired",
                "overlay_lane_impact": "edge-disk component supports vertical/projection review",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "source_id": "S4G_PIPELINE4_EDGE_DISK_GEOMETRY",
                "source_file": "data/derived/external_s4g_table7.csv",
                "source_line_refs": "Seq=1004; C=Z; Fn=edgedisk",
                "observable": "s4g_edge_disk_hr_hz",
                "extracted_value": f"hr={float(z['hr2']):.6g} arcsec; hz={float(z['hz2']):.6g} arcsec",
                "numeric_value": f"{hr_kpc:.9g};{hz_kpc:.9g};{h_over_r:.9g}",
                "unit": "kpc;kpc;dimensionless",
                "acquisition_status": "ACQUIRED_VERTICAL_KERNEL_EVIDENCE",
                "compact_lane_impact": "not compact support",
                "overlay_lane_impact": "source-native stellar edge-disk h/R supports vertical-overlay kernel",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "source_id": "COMERON2011_VERTICAL_DECOMPOSITION",
                "source_file": "data/external/literature/ngc4013_comeron_2011_unusual_vertical_mass_distribution.txt",
                "source_line_refs": "11-20;67-70;167-180;188-192",
                "observable": "thin_thick_extended_component_decomposition",
                "extracted_value": "thin+thick disk plus extra extended component; z_EC about 3 kpc; EC about 20 percent mass",
                "numeric_value": "3.0;0.20",
                "unit": "kpc;mass_fraction",
                "acquisition_status": "ACQUIRED_EXTENDED_VERTICAL_COMPONENT_EVIDENCE",
                "compact_lane_impact": "supports non-compact vertical/extended morphology rather than compact-only endpoint",
                "overlay_lane_impact": "strong support for warp/vertical-overlay candidate",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "source_id": "COMERON2011_BOXY_BULGE_CAVEAT",
                "source_file": "data/external/literature/ngc4013_comeron_2011_unusual_vertical_mass_distribution.txt",
                "source_line_refs": "76-83;89-92",
                "observable": "boxy_bulge_or_edge_on_bar_context",
                "extracted_value": "boxy bulge noted as possible edge-on bar or merger consequence; profile bins avoid bulge influence",
                "numeric_value": "",
                "unit": "context",
                "acquisition_status": "ACQUIRED_COMPACT_CAVEAT_NOT_RADIUS",
                "compact_lane_impact": "boxy-bulge context does not provide compact support radius",
                "overlay_lane_impact": "supports bar/merger/vertical-history caveat",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "n_acquired_source_rows": len(acquired),
                "s4g_components": ";".join(rows["C"].astype(str) + ":" + rows["Fn"].astype(str)),
                "has_s4g_bulge_component": has_bulge,
                "s4g_edge_disk_hr_kpc": hr_kpc,
                "s4g_edge_disk_hz_kpc": hz_kpc,
                "s4g_edge_disk_h_over_r": h_over_r,
                "extended_component_scaleheight_kpc": 3.0,
                "extended_component_mass_fraction": 0.20,
                "compact_support_radius_acquired": False,
                "bulge_core_decomposition_decision": "NO_S4G_BULGE_COMPONENT_ONLY_NUCLEAR_PSF_AND_BOXY_BULGE_CONTEXT",
                "compact_lane_decision": "COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED",
                "replacement_lane_recommendation": "PROMOTE_WARP_VERTICAL_OVERLAY_PREFLIGHT_NOT_ENDPOINT",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    acquired.to_csv(DATA / "ngc4013_compact_overlay_source_acquisition.csv", index=False)
    summary.to_csv(DATA / "ngc4013_compact_overlay_source_summary.csv", index=False)

    report = [
        "# NGC4013 Compact/Overlay Source Acquisition",
        "",
        "This pass acquires compact-support and overlay evidence for NGC4013.",
        "It preserves a negative result: the local S4G Pipeline 4 table contains",
        "no Sersic bulge component with an effective radius for NGC4013.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Acquired Source Rows",
        "",
        markdown_table(acquired),
        "",
        "## Interpretation",
        "",
        "The missing compact/bulge blocker is not resolved by finding a compact",
        "support radius. It is resolved in the opposite direction: the currently",
        "available S4G and literature sources do not support a compact endpoint",
        "lane. They support a warp/vertical-overlay preflight lane, with endpoint",
        "scoring still blocked until a source-frozen overlay formula is defined.",
        "",
    ]
    (REPORTS / "ngc4013_compact_overlay_source_acquisition.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
