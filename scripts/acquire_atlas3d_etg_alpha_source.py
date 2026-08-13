#!/usr/bin/env python3
"""Acquire the git-anchored Atlas3D ETG acceleration source from TPG."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TPG = Path("/Users/jolcsak/Projects/TPG")
GIT_PATH = "Dtl.Core/data/external/etg_lelli2017.txt"
OUT = ROOT / "data/external/catalogs/atlas3d_etg_lelli2017"
SUMMARY = ROOT / "data/derived/atlas3d_etg_alpha_source_v01.json"


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=TPG, text=True).strip()
    payload = subprocess.check_output(["git", "show", f"{commit}:{GIT_PATH}"], cwd=TPG)
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "etg_lelli2017.txt"
    target.write_bytes(payload)
    rows = [line for line in payload.decode("utf-8").splitlines() if line and not line.startswith("#")]
    result = {
        "schema": "atlas3d_etg_alpha_source_v01", "status": "SOURCE_ACQUISITION_ONLY",
        "source": "Lelli et al. 2017 Atlas3D ETG acceleration pairs",
        "upstream_tpg_commit": commit, "upstream_git_path": GIT_PATH,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "n_galaxies": len(rows), "n_acceleration_pairs": 2 * len(rows),
        "independent_of_sparc_175_membership": True, "endpoint_access": False,
    }
    SUMMARY.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["status"], len(rows))


if __name__ == "__main__":
    main()
