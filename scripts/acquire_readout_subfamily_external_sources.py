#!/usr/bin/env python3
"""Acquire targeted external source hits for readout-subfamily evidence.

The pass records external literature/source candidates found for the current
multi-galaxy subfamily-intake atlas. It is residual-blind and does not score
rotation endpoints or promote accepted subfamily labels.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "readout_subfamily_external_source_acquisition_not_endpoint"


SOURCE_HITS = [
    {
        "galaxy": "IC2574",
        "evidence_id": "hi_asymmetry_map",
        "source_status": "DIRECT_HI_CONTEXT_READY_REVIEW_REQUIRED",
        "source_title": "5 deg x 5 deg deep HI survey of the M81 group - II. HI distribution and kinematics of IC 2574 and HIJASS J1021+68",
        "source_authors_year": "de Blok et al. / MNRAS 2020 source family",
        "source_url": "https://academic.oup.com/mnras/article/493/2/2618/5734519",
        "source_evidence": "deep HI observations map the extended HI envelope around IC2574 and derive an extended 3D tilted-ring rotation curve",
        "promotion_relevance": "candidate source for disturbed-tail/HI-envelope subfamily; asymmetry and tail-transition radii still need extraction",
    },
    {
        "galaxy": "IC2574",
        "evidence_id": "environment_history",
        "source_status": "DIRECT_HI_CONTEXT_READY_REVIEW_REQUIRED",
        "source_title": "Holes and Shells in the Interstellar Medium of the Nearby Dwarf Galaxy IC 2574",
        "source_authors_year": "Walter & Brinks 1999",
        "source_url": "https://arxiv.org/abs/astro-ph/9904002",
        "source_evidence": "VLA HI synthesis observations report many HI holes/shells and an HI layer scaleheight context",
        "promotion_relevance": "supports morphology-memory/disturbed-gas review; not a tail-transition measurement by itself",
    },
    {
        "galaxy": "IC2574",
        "evidence_id": "outer_tail_transition",
        "source_status": "DIRECT_ASYMMETRY_CONTEXT_READY_REVIEW_REQUIRED",
        "source_title": "A New Look at the Holes of IC 2574",
        "source_authors_year": "Sánchez-Salcedo & Hidalgo-Gámez 2002",
        "source_url": "https://astronomia.unam.mx/journals/rmxaa/article/view/2002rmxaa..38...39s",
        "source_evidence": "abstract notes asymmetry between both sides in photometric properties and HI mass",
        "promotion_relevance": "candidate evidence for K_disturbed_outer_tail; needs accepted extraction/audit",
    },
    {
        "galaxy": "NGC4013",
        "evidence_id": "disk_overlay_check",
        "source_status": "DIRECT_HI_WARP_CONTEXT_READY_REVIEW_REQUIRED",
        "source_title": "The HI Kinematics of NGC 4013: a Steep and Radially Shallowing Extra-planar Rotational Lag",
        "source_authors_year": "Zschaechner & Rand 2015",
        "source_url": "https://arxiv.org/abs/1506.05123",
        "source_evidence": "paper describes NGC4013 as distinctly warped with evidence of disk-halo activity",
        "promotion_relevance": "warns compact-only classification may need disk/warp overlay review",
    },
    {
        "galaxy": "NGC5907",
        "evidence_id": "velocity_field_sanity",
        "source_status": "DIRECT_WARP_INTERACTION_CONTEXT_READY_REVIEW_REQUIRED",
        "source_title": "Ring structure and warp of NGC 5907 -- Interaction with dwarf galaxies",
        "source_authors_year": "Shang et al. 1998",
        "source_url": "https://arxiv.org/abs/astro-ph/9806395",
        "source_evidence": "edge-on NGC5907 is discussed as a warped galaxy; a dwarf is seen at the tip of the HI warp and in the direction of the warp",
        "promotion_relevance": "supports projection/warp/history audit for K_projection_dominated or warp overlay",
    },
    {
        "galaxy": "NGC5907",
        "evidence_id": "vertical_or_warp_source",
        "source_status": "DIRECT_VERTICAL_CONTEXT_READY_REVIEW_REQUIRED",
        "source_title": "The Interstellar Medium and Star Formation in Edge-On Galaxies. II. NGC 4157, 4565, and 5907",
        "source_authors_year": "Wiegert et al. 2015",
        "source_url": "https://arxiv.org/abs/1408.5905",
        "source_evidence": "study uses VLA HI, CO, and Spitzer data for vertical gas/stars structure in edge-on NGC5907",
        "promotion_relevance": "candidate source for projection/vertical sanity; needs subfamily-specific extraction",
    },
    {
        "galaxy": "NGC5907",
        "evidence_id": "projection_geometry",
        "source_status": "DIRECT_OPTICAL_WARP_CONTEXT_READY_REVIEW_REQUIRED",
        "source_title": "Surface Photometry of the Warping Edge-on Galaxy NGC 5907",
        "source_authors_year": "Sasaki 1987",
        "source_url": "https://academic.oup.com/pasj/article/39/6/849/8078264",
        "source_evidence": "surface photometry targets the optical warping of the outer disk and notes tidal interaction relevance",
        "promotion_relevance": "supports projection/warp review; no endpoint label promotion",
    },
    {
        "galaxy": "NGC7331",
        "evidence_id": "vertical_scale_or_thickness",
        "source_status": "DIRECT_VERTICAL_CONTEXT_READY_REVIEW_REQUIRED",
        "source_title": "Molecular scale height in NGC 7331",
        "source_authors_year": "Patra 2018",
        "source_url": "https://arxiv.org/abs/1706.08615",
        "source_evidence": "molecular disk projected to edge-on yields an observable thickness estimate around 500 pc",
        "promotion_relevance": "candidate source for K_thick_regular vertical-scale acceptance; needs mapping into h/Rs",
    },
    {
        "galaxy": "NGC4183",
        "evidence_id": "bar_core_projection_history_overlay",
        "source_status": "HI_WARP_SAMPLE_CONTEXT_REVIEW_REQUIRED",
        "source_title": "Warps and lopsidedness in HI disks from WHISP edge-on samples",
        "source_authors_year": "García-Ruiz et al. 2002 / WHISP source family",
        "source_url": "https://arxiv.org/abs/1103.4928",
        "source_evidence": "WHISP context reports HI maps, radial HI density profiles, rotation curves, warping and lopsidedness studies for edge-on disk samples",
        "promotion_relevance": "candidate projection/overlay source path for NGC4183; primary paper/table extraction still required",
    },
    {
        "galaxy": "UGC05716",
        "evidence_id": "hi_asymmetry_map",
        "source_status": "HI_PROFILE_SOURCE_CANDIDATE_REVIEW_REQUIRED",
        "source_title": "The rotation curves shapes of late-type dwarf galaxies",
        "source_authors_year": "Swaters et al. 2009",
        "source_url": "https://astroweb.case.edu/ssm/papers/AAv505p577.pdf",
        "source_evidence": "SPARC-linked source family includes UGC5716/D500-2 context for HI disk inclination/rotation analysis",
        "promotion_relevance": "candidate source for disturbed-tail review; specific HI asymmetry/transition extraction still missing",
    },
    {
        "galaxy": "IC4202",
        "evidence_id": "compact_support_radius",
        "source_status": "NO_TARGETED_EXTERNAL_SOURCE_HIT_THIS_PASS",
        "source_title": "",
        "source_authors_year": "",
        "source_url": "",
        "source_evidence": "local manifest has bulge/core proxy but no accepted compact support radius source",
        "promotion_relevance": "query S4G/NED/SIMBAD/decomposition next",
    },
    {
        "galaxy": "UGC12506",
        "evidence_id": "disk_scale_overlay",
        "source_status": "NO_TARGETED_EXTERNAL_SOURCE_HIT_THIS_PASS",
        "source_title": "",
        "source_authors_year": "",
        "source_url": "",
        "source_evidence": "local accepted manifest lacks disk scale; overlay reason remains proxy-only",
        "promotion_relevance": "query S4G/NED/decomposition and overlay/projection review next",
    },
]


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


def build_acquisition() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    matrix = pd.read_csv(DATA / "readout_subfamily_source_evidence_matrix.csv")
    hits = pd.DataFrame(SOURCE_HITS)
    hits["endpoint_scores_allowed"] = False
    hits["accepted_label_promoted"] = False
    hits["claim_boundary"] = CLAIM_BOUNDARY
    matrix_keys = set(zip(matrix["galaxy"], matrix["evidence_id"]))
    hits["matched_evidence_row"] = hits.apply(
        lambda row: (row["galaxy"], row["evidence_id"]) in matrix_keys,
        axis=1,
    )
    joined = matrix.merge(
        hits,
        on=["galaxy", "evidence_id"],
        how="left",
        suffixes=("", "_external"),
    )
    joined["external_source_status"] = joined["source_status"].fillna(
        "NO_EXTERNAL_SOURCE_HIT_RECORDED"
    )
    joined["source_title"] = joined["source_title"].fillna("")
    joined["source_url"] = joined["source_url"].fillna("")
    joined["source_evidence"] = joined["source_evidence"].fillna("")
    joined["promotion_relevance"] = joined["promotion_relevance"].fillna(
        "source still required"
    )
    joined["post_acquisition_status"] = joined.apply(
        lambda row: (
            "REVIEW_READY_NOT_ACCEPTED"
            if "READY" in str(row["external_source_status"])
            else "SOURCE_SEARCH_STILL_REQUIRED"
        ),
        axis=1,
    )
    summary = (
        joined.groupby(["galaxy", "proposed_readout_subfamily", "post_acquisition_status"], as_index=False)
        .agg(
            n_items=("evidence_id", "size"),
            n_external_hits=("external_source_status", lambda s: int((s != "NO_EXTERNAL_SOURCE_HIT_RECORDED").sum())),
            n_review_ready=("post_acquisition_status", lambda s: int((s == "REVIEW_READY_NOT_ACCEPTED").sum())),
        )
        .sort_values(["galaxy", "post_acquisition_status"])
    )
    galaxy_hits = (
        hits.groupby("galaxy", as_index=False)
        .agg(
            galaxy_external_hits=("evidence_id", "size"),
            galaxy_matched_hits=("matched_evidence_row", "sum"),
            galaxy_hit_ids=("evidence_id", lambda s: ";".join(s)),
        )
    )
    summary = summary.merge(galaxy_hits, on="galaxy", how="left")
    summary[["galaxy_external_hits", "galaxy_matched_hits"]] = summary[
        ["galaxy_external_hits", "galaxy_matched_hits"]
    ].fillna(0).astype(int)
    summary["galaxy_hit_ids"] = summary["galaxy_hit_ids"].fillna("")
    source_summary = (
        hits.groupby(["galaxy", "source_status"], as_index=False)
        .agg(
            n_hits=("evidence_id", "size"),
            matched_hits=("matched_evidence_row", "sum"),
            evidence_ids=("evidence_id", lambda s: ";".join(s)),
        )
        .sort_values(["galaxy", "source_status"])
    )
    source_summary["matched_hits"] = source_summary["matched_hits"].astype(int)
    source_summary["claim_boundary"] = CLAIM_BOUNDARY
    return joined, summary, source_summary


def write_report(joined: pd.DataFrame, summary: pd.DataFrame, source_summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    hits = pd.DataFrame(SOURCE_HITS)
    matrix_keys = set(zip(joined["galaxy"], joined["evidence_id"]))
    hits["matched_evidence_row"] = hits.apply(
        lambda row: (row["galaxy"], row["evidence_id"]) in matrix_keys,
        axis=1,
    )
    review_ready = joined[joined["post_acquisition_status"] == "REVIEW_READY_NOT_ACCEPTED"][
        [
            "galaxy",
            "proposed_readout_subfamily",
            "evidence_id",
            "source_status",
            "source_authors_year",
            "source_title",
            "source_url",
            "promotion_relevance",
        ]
    ]
    all_hits = hits[
        [
            "galaxy",
            "evidence_id",
            "matched_evidence_row",
            "source_status",
            "source_authors_year",
            "source_title",
            "source_url",
            "promotion_relevance",
        ]
    ]
    lines = [
        "# Readout-Subfamily External Source Acquisition",
        "",
        "This pass records targeted external source hits for the first-pass",
        "readout-subfamily evidence matrix. It is residual-blind: no endpoint",
        "score, best-fit readout, or required-S_tau diagnostic is used to promote",
        "a label.",
        "",
        "## By Galaxy",
        "",
        markdown_table(summary),
        "",
        "## Review-Ready Source Hits",
        "",
        markdown_table(review_ready),
        "",
        "## All Targeted Source Hits",
        "",
        markdown_table(all_hits),
        "",
        "## Source Hit Summary",
        "",
        markdown_table(source_summary),
        "",
        "## Claim Boundary",
        "",
        "A source hit is not an accepted subfamily label. The review-ready rows",
        "must still be audited for the exact observable required by the subfamily",
        "gate, such as warp onset, HI asymmetry, compact support radius, projection",
        "safety, or vertical scale mapping.",
        "",
    ]
    (REPORTS / "readout_subfamily_external_source_acquisition.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    joined, summary, source_summary = build_acquisition()
    joined.to_csv(DATA / "readout_subfamily_external_source_acquisition_matrix.csv", index=False)
    summary.to_csv(DATA / "readout_subfamily_external_source_acquisition_summary.csv", index=False)
    source_summary.to_csv(DATA / "readout_subfamily_external_source_hits.csv", index=False)
    write_report(joined, summary, source_summary)
    print(summary.to_string(index=False))
    print(source_summary.to_string(index=False))


if __name__ == "__main__":
    main()
