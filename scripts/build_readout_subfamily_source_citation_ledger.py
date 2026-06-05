#!/usr/bin/env python3
"""Build a citation ledger for readout-subfamily source candidates."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "citation_ledger_supports_data_review_not_label_acceptance"


CITATION_KEYS = {
    ("IC2574", "hi_asymmetry_map"): "deBlok2020IC2574HI",
    ("IC2574", "environment_history"): "WalterBrinks1999IC2574Holes",
    ("IC2574", "outer_tail_transition"): "SanchezSalcedo2002IC2574Holes",
    ("NGC4013", "disk_overlay_check"): "ZschaechnerRand2015NGC4013HI",
    ("NGC5907", "velocity_field_sanity"): "Shang1998NGC5907Warp",
    ("NGC5907", "vertical_or_warp_source"): "Wiegert2015EdgeOnISM",
    ("NGC5907", "projection_geometry"): "Sasaki1987NGC5907Warp",
    ("NGC7331", "vertical_scale_or_thickness"): "Patra2018NGC7331ScaleHeight",
    ("NGC4183", "bar_core_projection_history_overlay"): "vanEymeren2011WHISPLopsidedness",
    ("UGC05716", "hi_asymmetry_map"): "Swaters2009LateTypeDwarfs",
}


SOURCE_ROLE = {
    "hi_asymmetry_map": "HI asymmetry / disturbed gas context",
    "environment_history": "morphology-memory or disturbed-gas context",
    "outer_tail_transition": "outer-tail or asymmetry transition review",
    "disk_overlay_check": "disk/warp overlay review",
    "velocity_field_sanity": "velocity-field/projection sanity review",
    "vertical_or_warp_source": "vertical, flare, or warp source review",
    "projection_geometry": "projection and optical-warp geometry review",
    "vertical_scale_or_thickness": "vertical scale or thickness review",
    "bar_core_projection_history_overlay": "bar/core/projection/history overlay review",
}


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    acquisition = pd.read_csv(DATA / "readout_subfamily_external_source_acquisition_matrix.csv")
    cache = pd.read_csv(DATA / "readout_subfamily_external_source_cache_manifest.csv")
    source_rows = acquisition[
        (acquisition["external_source_status"] != "NO_EXTERNAL_SOURCE_HIT_RECORDED")
        & (acquisition["external_source_status"] != "NO_TARGETED_EXTERNAL_SOURCE_HIT_THIS_PASS")
    ].copy()
    source_rows["citation_key"] = source_rows.apply(
        lambda row: CITATION_KEYS.get((row["galaxy"], row["evidence_id"]), ""),
        axis=1,
    )
    source_rows["source_role"] = source_rows["evidence_id"].map(SOURCE_ROLE).fillna(
        "source review candidate"
    )
    cache_cols = [
        "galaxy",
        "evidence_id",
        "cache_status",
        "local_path",
        "text_cache_status",
        "text_local_path",
        "download_error",
    ]
    ledger = source_rows.merge(cache[cache_cols], on=["galaxy", "evidence_id"], how="left")
    ledger["accepted_label_promoted"] = False
    ledger["endpoint_scores_allowed"] = False
    ledger["claim_boundary"] = CLAIM_BOUNDARY
    ledger = ledger[
        [
            "galaxy",
            "proposed_readout_subfamily",
            "evidence_id",
            "source_role",
            "citation_key",
            "source_authors_year",
            "source_title",
            "source_url",
            "cache_status",
            "text_cache_status",
            "local_path",
            "text_local_path",
            "promotion_relevance",
            "accepted_label_promoted",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ].sort_values(["galaxy", "evidence_id"])
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    ledger.to_csv(DATA / "readout_subfamily_source_citation_ledger.csv", index=False)
    summary = (
        ledger.groupby(["galaxy", "cache_status"], dropna=False, as_index=False)
        .agg(n_sources=("evidence_id", "size"))
        .sort_values(["galaxy", "cache_status"])
    )
    summary.to_csv(DATA / "readout_subfamily_source_citation_ledger_summary.csv", index=False)
    report = [
        "# Readout-Subfamily Source Citation Ledger",
        "",
        "This ledger links residual-blind source candidates to BibTeX citation keys,",
        "local cache status, and the readout-subfamily observable each source may support.",
        "It does not promote any accepted morphology label and does not use endpoint scores.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Ledger",
        "",
        markdown_table(
            ledger[
                [
                    "galaxy",
                    "proposed_readout_subfamily",
                    "evidence_id",
                    "source_role",
                    "citation_key",
                    "cache_status",
                    "text_cache_status",
                    "claim_boundary",
                ]
            ]
        ),
        "",
    ]
    (REPORTS / "readout_subfamily_source_citation_ledger.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
