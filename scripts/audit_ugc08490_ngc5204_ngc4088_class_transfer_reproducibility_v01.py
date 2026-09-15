#!/usr/bin/env python3
"""Independent core recomputation for the UGC08490 class-transfer result."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
MANIFEST = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_freeze_v01.json"
MANIFEST_SHA = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_freeze_v01.sha256"
ENDPOINT = ROOT / "data" / "external" / "sparc" / "UGC08490_rotmod.dat"
POINTS = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_endpoint_v01_points.csv"
SCORES = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_endpoint_v01_scores.csv"
SUMMARY = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_endpoint_v01.json"
AUDIT = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_reproducibility_audit_v01.json"
REPORT = REPORTS / "ugc08490_ngc5204_ngc4088_class_transfer_reproducibility_audit_v01.md"

KPC_M = 3.0857e19
A0 = 1.2e-10
NGC4088_XW = 0.2983326403051493
TOL = 1.0e-10


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_raw() -> np.ndarray:
    rows = []
    for raw in ENDPOINT.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            rows.append(list(map(float, line.split()[:8])))
    return np.asarray(rows, dtype=float)


def predict(vn: np.ndarray, r: np.ndarray, r_hi: float, x_w: float, vflat: float) -> np.ndarray:
    kernel = np.maximum(0.0, (r / r_hi - x_w) / (1.0 - x_w))
    return np.sqrt(vn**2 + x_w * vflat**2 * kernel)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected_hash = MANIFEST_SHA.read_text(encoding="utf-8").split()[0]
    raw = parse_raw()
    r, vobs, _err, vgas, vdisk, vbul = [raw[:, i] for i in range(6)]
    vn = np.sqrt(vgas * np.abs(vgas) + 0.5 * vdisk**2 + 0.7 * vbul**2)

    source = manifest["frozen_source_inputs"]
    frozen = manifest["derived_frozen_values"]
    distance = float(source["distance_mpc"])
    r_hi = float(source["r_hi_kpc"])
    vflat = float(source["vflat_km_s_primary"])
    onset_arcsec = float(source["warp_onset_arcsec"])
    recomputed_xw = onset_arcsec * distance * 1000.0 / 206265.0 / r_hi
    recomputed_lambda = recomputed_xw * vflat**2
    primary = predict(vn, r, r_hi, recomputed_xw, vflat)
    wrong_onset = predict(vn, r, r_hi, NGC4088_XW, vflat)

    a_n = (vn * 1000.0) ** 2 / (r * KPC_M)
    f_mond = np.sqrt((1.0 + np.sqrt(1.0 + 4.0 * A0 / a_n)) / 2.0)
    mond = vn * f_mond

    primary_rmse = float(np.sqrt(np.mean((primary - vobs) ** 2)))
    wrong_rmse = float(np.sqrt(np.mean((wrong_onset - vobs) ** 2)))
    mond_rmse = float(np.sqrt(np.mean((mond - vobs) ** 2)))

    stored_points = pd.read_csv(POINTS)
    stored_scores = pd.read_csv(SCORES).set_index("model_id")
    stored_summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    checks = {
        "manifest_hash_matches": sha256(MANIFEST) == expected_hash,
        "source_body_declares_no_endpoint_construction": not manifest["source_selection"][
            "selection_uses_pointwise_vobs_or_residual"
        ],
        "freeze_precedes_current_score": bool(
            manifest["formula_frozen_before_current_endpoint_scoring"]
        ),
        "retuning_forbidden": not manifest["formula"]["post_freeze_retuning_allowed"],
        "xw_reproduces": abs(recomputed_xw - float(frozen["x_w"])) < TOL,
        "lambda_reproduces": abs(
            recomputed_lambda - float(frozen["lambda_w_primary_km2_s2"])
        ) < TOL,
        "point_count_reproduces": len(raw) == len(stored_points) == int(stored_summary["n_points"]),
        "primary_curve_reproduces": bool(
            np.allclose(
                primary,
                stored_points["pred_TAU_WARP_TRANSFER_PRIMARY"].to_numpy(),
                atol=TOL,
                rtol=0.0,
            )
        ),
        "mond_curve_reproduces": bool(
            np.allclose(
                mond,
                stored_points["pred_MOND_FIXED_A0"].to_numpy(),
                atol=TOL,
                rtol=0.0,
            )
        ),
        "primary_rmse_reproduces": abs(
            primary_rmse - float(stored_scores.loc["TAU_WARP_TRANSFER_PRIMARY", "rmse_km_s"])
        ) < TOL,
        "wrong_onset_rmse_reproduces": abs(
            wrong_rmse - float(stored_scores.loc["CONTROL_WRONG_NGC4088_ONSET", "rmse_km_s"])
        ) < TOL,
        "mond_rmse_reproduces": abs(
            mond_rmse - float(stored_scores.loc["MOND_FIXED_A0", "rmse_km_s"])
        ) < TOL,
        "source_correct_onset_beats_wrong_onset": primary_rmse < wrong_rmse,
        "source_correct_onset_does_not_beat_mond": primary_rmse >= mond_rmse,
        "negative_status_preserved": stored_summary["status"] == "RETROSPECTIVE_CLASS_TRANSFER_NEGATIVE",
        "no_post_endpoint_repair": not stored_summary["post_endpoint_repair_performed"],
    }
    passed = bool(all(checks.values()))
    audit = {
        "schema": "tau_core_ugc08490_ngc5204_ngc4088_class_transfer_reproducibility_audit_v01",
        "status": "REPRODUCIBILITY_AUDIT_PASS" if passed else "REPRODUCIBILITY_AUDIT_FAIL",
        "checks": checks,
        "recomputed": {
            "x_w": recomputed_xw,
            "lambda_w_km2_s2": recomputed_lambda,
            "primary_rmse_km_s": primary_rmse,
            "wrong_onset_rmse_km_s": wrong_rmse,
            "mond_rmse_km_s": mond_rmse,
        },
        "claim_boundary": "reproducibility_of_retrospective_negative_transfer_not_physical_validation",
    }
    AUDIT.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# UGC08490 / NGC5204 class-transfer reproducibility audit v01",
                "",
                f"Status: `{audit['status']}`",
                "",
                "An independent implementation rebuilt the baryonic carrier, fixed-MOND",
                "comparator, warp kernel, and wrong-onset control directly from the raw",
                "endpoint and the pre-existing hashed freeze manifest.",
                "",
                f"- reproduced `x_w`: `{recomputed_xw:.12f}`;",
                f"- reproduced primary RMSE: `{primary_rmse:.12f} km/s`;",
                f"- reproduced wrong-onset RMSE: `{wrong_rmse:.12f} km/s`;",
                f"- reproduced fixed-MOND RMSE: `{mond_rmse:.12f} km/s`;",
                f"- checks passed: `{sum(checks.values())}/{len(checks)}`.",
                "",
                "This audit validates numerical reproducibility and claim-boundary",
                "preservation. It does not turn the retrospective endpoint into a",
                "prospective or physically validating result.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(audit, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
