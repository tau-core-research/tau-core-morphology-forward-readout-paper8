import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"


def _load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_viva_source_and_operator_were_frozen_before_velocity_opening() -> None:
    prereg = _load("viva_2d_morphology_sensitivity_preregistration_v01.json")
    acquisition = _load("viva_2d_morphology_sensitivity_acquisition_v01.json")
    operator = _load("viva_2d_morphology_sensitivity_operator_freeze_v01.json")

    assert prereg["status"] == (
        "SOURCE_FROZEN_CONVENTIONAL_SENSITIVITY_CONTROL_READY_FOR_ACQUISITION"
    )
    assert [row["role"] for row in prereg["cohort"]].count("disturbed") == 3
    assert [row["role"] for row in prereg["cohort"]].count("quiet") == 3
    assert prereg["construction_uses_velocity_or_rotation_residual"] is False
    assert acquisition["status"] == "FROZEN_VIVA_CUBES_ACQUIRED_UNOPENED"
    assert acquisition["cube_count"] == 6
    assert acquisition["velocity_pixels_read"] is False
    assert acquisition["preregistration_sha256"] == _sha256(
        DATA / "viva_2d_morphology_sensitivity_preregistration_v01.json"
    )
    assert operator["status"] == "SOURCE_AND_IMPLEMENTATION_FROZEN_SCORE_ALLOWED"
    assert operator["velocity_pixels_opened_before_this_freeze"] is False
    assert operator["tau_endpoint_allowed"] is False
    assert operator["scoring_script_sha256"] == _sha256(
        ROOT / operator["scoring_script"]
    )


def test_viva_endpoint_preserves_the_frozen_support_failure_without_score() -> None:
    result = _load("viva_2d_morphology_sensitivity_endpoint_v01.json")

    assert result["status"] == "PREFLIGHT_BLOCKED_BY_FROZEN_SUPPORT_GATE"
    assert result["all_frozen_support_gates_pass"] is False
    assert result["conventional_sensitivity_demonstrated"] is False
    assert result["score_rows"] == []
    assert result["primary_disturbed_minus_quiet_specificity"] is None
    assert result["exact_one_sided_permutation_p"] is None
    assert result["tau_endpoint_scored"] is False
    assert len(result["support_gates"]) == 6
    assert all(not row["support_gate"] for row in result["support_gates"])
    assert {row["independent_samples"] for row in result["support_gates"]} == {
        4,
        27,
        28,
        29,
        45,
        81,
    }
