#!/usr/bin/env python3
"""Score the frozen Tau kernel on the new LITTLE THINGS external sample."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import run_source_native_readout_formula_endpoint as formula


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/little_things_prospective_kernel_score_v01.md"
A0 = 1.2e-10
KPC_M = 3.085677581491367e19


def rmse(frame: pd.DataFrame, column: str) -> float:
    return float(np.sqrt(np.mean((frame[column] - frame.velocity_km_s) ** 2)))


def summarize(scores: pd.DataFrame) -> dict:
    return {
        "n_galaxies": len(scores),
        "n_points": int(scores.n_points.sum()),
        "mean_rmse_km_s": {
            "tau_matched": float(scores.rmse_tau_matched.mean()),
            "wrong_family_mean": float(scores.rmse_wrong_family_mean.mean()),
            "tpg_v6": float(scores.rmse_tpg_v6.mean()),
            "mond": float(scores.rmse_mond.mean()),
            "newton": float(scores.rmse_newton.mean()),
        },
        "win_fraction": {
            "wrong_family_mean": float(scores.matched_beats_wrong.mean()),
            "best_wrong_family": float(scores.matched_beats_best_wrong.mean()),
            "tpg_v6": float(scores.matched_beats_tpg.mean()),
            "mond": float(scores.matched_beats_mond.mean()),
            "newton": float(scores.matched_beats_newton.mean()),
        },
        "mean_paired_rmse_delta_km_s": {
            "matched_minus_wrong": float(scores.matched_minus_wrong.mean()),
            "matched_minus_best_wrong": float(scores.matched_minus_best_wrong.mean()),
            "matched_minus_tpg_v6": float(scores.matched_minus_tpg_v6.mean()),
            "matched_minus_mond": float(scores.matched_minus_mond.mean()),
            "matched_minus_newton": float(scores.matched_minus_newton.mean()),
        },
    }


def main() -> None:
    points = pd.read_csv(DATA / "little_things_baryonic_vector_components_v01.csv")
    audit = pd.read_csv(DATA / "little_things_baryonic_vector_extraction_audit_v01.csv")
    freeze = pd.read_csv(DATA / "little_things_prospective_scoring_freeze_v01.csv")
    allowed = set(audit.loc[audit.status.eq("pass"), "galaxy"])
    points = points[points.galaxy.isin(allowed)].merge(
        freeze[["galaxy", "prospective_name_freeze", "inclination_deg", "gas_mass_1e7_msun",
                "stellar_mass_kin_1e7_msun"]], on="galaxy", validate="many_to_one"
    )
    points = points[points.prospective_name_freeze].copy()
    stats = points.groupby("galaxy").radius_kpc.agg(["median", "max"]).rename(
        columns={"median": "r_median", "max": "r_max"}
    )
    points = points.merge(stats, on="galaxy")
    denom = points.gas_mass_1e7_msun + points.stellar_mass_kin_1e7_msun
    points["gas_fraction"] = (points.gas_mass_1e7_msun / denom).fillna(1.0).clip(0.0, 1.0)
    points["scale_radius_proxy_kpc"] = points.r_median / 1.678
    points["tail_inner_radius_proxy_kpc"] = points.r_median * 0.35
    points["tail_cutoff_radius_proxy_kpc"] = points.r_max * (1.0 + 0.5 * points.gas_fraction)
    points["compact_support_radius_proxy_kpc"] = points.r_median
    points["thickness_h_over_rs_proxy"] = (0.08 + 0.45 * points.gas_fraction).clip(0.05, 0.75)
    points = points.rename(columns={"radius_kpc": "r"})
    points = formula.add_bridge_formula_kernels(points)

    vn = points.v_baryon_newton_km_s.clip(lower=1.0e-6)
    acceleration = (vn * 1000.0) ** 2 / (points.r.clip(lower=1.0e-6) * KPC_M)
    points["v_newton"] = vn
    points["v_tpg_v6"] = vn * (1.0 + 0.360 * np.log1p(A0 / acceleration))
    points["v_mond"] = vn * np.sqrt((1.0 + np.sqrt(1.0 + 4.0 * A0 / acceleration)) / 2.0)
    amplitudes = pd.read_csv(DATA / "amplitude_shrinkage_path_amplitudes.csv")
    amplitudes = amplitudes[amplitudes.family_weight.eq(0.40)]
    beta = dict(zip(amplitudes.formula_family, amplitudes.beta_delta_v2_amplitude))
    for family in formula.FORMULA_FAMILIES:
        points[f"v_{family}"] = np.sqrt(np.maximum(
            points.v_tpg_v6 ** 2 + beta[family] * points[f"kernel_{family}"], 0.0
        ))

    rows = []
    for galaxy, sub in points.groupby("galaxy"):
        family_scores = {family: rmse(sub, f"v_{family}") for family in formula.FORMULA_FAMILIES}
        matched = family_scores["K_scale_tail_spiral"]
        wrong = np.mean([value for family, value in family_scores.items() if family != "K_scale_tail_spiral"])
        row = {
            "galaxy": galaxy, "inclination_deg": float(sub.inclination_deg.iloc[0]),
            "n_points": len(sub), "formula_family": "K_scale_tail_spiral",
            "rmse_tau_matched": matched, "rmse_wrong_family_mean": float(wrong),
            "rmse_tpg_v6": rmse(sub, "v_tpg_v6"), "rmse_mond": rmse(sub, "v_mond"),
            "rmse_newton": rmse(sub, "v_newton"),
        }
        row.update({f"rmse_{family}": value for family, value in family_scores.items()})
        best_wrong = min(value for family, value in family_scores.items() if family != "K_scale_tail_spiral")
        row["matched_minus_wrong"] = matched - wrong
        row["matched_minus_best_wrong"] = matched - best_wrong
        row["matched_beats_best_wrong"] = matched < best_wrong
        row["matched_family_rank"] = (
            sorted(formula.FORMULA_FAMILIES, key=lambda family: family_scores[family]).index(
                "K_scale_tail_spiral"
            ) + 1
        )
        for label, column in [("tpg_v6", "rmse_tpg_v6"), ("mond", "rmse_mond"), ("newton", "rmse_newton")]:
            row[f"matched_minus_{label}"] = matched - row[column]
            row[f"matched_beats_{'tpg' if label == 'tpg_v6' else label}"] = matched < row[column]
        row["matched_beats_wrong"] = matched < wrong
        rows.append(row)
    scores = pd.DataFrame(rows).sort_values("galaxy")
    scores.to_csv(DATA / "little_things_prospective_kernel_scores_by_galaxy_v01.csv", index=False)
    points.to_csv(DATA / "little_things_prospective_kernel_scored_points_v01.csv", index=False)
    primary = scores[scores.inclination_deg >= 40].copy()
    result = {
        "schema": "little_things_prospective_kernel_score_v01",
        "status": "PROSPECTIVE_EXTERNAL_SCORE_COMPLETE_CAVEATED_VECTOR_EXTRACTION",
        "sample": "Oh et al. 2015 LITTLE THINGS galaxies new by exact name versus historical SPARC-175",
        "formula_family": "K_scale_tail_spiral",
        "amplitude_policy": "frozen_train_selected_family_to_global_shrinkage_0_40_no_external_refit",
        "primary_quality_lane": "inclination_deg >= 40",
        "primary": summarize(primary), "all_extraction_pass": summarize(scores),
        "family_diversity": False,
        "primary_matched_family_rank1_fraction": float((primary.matched_family_rank == 1).mean()),
        "shuffled_family_null_available": False,
        "endpoint_access": True,
        "prospective_formula_retuning": False,
        "claim_boundary": (
            "external prospective score of one frozen kernel family with vector-extracted baryonic components; "
            "not a multi-family attribution test and not identification of a physical time or quantum operator"
        ),
    }
    (DATA / "little_things_prospective_kernel_score_v01.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    p = result["primary"]
    REPORT.write_text(
        "# LITTLE THINGS prospective Tau-kernel score v01\n\n"
        f"Status: `{result['status']}`\n\n"
        f"The primary inclination-qualified lane contains {p['n_galaxies']} previously unscored "
        f"galaxies and {p['n_points']} points. The frozen scale-tail kernel beats the wrong-family "
        f"mean in `{p['win_fraction']['wrong_family_mean']:.3f}`, the best wrong family in "
        f"`{p['win_fraction']['best_wrong_family']:.3f}`, TPG/v6 in "
        f"`{p['win_fraction']['tpg_v6']:.3f}`, MOND in `{p['win_fraction']['mond']:.3f}`, and "
        f"Newton in `{p['win_fraction']['newton']:.3f}` of galaxies.\n\n"
        "No external amplitude, sign, scale rule, or family label was fitted to these endpoints. "
        "The baryonic components were recovered from the authors' vector PDF figures, with "
        "published rotation points used only for axis calibration.\n\n"
        "All eligible objects share the source-frozen scale-tail family, so this is a one-family "
        "external transfer test, not a shuffled-label or multi-family attribution result. It does "
        "not by itself distinguish morphology, time, quantum, or other channel factors.\n",
        encoding="utf-8",
    )
    print(result["status"], p["n_galaxies"], p["n_points"])


if __name__ == "__main__":
    main()
