import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_ngc3893_frozen_disturbed_control_score_is_preserved():
    subprocess.run([sys.executable, "scripts/run_ngc3893_disturbed_control_v01.py"], cwd=ROOT, check=True)
    result = json.loads((ROOT / "data/derived/ngc3893_disturbed_control_score_v01.json").read_text())
    assert result["freeze_unchanged"] is True
    assert result["projector_rank"] == 3
    assert result["status"] == "NEGATIVE_RESULT_PRESERVED"
    assert result["control_detected_at_5pct"] is False
    assert result["matched_outer_disturbance"]["two_sided_p"] > 0.05
