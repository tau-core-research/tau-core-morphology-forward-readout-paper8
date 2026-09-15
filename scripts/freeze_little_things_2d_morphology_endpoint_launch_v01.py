#!/usr/bin/env python3
"""Freeze the LITTLE THINGS target list and scoring implementation before target access."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
SOURCE_FREEZE = DATA / "little_things_2d_morphology_population_preregistration_v01.json"
PREFLIGHT = DATA / "little_things_2d_morphology_source_preflight_v01.json"
OPERATOR = DATA / "little_things_2d_morphology_operator_calibration_v01.json"
SCORER = ROOT / "scripts/run_little_things_2d_morphology_population_endpoint_v01.py"
ACQUIRER = ROOT / "scripts/acquire_little_things_2d_morphology_velocity_products_v01.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = json.loads(SOURCE_FREEZE.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    operator = json.loads(OPERATOR.read_text(encoding="utf-8"))
    if operator["status"] != "SOURCE_OPERATOR_CALIBRATED_20_GALAXY_VELOCITY_ACQUISITION_ALLOWED":
        raise RuntimeError("Operator population gate has not passed")
    rows = {row["galaxy"]: row for row in source["rows"]}
    targets = []
    for galaxy in operator["operator_passing_galaxies"]:
        row = rows[galaxy]
        source_path = next(
            item["source_map"] for item in __import__("csv").DictReader(
                (ROOT / preflight["support_ledger"]).open(encoding="utf-8")
            ) if item["galaxy"] == galaxy
        )
        with __import__("astropy.io.fits", fromlist=["fits"]).open(ROOT / source_path, memmap=True) as hdul:
            shape = list(__import__("numpy").squeeze(hdul[0].data).shape)
        targets.append({
            "galaxy": galaxy,
            "velocity_url": row["moment0_url"].replace("_R_X0_P_R.FITS", "_R_XMOM1.FITS"),
            "velocity_filename": f"{row['product_stem']}_R_XMOM1.FITS",
            "expected_image_shape": shape,
            "published_hi_asymmetry": row["published_hi_asymmetry"],
            "published_hi_asymmetry_error": row["published_hi_asymmetry_error"],
        })
    output = {
        "schema": "little_things_2d_morphology_endpoint_launch_freeze_v01",
        "status": "TARGET_LIST_AND_SCORER_FROZEN_VELOCITY_ACQUISITION_ALLOWED",
        "source_preflight": str(PREFLIGHT.relative_to(ROOT)),
        "source_preflight_sha256": sha256(PREFLIGHT),
        "operator_calibration": str(OPERATOR.relative_to(ROOT)),
        "operator_calibration_sha256": sha256(OPERATOR),
        "scoring_script": str(SCORER.relative_to(ROOT)),
        "scoring_script_sha256": sha256(SCORER),
        "acquisition_script": str(ACQUIRER.relative_to(ROOT)),
        "acquisition_script_sha256": sha256(ACQUIRER),
        "eligible_galaxies": operator["operator_passing_galaxies"],
        "targets": {row["galaxy"]: row for row in targets},
        "success_gate": {
            "minimum_endpoint_galaxies": 19,
            "minimum_positive_fraction": 0.60,
            "maximum_one_sided_sign_flip_p": 0.05,
            "mean_and_median_specificity_must_be_positive": True,
        },
        "velocity_pixels_opened_before_launch_freeze": False,
        "tau_endpoint_allowed": False,
        "claim_boundary": "frozen conventional same-tracer morphology-sensitivity endpoint; a pass cannot identify Tau or parent loss",
    }
    out = DATA / "little_things_2d_morphology_endpoint_launch_freeze_v01.json"
    out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(output["status"], len(targets), output["scoring_script_sha256"])


if __name__ == "__main__":
    main()
