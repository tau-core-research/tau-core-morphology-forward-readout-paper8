import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
PREFIX = "inverse_parent_loss_conditional_kernel_test_v01"


def test_conditional_kernel_outputs_and_boundaries():
    audit = json.loads((DATA / f"{PREFIX}.json").read_text())
    summary = pd.read_csv(DATA / f"{PREFIX}_summary.csv")
    pairs = pd.read_csv(DATA / f"{PREFIX}_pair_tests.csv")
    shuffles = pd.read_csv(DATA / f"{PREFIX}_family_shuffles.csv")
    assert audit["status"] == "DIAGNOSTIC_ONLY_NOT_ENDPOINT"
    assert audit["endpoint_authorized"] is False
    assert audit["checks"]["endpoint_predictor_overlap"] == []
    assert audit["checks"]["roundtrip_tolerance_pass"] is True
    assert len(summary) == 9
    assert len(pairs) == 6
    assert len(shuffles) == 3 * audit["checks"]["family_shuffle_count"]
    assert set(summary["baseline_id"]) == {
        "newtonian_baryonic", "tpg_v6", "mond_fixed"
    }
    assert summary.select_dtypes("number").notna().all().all()
