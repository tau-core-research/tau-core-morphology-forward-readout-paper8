#!/usr/bin/env python3
"""Score the frozen NGC4088 warp/history class law on UGC08490.

The companion freeze manifest is verified before this script opens the
pointwise SPARC endpoint.  No target parameter is retuned.  UGC08490 was seen
in earlier tracer analyses, so the result is explicitly retrospective.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import least_squares


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "paper8_submission_source" / "figures"

MANIFEST = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_freeze_v01.json"
MANIFEST_SHA = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_freeze_v01.sha256"
ENDPOINT = ROOT / "data" / "external" / "sparc" / "UGC08490_rotmod.dat"

POINTS_OUT = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_endpoint_v01_points.csv"
SCORES_OUT = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_endpoint_v01_scores.csv"
SUMMARY_OUT = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_endpoint_v01.json"
REPORT_OUT = REPORTS / "ugc08490_ngc5204_ngc4088_class_transfer_endpoint_v01.md"
FIGURE_OUT = FIGURES / "fig_ugc08490_ngc5204_ngc4088_class_transfer_v01.png"

CLAIM_BOUNDARY = "retrospective_single_galaxy_class_transfer_negative_not_tau_falsification"
KPC_M = 3.0857e19
A0_M_S2 = 1.2e-10
ALPHA_V6 = 0.360
H0_KM_S_KPC = 0.070
NGC4088_XW_CONTROL = 0.2983326403051493
BOOTSTRAP_SEED = 8490
N_BOOTSTRAP = 20000
BLOCK_LENGTH = 3


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_freeze() -> dict[str, object]:
    expected = MANIFEST_SHA.read_text(encoding="utf-8").split()[0]
    actual = sha256(MANIFEST)
    if actual != expected:
        raise RuntimeError("freeze manifest hash mismatch")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["freeze_status"] != "RETROSPECTIVE_SOURCE_FROZEN_CLASS_TRANSFER_READY_NOT_SCORED":
        raise RuntimeError("unexpected freeze status")
    if not manifest["formula_frozen_before_current_endpoint_scoring"]:
        raise RuntimeError("formula was not certified frozen before scoring")
    if manifest["formula"]["post_freeze_retuning_allowed"]:
        raise RuntimeError("retuning must remain forbidden")
    if manifest["source_selection"]["selection_uses_pointwise_vobs_or_residual"]:
        raise RuntimeError("target selection is not endpoint-blind")
    return manifest


def load_endpoint() -> pd.DataFrame:
    rows: list[dict[str, float]] = []
    for raw in ENDPOINT.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        values = list(map(float, line.split()[:8]))
        r, vobs, errv, vgas, vdisk, vbul, sbdisk, sbbul = values
        gas2 = vgas * abs(vgas)
        baryon_v2 = gas2 + 0.5 * vdisk**2 + 0.7 * vbul**2
        vn = math.sqrt(max(baryon_v2, 0.0))
        a_n = (vn * 1000.0) ** 2 / (r * KPC_M)
        f_v6 = 1.0 + ALPHA_V6 * math.log1p(A0_M_S2 / a_n)
        f_mond = math.sqrt((1.0 + math.sqrt(1.0 + 4.0 * A0_M_S2 / a_n)) / 2.0)
        rows.append(
            {
                "r_kpc": r,
                "vobs_km_s": vobs,
                "errv_km_s": errv,
                "vgas_km_s": vgas,
                "vdisk_km_s": vdisk,
                "vbul_km_s": vbul,
                "vn_km_s": vn,
                "v_tpg_v6_km_s": vn * f_v6,
                "v_mond_km_s": vn * f_mond,
            }
        )
    return pd.DataFrame(rows)


def warp_prediction(
    points: pd.DataFrame,
    *,
    r_hi_kpc: float,
    x_w: float,
    lambda_w: float,
    power: float,
    sign: float = 1.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = points["r_kpc"].to_numpy(dtype=float) / r_hi_kpc
    kernel = np.maximum(0.0, (x - x_w) / (1.0 - x_w)) ** power
    v2 = points["vn_km_s"].to_numpy(dtype=float) ** 2 + sign * lambda_w * kernel
    prediction = np.where(v2 >= 0.0, np.sqrt(np.maximum(v2, 0.0)), np.nan)
    return prediction, kernel, v2


def nfw_halo_v2(r: np.ndarray, v200: float, concentration: float) -> np.ndarray:
    r200 = v200 / (10.0 * H0_KM_S_KPC)
    x = np.maximum(r / r200, 1.0e-10)
    cx = concentration * x
    numerator = np.log1p(cx) - cx / (1.0 + cx)
    denominator = x * (math.log1p(concentration) - concentration / (1.0 + concentration))
    return v200**2 * numerator / denominator


def pseudo_iso_halo_v2(r: np.ndarray, v_inf: float, r_core: float) -> np.ndarray:
    ratio = np.maximum(r / r_core, 1.0e-10)
    return v_inf**2 * (1.0 - np.arctan(ratio) / ratio)


def fit_halo(points: pd.DataFrame, family: str) -> tuple[np.ndarray, dict[str, float]]:
    r = points["r_kpc"].to_numpy(dtype=float)
    vn2 = points["vn_km_s"].to_numpy(dtype=float) ** 2
    obs = points["vobs_km_s"].to_numpy(dtype=float)
    err = points["errv_km_s"].to_numpy(dtype=float)

    if family == "NFW":
        def pred(theta: np.ndarray) -> np.ndarray:
            return np.sqrt(vn2 + nfw_halo_v2(r, float(theta[0]), float(theta[1])))

        result = least_squares(
            lambda theta: (pred(theta) - obs) / err,
            x0=np.array([80.0, 10.0]),
            bounds=(np.array([5.0, 0.5]), np.array([300.0, 60.0])),
        )
        params = {"v200_km_s": float(result.x[0]), "concentration": float(result.x[1])}
    elif family == "PSEUDO_ISOTHERMAL":
        def pred(theta: np.ndarray) -> np.ndarray:
            return np.sqrt(vn2 + pseudo_iso_halo_v2(r, float(theta[0]), float(theta[1])))

        result = least_squares(
            lambda theta: (pred(theta) - obs) / err,
            x0=np.array([80.0, 1.5]),
            bounds=(np.array([1.0, 0.02]), np.array([300.0, 50.0])),
        )
        params = {"v_inf_km_s": float(result.x[0]), "r_core_kpc": float(result.x[1])}
    else:  # pragma: no cover
        raise ValueError(family)
    params["optimizer_success"] = bool(result.success)
    return pred(result.x), params


def metric_row(
    points: pd.DataFrame,
    model_id: str,
    role: str,
    prediction: np.ndarray,
    *,
    endpoint_fit_parameters: int = 0,
    imported_summary_scalars: int = 0,
) -> dict[str, object]:
    obs = points["vobs_km_s"].to_numpy(dtype=float)
    err = points["errv_km_s"].to_numpy(dtype=float)
    valid = np.isfinite(prediction)
    if not np.all(valid):
        return {
            "model_id": model_id,
            "role": role,
            "valid_full_endpoint": False,
            "n_points": int(valid.sum()),
            "rmse_km_s": np.nan,
            "mae_km_s": np.nan,
            "bias_km_s": np.nan,
            "chi2": np.nan,
            "chi2_per_point": np.nan,
            "aic_known_errors": np.nan,
            "bic_known_errors": np.nan,
            "endpoint_fit_parameters": endpoint_fit_parameters,
            "imported_summary_scalars": imported_summary_scalars,
        }
    residual = prediction - obs
    chi2 = float(np.sum((residual / err) ** 2))
    n = len(obs)
    return {
        "model_id": model_id,
        "role": role,
        "valid_full_endpoint": True,
        "n_points": n,
        "rmse_km_s": float(np.sqrt(np.mean(residual**2))),
        "mae_km_s": float(np.mean(np.abs(residual))),
        "bias_km_s": float(np.mean(residual)),
        "chi2": chi2,
        "chi2_per_point": chi2 / n,
        "aic_known_errors": chi2 + 2.0 * endpoint_fit_parameters,
        "bic_known_errors": chi2 + endpoint_fit_parameters * math.log(n),
        "endpoint_fit_parameters": endpoint_fit_parameters,
        "imported_summary_scalars": imported_summary_scalars,
    }


def circular_block_bootstrap_delta(
    primary_sq_error: np.ndarray,
    comparator_sq_error: np.ndarray,
) -> dict[str, float]:
    delta = primary_sq_error - comparator_sq_error
    n = len(delta)
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    means = np.empty(N_BOOTSTRAP, dtype=float)
    n_blocks = math.ceil(n / BLOCK_LENGTH)
    for draw in range(N_BOOTSTRAP):
        starts = rng.integers(0, n, size=n_blocks)
        idx = np.concatenate(
            [(np.arange(start, start + BLOCK_LENGTH) % n) for start in starts]
        )[:n]
        means[draw] = float(np.mean(delta[idx]))
    return {
        "observed_delta_mse_primary_minus_comparator": float(np.mean(delta)),
        "bootstrap_ci95_low": float(np.quantile(means, 0.025)),
        "bootstrap_ci95_high": float(np.quantile(means, 0.975)),
        "bootstrap_fraction_primary_better": float(np.mean(means < 0.0)),
        "n_bootstrap": N_BOOTSTRAP,
        "block_length": BLOCK_LENGTH,
    }


def markdown_table(frame: pd.DataFrame) -> str:
    display = frame.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(
                lambda value: "" if pd.isna(value) else f"{value:.6g}"
            )
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    manifest = verify_freeze()
    points = load_endpoint()
    frozen = manifest["derived_frozen_values"]
    source = manifest["frozen_source_inputs"]
    formula = manifest["formula"]

    r_hi = float(source["r_hi_kpc"])
    x_w = float(frozen["x_w"])
    lambda_primary = float(frozen["lambda_w_primary_km2_s2"])
    lambda_sensitivity = float(frozen["lambda_w_source_speed_sensitivity_km2_s2"])
    power = float(formula["turn_on_power"])

    primary, kernel, primary_v2 = warp_prediction(
        points, r_hi_kpc=r_hi, x_w=x_w, lambda_w=lambda_primary, power=power
    )
    source_speed, _, _ = warp_prediction(
        points, r_hi_kpc=r_hi, x_w=x_w, lambda_w=lambda_sensitivity, power=power
    )
    p2, _, _ = warp_prediction(
        points, r_hi_kpc=r_hi, x_w=x_w, lambda_w=lambda_primary, power=2.0
    )
    wrong_x_lambda = NGC4088_XW_CONTROL * float(source["vflat_km_s_primary"]) ** 2
    wrong_x, _, _ = warp_prediction(
        points,
        r_hi_kpc=r_hi,
        x_w=NGC4088_XW_CONTROL,
        lambda_w=wrong_x_lambda,
        power=1.0,
    )
    wrong_sign, _, wrong_sign_v2 = warp_prediction(
        points,
        r_hi_kpc=r_hi,
        x_w=x_w,
        lambda_w=lambda_primary,
        power=power,
        sign=-1.0,
    )
    nfw, nfw_params = fit_halo(points, "NFW")
    piso, piso_params = fit_halo(points, "PSEUDO_ISOTHERMAL")

    predictions = {
        "TAU_WARP_TRANSFER_PRIMARY": primary,
        "TAU_WARP_TRANSFER_SOURCE_SPEED_SENSITIVITY": source_speed,
        "NEWTONIAN_BARYONIC": points["vn_km_s"].to_numpy(dtype=float),
        "TPG_V6_FIXED": points["v_tpg_v6_km_s"].to_numpy(dtype=float),
        "MOND_FIXED_A0": points["v_mond_km_s"].to_numpy(dtype=float),
        "CONTROL_WRONG_NGC4088_ONSET": wrong_x,
        "CONTROL_WRONG_P2": p2,
        "CONTROL_WRONG_SIGN": wrong_sign,
        "NFW_TWO_PARAMETER_ENDPOINT_FIT": nfw,
        "PSEUDO_ISOTHERMAL_TWO_PARAMETER_ENDPOINT_FIT": piso,
    }
    specs = {
        "TAU_WARP_TRANSFER_PRIMARY": ("matched_frozen_transfer", 0, 2),
        "TAU_WARP_TRANSFER_SOURCE_SPEED_SENSITIVITY": ("predeclared_sensitivity", 0, 1),
        "NEWTONIAN_BARYONIC": ("fixed_standard_comparator", 0, 0),
        "TPG_V6_FIXED": ("fixed_standard_comparator", 0, 0),
        "MOND_FIXED_A0": ("fixed_standard_comparator", 0, 0),
        "CONTROL_WRONG_NGC4088_ONSET": ("morphology_control", 0, 2),
        "CONTROL_WRONG_P2": ("morphology_control", 0, 2),
        "CONTROL_WRONG_SIGN": ("morphology_control", 0, 2),
        "NFW_TWO_PARAMETER_ENDPOINT_FIT": ("fit_aided_standard_comparator", 2, 0),
        "PSEUDO_ISOTHERMAL_TWO_PARAMETER_ENDPOINT_FIT": ("fit_aided_standard_comparator", 2, 0),
    }
    score_rows = [
        metric_row(
            points,
            model_id,
            specs[model_id][0],
            prediction,
            endpoint_fit_parameters=specs[model_id][1],
            imported_summary_scalars=specs[model_id][2],
        )
        for model_id, prediction in predictions.items()
    ]
    scores = pd.DataFrame(score_rows)
    scores["claim_boundary"] = CLAIM_BOUNDARY
    scores = scores.sort_values(["valid_full_endpoint", "rmse_km_s"], ascending=[False, True])

    points_out = points.copy()
    points_out["x_R_over_RHI"] = points_out["r_kpc"] / r_hi
    points_out["x_w_frozen"] = x_w
    points_out["warp_kernel_frozen"] = kernel
    points_out["primary_total_v2_km2_s2"] = primary_v2
    for model_id, prediction in predictions.items():
        points_out[f"pred_{model_id}"] = prediction
        points_out[f"resid_{model_id}"] = prediction - points_out["vobs_km_s"]
    points_out["wrong_sign_total_v2_km2_s2"] = wrong_sign_v2
    points_out["construction_used_pointwise_vobs_or_residual"] = False
    points_out["scoring_used_vobs"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    pre = points_out[points_out["x_R_over_RHI"] <= x_w]
    post = points_out[points_out["x_R_over_RHI"] > x_w]
    radial_rows = []
    for zone_name, zone in [("pre_onset", pre), ("post_onset", post)]:
        for model_id in ["TAU_WARP_TRANSFER_PRIMARY", "MOND_FIXED_A0", "TPG_V6_FIXED"]:
            pred = zone[f"pred_{model_id}"].to_numpy(dtype=float)
            obs = zone["vobs_km_s"].to_numpy(dtype=float)
            radial_rows.append(
                {
                    "zone": zone_name,
                    "model_id": model_id,
                    "n_points": len(zone),
                    "rmse_km_s": float(np.sqrt(np.mean((pred - obs) ** 2))),
                    "bias_km_s": float(np.mean(pred - obs)),
                }
            )
    radial = pd.DataFrame(radial_rows)

    obs = points["vobs_km_s"].to_numpy(dtype=float)
    boot_mond = circular_block_bootstrap_delta((primary - obs) ** 2, (predictions["MOND_FIXED_A0"] - obs) ** 2)
    boot_wrong_x = circular_block_bootstrap_delta(
        (primary - obs) ** 2, (predictions["CONTROL_WRONG_NGC4088_ONSET"] - obs) ** 2
    )

    # Endpoint-informed diagnostic only: never used to repair the frozen result.
    scan_rows = []
    for trial_x in np.linspace(0.05, 0.90, 342):
        trial_lambda = trial_x * float(source["vflat_km_s_primary"]) ** 2
        trial, _, _ = warp_prediction(
            points, r_hi_kpc=r_hi, x_w=float(trial_x), lambda_w=trial_lambda, power=1.0
        )
        scan_rows.append(
            {
                "x_w": float(trial_x),
                "rmse_km_s": float(np.sqrt(np.mean((trial - obs) ** 2))),
            }
        )
    scan = pd.DataFrame(scan_rows)
    preferred = scan.sort_values("rmse_km_s").iloc[0]

    primary_score = scores.loc[scores["model_id"].eq("TAU_WARP_TRANSFER_PRIMARY")].iloc[0]
    mond_score = scores.loc[scores["model_id"].eq("MOND_FIXED_A0")].iloc[0]
    wrong_x_score = scores.loc[scores["model_id"].eq("CONTROL_WRONG_NGC4088_ONSET")].iloc[0]
    piso_score = scores.loc[
        scores["model_id"].eq("PSEUDO_ISOTHERMAL_TWO_PARAMETER_ENDPOINT_FIT")
    ].iloc[0]

    matched_beats_fixed_mond = bool(primary_score["rmse_km_s"] < mond_score["rmse_km_s"])
    matched_beats_wrong_onset = bool(primary_score["rmse_km_s"] < wrong_x_score["rmse_km_s"])
    matched_beats_fit_halo = bool(primary_score["rmse_km_s"] < piso_score["rmse_km_s"])
    transfer_status = (
        "RETROSPECTIVE_CLASS_TRANSFER_PASS"
        if matched_beats_fixed_mond and matched_beats_wrong_onset
        else "RETROSPECTIVE_CLASS_TRANSFER_NEGATIVE"
    )

    summary = {
        "schema": "tau_core_ugc08490_ngc5204_ngc4088_class_transfer_endpoint_v01",
        "status": transfer_status,
        "galaxy": "UGC08490",
        "alias": "NGC5204",
        "formula_id": manifest["formula_id"],
        "freeze_manifest_sha256": sha256(MANIFEST),
        "n_points": len(points),
        "n_pre_onset": len(pre),
        "n_post_onset": len(post),
        "x_w_frozen": x_w,
        "primary_rmse_km_s": float(primary_score["rmse_km_s"]),
        "fixed_mond_rmse_km_s": float(mond_score["rmse_km_s"]),
        "wrong_ngc4088_onset_rmse_km_s": float(wrong_x_score["rmse_km_s"]),
        "best_fit_halo_rmse_km_s": float(scores.loc[scores["role"].eq("fit_aided_standard_comparator"), "rmse_km_s"].min()),
        "matched_beats_fixed_mond": matched_beats_fixed_mond,
        "matched_beats_wrong_onset_control": matched_beats_wrong_onset,
        "matched_beats_best_fit_halo": matched_beats_fit_halo,
        "endpoint_informed_preferred_x_w_diagnostic": float(preferred["x_w"]),
        "endpoint_informed_preferred_x_w_rmse_km_s": float(preferred["rmse_km_s"]),
        "frozen_x_w_minus_endpoint_preferred_x_w": x_w - float(preferred["x_w"]),
        "bootstrap_primary_vs_mond": boot_mond,
        "bootstrap_primary_vs_wrong_onset": boot_wrong_x,
        "halo_fit_parameters": {"NFW": nfw_params, "PSEUDO_ISOTHERMAL": piso_params},
        "interpretation": (
            "The source-correct outer-warp law does not transfer as a complete rotation-law "
            "explanation if it fails the fixed MOND and wrong-onset controls. This is a "
            "negative result for the current universal class-law transfer, not a "
            "falsification of Tau Core or of morphology-conditioned readouts in general."
        ),
        "construction_used_pointwise_vobs_or_residual": False,
        "scoring_used_vobs": True,
        "prospective_blind_endpoint": False,
        "post_endpoint_repair_performed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    points_out.to_csv(POINTS_OUT, index=False)
    scores.to_csv(SCORES_OUT, index=False)
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    try:
        import matplotlib.pyplot as plt

        fig, (ax, axr) = plt.subplots(2, 1, figsize=(8.0, 7.2), sharex=True, height_ratios=[2.2, 1.0])
        ax.errorbar(
            points["r_kpc"], points["vobs_km_s"], yerr=points["errv_km_s"],
            fmt="o", color="black", ms=3.7, lw=0.8, label="SPARC observed", zorder=10,
        )
        ax.plot(points["r_kpc"], points["vn_km_s"], color="0.55", label="Newtonian baryonic")
        ax.plot(points["r_kpc"], points["v_mond_km_s"], color="#356cb4", label="fixed MOND")
        ax.plot(points["r_kpc"], primary, color="#f28e2b", lw=2.5, label="frozen source-correct warp transfer")
        ax.plot(points["r_kpc"], wrong_x, color="#8c564b", ls="--", label="wrong NGC4088 onset control")
        ax.plot(points["r_kpc"], piso, color="#2ca02c", ls=":", lw=2.0, label="2-parameter pseudo-isothermal fit")
        onset_radius = x_w * r_hi
        ax.axvline(onset_radius, color="#f28e2b", alpha=0.5, lw=1.2)
        ax.set_ylabel("velocity [km/s]")
        ax.set_title("UGC08490 / NGC5204: unchanged NGC4088 warp-law transfer")
        ax.legend(fontsize=7.5, ncol=2)
        ax.grid(alpha=0.2)
        axr.axhline(0.0, color="0.4", lw=0.8)
        axr.plot(points["r_kpc"], primary - obs, color="#f28e2b", label="frozen transfer")
        axr.plot(points["r_kpc"], predictions["MOND_FIXED_A0"] - obs, color="#356cb4", label="MOND")
        axr.axvline(onset_radius, color="#f28e2b", alpha=0.5, lw=1.2)
        axr.set_xlabel("R [kpc]")
        axr.set_ylabel("model - data")
        axr.grid(alpha=0.2)
        fig.tight_layout()
        fig.savefig(FIGURE_OUT, dpi=190)
        plt.close(fig)
    except Exception as exc:  # pragma: no cover
        print(f"plot skipped: {exc}")

    report = [
        "# UGC08490 / NGC5204 unchanged NGC4088-class transfer endpoint v01",
        "",
        f"Status: `{transfer_status}`",
        "",
        "The source-side formula and target parameters were frozen and hashed before",
        "this script opened the pointwise SPARC endpoint. UGC08490 had nevertheless",
        "been inspected in earlier, different tracer analyses, so this remains a",
        "retrospective transfer test.",
        "",
        "## Model scores",
        "",
        markdown_table(scores[[
            "model_id", "role", "valid_full_endpoint", "rmse_km_s", "bias_km_s",
            "chi2_per_point", "endpoint_fit_parameters", "imported_summary_scalars"
        ]]),
        "",
        "## Radial diagnosis",
        "",
        markdown_table(radial),
        "",
        "## Decisive checks",
        "",
        f"- frozen source-correct onset: `x_w={x_w:.6f}`;",
        f"- endpoint-informed preferred onset (diagnostic only): `x_w={float(preferred['x_w']):.6f}`;",
        f"- frozen transfer RMSE: `{float(primary_score['rmse_km_s']):.4f} km/s`;",
        f"- fixed MOND RMSE: `{float(mond_score['rmse_km_s']):.4f} km/s`;",
        f"- wrong NGC4088-onset control RMSE: `{float(wrong_x_score['rmse_km_s']):.4f} km/s`;",
        f"- best two-parameter halo-fit RMSE: `{float(summary['best_fit_halo_rmse_km_s']):.4f} km/s`;",
        f"- matched transfer beats fixed MOND: `{matched_beats_fixed_mond}`;",
        f"- matched transfer beats the wrong-onset control: `{matched_beats_wrong_onset}`.",
        "",
        "The block-bootstrap comparison is descriptive because radial points and the",
        "catalog `Vflat` input are not independent. Its role is robustness auditing,",
        "not a discovery p-value.",
        "",
        "## Interpretation",
        "",
        summary["interpretation"],
        "The failure mode is physically informative: the promoted warp begins only",
        "after the large inner baryonic discrepancy is already present. Therefore an",
        "outer-warp body can be a genuine morphology component without being the",
        "complete carrier of the galaxy's rotation discrepancy.",
        "",
        "No endpoint-informed repair is promoted. Any revised body/readout law must be",
        "derived and tested on a new target.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
