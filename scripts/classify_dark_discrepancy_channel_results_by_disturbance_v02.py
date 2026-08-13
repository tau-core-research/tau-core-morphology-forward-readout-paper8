#!/usr/bin/env python3
"""Classify dark-discrepancy channel results with the v02 S/P/O atlas."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"


def main() -> None:
    atlas = pd.read_csv(DATA / "sparc_lightcone_disturbance_atlas_v02.csv").set_index("galaxy")
    channel = json.loads((DATA / "dark_discrepancy_zone_multitracer_channel_audit_v01.json").read_text())
    classified = {}
    for galaxy, result in channel["galaxies"].items():
        row = atlas.loc[galaxy]
        classified[galaxy] = {
            "combined_class": row.combined_class,
            "source_class": row.source_disturbance_class,
            "path_class": row.path_disturbance_class,
            "observation_class": row.observation_disturbance_class,
            "foreground_candidate_count": int(row.foreground_candidate_count),
            "foreground_inverse_angle_weight": float(row.foreground_inverse_angle_weight),
            "post_d1p5_zero_p": result["post_d1p5"]["chi2_zero_p"],
            "local_channel_candidate": result["post_d1p5"]["chi2_zero_p"] <= 0.05,
        }
    payload = {
        "schema": "dark_discrepancy_channel_disturbance_classification_v02",
        "status": "LOCAL_CANDIDATE_ALIGNS_WITH_SOURCE_AND_PATH_DISTURBANCE_CONFOUNDED",
        "classified_results": classified,
        "pattern": "candidate=S3-P2-O0; null=S0-P0-O0",
        "source_vs_path_separable": False,
        "physical_channel_detected": False,
        "required_replication_cells": ["S0-P2-O0", "S3-P0-O0", "S0-P0-O0", "S3-P2-O0"],
        "interpretation": (
            "The only local candidate occurs where both source and preliminary foreground-path "
            "disturbance are elevated. The clean null differs on both axes, so morphology/source "
            "and path-channel effects are confounded rather than identified."
        ),
        "verdict": "FOREGROUND_ALIGNMENT_INTERESTING_BUT_SOURCE_PATH_CONFOUNDED",
    }
    (DATA / "dark_discrepancy_channel_disturbance_classification_v02.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["verdict"])


if __name__ == "__main__":
    main()
