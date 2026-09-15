from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_sdp81_open_transition_profile_lift_gate_v01.py"
OUT = ROOT / "data/derived/sdp81_open_transition_profile_lift_gate_v01.json"


def test_open_transition_profile_lift_fails_closed() -> None:
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    result = json.loads(OUT.read_text(encoding="utf-8"))
    assert result["status"] == (
        "INHERITED_CO87_PROFILE_LIFT_REJECTED_NEW_SOURCE_SPECTROSCOPY_REQUIRED"
    )
    assert result["profile_lift_authorized"] is False
    assert result["endpoint_authorized"] is False
    assert result["checks"]["official_open_source_maps_have_no_spectral_axis"] is True
    assert result["checks"]["image_plane_inverse_source_cube_not_promoted"] is True
    assert result["checks"]["three_path_to_fourth_path_transfer_not_established"] is True
    assert result["open_transition_diagnostics"]["loo_positive_fold_count"] == 1
    assert result["open_transition_diagnostics"]["loo_fold_count"] == 24
