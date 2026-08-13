import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_two_component_spatial_operator_v01.json"


def test_sdp81_two_component_spatial_operator() -> None:
    result = json.loads(SUMMARY.read_text())
    assert result["channels_one_based"] == list(range(48, 59))
    assert result["component_centers_one_based"] == [52, 55]
    assert result["source_basis_count_per_component"] == 49
    assert result["predictive_positive_path_count"] == 2
    assert result["two_component_spatial_source_promoted"] is False
    assert result["theta_M_identified"] is False
    assert result["a_O_identified"] is False
    assert result["time_score_authorized"] is False
