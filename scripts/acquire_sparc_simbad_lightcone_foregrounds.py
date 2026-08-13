#!/usr/bin/env python3
"""Acquire a residual-blind SIMBAD cone census for the S4G-SPARC sample."""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import astropy.units as u
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
SOURCE = DATA / "sparc_lightcone_disturbance_atlas_v01.csv"
OBJECTS_OUT = DATA / "sparc_simbad_lightcone_objects_v01.csv"
SUMMARY_OUT = DATA / "sparc_simbad_lightcone_foregrounds_v01.csv"
META_OUT = DATA / "sparc_simbad_lightcone_foregrounds_v01.json"
CONE_ARCMIN = 10.0
EXTRAGALACTIC_OTYPES = {
    "G", "EmG", "GiC", "GiG", "BiC", "IG", "PaG", "GrG", "CGG",
    "AGN", "AG?", "Sy1", "Sy2", "LIN", "QSO", "BLL",
}


def normalize_name(name: str) -> str:
    if name.startswith("NGC") and name[3:].isdigit():
        return f"NGC {int(name[3:])}"
    if name.startswith("UGC") and name[3:].isdigit():
        return f"UGC {int(name[3:])}"
    if name.startswith("IC") and name[2:].isdigit():
        return f"IC {int(name[2:])}"
    return name


def is_extragalactic(otype: str) -> bool:
    return otype.strip() in EXTRAGALACTIC_OTYPES


def main() -> None:
    names = pd.read_csv(SOURCE)["galaxy"].tolist()
    resolver = Simbad()
    resolver.add_votable_fields("otype", "rvz_redshift")
    resolved = resolver.query_objects([normalize_name(name) for name in names])
    if resolved is None or len(resolved) != len(names):
        raise RuntimeError("SIMBAD batch resolution did not preserve the target list")

    cone = Simbad()
    cone.add_votable_fields("otype", "rvz_redshift")
    object_rows = []
    summary_rows = []
    for index, galaxy in enumerate(names):
        target = resolved[index]
        if np.ma.is_masked(target["ra"]) or np.ma.is_masked(target["dec"]):
            summary_rows.append({"galaxy": galaxy, "query_status": "TARGET_UNRESOLVED"})
            continue
        ra = float(target["ra"])
        dec = float(target["dec"])
        target_z = float(target["rvz_redshift"]) if not np.ma.is_masked(target["rvz_redshift"]) else np.nan
        coordinate = SkyCoord(ra, dec, unit="deg")
        table = None
        error_text = ""
        for attempt in range(3):
            try:
                table = cone.query_region(coordinate, radius=CONE_ARCMIN * u.arcmin)
                break
            except Exception as error:  # network service retry
                error_text = str(error)
                time.sleep(1.5 * (attempt + 1))
        if table is None:
            summary_rows.append({
                "galaxy": galaxy, "ra_deg": ra, "dec_deg": dec,
                "target_redshift": target_z if np.isfinite(target_z) else "",
                "query_status": f"QUERY_FAILED:{error_text[:120]}",
            })
            continue

        foreground_count = 0
        foreground_weight = 0.0
        background_count = 0
        stellar_count = 0
        for row in table:
            object_coord = SkyCoord(float(row["ra"]), float(row["dec"]), unit="deg")
            separation = float(coordinate.separation(object_coord).arcmin)
            if separation < 0.05:
                continue
            otype = str(row["otype"])
            redshift = float(row["rvz_redshift"]) if not np.ma.is_masked(row["rvz_redshift"]) else np.nan
            extragalactic = is_extragalactic(otype)
            foreground = bool(
                extragalactic and np.isfinite(redshift) and redshift > 0
                and np.isfinite(target_z) and redshift < target_z - 0.0002
            )
            background = bool(
                extragalactic and np.isfinite(redshift) and np.isfinite(target_z)
                and redshift > target_z + 0.0002
            )
            stellar = "*" in otype
            if foreground:
                foreground_count += 1
                foreground_weight += 1.0 / (separation**2 + 0.25**2)
            background_count += int(background)
            stellar_count += int(stellar)
            object_rows.append({
                "target_galaxy": galaxy,
                "target_ra_deg": ra,
                "target_dec_deg": dec,
                "target_redshift": target_z if np.isfinite(target_z) else "",
                "object_id": str(row["main_id"]),
                "object_type": otype,
                "object_redshift": redshift if np.isfinite(redshift) else "",
                "separation_arcmin": separation,
                "is_extragalactic_with_redshift": extragalactic and np.isfinite(redshift),
                "is_foreground_candidate": foreground,
                "is_background_control": background,
                "is_stellar_crowding_control": stellar,
            })
        if not np.isfinite(target_z):
            path_class = "PX"
        elif foreground_count == 0:
            path_class = "P0"
        elif foreground_count == 1 and foreground_weight < 0.25:
            path_class = "P1"
        elif foreground_count <= 3 and foreground_weight < 1.0:
            path_class = "P2"
        else:
            path_class = "P3"
        summary_rows.append({
            "galaxy": galaxy,
            "ra_deg": ra,
            "dec_deg": dec,
            "target_redshift": target_z if np.isfinite(target_z) else "",
            "cone_radius_arcmin": CONE_ARCMIN,
            "foreground_candidate_count": foreground_count,
            "foreground_inverse_angle_weight": foreground_weight,
            "background_redshift_control_count": background_count,
            "stellar_crowding_control_count": stellar_count,
            "path_disturbance_class": path_class,
            "query_status": "OK",
        })
        time.sleep(0.05)

    objects = pd.DataFrame(object_rows)
    summaries = pd.DataFrame(summary_rows)
    objects.to_csv(OBJECTS_OUT, index=False)
    summaries.to_csv(SUMMARY_OUT, index=False)
    counts = summaries["path_disturbance_class"].value_counts(dropna=False).to_dict()
    payload = {
        "schema": "sparc_simbad_lightcone_foregrounds_v01",
        "status": "SIMBAD_FOREGROUND_CONE_CENSUS_ACQUIRED_PRELIMINARY_PATH_PROXY",
        "source_service": "SIMBAD astronomical database",
        "source_url": "https://simbad.cds.unistra.fr/",
        "cone_radius_arcmin": CONE_ARCMIN,
        "n_targets": len(names),
        "n_query_ok": int(summaries["query_status"].eq("OK").sum()),
        "n_object_rows": len(objects),
        "path_class_counts": counts,
        "limitations": [
            "SIMBAD is heterogeneous and not a complete magnitude-limited foreground catalogue",
            "foreground weight uses angular separation only and has no mass proxy",
            "objects without redshift cannot be classified as foreground or background",
            "P0 means no catalogued redshift-confirmed foreground in this cone, not an empty lightcone",
        ],
        "claim_boundary": "preliminary path-disturbance proxy for stratification only; not a physical lightcone transfer integral",
    }
    META_OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["status"])


if __name__ == "__main__":
    main()
