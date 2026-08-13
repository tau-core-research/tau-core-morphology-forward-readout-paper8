#!/usr/bin/env python3
"""Acquire source-native S4G stellar asymmetry and crossmatch it to SPARC."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd
from astroquery.vizier import Vizier


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXTERNAL = ROOT / "data/external/catalogs/s4g_holwerda_2014"
REPORTS = ROOT / "reports"
CATALOG_ID = "J/ApJ/781/12/galaxies"


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
    if not tables:
        raise RuntimeError(f"VizieR returned no table for {CATALOG_ID}")
    catalog = tables[0].to_pandas()
    required = {"channel", "Name", "A", "e_A"}
    missing = sorted(required - set(catalog.columns))
    if missing:
        raise RuntimeError(f"S4G asymmetry columns missing: {missing}")

    selected = catalog[["channel", "Name", "A", "e_A"]].copy()
    selected["channel"] = selected["channel"].map(decode)
    selected["s4g_name"] = selected["Name"].map(decode)
    selected["normalized_name"] = selected["s4g_name"].map(normalize_name)
    selected["asymmetry"] = pd.to_numeric(selected["A"], errors="coerce")
    selected["asymmetry_error"] = pd.to_numeric(selected["e_A"], errors="coerce")
    selected = selected[
        ["channel", "s4g_name", "normalized_name", "asymmetry", "asymmetry_error"]
    ].sort_values(["channel", "normalized_name"])

    EXTERNAL.mkdir(parents=True, exist_ok=True)
    raw_path = EXTERNAL / "s4g_holwerda_asymmetry_selected_v01.csv"
    selected.to_csv(raw_path, index=False)

    channel_frames = {}
    for channel, suffix in (("3.6um", "3p6"), ("4.5um", "4p5")):
        frame = selected.loc[selected["channel"].eq(channel)].copy()
        duplicate = frame["normalized_name"].duplicated(keep=False)
        if duplicate.any():
            names = sorted(frame.loc[duplicate, "normalized_name"].unique())
            raise RuntimeError(f"Duplicate {channel} normalized names: {names[:10]}")
        channel_frames[suffix] = frame.set_index("normalized_name")

    sparc_path = DATA / "external_sparc_master_table.csv"
    sparc = pd.read_csv(sparc_path)
    rows = []
    for _, source in sparc.iterrows():
        galaxy = str(source["Galaxy"])
        normalized = normalize_name(galaxy)
        row = {
            "galaxy": galaxy,
            "normalized_sparc_name": normalized,
            "sparc_distance_mpc": source["D_Mpc"],
        }
        matched_channels = 0
        for suffix in ("3p6", "4p5"):
            frame = channel_frames[suffix]
            if normalized in frame.index:
                match = frame.loc[normalized]
                row[f"s4g_name_{suffix}"] = match["s4g_name"]
                row[f"asymmetry_{suffix}"] = match["asymmetry"]
                row[f"asymmetry_error_{suffix}"] = match["asymmetry_error"]
                matched_channels += 1
            else:
                row[f"s4g_name_{suffix}"] = None
                row[f"asymmetry_{suffix}"] = None
                row[f"asymmetry_error_{suffix}"] = None
        row["match_status"] = (
            "UNIQUE_TWO_CHANNEL_NAME_MATCH"
            if matched_channels == 2
            else "INCOMPLETE_OR_NO_MATCH"
        )
        row["source_catalog"] = CATALOG_ID
        row["source_paper"] = "Holwerda_et_al_2014_ApJ_781_12"
        row["source_url"] = "https://cdsarc.cds.unistra.fr/viz-bin/cat/J/ApJ/781/12"
        row["residual_blind"] = True
        row["velocity_endpoint_used"] = False
        row["claim_boundary"] = "source_only_stellar_asymmetry_crossmatch_not_endpoint"
        rows.append(row)

    crossmatch = pd.DataFrame(rows)
    crossmatch_path = DATA / "s4g_stellar_asymmetry_crossmatch_v01.csv"
    crossmatch.to_csv(crossmatch_path, index=False)
    usable = crossmatch.loc[
        crossmatch["match_status"].eq("UNIQUE_TWO_CHANNEL_NAME_MATCH")
        & crossmatch["asymmetry_3p6"].notna()
        & crossmatch["asymmetry_4p5"].notna()
    ]

    provenance = {
        "schema": "s4g_stellar_asymmetry_source_v01",
        "status": "SOURCE_ONLY_S4G_STELLAR_ASYMMETRY_ACQUIRED",
        "catalog_id": CATALOG_ID,
        "catalog_rows": int(len(selected)),
        "catalog_galaxies_per_channel": 2345,
        "sparc_rows": int(len(crossmatch)),
        "usable_two_channel_matches": int(len(usable)),
        "asymmetry_definition": (
            "scale-independent 180-degree rotational asymmetry of S4G near-infrared light"
        ),
        "endpoint_access": False,
        "raw_selected_sha256": sha256(raw_path),
        "sparc_source_sha256": sha256(sparc_path),
        "crossmatch_sha256": sha256(crossmatch_path),
        "source_paper_arxiv": "https://arxiv.org/abs/1309.1444",
        "source_paper_doi": "10.1088/0004-637X/781/1/12",
        "claim_boundary": "source_acquisition_only_not_m_tau_attribution",
    }
    provenance_path = DATA / "s4g_stellar_asymmetry_source_v01.json"
    provenance_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "s4g_stellar_asymmetry_source_v01.md"
    report_path.write_text(
        f"""# S4G Stellar Asymmetry Source v0.1

**Status:** `SOURCE_ONLY_S4G_STELLAR_ASYMMETRY_ACQUIRED`

The Holwerda et al. S4G quantified-morphology catalog was acquired from
VizieR `{CATALOG_ID}`. The selected coordinate is the rotational asymmetry
`A`, measured independently in the 3.6 and 4.5 micron images.

| quantity | count |
| --- | ---: |
| catalog rows (two channels) | {len(selected)} |
| SPARC rows | {len(crossmatch)} |
| usable two-channel matches | {len(usable)} |

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
