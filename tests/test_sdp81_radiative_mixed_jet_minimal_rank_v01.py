import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_radiative_mixed_jet_minimal_rank_is_endpoint_blind() -> None:
    subprocess.run(
        [sys.executable, "scripts/audit_sdp81_radiative_mixed_jet_minimal_rank_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(
        (ROOT / "data/derived/sdp81_radiative_mixed_jet_minimal_rank_v01.json").read_text()
    )
    assert result["status"] == "RADIATIVE_BASIS_EXISTS_TWO_LINE_OPACITY_PROFILE_UNIDENTIFIED"
    assert result["checks_passed"] == result["checks_total"] == 13
    assert result["uniform_slab_centered_log_rank"] <= 3
    assert result["optically_thin_uniform_slab_rank"] <= 2
    assert result["two_component_centered_log_rank"] == 5
    assert result["coincident_component_control_rank"] < 5
    assert result["two_line_opacity_profile_identified"] is False
    assert result["physical_parent_to_gas_bridge_selected"] is False
