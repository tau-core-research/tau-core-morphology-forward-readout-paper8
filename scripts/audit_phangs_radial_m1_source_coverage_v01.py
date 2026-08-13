#!/usr/bin/env python3
"""Crossmatch PHANGS-MUSE bodies to source-native radial stellar m1 values."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
from astroquery.vizier import Vizier


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/phangs_radial_m1_source_coverage_v01.md"
PHANGS = ROOT / "data/external/literature/phangs_stuber_2023_muse_morphology_selected_v01.csv"
CATALOG_ID = "J/ApJ/772/135/table1"
M1_NULL_THRESHOLD = 0.1


def normalize(value: object) -> str:
    text = re.sub(r"[^A-Z0-9]", "", str(value).upper())
    match = re.fullmatch(r"(NGC|IC)0*(\d+)", text)
    return text if match is None else match.group(1) + str(int(match.group(2)))


def main() -> None:
    tables = Vizier(columns=["*"], row_limit=-1).get_catalogs(CATALOG_ID)
    if not tables:
        raise RuntimeError(f"VizieR returned no table for {CATALOG_ID}")
    catalog = tables[0].to_pandas()
    catalog["source_name"] = catalog["Name"].map(
        lambda value: value.decode().strip() if isinstance(value, bytes) else str(value).strip()
    )
    catalog["key"] = catalog.source_name.map(normalize)
    lookup = catalog.set_index("key")
    rows = []
    for galaxy in pd.read_csv(PHANGS).galaxy:
        key = normalize(galaxy)
        match = lookup.loc[key] if key in lookup.index else None
        inner = None if match is None else float(match["<A1>i"])
        outer = None if match is None else float(match["<A1>o"])
        certified = (
            match is not None
            and inner < M1_NULL_THRESHOLD
            and outer < M1_NULL_THRESHOLD
        )
        rows.append({
            "galaxy": galaxy,
            "catalog_match": match is not None,
            "source_name": None if match is None else match["source_name"],
            "a1_inner": inner,
            "a1_outer": outer,
            "m1_null_threshold": M1_NULL_THRESHOLD,
            "radial_m1_null_source_certified": certified,
            "selection_uses_velocity_contrast": False,
            "selection_uses_rotation_residual": False,
        })
    frame = pd.DataFrame(rows).sort_values("galaxy")
    certified = frame[frame.radial_m1_null_source_certified]
    result = {
        "schema": "phangs_radial_m1_source_coverage_v01",
        "status": "PHANGS_RADIAL_M1_SOURCE_COVERAGE_AUDITED",
        "catalog_id": CATALOG_ID,
        "population_size": int(len(frame)),
        "catalog_match_count": int(frame.catalog_match.sum()),
        "m1_null_threshold": M1_NULL_THRESHOLD,
        "m1_null_threshold_basis": (
            "conventional 10-percent fractional m1 boundary; frozen before catalog values were queried"
        ),
        "radial_m1_null_certified_count": int(len(certified)),
        "radial_m1_null_certified_bodies": certified.galaxy.tolist(),
        "source_paper": "Zaritsky et al. 2013",
        "source_url": "https://arxiv.org/abs/1305.2940",
        "construction_uses_velocity_contrast": False,
        "construction_uses_rotation_residual": False,
        "claim_boundary": (
            "source-only radial stellar m1 coverage and threshold classification; no tracer velocity endpoint, "
            "channel component, time, quantum, or Tau origin is tested"
        ),
    }
    frame.to_csv(DATA / "phangs_radial_m1_source_coverage_v01.csv", index=False)
    (DATA / "phangs_radial_m1_source_coverage_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        "# PHANGS radial m1 source coverage v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The endpoint-blind VizieR crossmatch covers `{result['catalog_match_count']}` of "
        f"`{result['population_size']}` PHANGS-MUSE bodies. Under the pre-frozen strict "
        f"`A1_inner<0.1` and `A1_outer<0.1` rule, `{result['radial_m1_null_certified_count']}` "
        f"bodies have a source-certified radial stellar `m1` null: "
        f"`{', '.join(result['radial_m1_null_certified_bodies'])}`. No velocity contrast was opened.\n",
        encoding="utf-8",
    )
    print(result["status"], result["radial_m1_null_certified_bodies"])


if __name__ == "__main__":
    main()
