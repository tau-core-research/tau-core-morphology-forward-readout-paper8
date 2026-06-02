#!/usr/bin/env python3
"""Build the accepted-source upgrade plan for morphology observables."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


UPGRADE_SPEC = {
    "formula_family": {
        "upgrade_priority": "P0",
        "accepted_source_class": "residual-blind image/decomposition morphology classification",
        "extraction_rule": "assign one predeclared Tau Core family before endpoint scoring",
        "leak_guard": "no vobs residuals, required_S_tau, or best-fit formula choice",
        "promotion_gate": "family label documented with source and pre-scoring timestamp",
    },
    "manifest_confidence": {
        "upgrade_priority": "P0",
        "accepted_source_class": "pre-scoring morphology-observable quality rubric",
        "extraction_rule": "score confidence from source quality and feature clarity only",
        "leak_guard": "no endpoint performance or baseline comparison input",
        "promotion_gate": "thresholds frozen before the endpoint run",
    },
    "manifest_caveat": {
        "upgrade_priority": "P0",
        "accepted_source_class": "geometry/catalog/source-quality caveat log",
        "extraction_rule": "record low inclination, distance uncertainty, weak feature, or none",
        "leak_guard": "no caveat added because the model scored poorly",
        "promotion_gate": "caveated rows preserved in support/control outputs",
    },
    "scale_radius_kpc": {
        "upgrade_priority": "P1",
        "accepted_source_class": "light-profile or morphology decomposition scale length",
        "extraction_rule": "use pre-scoring disk scale/support length with units and uncertainty",
        "leak_guard": "no radius chosen from residual shape or endpoint score",
        "promotion_gate": "positive physical scale with provenance",
    },
    "tail_inner_radius_kpc": {
        "upgrade_priority": "P1",
        "accepted_source_class": "outer-disk morphology transition feature",
        "extraction_rule": "measure transition radius before applying the readout formula",
        "leak_guard": "no radius chosen to minimize velocity residuals",
        "promotion_gate": "positive and not larger than tail_cutoff_radius_kpc",
    },
    "tail_cutoff_radius_kpc": {
        "upgrade_priority": "P1",
        "accepted_source_class": "outer disk/tail extent morphology observable",
        "extraction_rule": "measure tail support/cutoff before endpoint scoring",
        "leak_guard": "no endpoint-selected truncation radius",
        "promotion_gate": "positive and not smaller than tail_inner_radius_kpc",
    },
    "compact_support_radius_kpc": {
        "upgrade_priority": "P1",
        "accepted_source_class": "compact-source morphology support radius",
        "extraction_rule": "measure compact support from residual-blind source morphology",
        "leak_guard": "no support radius chosen from residual improvement",
        "promotion_gate": "positive support radius with provenance",
    },
    "thickness_h_over_rs": {
        "upgrade_priority": "P1",
        "accepted_source_class": "vertical thickness/flaring observable or documented proxy",
        "extraction_rule": "record dimensionless thickness ratio and uncertainty/caveat",
        "leak_guard": "no damping factor tuned to endpoint residuals",
        "promotion_gate": "positive ratio with source and caveat status",
    },
    "observable_provenance": {
        "upgrade_priority": "P0",
        "accepted_source_class": "dataset, method, and pre-scoring timestamp ledger",
        "extraction_rule": "document every family label and kernel observable source",
        "leak_guard": "no undocumented manual adjustment",
        "promotion_gate": "all rows have auditable residual-blind provenance",
    },
    "ring_radius_kpc": {
        "upgrade_priority": "P2",
        "accepted_source_class": "external ring/resonance morphology measurement",
        "extraction_rule": "include only if ring family enters a predeclared endpoint lane",
        "leak_guard": "no residual-peak-selected ring radius",
        "promotion_gate": "ring branch remains caveated until source-native fields exist",
    },
    "bar_m2_strength": {
        "upgrade_priority": "P2_velocity_field",
        "accepted_source_class": "image or velocity-field m=2 morphology observable",
        "extraction_rule": "promote only in a velocity-field/full-morphology branch",
        "leak_guard": "no 1D residual asymmetry fit",
        "promotion_gate": "not promoted from 1D SPARC curves alone",
    },
    "lopsided_m1_strength": {
        "upgrade_priority": "P2_velocity_field",
        "accepted_source_class": "image or velocity-field m=1 asymmetry observable",
        "extraction_rule": "promote only in a velocity-field/full-morphology branch",
        "leak_guard": "no 1D residual asymmetry fit",
        "promotion_gate": "not promoted from 1D SPARC curves alone",
    },
}


BATCH_ROWS = [
    {
        "batch": "B0_protocol_lock",
        "purpose": "freeze endpoint lanes, amplitude policy, forbidden inputs, and source intake schema",
        "fields": "all protocol fields",
        "entry_condition": "current package reproduced",
        "exit_condition": "source collection begins without changing endpoint gates",
    },
    {
        "batch": "B1_core_labels_and_quality",
        "purpose": "replace proxy family labels, confidence, caveats, and provenance",
        "fields": "formula_family; manifest_confidence; manifest_caveat; observable_provenance",
        "entry_condition": "source catalogs/images chosen before scoring",
        "exit_condition": "every row has residual-blind family label and provenance",
    },
    {
        "batch": "B2_active_family_kernel_observables",
        "purpose": "replace proxy kernel-driving fields for active 1D SPARC morphology families",
        "fields": "scale_radius_kpc; tail_inner_radius_kpc; tail_cutoff_radius_kpc; compact_support_radius_kpc; thickness_h_over_rs",
        "entry_condition": "B1 complete",
        "exit_condition": "all active-family required fields accepted or row explicitly caveated",
    },
    {
        "batch": "B3_optional_non_axisymmetric_extension",
        "purpose": "prepare ring, bar, and lopsided branches without promoting them from 1D residuals",
        "fields": "ring_radius_kpc; bar_m2_strength; lopsided_m1_strength",
        "entry_condition": "external morphology or velocity-field support exists",
        "exit_condition": "non-axisymmetric branch declared as separate endpoint or kept caveated",
    },
    {
        "batch": "B4_blind_endpoint_run",
        "purpose": "run the frozen matched-vs-wrong family endpoint on accepted observables",
        "fields": "all promoted fields",
        "entry_condition": "B1 and B2 complete with no missing required accepted fields",
        "exit_condition": "matched/wrong, shuffled-K, Newtonian, MOND, RAR, and TGP comparisons reported",
    },
]


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def build_plan(gap: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, item in gap.iterrows():
        field = item["field"]
        if field not in UPGRADE_SPEC:
            continue
        spec = UPGRADE_SPEC[field]
        if item["availability_status"] == "accepted_available":
            endpoint_role = "already usable as pre-scoring catalog/geometry input"
        elif item["availability_status"] == "not_in_current_family_set":
            endpoint_role = "optional branch; keep out of current primary 1D endpoint"
        else:
            endpoint_role = "must be upgraded before discovery-style endpoint claim"
        rows.append(
            {
                "field": field,
                "current_availability_status": item["availability_status"],
                "current_manifest_source_field": item["manifest_source_field"],
                "upgrade_priority": spec["upgrade_priority"],
                "accepted_source_class": spec["accepted_source_class"],
                "extraction_rule": spec["extraction_rule"],
                "leak_guard": spec["leak_guard"],
                "promotion_gate": spec["promotion_gate"],
                "endpoint_role": endpoint_role,
            }
        )
    return pd.DataFrame(rows)


def write_report(plan: pd.DataFrame, batches: pd.DataFrame) -> None:
    active = plan[
        plan["endpoint_role"].str.contains("must be upgraded", regex=False)
    ]
    p0 = int((active["upgrade_priority"] == "P0").sum())
    p1 = int((active["upgrade_priority"] == "P1").sum())
    lines = [
        "# Morphology Observable Source Upgrade Plan",
        "",
        "This plan converts the gap audit into a residual-blind source collection",
        "protocol. It is not a data source claim, not an endpoint score, and not",
        "an empirical validation result.",
        "",
        "## Verdict",
        "",
        "The next Paper 8 upgrade is source replacement, not endpoint redesign.",
        "The active proxy manifest needs accepted morphology sources for the",
        f"P0 bookkeeping/label fields ({p0} fields) and P1 active-family kernel",
        f"observables ({p1} fields). Optional ring, bar, and lopsided branches",
        "should stay caveated unless external morphology or velocity-field support",
        "is added before scoring.",
        "",
        "## Field Upgrade Plan",
        "",
        markdown_table(plan),
        "",
        "## Collection Batches",
        "",
        markdown_table(batches),
        "",
        "## Claim Boundary",
        "",
        "Completing this plan would still not by itself prove Tau Core.",
        "",
        "Completing this plan would make the endpoint auditable; it would still not",
        "by itself prove Tau Core or guarantee a baseline win. The empirical claim",
        "can only be assessed after the frozen protocol is rerun on the accepted",
        "observables.",
    ]
    (REPORTS / "morphology_observable_source_upgrade_plan.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    gap = pd.read_csv(DATA / "morphology_observable_gap_audit.csv")
    plan = build_plan(gap)
    batches = pd.DataFrame(BATCH_ROWS)
    plan.to_csv(DATA / "morphology_observable_source_upgrade_plan.csv", index=False)
    batches.to_csv(DATA / "morphology_observable_collection_batches.csv", index=False)
    write_report(plan, batches)
    print("PAPER8_MORPHOLOGY_OBSERVABLE_SOURCE_UPGRADE_PLAN_COMPLETE")


if __name__ == "__main__":
    main()
