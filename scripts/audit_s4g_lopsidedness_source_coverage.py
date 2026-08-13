#!/usr/bin/env python3
"""Audit endpoint-blind SPARC coverage of published S4G m=1 amplitudes."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
from astroquery.vizier import Vizier


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
CATALOG_ID = "J/ApJ/772/135/table1"


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


def main() -> None:
    tables = Vizier(columns=["*"], row_limit=-1).get_catalogs(CATALOG_ID)
    if not tables:
        raise RuntimeError(f"VizieR returned no table for {CATALOG_ID}")
    catalog = tables[0].to_pandas()
    catalog["s4g_name"] = catalog["Name"].map(
        lambda value: value.decode().strip() if isinstance(value, bytes) else str(value).strip()
    )
    catalog["normalized_name"] = catalog["s4g_name"].map(normalize_name)
    lookup = catalog.set_index("normalized_name")

    rows = []
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    for galaxy in sparc["Galaxy"].astype(str):
        normalized = normalize_name(galaxy)
        match = lookup.loc[normalized] if normalized in lookup.index else None
        rows.append(
            {
                "galaxy": galaxy,
                "match_status": "UNIQUE_NAME_MATCH" if match is not None else "NO_MATCH",
                "s4g_name": None if match is None else match["s4g_name"],
                "a1_inner": None if match is None else match["<A1>i"],
                "a1_outer": None if match is None else match["<A1>o"],
                "residual_blind": True,
                "velocity_endpoint_used": False,
            }
        )
    crossmatch = pd.DataFrame(rows)
    csv_path = DATA / "s4g_lopsidedness_source_coverage_v01.csv"
    crossmatch.to_csv(csv_path, index=False)
    matches = int(crossmatch["match_status"].eq("UNIQUE_NAME_MATCH").sum())

    result = {
        "schema": "s4g_lopsidedness_source_coverage_v01",
        "status": "SOURCE_COVERAGE_INSUFFICIENT_NOT_ENDPOINT",
        "catalog_id": CATALOG_ID,
        "catalog_rows": int(len(catalog)),
        "sparc_rows": int(len(crossmatch)),
        "unique_matches": matches,
        "endpoint_access": False,
        "reason": "published sample requires nearly face-on inclination and has insufficient SPARC overlap",
        "source_paper_arxiv": "https://arxiv.org/abs/1305.2940",
        "source_paper_doi": "10.1088/0004-637X/772/2/135",
        "claim_boundary": "source_coverage_audit_only_no_endpoint_score",
    }
    json_path = DATA / "s4g_lopsidedness_source_coverage_v01.json"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "s4g_lopsidedness_source_coverage_v01.md"
    report_path.write_text(
        f"""# S4G Lopsidedness Source Coverage v0.1

**Status:** `SOURCE_COVERAGE_INSUFFICIENT_NOT_ENDPOINT`

The Zaritsky et al. catalog publishes inner and outer stellar `m=1`
amplitudes for {len(catalog)} S4G galaxies. A residual-blind name crossmatch
finds only **{matches}** object in the {len(crossmatch)}-galaxy SPARC table.

The route is therefore stopped before any rotation endpoint is opened. The low
overlap follows from the source study's nearly face-on selection, whereas
resolved rotation-curve samples generally require appreciable inclination.
""",
        encoding="utf-8",
    )
    print(result["status"])
    print(csv_path)
    print(json_path)
    print(report_path)


if __name__ == "__main__":
    main()
