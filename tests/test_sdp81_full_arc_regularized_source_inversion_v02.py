import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_arc_open_line_inverse_preserves_negative_result() -> None:
    result = json.loads(
        (ROOT / "data/derived/sdp81_full_arc_regularized_source_inversion_v02.json").read_text()
    )
    assert result["status"] == "FULL_ARC_REFERENCE_IMAGE_INVERSION_NOT_PROMOTED"
    assert result["configuration"]["selected_lambda"] == 100.0
    assert result["held_path_positive_median_count"] == 4
    assert 0.015 < result["median_held_path_squared_residual_improvement"] < 0.03
    assert result["median_held_path_squared_residual_improvement"] < 0.05
    assert result["matched_minus_wrong_median_improvement"] < 0.01
    assert result["zero_source_limit_norm"] == 0.0
    assert result["development_source_profile_promoted"] is False
    assert result["transition_readiness_increment"] == 0
    assert result["co109_header_read"] is False
    assert result["co109_pixels_read"] is False
    assert result["endpoint_authorized"] is False
