import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_reference_image_route_is_small_development_only_and_sealed() -> None:
    subprocess.run(
        [sys.executable, "scripts/audit_sdp81_reference_image_source_route_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(
        (ROOT / "data/derived/sdp81_reference_image_source_route_v01.json").read_text()
    )
    assert result["status"] == "LOCAL_REFERENCE_IMAGE_ROUTE_AVAILABLE_DEVELOPMENT_ONLY"
    assert result["total_bytes"] == 395928000
    assert result["checks_passed"] == result["checks_total"] == 8
    assert result["source_reconstruction_completed"] is False
    assert result["transition_readiness_increment"] == 0
    assert result["endpoint_authorized"] is False
    assert result["checks"]["co109_header_not_read"] is True
    assert result["checks"]["co109_pixels_not_read"] is True
