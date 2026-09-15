import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
STEM = "phangs_postopen_resolved_morphology_diagnostic_v01"


def test_postopen_diagnostic_preserves_failed_endpoint_and_controls():
    audit = json.loads((DATA / f"{STEM}.json").read_text())
    summary = pd.read_csv(DATA / f"{STEM}_summary.csv")
    detail = pd.read_csv(DATA / f"{STEM}_by_galaxy.csv")
    assert audit["status"] == "NEGATIVE_RESULT_PRESERVED_POSTOPEN_DIAGNOSTIC"
    assert audit["endpoint_reopened"] is False
    assert audit["original_gate_failure_preserved"] is True
    assert len(summary) == 3
    assert len(detail) == 12
    assert (summary["p_primary_formal"] < 0.01).all()
    assert not summary["radial_control_pass"].any()
    assert not summary["phase_control_pass"].any()
