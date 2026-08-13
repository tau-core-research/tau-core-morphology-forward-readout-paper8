#!/usr/bin/env python3
"""Freeze the small-sample S4G disk-break/dynamic-onset alignment pilot."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORTS = ROOT / "reports"
SOURCE_PATH = DATA / "s4g_disk_break_onset_source_v01.csv"
PROVENANCE_PATH = DATA / "s4g_disk_break_onset_source_v01.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
    if provenance["endpoint_access"]:
        raise RuntimeError("Disk-break source provenance permits endpoint access")
    source = pd.read_csv(SOURCE_PATH)
    frozen = source.loc[
        source["match_status"].eq("UNIQUE_NAME_MATCH")
        & source["break_radius_kpc"].notna(),
        [
            "galaxy",
            "profile_type",
            "break_radius_kpc",
            "break_radius_error_kpc",
            "inner_scale_kpc",
            "outer_scale_kpc",
            "sparc_rdisk_kpc",
        ],
    ].sort_values("galaxy")
    frozen["endpoint_blind"] = True
    frozen["retrospective_lock"] = True
    frozen_path = DATA / "s4g_disk_break_dynamic_onset_freeze_v01.csv"
    frozen.to_csv(frozen_path, index=False)

    manifest = {
        "schema": "s4g_disk_break_dynamic_onset_freeze_v01",
        "status": "SOURCE_ONLY_DISK_BREAK_ALIGNMENT_PILOT_FREEZE_READY_SMALL_N",
        "source_only": True,
        "endpoint_access": False,
        "retrospective_lock": True,
        "n_source_rows": int(len(frozen)),
        "minimum_population_n": 15,
        "population_claim_allowed": False,
        "primary_dynamic_onset": {
            "mass_discrepancy_threshold": 2.0,
            "persistence_points": 3,
            "outer_median_must_remain_above_threshold": True,
        },
        "sensitivity_thresholds": [1.5, 3.0],
        "primary_alignment_metric": "median_absolute_log_rdyn_over_rbreak",
        "null": "exact_or_10000_draw_permutation_of_break_radii_across_paired_galaxies",
        "promotion_rule": (
            "descriptive pilot only because frozen source N<15; no pass status is available"
        ),
        "claim_boundary": (
            "retrospective small-N onset-alignment diagnostic; cannot distinguish source "
            "activation from time, quantum, path, gravity, or mixed channel origin"
        ),
        "input_sha256": {
            "source": sha256(SOURCE_PATH),
            "provenance": sha256(PROVENANCE_PATH),
        },
        "frozen_source_sha256": sha256(frozen_path),
    }
    manifest_path = DATA / "s4g_disk_break_dynamic_onset_freeze_v01.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / "s4g_disk_break_dynamic_onset_freeze_v01.md"
    report_path.write_text(
        f"""# S4G Disk-Break/Dynamic-Onset Freeze v0.1

**Status:** `SOURCE_ONLY_DISK_BREAK_ALIGNMENT_PILOT_FREEZE_READY_SMALL_N`

The source-only freeze contains {len(frozen)} published disk-break radii. The
dynamic endpoint rule is fixed to the first persistent `D>=2` onset, with
`D>=1.5` and `D>=3` retained as sensitivity coordinates. The primary metric
and permutation null are fixed before the dynamic-onset atlas is opened.

Because source `N={len(frozen)}<15`, this route is descriptive regardless of
its eventual score.
""",
        encoding="utf-8",
    )
    print(manifest["status"])
    print(frozen_path)
    print(manifest_path)
    print(report_path)


if __name__ == "__main__":
    main()
