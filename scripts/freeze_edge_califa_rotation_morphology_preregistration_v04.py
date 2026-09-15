#!/usr/bin/env python3
"""Freeze the development-informed, confirmatory-unopened EDGE v04 amendment."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
V03 = DATA / "edge_califa_rotation_morphology_preregistration_v03.json"
PREFLIGHT = DATA / "edge_califa_rotation_morphology_source_preflight_v02.json"
DEVELOPMENT_V01 = DATA / "edge_califa_rotation_morphology_development_endpoint_v01.json"
OUTPUT = DATA / "edge_califa_rotation_morphology_preregistration_v04.json"
HASH = DATA / "edge_califa_rotation_morphology_preregistration_v04.sha256"
REPORT = ROOT / "reports/edge_califa_rotation_morphology_preregistration_v04.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    v03 = json.loads(V03.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    development = json.loads(DEVELOPMENT_V01.read_text(encoding="utf-8"))
    expected_status = "DEVELOPMENT_ENDPOINT_OPENED_FROZEN_GATE_FAILURE_NO_SCORE_RELEASED"
    if development["status"] != expected_status or development["scores_released"]:
        raise RuntimeError("v04 requires the score-blind v01 development gate failure")
    if set(development["failures"]) != set(preflight["development_no_claim"]):
        raise RuntimeError("Unexpected development membership")
    if any("does not occupy all six terminal macrosectors" not in text for text in development["failures"].values()):
        raise RuntimeError("v04 may address only the observed terminal-sector coverage failure")

    protocol = copy.deepcopy(v03)
    protocol["schema"] = "edge_califa_rotation_morphology_preregistration_v04"
    protocol["status"] = "DEVELOPMENT_INFORMED_V04_PROTOCOL_FROZEN_CONFIRMATORY_ENDPOINT_UNOPENED"
    protocol["supersedes"] = {
        "v03_protocol_sha256": sha256(V03),
        "v01_development_endpoint_sha256": sha256(DEVELOPMENT_V01),
        "development_result": development["status"],
        "development_scores_released": False,
        "confirmatory_velocity_values_opened": False,
        "source_cohort_or_matrices_changed": False,
    }
    protocol["development_informed_change"] = {
        "observed_failure_only": (
            "the outer development zone retained five rather than six occupied terminal "
            "macrosectors after the frozen velocity-error gate"
        ),
        "change": (
            "require at least five of the six fixed macrosectors in every terminal zone and "
            "jackknife only the occupied sectors"
        ),
        "unchanged": [
            "all galaxy memberships",
            "all source supports, radial edges and source matrices",
            "velocity frame/convention conversion",
            "minimum 20 terminal rows per zone",
            "full-rank positive-definite 4x4 covariance in every zone",
            "all projections, controls, exact inference and thresholds",
        ],
        "why_not_a_score_tune": (
            "the v01 development route released no terminal coefficient, Q score, sign or "
            "effect magnitude; the amendment uses only a support-failure label"
        ),
    }
    protocol["terminal_opening"]["zone_gate"] = (
        "at least 20 rows and at least five of the six fixed macrosectors in every frozen zone"
    )
    protocol["terminal_opening"]["covariance"] = (
        "delete-one-occupied-macrosector jackknife in each zone with J in {5,6}, using "
        "(J-1)/J scaling; every retained 4x4 block and the assembled 20x20 covariance "
        "must remain full rank and positive definite without regularization"
    )
    protocol["decision_rule"]["hard_fail"] = [
        "fewer than 6 source-eligible confirmatory galaxies",
        "fewer than 20 terminal rows or fewer than 5 occupied macrosectors in any zone",
        "any rank, covariance, support, provenance, or hash gate failure",
        "any post-confirmatory-open change to fields, zones, masks, split, controls, conversions, or thresholds",
    ]
    protocol["interpretation"]["v04_limit"] = (
        "the terminal sector threshold was selected after one score-blind development support "
        "failure; all confirmatory velocity values remained unopened, but the route is explicitly "
        "development-informed prevalidation"
    )

    payload = json.dumps(protocol, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    HASH.write_text(f"{digest}  data/derived/{OUTPUT.name}\n", encoding="utf-8")
    REPORT.write_text(
        "# EDGE--CALIFA rotation-morphology preregistration v04\n\n"
        f"Status: `{protocol['status']}`\n\n"
        "The v01 development opening released no score and failed only because one zone "
        "retained five of six fixed terminal macrosectors. v04 permits five or six occupied "
        "sectors but still requires an unregularized full-rank positive-definite 4x4 "
        "jackknife covariance in every zone. The seven confirmatory galaxies remain unopened.\n",
        encoding="utf-8",
    )
    print(protocol["status"], digest)


if __name__ == "__main__":
    main()
