#!/usr/bin/env python3
"""Audit P0 requested source-family availability.

This is a pre-review availability test for the requested S4G/NED/DustPedia/HI/
PHANGS source families. It records whether a source path is ready, already
partly acquired, or still needs residual-blind external acquisition. It does
not classify morphology and does not compute endpoint scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_requested_source_availability_not_label_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def source_status(
    galaxy: str,
    source_family: str,
    p0_request: pd.Series,
    s4g_candidate: pd.Series | None,
    plan_rows: pd.DataFrame,
) -> tuple[str, str]:
    required = plan_rows["acquisition_priority"].str.startswith("P0_REQUIRED").any()
    if source_family == "S4G":
        if s4g_candidate is not None and s4g_candidate["s4g_match_status"] == "S4G_MATCHED":
            return (
                "PARTIAL_SOURCE_READY",
                "S4G crossmatch and Pipeline 4 disk-scale candidate already acquired; label/audit still pending",
            )
        return "SOURCE_TO_BE_QUERIED", "S4G source path requested but no local crossmatch is available"
    if source_family == "NED_NEDD":
        if str(p0_request.get("ned_url", "")).startswith("https://"):
            return (
                "LOOKUP_READY",
                "NED lookup URL is present for identity/provenance review",
            )
        return "SOURCE_TO_BE_QUERIED", "NED lookup URL missing"
    if source_family == "DustPedia":
        return (
            "SOURCE_TO_BE_QUERIED",
            "DustPedia multiband fallback/validation must be checked residual-blind",
        )
    if source_family == "HI_SURVEYS":
        return (
            "REQUIRED_SOURCE_TO_BE_QUERIED" if required else "SUPPORTING_SOURCE_TO_BE_QUERIED",
            "THINGS/LITTLE_THINGS/WALLABY/HALOGAS availability and gas morphology evidence must be checked",
        )
    if source_family == "PHANGS":
        if galaxy == "NGC0247":
            return (
                "REQUIRED_OPTIONAL_BRANCH_TO_BE_QUERIED",
                "PHANGS/velocity-field support is required for the P0 non-axisymmetric check if available",
            )
        return (
            "SUPPORTING_OPTIONAL_BRANCH_TO_BE_QUERIED",
            "PHANGS is a supporting optional source path for non-axisymmetric evidence",
        )
    return "SOURCE_TO_BE_QUERIED", "Unknown source family in availability audit"


def build_availability() -> pd.DataFrame:
    plan = pd.read_csv(DATA / "p0_missing_data_source_acquisition_plan.csv")
    requests = pd.read_csv(DATA / "p0_external_imaging_request_manifest.csv")
    s4g = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    source_families = pd.read_csv(DATA / "p0_missing_data_source_acquisition_summary.csv")
    s4g_by_galaxy = {
        row["galaxy"]: row for _, row in s4g.iterrows() if row["galaxy"] in set(plan["galaxy"])
    }
    rows = []
    for _, request in requests.iterrows():
        galaxy = request["galaxy"]
        for source_family in source_families["source_family"]:
            source_plan = plan[
                (plan["galaxy"] == galaxy)
                & plan["required_source_families"].str.contains(source_family, regex=False)
            ]
            if source_plan.empty:
                continue
            status, evidence = source_status(
                galaxy,
                source_family,
                request,
                s4g_by_galaxy.get(galaxy),
                source_plan,
            )
            rows.append(
                {
                    "galaxy": galaxy,
                    "source_family": source_family,
                    "n_plan_tasks": int(len(source_plan)),
                    "n_required_plan_tasks": int(
                        source_plan["acquisition_priority"]
                        .str.startswith("P0_REQUIRED")
                        .sum()
                    ),
                    "availability_status": status,
                    "availability_evidence": evidence,
                    "accepted_label_output_allowed": False,
                    "endpoint_scores_allowed": False,
                    "endpoint_scores_computed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def build_summary(availability: pd.DataFrame) -> pd.DataFrame:
    return (
        availability.groupby("source_family", as_index=False)
        .agg(
            n_p0_galaxies=("galaxy", "nunique"),
            n_source_family_rows=("galaxy", "count"),
            n_partial_source_ready=("availability_status", lambda s: int((s == "PARTIAL_SOURCE_READY").sum())),
            n_lookup_ready=("availability_status", lambda s: int((s == "LOOKUP_READY").sum())),
            n_to_be_queried=(
                "availability_status",
                lambda s: int(s.astype(str).str.contains("TO_BE_QUERIED").sum()),
            ),
            endpoint_scores_computed=("endpoint_scores_computed", "any"),
        )
        .assign(
            accepted_label_output_allowed=False,
            claim_boundary=CLAIM_BOUNDARY,
        )
    )


def write_report(availability: pd.DataFrame, summary: pd.DataFrame) -> None:
    blockers = availability[
        availability["availability_status"].astype(str).str.contains("TO_BE_QUERIED")
    ]
    lines = [
        "# P0 Requested Source-Family Availability Audit",
        "",
        "This audit tests the P0 source-acquisition plan against currently available",
        "source paths. It is an availability preflight only: it does not classify",
        "galaxies, does not create accepted morphology labels, and does not compute",
        "endpoint scores.",
        "",
        "## Verdict",
        "",
        f"P0 source-family rows: {len(availability)}.",
        f"Rows still requiring residual-blind external acquisition: {len(blockers)}.",
        "",
        "S4G is partially source-ready for the P0 galaxies through existing",
        "crossmatches and disk-scale candidates. NED/NED-D lookup paths are ready.",
        "DustPedia, HI surveys, and PHANGS remain residual-blind acquisition tasks",
        "rather than accepted morphology evidence.",
        "",
        "## Source Summary",
        "",
        markdown_table(summary),
        "",
        "## Availability Rows",
        "",
        markdown_table(
            availability[
                [
                    "galaxy",
                    "source_family",
                    "n_required_plan_tasks",
                    "availability_status",
                    "availability_evidence",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This is not an accepted morphology manifest and not an endpoint score. It",
        "only tells the review pipeline where source evidence is already partly",
        "available and where residual-blind acquisition is still needed.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_requested_source_family_availability.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    availability = build_availability()
    summary = build_summary(availability)
    availability.to_csv(DATA / "p0_requested_source_family_availability.csv", index=False)
    summary.to_csv(DATA / "p0_requested_source_family_availability_summary.csv", index=False)
    write_report(availability, summary)
    print("PAPER8_P0_REQUESTED_SOURCE_FAMILY_AVAILABILITY_COMPLETE")


if __name__ == "__main__":
    main()
