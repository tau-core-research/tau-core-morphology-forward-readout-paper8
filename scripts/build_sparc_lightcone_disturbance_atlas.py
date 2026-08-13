#!/usr/bin/env python3
"""Build a source/path/observation disturbance atlas for the S4G-SPARC sample."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
SOURCE = DATA / "s4g_stellar_asymmetry_attribution_source_v01.csv"
ENVIRONMENT = DATA / "ungc_sparc_tidal_environment_crossmatch_v01.csv"
OUT_CSV = DATA / "sparc_lightcone_disturbance_atlas_v01.csv"
OUT_JSON = DATA / "sparc_lightcone_disturbance_atlas_v01.json"


def source_class(asymmetry: float, theta1: float) -> tuple[str, str]:
    if np.isfinite(theta1):
        if theta1 <= 0:
            return "S0", "Theta1<=0"
        if theta1 <= 1:
            return "S1", "0<Theta1<=1"
        if theta1 <= 2:
            return "S2", "1<Theta1<=2"
        return "S3", "Theta1>2"
    if not np.isfinite(asymmetry):
        return "SX", "no source-disturbance proxy"
    if asymmetry < 0.2:
        return "S0", "A3.6<0.2 proxy"
    if asymmetry < 0.4:
        return "S1", "0.2<=A3.6<0.4 proxy"
    if asymmetry < 0.6:
        return "S2", "0.4<=A3.6<0.6 proxy"
    return "S3", "A3.6>=0.6 proxy"


def observation_class(inclination: float, missing_count: int) -> tuple[str, str]:
    if not np.isfinite(inclination):
        return "OX", "inclination unavailable"
    edge_penalty = 0
    if inclination < 20 or inclination > 85:
        edge_penalty = 3
    elif inclination < 30 or inclination > 80:
        edge_penalty = 2
    elif inclination > 75:
        edge_penalty = 1
    missing_penalty = min(2, missing_count // 2)
    level = min(3, edge_penalty + missing_penalty)
    return f"O{level}", f"inclination={inclination:g};missing_fields={missing_count}"


def main() -> None:
    source = pd.read_csv(SOURCE)
    environment = pd.read_csv(ENVIRONMENT)[
        ["galaxy", "theta1", "main_disturber", "match_status"]
    ]
    joined = source.merge(environment, on="galaxy", how="left", validate="one_to_one")
    missing_columns = [column for column in joined if column.endswith("__missing")]
    rows = []
    for record in joined.to_dict("records"):
        asymmetry = float(record["asymmetry_3p6"]) if pd.notna(record["asymmetry_3p6"]) else np.nan
        theta1 = float(record["theta1"]) if pd.notna(record["theta1"]) else np.nan
        s_class, s_basis = source_class(asymmetry, theta1)
        missing_count = int(sum(float(record[column]) > 0 for column in missing_columns))
        o_class, o_basis = observation_class(float(record["inclination_deg"]), missing_count)
        rows.append({
            "galaxy": record["galaxy"],
            "split": record["split"],
            "source_disturbance_class": s_class,
            "source_disturbance_basis": s_basis,
            "theta1": theta1 if np.isfinite(theta1) else "",
            "main_disturber": record.get("main_disturber", "") if pd.notna(record.get("main_disturber")) else "",
            "asymmetry_3p6": asymmetry if np.isfinite(asymmetry) else "",
            "path_disturbance_class": "PX",
            "path_disturbance_basis": "foreground lightcone catalogue not yet acquired",
            "observation_disturbance_class": o_class,
            "observation_disturbance_basis": o_basis,
            "inclination_deg": record["inclination_deg"],
            "missing_source_fields": missing_count,
            "combined_class": f"{s_class}-PX-{o_class}",
            "endpoint_blind": True,
            "dark_discrepancy_used": False,
        })
    atlas = pd.DataFrame(rows).sort_values("galaxy")
    atlas.to_csv(OUT_CSV, index=False)
    s_counts = atlas["source_disturbance_class"].value_counts().sort_index().to_dict()
    o_counts = atlas["observation_disturbance_class"].value_counts().sort_index().to_dict()
    payload = {
        "schema": "sparc_lightcone_disturbance_atlas_v01",
        "status": "SOURCE_AND_OBSERVATION_CLASSES_READY_PATH_CLASS_BLOCKED",
        "n_galaxies": len(atlas),
        "source_class_counts": s_counts,
        "path_class_counts": {"PX": len(atlas)},
        "observation_class_counts": o_counts,
        "class_semantics": {
            "S": "source-side environmental or asymmetry disturbance proxy",
            "P": "foreground observer-source lightcone/path disturbance",
            "O": "observational geometry and source-field completeness",
            "X": "not classifiable from current source data",
        },
        "path_data_requirements": [
            "foreground objects in an angular cone around every galaxy",
            "foreground redshift or distance separation from the target",
            "mass or luminosity proxy per intervenor",
            "angular impact parameter",
            "Galactic extinction and sky-background fields",
            "weak-lensing convergence/shear proxy where available",
        ],
        "allowed_current_use": "stratify future endpoint results by S and O; P remains unknown",
        "forbidden_current_use": "claim physical lightcone disturbance or fit a path coefficient",
        "verdict": "DISTURBANCE_ATLAS_PARTIAL_P_AXIS_REQUIRES_FOREGROUND_DATA",
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "sparc_lightcone_disturbance_atlas_v01.md").write_text(
        f"""# SPARC Lightcone Disturbance Atlas v0.1

**Status:** `{payload['status']}`

The atlas classifies {len(atlas)} S4G-SPARC galaxies as `(S,P,O)`. Source-side
`S` uses residual-blind `Theta1` where available and otherwise a declared
3.6-micron asymmetry proxy. Observation-side `O` uses inclination and source
field completeness. Every path-side class is `PX`: the current package has no
object-level foreground lightcone catalogue, so it cannot measure physical
path disturbance.

This partial atlas may stratify future tests by source and observational
cleanliness. It may not support a foreground/path-channel coefficient until
the listed intervenor data are acquired.
""", encoding="utf-8")
    print(payload["verdict"])


if __name__ == "__main__":
    main()
