#!/usr/bin/env python3
"""Fit and score the frozen local dimensionless body-kernel response."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import run_source_native_readout_formula_endpoint as source


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/local_kernel_invariant_response_score_v01.md"
FAMILIES = source.FORMULA_FAMILIES


def rmse(frame, prediction):
    return float(np.sqrt(np.mean((prediction - frame.vobs.to_numpy()) ** 2)))


def add_phi(points, family):
    values = np.zeros(len(points))
    for _, idx in points.groupby("galaxy").groups.items():
        sub = points.loc[idx].sort_values("r")
        kernel = sub[f"kernel_{family}"].to_numpy()
        radius = sub.r.to_numpy()
        r_s = float(sub.scale_radius_proxy_kpc.iloc[0])
        reference = float(np.interp(r_s, radius, kernel))
        floor = 1e-12 * max(float(np.max(np.abs(kernel))), 1.0)
        denom = max(abs(reference), floor)
        u = np.maximum(kernel / denom, 0.0)
        values[sub.index] = u / (1.0 + u)
    return values


def main() -> None:
    freeze = json.loads((DATA / "local_kernel_invariant_response_freeze_v01.json").read_text())
    assert freeze["uses_vobs_or_residual"] is False
    points, _ = source.load_points()
    points = source.add_bridge_formula_kernels(points).reset_index(drop=True)
    for family in FAMILIES:
        points[f"phi_{family}"] = add_phi(points, family)
    train = points[points.split.eq("train")]
    eta = {}
    fit_rows = []
    for family in FAMILIES:
        sub = train[train.formula_family.eq(family)]
        galaxy_scores = []
        for candidate in freeze["eta_grid"]:
            prediction = sub.vn.to_numpy() * np.exp(0.5 * candidate * sub[f"phi_{family}"].to_numpy())
            temp = sub[["galaxy", "vobs"]].copy()
            temp["sq"] = (prediction - temp.vobs.to_numpy()) ** 2
            score = float(np.mean(np.sqrt(temp.groupby("galaxy").sq.mean())))
            galaxy_scores.append({"eta": candidate, "galaxy_balanced_rmse": score})
        selected = min(galaxy_scores, key=lambda row: row["galaxy_balanced_rmse"])
        eta[family] = selected["eta"]
        fit_rows.append({"family": family, "selected_eta": selected["eta"], "grid": galaxy_scores})
    for family in FAMILIES:
        points[f"v_local_{family}"] = points.vn * np.exp(0.5 * eta[family] * points[f"phi_{family}"])
    rows = []
    for name, sub in points.groupby("galaxy"):
        matched_family = sub.formula_family.iloc[0]
        fs = {family: rmse(sub, sub[f"v_local_{family}"].to_numpy()) for family in FAMILIES}
        matched = fs[matched_family]
        wrong = np.mean([v for f, v in fs.items() if f != matched_family])
        base = {"newton": rmse(sub, sub.vn.to_numpy()), "tpg_v6": rmse(sub, sub.v_v6.to_numpy()), "mond": rmse(sub, sub.v_mond.to_numpy())}
        rows.append({
            "galaxy": name, "split": sub.split.iloc[0], "formula_family": matched_family,
            "n_points": len(sub), "rmse_matched": matched, "rmse_wrong_mean": wrong,
            **{f"rmse_{key}": value for key, value in base.items()},
            "matched_minus_wrong": matched-wrong,
            **{f"matched_minus_{key}": matched-value for key, value in base.items()},
            **{f"rmse_{family}": value for family, value in fs.items()},
        })
    scores = pd.DataFrame(rows).sort_values(["split", "galaxy"])
    holdout = scores[scores.split.eq("holdout")]
    def summarize(column):
        values = holdout[column]
        return {"win_fraction": float((values < 0).mean()), "mean_delta_km_s": float(values.mean())}
    result = {
        "schema": "tau-core.paper8.local-kernel-invariant-response-score.v01",
        "status": "LOCAL_DIMENSIONLESS_KERNEL_RESPONSE_HOLDOUT_SCORED",
        "selected_family_eta": fit_rows,
        "n_holdout_galaxies": len(holdout), "n_holdout_points": int(holdout.n_points.sum()),
        "matched_vs_wrong": summarize("matched_minus_wrong"),
        "matched_vs_newton": summarize("matched_minus_newton"),
        "matched_vs_tpg_v6": summarize("matched_minus_tpg_v6"),
        "matched_vs_mond": summarize("matched_minus_mond"),
        "channel_coordinates_used": [],
        "claim_boundary": (
            "retrospective fixed-form local invariant diagnostic; train-fitted family eta; "
            "not prospective, parent-derived, or physical validation"
        ),
    }
    (DATA / "local_kernel_invariant_response_score_v01.json").write_text(json.dumps(result, indent=2)+"\n")
    scores.to_csv(DATA / "local_kernel_invariant_response_scores_by_galaxy_v01.csv", index=False)
    REPORT.write_text(
        "# Local dimensionless body-kernel response score v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"On `{len(holdout)}` holdout galaxies the bounded local invariant response beats "
        f"wrong-family, Newton, TPG/v6, and MOND in "
        f"`{result['matched_vs_wrong']['win_fraction']:.3f}`, "
        f"`{result['matched_vs_newton']['win_fraction']:.3f}`, "
        f"`{result['matched_vs_tpg_v6']['win_fraction']:.3f}`, and "
        f"`{result['matched_vs_mond']['win_fraction']:.3f}`. Mean matched-minus-TPG and "
        f"MOND RMSE are `{result['matched_vs_tpg_v6']['mean_delta_km_s']:.3f}` and "
        f"`{result['matched_vs_mond']['mean_delta_km_s']:.3f} km/s`. No channel coordinate "
        "or TPG carrier enters the candidate.\n"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
