import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_spectral_leave_one_path_out_v01.json"


def test_sdp81_spectral_leave_one_path_out() -> None:
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["fold_count"] == 24
    assert all(fold["uses_heldout_gain"] is False for fold in result["folds"])
    assert 0 <= result["positive_fold_count"] <= 24
    assert set(result["path_median_predictive_r2"]) == {"1", "2", "3", "4"}
    assert result["body_clock_theta_M_materialized"] is False
    assert result["time_score_authorized"] is False
