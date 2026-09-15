#!/usr/bin/env python3
"""Score the frozen UGC03580 standard projection control on the opened endpoint."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from warp_class_transfer_common_v01 import load_sparc_endpoint, markdown_table, metric_row


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
MANIFEST = DATA / "ugc03580_signed_descriptor_projection_control_freeze_v01.json"
MANIFEST_SHA = DATA / "ugc03580_signed_descriptor_projection_control_freeze_v01.sha256"
FREEZE_POINTS = DATA / "ugc03580_signed_descriptor_projection_control_freeze_v01_points.csv"
ENDPOINT = ROOT / "data" / "external" / "sparc" / "UGC03580_rotmod.dat"
SCORES_OUT = DATA / "ugc03580_signed_descriptor_projection_control_score_v01.csv"
POINTS_OUT = DATA / "ugc03580_signed_descriptor_projection_control_score_v01_points.csv"
SUMMARY_OUT = DATA / "ugc03580_signed_descriptor_projection_control_score_v01.json"
REPORT = ROOT / "reports" / "ugc03580_signed_descriptor_projection_control_score_v01.md"
CLAIM = "ugc03580_standard_projection_systematics_control_not_tau_endpoint"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    expected = MANIFEST_SHA.read_text(encoding="utf-8").split()[0]
    if sha256(MANIFEST) != expected:
        raise RuntimeError("freeze manifest hash mismatch")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["status"] != "SOURCE_FROZEN_STANDARD_PROJECTION_CONTROL_READY_DIAGNOSTIC_ONLY":
        raise RuntimeError("unexpected freeze status")
    if manifest["endpoint_values_used"] or not manifest["endpoint_scoring_allowed"]:
        raise RuntimeError("freeze did not authorize the diagnostic control")
    if manifest["terminal_formula"]["post_freeze_retuning_allowed"]:
        raise RuntimeError("post-freeze retuning is forbidden")

    frozen = pd.read_csv(FREEZE_POINTS)
    points = load_sparc_endpoint(ENDPOINT)
    radius = points["r_kpc"].to_numpy(float)
    lo = float(frozen["radius_kpc_terminal_calibration"].min())
    hi = float(frozen["radius_kpc_terminal_calibration"].max())
    if radius.min() < lo - 1.0e-12 or radius.max() > hi + 1.0e-12:
        raise RuntimeError("rotation endpoint extends outside frozen projection support")
    factor = np.interp(
        radius,
        frozen["radius_kpc_terminal_calibration"].to_numpy(float),
        frozen["projection_velocity_factor"].to_numpy(float),
    )
    carriers = {
        "NEWTONIAN": points["vn_km_s"].to_numpy(float),
        "TPG_V6": points["v_tpg_v6_km_s"].to_numpy(float),
        "MOND": points["v_mond_km_s"].to_numpy(float),
    }
    predictions: dict[str, np.ndarray] = {}
    roles: dict[str, str] = {}
    for name, carrier in carriers.items():
        predictions[f"{name}_UNCORRECTED"] = carrier
        roles[f"{name}_UNCORRECTED"] = "fixed_baseline"
        predictions[f"{name}_SOURCE_PROJECTION_CONTROL"] = factor * carrier
        roles[f"{name}_SOURCE_PROJECTION_CONTROL"] = "standard_projection_systematics_control"
    scores = pd.DataFrame(
        [metric_row(points, key, roles[key], value) for key, value in predictions.items()]
    ).sort_values("rmse_km_s")
    scores["claim_boundary"] = CLAIM
    scores.to_csv(SCORES_OUT, index=False, float_format="%.12g")

    point_out = points.copy()
    point_out["projection_velocity_factor_frozen"] = factor
    for key, value in predictions.items():
        point_out[f"pred_{key}"] = value
    point_out["construction_used_vobs_or_residual"] = False
    point_out["scoring_used_vobs"] = True
    point_out["claim_boundary"] = CLAIM
    point_out.to_csv(POINTS_OUT, index=False, float_format="%.12g")

    lookup = scores.set_index("model_id")
    changes = {}
    for name in carriers:
        before = float(lookup.loc[f"{name}_UNCORRECTED", "rmse_km_s"])
        after = float(lookup.loc[f"{name}_SOURCE_PROJECTION_CONTROL", "rmse_km_s"])
        changes[name] = {
            "rmse_uncorrected_km_s": before,
            "rmse_projection_control_km_s": after,
            "delta_rmse_projection_minus_uncorrected_km_s": after - before,
            "projection_improves_rmse": after < before,
        }
    result = {
        "schema": "tau_core_ugc03580_signed_descriptor_projection_control_score_v01",
        "status": "DIAGNOSTIC_STANDARD_PROJECTION_CONTROL_SCORED_NOT_TAU_ENDPOINT",
        "galaxy": "UGC03580",
        "n_points": int(len(points)),
        "freeze_manifest_sha256": expected,
        "endpoint_sha256": sha256(ENDPOINT),
        "construction_used_vobs_or_residual": False,
        "scoring_used_vobs": True,
        "projection_factor_range": [float(factor.min()), float(factor.max())],
        "carrier_results": changes,
        "best_model": str(scores.iloc[0]["model_id"]),
        "interpretation": (
            "This measures an ordinary inclination/projection sensitivity from a source-frozen "
            "signed descriptor. It is not a Tau score. If the SPARC terminal already includes "
            "the same tilted-ring correction, applying it again is double counting, so the result "
            "must remain a systematics control."
        ),
        "claim_boundary": CLAIM,
    }
    SUMMARY_OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    summary = pd.DataFrame([
        {
            "status": result["status"],
            "n_points": len(points),
            "best_model": result["best_model"],
            "projection_factor_min": factor.min(),
            "projection_factor_max": factor.max(),
            "construction_used_vobs_or_residual": False,
            "scoring_used_vobs": True,
        }
    ])
    change_frame = pd.DataFrame(
        [{"carrier": key, **value} for key, value in changes.items()]
    )
    REPORT.write_text(
        "# UGC03580 signed-descriptor standard projection control score v01\n\n"
        + markdown_table(summary)
        + "\n\n## Carrier comparison\n\n"
        + markdown_table(change_frame)
        + "\n\n## All declared models\n\n"
        + markdown_table(scores)
        + "\n\nThis is a diagnostic standard-systematics control, not a Tau endpoint. "
        "It cannot be interpreted as evidence for parent morphology or as a dark-matter replacement.\n",
        encoding="utf-8",
    )
    print("UGC03580_SIGNED_DESCRIPTOR_PROJECTION_SCORE_PASS")


if __name__ == "__main__":
    main()
