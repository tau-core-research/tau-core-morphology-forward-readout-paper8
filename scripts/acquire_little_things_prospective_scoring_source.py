#!/usr/bin/env python3
"""Acquire and freeze LITTLE THINGS as a prospective Paper 8 scoring source."""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import urllib.request
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/external/catalogs/little_things_oh2015"
DATA = ROOT / "data/derived"
BASE = "https://cdsarc.cds.unistra.fr/ftp/J/AJ/149/180"
FILES = ["ReadMe", "table1.dat.gz", "table2.dat.gz", "rotdmbar.dat.gz"]


def fetch(name: str) -> bytes:
    return urllib.request.urlopen(f"{BASE}/{name}", timeout=120).read()


def text(name: str) -> str:
    raw = (OUT / name).read_bytes()
    return gzip.decompress(raw).decode("ascii") if name.endswith(".gz") else raw.decode("ascii")


def normalize(name: str) -> str:
    compact = "".join(character for character in name.upper() if character.isalnum())
    match = re.fullmatch(r"(DDO|NGC|UGC|IC)0*(\d+)", compact)
    return f"{match.group(1)}{int(match.group(2))}" if match else compact


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for name in FILES:
        payload = fetch(name)
        (OUT / name).write_bytes(payload)
        hashes[name] = hashlib.sha256(payload).hexdigest()

    properties = []
    for line in text("table1.dat.gz").splitlines():
        if not line.strip():
            continue
        properties.append({
            "galaxy": line[0:8].strip(), "distance_mpc": float(line[32:36]),
            "inclination_deg": float(line[59:63]), "inclination_error_deg": float(line[64:68]),
            "absolute_v_magnitude": float(line[69:74]),
        })
    mass = []
    for line in text("table2.dat.gz").splitlines():
        if not line.strip():
            continue
        def number(a: int, b: int):
            value = line[a:b].strip()
            return float(value) if value else None
        mass.append({
            "galaxy": line[0:8].strip(), "rmax_kpc": number(9, 13), "r03_kpc": number(14, 18),
            "v_rmax_km_s": number(19, 24), "gas_mass_1e7_msun": number(139, 145),
            "rmax_over_hi_beam": number(31, 36),
            "stellar_mass_kin_1e7_msun": number(146, 151),
            "stellar_mass_sed_1e7_msun": number(152, 157),
        })
    catalog = pd.DataFrame(properties).merge(pd.DataFrame(mass), on="galaxy", validate="one_to_one")
    historically_scored = pd.read_csv(DATA / "amplitude_shrinkage_path_scores_by_galaxy.csv").galaxy.unique()
    historical = {normalize(name) for name in historically_scored}
    catalog["normalized_name"] = catalog.galaxy.map(normalize)
    catalog["exact_name_overlap_with_historical_175"] = catalog.normalized_name.isin(historical)
    catalog["prospective_name_freeze"] = ~catalog.exact_name_overlap_with_historical_175
    catalog["observed_rotation_curve_available"] = True
    catalog["global_baryonic_masses_available"] = True
    catalog["hi_beam_fwhm_kpc"] = catalog.rmax_kpc / catalog.rmax_over_hi_beam
    catalog["radial_gas_velocity_component_available"] = False
    catalog["radial_stellar_velocity_component_available"] = False
    catalog["comparable_tpg_mond_scoring_allowed"] = False
    catalog["endpoint_access"] = False
    catalog.to_csv(DATA / "little_things_prospective_scoring_freeze_v01.csv", index=False)

    rotation_rows = []
    for line in text("rotdmbar.dat.gz").splitlines():
        if not line.strip():
            continue
        rotation_rows.append({
            "galaxy": line[0:8].strip(), "curve_type": line[9:14].strip(),
            "r03_kpc": float(line[15:23]), "v03_km_s": float(line[24:34]),
            "radius_kpc": float(line[35:44]) * float(line[15:23]),
            "velocity_km_s": float(line[45:54]) * float(line[24:34]),
            "velocity_error_km_s": float(line[55:63]) * float(line[24:34]),
            "endpoint_access": False,
        })
    pd.DataFrame(rotation_rows).to_csv(DATA / "little_things_rotation_curves_v01.csv", index=False)
    result = {
        "schema": "little_things_prospective_scoring_source_v01",
        "status": "PROSPECTIVE_SAMPLE_FROZEN_SCORING_BLOCKED_BARYONIC_RADIAL_COMPONENTS",
        "source": "Oh et al. 2015 LITTLE THINGS, VizieR J/AJ/149/180",
        "source_url": BASE, "file_sha256": hashes,
        "n_catalog_galaxies": len(catalog),
        "n_exact_name_new_vs_historical_175": int(catalog.prospective_name_freeze.sum()),
        "n_exact_name_overlap": int(catalog.exact_name_overlap_with_historical_175.sum()),
        "n_rotation_rows": len(rotation_rows),
        "source_native_numeric_rotation_curves": True,
        "source_native_global_baryonic_masses": True,
        "source_native_radial_baryonic_velocity_components": False,
        "prospective_scoring_allowed": False,
        "next_required_acquisition": "radial v_gas(R) and v_star(R), or author-supplied mass-model tables",
        "endpoint_access": False,
        "claim_boundary": "sample freeze and source acquisition only; no endpoint score",
    }
    (DATA / "little_things_prospective_scoring_source_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"], result["n_exact_name_new_vs_historical_175"])


if __name__ == "__main__":
    main()
