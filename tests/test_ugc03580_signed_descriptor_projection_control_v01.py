from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"


def test_signed_descriptor_projection_control_freeze_then_score() -> None:
    subprocess.run(
        [sys.executable, "scripts/freeze_ugc03580_signed_descriptor_projection_control_v01.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    freeze = json.loads(
        (DATA / "ugc03580_signed_descriptor_projection_control_freeze_v01.json").read_text()
    )
    assert freeze["endpoint_values_used"] is False
    assert freeze["terminal_formula"]["free_parameters"] == 0
    assert freeze["descriptor"]["scalar_K1_is_complete"] is False
    assert freeze["mixed_hessian_terminal_chain"]["maximum_finite_difference_error"] < 1e-8
    assert freeze["mixed_hessian_terminal_chain"]["nonzero_on_source_support"] is True

    subprocess.run(
        [sys.executable, "scripts/run_ugc03580_signed_descriptor_projection_control_v01.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    score = json.loads(
        (DATA / "ugc03580_signed_descriptor_projection_control_score_v01.json").read_text()
    )
    assert score["status"] == "DIAGNOSTIC_STANDARD_PROJECTION_CONTROL_SCORED_NOT_TAU_ENDPOINT"
    assert score["construction_used_vobs_or_residual"] is False
    assert score["scoring_used_vobs"] is True
    assert score["n_points"] > 0
    assert set(score["carrier_results"]) == {"NEWTONIAN", "TPG_V6", "MOND"}

    subprocess.run(
        [
            sys.executable,
            "scripts/audit_ugc03580_signed_descriptor_projection_control_robustness_v01.py",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    robust = json.loads(
        (DATA / "ugc03580_signed_descriptor_projection_control_robustness_v01.json").read_text()
    )
    assert robust["status"] == "POST_SCORE_ROBUSTNESS_AUDIT_COMPLETE_NOT_CLAIM_RAISING"
    assert all(robust["checks"].values())
    assert robust["grid"]["n_rows"] == 54
