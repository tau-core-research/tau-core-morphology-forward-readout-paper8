import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_image_g_wcs_registration_v01.json"


def test_sdp81_image_g_wcs_registration() -> None:
    subprocess.run(
        [sys.executable, "scripts/register_sdp81_image_g_wcs_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["q1_path_count"] == 4
    assert result["absolute_wcs_registration_operational"] is True
    assert result["local_compact_peak"]["counterpart_consistent_within_tolerance"] is True
    assert result["body_covector_pullback_materialized"] is False
    for path in result["q1_paths"]:
        assert 0.0 <= path["pixel_x_zero_based"] < 3000.0
        assert 0.0 <= path["pixel_y_zero_based"] < 3000.0
