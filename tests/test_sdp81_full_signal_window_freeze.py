import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/sdp81_full_signal_window_freeze_v01.json"


def test_sdp81_full_signal_window_freeze() -> None:
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["selected_channels_one_based"] == list(range(48, 59))
    assert result["selected_channel_count"] == 11
    assert result["contiguous"] is True
    assert result["previous_window_omitted_selected_channels"] == [53, 54, 55, 56, 57, 58]
    assert result["uses_time_delay_or_rotation_residual"] is False
    assert result["velocity_field_rescore_authorized"] is True
