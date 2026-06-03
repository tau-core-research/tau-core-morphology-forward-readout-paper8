#!/usr/bin/env python3
"""Build a P0 missing-data source acquisition plan.

This plan maps the still-empty P0 residual-blind review fields to the external
source families requested for Paper 8: S4G, NED/NED-D, DustPedia, HI surveys,
and PHANGS. It does not create accepted labels and does not compute endpoint
scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_missing_data_source_plan_not_label_not_endpoint"

SOURCE_URLS = {
    "S4G": "https://irsa.ipac.caltech.edu/data/SPITZER/S4G/overview.html",
    "NED_NEDD": "https://ned.ipac.caltech.edu/",
    "DustPedia": "https://arxiv.org/abs/1708.05335",
    "HI_SURVEYS": "THINGS; LITTLE_THINGS; WALLABY; HALOGAS",
    "PHANGS": "https://www.phangs.org/home/data",
}

FIELD_PLAN = {
    "present_day_morphology_label": {
        "required_source_families": "S4G;NED_NEDD;DustPedia",
        "source_task": "record residual-blind catalog/image morphology support and provenance",
        "promotion_use": "candidate accepted family-label evidence after independent audit",
    },
    "outer_disk_lsb_tail_evidence": {
        "required_source_families": "S4G;DustPedia;HI_SURVEYS",
        "source_task": "check outer-disk, low-surface-brightness, truncation, tail, and gas-extent support",
        "promotion_use": "scale-tail versus exponential/compact family caveat evidence",
    },
    "hi_extent_or_asymmetry_evidence": {
        "required_source_families": "HI_SURVEYS;NED_NEDD",
        "source_task": "look for THINGS/LITTLE_THINGS/WALLABY/HALOGAS availability and record gas extent or asymmetry evidence",
        "promotion_use": "history/memory, lopsidedness, warp, and outer-disk support",
    },
    "bar_m2_evidence": {
        "required_source_families": "S4G;PHANGS",
        "source_task": "record bar component, m=2 morphology, and velocity-field support where available",
        "promotion_use": "optional barred-spiral branch support, especially for NGC0247",
    },
    "edge_projection_caveat": {
        "required_source_families": "NED_NEDD;S4G;DustPedia",
        "source_task": "record inclination, distance/projection caveats, and edge-on decomposition support",
        "promotion_use": "projection caveat and possible thick/flared or memory/history review flag",
    },
    "vertical_flare_warp_evidence": {
        "required_source_families": "S4G;DustPedia;HI_SURVEYS",
        "source_task": "look for edge/thick disk, flare, warp, or extended gas-plane evidence",
        "promotion_use": "thick/flared or projection-sensitive family support",
    },
    "compact_bulge_evidence": {
        "required_source_families": "S4G;DustPedia;NED_NEDD",
        "source_task": "record bulge/compact support and central concentration provenance",
        "promotion_use": "compact finite-source branch caveat/support",
    },
    "ring_resonance_evidence": {
        "required_source_families": "S4G;PHANGS;DustPedia",
        "source_task": "record ring, resonance, or spiral-structure evidence without using residual peaks",
        "promotion_use": "optional ring/resonance branch support",
    },
    "morphological_memory_history_proxy_judgment": {
        "required_source_families": "S4G;DustPedia;HI_SURVEYS;PHANGS",
        "source_task": "combine residual-blind current morphology, gas asymmetry, warp/tail, and velocity-field evidence",
        "promotion_use": "history/memory proxy only; not a recovered historical morphology",
    },
    "review_confidence": {
        "required_source_families": "S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS",
        "source_task": "score source agreement, source coverage, and caveat severity before endpoint scoring",
        "promotion_use": "confidence gate input for later accepted-manifest audit",
    },
    "residual_blind_family_recommendation": {
        "required_source_families": "S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS",
        "source_task": "make a residual-blind family recommendation only after source evidence is logged",
        "promotion_use": "candidate label for independent accepted-manifest audit",
    },
    "review_sources_used": {
        "required_source_families": "S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS",
        "source_task": "record exact source list, access path, and notes",
        "promotion_use": "mandatory provenance field",
    },
    "review_notes": {
        "required_source_families": "S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS",
        "source_task": "record residual-blind caveats and unresolved data gaps",
        "promotion_use": "audit notes; cannot override missing required evidence",
    },
}


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def task_priority(galaxy: str, field: str, inspection_focus: str) -> str:
    if field in {
        "present_day_morphology_label",
        "residual_blind_family_recommendation",
        "review_confidence",
        "review_sources_used",
    }:
        return "P0_REQUIRED"
    if field in {"outer_disk_lsb_tail_evidence", "hi_extent_or_asymmetry_evidence"}:
        return "P0_REQUIRED"
    if galaxy == "NGC0247" and field in {"bar_m2_evidence", "ring_resonance_evidence"}:
        return "P0_REQUIRED_NONAXISYMMETRIC_CHECK"
    if galaxy == "NGC0100" and field == "edge_projection_caveat":
        return "P0_REQUIRED_PROJECTION_CHECK"
    if "edge_on_projection_degeneracy" in inspection_focus and field in {
        "vertical_flare_warp_evidence",
        "edge_projection_caveat",
    }:
        return "P0_REQUIRED_PROJECTION_CHECK"
    return "P0_SUPPORTING"


def build_plan() -> pd.DataFrame:
    template = pd.read_csv(DATA / "p0_visual_review_template.csv")
    rows = []
    for _, item in template.iterrows():
        galaxy = item["galaxy"]
        for field, spec in FIELD_PLAN.items():
            rows.append(
                {
                    "galaxy": galaxy,
                    "review_field": field,
                    "acquisition_priority": task_priority(
                        galaxy, field, item["inspection_focus"]
                    ),
                    "required_source_families": spec["required_source_families"],
                    "source_urls_or_catalogs": "; ".join(
                        SOURCE_URLS[source]
                        for source in spec["required_source_families"].split(";")
                    ),
                    "source_task": spec["source_task"],
                    "promotion_use": spec["promotion_use"],
                    "current_field_status": item[field],
                    "source_acquisition_status": "TO_BE_ACQUIRED_RESIDUAL_BLIND",
                    "accepted_label_output_allowed": False,
                    "endpoint_scores_allowed": False,
                    "endpoint_scores_computed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def build_source_summary(plan: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for source in SOURCE_URLS:
        mask = plan["required_source_families"].str.contains(source, regex=False)
        rows.append(
            {
                "source_family": source,
                "url_or_catalog": SOURCE_URLS[source],
                "n_p0_tasks": int(mask.sum()),
                "n_p0_galaxies": int(plan.loc[mask, "galaxy"].nunique()),
                "source_acquisition_status": "TO_BE_ACQUIRED_RESIDUAL_BLIND",
                "accepted_label_output_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_galaxy_summary(plan: pd.DataFrame) -> pd.DataFrame:
    grouped = plan.groupby("galaxy", as_index=False).agg(
        n_source_tasks=("review_field", "count"),
        n_required_tasks=(
            "acquisition_priority",
            lambda s: int(sum(str(value).startswith("P0_REQUIRED") for value in s)),
        ),
        n_pending_tasks=("source_acquisition_status", lambda s: int((s == "TO_BE_ACQUIRED_RESIDUAL_BLIND").sum())),
    )
    grouped["accepted_label_output_allowed"] = False
    grouped["endpoint_scores_computed"] = False
    grouped["claim_boundary"] = CLAIM_BOUNDARY
    return grouped


def write_report(
    plan: pd.DataFrame, source_summary: pd.DataFrame, galaxy_summary: pd.DataFrame
) -> None:
    required = plan[plan["acquisition_priority"].str.startswith("P0_REQUIRED")]
    lines = [
        "# P0 Missing-Data Source Acquisition Plan",
        "",
        "This report operationalizes the requested source policy for the Paper 8",
        "P0 review lane: use S4G, NED/NED-D, DustPedia, HI survey data, and PHANGS",
        "where appropriate. It is a source-acquisition plan only, not an accepted morphology manifest and not an endpoint score.",
        "",
        "## Verdict",
        "",
        f"P0 galaxies covered: {plan['galaxy'].nunique()}.",
        f"Residual-blind source tasks: {len(plan)}.",
        f"Required P0 source tasks: {len(required)}.",
        "",
        "All tasks remain `TO_BE_ACQUIRED_RESIDUAL_BLIND`; no accepted label is",
        "created and no Tau/MOND/RAR/TGP/Newtonian endpoint comparison is run.",
        "",
        "## Source Family Summary",
        "",
        markdown_table(source_summary),
        "",
        "## Galaxy Summary",
        "",
        markdown_table(galaxy_summary),
        "",
        "## Required Task Extract",
        "",
        markdown_table(
            required[
                [
                    "galaxy",
                    "review_field",
                    "acquisition_priority",
                    "required_source_families",
                    "source_task",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This layer is upstream of the accepted-manifest audit. It must not use",
        "endpoint residual gain, required-S_tau diagnostics, best-fit Tau Core",
        "readout families, MOND/RAR/TGP comparison scores, or post-hoc family",
        "switching. Successful source acquisition would still require independent",
        "promotion and readiness gates before any endpoint scoring.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_missing_data_source_acquisition_plan.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    plan = build_plan()
    source_summary = build_source_summary(plan)
    galaxy_summary = build_galaxy_summary(plan)
    plan.to_csv(DATA / "p0_missing_data_source_acquisition_plan.csv", index=False)
    source_summary.to_csv(
        DATA / "p0_missing_data_source_acquisition_summary.csv", index=False
    )
    galaxy_summary.to_csv(
        DATA / "p0_missing_data_source_acquisition_by_galaxy.csv", index=False
    )
    write_report(plan, source_summary, galaxy_summary)
    print("PAPER8_P0_MISSING_DATA_SOURCE_ACQUISITION_PLAN_COMPLETE")


if __name__ == "__main__":
    main()
