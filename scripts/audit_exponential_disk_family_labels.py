#!/usr/bin/env python3
"""Strengthen the near-term exponential-disk family-label audit pool.

This script uses only residual-blind S4G component information already acquired
by the package.  It does not inspect endpoint scores and it does not run the
Paper 8 endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


NEAR_LANE = "NEAR_TERM_EXPONENTIAL_DISK_FAMILY_LABEL_AUDIT_POOL"


def has_bar(components: object) -> bool:
    return "BAR" in str(components).split(";")


def label_status(row: pd.Series) -> str:
    source = str(row["s4g_disk_component_source"])
    if "D:expdisk" in source and not has_bar(row["s4g_model_components"]):
        return "ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG"
    if "D:expdisk" in source and has_bar(row["s4g_model_components"]):
        return "ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR"
    if "Z:edgedisk" in source:
        return "ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON"
    return "REVIEW_EXTERNAL_DISK_LABEL_SUPPORT"


def strict_lane(status: str) -> str:
    if status == "ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG":
        return "STRICT_NARROW_DRY_RUN_READY_CANDIDATE"
    if status.startswith("ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED"):
        return "CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL"
    return "REVIEW_ONLY"


def label_confidence(status: str) -> float:
    if status == "ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG":
        return 1.0
    if status.startswith("ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED"):
        return 0.85
    return 0.5


def label_caveat(row: pd.Series) -> str:
    status = row["external_family_label_status"]
    caveats = []
    if status.endswith("CAVEATED_BAR"):
        caveats.append("bar_component_present")
    if status.endswith("CAVEATED_EDGEON"):
        caveats.append("edgedisk_component_orientation_caveat")
    manifest_caveat = str(row["manifest_caveat"])
    if manifest_caveat and manifest_caveat != "none" and manifest_caveat != "nan":
        caveats.append(manifest_caveat)
    return ";".join(caveats) if caveats else "none"


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    audit = pd.read_csv(DATA / "accepted_morphology_manifest_audit.csv")
    manifest = pd.read_csv(DATA / "accepted_morphology_manifest.csv")
    pool = (
        audit[audit["audit_lane"] == NEAR_LANE]
        .merge(
            manifest[
                [
                    "galaxy",
                    "inclination_deg",
                    "distance_frac_error",
                    "observable_provenance",
                    "residual_blind_certification",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        .copy()
    )
    pool["external_family_label"] = "K_exponential_disk"
    pool["external_family_label_source"] = "VizieR_J/ApJS/219/4_S4G_Pipeline4"
    pool["external_family_label_method"] = (
        "S4G component model contains expdisk or edgedisk decomposition component"
    )
    pool["external_family_label_status"] = pool.apply(label_status, axis=1)
    pool["external_family_label_confidence"] = pool[
        "external_family_label_status"
    ].apply(label_confidence)
    pool["external_family_label_caveat"] = pool.apply(label_caveat, axis=1)
    pool["narrow_dry_run_lane"] = pool["external_family_label_status"].apply(strict_lane)
    pool["endpoint_scores_computed"] = False
    pool["claim_boundary"] = (
        "external_family_label_audit_not_endpoint_score_not_empirical_validation"
    )
    columns = [
        "galaxy",
        "external_family_label",
        "external_family_label_status",
        "external_family_label_confidence",
        "external_family_label_caveat",
        "narrow_dry_run_lane",
        "scale_radius_kpc",
        "s4g_name",
        "s4g_disk_component_source",
        "s4g_model_components",
        "s4g_model_quality_values",
        "inclination_deg",
        "distance_frac_error",
        "external_family_label_source",
        "external_family_label_method",
        "observable_provenance",
        "residual_blind_certification",
        "endpoint_scores_computed",
        "claim_boundary",
    ]
    pool = pool[columns].sort_values(["narrow_dry_run_lane", "galaxy"])
    summary = (
        pool.groupby(
            ["external_family_label_status", "narrow_dry_run_lane"], as_index=False
        )
        .agg(
            n_rows=("galaxy", "size"),
            mean_label_confidence=("external_family_label_confidence", "mean"),
            endpoint_scores_computed=("endpoint_scores_computed", "any"),
        )
        .sort_values(["narrow_dry_run_lane", "external_family_label_status"])
    )
    return pool, summary


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(pool: pd.DataFrame, summary: pd.DataFrame) -> None:
    strict = pool[pool["narrow_dry_run_lane"] == "STRICT_NARROW_DRY_RUN_READY_CANDIDATE"]
    caveated = pool[
        pool["narrow_dry_run_lane"] == "CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL"
    ]
    lines = [
        "# Exponential-Disk Family-Label Audit",
        "",
        "This audit strengthens the near-term exponential-disk pool using S4G",
        "component decompositions only. It is residual-blind and does not compute",
        "endpoint scores.",
        "",
        "## Verdict",
        "",
        f"Audited near-term exponential-disk rows: {len(pool)}.",
        f"Strict external expdisk support: {len(strict)}.",
        f"Caveated external disk support: {len(caveated)}.",
        "",
        "All audited rows retain an external disk-family support label, but only the",
        "strict subset is proposed as the first narrow dry-run candidate lane. The",
        "barred and edge-on rows remain useful support rows with caveats.",
        "",
        "## Status Summary",
        "",
        markdown_table(summary),
        "",
        "## Audited Rows",
        "",
        markdown_table(pool),
        "",
        "## Claim Boundary",
        "",
        "This is not an endpoint score, not a claim that Tau Core fits these galaxies",
        "better than baselines, and not a final Paper 8 result. It only promotes",
        "the near-term family-label audit pool from proxy-label review to external",
        "S4G-supported disk-family labels.",
    ]
    (REPORTS / "exponential_disk_family_label_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    pool, summary = build_audit()
    pool.to_csv(DATA / "exponential_disk_family_label_audit.csv", index=False)
    summary.to_csv(DATA / "exponential_disk_family_label_audit_summary.csv", index=False)
    write_report(pool, summary)
    print("PAPER8_EXPONENTIAL_DISK_FAMILY_LABEL_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
