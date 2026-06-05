#!/usr/bin/env python3
"""Run the dedicated NGC7331 V2/V3 replay/holdout endpoint.

This is a replay/holdout scoring script. It reads observed velocities only in
the scoring block and does not update the already accepted caveated V1 endpoint.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc7331_v2_v3_replay_holdout_endpoint_not_v1_update"

sys.path.insert(0, str(ROOT / "scripts"))
import run_mixed_kernel_sharpened_replay_holdout_endpoint as sharpened  # noqa: E402
import run_mixed_readout_population_endpoint as endpoint  # noqa: E402


def rmse(obs: pd.Series, pred: pd.Series) -> float:
    return float(np.sqrt(np.mean(np.square(pred.to_numpy() - obs.to_numpy()))))


def mae(obs: pd.Series, pred: pd.Series) -> float:
    return float(np.mean(np.abs(pred.to_numpy() - obs.to_numpy())))


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def score_model(points: pd.DataFrame, model_id: str, model_role: str, column: str) -> dict[str, object]:
    return {
        "galaxy": "NGC7331",
        "model_id": model_id,
        "model_role": model_role,
        "n_points": len(points),
        "rmse_km_s": rmse(points["vobs"], points[column]),
        "mae_km_s": mae(points["vobs"], points[column]),
        "construction_used_vobs": False,
        "scoring_used_vobs": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    v2_summary = pd.read_csv(DATA / "ngc7331_fractional_onset_v2_replay_freeze_summary.csv").iloc[0]
    if str(v2_summary["v2_replay_freeze_status"]) != "V2_REPLAY_PROTOCOL_READY_NOT_SCORED":
        raise RuntimeError("NGC7331 V2 replay freeze is not ready")

    sharpened_summary = pd.read_csv(DATA / "mixed_kernel_sharpened_replay_freeze_summary.csv").iloc[0]
    if str(sharpened_summary["freeze_status"]) != "SHARPENED_REPLAY_FREEZE_READY_NOT_SCORED":
        raise RuntimeError("source-sharpened replay freeze is not ready")

    v1_manifest = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_manifest.csv"
    ).iloc[0]
    v2_manifest = pd.read_csv(DATA / "ngc7331_fractional_onset_v2_replay_freeze_manifest.csv").iloc[0]
    sharp_manifest = pd.read_csv(DATA / "mixed_kernel_sharpened_replay_freeze_manifest.csv")
    v3_manifest = sharp_manifest.loc[sharp_manifest["galaxy"].eq("NGC7331")].iloc[0]
    wrong_sharp_manifest = sharp_manifest.loc[sharp_manifest["galaxy"].eq("NGC5907")].iloc[0]

    for manifest, name in [(v1_manifest, "V1"), (v2_manifest, "V2"), (v3_manifest, "V3")]:
        if bool(manifest["uses_vobs_or_residual_in_construction"]):
            raise RuntimeError(f"{name} manifest is not endpoint-blind")

    generic = endpoint.build_generic_predictions()
    v1_points = endpoint.add_ngc7331_mixed(generic, v1_manifest)
    v2_points = endpoint.add_ngc7331_mixed(generic, v2_manifest)
    v3_points = sharpened.apply_formula(generic, "NGC7331", v3_manifest)
    wrong_v3_points = sharpened.apply_formula(generic, "NGC7331", wrong_sharp_manifest)

    points = v1_points[
        ["galaxy", "r", "vobs", "errv", "vn", "v_v6", "v_mond", "v_K_exponential_disk"]
    ].copy()
    points["v_v1_broad_window_accepted_reference"] = v1_points["v_mixed_population"].to_numpy()
    points["kernel_v1_broad_window"] = v1_points["mixed_kernel"].to_numpy()
    points["v_v2_fractional_onset_replay"] = v2_points["v_mixed_population"].to_numpy()
    points["kernel_v2_fractional_onset"] = v2_points["mixed_kernel"].to_numpy()
    points["v_v3_source_sharpened_replay"] = v3_points["v_mixed_sharpened_replay"].to_numpy()
    points["kernel_v3_source_sharpened"] = v3_points["mixed_kernel_sharpened"].to_numpy()
    points["v_wrong_projection_sharpened_control"] = wrong_v3_points[
        "v_mixed_sharpened_replay"
    ].to_numpy()
    points["kernel_wrong_projection_sharpened_control"] = wrong_v3_points[
        "mixed_kernel_sharpened"
    ].to_numpy()
    points["construction_used_vobs"] = False
    points["scoring_used_vobs"] = True
    points["current_v1_endpoint_updated"] = False
    points["claim_boundary"] = CLAIM_BOUNDARY

    score_rows = [
        score_model(points, "TAU_NGC7331_V3_SOURCE_SHARPENED_REPLAY", "matched_v3_replay", "v_v3_source_sharpened_replay"),
        score_model(points, "TAU_NGC7331_V2_FRACTIONAL_ONSET_REPLAY", "matched_v2_replay", "v_v2_fractional_onset_replay"),
        score_model(points, "TAU_NGC7331_V1_ACCEPTED_REFERENCE_NOT_UPDATED", "v1_accepted_reference", "v_v1_broad_window_accepted_reference"),
        score_model(points, "WRONG_SHARPENED_NGC5907_PROJECTION", "wrong_sharpened_replay_control", "v_wrong_projection_sharpened_control"),
        score_model(points, "EXPONENTIAL_DISK_CARRIER", "baseline", "v_K_exponential_disk"),
        score_model(points, "TPG_V6_v_v6", "baseline", "v_v6"),
        score_model(points, "MOND_v_mond", "baseline", "v_mond"),
        score_model(points, "NEWTONIAN_vn", "baseline", "vn"),
    ]
    scores = pd.DataFrame(score_rows).sort_values("rmse_km_s").reset_index(drop=True)

    v1 = scores.loc[scores["model_id"].eq("TAU_NGC7331_V1_ACCEPTED_REFERENCE_NOT_UPDATED")].iloc[0]
    v2 = scores.loc[scores["model_id"].eq("TAU_NGC7331_V2_FRACTIONAL_ONSET_REPLAY")].iloc[0]
    v3 = scores.loc[scores["model_id"].eq("TAU_NGC7331_V3_SOURCE_SHARPENED_REPLAY")].iloc[0]
    wrong = scores.loc[scores["model_role"].eq("wrong_sharpened_replay_control")].iloc[0]
    baselines = scores.loc[scores["model_role"].eq("baseline")]

    summary = pd.DataFrame(
        [
            {
                "endpoint_status": "NGC7331_V2_V3_REPLAY_HOLDOUT_PRELIMINARY_CONTROL_RESULT",
                "galaxy": "NGC7331",
                "n_points": len(points),
                "v1_reference_rmse_km_s": float(v1["rmse_km_s"]),
                "v2_fractional_onset_rmse_km_s": float(v2["rmse_km_s"]),
                "v3_source_sharpened_rmse_km_s": float(v3["rmse_km_s"]),
                "best_baseline_rmse_km_s": float(baselines["rmse_km_s"].min()),
                "wrong_projection_sharpened_rmse_km_s": float(wrong["rmse_km_s"]),
                "v3_minus_v1_rmse_km_s": float(v3["rmse_km_s"] - v1["rmse_km_s"]),
                "v3_minus_v2_rmse_km_s": float(v3["rmse_km_s"] - v2["rmse_km_s"]),
                "v3_minus_best_baseline_rmse_km_s": float(
                    v3["rmse_km_s"] - baselines["rmse_km_s"].min()
                ),
                "v3_minus_wrong_projection_rmse_km_s": float(v3["rmse_km_s"] - wrong["rmse_km_s"]),
                "v3_beats_v1_reference": bool(v3["rmse_km_s"] < v1["rmse_km_s"]),
                "v3_beats_v2_fractional_onset": bool(v3["rmse_km_s"] < v2["rmse_km_s"]),
                "v3_beats_best_baseline": bool(v3["rmse_km_s"] < baselines["rmse_km_s"].min()),
                "v3_beats_wrong_projection_control": bool(v3["rmse_km_s"] < wrong["rmse_km_s"]),
                "current_v1_endpoint_updated": False,
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "claim_status": (
                    "dedicated NGC7331 replay/holdout result; not a retroactive V1 endpoint update"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_RHG1_V2_FREEZE_READY",
                "gate_status": "PASS",
                "evidence": str(v2_summary["v2_replay_freeze_status"]),
                "remaining_obligation": "none at V2 replay-freeze level",
            },
            {
                "gate_id": "N7331_RHG2_V3_SHARPENED_FREEZE_READY",
                "gate_status": "PASS",
                "evidence": str(sharpened_summary["freeze_status"]),
                "remaining_obligation": "none at V3 sharpened-freeze level",
            },
            {
                "gate_id": "N7331_RHG3_ENDPOINT_BLIND_CONSTRUCTION",
                "gate_status": "PASS",
                "evidence": "all replay manifests have uses_vobs_or_residual_in_construction=false",
                "remaining_obligation": "scoring reads vobs only in this script",
            },
            {
                "gate_id": "N7331_RHG4_NO_RETROACTIVE_V1_UPDATE",
                "gate_status": "PASS",
                "evidence": "current_v1_endpoint_updated=false",
                "remaining_obligation": "accepted V1 score remains caveated accepted endpoint",
            },
            {
                "gate_id": "N7331_RHG5_REPLAY_CONTROL_SCOPE",
                "gate_status": "PASS_CLAIM_BOUNDED",
                "evidence": "single-galaxy replay/holdout control",
                "remaining_obligation": "do not use as population validation",
            },
        ]
    )
    gates["endpoint_scores_allowed"] = True
    gates["current_v1_endpoint_updated"] = False
    gates["uses_vobs_or_residual_in_construction"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    points.to_csv(DATA / "ngc7331_v2_v3_replay_holdout_endpoint_points.csv", index=False)
    scores.to_csv(DATA / "ngc7331_v2_v3_replay_holdout_endpoint_scores.csv", index=False)
    summary.to_csv(DATA / "ngc7331_v2_v3_replay_holdout_endpoint_summary.csv", index=False)
    gates.to_csv(DATA / "ngc7331_v2_v3_replay_holdout_endpoint_gates.csv", index=False)

    report = [
        "# NGC7331 V2/V3 Replay/Holdout Endpoint",
        "",
        "This dedicated replay/holdout endpoint scores the NGC7331 V2 fractional",
        "onset and V3 source-sharpened manifests. It does not update the accepted",
        "V1 endpoint.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "Status: this is not a retroactive update of the accepted V1 endpoint.",
        "",
        "The result is a single-galaxy replay/holdout control. It can reduce the",
        "NGC7331 broad-window caveat for the replay path, but it is not a",
        "retroactive update of the already accepted V1 endpoint and not population",
        "validation.",
        "",
    ]
    (REPORTS / "ngc7331_v2_v3_replay_holdout_endpoint.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
