#!/usr/bin/env python3
"""Shared numerical utilities for frozen warp-class transfer endpoints."""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import least_squares


KPC_M = 3.0857e19
A0_M_S2 = 1.2e-10
ALPHA_V6 = 0.360
H0_KM_S_KPC = 0.070


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_sparc_endpoint(path: Path) -> pd.DataFrame:
    rows: list[dict[str, float]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        r, vobs, errv, vgas, vdisk, vbul, *_ = map(float, line.split()[:8])
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


def fit_halo(points: pd.DataFrame, family: str) -> tuple[np.ndarray, dict[str, float | bool]]:
    r = points["r_kpc"].to_numpy(dtype=float)
    vn2 = points["vn_km_s"].to_numpy(dtype=float) ** 2
    obs = points["vobs_km_s"].to_numpy(dtype=float)
    err = points["errv_km_s"].to_numpy(dtype=float)

    if family == "NFW":
        def pred(theta: np.ndarray) -> np.ndarray:
            return np.sqrt(vn2 + nfw_halo_v2(r, float(theta[0]), float(theta[1])))

        result = least_squares(
            lambda theta: (pred(theta) - obs) / err,
            x0=np.array([100.0, 10.0]),
            bounds=(np.array([5.0, 0.5]), np.array([300.0, 60.0])),
        )
        params: dict[str, float | bool] = {
            "v200_km_s": float(result.x[0]),
            "concentration": float(result.x[1]),
        }
    elif family == "PSEUDO_ISOTHERMAL":
        def pred(theta: np.ndarray) -> np.ndarray:
            return np.sqrt(vn2 + pseudo_iso_halo_v2(r, float(theta[0]), float(theta[1])))

        result = least_squares(
            lambda theta: (pred(theta) - obs) / err,
            x0=np.array([100.0, 1.5]),
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
    *,
    seed: int,
    n_bootstrap: int = 20000,
    block_length: int = 3,
) -> dict[str, float | int]:
    delta = primary_sq_error - comparator_sq_error
    n = len(delta)
    rng = np.random.default_rng(seed)
    means = np.empty(n_bootstrap, dtype=float)
    n_blocks = math.ceil(n / block_length)
    for draw in range(n_bootstrap):
        starts = rng.integers(0, n, size=n_blocks)
        idx = np.concatenate(
            [(np.arange(start, start + block_length) % n) for start in starts]
        )[:n]
        means[draw] = float(np.mean(delta[idx]))
    return {
        "observed_delta_mse_primary_minus_comparator": float(np.mean(delta)),
        "bootstrap_ci95_low": float(np.quantile(means, 0.025)),
        "bootstrap_ci95_high": float(np.quantile(means, 0.975)),
        "bootstrap_fraction_primary_better": float(np.mean(means < 0.0)),
        "n_bootstrap": n_bootstrap,
        "block_length": block_length,
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
