from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_sdp81_observed_4d_incidence_measure_v01.py"
RESULT = ROOT / "data/derived/sdp81_observed_4d_incidence_measure_v01.json"


def test_observed_4d_incidence_measure_is_positive_and_endpoint_blind() -> None:
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["status"] == "OBSERVED_4D_INCIDENCE_MEASURE_PASS"
    assert result["checks_passed"] == result["checks_total"] == 10
    assert result["counting_measure"]["total_mass"] == 4.0
    assert all(atom["detected"] for atom in result["atoms"])
    assert result["inputs"]["spectral_or_velocity_endpoint_read"] is False
    assert result["parent_selector_or_lift_occupation_materialized"] is False


def test_observed_4d_incidence_measure_is_deterministic_and_hashed() -> None:
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    first = RESULT.read_bytes()
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    assert RESULT.read_bytes() == first
    result = json.loads(first)
    continuum = ROOT / result["inputs"]["continuum"]
    registration = ROOT / result["inputs"]["registration"]
    assert hashlib.sha256(continuum.read_bytes()).hexdigest() == result["inputs"]["continuum_sha256"]
    assert hashlib.sha256(registration.read_bytes()).hexdigest() == result["inputs"]["registration_sha256"]
