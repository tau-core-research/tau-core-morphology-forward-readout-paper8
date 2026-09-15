import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_post_open_orthogonalization_is_algebraically_valid_but_not_a_repair():
    subprocess.run(
        [sys.executable, "scripts/audit_ngc4062_velocity_zero_point_orthogonalization_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(
        (ROOT / "data/derived/ngc4062_velocity_zero_point_orthogonalization_v01.json").read_text()
    )
    assert result["status"] == "POST_OPEN_ORTHOGONALIZATION_DERIVED_FUTURE_FREEZE_REQUIRED"
    assert result["endpoint_rescored"] is False
    assert result["confirmatory_status_changed"] is False
    assert result["operator_checks_pass"] is True
    assert result["exact_common_mode_counterexample"]["projected_common_information"] < 1.0e-12
    for row in result["resolutions"].values():
        assert row["nuisance_rank"] == 1
        assert row["projector_rank"] == 1
        assert row["annihilation_max_abs"] < 1.0e-12
        assert row["zero_point_shift_invariance_max_abs_km_s"] < 1.0e-10
        assert row["post_open_projected_zero_p"] > 0.05
