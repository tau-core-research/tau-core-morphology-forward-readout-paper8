#!/usr/bin/env python3
"""Independent reproducibility audit for the UGC03580 class transfer."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
BODY = DATA / "ugc03580_ugc3580_warp_body_v01.json"
MANIFEST = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_freeze_v01.json"
MANIFEST_SHA = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_freeze_v01.sha256"
ENDPOINT = ROOT / "data" / "external" / "sparc" / "UGC03580_rotmod.dat"
SUMMARY = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01.json"
SCORES = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01_scores.csv"
ZONE_SCORES = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01_zone_scores.csv"
OUT = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_reproducibility_audit_v01.json"
REPORT = REPORTS / "ugc03580_ugc3580_ngc4088_class_transfer_reproducibility_audit_v01.md"

EXPECTED_ENDPOINT_SHA256 = "60e65aa00bff8714755a111e5065194bb1a3fe1aa4573a319ca058ab6d3a8425"
EXPECTED_SOURCE_SHA256 = "15b4ae9e2bb3268509e75b40e62def8cc4664a117fdcccafae8afb7f170ec8ba"
UGC08490_XW = 0.4508762999054615


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def close(a: float, b: float, tol: float = 1.0e-9) -> bool:
    return bool(math.isclose(a, b, rel_tol=tol, abs_tol=tol))


def score_map(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["model_id"]: row for row in csv.DictReader(handle)}


def main() -> None:
    body = json.loads(BODY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    scores = score_map(SCORES)

    raw = np.loadtxt(ENDPOINT)
    r = raw[:, 0]
    obs = raw[:, 1]
    vgas, vdisk, vbul = raw[:, 3], raw[:, 4], raw[:, 5]
    vn = np.sqrt(np.maximum(vgas * np.abs(vgas) + 0.5 * vdisk**2 + 0.7 * vbul**2, 0.0))

    source = manifest["frozen_source_inputs"]
    frozen = manifest["derived_frozen_values"]
    r_hi = float(source["r_hi_kpc"])
    vflat = float(source["vflat_km_s_primary"])
    onset_arcsec = float(source["warp_onset_arcsec"])
    distance_mpc = float(source["distance_mpc"])
    x_w = onset_arcsec * distance_mpc * 1000.0 / 206265.0 / r_hi
    lambda_w = x_w * vflat**2
    x = r / r_hi
    kernel = np.maximum(0.0, (x - x_w) / (1.0 - x_w))
    primary = np.sqrt(vn**2 + lambda_w * kernel)

    wrong_kernel = np.maximum(0.0, (x - UGC08490_XW) / (1.0 - UGC08490_XW))
    wrong = np.sqrt(vn**2 + UGC08490_XW * vflat**2 * wrong_kernel)
    within = x <= 1.0

    primary_rmse = float(np.sqrt(np.mean((primary - obs) ** 2)))
    newton_rmse = float(np.sqrt(np.mean((vn - obs) ** 2)))
    wrong_rmse = float(np.sqrt(np.mean((wrong - obs) ** 2)))
    within_primary_rmse = float(np.sqrt(np.mean((primary[within] - obs[within]) ** 2)))
    within_newton_rmse = float(np.sqrt(np.mean((vn[within] - obs[within]) ** 2)))

    checks = {
        "source_pdf_hash_matches": body["source_pdf_sha256"] == EXPECTED_SOURCE_SHA256,
        "endpoint_hash_matches": sha256(ENDPOINT) == EXPECTED_ENDPOINT_SHA256,
        "freeze_hash_matches": sha256(MANIFEST) == MANIFEST_SHA.read_text(encoding="utf-8").split()[0],
        "body_uses_no_endpoint": body["endpoint_values_used_for_body_construction"] is False,
        "freeze_script_certifies_no_pointwise_endpoint": manifest["independence_audit"]["pointwise_endpoint_curve_read_by_freeze_script"] is False,
        "historical_exposure_disclosed": manifest["independence_audit"]["historical_human_exposure_to_target_endpoint"] is True,
        "point_count_is_47": len(raw) == 47,
        "x_w_recomputed": close(x_w, float(frozen["x_w_primary_sparc_rhi"])),
        "lambda_recomputed": close(lambda_w, float(frozen["lambda_w_primary_km2_s2"])),
        "primary_rmse_recomputed": close(primary_rmse, float(summary["primary_rmse_full_km_s"])),
        "within_rhi_rmse_recomputed": close(within_primary_rmse, float(summary["primary_rmse_within_rhi_km_s"])),
        "wrong_onset_rmse_recomputed": close(wrong_rmse, float(summary["wrong_ugc08490_onset_rmse_full_km_s"])),
        "score_csv_primary_matches": close(primary_rmse, float(scores["TAU_WARP_TRANSFER_PRIMARY"]["rmse_km_s"])),
        "primary_worse_than_newtonian_full": primary_rmse > newton_rmse,
        "primary_better_than_newtonian_within_rhi": within_primary_rmse < within_newton_rmse,
        "source_correct_worse_than_wrong_onset": primary_rmse > wrong_rmse,
        "three_points_beyond_rhi": int(np.sum(x > 1.0)) == 3,
        "uncapped_kernel_exceeds_one": float(np.max(kernel)) > 1.0,
        "negative_status_preserved": summary["status"] == "RETROSPECTIVE_CLASS_TRANSFER_REJECTS_UNCAPPED_UNIVERSAL_LAW",
        "zone_table_present": ZONE_SCORES.exists() and ZONE_SCORES.stat().st_size > 0,
    }
    passed = int(sum(checks.values()))
    status = "REPRODUCIBILITY_AUDIT_PASS" if passed == len(checks) else "REPRODUCIBILITY_AUDIT_FAIL"
    result = {
        "schema": "tau_core_ugc03580_ugc3580_class_transfer_reproducibility_audit_v01",
        "status": status,
        "checks_passed": passed,
        "checks_total": len(checks),
        "checks": checks,
        "independent_recomputation": {
            "x_w": x_w,
            "lambda_w_km2_s2": lambda_w,
            "primary_rmse_full_km_s": primary_rmse,
            "primary_rmse_within_rhi_km_s": within_primary_rmse,
            "newtonian_rmse_full_km_s": newton_rmse,
            "newtonian_rmse_within_rhi_km_s": within_newton_rmse,
            "wrong_ugc08490_onset_rmse_full_km_s": wrong_rmse,
            "max_uncapped_kernel": float(np.max(kernel)),
        },
        "claim_boundary": "numerical reproducibility only; not physical validation",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# UGC03580 class-transfer reproducibility audit v01",
                "",
                f"Status: `{status}`",
                "",
                f"Independent checks passed: `{passed}/{len(checks)}`.",
                "",
                "The audit independently reloads the raw endpoint, reconstructs the",
                "baryonic curve, source onset, amplitude, unchanged warp kernel, wrong-onset",
                "control, full and within-R_HI RMSE values, and verifies the negative status.",
                "It also confirms that three points lie beyond R_HI and that the unchanged",
                "uncapped kernel exceeds unity there.",
                "",
                "This establishes computational reproducibility, not physical validation.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if status != "REPRODUCIBILITY_AUDIT_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
