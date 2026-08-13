#!/usr/bin/env python3
"""Attach source/path/observation disturbance classes to channel-zone results."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"


def main() -> None:
    atlas = pd.read_csv(DATA / "sparc_lightcone_disturbance_atlas_v01.csv").set_index("galaxy")
    channel = json.loads(
        (DATA / "dark_discrepancy_zone_multitracer_channel_audit_v01.json").read_text()
    )
    classified = {}
    for galaxy, result in channel["galaxies"].items():
        row = atlas.loc[galaxy]
        classified[galaxy] = {
            "combined_class": row["combined_class"],
            "source_class": row["source_disturbance_class"],
            "source_basis": row["source_disturbance_basis"],
            "path_class": row["path_disturbance_class"],
            "observation_class": row["observation_disturbance_class"],
            "post_d1p5_zero_p": result["post_d1p5"]["chi2_zero_p"],
            "local_channel_candidate": result["post_d1p5"]["chi2_zero_p"] <= 0.05,
        }
    payload = {
        "schema": "dark_discrepancy_channel_disturbance_classification_v01",
        "status": "LOCAL_CANDIDATE_OCCURS_IN_SOURCE_DISTURBED_PATH_UNKNOWN_CLASS",
        "classified_results": classified,
        "candidate_clean_source_replication": False,
        "candidate_clean_path_replication": False,
        "interpretation": (
            "The NGC3726 local candidate is S3-PX-O0: observational geometry is clean, "
            "but strong source-side asymmetry and unknown foreground path prevent a physical "
            "observer-channel attribution. The S0-PX-O0 NGC4559 comparison is null."
        ),
        "verdict": "DISTURBANCE_CLASSIFICATION_WEAKENS_CHANNEL_INTERPRETATION",
    }
    (DATA / "dark_discrepancy_channel_disturbance_classification_v01.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(payload["verdict"])


if __name__ == "__main__":
    main()
