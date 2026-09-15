#!/usr/bin/env python3
"""Freeze the development-informed v02 endpoint before confirmatory opening."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from run_edge_califa_rotation_morphology_endpoint_v01 import self_test


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
ENDPOINT_SCRIPT = ROOT / "scripts/run_edge_califa_rotation_morphology_endpoint_v02.py"
PREREG = DATA / "edge_califa_rotation_morphology_preregistration_v04.json"
CONTRACT = DATA / "edge_califa_rotation_morphology_scoring_contract_v02.json"
PREFLIGHT = DATA / "edge_califa_rotation_morphology_source_preflight_v02.json"
DEVELOPMENT_V01 = DATA / "edge_califa_rotation_morphology_development_endpoint_v01.json"
OUTPUT = DATA / "edge_califa_rotation_morphology_endpoint_implementation_v02.json"
HASH = DATA / "edge_califa_rotation_morphology_endpoint_implementation_v02.sha256"
REPORT = ROOT / "reports/edge_califa_rotation_morphology_endpoint_implementation_v02.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    development = json.loads(DEVELOPMENT_V01.read_text(encoding="utf-8"))
    if contract["confirmatory_terminal_values_opened"]:
        raise RuntimeError("Implementation freeze must precede confirmatory opening")
    if development.get("scores_released", True):
        raise RuntimeError("The development-informed change was not score blind")
    audit = self_test()
    if not audit["all_pass"] or not contract["synthetic_covariance_audit"]["all_gates_pass"]:
        raise RuntimeError("v02 endpoint implementation audits failed")
    result = {
        "schema": "edge_califa_rotation_morphology_endpoint_implementation_v02",
        "status": "V02_IMPLEMENTATION_HASH_FROZEN_ALL_SYNTHETIC_TESTS_PASS_CONFIRMATORY_UNOPENED",
        "endpoint_script": str(ENDPOINT_SCRIPT.relative_to(ROOT)),
        "endpoint_script_sha256": sha256(ENDPOINT_SCRIPT),
        "preregistration_sha256": sha256(PREREG),
        "scoring_contract_sha256": sha256(CONTRACT),
        "source_preflight_sha256": sha256(PREFLIGHT),
        "score_blind_development_v01_sha256": sha256(DEVELOPMENT_V01),
        "conversion_and_exact_inference_self_test": audit,
        "occupied_sector_covariance_self_test": contract["synthetic_covariance_audit"],
        "confirmatory_terminal_values_opened": False,
        "post_confirmatory_open_code_change_policy": (
            "any implementation change invalidates this endpoint and no same-packet repair "
            "or replacement is permitted"
        ),
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    HASH.write_text(f"{digest}  data/derived/{OUTPUT.name}\n", encoding="utf-8")
    REPORT.write_text(
        "# EDGE--CALIFA endpoint implementation freeze v02\n\n"
        f"Status: `{result['status']}`\n\n"
        "The development-informed code hash, convention Jacobians, exact-sign engine and "
        "five/six-sector covariance algebra are frozen. Confirmatory velocity values remain unopened.\n",
        encoding="utf-8",
    )
    print(result["status"], result["endpoint_script_sha256"])


if __name__ == "__main__":
    main()
