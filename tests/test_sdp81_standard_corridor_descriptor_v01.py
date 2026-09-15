from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_sdp81_standard_corridor_descriptor_v01.py"
RESULT = ROOT / "data/derived/sdp81_standard_corridor_descriptor_v01.json"


def test_sdp81_standard_corridor_descriptor() -> None:
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["status"] == "STANDARD_CORRIDOR_COMPARATOR_DERIVED_TAU_PARENT_DEPTH_OPEN"
    assert result["checks_passed"] == result["checks_total"] == 7
    assert result["inputs"]["spectral_or_velocity_endpoint_read"] is False
    assert result["endpoint_authorized"] is False
    assert len(result["paths"]) == 4
    assert {path["parity"] for path in result["paths"]} == {"positive", "negative"}
    assert result["summary"]["centered_descriptor_rank"] >= 2
    assert result["summary"]["paths_above_unit_operator_norm"] == 1
    assert result["direct_parent_contraction_identification_allowed"] is False


def test_sdp81_standard_corridor_descriptor_is_deterministic() -> None:
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    first = RESULT.read_bytes()
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    assert RESULT.read_bytes() == first
