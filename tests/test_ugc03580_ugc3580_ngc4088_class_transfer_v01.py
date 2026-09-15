from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ugc03580_class_transfer_reproducibility() -> None:
    scripts = [
        "scripts/build_ugc03580_ugc3580_warp_body_v01.py",
        "scripts/freeze_ugc03580_ugc3580_ngc4088_class_transfer_v01.py",
        "scripts/run_ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01.py",
        "scripts/audit_ugc03580_ugc3580_ngc4088_class_transfer_reproducibility_v01.py",
    ]
    for script in scripts:
        subprocess.run([sys.executable, script], cwd=ROOT, check=True, capture_output=True)

    audit = json.loads(
        (ROOT / "data/derived/ugc03580_ugc3580_ngc4088_class_transfer_reproducibility_audit_v01.json").read_text(
            encoding="utf-8"
        )
    )
    summary = json.loads(
        (ROOT / "data/derived/ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01.json").read_text(
            encoding="utf-8"
        )
    )
    assert audit["status"] == "REPRODUCIBILITY_AUDIT_PASS"
    assert audit["checks_passed"] == audit["checks_total"]
    assert summary["status"] == "RETROSPECTIVE_CLASS_TRANSFER_REJECTS_UNCAPPED_UNIVERSAL_LAW"
    assert summary["primary_beats_wrong_onset_full"] is False
    assert summary["post_endpoint_repair_performed"] is False
