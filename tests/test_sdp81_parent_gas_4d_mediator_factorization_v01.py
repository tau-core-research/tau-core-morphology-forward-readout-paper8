import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_parent_gas_4d_mediator_factorization_is_endpoint_blind() -> None:
    subprocess.run(
        [sys.executable, "scripts/audit_sdp81_parent_gas_4d_mediator_factorization_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(
        (ROOT / "data/derived/sdp81_parent_gas_4d_mediator_factorization_v01.json").read_text()
    )
    assert result["status"] == (
        "FOUR_D_MEDIATOR_FACTORIZATION_DERIVED_DIRECT_REMAINDER_AND_PHYSICAL_DESCENT_OPEN"
    )
    assert result["checks_passed"] == result["checks_total"] == 13
    assert result["mediator_jacobian_rank"] == result["derived_bridge_rank"] == 5
    assert result["physical_D_Z_e_owned"] is False
    assert result["no_direct_coupling_certificate_owned"] is False
    assert result["endpoint_authorized"] is False
