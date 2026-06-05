#!/usr/bin/env python3
"""Record literature source hits for S4G75 remaining kernel blockers.

This pass is a residual-blind literature/source acquisition layer.  It records
candidate papers and whether they provide a direct kernel observable, a direct
profile that still needs mapping into the executable shell, or only contextual
support for a future theorem/extraction step.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_literature_kernel_source_hits_not_endpoint"


SOURCE_HITS = {
    "NGC2683": {
        "literature_status": "DIRECT_LITERATURE_FLARE_PROFILE_READY_MAPPING_REQUIRED",
        "source_title": "The flaring HI disk of the nearby spiral galaxy NGC 2683",
        "source_authors_year": "Vollmer, Nehlig & Ibata 2016",
        "source_url": "https://arxiv.org/abs/1512.07058",
        "direct_kernel_evidence": (
            "Best-fit HI model includes thin disk inclined by about 80 deg, "
            "inclination warp, and exponential flare."
        ),
        "extracted_profile": (
            "flare height H=FWHM/2 rises from 0.5 kpc at R=9 kpc to 4 kpc "
            "at R=15 kpc, remains constant to R=22 kpc, then decreases; "
            "outer low-surface-density ring has vertical offset 1.3 kpc"
        ),
        "numeric_kernel_fields": "flare_H_start_kpc=0.5; flare_R_start_kpc=9; flare_H_max_kpc=4; flare_R_max_kpc=15; flare_R_saturation_end_kpc=22; ring_vertical_offset_kpc=1.3",
        "endpoint_mapping_status": "MAPPING_REQUIRED_PROFILE_TO_THICK_FLARED_EXECUTABLE_KERNEL",
        "promotion_interpretation": (
            "direct vertical/flare source evidence exists, but the current "
            "executable endpoint uses a scalar h/Rs proxy; do not override "
            "endpoint fields until a residual-blind profile-to-kernel mapping "
            "is implemented"
        ),
    },
    "NGC4214": {
        "literature_status": "HI_WARP_PROFILE_CONTEXT_READY_TRANSITION_RADIUS_NOT_EXTRACTED",
        "source_title": "Dynamics of Starbursting Dwarf Galaxies. III. A HI study of 18 nearby objects",
        "source_authors_year": "Lelli, Verheijen & Fraternali 2014",
        "source_url": "https://arxiv.org/abs/1404.6252",
        "direct_kernel_evidence": "HI study includes resolved kinematic/morphological context for NGC4214.",
        "extracted_profile": "no machine-extracted tail transition radius in this pass",
        "numeric_kernel_fields": "",
        "endpoint_mapping_status": "DIRECT_TRANSITION_EXTRACTION_REQUIRED",
        "promotion_interpretation": (
            "source is relevant for HI/warp morphology, but no direct "
            "tail inner/cutoff transition radius has been extracted"
        ),
    },
    "UGC06917": {
        "literature_status": "HI_ATLAS_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION",
        "source_title": "The Ursa Major Cluster of Galaxies. IV: HI synthesis observations",
        "source_authors_year": "Verheijen & Sancisi 2001",
        "source_url": "https://arxiv.org/abs/astro-ph/0101404",
        "direct_kernel_evidence": (
            "paper reports an HI atlas with radial HI surface density profiles, "
            "channel maps, velocity fields, and rotation curves"
        ),
        "extracted_profile": "no galaxy-specific transition radius parsed in this pass",
        "numeric_kernel_fields": "",
        "endpoint_mapping_status": "ATLAS_PROFILE_EXTRACTION_REQUIRED",
        "promotion_interpretation": (
            "candidate direct profile source exists, but the transition/break "
            "radius must be extracted residual-blind before promotion"
        ),
    },
    "UGC06983": {
        "literature_status": "HI_ATLAS_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION",
        "source_title": "The Ursa Major Cluster of Galaxies. IV: HI synthesis observations",
        "source_authors_year": "Verheijen & Sancisi 2001",
        "source_url": "https://arxiv.org/abs/astro-ph/0101404",
        "direct_kernel_evidence": (
            "paper reports an HI atlas with radial HI surface density profiles, "
            "channel maps, velocity fields, and rotation curves"
        ),
        "extracted_profile": "no galaxy-specific transition radius parsed in this pass",
        "numeric_kernel_fields": "",
        "endpoint_mapping_status": "ATLAS_PROFILE_EXTRACTION_REQUIRED",
        "promotion_interpretation": (
            "candidate direct profile source exists, but the transition/break "
            "radius must be extracted residual-blind before promotion"
        ),
    },
    "UGC00891": {
        "literature_status": "HI_ROTATION_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION",
        "source_title": "van Zee et al. 1997 / SPARC vZ97 reference family",
        "source_authors_year": "van Zee et al. 1997",
        "source_url": "https://adsabs.harvard.edu/pdf/1997AJ....113.1638V",
        "direct_kernel_evidence": "candidate HI/rotation-profile source family cited by SPARC",
        "extracted_profile": "no direct tail transition radius parsed in this pass",
        "numeric_kernel_fields": "",
        "endpoint_mapping_status": "PROFILE_EXTRACTION_REQUIRED",
        "promotion_interpretation": (
            "source family remains a candidate until the needed outer transition "
            "radius is extracted from the source-native profile"
        ),
    },
    "UGC04499": {
        "literature_status": "HI_ROTATION_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION",
        "source_title": "The rotation curves shapes of late-type dwarf galaxies",
        "source_authors_year": "Swaters et al. 2009",
        "source_url": "https://arxiv.org/abs/0901.4222",
        "direct_kernel_evidence": "rotation-curve/HI source family cited by SPARC Sw09/Sw02 fields",
        "extracted_profile": "no direct tail transition radius parsed in this pass",
        "numeric_kernel_fields": "",
        "endpoint_mapping_status": "PROFILE_EXTRACTION_REQUIRED",
        "promotion_interpretation": (
            "source family remains a candidate until the needed outer transition "
            "radius is extracted from the source-native profile"
        ),
    },
    "UGC05829": {
        "literature_status": "HI_ROTATION_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION",
        "source_title": "The rotation curves shapes of late-type dwarf galaxies",
        "source_authors_year": "Swaters et al. 2009",
        "source_url": "https://arxiv.org/abs/0901.4222",
        "direct_kernel_evidence": "rotation-curve/HI source family cited by SPARC Sw09/Sw02 fields",
        "extracted_profile": "no direct tail transition radius parsed in this pass",
        "numeric_kernel_fields": "",
        "endpoint_mapping_status": "PROFILE_EXTRACTION_REQUIRED",
        "promotion_interpretation": (
            "source family remains a candidate until the needed outer transition "
            "radius is extracted from the source-native profile"
        ),
    },
}


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


def build_hits() -> tuple[pd.DataFrame, pd.DataFrame]:
    ledger = pd.read_csv(DATA / "s4g75_remaining_kernel_acquisition_ledger.csv")
    rows = []
    for _, row in ledger.iterrows():
        hit = SOURCE_HITS.get(
            row["galaxy"],
            {
                "literature_status": "NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS",
                "source_title": "",
                "source_authors_year": "",
                "source_url": "",
                "direct_kernel_evidence": "",
                "extracted_profile": "",
                "numeric_kernel_fields": "",
                "endpoint_mapping_status": "SOURCE_SEARCH_STILL_REQUIRED",
                "promotion_interpretation": "no targeted source hit recorded in this pass",
            },
        )
        rows.append(
            {
                "galaxy": row["galaxy"],
                "formula_family": row["formula_family"],
                "blocker_class": row["blocker_class"],
                "acquisition_priority": row["acquisition_priority"],
                "primary_acquisition_lane": row["primary_acquisition_lane"],
                **hit,
                "strict_kernel_ready": False,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    hits = pd.DataFrame(rows)
    summary = (
        hits.groupby(["blocker_class", "literature_status", "endpoint_mapping_status"], as_index=False)
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
        )
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY
    return hits, summary


def write_report(hits: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# S4G75 Literature Kernel Source Hits",
        "",
        "This report records targeted literature/source hits for the remaining "
        "S4G75 kernel blockers. It is source acquisition only: no accepted label "
        "is created and no endpoint score is computed.",
        "",
        "## Verdict",
        "",
        "One strong direct vertical-profile source is recorded for NGC2683, but it "
        "requires a residual-blind mapping from a flare profile into the current "
        "thick/flared executable kernel. Several scale-tail rows have candidate "
        "HI atlas/profile source families, but no direct transition radius is "
        "extracted in this pass.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Galaxy-Level Hits",
        "",
        markdown_table(
            hits[
                [
                    "galaxy",
                    "formula_family",
                    "blocker_class",
                    "literature_status",
                    "source_authors_year",
                    "source_title",
                    "source_url",
                    "extracted_profile",
                    "endpoint_mapping_status",
                    "promotion_interpretation",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "A literature source hit is not endpoint eligibility. NGC2683 is a direct "
        "profile candidate, not a scalar h/Rs override. Tail-source hits remain "
        "profile-extraction tasks until a residual-blind transition radius is "
        "measured or a Tau-side promotion theorem is accepted.",
        "",
    ]
    (REPORTS / "s4g75_literature_kernel_source_hits.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    hits, summary = build_hits()
    hits.to_csv(DATA / "s4g75_literature_kernel_source_hits.csv", index=False)
    summary.to_csv(DATA / "s4g75_literature_kernel_source_hit_summary.csv", index=False)
    write_report(hits, summary)
    print(f"wrote {DATA / 's4g75_literature_kernel_source_hits.csv'}")
    print(f"wrote {DATA / 's4g75_literature_kernel_source_hit_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_literature_kernel_source_hits.md'}")


if __name__ == "__main__":
    main()
