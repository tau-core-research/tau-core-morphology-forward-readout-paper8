import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_parent_gas_conditional_response_is_endpoint_blind() -> None:
    subprocess.run(
        [sys.executable, "scripts/audit_sdp81_parent_gas_conditional_response_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(
        (ROOT / "data/derived/sdp81_parent_gas_conditional_response_v01.json").read_text()
    )
    assert result["status"] == "CONDITIONAL_PARENT_GAS_RESPONSE_DERIVED_PHYSICAL_MIXED_JET_OPEN"
    assert result["proof_checks_passed"] == result["proof_checks_total"] == 11
    assert result["derived_bridge_rank"] == result["mixed_derivative_rank"] == 5
    assert result["backreaction_frobenius_norm"] > 0.0
    assert result["physical_mixed_derivative_selected"] is False
