import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_ngc3893_disturbed_control_freezes_without_velocity_access():
    subprocess.run([sys.executable, "scripts/freeze_ngc3893_disturbed_control_v01.py"], cwd=ROOT, check=True)
    result = json.loads((ROOT / "data/derived/ngc3893_disturbed_control_freeze_v01.json").read_text())
    assert result["velocity_columns_parsed_during_freeze"] is False
    assert result["endpoint_access"] is False
    assert result["common_radii_arcsec"] == [20.0, 40.0, 60.0, 80.0]
    assert result["source_template"] == [0.0, 0.0, 0.0, 1.0]
    assert result["expected_projector_rank"] == 3
