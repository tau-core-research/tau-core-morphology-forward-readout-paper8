#!/usr/bin/env python3
"""Run the frozen mixed-readout population endpoint from unchanged manifests.

Construction functions read only frozen formula manifests and generic
prediction columns. Observed velocities are used only in the scoring block.
The current run is a preliminary mixed-population endpoint audit: NGC4013 is
kept as a retrospective frozen-reference protocol, while NGC5907 and caveated
NGC7331 are fresh prospective mixed protocols.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "mixed_readout_population_endpoint_preliminary_control"

sys.path.insert(0, str(ROOT / "scripts"))
import run_source_native_readout_formula_endpoint as src  # noqa: E402
import run_s4g75_promoted_kernel_endpoint_stress_test as promoted  # noqa: E402


def rmse(obs: pd.Series, pred: pd.Series) -> float:
    return float(np.sqrt(np.mean(np.square(pred.to_numpy() - obs.to_numpy()))))


def smoothstep(x: np.ndarray) -> np.ndarray:
    clipped = np.clip(x, 0.0, 1.0)
    return clipped * clipped * (3.0 - 2.0 * clipped)


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


def build_generic_predictions() -> pd.DataFrame:
    points, _labels = src.load_points()
    points = promoted.apply_promoted_observables(points)
    points = src.add_bridge_formula_kernels(points)
    amplitudes = src.fit_amplitudes(points)
    return src.add_predictions(points, amplitudes)


def add_ngc4013_mixed(points: pd.DataFrame, manifest: pd.Series) -> pd.DataFrame:
    sub = points.loc[points["galaxy"].eq("NGC4013")].sort_values("r").reset_index(drop=True).copy()
    r = sub["r"].to_numpy(dtype=float)
    r_warp = float(manifest["r_warp_kpc"])
    r_outer = float(manifest["r_outer_kpc"])
    r_lag_start = float(manifest["r_lag_start_kpc"])
    r_lag_zero = float(manifest["r_lag_zero_kpc"])
    r_s = float(manifest["r_s_kpc"])
    z_ec = float(manifest["z_ec_kpc"])
    gamma = float(manifest["gamma_overlay_upper"])
    omega_z = float(manifest["omega_z"])
    omega_ec = float(manifest["omega_ec"])
    omega_lag = float(manifest["omega_lag"])

    w_warp = smoothstep((r - r_warp) / max(r_outer - r_warp, 1.0e-9))
    k_z = 1.0 / (1.0 + r / max(r_s, 1.0e-9))
    k_ec = 1.0 / (1.0 + r / max(z_ec, 1.0e-9))
    k_lag = np.clip((r_lag_zero - r) / max(r_lag_zero - r_lag_start, 1.0e-9), 0.0, 1.0)
    kernel = w_warp * (omega_z * k_z + omega_ec * k_ec + omega_lag * k_lag)
    attenuation = np.clip(gamma * kernel, 0.0, 0.95)

    v2_carrier = sub["v_K_exponential_disk"].to_numpy(dtype=float) ** 2
    v2_mix = np.maximum(v2_carrier * (1.0 - attenuation), 0.0)
    sub["mixed_kernel"] = kernel
    sub["mixed_attenuation"] = attenuation
    sub["v_mixed_population"] = np.sqrt(v2_mix)
    sub["mixed_formula_id"] = str(manifest["formula_id"])
    sub["mixed_case_status"] = "RETROSPECTIVE_REFERENCE_FROZEN_PROTOCOL_SCORED"
    sub["mixed_case_caveat"] = "not_new_prospective_endpoint_validation"
    return sub


def add_ngc5907_mixed(points: pd.DataFrame, manifest: pd.Series) -> pd.DataFrame:
    sub = points.loc[points["galaxy"].eq("NGC5907")].sort_values("r").reset_index(drop=True).copy()
    r = sub["r"].to_numpy(dtype=float)
    r_in = float(manifest["r_in_kpc"])
    r_out = float(manifest["r_out_kpc"])
    truncation_contrast = float(manifest["truncation_contrast"])
    gamma = float(manifest["gamma_projection"])

    x = (r - r_in) / max(r_out - r_in, 1.0e-9)
    window = smoothstep(x)
    kernel = window * (1.0 + truncation_contrast * window) / (1.0 + truncation_contrast)
    attenuation = np.clip(gamma * kernel, 0.0, 0.95)
    v2_carrier = sub["v_K_exponential_disk"].to_numpy(dtype=float) ** 2
    v2_mix = np.maximum(v2_carrier * (1.0 - attenuation), 0.0)

    sub["mixed_kernel"] = kernel
    sub["mixed_attenuation"] = attenuation
    sub["v_mixed_population"] = np.sqrt(v2_mix)
    sub["mixed_formula_id"] = str(manifest["formula_id"])
    sub["mixed_case_status"] = "FRESH_PROSPECTIVE_MIXED_PROTOCOL_SCORED"
    sub["mixed_case_caveat"] = "prior_projection_endpoint_not_reused_as_mixed_evidence"
    return sub


def add_ngc7331_mixed(points: pd.DataFrame, manifest: pd.Series) -> pd.DataFrame:
    sub = points.loc[points["galaxy"].eq("NGC7331")].sort_values("r").reset_index(drop=True).copy()
    r = sub["r"].to_numpy(dtype=float)
    r_inner = float(manifest["r_window_inner_kpc"])
    r_outer = float(manifest["r_window_outer_kpc"])
    projected_hwhm_over_rs = float(manifest["projected_hwhm_over_Rs"])
    gamma = float(manifest["gamma_vow"])

    x = (r - r_inner) / max(r_outer - r_inner, 1.0e-9)
    w_outer = smoothstep(x)
    k_vertical = 0.5 / (1.0 + r / max(r_inner, 1.0e-9)) + 0.5 * projected_hwhm_over_rs
    kernel = w_outer * k_vertical
    attenuation = np.clip(gamma * kernel, 0.0, 0.95)
    v2_carrier = sub["v_K_exponential_disk"].to_numpy(dtype=float) ** 2
    v2_mix = np.maximum(v2_carrier * (1.0 - attenuation), 0.0)

    sub["mixed_kernel"] = kernel
    sub["mixed_attenuation"] = attenuation
    sub["v_mixed_population"] = np.sqrt(v2_mix)
    sub["mixed_formula_id"] = str(manifest["formula_id"])
    sub["mixed_case_status"] = "CAVEATED_FRESH_PROSPECTIVE_MIXED_PROTOCOL_SCORED"
    sub["mixed_case_caveat"] = "broad_outer_window_no_numeric_warp_onset"
    return sub


def score_case(sub: pd.DataFrame) -> dict[str, object]:
    mixed_rmse = rmse(sub["vobs"], sub["v_mixed_population"])
    return {
        "galaxy": str(sub["galaxy"].iloc[0]),
        "n_points": len(sub),
        "rmse_newton": rmse(sub["vobs"], sub["vn"]),
        "rmse_tpg_v6": rmse(sub["vobs"], sub["v_v6"]),
        "rmse_mond": rmse(sub["vobs"], sub["v_mond"]),
        "rmse_exponential_disk_carrier": rmse(sub["vobs"], sub["v_K_exponential_disk"]),
        "rmse_mixed_population": mixed_rmse,
        "mixed_minus_newton": mixed_rmse - rmse(sub["vobs"], sub["vn"]),
        "mixed_minus_tpg_v6": mixed_rmse - rmse(sub["vobs"], sub["v_v6"]),
        "mixed_minus_mond": mixed_rmse - rmse(sub["vobs"], sub["v_mond"]),
        "mixed_minus_exponential_disk_carrier": mixed_rmse
        - rmse(sub["vobs"], sub["v_K_exponential_disk"]),
        "beats_newton": mixed_rmse < rmse(sub["vobs"], sub["vn"]),
        "beats_tpg_v6": mixed_rmse < rmse(sub["vobs"], sub["v_v6"]),
        "beats_mond": mixed_rmse < rmse(sub["vobs"], sub["v_mond"]),
        "beats_exponential_disk_carrier": mixed_rmse < rmse(sub["vobs"], sub["v_K_exponential_disk"]),
        "mixed_formula_id": str(sub["mixed_formula_id"].iloc[0]),
        "mixed_case_status": str(sub["mixed_case_status"].iloc[0]),
        "mixed_case_caveat": str(sub["mixed_case_caveat"].iloc[0]),
        "construction_used_vobs": False,
        "scoring_used_vobs": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    population = pd.read_csv(DATA / "mixed_readout_population_validation_summary.csv").iloc[0]
    if population["validation_gate_status"] != "MIXED_POPULATION_VALIDATION_READY":
        raise RuntimeError("mixed population gate is not ready for endpoint scoring")
    if bool(population["endpoint_scores_run"]):
        raise RuntimeError("population validation gate should be pre-scoring before this endpoint")

    points = build_generic_predictions()
    manifests = {
        "NGC4013": pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_manifest.csv").iloc[0],
        "NGC5907": pd.read_csv(
            DATA / "ngc5907_expdisk_projection_mixed_formula_freeze_manifest.csv"
        ).iloc[0],
        "NGC7331": pd.read_csv(
            DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_manifest.csv"
        ).iloc[0],
    }
    for galaxy, manifest in manifests.items():
        if bool(manifest.get("uses_vobs_or_residual_in_construction", False)):
            raise RuntimeError(f"{galaxy} mixed manifest is not endpoint-blind")

    case_points = [
        add_ngc4013_mixed(points, manifests["NGC4013"]),
        add_ngc5907_mixed(points, manifests["NGC5907"]),
        add_ngc7331_mixed(points, manifests["NGC7331"]),
    ]
    all_points = pd.concat(case_points, ignore_index=True)
    scores = pd.DataFrame([score_case(sub) for sub in case_points])

    summary = pd.DataFrame(
        [
            {
                "endpoint_status": "MIXED_POPULATION_ENDPOINT_PRELIMINARY_CONTROL_RESULT",
                "n_cases_scored": len(scores),
                "n_fresh_prospective_cases": int(
                    scores["mixed_case_status"].str.contains("FRESH_PROSPECTIVE").sum()
                ),
                "n_caveated_cases": int(scores["mixed_case_status"].str.contains("CAVEATED").sum()),
                "mean_rmse_mixed_population": float(scores["rmse_mixed_population"].mean()),
                "mean_rmse_newton": float(scores["rmse_newton"].mean()),
                "mean_rmse_tpg_v6": float(scores["rmse_tpg_v6"].mean()),
                "mean_rmse_mond": float(scores["rmse_mond"].mean()),
                "mean_rmse_exponential_disk_carrier": float(
                    scores["rmse_exponential_disk_carrier"].mean()
                ),
                "n_beats_newton": int(scores["beats_newton"].sum()),
                "n_beats_tpg_v6": int(scores["beats_tpg_v6"].sum()),
                "n_beats_mond": int(scores["beats_mond"].sum()),
                "n_beats_exponential_disk_carrier": int(
                    scores["beats_exponential_disk_carrier"].sum()
                ),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "claim_boundary": CLAIM_BOUNDARY,
                "claim_status": (
                    "preliminary endpoint scores from frozen mixed manifests; "
                    "not population validation and not baseline-superiority proof"
                ),
            }
        ]
    )

    points_out = all_points[
        [
            "galaxy",
            "r",
            "vobs",
            "errv",
            "vn",
            "v_v6",
            "v_mond",
            "v_K_exponential_disk",
            "mixed_kernel",
            "mixed_attenuation",
            "v_mixed_population",
            "mixed_formula_id",
            "mixed_case_status",
            "mixed_case_caveat",
        ]
    ].copy()
    points_out["construction_used_vobs"] = False
    points_out["scoring_used_vobs"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    scores.to_csv(DATA / "mixed_readout_population_endpoint_scores.csv", index=False)
    points_out.to_csv(DATA / "mixed_readout_population_endpoint_points.csv", index=False)
    summary.to_csv(DATA / "mixed_readout_population_endpoint_summary.csv", index=False)

    report = [
        "# Mixed Readout Population Endpoint",
        "",
        "This script scores the three frozen mixed-readout protocols from unchanged",
        "manifests. Observed velocities are read only by this scoring script.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Claim Boundary",
        "",
        "This is a preliminary control endpoint, not a validation claim. NGC4013 is",
        "a frozen retrospective reference protocol; NGC5907 and caveated NGC7331",
        "are fresh prospective mixed protocols. The NGC7331 broad-window caveat is",
        "preserved.",
        "",
    ]
    (REPORTS / "mixed_readout_population_endpoint.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
