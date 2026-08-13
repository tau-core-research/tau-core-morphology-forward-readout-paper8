import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_continuum_path_registration_v01.json"


def test_sdp81_continuum_path_registration() -> None:
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["source_tracer"] == "ALMA Band-7 continuum"
    assert result["shift_grid_mas"] == [-40.0, -20.0, 0.0, 20.0, 40.0]
    assert len(result["path_calibrations"]) == 4
    assert all(
        row["heldout_gain_fitted"] is False
        for row in result["path_calibrations"]
    )
