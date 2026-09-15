import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_parent_gas_equivariant_intertwiner_is_endpoint_blind() -> None:
    subprocess.run(
        [sys.executable, "scripts/audit_sdp81_parent_gas_equivariant_intertwiner_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(
        (ROOT / "data/derived/sdp81_parent_gas_equivariant_intertwiner_v01.json").read_text()
    )
    assert result["status"] == "SYMMETRY_INTERTWINER_SHAPE_DERIVED_CURRENT_SYMMETRIES_NONSELECTING"
    assert result["checks_passed"] == result["checks_total"] == 14
    assert result["p6_reflection_intertwiner_dimension"] == 13
    assert result["hypothetical_s6_commutant_dimension"] == 1
    assert result["two_component_swap_fixed_radiative_rank"] < 5
    assert result["physical_common_representation_owned"] is False
