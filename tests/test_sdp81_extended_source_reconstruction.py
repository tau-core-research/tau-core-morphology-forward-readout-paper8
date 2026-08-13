import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_extended_source_reconstruction_v01.json"


def test_sdp81_extended_source_reconstruction() -> None:
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["model"]["source_basis_count"] == 49
    assert result["model"]["beam_convolution"] is True
    assert result["model"]["nonnegative_source"] is True
    assert result["path_count"] == 4
    assert len(result["jacobian_determinants"]) == 4
    assert result["common_source_relative_residual"] >= 0.0
    assert result["independent_source_relative_residual"] >= 0.0
    assert result["body_covector_materialized"] is False
    assert result["time_covector_identified"] is False
    assert result["time_score_authorized"] is False
