#!/usr/bin/env python3
"""Build residual-blind morphology-observable intake schema for the next run."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


SCHEMA_ROWS = [
    {
        "field": "galaxy",
        "required": True,
        "scope": "all",
        "accepted_source": "catalog identifier before endpoint scoring",
        "forbidden_source": "none",
        "acceptance_rule": "must uniquely match component/rotation-curve table",
        "failure_mode": "row cannot enter endpoint",
    },
    {
        "field": "formula_family",
        "required": True,
        "scope": "all",
        "accepted_source": "residual-blind morphology classification",
        "forbidden_source": "vobs residual pattern; required_S_tau; best-fit formula choice",
        "acceptance_rule": "one of predeclared Tau Core morphology families",
        "failure_mode": "leakage risk; row becomes diagnostic-only",
    },
    {
        "field": "manifest_confidence",
        "required": True,
        "scope": "all",
        "accepted_source": "pre-scoring morphology-observable quality assessment",
        "forbidden_source": "endpoint residual performance",
        "acceptance_rule": "numeric in [0,1]; threshold gate predeclared",
        "failure_mode": "quality gate cannot be audited",
    },
    {
        "field": "manifest_caveat",
        "required": True,
        "scope": "all",
        "accepted_source": "observability caveats from geometry/catalog quality",
        "forbidden_source": "bad endpoint score after model application",
        "acceptance_rule": "must include none or explicit caveat tokens",
        "failure_mode": "cannot preserve limited-observability evidence",
    },
    {
        "field": "inclination_deg",
        "required": True,
        "scope": "primary quality gate",
        "accepted_source": "external geometry/catalog measurement",
        "forbidden_source": "endpoint residual fit",
        "acceptance_rule": "used to apply no_low_inclination gate before scoring",
        "failure_mode": "primary endpoint lane cannot be reproduced",
    },
    {
        "field": "distance_frac_error",
        "required": True,
        "scope": "secondary quality gate",
        "accepted_source": "external distance estimate uncertainty",
        "forbidden_source": "baseline-comparison outcome",
        "acceptance_rule": "used to apply no_large_distance_error support gate",
        "failure_mode": "secondary baseline lane cannot be reproduced",
    },
    {
        "field": "scale_radius_kpc",
        "required": True,
        "scope": "K_scale_tail_spiral; K_exponential_disk; K_thick_flared",
        "accepted_source": "morphology/light-profile decomposition before endpoint scoring",
        "forbidden_source": "rotation residual shape or endpoint-selected scale",
        "acceptance_rule": "positive physical length with provenance",
        "failure_mode": "kernel scale remains proxy-level",
    },
    {
        "field": "tail_inner_radius_kpc",
        "required": True,
        "scope": "K_scale_tail_spiral",
        "accepted_source": "morphological transition or disk-structure feature",
        "forbidden_source": "radius chosen to minimize residuals",
        "acceptance_rule": "positive and <= tail_cutoff_radius_kpc",
        "failure_mode": "scale-tail formula cannot be source-native",
    },
    {
        "field": "tail_cutoff_radius_kpc",
        "required": True,
        "scope": "K_scale_tail_spiral",
        "accepted_source": "outer disk/tail morphology extent",
        "forbidden_source": "endpoint-selected truncation radius",
        "acceptance_rule": "positive and >= tail_inner_radius_kpc",
        "failure_mode": "tail response normalization is not reproducible",
    },
    {
        "field": "compact_support_radius_kpc",
        "required": True,
        "scope": "K_compact_finite",
        "accepted_source": "residual-blind compact-source morphology support",
        "forbidden_source": "radius chosen from residual improvement",
        "acceptance_rule": "positive support radius with provenance",
        "failure_mode": "compact finite source row remains proxy-level",
    },
    {
        "field": "thickness_h_over_rs",
        "required": True,
        "scope": "K_thick_flared",
        "accepted_source": "vertical/thickness proxy or direct morphology estimate",
        "forbidden_source": "endpoint-tuned damping factor",
        "acceptance_rule": "positive dimensionless ratio with uncertainty/caveat",
        "failure_mode": "thick/flared kernel cannot be audited",
    },
    {
        "field": "ring_radius_kpc",
        "required": False,
        "scope": "K_ring_resonance",
        "accepted_source": "external ring/resonance morphology",
        "forbidden_source": "residual peak location",
        "acceptance_rule": "positive radius if ring family is included",
        "failure_mode": "ring row must remain caveated/proxy",
    },
    {
        "field": "bar_m2_strength",
        "required": False,
        "scope": "K_barred_m2",
        "accepted_source": "image/velocity-field morphology before endpoint scoring",
        "forbidden_source": "1D residual asymmetry fit",
        "acceptance_rule": "only velocity-field/full morphology endpoint can promote this row",
        "failure_mode": "1D SPARC row remains caveated proxy",
    },
    {
        "field": "lopsided_m1_strength",
        "required": False,
        "scope": "K_lopsided_m1",
        "accepted_source": "image/velocity-field asymmetry before endpoint scoring",
        "forbidden_source": "1D residual asymmetry fit",
        "acceptance_rule": "only velocity-field/full morphology endpoint can promote this row",
        "failure_mode": "1D SPARC row remains caveated proxy",
    },
    {
        "field": "observable_provenance",
        "required": True,
        "scope": "all",
        "accepted_source": "dataset name, measurement method, and pre-scoring timestamp",
        "forbidden_source": "undocumented manual adjustment",
        "acceptance_rule": "must document source and residual-blind status",
        "failure_mode": "row cannot support a claim-safe endpoint",
    },
]


ACCEPTANCE_ROWS = [
    {
        "gate": "residual_blindness",
        "pass_condition": "No observable may use vobs residual gain, required_S_tau, or posthoc family choice.",
        "status": "required",
    },
    {
        "gate": "primary_quality_gate_ready",
        "pass_condition": "inclination fields and low-inclination caveat must reproduce no_low_inclination lane.",
        "status": "required",
    },
    {
        "gate": "family_kernel_parameters_ready",
        "pass_condition": "Each included formula family has all required scale/support/thickness fields.",
        "status": "required",
    },
    {
        "gate": "provenance_ready",
        "pass_condition": "Every row records external morphology-observable provenance.",
        "status": "required",
    },
    {
        "gate": "caveated_rows_preserved",
        "pass_condition": "Rows failing a quality gate remain in support/control outputs.",
        "status": "required",
    },
    {
        "gate": "non_axisymmetric_caveat",
        "pass_condition": "m=1/m=2 rows are not promoted from 1D curves without velocity-field support.",
        "status": "required",
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


def write_report(schema: pd.DataFrame, acceptance: pd.DataFrame) -> None:
    lines = [
        "# Morphology Observable Intake Schema",
        "",
        "This schema defines the residual-blind morphology observables needed for",
        "the next Paper 8 endpoint run. It is a data-intake contract, not a fit",
        "and not an empirical validation claim.",
        "",
        "## Required Observable Fields",
        "",
        markdown_table(schema),
        "",
        "## Acceptance Gates",
        "",
        markdown_table(acceptance),
        "",
        "## Claim Boundary",
        "",
        "The current available-data manifest remains a proxy manifest. A future",
        "Paper 8 empirical run should not be treated as claim-ready until this",
        "schema is populated from accepted residual-blind morphology observables",
        "and the predeclared endpoint protocol is run without changing gates after",
        "seeing scores.",
    ]
    (REPORTS / "morphology_observable_intake_schema.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    schema = pd.DataFrame(SCHEMA_ROWS)
    acceptance = pd.DataFrame(ACCEPTANCE_ROWS)
    schema.to_csv(DATA / "morphology_observable_intake_schema.csv", index=False)
    acceptance.to_csv(DATA / "morphology_observable_acceptance_gates.csv", index=False)
    write_report(schema, acceptance)
    print("PAPER8_MORPHOLOGY_OBSERVABLE_INTAKE_SCHEMA_COMPLETE")


if __name__ == "__main__":
    main()
