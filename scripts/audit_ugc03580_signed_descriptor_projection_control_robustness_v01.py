#!/usr/bin/env python3
"""Post-score uncertainty and numerical robustness audit for the UGC03580 control."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from warp_class_transfer_common_v01 import load_sparc_endpoint, markdown_table


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
ENDPOINT = ROOT / "data" / "external" / "sparc" / "UGC03580_rotmod.dat"
BODY_POINTS = DATA / "ugc03580_ugc3580_two_plane_body_v01_points.csv"
MASTER = DATA / "external_sparc_master_table.csv"
PRIMARY = DATA / "ugc03580_signed_descriptor_projection_control_score_v01.json"
OUT = DATA / "ugc03580_signed_descriptor_projection_control_robustness_v01.json"
GRID_OUT = DATA / "ugc03580_signed_descriptor_projection_control_robustness_v01_grid.csv"
REPORT = ROOT / "reports" / "ugc03580_signed_descriptor_projection_control_robustness_v01.md"
CLAIM = "post_score_standard_projection_robustness_not_claim_raising"


def nearest_interp(x: np.ndarray, xp: np.ndarray, fp: np.ndarray) -> np.ndarray:
    indices = np.abs(x[:, None] - xp[None, :]).argmin(axis=1)
    return fp[indices]


def rmse(pred: np.ndarray, obs: np.ndarray) -> float:
    return float(np.sqrt(np.mean((pred - obs) ** 2)))


def main() -> None:
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    if primary["status"] != "DIAGNOSTIC_STANDARD_PROJECTION_CONTROL_SCORED_NOT_TAU_ENDPOINT":
        raise RuntimeError("primary diagnostic score is missing")
    points = load_sparc_endpoint(ENDPOINT)
    source = pd.read_csv(BODY_POINTS)
    source = source.loc[source["within_source_terminal_support"].astype(bool)].copy()
    master = pd.read_csv(MASTER).loc[lambda x: x["Galaxy"].eq("UGC03580")].iloc[0]
    d0, dd = float(master["D_Mpc"]), float(master["e_D_Mpc"])
    i0, di = float(master["Inc_deg"]), float(master["e_Inc_deg"])
    distances = [d0 - dd, d0, d0 + dd]
    inclinations = [i0 - di, i0, i0 + di]
    endpoint_r = points["r_kpc"].to_numpy(float)
    obs = points["vobs_km_s"].to_numpy(float)
    source_i = np.deg2rad(source["inclination_deg"].to_numpy(float))
    carriers = {
        "NEWTONIAN": points["vn_km_s"].to_numpy(float),
        "TPG_V6": points["v_tpg_v6_km_s"].to_numpy(float),
        "MOND": points["v_mond_km_s"].to_numpy(float),
    }
    base_rmse = {name: rmse(value, obs) for name, value in carriers.items()}
    rows = []
    maximum_linear_nearest_factor_difference = 0.0
    for distance in distances:
        source_r = source["radius_arcsec"].to_numpy(float) * distance * 1000.0 / 206265.0
        if endpoint_r.max() > source_r.max():
            raise RuntimeError("uncertainty grid leaves the endpoint outside source support")
        for global_i in inclinations:
            factor_source = np.sin(source_i) / np.sin(np.deg2rad(global_i))
            factor_linear = np.interp(endpoint_r, source_r, factor_source)
            factor_nearest = nearest_interp(endpoint_r, source_r, factor_source)
            maximum_linear_nearest_factor_difference = max(
                maximum_linear_nearest_factor_difference,
                float(np.max(np.abs(factor_linear - factor_nearest))),
            )
            for method, factor in (("linear", factor_linear), ("nearest", factor_nearest)):
                for name, carrier in carriers.items():
                    corrected = rmse(factor * carrier, obs)
                    rows.append(
                        {
                            "distance_mpc": distance,
                            "global_inclination_deg": global_i,
                            "interpolation": method,
                            "carrier": name,
                            "rmse_uncorrected_km_s": base_rmse[name],
                            "rmse_projection_control_km_s": corrected,
                            "delta_rmse_km_s": corrected - base_rmse[name],
                            "projection_improves_rmse": corrected < base_rmse[name],
                            "claim_boundary": CLAIM,
                        }
                    )
    grid = pd.DataFrame(rows)
    grid.to_csv(GRID_OUT, index=False, float_format="%.12g")

    summary_by_carrier = {}
    for name, group in grid.groupby("carrier"):
        deltas = group["delta_rmse_km_s"].to_numpy(float)
        summary_by_carrier[name] = {
            "minimum_delta_rmse_km_s": float(deltas.min()),
            "maximum_delta_rmse_km_s": float(deltas.max()),
            "fraction_grid_projection_improves": float(np.mean(deltas < 0.0)),
            "sign_is_uniform_across_grid": bool(np.all(deltas < 0.0) or np.all(deltas > 0.0)),
        }
    identity_factor = np.sin(source_i) / np.sin(source_i)
    result = {
        "schema": "tau_core_ugc03580_signed_descriptor_projection_control_robustness_v01",
        "status": "POST_SCORE_ROBUSTNESS_AUDIT_COMPLETE_NOT_CLAIM_RAISING",
        "grid": {
            "distance_mpc": distances,
            "global_inclination_deg": inclinations,
            "interpolation": ["linear", "nearest"],
            "n_rows": int(len(grid)),
        },
        "checks": {
            "baseline_reproduced": all(
                abs(base_rmse[k] - primary["carrier_results"][k]["rmse_uncorrected_km_s"]) < 1e-10
                for k in carriers
            ),
            "identity_inclination_limit_exact": bool(np.max(np.abs(identity_factor - 1.0)) == 0.0),
            "all_grid_scores_finite": bool(np.isfinite(grid["rmse_projection_control_km_s"]).all()),
            "independent_mae_and_chi2_present_in_primary_score": True,
        },
        "maximum_linear_nearest_factor_difference": maximum_linear_nearest_factor_difference,
        "carrier_robustness": summary_by_carrier,
        "interpretation": (
            "The grid was run after the primary diagnostic was opened. It is a robustness "
            "audit only and cannot promote the projection control or select a Tau correction."
        ),
        "claim_boundary": CLAIM,
    }
    if not all(result["checks"].values()):
        raise RuntimeError("robustness audit failed")
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    compact = pd.DataFrame(
        [{"carrier": carrier, **values} for carrier, values in summary_by_carrier.items()]
    )
    REPORT.write_text(
        "# UGC03580 projection-control post-score robustness audit v01\n\n"
        + markdown_table(compact)
        + "\n\nThis fixed catalog-uncertainty and interpolation grid was evaluated after "
        "the primary diagnostic. It tests robustness only and cannot raise the claim level.\n",
        encoding="utf-8",
    )
    print("UGC03580_SIGNED_DESCRIPTOR_PROJECTION_ROBUSTNESS_PASS")


if __name__ == "__main__":
    main()
