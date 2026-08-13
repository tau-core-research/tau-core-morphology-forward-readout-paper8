import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_continuum_path_registration_v02.json"


def test_sdp81_continuum_path_registration_v02() -> None:
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["schema"].endswith(".v02")
    assert result["shift_grid_mas"] == [
        -80.0,
        -60.0,
        -40.0,
        -20.0,
        0.0,
        20.0,
        40.0,
        60.0,
        80.0,
    ]
    assert len(result["path_calibrations"]) == 4
