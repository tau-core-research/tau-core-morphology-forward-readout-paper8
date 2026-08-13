import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_source_spectral_cube_v01.json"


def test_sdp81_source_spectral_cube() -> None:
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["tracer"] == "ALMA Band-6 CO(8-7)"
    assert result["channels_one_based"] == [47, 48, 49, 50, 51, 52]
    assert result["path_count"] == 4
    assert result["source_basis_count"] == 49
    assert len(result["channel_fits"]) == 6
    assert result["all_common_channel_residuals_finite"] is True
    assert result["active_source_cell_count"] >= 3
    assert result["source_clock_proxy"]["nonzero_fit"] is True
    assert result["source_clock_proxy"]["stable"] is False
    assert result["common_source_spectral_cube_promoted"] is False
    assert result["source_clock_proxy"]["parent_body_clock_identified"] is False
    assert result["body_clock_theta_M_materialized"] is False
    assert result["quotient_basic_time_covector_a_O_materialized"] is False
    assert result["time_score_authorized"] is False
