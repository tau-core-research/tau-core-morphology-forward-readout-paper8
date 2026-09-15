from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"


def test_ngc2541_signed_descriptor_source_geometry_freeze() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/freeze_ngc2541_signed_descriptor_source_geometry_v01.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "NGC2541_SIGNED_DESCRIPTOR_SOURCE_GEOMETRY_FREEZE_PASS" in completed.stdout
    result = json.loads(
        (DATA / "ngc2541_signed_descriptor_source_geometry_freeze_v01.json").read_text()
    )
    assert result["status"] == "SOURCE_GEOMETRY_READY_TERMINAL_CALIBRATION_AND_UNTOUCHED_ENDPOINT_BLOCKED"
    assert result["descriptor"]["n_support_rings"] == 25
    assert result["descriptor"]["maximum_decoder_error"] < 1.0e-10
    assert result["reference_projection_sensitivity"]["maximum_finite_difference_error"] < 1.0e-8
    assert result["physical_terminal_branch"]["status"] == "BLOCKED_PENDING_ENDPOINT_CALIBRATION"
    assert result["endpoint_values_used"] is False
    assert result["endpoint_scoring_allowed"] is False
    assert result["free_parameters"] == 0
