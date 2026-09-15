import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_sdp81_g4d_coframe_parent_gas_mediator_compiler_is_endpoint_blind() -> None:
    subprocess.run(
        [sys.executable, "scripts/audit_sdp81_g4d_coframe_parent_gas_mediator_compiler_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(
        (ROOT / "data/derived/sdp81_g4d_coframe_parent_gas_mediator_compiler_v01.json").read_text()
    )
    assert result["status"] == (
        "OPACITY_SHAPE_SURVIVAL_DERIVED_SOURCE_PROFILE_OPEN"
    )
    assert result["checks_passed"] == result["checks_total"] == 56
    assert result["coframe_metric_rank"] == 10
    assert result["coframe_metric_gauge_nullity"] == 6
    assert result["D_Z_metric_rank"] == 5
    assert result["parent_gas_bridge_rank"] == 5
    assert result["B_AZ_rank"] == result["I_ZA_rank"] == 5
    assert result["schur_backreaction_norm"] > 0.0
    assert result["current_AORS_D_A_rank"] == 4
    assert result["current_AORS_D_Z_metric_rank"] == 4
    assert result["minimal_independent_scalar_enrichment_rank"] == 5
    assert result["natural_common_volume_enrichment_rank"] == 5
    assert result["common_volume_response_increment_rank"] == 1
    assert result["common_volume_metric_increment_rank"] == 1
    assert result["common_volume_gas_increment_rank"] == 1
    assert result["standard_cold_matter_volume_coupling_nonzero"] is True
    assert result["conditional_opacity_shape_terminal_survival_derived"] is True
    assert result["physical_channel_opacity_profile_owned"] is False
    assert result["endpoint_authorized"] is False
