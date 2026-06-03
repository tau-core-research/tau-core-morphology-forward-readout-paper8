#!/usr/bin/env python3
"""Build the readout-state vector intake schema and gap audit.

The readout-mixture proxy diagnostic showed that a coarse available-data
mixture is not automatically better than hard family selection.  This script
turns that negative result into an operational data gate: which residual-blind
source observables would be needed before mixture weights can be treated as an
accepted Tau-side readout-state vector?

No endpoint score is computed here.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "readout_state_vector_intake_not_endpoint_not_accepted_state"

COMPONENTS = [
    {
        "readout_component": "K_exponential_disk",
        "weight_channel": "w_K_exponential_disk",
        "required_observable": "accepted disk scale/decomposition and clean disk label",
        "accepted_source_path": "S4G/SPARC scale radius plus external family-label audit",
        "proxy_columns": "scale_radius_kpc;family_label_source_status",
        "pass_rule": "accepted scale radius and accepted external disk family label",
        "failure_mode": "disk weight remains present-day 4D proxy rather than readout-state weight",
    },
    {
        "readout_component": "K_scale_tail_spiral",
        "weight_channel": "w_K_scale_tail_spiral",
        "required_observable": "accepted outer-disk/HI extent, tail, LSB, or asymmetry support",
        "accepted_source_path": "HI surveys;deep optical/IR outer-disk review;DustPedia fallback",
        "proxy_columns": "tail_inner_radius_kpc;tail_cutoff_radius_kpc;source_memory_proxy_flags",
        "pass_rule": "accepted tail radii or accepted HI/outer-disk memory observable",
        "failure_mode": "tail weight remains gas/LSB heuristic",
    },
    {
        "readout_component": "K_compact_finite",
        "weight_channel": "w_K_compact_finite",
        "required_observable": "accepted compact core, bulge, nuclear component, or finite support",
        "accepted_source_path": "S4G decomposition;NED/SIMBAD notes;high-resolution imaging review",
        "proxy_columns": "compact_support_radius_kpc;source_memory_proxy_flags",
        "pass_rule": "accepted compact support or accepted bulge/core memory observable",
        "failure_mode": "compact weight remains bulge-fraction proxy",
    },
    {
        "readout_component": "K_thick_flared",
        "weight_channel": "w_K_thick_flared",
        "required_observable": "accepted vertical thickness, flare, warp, or projection-sensitive support",
        "accepted_source_path": "edge-on morphology review;HI warp/flare evidence;PHANGS/S4G support",
        "proxy_columns": "thickness_h_over_rs;manifest_caveat;source_memory_proxy_flags",
        "pass_rule": "accepted thickness/flare observable or accepted projection/warp memory observable",
        "failure_mode": "vertical weight remains inclination/thickness proxy",
    },
    {
        "readout_component": "normalization",
        "weight_channel": "amplitude_normalization",
        "required_observable": "source-native family-to-global or component normalization rule",
        "accepted_source_path": "Tau-side source-normalization derivation plus residual-blind scale observables",
        "proxy_columns": "amplitude_policy",
        "pass_rule": "normalization is derived or predeclared from source observables, not endpoint fit",
        "failure_mode": "mixture may carry correct components but wrong amplitude scale",
    },
    {
        "readout_component": "memory_history",
        "weight_channel": "history_memory_correction",
        "required_observable": "accepted morphology-memory/history or current-shape/readout mismatch evidence",
        "accepted_source_path": "residual-blind visual/decomposition/HI history review",
        "proxy_columns": "memory_history_proxy_class;source_memory_proxy_flags",
        "pass_rule": "history/memory judgment accepted before endpoint scoring",
        "failure_mode": "K_obs may be incorrectly promoted to K_readout",
    },
]


def source_flag_has(flags: str, needle: str) -> bool:
    return needle in str(flags).split(";")


def has_value(row: pd.Series, column: str) -> bool:
    return column in row.index and pd.notna(row[column])


def status_for_component(row: pd.Series, component: str) -> tuple[str, str]:
    family_status = str(row.get("family_label_source_status", ""))
    scale_status = str(row.get("scale_radius_source_status", ""))
    flags = str(row.get("source_memory_proxy_flags", ""))
    caveat = str(row.get("manifest_caveat", ""))

    if component == "K_exponential_disk":
        if scale_status == "ACCEPTED_S4G_SPARC_DERIVED_SCALE_RADIUS" and "ACCEPTED_EXTERNAL" in family_status:
            return "ACCEPTED_COMPONENT_INPUT_READY", "accepted scale and accepted external disk label"
        if scale_status == "ACCEPTED_S4G_SPARC_DERIVED_SCALE_RADIUS":
            return "FIELD_LEVEL_PARTIAL_FAMILY_LABEL_BLOCKED", "accepted scale exists, family label audit pending"
        return "MISSING_ACCEPTED_COMPONENT_INPUT", "accepted disk scale/family label missing"

    if component == "K_scale_tail_spiral":
        has_tail = has_value(row, "tail_inner_radius_kpc") and has_value(row, "tail_cutoff_radius_kpc")
        has_memory = source_flag_has(flags, "gas_rich_late_or_irregular") or source_flag_has(
            flags, "low_surface_brightness_or_diffuse"
        )
        if has_tail:
            return "ACCEPTED_COMPONENT_INPUT_READY", "accepted tail support radii present"
        if has_memory:
            return "PROXY_MEMORY_SIGNAL_NEEDS_ACCEPTED_SOURCE", "gas/LSB proxy present, accepted HI/tail source missing"
        return "MISSING_ACCEPTED_COMPONENT_INPUT", "accepted HI/tail/outer-disk observable missing"

    if component == "K_compact_finite":
        has_compact = has_value(row, "compact_support_radius_kpc")
        has_memory = source_flag_has(flags, "bulge_or_compact_core_memory")
        if has_compact:
            return "ACCEPTED_COMPONENT_INPUT_READY", "accepted compact support radius present"
        if has_memory:
            return "PROXY_MEMORY_SIGNAL_NEEDS_ACCEPTED_SOURCE", "bulge/core proxy present, accepted compact source missing"
        return "MISSING_ACCEPTED_COMPONENT_INPUT", "accepted compact/core observable missing"

    if component == "K_thick_flared":
        has_thickness = has_value(row, "thickness_h_over_rs")
        has_projection = "low_inclination" in caveat or source_flag_has(
            flags, "rotation_current_proxy_mismatch"
        )
        if has_thickness:
            return "ACCEPTED_COMPONENT_INPUT_READY", "accepted thickness/flare observable present"
        if has_projection:
            return "PROXY_MEMORY_SIGNAL_NEEDS_ACCEPTED_SOURCE", "projection/history proxy present, accepted vertical source missing"
        return "MISSING_ACCEPTED_COMPONENT_INPUT", "accepted vertical/flare/warp observable missing"

    if component == "normalization":
        return "MISSING_TAU_SIDE_NORMALIZATION_RULE", "current amplitude policy is train/preflight, not source-normalization law"

    if component == "memory_history":
        proxy_class = str(row.get("memory_history_proxy_class", ""))
        if proxy_class == "current_readout_consistent_no_memory_proxy_flag":
            return "NO_MEMORY_PROXY_FLAG", "current proxy and rotation-inferred readout are consistent"
        return "PROXY_MEMORY_SIGNAL_NEEDS_ACCEPTED_SOURCE", "memory/history proxy exists but is not accepted source evidence"

    raise ValueError(component)


def build_schema() -> pd.DataFrame:
    rows = []
    for order, item in enumerate(COMPONENTS, start=1):
        rows.append(
            {
                "component_order": order,
                **item,
                "allowed_use": "readout-state vector intake before endpoint scoring",
                "forbidden_inputs": "endpoint_residual_gain;required_S_tau;best_fit_readout_family;posthoc_family_choice;per_galaxy_endpoint_tuning",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_gap_audit(schema: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    accepted = pd.read_csv(DATA / "accepted_morphology_manifest.csv")
    memory = pd.read_csv(DATA / "morphological_memory_history_proxy.csv")
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    base = accepted.merge(
        memory[
            [
                "galaxy",
                "rotation_inferred_family",
                "source_memory_proxy_flags",
                "memory_history_proxy_class",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    ).merge(
        manifest[["galaxy", "amplitude_policy"]],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )

    rows = []
    for _, galaxy_row in base.iterrows():
        for _, component_row in schema.iterrows():
            status, reason = status_for_component(galaxy_row, component_row["readout_component"])
            rows.append(
                {
                    "galaxy": galaxy_row["galaxy"],
                    "split": galaxy_row["split"],
                    "formula_family": galaxy_row["formula_family"],
                    "readout_component": component_row["readout_component"],
                    "weight_channel": component_row["weight_channel"],
                    "component_status": status,
                    "status_reason": reason,
                    "endpoint_ready_component": status == "ACCEPTED_COMPONENT_INPUT_READY",
                    "proxy_only_component": "PROXY" in status or status == "NO_MEMORY_PROXY_FLAG",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    audit = pd.DataFrame(rows).sort_values(["split", "galaxy", "readout_component"])
    summary = (
        audit.groupby(["readout_component", "component_status"], as_index=False)
        .agg(
            n_rows=("galaxy", "size"),
            n_galaxies=("galaxy", "nunique"),
            endpoint_ready_components=("endpoint_ready_component", "sum"),
        )
        .sort_values(["readout_component", "component_status"])
    )
    return audit, summary


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(schema: pd.DataFrame, summary: pd.DataFrame) -> None:
    total_ready = int(summary["endpoint_ready_components"].sum())
    lines = [
        "# Readout-State Vector Intake Schema and Gap Audit",
        "",
        "This report records the source-observable gate required before the",
        "readout-mixture idea can be promoted from a proxy diagnostic to an",
        "accepted Tau-side readout-state vector. It computes no endpoint score.",
        "",
        f"Total accepted component inputs currently ready: {total_ready}.",
        "",
        "## Intake Schema",
        "",
        markdown_table(
            schema[
                [
                    "readout_component",
                    "weight_channel",
                    "required_observable",
                    "accepted_source_path",
                    "failure_mode",
                ]
            ]
        ),
        "",
        "## Gap Summary",
        "",
        markdown_table(summary),
        "",
        "## Verdict",
        "",
        "The current mixture weights remain proxy weights. The next run needs",
        "accepted residual-blind source observables for component weights,",
        "morphology-memory/history correction, and source normalization before",
        "the mixture can be scored as a frozen endpoint.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "readout_state_vector_intake_schema.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    schema = build_schema()
    audit, summary = build_gap_audit(schema)
    schema.to_csv(DATA / "readout_state_vector_intake_schema.csv", index=False)
    audit.to_csv(DATA / "readout_state_vector_gap_audit.csv", index=False)
    summary.to_csv(DATA / "readout_state_vector_gap_summary.csv", index=False)
    write_report(schema, summary)
    print("PAPER8_READOUT_STATE_VECTOR_INTAKE_SCHEMA_COMPLETE")


if __name__ == "__main__":
    main()
