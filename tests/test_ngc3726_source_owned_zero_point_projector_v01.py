import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ngc3726_source_owned_zero_point_projector_preserves_null_status():
    subprocess.run(
        [sys.executable, "scripts/audit_ngc3726_source_owned_zero_point_projector_v01.py"],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(
        (ROOT / "data/derived/ngc3726_source_owned_zero_point_projector_v01.json").read_text()
    )
    assert result["operator_checks_pass"] is True
    assert result["confirmatory_endpoint"] is False
    assert result["endpoint_rescored"] is False
    assert result["n_common_radii"] == 6
    assert result["nuisance_rank"] == 1
    assert result["projector_rank"] == 5
    assert result["shape_zero_dof"] == 5
    assert result["shape_zero_p"] > 0.05
    assert result["operator_checks"]["constant_radial_mode_annihilated"] is True
