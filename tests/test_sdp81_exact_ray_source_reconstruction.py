import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_exact_ray_source_reconstruction_v02.json"


def test_sdp81_exact_ray_source_reconstruction() -> None:
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["path_count"] == 4
    assert result["source_basis_count"] == 49
    assert result["mapping"].startswith("exact lenstronomy ray_shooting")
    assert result["common_source_relative_residual"] >= 0.0
    assert result["independent_source_relative_residual"] >= 0.0
    assert result["body_covector_materialized"] is False
    assert result["time_covector_identified"] is False
    assert result["time_score_authorized"] is False
