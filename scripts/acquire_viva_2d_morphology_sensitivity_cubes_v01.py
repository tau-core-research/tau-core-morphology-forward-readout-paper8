#!/usr/bin/env python3
"""Acquire the exact VIVA cubes named by the frozen sensitivity protocol."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
EXTERNAL = ROOT / "data/external/literature/viva_2d_morphology_sensitivity_v01"
FREEZE = DATA / "viva_2d_morphology_sensitivity_preregistration_v01.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    if freeze["status"] != "SOURCE_FROZEN_CONVENTIONAL_SENSITIVITY_CONTROL_READY_FOR_ACQUISITION":
        raise RuntimeError("Unexpected preregistration state")
    cohort_csv = ROOT / freeze["cohort_csv"]
    if sha256(cohort_csv) != freeze["cohort_csv_sha256"]:
        raise RuntimeError("Frozen cohort CSV hash mismatch")
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in freeze["cohort"]:
        url = f"{freeze['primary_source']['data_root']}/{item['cube']}"
        target = EXTERNAL / item["cube"]
        reused = target.exists() and target.stat().st_size > 0
        if not reused:
            partial = target.with_suffix(target.suffix + ".part")
            with urllib.request.urlopen(url, timeout=120) as response, partial.open("wb") as handle:
                while block := response.read(1024 * 1024):
                    handle.write(block)
            os.replace(partial, target)
        rows.append({
            "galaxy": item["galaxy"], "role": item["role"], "url": url,
            "local_path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size,
            "sha256": sha256(target), "status": "reused" if reused else "downloaded",
            "velocity_opened_by_acquisition": False,
        })
    ledger = DATA / "viva_2d_morphology_sensitivity_acquisition_v01.csv"
    with ledger.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "schema": "viva_2d_morphology_sensitivity_acquisition_v01",
        "status": "FROZEN_VIVA_CUBES_ACQUIRED_UNOPENED",
        "preregistration": str(FREEZE.relative_to(ROOT)),
        "preregistration_sha256": sha256(FREEZE),
        "ledger": str(ledger.relative_to(ROOT)),
        "ledger_sha256": sha256(ledger),
        "cube_count": len(rows),
        "total_bytes": sum(row["bytes"] for row in rows),
        "all_nonempty": all(row["bytes"] > 0 for row in rows),
        "velocity_pixels_read": False,
        "claim_boundary": "source acquisition under a prior frozen conventional-control protocol; no velocity-field score and no Tau endpoint",
    }
    (DATA / "viva_2d_morphology_sensitivity_acquisition_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(result["status"], result["cube_count"], result["total_bytes"])


if __name__ == "__main__":
    main()
