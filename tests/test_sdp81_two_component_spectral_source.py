import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_two_component_spectral_source_v01.json"


def test_sdp81_two_component_spectral_source() -> None:
    result = json.loads(SUMMARY.read_text())
    assert result["channels_one_based"] == list(range(48, 59))
    assert result["two_component_centers_one_based"] == [52, 55]
    assert result["velocity_field_or_clock_identified"] is False
    assert result["time_score_authorized"] is False
