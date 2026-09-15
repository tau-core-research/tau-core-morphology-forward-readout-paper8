#!/usr/bin/env python3
"""Freeze the exact VIVA 2D scoring implementation before pixel opening."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
PREREG = DATA / "viva_2d_morphology_sensitivity_preregistration_v01.json"
ACQUISITION = DATA / "viva_2d_morphology_sensitivity_acquisition_v01.json"
SCORER = ROOT / "scripts/run_viva_2d_morphology_sensitivity_endpoint_v01.py"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    acquisition = json.loads(ACQUISITION.read_text(encoding="utf-8"))
    if acquisition["preregistration_sha256"] != sha256(PREREG):
        raise RuntimeError("Preregistration changed after cube acquisition")
    result = {
        "schema": "viva_2d_morphology_sensitivity_operator_freeze_v01",
        "status": "SOURCE_AND_IMPLEMENTATION_FROZEN_SCORE_ALLOWED",
        "preregistration_sha256": sha256(PREREG),
        "acquisition_sha256": sha256(ACQUISITION),
        "scoring_script": str(SCORER.relative_to(ROOT)),
        "scoring_script_sha256": sha256(SCORER),
        "exact_operator": {
            "radial_edges_r25": [0.20, 0.40, 0.60, 0.80, 1.00],
            "morphology_mode": 1,
            "velocity_upper_sideband": 2,
            "nuisance_per_annulus": ["constant", "cos_theta", "sin_theta"],
            "phase_wrong_offsets_rad": [0.0, 1.5707963267948966, 3.141592653589793, 4.71238898038469],
            "cross_galaxy_control": "lexicographic cyclic donor within the same frozen role",
            "held_out_sectors": 12,
            "fit_weight": "equal beam-independent pixels",
            "primary_score": "fractional held-out SSE reduction",
            "specificity": "matched minus arithmetic mean of three wrong-template fractional reductions",
            "permutation": "all 20 choices of three disturbed labels among six; one-sided including observed",
        },
        "geometry_policy": "use published fixed VIVA center/PA/inclination; no geometry refit; lack of source covariance is an explicit limitation rather than a fitted repair",
        "velocity_pixels_opened_before_this_freeze": False,
        "tau_endpoint_allowed": False,
        "claim_boundary": "implementation freeze for a conventional sensitivity control; no Tau, gravity, or parent-loss score",
    }
    out = DATA / "viva_2d_morphology_sensitivity_operator_freeze_v01.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["status"], result["scoring_script_sha256"])


if __name__ == "__main__":
    main()
