#!/usr/bin/env python3
"""Test a source-normalized, bounded composite scale-tail kernel candidate."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

import run_source_native_readout_formula_endpoint as source


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/theory_completed_scale_tail_kernel_v02.md"


def add_channel_shape(points: pd.DataFrame) -> pd.DataFrame:
    out = points.copy()
    out["kernel_tail_reference"] = 0.0
    for _, indices in out.groupby("galaxy").groups.items():
        row = out.loc[indices].iloc[0]
        reference = source.tail_i2_over_r(
            np.asarray([row.tail_cutoff_radius_proxy_kpc]),
            float(row.tail_inner_radius_proxy_kpc),
            float(row.tail_cutoff_radius_proxy_kpc),
        )[0]
        out.loc[indices, "kernel_tail_reference"] = max(float(reference), 1.0e-12)
    out["u_tail_source_normalized"] = (
        out.kernel_K_scale_tail_spiral / out.kernel_tail_reference
    ).clip(lower=0.0)
    out["phi_tail_bounded"] = (
        out.u_tail_source_normalized / (1.0 + out.u_tail_source_normalized)
    )
    x = out.r / out.scale_radius_proxy_kpc.clip(lower=1.0e-12)
    out["phi_tail_holographic"] = 1.0 - np.exp(-out.u_tail_source_normalized)
    out["phi_radial_bounded"] = x / (1.0 + x)
    out["phi_bilinear_bounded"] = out.phi_tail_bounded * out.phi_radial_bounded
    return out


def fit_eta(train: pd.DataFrame, feature: str) -> tuple[float, float]:
    def objective(eta: float) -> float:
        predicted_v2 = train.v_v6.pow(2) * np.exp(eta * train[feature])
        return float(np.mean((predicted_v2 - train.vobs.pow(2)) ** 2))

    result = minimize_scalar(objective, bounds=(-2.0, 2.0), method="bounded")
    if not result.success:
        raise RuntimeError(result.message)
    return float(result.x), float(result.fun)


def score(frame: pd.DataFrame, prediction: str) -> pd.DataFrame:
    rows = []
    for galaxy, sub in frame.groupby("galaxy"):
        def rmse(column: str) -> float:
            return float(np.sqrt(np.mean((sub[column] - sub.vobs) ** 2)))
        rows.append({
            "galaxy": galaxy, "split": sub.split.iloc[0], "n_points": len(sub),
            "rmse_kernel_v02": rmse(prediction), "rmse_tpg_v6": rmse("v_v6"),
            "rmse_mond": rmse("v_mond"),
        })
    out = pd.DataFrame(rows)
    out["v02_minus_tpg_v6"] = out.rmse_kernel_v02 - out.rmse_tpg_v6
    out["v02_minus_mond"] = out.rmse_kernel_v02 - out.rmse_mond
    return out


def summary(scores: pd.DataFrame) -> dict:
    return {
        "n_galaxies": len(scores), "n_points": int(scores.n_points.sum()),
        "mean_rmse_km_s": {
            "kernel_v02": float(scores.rmse_kernel_v02.mean()),
            "tpg_v6": float(scores.rmse_tpg_v6.mean()),
            "mond": float(scores.rmse_mond.mean()),
        },
        "win_fraction": {
            "tpg_v6": float((scores.v02_minus_tpg_v6 < 0).mean()),
            "mond": float((scores.v02_minus_mond < 0).mean()),
        },
        "mean_paired_delta_km_s": {
            "v02_minus_tpg_v6": float(scores.v02_minus_tpg_v6.mean()),
            "v02_minus_mond": float(scores.v02_minus_mond.mean()),
        },
    }


def external_score(eta: float, feature: str) -> pd.DataFrame:
    points = pd.read_csv(DATA / "little_things_prospective_kernel_scored_points_v01.csv")
    audit = pd.read_csv(DATA / "little_things_baryonic_vector_extraction_audit_v01.csv")
    allowed = set(audit.loc[audit.status.eq("pass"), "galaxy"])
    points = points[points.galaxy.isin(allowed) & points.prospective_name_freeze].copy()
    points = add_channel_shape(points)
    points["v_kernel_v02"] = points.v_tpg_v6 * np.exp(0.5 * eta * points[feature])
    points = points.rename(columns={"velocity_km_s": "vobs", "v_tpg_v6": "v_v6"})
    points["split"] = "external_opened_diagnostic"
    return score(points, "v_kernel_v02").merge(
        points[["galaxy", "inclination_deg"]].drop_duplicates(), on="galaxy"
    )


def main() -> None:
    points, _ = source.load_points()
    points = source.add_bridge_formula_kernels(points)
    scale_tail = add_channel_shape(points[points.formula_family.eq("K_scale_tail_spiral")].copy())
    candidates = [
        "phi_tail_bounded", "phi_tail_holographic", "phi_radial_bounded",
        "phi_bilinear_bounded",
    ]
    fits = [
        {"feature": feature, "eta": eta, "train_v2_mse": loss}
        for feature in candidates
        for eta, loss in [fit_eta(scale_tail[scale_tail.split.eq("train")], feature)]
    ]
    selected = min(fits, key=lambda row: row["train_v2_mse"])
    eta = selected["eta"]
    feature = selected["feature"]
    scale_tail["v_kernel_v02"] = scale_tail.v_v6 * np.exp(
        0.5 * eta * scale_tail[feature]
    )
    historical = score(scale_tail, "v_kernel_v02")
    external = external_score(eta, feature)
    historical.to_csv(DATA / "theory_completed_scale_tail_kernel_v02_historical_scores.csv", index=False)
    external.to_csv(DATA / "theory_completed_scale_tail_kernel_v02_external_scores.csv", index=False)
    holdout = historical[historical.split.eq("holdout")]
    external_primary = external[external.inclination_deg >= 40]
    result = {
        "schema": "theory_completed_scale_tail_kernel_v02",
        "status": "THEORY_MOTIVATED_KERNEL_CANDIDATE_HISTORICAL_HOLDOUT_AND_OPENED_EXTERNAL_DIAGNOSTIC",
        "formula": f"v_v02^2=v_tpg^2 exp(eta phi); selected feature={feature}",
        "theory_roles": {
            "K_tail": "morphology-hosted support",
            "source_normalization": "source-quotient-compatible dimensionless coordinate",
            "phi": "bounded channel completion",
            "radial_factor_candidate": "bounded observer-source radial activation",
            "bilinear_candidate": "leading body-channel mixed response; retained only if train-selected",
            "exponential": "positive multiplicative carrier composition",
        },
        "candidate_scan": fits, "selected_feature": feature,
        "eta": eta, "eta_units": "dimensionless",
        "eta_fit_scope": "historical SPARC train scale-tail family only",
        "historical_holdout": summary(holdout),
        "little_things_opened_external_diagnostic": summary(external_primary),
        "little_things_is_prospective_for_v02": False,
        "time_operator_identified": False, "quantum_operator_identified": False,
        "claim_boundary": (
            "theory-motivated composite-kernel candidate; LITTLE THINGS was already opened before v02, "
            "so its v02 result is diagnostic and cannot promote a prospective claim"
        ),
    }
    (DATA / "theory_completed_scale_tail_kernel_v02.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    h, e = result["historical_holdout"], result["little_things_opened_external_diagnostic"]
    REPORT.write_text(
        "# Theory-completed scale-tail kernel v02\n\n"
        f"Status: `{result['status']}`\n\n"
        "The candidate replaces the dimensionful additive tail with a source-normalized, "
        "bounded, multiplicative composite response:\n\n"
        "```text\n"
        "u=K_tail(R)/K_tail(R_cut)\nphi=u/(1+u)\n"
        "v_v02^2=v_TPG^2 exp(eta phi)\n"
        "```\n\n"
        f"Historical train selects `{feature}` and gives `eta={eta:.8g}`. On historical scale-tail "
        f"holdout it beats TPG/v6 in `{h['win_fraction']['tpg_v6']:.3f}` and MOND in "
        f"`{h['win_fraction']['mond']:.3f}` of galaxies. On the already opened LITTLE THINGS "
        f"primary lane the corresponding diagnostic fractions are `{e['win_fraction']['tpg_v6']:.3f}` "
        f"and `{e['win_fraction']['mond']:.3f}`.\n\n"
        "The external v02 result is not prospective because the sample was inspected before this "
        "kernel was defined. The formula does not identify physical time or quantum operators.\n",
        encoding="utf-8",
    )
    print(result["status"], eta)


if __name__ == "__main__":
    main()
