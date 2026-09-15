#!/usr/bin/env python3
"""Acquire only source-side LITTLE THINGS robust H I moment-0 maps."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
FREEZE = DATA / "little_things_2d_morphology_population_preregistration_v01.json"
EXTERNAL = ROOT / "data/external/literature/little_things_2d_morphology_population_v01/moment0"
ALLOWED = {"PROVISIONAL_SOURCE_CANDIDATE", "SOURCE_MOM0_SUPPORT_PENDING"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def acquire(item: dict) -> dict:
    url = item["moment0_url"]
    filename = f"{item['product_stem']}_R_X0_P_R.FITS"
    if not url.endswith(filename) or any(token in url.upper() for token in ("MOM1", "MOM2", "ICL001")):
        raise RuntimeError(f"Non-source product rejected for {item['galaxy']}: {url}")
    target = EXTERNAL / filename
    reused = target.exists() and target.stat().st_size > 0
    if not reused:
        partial = target.with_suffix(target.suffix + ".part")
        request = urllib.request.Request(url, headers={"User-Agent": "tau-core-paper8-source-acquisition/1.0"})
        with urllib.request.urlopen(request, timeout=180) as response, partial.open("wb") as handle:
            while block := response.read(1024 * 1024):
                handle.write(block)
        os.replace(partial, target)
    return {
        "galaxy": item["galaxy"],
        "source_status_at_freeze": item["source_status"],
        "url": url,
        "local_path": str(target.relative_to(ROOT)),
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
        "acquisition_status": "reused" if reused else "downloaded",
        "velocity_pixels_read": False,
    }


def main() -> None:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    if freeze["status"] != "SOURCE_POPULATION_FROZEN_MOM0_ONLY_ACQUISITION_ALLOWED":
        raise RuntimeError("Unexpected source freeze state")
    cohort = ROOT / freeze["cohort_csv"]
    if sha256(cohort) != freeze["cohort_csv_sha256"]:
        raise RuntimeError("Frozen source cohort hash mismatch")
    selected = [row for row in freeze["rows"] if row["source_status"] in ALLOWED]
    if len(selected) != 25:
        raise RuntimeError(f"Frozen source-only acquisition count changed: {len(selected)}")

    EXTERNAL.mkdir(parents=True, exist_ok=True)
    rows = []
    failures = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(acquire, item): item for item in selected}
        for future in as_completed(futures):
            item = futures[future]
            try:
                rows.append(future.result())
            except Exception as exc:  # preserve every source failure in the ledger
                failures.append({
                    "galaxy": item["galaxy"],
                    "url": item["moment0_url"],
                    "error": f"{type(exc).__name__}: {exc}",
                })
    rows.sort(key=lambda row: row["galaxy"])
    failures.sort(key=lambda row: row["galaxy"])

    ledger = DATA / "little_things_2d_morphology_source_acquisition_v01.csv"
    fields = [
        "galaxy", "source_status_at_freeze", "url", "local_path", "bytes",
        "sha256", "acquisition_status", "velocity_pixels_read",
    ]
    with ledger.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "schema": "little_things_2d_morphology_source_acquisition_v01",
        "status": "SOURCE_MOM0_ACQUISITION_COMPLETE" if not failures else "SOURCE_MOM0_ACQUISITION_INCOMPLETE",
        "preregistration": str(FREEZE.relative_to(ROOT)),
        "preregistration_sha256": sha256(FREEZE),
        "ledger": str(ledger.relative_to(ROOT)),
        "ledger_sha256": sha256(ledger),
        "requested_count": len(selected),
        "acquired_count": len(rows),
        "failure_count": len(failures),
        "failures": failures,
        "total_bytes": sum(row["bytes"] for row in rows),
        "product_family": "robust-weighted primary-beam-corrected H I moment 0 only",
        "same_cube_target_caveat": "future moment-1 targets are reductions of the same H I cube and may share masks/noise with moment 0; wrong-template and injection controls do not erase this dependence",
        "velocity_products_downloaded": False,
        "velocity_pixels_read": False,
        "endpoint_scoring_allowed": False,
        "claim_boundary": "source-map acquisition only; no kinematic result and no Tau endpoint",
    }
    out = DATA / "little_things_2d_morphology_source_acquisition_v01.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["status"], result["acquired_count"], result["failure_count"], result["total_bytes"])
    if failures:
        for failure in failures:
            print(failure)


if __name__ == "__main__":
    main()
