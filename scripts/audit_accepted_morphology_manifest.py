#!/usr/bin/env python3
"""Audit the partial accepted morphology manifest without launching endpoints."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


def has_text(value: object) -> bool:
    text = "" if pd.isna(value) else str(value).strip()
    return bool(text) and text.lower() != "nan"


def component_support(row: pd.Series) -> str:
    source = str(row.get("s4g_disk_component_source", ""))
    components = str(row.get("s4g_model_components", ""))
    if row["scale_radius_source_status"] != "ACCEPTED_SOURCE_OBSERVABLE":
        return "NO_ACCEPTED_SCALE_TO_AUDIT"
    if "D:expdisk" in source:
        if "BAR" in components:
            return "S4G_EXPDISK_WITH_BAR_CAVEAT"
        return "S4G_EXPDISK_SUPPORT"
    if "Z:edgedisk" in source:
        return "S4G_EDGEDISK_SUPPORT_CAVEATED"
    return "S4G_DISK_SCALE_SOURCE_UNCLASSIFIED"


def primary_blocker(row: pd.Series) -> str:
    if row["family_label_source_status"].startswith("REVIEW_PROXY"):
        if not has_text(row["missing_required_fields"]):
            return "external_family_label_audit_only"
        return "family_label_and_kernel_fields"
    if has_text(row["missing_required_fields"]):
        return "kernel_fields"
    return "none"


def audit_lane(row: pd.Series) -> str:
    if (
        row["formula_family"] == "K_exponential_disk"
        and row["scale_radius_source_status"] == "ACCEPTED_SOURCE_OBSERVABLE"
        and not has_text(row["missing_required_fields"])
    ):
        return "NEAR_TERM_EXPONENTIAL_DISK_FAMILY_LABEL_AUDIT_POOL"
    if row["scale_radius_source_status"] == "ACCEPTED_SOURCE_OBSERVABLE":
        return "PARTIAL_SCALE_READY_KERNEL_BLOCKED"
    if row["s4g_match_status"] == "S4G_MATCHED":
        return "S4G_MATCHED_BUT_NO_ACCEPTED_SCALE"
    return "NO_S4G_MATCH_EXTERNAL_SOURCE_NEEDED"


def next_action(row: pd.Series) -> str:
    lane = row["audit_lane"]
    if lane == "NEAR_TERM_EXPONENTIAL_DISK_FAMILY_LABEL_AUDIT_POOL":
        return "audit external morphology family label; do not score endpoint yet"
    if lane == "PARTIAL_SCALE_READY_KERNEL_BLOCKED":
        return "collect family-specific kernel observables before endpoint eligibility"
    if lane == "S4G_MATCHED_BUT_NO_ACCEPTED_SCALE":
        return "inspect S4G component table or fallback morphology source for scale"
    return "crossmatch NED/NED-D/DustPedia or other residual-blind morphology source"


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    manifest = pd.read_csv(DATA / "accepted_morphology_manifest.csv")
    candidates = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    components = pd.read_csv(DATA / "external_s4g_disk_component_summary.csv")
    audit = (
        manifest.merge(
            candidates[
                [
                    "galaxy",
                    "s4g_match_status",
                    "s4g_name",
                    "s4g_model_components",
                    "s4g_model_quality_values",
                    "bar_radius_kpc",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        .merge(
            components[["s4g_name", "s4g_disk_component_source"]],
            on="s4g_name",
            how="left",
        )
        .copy()
    )
    audit["s4g_component_support_status"] = audit.apply(component_support, axis=1)
    audit["primary_blocker"] = audit.apply(primary_blocker, axis=1)
    audit["audit_lane"] = audit.apply(audit_lane, axis=1)
    audit["next_action"] = audit.apply(next_action, axis=1)
    audit["audit_claim_boundary"] = (
        "accepted_manifest_audit_not_endpoint_score_not_family_validation"
    )
    columns = [
        "galaxy",
        "formula_family",
        "audit_lane",
        "primary_blocker",
        "scale_radius_source_status",
        "scale_radius_kpc",
        "s4g_match_status",
        "s4g_name",
        "s4g_disk_component_source",
        "s4g_model_components",
        "s4g_model_quality_values",
        "s4g_component_support_status",
        "missing_required_fields",
        "manifest_confidence",
        "manifest_caveat",
        "endpoint_eligibility_status",
        "next_action",
        "audit_claim_boundary",
    ]
    audit = audit[columns]
    summary = (
        audit.groupby(["formula_family", "audit_lane"], as_index=False)
        .agg(
            n_rows=("galaxy", "size"),
            n_accepted_scale=(
                "scale_radius_source_status",
                lambda s: int((s == "ACCEPTED_SOURCE_OBSERVABLE").sum()),
            ),
            n_s4g_matched=(
                "s4g_match_status",
                lambda s: int((s == "S4G_MATCHED").sum()),
            ),
        )
        .sort_values(["formula_family", "audit_lane"])
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


def write_report(audit: pd.DataFrame, summary: pd.DataFrame) -> None:
    lane_counts = (
        audit.groupby("audit_lane", as_index=False)
        .size()
        .rename(columns={"size": "n_rows"})
        .sort_values("audit_lane")
    )
    support_counts = (
        audit.groupby("s4g_component_support_status", as_index=False)
        .size()
        .rename(columns={"size": "n_rows"})
        .sort_values("s4g_component_support_status")
    )
    near = audit[
        audit["audit_lane"] == "NEAR_TERM_EXPONENTIAL_DISK_FAMILY_LABEL_AUDIT_POOL"
    ][
        [
            "galaxy",
            "scale_radius_kpc",
            "s4g_disk_component_source",
            "s4g_model_components",
            "manifest_caveat",
            "s4g_component_support_status",
        ]
    ]
    lines = [
        "# Accepted Morphology Manifest Audit",
        "",
        "This audit inspects the partial accepted morphology manifest without running",
        "endpoint scores. It separates field-level source acceptance, external",
        "family-label support candidates, and remaining endpoint blockers.",
        "",
        "## Verdict",
        "",
        "The closest near-term lane is the exponential-disk family-label audit pool:",
        f"{len(near)} rows have an accepted S4G/SPARC scale radius and no missing",
        "kernel field beyond the external family-label audit. These rows are not",
        "endpoint-ready; they are the next audit pool.",
        "",
        "## Audit Lanes",
        "",
        markdown_table(lane_counts),
        "",
        "## S4G Component Support",
        "",
        markdown_table(support_counts),
        "",
        "## Family/Lane Summary",
        "",
        markdown_table(summary),
        "",
        "## Near-Term Exponential-Disk Audit Pool",
        "",
        markdown_table(near),
        "",
        "## Claim Boundary",
        "",
        "This audit is not an endpoint score and not a validation of Tau Core. It does",
        "not promote proxy family labels into accepted labels.",
        "This audit does not promote proxy family labels. It identifies which",
        "rows should be audited next using external residual-blind morphology support.",
    ]
    (REPORTS / "accepted_morphology_manifest_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    audit, summary = build_audit()
    audit.to_csv(DATA / "accepted_morphology_manifest_audit.csv", index=False)
    summary.to_csv(DATA / "accepted_morphology_manifest_audit_summary.csv", index=False)
    write_report(audit, summary)
    print("PAPER8_ACCEPTED_MORPHOLOGY_MANIFEST_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
