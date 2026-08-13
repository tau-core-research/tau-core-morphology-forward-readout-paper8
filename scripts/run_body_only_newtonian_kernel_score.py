#!/usr/bin/env python3
"""Score frozen morphology kernels directly on the Newtonian dark discrepancy."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import run_source_native_readout_formula_endpoint as source


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/body_only_newtonian_kernel_score_v01.md"
SEED = 20260711
N_SHUFFLES = 10_000


def rmse(frame: pd.DataFrame, column: str) -> float:
    return float(np.sqrt(np.mean((frame[column] - frame.vobs) ** 2)))


def main() -> None:
    points, _ = source.load_points()
    points = source.add_bridge_formula_kernels(points)
    train = points[points.split.eq("train")].copy()
    target = train.vobs**2 - train.vn**2
    betas = {}
    beta_rows = []
    for family in source.FORMULA_FAMILIES:
        sub = train[train.formula_family.eq(family)]
        kernel = sub[f"kernel_{family}"]
        beta = float((target.loc[sub.index] * kernel).sum() / (kernel**2).sum())
        betas[family] = beta
        beta_rows.append({
            "formula_family": family,
            "beta_newtonian_delta_v2": beta,
            "n_train_galaxies": int(sub.galaxy.nunique()),
            "n_train_points": len(sub),
        })
    scored = points.copy()
    for family in source.FORMULA_FAMILIES:
        pred_v2 = scored.vn**2 + betas[family] * scored[f"kernel_{family}"]
        scored[f"v_body_{family}"] = np.sqrt(np.maximum(pred_v2, 0.0))

    rows = []
    for galaxy, sub in scored.groupby("galaxy"):
        matched_family = sub.formula_family.iloc[0]
        family_scores = {
            family: rmse(sub, f"v_body_{family}") for family in source.FORMULA_FAMILIES
        }
        matched = family_scores[matched_family]
        wrong = np.mean([v for f, v in family_scores.items() if f != matched_family])
        row = {
            "galaxy": galaxy,
            "split": sub.split.iloc[0],
            "formula_family": matched_family,
            "n_points": len(sub),
            "rmse_body_matched": matched,
            "rmse_body_wrong_mean": float(wrong),
            "rmse_newton": rmse(sub, "vn"),
            "rmse_tpg_v6": rmse(sub, "v_v6"),
            "rmse_mond": rmse(sub, "v_mond"),
            "matched_minus_wrong": float(matched - wrong),
            "matched_minus_newton": float(matched - rmse(sub, "vn")),
            "matched_minus_tpg_v6": float(matched - rmse(sub, "v_v6")),
            "matched_minus_mond": float(matched - rmse(sub, "v_mond")),
        }
        row.update({f"rmse_body_{family}": value for family, value in family_scores.items()})
        rows.append(row)
    scores = pd.DataFrame(rows).sort_values(["split", "galaxy"])
    holdout = scores[scores.split.eq("holdout")].copy()

    rng = np.random.default_rng(SEED)
    observed_fraction = float((holdout.matched_minus_wrong < 0).mean())
    observed_mean = float(holdout.matched_minus_wrong.mean())
    null_fraction = np.empty(N_SHUFFLES)
    null_mean = np.empty(N_SHUFFLES)
    labels = holdout.formula_family.to_numpy()
    for i in range(N_SHUFFLES):
        shuffled = rng.permutation(labels)
        deltas = []
        for (_, row), label in zip(holdout.iterrows(), shuffled):
            values = {
                family: row[f"rmse_body_{family}"] for family in source.FORMULA_FAMILIES
            }
            selected = values[label]
            wrong = np.mean([v for f, v in values.items() if f != label])
            deltas.append(selected - wrong)
        null_fraction[i] = np.mean(np.asarray(deltas) < 0)
        null_mean[i] = np.mean(deltas)
    p_fraction = float((1 + np.sum(null_fraction >= observed_fraction)) / (N_SHUFFLES + 1))
    p_mean = float((1 + np.sum(null_mean <= observed_mean)) / (N_SHUFFLES + 1))

    def comparison(column: str) -> dict:
        delta = holdout[column].to_numpy()
        return {
            "win_fraction": float(np.mean(delta < 0)),
            "mean_delta_km_s": float(np.mean(delta)),
            "median_delta_km_s": float(np.median(delta)),
        }

    result = {
        "schema": "tau-core.paper8.body-only-newtonian-kernel-score.v01",
        "status": "BODY_ONLY_NEWTONIAN_KERNEL_HOLDOUT_SCORED",
        "model": "v_body^2 = max(v_Newton^2 + beta_family K_family(B), 0)",
        "fit_target": "train-only vobs^2-v_Newton^2",
        "nonconventional_channel_parameters": 0,
        "tpg_used_in_fit_or_prediction": False,
        "n_train_galaxies": int(train.galaxy.nunique()),
        "n_holdout_galaxies": len(holdout),
        "n_holdout_points": int(holdout.n_points.sum()),
        "family_amplitudes": beta_rows,
        "matched_vs_wrong": {
            "win_fraction": observed_fraction,
            "mean_delta_km_s": observed_mean,
            "shuffle_p_win_fraction": p_fraction,
            "shuffle_p_mean_delta": p_mean,
        },
        "matched_vs_newton": comparison("matched_minus_newton"),
        "matched_vs_tpg_v6": comparison("matched_minus_tpg_v6"),
        "matched_vs_mond": comparison("matched_minus_mond"),
        "claim_boundary": (
            "retrospective fixed-split body-only morphology-kernel test; family shapes and "
            "labels are source-side but amplitudes are train-fitted; not prospective, not "
            "a parent derivation, and not a dark-matter or Tau Core validation"
        ),
    }
    (DATA / "body_only_newtonian_kernel_score_v01.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    scores.to_csv(DATA / "body_only_newtonian_kernel_scores_by_galaxy_v01.csv", index=False)
    pd.DataFrame({"null_win_fraction": null_fraction, "null_mean_delta": null_mean}).to_csv(
        DATA / "body_only_newtonian_kernel_shuffle_v01.csv", index=False
    )
    REPORT.write_text(
        "# Body-only Newtonian morphology-kernel score v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The fixed holdout contains `{len(holdout)}` galaxies and "
        f"`{int(holdout.n_points.sum())}` rotation points. The matched body kernel beats "
        f"the wrong-family mean in `{observed_fraction:.3f}` of galaxies "
        f"(`p_fraction={p_fraction:.4f}`, `p_mean={p_mean:.4f}`). It beats Newton in "
        f"`{result['matched_vs_newton']['win_fraction']:.3f}`, TPG/v6 in "
        f"`{result['matched_vs_tpg_v6']['win_fraction']:.3f}`, and MOND in "
        f"`{result['matched_vs_mond']['win_fraction']:.3f}`. Mean paired RMSE deltas are "
        f"`{result['matched_vs_newton']['mean_delta_km_s']:.3f}`, "
        f"`{result['matched_vs_tpg_v6']['mean_delta_km_s']:.3f}`, and "
        f"`{result['matched_vs_mond']['mean_delta_km_s']:.3f} km/s`, respectively.\n\n"
        "No TPG, path, time, light-cone, or quantum coordinate enters the fitted model. "
        "This is a retrospective body-only discriminant, not a prospective endpoint or "
        "parent-theory derivation.\n"
    )
    print(result["status"])


if __name__ == "__main__":
    main()
