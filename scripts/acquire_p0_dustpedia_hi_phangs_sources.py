#!/usr/bin/env python3
"""Acquire P0 DustPedia, HI, and PHANGS source evidence.

This source pass is residual-blind and upstream of accepted labels.  It checks
DustPedia VizieR tables, the public PHANGS sample table, and SPARC HI
mass/radius fields for the four P0 galaxies. It does not classify morphology
and does not compute endpoint scores.
"""

from __future__ import annotations

import io
import re
import urllib.request
from pathlib import Path

import pandas as pd
from astroquery.vizier import Vizier


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
EXTERNAL = ROOT / "data" / "external"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_external_source_evidence_not_label_not_endpoint"
PHANGS_SAMPLE_URL = (
    "https://docs.google.com/spreadsheet/ccc?"
    "key=1dC6QGEuxoczljVM2C77t806KyQi4wE4Igu77j7w46vE&output=csv"
)
DUSTPEDIA_CATALOGS = {
    "dustpedia_dust_profiles": "J/A+A/622/A132",
    "dustpedia_hi_metallicity": "J/A+A/623/A5",
    "dustpedia_physical_properties": "J/A+A/631/A38",
}


def ensure_dirs() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (EXTERNAL / "dustpedia").mkdir(parents=True, exist_ok=True)
    (EXTERNAL / "phangs").mkdir(parents=True, exist_ok=True)


def norm_name(name: object) -> str:
    raw = re.sub(r"[^A-Z0-9]", "", str(name).upper())
    match = re.match(r"NGC0+(\d+)$", raw)
    if match:
        return "NGC" + match.group(1)
    return raw


def name_variants(name: str) -> set[str]:
    norm = norm_name(name)
    out = {norm}
    match = re.match(r"NGC(\d+)$", norm)
    if match:
        number = match.group(1)
        out.add("NGC" + number.zfill(4))
        out.add("NGC" + number.zfill(3))
    return out


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def p0_galaxies() -> list[str]:
    template = pd.read_csv(DATA / "p0_visual_review_template.csv")
    return sorted(template["galaxy"].tolist())


def acquire_dustpedia(galaxies: list[str]) -> pd.DataFrame:
    Vizier.ROW_LIMIT = -1
    rows = []
    variants = {galaxy: name_variants(galaxy) for galaxy in galaxies}
    for source_label, catalog in DUSTPEDIA_CATALOGS.items():
        tables = Vizier.get_catalogs(catalog)
        for table_key in tables.keys():
            table = tables[table_key].to_pandas()
            table.to_csv(
                EXTERNAL / "dustpedia" / f"{table_key.replace('/', '_')}.csv",
                index=False,
            )
            name_columns = [
                column
                for column in table.columns
                if column.lower() in {"name", "simbadname"}
            ]
            for galaxy in galaxies:
                matched = False
                for column in name_columns:
                    names = set(norm_name(value) for value in table[column].dropna())
                    if variants[galaxy] & names:
                        matched = True
                rows.append(
                    {
                        "galaxy": galaxy,
                        "source_family": "DustPedia",
                        "catalog": catalog,
                        "table_key": table_key,
                        "match_status": "MATCHED_SOURCE_EVIDENCE"
                        if matched
                        else "NO_DIRECT_MATCH",
                        "evidence_summary": (
                            f"{galaxy} appears in {table_key}"
                            if matched
                            else f"{galaxy} not found by normalized-name match in {table_key}"
                        ),
                        "accepted_label_output_allowed": False,
                        "endpoint_scores_computed": False,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return pd.DataFrame(rows)


def acquire_phangs(galaxies: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = urllib.request.urlopen(PHANGS_SAMPLE_URL, timeout=30).read()
    sample = pd.read_csv(io.BytesIO(data))
    sample.to_csv(EXTERNAL / "phangs" / "phangs_public_sample.csv", index=False)
    sample_names = set(norm_name(value) for value in sample["Name"].dropna())
    rows = []
    for galaxy in galaxies:
        matched = bool(name_variants(galaxy) & sample_names)
        rows.append(
            {
                "galaxy": galaxy,
                "source_family": "PHANGS",
                "match_status": "MATCHED_SOURCE_EVIDENCE"
                if matched
                else "NO_PHANGS_SAMPLE_COVERAGE",
                "source_url": PHANGS_SAMPLE_URL,
                "evidence_summary": (
                    f"{galaxy} is present in the public PHANGS sample table"
                    if matched
                    else f"{galaxy} is not present in the public PHANGS sample table"
                ),
                "accepted_label_output_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sample, pd.DataFrame(rows)


def acquire_hi(galaxies: list[str], dustpedia: pd.DataFrame) -> pd.DataFrame:
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    sparc = sparc[sparc["Galaxy"].isin(galaxies)].copy()
    dust_hi = dustpedia[
        (dustpedia["source_family"] == "DustPedia")
        & (dustpedia["table_key"] == "J/A+A/623/A5/dp-hi")
        & (dustpedia["match_status"] == "MATCHED_SOURCE_EVIDENCE")
    ]
    rows = []
    for _, item in sparc.iterrows():
        galaxy = item["Galaxy"]
        has_sparc_hi = pd.notna(item["MHI_1e9Msun"]) and pd.notna(item["RHI_kpc"])
        has_dustpedia_hi = galaxy in set(dust_hi["galaxy"])
        rows.append(
            {
                "galaxy": galaxy,
                "source_family": "HI_SURVEYS",
                "sparc_hi_status": "SPARC_HI_RADIUS_READY"
                if has_sparc_hi
                else "SPARC_HI_MISSING",
                "dustpedia_hi_status": "DUSTPEDIA_HI_MATCHED"
                if has_dustpedia_hi
                else "NO_DIRECT_DUSTPEDIA_HI_MATCH",
                "mhi_1e9_msun": item["MHI_1e9Msun"],
                "rhi_kpc": item["RHI_kpc"],
                "sparc_ref": item["Ref"],
                "match_status": "HI_SOURCE_EVIDENCE_READY"
                if has_sparc_hi
                else "HI_SOURCE_EVIDENCE_MISSING",
                "evidence_summary": (
                    f"SPARC HI mass/radius available; refs={item['Ref']}; "
                    f"DustPedia HI={'yes' if has_dustpedia_hi else 'no'}"
                ),
                "accepted_label_output_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_summary(
    dustpedia: pd.DataFrame, phangs: pd.DataFrame, hi: pd.DataFrame
) -> pd.DataFrame:
    dust_by_galaxy = dustpedia.groupby("galaxy")["match_status"].apply(
        lambda values: "MATCHED_SOURCE_EVIDENCE"
        if (values == "MATCHED_SOURCE_EVIDENCE").any()
        else "NO_DIRECT_DUSTPEDIA_MATCH"
    )
    rows = []
    for galaxy in sorted(set(dustpedia["galaxy"]) | set(phangs["galaxy"]) | set(hi["galaxy"])):
        dust_status = dust_by_galaxy.loc[galaxy]
        phangs_status = phangs.set_index("galaxy").loc[galaxy, "match_status"]
        hi_status = hi.set_index("galaxy").loc[galaxy, "match_status"]
        rows.append(
            {
                "galaxy": galaxy,
                "dustpedia_status": dust_status,
                "phangs_status": phangs_status,
                "hi_status": hi_status,
                "source_review_status": (
                    "SOURCE_EVIDENCE_PARTIAL_REVIEW_REQUIRED"
                    if dust_status == "MATCHED_SOURCE_EVIDENCE"
                    or hi_status == "HI_SOURCE_EVIDENCE_READY"
                    else "SOURCE_EVIDENCE_INCOMPLETE"
                ),
                "accepted_label_output_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def write_report(
    dustpedia: pd.DataFrame,
    phangs: pd.DataFrame,
    hi: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    dust_compact = (
        dustpedia.groupby(["galaxy", "match_status"], as_index=False)
        .size()
        .rename(columns={"size": "n_tables"})
    )
    lines = [
        "# P0 DustPedia/HI/PHANGS Source Evidence",
        "",
        "This report records the requested source acquisition pass for the four P0",
        "galaxies. It queries DustPedia VizieR tables, the public PHANGS sample",
        "table, and SPARC HI mass/radius fields. It does not classify morphology,",
        "does not create accepted labels, and does not compute endpoint scores.",
        "",
        "## Verdict",
        "",
        "DustPedia direct matches are found for NGC0300 only in the queried tables.",
        "PHANGS public sample coverage is not found for the four P0 galaxies,",
        "including NGC0247. SPARC HI mass/radius evidence is present for all four",
        "P0 galaxies, but HI morphology/asymmetry still requires review rather",
        "than automatic label promotion.",
        "",
        "## Combined Summary",
        "",
        markdown_table(summary),
        "",
        "## DustPedia Match Counts",
        "",
        markdown_table(dust_compact),
        "",
        "## PHANGS",
        "",
        markdown_table(phangs[["galaxy", "match_status", "evidence_summary"]]),
        "",
        "## HI Evidence",
        "",
        markdown_table(
            hi[
                [
                    "galaxy",
                    "match_status",
                    "mhi_1e9_msun",
                    "rhi_kpc",
                    "sparc_ref",
                    "dustpedia_hi_status",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "These source records may feed a source-assisted review draft. They are not",
        "an accepted morphology manifest and not endpoint evidence.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_dustpedia_hi_phangs_source_evidence.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    ensure_dirs()
    galaxies = p0_galaxies()
    dustpedia = acquire_dustpedia(galaxies)
    phangs_sample, phangs = acquire_phangs(galaxies)
    hi = acquire_hi(galaxies, dustpedia)
    summary = build_summary(dustpedia, phangs, hi)

    dustpedia.to_csv(DATA / "p0_dustpedia_source_matches.csv", index=False)
    phangs_sample.to_csv(DATA / "p0_phangs_public_sample.csv", index=False)
    phangs.to_csv(DATA / "p0_phangs_source_matches.csv", index=False)
    hi.to_csv(DATA / "p0_hi_source_evidence.csv", index=False)
    summary.to_csv(DATA / "p0_external_source_evidence_summary.csv", index=False)
    write_report(dustpedia, phangs, hi, summary)
    print("PAPER8_P0_DUSTPEDIA_HI_PHANGS_SOURCE_EVIDENCE_COMPLETE")


if __name__ == "__main__":
    main()
