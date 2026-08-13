#!/usr/bin/env python3
"""Acquire S4G disk-break radii and build an endpoint-blind SPARC crossmatch."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd
from astroquery.vizier import Vizier


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXTERNAL = ROOT / "data/external/catalogs/s4g_disk_breaks_2014"
REPORTS = ROOT / "reports"
CATALOG_ID = "J/MNRAS/441/1992"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_name(value: object) -> str:
    text = re.sub(r"[^A-Z0-9]", "", str(value).upper())
    for prefix in ("NGC", "UGC", "IC", "DDO"):
        match = re.fullmatch(prefix + r"0*(\d+)", text)
        if match:
            return prefix + str(int(match.group(1)))
    match = re.fullmatch(r"ESO0*(\d+)[G-]?0*(\d+)", text)
    if match:
        return "ESO" + str(int(match.group(1))) + "G" + str(int(match.group(2)))
    return text


def decode(value: object) -> str:
    return value.decode().strip() if isinstance(value, bytes) else str(value).strip()


def main() -> None:
    tables = Vizier(columns=["*"], row_limit=-1).get_catalogs(CATALOG_ID)
    if len(tables) != 2:
        raise RuntimeError(f"Expected two VizieR tables for {CATALOG_ID}")
    properties = tables[0].to_pandas()
    profiles = tables[1].to_pandas()
    for frame in (properties, profiles):
        frame["source_name"] = frame["Name"].map(decode)
        frame["normalized_name"] = frame["source_name"].map(normalize_name)

    selected = profiles[
        [
            "source_name",
            "normalized_name",
            "Prof",
            "Rb.pc",
            "e_Rb.pc",
            "hi.pc",
            "e_hi.pc",
            "ho.pc",
            "e_ho.pc",
        ]
    ].copy()
    selected.columns = [
        "source_name",
        "normalized_name",
        "profile_type",
        "break_radius_kpc",
        "break_radius_error_kpc",
        "inner_scale_kpc",
        "inner_scale_error_kpc",
        "outer_scale_kpc",
        "outer_scale_error_kpc",
    ]
    selected["profile_type"] = selected["profile_type"].map(decode)
    for column in selected.columns[3:]:
        selected[column] = pd.to_numeric(selected[column], errors="coerce")
    selected = selected.sort_values(["normalized_name", "profile_type"])

    EXTERNAL.mkdir(parents=True, exist_ok=True)
    raw_path = EXTERNAL / "s4g_disk_break_profiles_selected_v01.csv"
    selected.to_csv(raw_path, index=False)

    grouped = {name: group for name, group in selected.groupby("normalized_name")}
    sparc_path = DATA / "external_sparc_master_table.csv"
    sparc = pd.read_csv(sparc_path)
    rows = []
    for _, source in sparc.iterrows():
        galaxy = str(source["Galaxy"])
        normalized = normalize_name(galaxy)
        candidates = grouped.get(normalized)
        status = "NO_MATCH"
        match = None
        if candidates is not None and len(candidates) == 1:
            status = "UNIQUE_NAME_MATCH"
            match = candidates.iloc[0]
        elif candidates is not None:
            status = "MULTIPLE_PROFILE_ROWS"
        rows.append(
            {
                "galaxy": galaxy,
                "normalized_sparc_name": normalized,
                "match_status": status,
                "source_name": None if match is None else match["source_name"],
                "profile_type": None if match is None else match["profile_type"],
                "break_radius_kpc": None if match is None else match["break_radius_kpc"],
                "break_radius_error_kpc": None
                if match is None
                else match["break_radius_error_kpc"],
                "inner_scale_kpc": None if match is None else match["inner_scale_kpc"],
                "outer_scale_kpc": None if match is None else match["outer_scale_kpc"],
                "sparc_rdisk_kpc": source["Rdisk_kpc"],
                "source_catalog": CATALOG_ID,
                "source_paper": "Laine_et_al_2014_MNRAS_441_1992",
                "source_url": "https://cdsarc.cds.unistra.fr/viz-bin/cat/J/MNRAS/441/1992",
                "residual_blind": True,
                "velocity_endpoint_used": False,
                "claim_boundary": "source_only_disk_break_crossmatch_not_endpoint",
            }
        )

    crossmatch = pd.DataFrame(rows)
    crossmatch_path = DATA / "s4g_disk_break_onset_source_v01.csv"
    crossmatch.to_csv(crossmatch_path, index=False)
    matches = crossmatch.loc[crossmatch["match_status"].eq("UNIQUE_NAME_MATCH")]
    numeric = matches.loc[matches["break_radius_kpc"].notna()]

    result = {
        "schema": "s4g_disk_break_onset_source_v01",
        "status": "SOURCE_ONLY_S4G_DISK_BREAK_ONSET_ACQUIRED_SMALL_SAMPLE",
        "catalog_id": CATALOG_ID,
        "catalog_profile_rows": int(len(selected)),
        "sparc_rows": int(len(crossmatch)),
        "unique_matches": int(len(matches)),
        "numeric_break_matches": int(len(numeric)),
        "endpoint_access": False,
        "source_paper_arxiv": "https://arxiv.org/abs/1404.0559",
        "source_paper_doi": "10.1093/mnras/stu628",
        "raw_selected_sha256": sha256(raw_path),
        "crossmatch_sha256": sha256(crossmatch_path),
        "claim_boundary": "source_acquisition_only_small_sample_not_channel_attribution",
    }
    json_path = DATA / "s4g_disk_break_onset_source_v01.json"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "s4g_disk_break_onset_source_v01.md"
    report_path.write_text(
        f"""# S4G Disk-Break Onset Source v0.1

**Status:** `SOURCE_ONLY_S4G_DISK_BREAK_ONSET_ACQUIRED_SMALL_SAMPLE`

| quantity | count |
| --- | ---: |
| catalog profile rows | {len(selected)} |
| SPARC rows | {len(crossmatch)} |
| unique name matches | {len(matches)} |
| numeric break-radius matches | {len(numeric)} |

The source coordinate is the published 3.6 micron disk break radius. No
rotation velocity, residual, mass discrepancy, dynamic onset, or endpoint
score is read. The numeric overlap is too small for a population claim.
""",
        encoding="utf-8",
    )
    print(result["status"])
    print(crossmatch_path)
    print(json_path)
    print(report_path)


if __name__ == "__main__":
    main()
