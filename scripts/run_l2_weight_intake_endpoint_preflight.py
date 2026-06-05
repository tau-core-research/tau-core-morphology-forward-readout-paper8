#!/usr/bin/env python3
"""Score the residual-blind L2 weight-intake candidates as an endpoint preflight.

This is a stress test of the source-derived candidate weights produced by
``build_l2_weight_intake_candidates.py``.  It does not promote those weights to
accepted Tau-side readout states.  It only asks whether the source-intake layer
is already useful relative to the older coarse mixture proxy and standard
baselines.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import run_source_native_readout_formula_endpoint as source_native


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FAMILIES = source_native.FORMULA_FAMILIES
CLAIM_BOUNDARY = "l2_weight_intake_endpoint_preflight_not_validation"


def load_weights() -> pd.DataFrame:
    path = DATA / "morphology_information_gain_l2_weight_intake_candidates.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} is missing; run scripts/build_l2_weight_intake_candidates.py first"
        )
    weights = pd.read_csv(path)
    weight_cols = [f"w_{family}" for family in FAMILIES]
    if not weights[weight_cols].sum(axis=1).round(12).eq(1.0).all():
        raise RuntimeError("L2 intake weights must sum to one per galaxy.")
    if weights["uses_endpoint_residuals"].astype(bool).any():
        raise RuntimeError("L2 intake weights must remain residual-blind.")
    return weights


def add_intake_predictions(
    points: pd.DataFrame, amplitudes: pd.DataFrame, weights: pd.DataFrame
) -> pd.DataFrame:
    beta_map = dict(zip(amplitudes["formula_family"], amplitudes["beta_delta_v2_amplitude"]))
    out = points.merge(
        weights[
            ["galaxy", "dominant_intake_family", "weight_intake_status"]
            + [f"w_{family}" for family in FAMILIES]
        ],
        on="galaxy",
        how="left",
        validate="many_to_one",
    )
    if out[[f"w_{family}" for family in FAMILIES]].isna().any().any():
        raise RuntimeError("Missing L2 intake weights for scored points.")

    base_v2 = out["v_v6"].pow(2)
    delta_v2 = np.zeros(len(out), dtype=float)
    for family in FAMILIES:
        delta_v2 += (
            out[f"w_{family}"].to_numpy()
            * float(beta_map[family])
            * out[f"kernel_{family}"].to_numpy()
        )
    out["v_l2_weight_intake_preflight"] = np.sqrt(np.maximum(base_v2.to_numpy() + delta_v2, 0.0))
    return out


def rmse(df: pd.DataFrame, pred_col: str) -> float:
    return float(((df[pred_col] - df["vobs"]).pow(2).mean()) ** 0.5)


def score_galaxies(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows = []
    for galaxy, sub in scored.groupby("galaxy"):
        matched_family = str(sub["formula_family"].iloc[0])
        row = {
            "galaxy": galaxy,
            "split": sub["split"].iloc[0],
            "coarse_formula_family": matched_family,
            "dominant_intake_family": sub["dominant_intake_family"].iloc[0],
            "weight_intake_status": sub["weight_intake_status"].iloc[0],
            "n_points": int(len(sub)),
            "rmse_l2_weight_intake": rmse(sub, "v_l2_weight_intake_preflight"),
            "rmse_single_matched_family": rmse(sub, f"v_{matched_family}"),
            "rmse_tpg_v6": rmse(sub, "v_v6"),
            "rmse_mond": rmse(sub, "v_mond"),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append(row)
    scores = pd.DataFrame(rows).sort_values(["split", "galaxy"])

    old_l2_path = DATA / "readout_mixture_proxy_scores_by_galaxy.csv"
    if old_l2_path.exists():
        old_l2 = pd.read_csv(old_l2_path)[["galaxy", "rmse_mixture_proxy"]]
        scores = scores.merge(old_l2, on="galaxy", how="left", validate="one_to_one")
    else:
        scores["rmse_mixture_proxy"] = np.nan

    scores["intake_minus_old_l2_proxy"] = (
        scores["rmse_l2_weight_intake"] - scores["rmse_mixture_proxy"]
    )
    scores["intake_minus_single_matched"] = (
        scores["rmse_l2_weight_intake"] - scores["rmse_single_matched_family"]
    )
    scores["intake_minus_tpg_v6"] = scores["rmse_l2_weight_intake"] - scores["rmse_tpg_v6"]
    scores["intake_minus_mond"] = scores["rmse_l2_weight_intake"] - scores["rmse_mond"]
    scores["intake_beats_old_l2_proxy"] = scores["intake_minus_old_l2_proxy"] < 0
    scores["intake_beats_single_matched"] = scores["intake_minus_single_matched"] < 0
    scores["intake_beats_tpg_v6"] = scores["intake_minus_tpg_v6"] < 0
    scores["intake_beats_mond"] = scores["intake_minus_mond"] < 0
    scores["dominant_intake_matches_coarse_family"] = (
        scores["dominant_intake_family"] == scores["coarse_formula_family"]
    )

    return scores, summarize(scores), compare_by_dominant_family(scores)


def summarize(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, sub in scores.groupby("split"):
        rows.append(
            {
                "split": split,
                "n_galaxies": int(len(sub)),
                "median_rmse_l2_weight_intake": float(sub["rmse_l2_weight_intake"].median()),
                "mean_rmse_l2_weight_intake": float(sub["rmse_l2_weight_intake"].mean()),
                "beats_old_l2_proxy_fraction": float(sub["intake_beats_old_l2_proxy"].mean()),
                "beats_single_matched_fraction": float(sub["intake_beats_single_matched"].mean()),
                "beats_tpg_v6_fraction": float(sub["intake_beats_tpg_v6"].mean()),
                "beats_mond_fraction": float(sub["intake_beats_mond"].mean()),
                "dominant_matches_coarse_family_fraction": float(
                    sub["dominant_intake_matches_coarse_family"].mean()
                ),
                "median_intake_minus_old_l2_proxy": float(
                    sub["intake_minus_old_l2_proxy"].median()
                ),
                "median_intake_minus_single_matched": float(
                    sub["intake_minus_single_matched"].median()
                ),
                "median_intake_minus_tpg_v6": float(sub["intake_minus_tpg_v6"].median()),
                "median_intake_minus_mond": float(sub["intake_minus_mond"].median()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows).sort_values("split")


def compare_by_dominant_family(scores: pd.DataFrame) -> pd.DataFrame:
    return (
        scores.groupby(["split", "dominant_intake_family"])
        .agg(
            n_galaxies=("galaxy", "count"),
            beats_old_l2_proxy_fraction=("intake_beats_old_l2_proxy", "mean"),
            beats_tpg_v6_fraction=("intake_beats_tpg_v6", "mean"),
            beats_mond_fraction=("intake_beats_mond", "mean"),
            median_intake_minus_old_l2_proxy=("intake_minus_old_l2_proxy", "median"),
            median_intake_minus_tpg_v6=("intake_minus_tpg_v6", "median"),
            median_intake_minus_mond=("intake_minus_mond", "median"),
        )
        .reset_index()
    )


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: f"{value:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def write_report(scores: pd.DataFrame, summary: pd.DataFrame, by_family: pd.DataFrame) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    lines = [
        "# L2 Weight-Intake Endpoint Preflight",
        "",
        "This endpoint preflight scores the residual-blind L2 weight-intake",
        "candidates. It is not validation and does not promote accepted Tau-side",
        "readout-state weights. It asks whether the source-derived candidate",
        "weights already improve over the older coarse mixture proxy.",
        "",
        "## Holdout Verdict",
        "",
        f"- Holdout galaxies: {int(holdout['n_galaxies'])}",
        f"- Beats old L2 mixture proxy: {holdout['beats_old_l2_proxy_fraction']:.3f}",
        f"- Beats hard source-native matched family: {holdout['beats_single_matched_fraction']:.3f}",
        f"- Beats TPG/v6: {holdout['beats_tpg_v6_fraction']:.3f}",
        f"- Beats MOND: {holdout['beats_mond_fraction']:.3f}",
        f"- Median intake-minus-old-L2 RMSE: {holdout['median_intake_minus_old_l2_proxy']:.6g}",
        f"- Median intake-minus-MOND RMSE: {holdout['median_intake_minus_mond']:.6g}",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Dominant Intake Family Breakdown",
        "",
        markdown_table(by_family),
        "",
        "## Claim Boundary",
        "",
        "The weights were not selected from endpoint residuals. The endpoint score",
        "is a preflight stress test of the intake map, not an accepted readout",
        "state, not a baseline-superiority claim, and not a Tau Core validation.",
    ]
    (REPORTS / "morphology_information_gain_l2_weight_intake_endpoint_preflight.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, _ = source_native.load_points()
    points = source_native.add_bridge_formula_kernels(points)
    amplitudes = source_native.fit_amplitudes(points)
    single_scored = source_native.add_predictions(points, amplitudes)
    weights = load_weights()
    scored = add_intake_predictions(single_scored, amplitudes, weights)
    scores, summary, by_family = score_galaxies(scored)

    scores.to_csv(DATA / "morphology_information_gain_l2_weight_intake_endpoint_scores.csv", index=False)
    summary.to_csv(DATA / "morphology_information_gain_l2_weight_intake_endpoint_summary.csv", index=False)
    by_family.to_csv(DATA / "morphology_information_gain_l2_weight_intake_endpoint_by_family.csv", index=False)
    write_report(scores, summary, by_family)
    print("PAPER8_L2_WEIGHT_INTAKE_ENDPOINT_PREFLIGHT_COMPLETE")


if __name__ == "__main__":
    main()
