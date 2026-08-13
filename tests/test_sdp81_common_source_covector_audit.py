import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_common_source_covector_audit_v01.json"


def test_sdp81_common_source_covector_audit() -> None:
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["path_count"] == 4
    assert len(result["runs"]) == 6
    assert result["all_designs_full_rank"] is True
    assert result["relative_residual_range"][0] < 0.5
    assert result["relative_residual_range"][1] > 0.5
    assert result["common_covector_promoted"] is False
    assert result["time_covector_identified"] is False
    assert result["time_score_authorized"] is False
