#!/usr/bin/env python3
"""Audit local source-native availability for the S4G75 acquisition manifest.

This script checks the already acquired local S4G/SPARC/DustPedia/HI/PHANGS
tables against the S4G75 direct source-native acquisition queue.  It separates
generic source support from kernel-specific direct observables.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
EXTERNAL = ROOT / "data" / "external"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_source_native_availability_audit_not_endpoint"


def norm_name(name: object) -> str:
    raw = re.sub(r"[^A-Z0-9]", "", str(name).upper())
    match = re.match(r"NGC0+(\d+)$", raw)
    if match:
        return "NGC" + match.group(1)
    match = re.match(r"UGC0+(\d+)$", raw)
    if match:
        return "UGC" + match.group(1)
    return raw


def variants(name: str) -> set[str]:
    norm = norm_name(name)
    out = {norm}
    for prefix in ["NGC", "UGC"]:
        match = re.match(rf"{prefix}(\d+)$", norm)
        if match:
            number = match.group(1)
            out.add(prefix + number.zfill(4))
            out.add(prefix + number.zfill(5))
            out.add(prefix + number.zfill(3))
    return out


def finite(value: object) -> bool:
    try:
        return pd.notna(value) and float(value) > 0
    except (TypeError, ValueError):
        return False


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def load_phangs_names() -> set[str]:
    path = EXTERNAL / "phangs" / "phangs_public_sample.csv"
    if not path.exists():
        return set()
    sample = pd.read_csv(path)
    return {norm_name(value) for value in sample.get("Name", pd.Series(dtype=str)).dropna()}


def dustpedia_match_status(galaxy: str, matches: pd.DataFrame) -> tuple[str, str]:
    sub = matches.loc[matches["galaxy"] == galaxy]
    if sub.empty:
        return "NO_LOCAL_DUSTPEDIA_CHECK", ""
    matched = sub.loc[sub["match_status"] == "MATCHED_SOURCE_EVIDENCE"]
    if matched.empty:
        return "NO_DIRECT_DUSTPEDIA_MATCH", ""
    return "DUSTPEDIA_MATCHED", ";".join(sorted(matched["dustpedia_table"].astype(str).unique()))


def phangs_status(galaxy: str, phangs_names: set[str]) -> str:
    return (
        "PHANGS_PUBLIC_SAMPLE_MATCH"
        if variants(galaxy) & phangs_names
        else "NO_PHANGS_PUBLIC_SAMPLE_MATCH"
    )


def source_status(row: pd.Series) -> tuple[str, str]:
    driver = row["observable_driver_type"]
    notes: list[str] = []
    blockers: list[str] = []

    if row["s4g_match_status"] == "S4G_MATCHED":
        notes.append("S4G matched")
    else:
        blockers.append("no S4G match")

    if row["dustpedia_status"] == "DUSTPEDIA_MATCHED":
        notes.append("DustPedia matched")
    else:
        blockers.append("no DustPedia direct match")

    if finite(row["RHI_kpc"]):
        notes.append("SPARC HI radius ready")
    else:
        blockers.append("no SPARC HI radius")

    if row["phangs_status"] == "PHANGS_PUBLIC_SAMPLE_MATCH":
        notes.append("PHANGS public sample match")
    else:
        blockers.append("no PHANGS public sample match")

    components = str(row.get("s4g_model_components", ""))
    disk_source = str(row.get("s4g_disk_component_source", ""))

    if driver == "tail_inner_cutoff_candidate":
        if finite(row["RHI_kpc"]):
            blockers.append("HI extent is not a direct outer-disk transition profile")
            return "PARTIAL_HI_EXTENT_READY_TRANSITION_MISSING", "; ".join(notes + blockers)
        return "KERNEL_SOURCE_MISSING", "; ".join(notes + blockers)

    if driver == "compact_support_candidate":
        if "B" in components and finite(row["bar_radius_kpc"]):
            return "DIRECT_COMPACT_OR_BAR_SUPPORT_READY", "; ".join(notes + ["S4G compact/bar radius ready"])
        if "B" in components:
            blockers.append("S4G bulge component present but no direct compact radius")
            return "PARTIAL_COMPACT_COMPONENT_READY_RADIUS_MISSING", "; ".join(notes + blockers)
        if finite(row["Reff_kpc"]):
            blockers.append("SPARC Reff available but not direct compact support")
            return "PARTIAL_REFF_READY_COMPACT_RADIUS_MISSING", "; ".join(notes + blockers)
        return "KERNEL_SOURCE_MISSING", "; ".join(notes + blockers)

    if driver == "thickness_h_over_rs_candidate":
        if "Z" in components or "edgedisk" in disk_source:
            notes.append("S4G edge-disk component supports vertical candidate")
            return "PARTIAL_EDGE_DISK_VERTICAL_EVIDENCE_READY", "; ".join(notes + blockers)
        blockers.append("no direct vertical scale height / flare / warp measurement")
        return "KERNEL_SOURCE_MISSING_DIRECT_VERTICAL_GEOMETRY", "; ".join(notes + blockers)

    return "NOT_APPLICABLE", "; ".join(notes + blockers)


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    manifest = pd.read_csv(DATA / "s4g75_direct_source_native_acquisition_manifest.csv")
    s4g = pd.read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv").rename(columns={"Galaxy": "galaxy"})
    dust_matches = pd.read_csv(DATA / "morphology_information_gain_dustpedia_matches.csv")
    phangs_names = load_phangs_names()
    accepted = pd.read_csv(DATA / "accepted_morphology_manifest_audit.csv")

    table = (
        manifest.merge(
            s4g[
                [
                    "galaxy",
                    "s4g_match_status",
                    "s4g_name",
                    "s4g_model_components",
                    "s4g_bar_radius_arcsec",
                    "bar_radius_kpc",
                    "candidate_observable_status",
                    "observable_provenance",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        .merge(
            sparc[
                [
                    "galaxy",
                    "D_Mpc",
                    "e_D_Mpc",
                    "Inc_deg",
                    "e_Inc_deg",
                    "Reff_kpc",
                    "Rdisk_kpc",
                    "MHI_1e9Msun",
                    "RHI_kpc",
                    "Ref",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        .merge(
            accepted[["galaxy", "s4g_disk_component_source"]],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
    )
    dust_status = [dustpedia_match_status(galaxy, dust_matches) for galaxy in table["galaxy"]]
    table["dustpedia_status"] = [item[0] for item in dust_status]
    table["dustpedia_tables"] = [item[1] for item in dust_status]
    table["phangs_status"] = [phangs_status(galaxy, phangs_names) for galaxy in table["galaxy"]]
    statuses = [source_status(row) for _, row in table.iterrows()]
    table["kernel_specific_source_status"] = [item[0] for item in statuses]
    table["source_status_notes"] = [item[1] for item in statuses]
    table["accepted_endpoint_ready"] = False
    table["endpoint_scores_computed"] = False
    table["claim_boundary"] = CLAIM_BOUNDARY

    summary = (
        table.groupby(
            [
                "formula_family",
                "observable_driver_type",
                "source_priority",
                "kernel_specific_source_status",
            ],
            as_index=False,
        )
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
        )
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY

    source_coverage = []
    for source_column, positive_status in [
        ("s4g_match_status", "S4G_MATCHED"),
        ("dustpedia_status", "DUSTPEDIA_MATCHED"),
        ("phangs_status", "PHANGS_PUBLIC_SAMPLE_MATCH"),
    ]:
        source_coverage.append(
            {
                "source_column": source_column,
                "positive_status": positive_status,
                "n_positive": int((table[source_column] == positive_status).sum()),
                "n_total": len(table),
                "positive_fraction": float((table[source_column] == positive_status).mean()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    source_coverage.append(
        {
            "source_column": "SPARC_RHI",
            "positive_status": "RHI_kpc_positive",
            "n_positive": int(table["RHI_kpc"].apply(finite).sum()),
            "n_total": len(table),
            "positive_fraction": float(table["RHI_kpc"].apply(finite).mean()),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return table, summary, pd.DataFrame(source_coverage)


def write_report(audit: pd.DataFrame, summary: pd.DataFrame, coverage: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# S4G75 Source-Native Availability Audit",
        "",
        "This audit checks the S4G75 direct source-native acquisition queue against "
        "already acquired local S4G, SPARC/HI, DustPedia, and PHANGS tables. It "
        "is not an endpoint and does not promote accepted labels.",
        "",
        "## Source Coverage",
        "",
        markdown_table(coverage),
        "",
        "## Kernel-Specific Availability Summary",
        "",
        markdown_table(summary),
        "",
        "## Galaxy-Level Availability",
        "",
        markdown_table(
            audit[
                [
                    "galaxy",
                    "formula_family",
                    "source_priority",
                    "observable_driver_type",
                    "kernel_specific_source_status",
                    "s4g_match_status",
                    "dustpedia_status",
                    "phangs_status",
                    "RHI_kpc",
                    "s4g_model_components",
                    "s4g_disk_component_source",
                    "source_status_notes",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "Generic source coverage is not the same as kernel-specific direct "
        "observables. HI radius can support a tail cutoff candidate but does not "
        "by itself provide an outer-disk transition profile. Inclination plus HI "
        "extent can support a thickness proxy but does not provide a vertical "
        "scale height, flare, or warp measurement.",
        "",
    ]
    (REPORTS / "s4g75_source_native_availability_audit.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    audit, summary, coverage = build_audit()
    audit.to_csv(DATA / "s4g75_source_native_availability_audit.csv", index=False)
    summary.to_csv(DATA / "s4g75_source_native_availability_summary.csv", index=False)
    coverage.to_csv(DATA / "s4g75_source_native_availability_source_coverage.csv", index=False)
    write_report(audit, summary, coverage)
    print(f"wrote {DATA / 's4g75_source_native_availability_audit.csv'}")
    print(f"wrote {DATA / 's4g75_source_native_availability_summary.csv'}")
    print(f"wrote {DATA / 's4g75_source_native_availability_source_coverage.csv'}")
    print(f"wrote {REPORTS / 's4g75_source_native_availability_audit.md'}")


if __name__ == "__main__":
    main()
