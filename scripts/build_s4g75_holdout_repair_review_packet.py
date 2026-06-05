#!/usr/bin/env python3
"""Build residual-blind review packets for S4G75 holdout P0/P1 repairs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_holdout_repair_review_packet_not_endpoint"


REVIEW_FIELDS = {
    "P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT": [
        "distance_source_review",
        "scale_radius_consistency_review",
        "projection_safety_review",
        "family_label_external_audit",
        "kernel_observable_completion",
    ],
    "P1_INCLINATION_PROJECTION_REVIEW": [
        "inclination_source_review",
        "distance_source_review",
        "projection_safety_review",
        "tail_extent_source_review",
        "family_label_external_audit",
    ],
    "P1_VERTICAL_GEOMETRY_SOURCE": [
        "vertical_thickness_or_flare_source_review",
        "warp_or_gas_plane_source_review",
        "edge_projection_safety_review",
        "family_label_external_audit",
        "thick_flared_kernel_observable_completion",
    ],
    "P2_SOURCE_NORMALIZATION_REVIEW": [
        "source_normalization_factor_review",
        "baryonic_scale_consistency_review",
        "component_weight_review",
    ],
}


FIELD_ACTIONS = {
    "distance_source_review": "compare SPARC distance/caveat with external distance source before scale promotion",
    "scale_radius_consistency_review": "check S4G disk scale radius against SPARC disk scale and morphology context",
    "projection_safety_review": "record whether inclination/projection makes the scale-sensitive readout unsafe",
    "family_label_external_audit": "audit the residual-blind family label against image/decomposition sources",
    "kernel_observable_completion": "collect missing family-specific kernel observables before endpoint eligibility",
    "inclination_source_review": "review inclination reliability and low-inclination caveat from metadata/catalog sources",
    "tail_extent_source_review": "collect residual-blind tail inner/cutoff or HI extent proxy for scale-tail readout",
    "vertical_thickness_or_flare_source_review": "collect source-native thickness/flaring evidence or keep vertical proxy blocked",
    "warp_or_gas_plane_source_review": "check HI/optical evidence for warp, flare, or gas-plane geometry",
    "edge_projection_safety_review": "review edge/projection caveat before thick/flared damping use",
    "thick_flared_kernel_observable_completion": "replace proxy h/Rs with source-native vertical observable or block endpoint",
    "source_normalization_factor_review": "audit q_i and source-normalization factors without endpoint residual tuning",
    "baryonic_scale_consistency_review": "check baryonic scale inputs used by source-normalization candidate",
    "component_weight_review": "audit component weights as source-readout weights, not endpoint-selected weights",
}


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: f"{value:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def available_text(value: object) -> str:
    if pd.isna(value):
        return "MISSING"
    return str(value)


def build_packet() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    action = pd.read_csv(DATA / "s4g75_source_rich_lane_action_plan.csv")
    s4g = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    accepted = pd.read_csv(DATA / "accepted_morphology_manifest.csv")
    audit = pd.read_csv(DATA / "accepted_morphology_manifest_audit.csv")
    crossmatch = pd.read_csv(DATA / "sparc_external_source_crossmatch_acquired.csv")

    holdout = action.loc[
        (action["split"] == "holdout")
        & action["repair_priority"].isin(
            [
                "P0_EXISTING_SCALE_PLUS_DISTANCE_AUDIT",
                "P1_INCLINATION_PROJECTION_REVIEW",
                "P1_VERTICAL_GEOMETRY_SOURCE",
                "P2_SOURCE_NORMALIZATION_REVIEW",
            ]
        )
    ].copy()

    merged = (
        holdout.merge(
            s4g[
                [
                    "galaxy",
                    "sparc_distance_mpc",
                    "sparc_rdisk_kpc",
                    "sparc_inclination_deg",
                    "s4g_match_status",
                    "s4g_name",
                    "scale_radius_kpc",
                    "s4g_bar_radius_arcsec",
                    "bar_radius_kpc",
                    "s4g_model_components",
                    "s4g_model_quality_values",
                    "candidate_observable_status",
                    "observable_provenance",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        .merge(
            accepted[
                [
                    "galaxy",
                    "manifest_confidence",
                    "manifest_caveat",
                    "missing_required_fields",
                    "endpoint_eligibility_status",
                    "endpoint_blocker",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        .merge(
            audit[
                [
                    "galaxy",
                    "audit_lane",
                    "s4g_disk_component_source",
                    "s4g_component_support_status",
                    "next_action",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        .merge(
            crossmatch[
                [
                    "galaxy",
                    "dustpedia_match_status",
                    "phangs_match_status",
                    "hi_survey_match_status",
                    "accepted_observable_collection_status",
                    "crossmatch_notes",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
    )

    packet_rows = []
    for _, row in merged.iterrows():
        for field in REVIEW_FIELDS.get(row["repair_priority"], []):
            packet_rows.append(
                {
                    "galaxy": row["galaxy"],
                    "split": row["split"],
                    "formula_family": row["formula_family"],
                    "repair_priority": row["repair_priority"],
                    "repair_status": row["repair_status"],
                    "review_field": field,
                    "residual_blind_review_action": FIELD_ACTIONS[field],
                    "source_targets": row["source_targets"],
                    "sparc_distance_mpc": row["sparc_distance_mpc"],
                    "sparc_inclination_deg": row["sparc_inclination_deg"],
                    "sparc_rdisk_kpc": row["sparc_rdisk_kpc"],
                    "s4g_match_status": row["s4g_match_status"],
                    "s4g_name": available_text(row["s4g_name"]),
                    "scale_radius_kpc": row["scale_radius_kpc"],
                    "s4g_components": available_text(row["s4g_model_components"]),
                    "s4g_bar_radius_arcsec": row["s4g_bar_radius_arcsec"],
                    "bar_radius_kpc": row["bar_radius_kpc"],
                    "s4g_support_status": available_text(row["s4g_component_support_status"]),
                    "audit_lane": available_text(row["audit_lane"]),
                    "s4g_disk_component_source": available_text(row["s4g_disk_component_source"]),
                    "manifest_confidence": row["manifest_confidence"],
                    "manifest_caveat": available_text(row["manifest_caveat"]),
                    "missing_required_fields": available_text(row["missing_required_fields"]),
                    "endpoint_blocker": available_text(row["endpoint_blocker"]),
                    "dustpedia_match_status": row["dustpedia_match_status"],
                    "phangs_match_status": row["phangs_match_status"],
                    "hi_survey_match_status": row["hi_survey_match_status"],
                    "current_review_status": "TO_BE_REVIEWED_RESIDUAL_BLIND",
                    "accepted_label_output_allowed": False,
                    "endpoint_scores_computed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    packet = pd.DataFrame(packet_rows)
    galaxy_summary = (
        packet.groupby(["galaxy", "repair_priority", "formula_family"])
        .agg(
            n_review_fields=("review_field", "count"),
            scale_radius_kpc=("scale_radius_kpc", "first"),
            sparc_inclination_deg=("sparc_inclination_deg", "first"),
            manifest_caveat=("manifest_caveat", "first"),
            missing_required_fields=("missing_required_fields", "first"),
            s4g_support_status=("s4g_support_status", "first"),
            audit_lane=("audit_lane", "first"),
            dustpedia_match_status=("dustpedia_match_status", "first"),
            phangs_match_status=("phangs_match_status", "first"),
            hi_survey_match_status=("hi_survey_match_status", "first"),
            endpoint_blocker=("endpoint_blocker", "first"),
        )
        .reset_index()
        .sort_values(["repair_priority", "galaxy"])
    )
    field_summary = (
        packet.groupby(["repair_priority", "review_field"])
        .agg(n_galaxies=("galaxy", "nunique"))
        .reset_index()
        .sort_values(["repair_priority", "review_field"])
    )
    return packet, galaxy_summary, field_summary


def write_report(packet: pd.DataFrame, galaxy_summary: pd.DataFrame, field_summary: pd.DataFrame) -> None:
    lines = [
        "# S4G75 Holdout Repair Review Packet",
        "",
        "This packet converts the S4G75 holdout P0/P1/P2 repair queue into "
        "residual-blind source-review fields. It uses existing S4G/SPARC and "
        "crossmatch tables where available, but it does not promote accepted "
        "labels and does not run endpoint scores.",
        "",
        "## Verdict",
        "",
        f"Galaxies in packet: {packet['galaxy'].nunique()}.",
        f"Review fields: {len(packet)}.",
        "",
        "Existing S4G/SPARC scale evidence is present for these rows, but family "
        "labels and family-specific kernel fields remain blocked until the review "
        "fields below are completed.",
        "",
        "## Galaxy Summary",
        "",
        markdown_table(galaxy_summary),
        "",
        "## Field Summary",
        "",
        markdown_table(field_summary),
        "",
        "## Claim Boundary",
        "",
        "This packet is a repair workflow, not a validation result. Filling it may "
        "make a future frozen endpoint cleaner, but no endpoint gate changes here.",
    ]
    (REPORTS / "s4g75_holdout_repair_review_packet.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    packet, galaxy_summary, field_summary = build_packet()
    packet.to_csv(DATA / "s4g75_holdout_repair_review_packet.csv", index=False)
    galaxy_summary.to_csv(
        DATA / "s4g75_holdout_repair_review_galaxy_summary.csv", index=False
    )
    field_summary.to_csv(
        DATA / "s4g75_holdout_repair_review_field_summary.csv", index=False
    )
    write_report(packet, galaxy_summary, field_summary)
    print("PAPER8_S4G75_HOLDOUT_REPAIR_REVIEW_PACKET_COMPLETE")
    print(galaxy_summary.to_string(index=False))


if __name__ == "__main__":
    main()
