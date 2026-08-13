#!/usr/bin/env python3
"""Freeze a source-only S4G morphology test for outer mass discrepancy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
SOURCE = DATA / "s4g_optical_morphology_attribution_source_features_v02.csv"
PARENT_FREEZE = DATA / "s4g_optical_morphology_attribution_freeze_v02.json"
OUT = DATA / "s4g_dark_discrepancy_morphology_freeze_v01.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parent = json.loads(PARENT_FREEZE.read_text(encoding="utf-8"))
    if parent["status"] != "SOURCE_ONLY_RETROSPECTIVE_LOCK_V02_READY":
        raise RuntimeError("Parent source freeze is not ready")
    if sha256(SOURCE) != parent["output_sha256"]:
        raise RuntimeError("Source feature hash mismatch")
    payload = {
        "schema": "s4g_dark_discrepancy_morphology_freeze_v01",
        "status": "SOURCE_ONLY_DARK_DISCREPANCY_MORPHOLOGY_FREEZE_READY",
        "claim_level": "retrospective_locked_prevalidation",
        "source_only": True,
        "endpoint_access": False,
        "source_features_path": str(SOURCE.relative_to(ROOT)),
        "source_features_sha256": sha256(SOURCE),
        "split_column": "split",
        "baseline_features": parent["baseline_features"] + parent["baseline_missingness_features"],
        "morphology_features": parent["morphology_features"] + parent["morphology_missingness_features"],
        "imputation": parent["imputation"],
        "standardization": parent["standardization"],
        "model": "ridge_linear_fixed_lambda_1",
        "primary_target": {
            "name": "log_outer3_mass_discrepancy",
            "definition": "log D_outer3 = -2 log median_outer3(vbar/vobs)",
            "physical_role": "direct dark-matter-like outer rotation discrepancy burden",
        },
        "primary_metric": "holdout_mse_baseline_minus_baseline_plus_morphology",
        "nulls": {
            "row_shuffle": 2000,
            "independent_column_shuffle": 2000,
            "rng_seed": 20260711,
        },
        "promotion_rule": (
            "positive holdout MSE reduction; both shuffle p<=0.05; observed reduction "
            "above both null 95th percentiles"
        ),
        "forbidden_interpretation": [
            "morphological-body proof",
            "observer-time channel detection",
            "quantum channel detection",
            "dark matter exclusion",
        ],
        "claim_boundary": (
            "retrospective locked 4D inverse test; a pass establishes incremental "
            "source-morphology information about outer mass discrepancy only"
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(payload["status"])


if __name__ == "__main__":
    main()
