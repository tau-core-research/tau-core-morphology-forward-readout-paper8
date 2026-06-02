#!/usr/bin/env python3
"""Build the external source registry and SPARC crossmatch template."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


SOURCE_ROWS = [
    {
        "source_id": "SPARC",
        "priority": "sample_and_baseline",
        "url": "https://astronomy.case.edu/2016/08/26/sparc-galaxy-database/",
        "use_for_fields": "galaxy; inclination_deg; distance_frac_error; baryonic baseline; rotation curve",
        "not_accepted_for_fields": "formula_family; kernel morphology parameters",
        "residual_blind_role": "endpoint sample and baryonic/rotation baseline, not final morphology source",
        "coverage_expectation": "full 175-galaxy sample",
    },
    {
        "source_id": "S4G",
        "priority": "primary_morphology_decomposition",
        "url": "https://irsa.ipac.caltech.edu/data/SPITZER/S4G/overview.html",
        "use_for_fields": "formula_family; scale_radius_kpc; compact_support_radius_kpc; ring_radius_kpc; bar_m2_strength; observable_provenance",
        "not_accepted_for_fields": "rotation residual endpoints",
        "residual_blind_role": "primary 3.6 micron morphology/decomposition source where crossmatch exists",
        "coverage_expectation": "partial SPARC overlap; must be measured",
    },
    {
        "source_id": "NED_NEDD",
        "priority": "identity_distance_provenance",
        "url": "https://ned.ipac.caltech.edu/",
        "use_for_fields": "galaxy identity; aliases; distance provenance; observable_provenance",
        "not_accepted_for_fields": "endpoint-selected morphology family",
        "residual_blind_role": "crossmatch/provenance and distance consistency layer",
        "coverage_expectation": "broad coverage; quality varies by object",
    },
    {
        "source_id": "DustPedia",
        "priority": "fallback_multiband_morphology",
        "url": "https://arxiv.org/abs/1708.05335",
        "use_for_fields": "scale_radius_kpc; compact_support_radius_kpc; tail_cutoff_radius_kpc; observable_provenance",
        "not_accepted_for_fields": "velocity-field-only asymmetry claims",
        "residual_blind_role": "fallback and independent multiband morphology/source validation",
        "coverage_expectation": "partial SPARC overlap; must be measured",
    },
    {
        "source_id": "PHANGS",
        "priority": "optional_velocity_field_morphology",
        "url": "https://www.phangs.org/home/data",
        "use_for_fields": "bar_m2_strength; lopsided_m1_strength; ring_radius_kpc; non-axisymmetric caveat support",
        "not_accepted_for_fields": "full 1D SPARC primary endpoint coverage",
        "residual_blind_role": "optional high-quality branch for bars, rings, asymmetry, and velocity-field support",
        "coverage_expectation": "small high-quality overlap; not primary full-sample source",
    },
]


FIELD_SOURCE_ROWS = [
    {
        "field": "formula_family",
        "primary_source": "S4G",
        "secondary_source": "DustPedia; NED_NEDD morphology references",
        "fallback_policy": "leave row diagnostic-only if residual-blind family assignment is ambiguous",
        "acceptance_check": "family assigned before endpoint scoring with source provenance",
    },
    {
        "field": "manifest_confidence",
        "primary_source": "source-quality rubric over S4G/NED/DustPedia evidence",
        "secondary_source": "manual pre-scoring morphology audit log",
        "fallback_policy": "low confidence rows remain in caveated/support outputs",
        "acceptance_check": "confidence threshold frozen before endpoint scoring",
    },
    {
        "field": "manifest_caveat",
        "primary_source": "geometry/catalog/source-quality caveat log",
        "secondary_source": "NED_NEDD distance and inclination provenance",
        "fallback_policy": "caveat rather than drop unless predeclared exclusion applies",
        "acceptance_check": "no caveat is based on bad endpoint residual performance",
    },
    {
        "field": "scale_radius_kpc",
        "primary_source": "S4G",
        "secondary_source": "DustPedia",
        "fallback_policy": "block active-family endpoint row if no accepted scale exists",
        "acceptance_check": "positive physical scale, residual-blind method, provenance recorded",
    },
    {
        "field": "tail_inner_radius_kpc",
        "primary_source": "S4G profile/decomposition or morphology feature log",
        "secondary_source": "DustPedia outer-disk morphology",
        "fallback_policy": "scale-tail row remains diagnostic-only if transition is not source-defined",
        "acceptance_check": "positive and <= tail_cutoff_radius_kpc; not chosen from residuals",
    },
    {
        "field": "tail_cutoff_radius_kpc",
        "primary_source": "S4G outer-disk extent or DustPedia support radius",
        "secondary_source": "NED/DustPedia size provenance",
        "fallback_policy": "scale-tail row remains diagnostic-only if support is not source-defined",
        "acceptance_check": "positive and >= tail_inner_radius_kpc; not endpoint-selected",
    },
    {
        "field": "compact_support_radius_kpc",
        "primary_source": "S4G decomposition",
        "secondary_source": "DustPedia compact-source morphology",
        "fallback_policy": "compact row remains proxy-level if no compact support source exists",
        "acceptance_check": "positive support radius with residual-blind provenance",
    },
    {
        "field": "thickness_h_over_rs",
        "primary_source": "external vertical/thickness estimate or documented morphology proxy",
        "secondary_source": "source-quality caveat if no direct thickness observable exists",
        "fallback_policy": "thick/flared row is caveated unless thickness proxy is predeclared",
        "acceptance_check": "positive dimensionless ratio; not endpoint-tuned damping",
    },
    {
        "field": "ring_radius_kpc",
        "primary_source": "S4G or PHANGS ring/resonance morphology",
        "secondary_source": "DustPedia/NED morphology notes",
        "fallback_policy": "optional branch only; no primary 1D endpoint promotion",
        "acceptance_check": "not selected from residual peak location",
    },
    {
        "field": "bar_m2_strength",
        "primary_source": "PHANGS or S4G bar morphology",
        "secondary_source": "image morphology caveat only",
        "fallback_policy": "velocity-field/full-morphology branch only",
        "acceptance_check": "not inferred from 1D residual asymmetry",
    },
    {
        "field": "lopsided_m1_strength",
        "primary_source": "PHANGS or external asymmetry morphology",
        "secondary_source": "image morphology caveat only",
        "fallback_policy": "velocity-field/full-morphology branch only",
        "acceptance_check": "not inferred from 1D residual asymmetry",
    },
    {
        "field": "observable_provenance",
        "primary_source": "NED_NEDD plus source-specific dataset/method records",
        "secondary_source": "manual pre-scoring provenance ledger",
        "fallback_policy": "row cannot enter claim-ready endpoint without provenance",
        "acceptance_check": "dataset, method, and pre-scoring timestamp present",
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


def build_crossmatch_template(manifest: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "galaxy",
        "proxy_formula_family_for_scope",
        "sparc_present",
        "s4g_match_status",
        "ned_nedd_match_status",
        "dustpedia_match_status",
        "phangs_match_status",
        "primary_morphology_source",
        "secondary_morphology_source",
        "accepted_observable_collection_status",
        "crossmatch_notes",
    ]
    rows = []
    for _, item in manifest.iterrows():
        rows.append(
            {
                "galaxy": item["galaxy"],
                "proxy_formula_family_for_scope": item["formula_family"],
                "sparc_present": True,
                "s4g_match_status": "TO_BE_CHECKED",
                "ned_nedd_match_status": "TO_BE_CHECKED",
                "dustpedia_match_status": "TO_BE_CHECKED",
                "phangs_match_status": "TO_BE_CHECKED",
                "primary_morphology_source": "TO_BE_ASSIGNED",
                "secondary_morphology_source": "TO_BE_ASSIGNED",
                "accepted_observable_collection_status": "NOT_STARTED",
                "crossmatch_notes": "",
            }
        )
    return pd.DataFrame(rows, columns=columns)


def write_report(
    source_registry: pd.DataFrame,
    field_map: pd.DataFrame,
    crossmatch: pd.DataFrame,
) -> None:
    lines = [
        "# External Morphology Source Registry",
        "",
        "This registry records where the missing accepted morphology inputs should",
        "come from. It is a source-acquisition plan and crossmatch template, not a",
        "claim that the accepted inputs have already been collected.",
        "",
        "## Verdict",
        "",
        "Use SPARC as the sample and baryonic/rotation baseline, S4G as the first",
        "primary morphology/decomposition source, NED/NED-D as the identity and",
        "distance/provenance layer, DustPedia as multiband fallback/validation, and",
        "PHANGS only for optional high-quality non-axisymmetric branches. The next",
        "practical step is to fill the 175-row crossmatch template before endpoint",
        "launch is considered.",
        "",
        "## Source Registry",
        "",
        markdown_table(source_registry),
        "",
        "## Field-To-Source Map",
        "",
        markdown_table(field_map),
        "",
        "## Crossmatch Template Summary",
        "",
        f"Rows: {len(crossmatch)}",
        "",
        "All external source match fields are intentionally `TO_BE_CHECKED`. This",
        "prevents the current proxy manifest from masquerading as accepted-source",
        "coverage.",
        "",
        "## Claim Boundary",
        "",
        "A successful crossmatch would provide candidate accepted inputs for the",
        "readiness gate. It would not by itself compute endpoint scores or validate",
        "Tau Core against MOND, RAR, TGP, or Newtonian baselines.",
    ]
    (REPORTS / "external_morphology_source_registry.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    source_registry = pd.DataFrame(SOURCE_ROWS)
    field_map = pd.DataFrame(FIELD_SOURCE_ROWS)
    crossmatch = build_crossmatch_template(manifest)

    source_registry.to_csv(DATA / "external_morphology_source_registry.csv", index=False)
    field_map.to_csv(DATA / "morphology_field_source_map.csv", index=False)
    crossmatch.to_csv(DATA / "sparc_external_source_crossmatch_template.csv", index=False)
    write_report(source_registry, field_map, crossmatch)
    print("PAPER8_EXTERNAL_MORPHOLOGY_SOURCE_REGISTRY_COMPLETE")


if __name__ == "__main__":
    main()
