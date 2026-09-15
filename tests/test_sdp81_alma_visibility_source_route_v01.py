import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/freeze_sdp81_alma_visibility_source_route_v01.py"
OUT = ROOT / "data/derived/sdp81_alma_visibility_source_route_v01.json"


def test_visibility_source_route_is_frozen_and_endpoint_blind() -> None:
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    result = json.loads(OUT.read_text())
    assert result["status"] == "RAW_VISIBILITY_SOURCE_ROUTE_IDENTIFIED_ACQUISITION_NOT_EXECUTED"
    assert result["checks_passed"] == result["checks_total"] == 9
    assert result["allowed_execution_count"] == 21
    assert result["allowed_content_length_bytes"] == 211709114368
    assert result["transition_readiness_increment"] == 0
    assert result["acquisition_executed"] is False
    assert result["source_cube_reconstructed"] is False
    assert result["endpoint_authorized"] is False
    assert result["checks"]["no_allowed_uid_is_band7"] is True
    assert result["checks"]["co109_header_not_read"] is True
    assert result["checks"]["co109_pixels_not_read"] is True
