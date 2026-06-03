#!/usr/bin/env python3
"""Build a residual-blind morphology inspection queue.

The queue prioritizes galaxies for external image/decomposition/history-proxy
review after the morphology-memory diagnostic.  It is an acquisition plan, not
an accepted morphology-label table and not an endpoint score.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "morphology_inspection_queue_not_accepted_label_not_endpoint"


def has_flag(flags: str, needle: str) -> bool:
    return needle in str(flags).split(";")


def priority_score(row: pd.Series) -> int:
    score = 0
    if not bool(row["matches_current_proxy_family"]):
        score += 35
    if row["rotation_inferred_confidence"] == "HIGH":
        score += 20
    elif row["rotation_inferred_confidence"] == "MEDIUM":
        score += 10
    if bool(row["external_family_mismatch"]):
        score += 20
    if float(row["manifest_confidence"]) >= 0.75:
        score += 10
    if row["s4g_match_status"] == "S4G_MATCHED":
        score += 8
    flags = str(row["source_memory_proxy_flags"])
    for flag in [
        "gas_rich_late_or_irregular",
        "low_surface_brightness_or_diffuse",
        "bulge_or_compact_core_memory",
        "vertical_geometry_proxy_only",
        "bar_component_caveat",
        "edge_or_projection_caveat",
    ]:
        if has_flag(flags, flag):
            score += 5
    return score


def priority_tier(score: int) -> str:
    if score >= 85:
        return "P0"
    if score >= 70:
        return "P1"
    if score >= 55:
        return "P2"
    return "P3"


def inspection_focus(row: pd.Series) -> str:
    klass = row["memory_history_proxy_class"]
    inferred = row["rotation_inferred_family"]
    flags = str(row["source_memory_proxy_flags"])
    focuses: list[str] = []
    if "scale_tail" in klass or inferred == "K_scale_tail_spiral":
        focuses.append("outer_disk_tail_lsb_or_hi_extent")
    if "vertical" in klass or inferred == "K_thick_flared" or has_flag(
        flags, "vertical_geometry_proxy_only"
    ):
        focuses.append("thickness_flare_warp_or_projection")
    if "compact" in klass or inferred == "K_compact_finite" or has_flag(
        flags, "bulge_or_compact_core_memory"
    ):
        focuses.append("bulge_compact_core_or_central_support")
    if has_flag(flags, "bar_component_caveat"):
        focuses.append("bar_m2_component")
    if has_flag(flags, "edge_or_projection_caveat"):
        focuses.append("edge_on_projection_degeneracy")
    if not focuses:
        focuses.append("current_label_vs_readout_subtype_split")
    return ";".join(sorted(set(focuses)))


def requested_sources(row: pd.Series) -> str:
    focus = inspection_focus(row)
    sources = ["residual_blind_multiband_image_morphology_label"]
    if "outer_disk_tail_lsb_or_hi_extent" in focus:
        sources.extend(["deep_optical_or_ir_outer_disk_profile", "hi_extent_or_asymmetry"])
    if "thickness_flare_warp_or_projection" in focus:
        sources.extend(["edge_on_projection_audit", "vertical_profile_or_warp_observable"])
    if "bulge_compact_core_or_central_support" in focus:
        sources.extend(["bulge_disk_decomposition", "central_surface_brightness_profile"])
    if "bar_m2_component" in focus:
        sources.extend(["bar_length_and_m2_component", "velocity_field_if_available"])
    if row["s4g_match_status"] != "S4G_MATCHED":
        sources.append("non_s4g_external_morphology_source")
    return ";".join(dict.fromkeys(sources))


def build_queue() -> tuple[pd.DataFrame, pd.DataFrame]:
    memory = pd.read_csv(DATA / "morphological_memory_history_proxy.csv")
    external = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    queue = memory.merge(
        external[
            [
                "galaxy",
                "s4g_match_status",
                "scale_radius_kpc",
                "bar_radius_kpc",
                "s4g_model_components",
                "candidate_observable_status",
                "observable_provenance",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    queue["inspection_priority_score"] = queue.apply(priority_score, axis=1)
    queue["inspection_priority_tier"] = queue["inspection_priority_score"].map(
        priority_tier
    )
    queue["inspection_focus"] = queue.apply(inspection_focus, axis=1)
    queue["requested_external_sources"] = queue.apply(requested_sources, axis=1)
    queue["inspection_status"] = "PENDING_RESIDUAL_BLIND_MORPHOLOGY_REVIEW"
    queue["accepted_label_output_allowed"] = False
    queue["endpoint_scores_allowed"] = False
    queue["claim_boundary"] = CLAIM_BOUNDARY
    columns = [
        "galaxy",
        "inspection_priority_tier",
        "inspection_priority_score",
        "inspection_focus",
        "requested_external_sources",
        "current_proxy_family",
        "rotation_inferred_family",
        "rotation_inferred_confidence",
        "memory_history_proxy_class",
        "source_memory_proxy_flags",
        "manifest_confidence",
        "manifest_caveat",
        "external_family_label",
        "external_family_mismatch",
        "s4g_match_status",
        "scale_radius_kpc",
        "bar_radius_kpc",
        "s4g_model_components",
        "candidate_observable_status",
        "observable_provenance",
        "inspection_status",
        "accepted_label_output_allowed",
        "endpoint_scores_allowed",
        "claim_boundary",
    ]
    queue = queue[columns].sort_values(
        ["inspection_priority_score", "galaxy"], ascending=[False, True]
    )
    summary = (
        queue.groupby(["inspection_priority_tier", "inspection_focus"], as_index=False)
        .agg(
            n_galaxies=("galaxy", "size"),
            median_priority_score=("inspection_priority_score", "median"),
            n_s4g_matched=("s4g_match_status", lambda values: int((values == "S4G_MATCHED").sum())),
            n_external_family_mismatches=("external_family_mismatch", "sum"),
        )
        .sort_values(["inspection_priority_tier", "n_galaxies"], ascending=[True, False])
    )
    return queue, summary


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(queue: pd.DataFrame, summary: pd.DataFrame) -> None:
    tier_counts = (
        queue.groupby("inspection_priority_tier", as_index=False)
        .size()
        .rename(columns={"size": "n_galaxies"})
        .sort_values("inspection_priority_tier")
    )
    top = queue.head(20)[
        [
            "galaxy",
            "inspection_priority_tier",
            "inspection_priority_score",
            "inspection_focus",
            "current_proxy_family",
            "rotation_inferred_family",
            "s4g_match_status",
        ]
    ]
    lines = [
        "# Morphology Inspection Queue",
        "",
        "This queue prioritizes galaxies for residual-blind morphology review after",
        "the morphology-memory/history proxy diagnostic. It is an acquisition and",
        "audit plan only. It does not promote rotation-inferred readout choices to",
        "accepted morphology labels.",
        "",
        "## Verdict",
        "",
        "The queue turns the current-shape/readout-history mismatch signal into a",
        "concrete inspection order: which galaxies need image/decomposition review,",
        "which memory/history observables to request, and which cases need external",
        "sources beyond the current S4G crossmatch.",
        "",
        "## Priority Counts",
        "",
        markdown_table(tier_counts),
        "",
        "## Focus Summary",
        "",
        markdown_table(summary),
        "",
        "## Top 20 Inspection Targets",
        "",
        markdown_table(top),
        "",
        "## Claim Boundary",
        "",
        "This is not an accepted morphology manifest, not a morphology validation,",
        "and not an endpoint score. The queue is allowed to guide future",
        "residual-blind source collection only.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "morphology_inspection_queue.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    queue, summary = build_queue()
    queue.to_csv(DATA / "morphology_inspection_queue.csv", index=False)
    summary.to_csv(DATA / "morphology_inspection_queue_summary.csv", index=False)
    write_report(queue, summary)
    print("PAPER8_MORPHOLOGY_INSPECTION_QUEUE_COMPLETE")


if __name__ == "__main__":
    main()
