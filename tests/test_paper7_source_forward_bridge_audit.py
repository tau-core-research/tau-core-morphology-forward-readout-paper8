import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/paper7_source_forward_bridge_audit_v01.json"


def test_paper7_source_forward_bridge_audit() -> None:
    subprocess.run(
        [sys.executable, "scripts/audit_paper7_source_forward_bridge_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["direct_object_overlap_count"] == 0
    assert result["sdp81"]["same_source_path_count"] == 4
    assert result["sdp81"]["transition_count"] == 2
    assert result["sdp81"]["relative_lens_geometry_reproduced"] is True
    assert result["sdp81"]["absolute_wcs_registration_complete"] is False
    assert result["sdp81"]["absolute_wcs_registration_operational"] is True
    assert result["sdp81"]["shared_parent_lens_mode_supported"] is True
    assert result["sdp81"]["independent_auxiliary_mode_detected"] is False
    assert result["sdp81"]["minimal_common_source_covector_promoted"] is False
    assert result["sdp81"]["minimal_covector_relative_residual_range"][0] < 0.5
    assert result["sdp81"]["minimal_covector_relative_residual_range"][1] > 0.5
    assert result["sdp81"]["exact_ray_common_extended_source_supported"] is True
    assert result["sdp81"]["exact_ray_common_source_relative_residual"] < 0.5
    assert result["sdp81"]["spectral_leave_one_path_out_promoted"] is False
    assert result["sdp81"]["spectral_leave_one_path_out_positive_folds"] == 1
    assert result["sdp81"]["continuum_registration_boundary_count"] == 3
    assert result["sdp81"]["continuum_registration_usable_for_band6"] is False
    assert result["sdp81"]["full_window_velocity_operator_promoted"] is False
    assert result["sdp81"]["full_window_velocity_gradient_norm"] == 0.0
    assert result["source_forward_h_tau_materialized"] is False
    assert result["rank_repair_authorized"] is False
    assert result["time_score_authorized"] is False
