import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_standard_path_radiative_factorization_is_endpoint_blind() -> None:
    subprocess.run(
        [sys.executable, "scripts/derive_sdp81_standard_path_radiative_factorization_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(
        (ROOT / "data/derived/sdp81_standard_path_radiative_factorization_v01.json").read_text()
    )
    assert result["status"] == "STANDARD_PATH_FUNCTIONAL_DERIVED_RADIATIVE_MIXED_JET_OPEN"
    assert result["checks_passed"] == result["checks_total"] == 8
    assert result["rank"] == 4
    assert result["per_channel_spatial_nullity"] == 45
    assert result["separable_source_control"]["all_paths_reduce_to_identity"] is True
    assert result["spatial_spectral_countermodel"]["parent_loss_present"] is False
    assert result["checks"]["no_spectral_or_velocity_endpoint_read"] is True
    assert result["checks"]["no_co109_header_or_pixel_read"] is True
