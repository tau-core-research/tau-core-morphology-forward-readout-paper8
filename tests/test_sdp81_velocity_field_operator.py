import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_velocity_field_operator_v01.json"


def test_sdp81_velocity_field_operator() -> None:
    result = json.loads(SUMMARY.read_text())
    assert result["fit_blocks"] == 24
    assert result["source_amplitude_count"] == 49
    assert result["relative_residual"] >= 0
    assert result["spectrally_flat_null_relative_residual"] >= 0
    assert result["theta_M_identified"] is False
    assert result["a_O_identified"] is False
    assert result["time_score_authorized"] is False
