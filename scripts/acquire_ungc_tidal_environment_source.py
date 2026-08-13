#!/usr/bin/env python3
"""Acquire the UNGC tidal index and build an endpoint-blind SPARC crossmatch."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd
from astroquery.vizier import Vizier


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXTERNAL = ROOT / "data/external/catalogs/ungc_2013"
REPORTS = ROOT / "reports"
CATALOG_ID = "J/AJ/145/101/catalog"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_name(value: object) -> str:
    text = re.sub(r"[^A-Z0-9]", "", str(value).upper())
    for prefix in ("NGC", "UGC", "IC", "DDO"):
        match = re.fullmatch(prefix + r"0*(\d+)", text)
        if match:
            return prefix + str(int(match.group(1)))
    match = re.fullmatch(r"ESO0*(\d+)G?0*(\d+)", text)
    if match:
        return "ESO" + str(int(match.group(1))) + "G" + str(int(match.group(2)))
    return text


def main() -> None:
    vizier = Vizier(columns=["*"], row_limit=-1)
    tables = vizier.get_catalogs(CATALOG_ID)
    if not tables:
        raise RuntimeError(f"VizieR returned no table for {CATALOG_ID}")
    catalog = tables[0].to_pandas()
    required = {"Name", "Dist", "Ti1", "SimbadName", "NEDname"}
    missing = sorted(required - set(catalog.columns))
    if missing:
        raise RuntimeError(f"UNGC columns missing: {missing}")

    selected = catalog[
        ["Name", "Dist", "Ti1", "SimbadName", "NEDname"]
    ].copy()
    selected.columns = [
        "ungc_name",
        "ungc_distance_mpc",
        "theta1",
        "simbad_name",
        "ned_name",
    ]
    for column in selected.select_dtypes(include="object").columns:
        selected[column] = selected[column].apply(
            lambda value: value.decode().strip()
            if isinstance(value, bytes)
            else str(value).strip()
        )
    selected["theta1"] = pd.to_numeric(selected["theta1"], errors="coerce")
    selected["ungc_distance_mpc"] = pd.to_numeric(
        selected["ungc_distance_mpc"], errors="coerce"
    )

    EXTERNAL.mkdir(parents=True, exist_ok=True)
    raw_path = EXTERNAL / "ungc_catalog_selected_v01.csv"
    selected.to_csv(raw_path, index=False)

    sparc_path = DATA / "external_sparc_master_table.csv"
    sparc = pd.read_csv(sparc_path)
    alias_lookup: dict[str, set[int]] = {}
    for index, row in selected.iterrows():
        for column in ("ungc_name", "simbad_name", "ned_name"):
            normalized = normalize_name(row[column])
            if normalized and normalized != "NAN":
                alias_lookup.setdefault(normalized, set()).add(index)

    rows = []
    for _, source in sparc.iterrows():
        galaxy = str(source["Galaxy"])
        normalized = normalize_name(galaxy)
        candidates = sorted(alias_lookup.get(normalized, set()))
        status = "NO_MATCH"
        match = None
        if len(candidates) == 1:
            status = "UNIQUE_NAME_MATCH"
            match = selected.loc[candidates[0]]
        elif len(candidates) > 1:
            status = "AMBIGUOUS_NAME_MATCH"
        rows.append(
            {
                "galaxy": galaxy,
                "normalized_sparc_name": normalized,
                "match_status": status,
                "ungc_name": None if match is None else match["ungc_name"],
                "theta1": None if match is None else match["theta1"],
                "ungc_distance_mpc": None
                if match is None
                else match["ungc_distance_mpc"],
                "main_disturber": None,
                "sparc_distance_mpc": source["D_Mpc"],
                "source_catalog": CATALOG_ID,
                "source_paper": "Karachentsev_Makarov_Kaisina_2013_AJ_145_101",
                "source_url": "https://cdsarc.cds.unistra.fr/viz-bin/cat/J/AJ/145/101",
                "residual_blind": True,
                "velocity_endpoint_used": False,
                "claim_boundary": "source_only_tidal_environment_crossmatch_not_endpoint",
            }
        )

    crossmatch = pd.DataFrame(rows)
    crossmatch_path = DATA / "ungc_sparc_tidal_environment_crossmatch_v01.csv"
    crossmatch.to_csv(crossmatch_path, index=False)
    usable = crossmatch.loc[
        crossmatch["match_status"].eq("UNIQUE_NAME_MATCH")
        & crossmatch["theta1"].notna()
    ]

    provenance = {
        "schema": "ungc_sparc_tidal_environment_source_v01",
        "status": "SOURCE_ONLY_TIDAL_ENVIRONMENT_ACQUIRED",
        "catalog_id": CATALOG_ID,
        "catalog_rows": int(len(selected)),
        "sparc_rows": int(len(crossmatch)),
        "unique_matches": int(crossmatch["match_status"].eq("UNIQUE_NAME_MATCH").sum()),
        "usable_theta1_matches": int(len(usable)),
        "ambiguous_matches": int(
            crossmatch["match_status"].eq("AMBIGUOUS_NAME_MATCH").sum()
        ),
        "theta1_definition": (
            "maximum dominant-neighbor tidal influence; positive values indicate "
            "group membership and negative values isolation under the source catalog"
        ),
        "endpoint_access": False,
        "raw_selected_sha256": sha256(raw_path),
        "sparc_source_sha256": sha256(sparc_path),
        "crossmatch_sha256": sha256(crossmatch_path),
        "source_paper_arxiv": "https://arxiv.org/abs/1303.5328",
        "claim_boundary": "source_acquisition_only_not_m_tau_attribution",
    }
    provenance_path = DATA / "ungc_sparc_tidal_environment_source_v01.json"
    provenance_path.write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "ungc_sparc_tidal_environment_source_v01.md"
    report_path.write_text(
        f"""# UNGC-SPARC Tidal Environment Source v0.1

**Status:** `SOURCE_ONLY_TIDAL_ENVIRONMENT_ACQUIRED`

The Updated Nearby Galaxy Catalog was acquired from VizieR catalog
`{CATALOG_ID}`. Three source identifiers were normalized for a name-only SPARC
crossmatch. Ambiguous matches are rejected.

| quantity | count |
| --- | ---: |
| UNGC rows | {len(selected)} |
| SPARC rows | {len(crossmatch)} |
| unique name matches | {provenance['unique_matches']} |
| usable numeric Theta1 matches | {len(usable)} |
| ambiguous matches | {provenance['ambiguous_matches']} |

`Theta1` measures the strongest neighboring tidal influence. Positive values
mark group-bound systems under the catalog definition; negative values mark
isolated systems.

This acquisition reads no observed rotation velocity, residual, RMSE, model
score, or endpoint artifact. It does not claim a Tau Core signal.
""",
        encoding="utf-8",
    )
    print(provenance["status"])
    print(raw_path)
    print(crossmatch_path)
    print(provenance_path)
    print(report_path)


if __name__ == "__main__":
    main()
