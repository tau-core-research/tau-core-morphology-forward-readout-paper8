#!/usr/bin/env python3
"""Acquire the launch-frozen LITTLE THINGS moment-1 targets without opening pixels."""

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
LAUNCH = DATA / "little_things_2d_morphology_endpoint_launch_freeze_v01.json"
EXTERNAL = ROOT / "data/external/literature/little_things_2d_morphology_population_v01/moment1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def acquire(item: dict) -> dict:
    url = item["velocity_url"]
    if not url.endswith("_R_XMOM1.FITS") or any(token in url.upper() for token in ("X0_P_R", "MOM2", "ICL001")):
        raise RuntimeError(f"Unexpected target product: {url}")
    target = EXTERNAL / item["velocity_filename"]
    reused = target.exists() and target.stat().st_size > 0
    if not reused:
        partial = target.with_suffix(target.suffix + ".part")
        request = urllib.request.Request(url, headers={"User-Agent": "tau-core-paper8-frozen-target-acquisition/1.0"})
        with urllib.request.urlopen(request, timeout=180) as response, partial.open("wb") as handle:
            while block := response.read(1024 * 1024):
                handle.write(block)
        os.replace(partial, target)
    return {
        "galaxy": item["galaxy"], "url": url, "local_path": str(target.relative_to(ROOT)),
        "bytes": target.stat().st_size, "sha256": sha256(target),
        "status": "reused" if reused else "downloaded", "velocity_pixels_opened_by_acquisition": False,
    }


def main() -> None:
    launch = json.loads(LAUNCH.read_text(encoding="utf-8"))
    if launch["status"] != "TARGET_LIST_AND_SCORER_FROZEN_VELOCITY_ACQUISITION_ALLOWED":
        raise RuntimeError("Endpoint launch is not frozen")
    scorer = ROOT / launch["scoring_script"]
    if sha256(scorer) != launch["scoring_script_sha256"]:
        raise RuntimeError("Scoring script changed after launch freeze")
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(acquire, item) for item in launch["targets"].values()]
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda row: row["galaxy"])
    ledger = DATA / "little_things_2d_morphology_velocity_acquisition_v01.csv"
    with ledger.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    output = {
        "schema": "little_things_2d_morphology_velocity_acquisition_v01",
        "status": "FROZEN_VELOCITY_PRODUCTS_ACQUIRED_UNOPENED",
        "launch_freeze": str(LAUNCH.relative_to(ROOT)),
        "launch_freeze_sha256": sha256(LAUNCH),
        "ledger": str(ledger.relative_to(ROOT)),
        "ledger_sha256": sha256(ledger),
        "target_count": len(rows),
        "total_bytes": sum(row["bytes"] for row in rows),
        "velocity_pixels_opened_by_acquisition": False,
        "claim_boundary": "target acquisition after source/operator/scorer freeze; no score in this step",
    }
    (DATA / "little_things_2d_morphology_velocity_acquisition_v01.json").write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(output["status"], len(rows), output["total_bytes"])


if __name__ == "__main__":
    main()
