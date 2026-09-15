import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ngc0925_outer_only_route_is_geometrically_possible_but_not_clean():
    subprocess.run(
        [sys.executable, "scripts/audit_ngc0925_outer_only_source_support_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads((ROOT / "data/derived/ngc0925_outer_only_source_support_v01.json").read_text())
    assert result["status"] == "OUTER_GEOMETRIC_CAPACITY_PASS_TERMINAL_CLEANLINESS_FAIL_ENDPOINT_BLOCKED"
    assert result["retained_ring_count"] == 6
    assert result["minimum_full_half_annulus_capacity_beam_areas"] > 10.0
    assert result["next_source_target"] == "NGC4062"
    assert result["endpoint_pixels_read"] is False
    assert result["endpoint_allowed"] is False
