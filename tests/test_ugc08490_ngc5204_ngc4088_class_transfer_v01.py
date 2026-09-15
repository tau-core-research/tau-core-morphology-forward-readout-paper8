from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"


def test_ugc08490_class_transfer_is_reproducible_negative_result() -> None:
    audit = json.loads(
        (DATA / "ugc08490_ngc5204_ngc4088_class_transfer_reproducibility_audit_v01.json")
        .read_text(encoding="utf-8")
    )
    summary = json.loads(
        (DATA / "ugc08490_ngc5204_ngc4088_class_transfer_endpoint_v01.json")
        .read_text(encoding="utf-8")
    )
    scores = pd.read_csv(
        DATA / "ugc08490_ngc5204_ngc4088_class_transfer_endpoint_v01_scores.csv"
    ).set_index("model_id")

    assert audit["status"] == "REPRODUCIBILITY_AUDIT_PASS"
    assert all(audit["checks"].values())
    assert summary["status"] == "RETROSPECTIVE_CLASS_TRANSFER_NEGATIVE"
    assert not summary["prospective_blind_endpoint"]
    assert not summary["post_endpoint_repair_performed"]
    assert (
        scores.loc["TAU_WARP_TRANSFER_PRIMARY", "rmse_km_s"]
        < scores.loc["CONTROL_WRONG_NGC4088_ONSET", "rmse_km_s"]
    )
    assert (
        scores.loc["TAU_WARP_TRANSFER_PRIMARY", "rmse_km_s"]
        > scores.loc["MOND_FIXED_A0", "rmse_km_s"]
    )
