import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_velocity_field_operator_v02.json"


def test_sdp81_velocity_field_operator_v02() -> None:
    result = json.loads(SUMMARY.read_text())
    assert result["schema"].endswith(".v02")
    assert result["channels_one_based"] == list(range(48, 59))
    assert result["fit_blocks"] == 44
    assert result["theta_M_identified"] is False
    assert result["a_O_identified"] is False
    assert result["time_score_authorized"] is False
