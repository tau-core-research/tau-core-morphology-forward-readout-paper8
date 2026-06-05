#!/usr/bin/env python3
"""Audit targeted vertical/flare source searches for S4G75 thick/flared blockers.

This is a source-acquisition audit, not an endpoint-scoring step.  It records
both constructive hits and negative searches so that general HI/EPG context is
not accidentally promoted into a galaxy-specific vertical kernel.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
LITERATURE = ROOT / "data" / "external" / "literature"
CLAIM_BOUNDARY = "s4g75_vertical_source_search_audit_not_endpoint"


SOURCE_AUDIT_ROWS = [
    {
        "galaxy": "NGC2683",
        "source_status": "DIRECT_PROFILE_SOURCE_ALREADY_REGISTERED",
        "source_title": "The flaring HI disk of the nearby spiral galaxy NGC 2683",
        "source_authors_year": "Vollmer, Nehlig & Ibata 2016",
        "source_url": "https://arxiv.org/abs/1512.07058",
        "search_result": (
            "direct source-native flare profile exists and is handled by the "
            "NGC2683 mapping/prototype branch"
        ),
        "kernel_relevance": "DIRECT_PROFILE_READY_FOR_MAPPING_NOT_ENDPOINT",
        "direct_profile_extracted": True,
        "endpoint_scores_allowed": False,
    },
    {
        "galaxy": "NGC3972",
        "source_status": "HI_MORPHOLOGY_SOURCE_READY_VERTICAL_KERNEL_NOT_EXTRACTED",
        "source_title": "Baryonic distributions in galaxy dark matter haloes I",
        "source_authors_year": "O'Brien et al. 2016",
        "source_url": "https://academic.oup.com/mnras/article/460/1/689/2608817",
        "search_result": (
            "web source describes new VLA HI observations of NGC3972 with HI "
            "morphology matching the stellar morphology and appearing as a "
            "highly inclined disc; it does not provide a vertical scale, flare "
            "profile, warp radius, or gas-plane thickness in this audit"
        ),
        "kernel_relevance": "OBJECT_HI_MORPHOLOGY_READY_NOT_VERTICAL_KERNEL",
        "direct_profile_extracted": False,
        "endpoint_scores_allowed": False,
    },
    {
        "galaxy": "NGC3972",
        "source_status": "OBJECT_CONTEXT_ONLY_NOT_VERTICAL_KERNEL",
        "source_title": "NGC 3972 HST/NASA object context",
        "source_authors_year": "NASA/Hubble object page",
        "source_url": "https://science.nasa.gov/asset/hubble/ngc-3972/",
        "search_result": (
            "object and image context only; no vertical scale, flare profile, "
            "warp radius, or gas-plane thickness extracted"
        ),
        "kernel_relevance": "CONTEXT_ONLY_NOT_KERNEL_INPUT",
        "direct_profile_extracted": False,
        "endpoint_scores_allowed": False,
    },
    {
        "galaxy": "NGC3972",
        "source_status": "WHISP_URSA_MAJOR_OBSERVING_PARAMETERS_ONLY",
        "source_title": "The Ursa Major Cluster of Galaxies. IV: HI synthesis observations",
        "source_authors_year": "Verheijen & Sancisi 2001",
        "source_url": "https://www.aanda.org/articles/aa/pdf/2001/18/aa10469.pdf",
        "search_result": (
            "local PDF text includes observing parameters for NGC3972, but no "
            "profile-level vertical/warp extraction is recorded in this audit"
        ),
        "kernel_relevance": "OBJECT_HI_OBSERVING_CONTEXT_NOT_VERTICAL_KERNEL",
        "direct_profile_extracted": False,
        "endpoint_scores_allowed": False,
    },
    {
        "galaxy": "NGC3972",
        "source_status": "HALOGAS_TEXT_SEARCH_NEGATIVE_FOR_OBJECT",
        "source_title": "HALOGAS: the properties of extraplanar HI in disc galaxies",
        "source_authors_year": "Marasco et al. 2019",
        "source_url": "https://arxiv.org/abs/1909.04048",
        "search_result": (
            "local PDF text search did not find NGC3972/3972; HALOGAS is useful "
            "EPG context but not a direct NGC3972 kernel source in this pass"
        ),
        "kernel_relevance": "GENERAL_EPG_CONTEXT_NOT_GALAXY_KERNEL",
        "direct_profile_extracted": False,
        "endpoint_scores_allowed": False,
    },
    {
        "galaxy": "NGC4088",
        "source_status": "WHISP_WARP_ASYMMETRY_SOURCE_READY_PROFILE_NOT_EXTRACTED",
        "source_title": "The Ursa Major Cluster of Galaxies. IV: HI synthesis observations",
        "source_authors_year": "Verheijen & Sancisi 2001",
        "source_url": "https://www.aanda.org/articles/aa/pdf/2001/18/aa10469.pdf",
        "search_result": (
            "local PDF text records NGC4088 as strongly distorted, with a "
            "strongly asymmetric position-velocity diagram, asymmetric warp, "
            "and stronger position-angle changes in the southern part"
        ),
        "kernel_relevance": "OBJECT_WARP_ASYMMETRY_READY_NEEDS_PROFILE_EXTRACTION",
        "direct_profile_extracted": False,
        "endpoint_scores_allowed": False,
    },
    {
        "galaxy": "NGC4088",
        "source_status": "HI_KINEMATIC_ASYMMETRY_SOURCE_READY_NOT_VERTICAL_KERNEL",
        "source_title": "Baryonic distributions in galaxy dark matter haloes II",
        "source_authors_year": "O'Brien et al. 2018",
        "source_url": "https://academic.oup.com/mnras/article/476/4/5127/4907988",
        "search_result": (
            "web source describes WHISP HI observations of NGC4088 with an "
            "asymmetric HI disc and kinematic discrepancy between ionized and "
            "neutral gas; no vertical profile is extracted here"
        ),
        "kernel_relevance": "OBJECT_HI_ASYMMETRY_READY_NOT_VERTICAL_KERNEL",
        "direct_profile_extracted": False,
        "endpoint_scores_allowed": False,
    },
    {
        "galaxy": "NGC4088",
        "source_status": "HALOGAS_TEXT_SEARCH_NEGATIVE_FOR_OBJECT",
        "source_title": "HALOGAS: the properties of extraplanar HI in disc galaxies",
        "source_authors_year": "Marasco et al. 2019",
        "source_url": "https://arxiv.org/abs/1909.04048",
        "search_result": (
            "local PDF text search did not find NGC4088/4088; HALOGAS reports "
            "typical EPG thickness for its own sample, but no direct NGC4088 "
            "vertical profile is recorded here"
        ),
        "kernel_relevance": "GENERAL_EPG_CONTEXT_NOT_GALAXY_KERNEL",
        "direct_profile_extracted": False,
        "endpoint_scores_allowed": False,
    },
    {
        "galaxy": "NGC4088",
        "source_status": "GENERAL_HI_SCALE_HEIGHT_CONTEXT_ONLY",
        "source_title": "HI scale height in spiral galaxies",
        "source_authors_year": "Patra 2020",
        "source_url": "https://arxiv.org/abs/2009.11299",
        "search_result": (
            "paper supports the general premise that HI scale-height profiles "
            "can flare radially, but its seven-galaxy sample does not include "
            "NGC4088 in the extracted text"
        ),
        "kernel_relevance": "THEORY_CONTEXT_NOT_OBJECT_KERNEL",
        "direct_profile_extracted": False,
        "endpoint_scores_allowed": False,
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


def text_contains(path: Path, tokens: list[str]) -> dict[str, bool]:
    if not path.exists():
        return {token: False for token in tokens}
    text = path.read_text(encoding="utf-8", errors="ignore")
    return {token: token in text for token in tokens}


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    ledger = pd.read_csv(DATA / "s4g75_remaining_kernel_acquisition_ledger.csv")
    thick = ledger.loc[ledger["formula_family"] == "K_thick_flared"].copy()
    audit = pd.DataFrame(SOURCE_AUDIT_ROWS)
    halogas_hits = text_contains(
        LITERATURE / "1909.04048_halogas_epg.txt",
        ["NGC 3972", "NGC3972", "3972", "NGC 4088", "NGC4088", "4088"],
    )
    patra_hits = text_contains(
        LITERATURE / "2009.11299_hi_scale_height.txt",
        ["NGC 3972", "NGC3972", "3972", "NGC 4088", "NGC4088", "4088"],
    )
    audit["halogas_text_contains_ngc3972_or_4088"] = any(halogas_hits.values())
    audit["patra_text_contains_ngc3972_or_4088"] = any(patra_hits.values())
    audit["strict_kernel_ready"] = False
    audit["endpoint_scores_computed"] = False
    audit["claim_boundary"] = CLAIM_BOUNDARY
    audit = audit.merge(
        thick[["galaxy", "inclination_deg", "acquisition_priority"]],
        on="galaxy",
        how="left",
        validate="many_to_one",
    )
    summary = (
        audit.groupby(["galaxy"], as_index=False)
        .agg(
            n_source_checks=("source_status", "count"),
            any_direct_profile=("direct_profile_extracted", "any"),
            statuses=("source_status", lambda values: ";".join(values)),
            kernel_relevance=("kernel_relevance", lambda values: ";".join(values)),
        )
    )
    summary["endpoint_scores_allowed"] = False
    summary["claim_boundary"] = CLAIM_BOUNDARY
    return audit, summary


def write_report(audit: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# S4G75 Vertical Source Search Audit",
        "",
        "This audit records targeted vertical/flare source-search evidence for the "
        "thick/flared blockers. It deliberately records negative searches and "
        "general context sources without promoting them to kernel readiness.",
        "",
        "## Verdict",
        "",
        "NGC2683 remains the only row with a direct profile source. NGC3972 and "
        "NGC4088 still need galaxy-specific vertical scale, flare, warp, or "
        "gas-plane-thickness extraction. HALOGAS and Patra 2020 are useful "
        "context for extraplanar/scale-height physics, but they are not direct "
        "NGC3972/NGC4088 kernel inputs in this pass.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source Checks",
        "",
        markdown_table(
            audit[
                [
                    "galaxy",
                    "source_status",
                    "source_authors_year",
                    "source_title",
                    "source_url",
                    "kernel_relevance",
                    "direct_profile_extracted",
                    "endpoint_scores_allowed",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "General HI flaring or EPG literature can justify a future theorem lane, "
        "but it cannot fill a galaxy-specific kernel observable unless the "
        "needed profile/bound is extracted residual-blind for that galaxy.",
        "",
    ]
    (REPORTS / "s4g75_vertical_source_search_audit.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    audit, summary = build_audit()
    audit.to_csv(DATA / "s4g75_vertical_source_search_audit.csv", index=False)
    summary.to_csv(DATA / "s4g75_vertical_source_search_summary.csv", index=False)
    write_report(audit, summary)
    print(f"wrote {DATA / 's4g75_vertical_source_search_audit.csv'}")
    print(f"wrote {DATA / 's4g75_vertical_source_search_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_vertical_source_search_audit.md'}")


if __name__ == "__main__":
    main()
