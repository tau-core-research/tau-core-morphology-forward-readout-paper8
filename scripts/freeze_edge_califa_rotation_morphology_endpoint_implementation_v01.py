#!/usr/bin/env python3
"""Freeze the tested endpoint implementation before real velocity values are opened."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from run_edge_califa_rotation_morphology_endpoint_v01 import self_test


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
ENDPOINT_SCRIPT = ROOT / "scripts/run_edge_califa_rotation_morphology_endpoint_v01.py"
PREREG = DATA / "edge_califa_rotation_morphology_preregistration_v03.json"
CONTRACT = DATA / "edge_califa_rotation_morphology_scoring_contract_v01.json"
PREFLIGHT = DATA / "edge_califa_rotation_morphology_source_preflight_v02.json"
OUTPUT = DATA / "edge_califa_rotation_morphology_endpoint_implementation_v01.json"
HASH = DATA / "edge_califa_rotation_morphology_endpoint_implementation_v01.sha256"
REPORT = ROOT / "reports/edge_califa_rotation_morphology_endpoint_implementation_v01.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if prereg["endpoint_opened"] or preflight["velocity_terminal_values_opened"]:
        raise RuntimeError("Endpoint implementation must be frozen before terminal opening")
    if contract["terminal_values_opened"]:
        raise RuntimeError("Scoring contract crossed the terminal-opening boundary")
    audit = self_test()
    if not audit["all_pass"]:
        raise RuntimeError("Endpoint implementation self-test failed")
    result = {
        "schema": "edge_califa_rotation_morphology_endpoint_implementation_v01",
        "status": "ENDPOINT_IMPLEMENTATION_HASH_FROZEN_SYNTHETIC_TESTS_PASS_VALUES_UNOPENED",
        "endpoint_script": str(ENDPOINT_SCRIPT.relative_to(ROOT)),
        "endpoint_script_sha256": sha256(ENDPOINT_SCRIPT),
        "preregistration_sha256": sha256(PREREG),
        "scoring_contract_sha256": sha256(CONTRACT),
        "source_preflight_sha256": sha256(PREFLIGHT),
        "self_test": audit,
        "terminal_values_opened": False,
        "post_open_code_change_policy": (
            "any change invalidates this implementation hash and forbids reuse of the current "
            "confirmatory packet; development diagnostics may motivate only a separately "
            "versioned future endpoint"
        ),
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    HASH.write_text(f"{digest}  data/derived/{OUTPUT.name}\n", encoding="utf-8")
    REPORT.write_text(
        "# EDGE--CALIFA endpoint implementation freeze v01\n\n"
        f"Status: `{result['status']}`\n\n"
        "The endpoint script hash is frozen. Analytic velocity-conversion Jacobians agree "
        "with finite differences and the seven-galaxy exact-sign engine enumerates 128 "
        "vectors. No real CO or Halpha terminal velocity value was opened.\n",
        encoding="utf-8",
    )
    print(result["status"], result["endpoint_script_sha256"])


if __name__ == "__main__":
    main()
