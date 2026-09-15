#!/usr/bin/env python3
"""Freeze the public EDGE LSRK-to-heliocentric corrections before endpoint opening."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
PREFLIGHT = DATA / "edge_califa_rotation_morphology_source_preflight_v02.json"
OUTPUT = DATA / "edge_califa_velocity_frame_calibration_v01.json"
TABLE = DATA / "edge_califa_velocity_frame_calibration_v01.csv"
HASH = DATA / "edge_califa_velocity_frame_calibration_v01.sha256"
REPORT = ROOT / "reports/edge_califa_velocity_frame_calibration_v01.md"

EXPECTED_CATALOG_SHA256 = "97582d96f69c5d8a26bf52d3b413ec620b4229fdc26fff09dd7686f1b28dfed3"
EXPECTED_EDGE_PYDB_COMMIT = "1af9ae612024baecf44c8f16244c841e4be4352b"
DEFAULT_CATALOG = Path("/tmp/edge_pydb_src/edge_pydb/dat_glob/derived/edge_rfpars.csv")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()

    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    if preflight["velocity_terminal_values_opened"]:
        raise RuntimeError("Frame calibration must precede terminal opening")
    if not preflight["endpoint_opening_authorized"]:
        raise RuntimeError("The source-only cohort did not pass its opening gate")
    observed_hash = sha256(args.catalog)
    if observed_hash != EXPECTED_CATALOG_SHA256:
        raise RuntimeError("Official edge_rfpars.csv hash mismatch")

    catalog = pd.read_csv(args.catalog, comment="#")
    required = {"Name", "rfLSRK2helio"}
    if not required.issubset(catalog.columns):
        raise RuntimeError("Frame-calibration catalog is missing required columns")
    if catalog["Name"].duplicated().any():
        raise RuntimeError("Frame-calibration catalog contains duplicate galaxy names")

    eligible = list(preflight["source_eligible"])
    selected = (
        catalog.loc[catalog["Name"].isin(eligible), ["Name", "rfLSRK2helio"]]
        .sort_values("Name")
        .reset_index(drop=True)
    )
    if selected["Name"].tolist() != sorted(eligible):
        raise RuntimeError("Not every frozen EDGE galaxy has a frame correction")
    if selected["rfLSRK2helio"].isna().any():
        raise RuntimeError("A frozen frame correction is non-finite")
    selected = selected.rename(
        columns={"Name": "galaxy", "rfLSRK2helio": "lsrk_to_heliocentric_subtract_km_s"}
    )
    selected.to_csv(TABLE, index=False, float_format="%.8f")

    table_hash = sha256(TABLE)
    result = {
        "schema": "edge_califa_velocity_frame_calibration_v01",
        "status": "PUBLIC_FRAME_CORRECTIONS_FROZEN_VELOCITY_FIELDS_UNOPENED",
        "source": {
            "repository": "https://github.com/tonywong94/edge_pydb",
            "commit": EXPECTED_EDGE_PYDB_COMMIT,
            "path": "edge_pydb/dat_glob/derived/edge_rfpars.csv",
            "sha256": EXPECTED_CATALOG_SHA256,
            "catalog_definition": "V(helio)=V(LSRK)-rfLSRK2helio",
        },
        "frozen_galaxies": selected["galaxy"].tolist(),
        "correction_table": str(TABLE.relative_to(ROOT)),
        "correction_table_sha256": table_hash,
        "velocity_terminal_values_opened": False,
        "calibration_boundary": (
            "only the public sky/frame correction was read; rfVsys, rotation velocities, "
            "CO moment-1 and Halpha velocity values were not used"
        ),
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    HASH.write_text(
        f"{hashlib.sha256(payload.encode('utf-8')).hexdigest()}  data/derived/{OUTPUT.name}\n",
        encoding="utf-8",
    )
    REPORT.write_text(
        "# EDGE--CALIFA velocity-frame calibration v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The official EDGE catalog correction `V(helio)=V(LSRK)-rfLSRK2helio` "
        "is frozen for the eight source-eligible galaxies. No CO or Halpha velocity "
        "field value was requested or opened. The endpoint must next convert the "
        "heliocentric radio and optical velocities separately to the relativistic "
        "convention before forming their contrast.\n",
        encoding="utf-8",
    )
    print(result["status"], table_hash)


if __name__ == "__main__":
    main()
