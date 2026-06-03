#!/usr/bin/env python3
"""Run a residual-blind readout-mixture proxy diagnostic.

This is a preflight refinement of the single-family source-native bridge
formula endpoint.  It keeps the same concrete Tau Core bridge kernels, but
replaces the hard "one galaxy = one family" selection by a residual-blind
morphology-component mixture derived from the available morphology manifest.

The mixture weights are proxy weights, not accepted Tau-side readout states.
They use no endpoint residual gain, no required-S_tau diagnostic, and no
post-hoc best-family choice.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import run_source_native_readout_formula_endpoint as source_native


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

FORMULA_FAMILIES = source_native.FORMULA_FAMILIES


def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    clipped = {key: max(float(value), 0.0) for key, value in weights.items()}
    total = sum(clipped.values())
    if total <= 0.0:
        return {key: 1.0 / len(clipped) for key in clipped}
    return {key: value / total for key, value in clipped.items()}


def readout_weights(row: pd.Series) -> dict[str, float]:
    """Residual-blind proxy weights for readout mixture components."""
    weights = {family: 0.05 for family in FORMULA_FAMILIES}
    weights[str(row["formula_family"])] += 0.55

    mean_bulge = float(row["mean_bulge"])
    max_bulge = float(row["max_bulge"])
    mean_gas = float(row["mean_gas"])
    mean_log_sbdisk = float(row["mean_log_sbdisk"])
    inclination = float(row["inclination_deg"])
    thickness = float(row["thickness_h_over_rs_proxy"])
    type_bin = str(row["type_bin"])
    caveat = str(row["manifest_caveat"])

    compact_signal = min(0.35, 0.9 * mean_bulge + 0.35 * max_bulge)
    if type_bin == "early_T_le_2":
        compact_signal += 0.15
    weights["K_compact_finite"] += compact_signal

    tail_signal = 0.0
    if type_bin == "irregular_T_ge_9":
        tail_signal += 0.25
    tail_signal += min(0.25, 0.45 * mean_gas)
    if mean_log_sbdisk <= 0.9:
        tail_signal += 0.15
    weights["K_scale_tail_spiral"] += tail_signal

    exp_signal = 0.20 if type_bin == "late_T_6_8" else 0.0
    if mean_bulge < 0.05 and 0.10 <= mean_gas <= 0.35:
        exp_signal += 0.10
    weights["K_exponential_disk"] += exp_signal

    thick_signal = 0.0
    if thickness >= 0.20:
        thick_signal += min(0.25, thickness)
    if inclination >= 60.0:
        thick_signal += 0.10
    if "low_inclination" in caveat:
        thick_signal -= 0.05
    weights["K_thick_flared"] += thick_signal

    return normalize_weights(weights)


def build_weight_table(labels: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in labels.iterrows():
        weights = readout_weights(row)
        out = {
            "galaxy": row["galaxy"],
            "split": row["split"],
            "formula_family": row["formula_family"],
            "weight_source": "available_data_residual_blind_morphology_proxy",
            "claim_boundary": "readout_mixture_proxy_not_accepted_tau_side_state_not_endpoint",
        }
        for family in FORMULA_FAMILIES:
            out[f"w_{family}"] = weights[family]
        out["dominant_mixture_family"] = max(FORMULA_FAMILIES, key=lambda family: weights[family])
        out["hard_family_is_dominant"] = out["dominant_mixture_family"] == row["formula_family"]
        rows.append(out)
    return pd.DataFrame(rows).sort_values(["split", "galaxy"])


def add_mixture_predictions(points: pd.DataFrame, amplitudes: pd.DataFrame, weights: pd.DataFrame) -> pd.DataFrame:
    beta_map = dict(zip(amplitudes["formula_family"], amplitudes["beta_delta_v2_amplitude"]))
    weight_cols = ["galaxy"] + [f"w_{family}" for family in FORMULA_FAMILIES]
    out = points.merge(weights[weight_cols], on="galaxy", how="left", validate="many_to_one")
    if out[[f"w_{family}" for family in FORMULA_FAMILIES]].isna().any().any():
        raise RuntimeError("Missing readout mixture weights for scored points.")
    base_v2 = out["v_v6"].pow(2)
    delta_v2 = np.zeros(len(out), dtype=float)
    for family in FORMULA_FAMILIES:
        delta_v2 += (
            out[f"w_{family}"].to_numpy()
            * float(beta_map[family])
            * out[f"kernel_{family}"].to_numpy()
        )
    out["v_readout_mixture_proxy"] = np.sqrt(np.maximum(base_v2.to_numpy() + delta_v2, 0.0))
    return out


def rmse(df: pd.DataFrame, pred_col: str) -> float:
    return float(((df[pred_col] - df["vobs"]).pow(2).mean()) ** 0.5)


def score_galaxies(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for galaxy, sub in scored.groupby("galaxy"):
        matched_family = str(sub["formula_family"].iloc[0])
        row = {
            "galaxy": galaxy,
            "split": sub["split"].iloc[0],
            "formula_family": matched_family,
            "n_points": int(len(sub)),
            "rmse_mixture_proxy": rmse(sub, "v_readout_mixture_proxy"),
            "rmse_single_matched_family": rmse(sub, f"v_{matched_family}"),
            "rmse_tpg_v6": rmse(sub, "v_v6"),
            "rmse_mond": rmse(sub, "v_mond"),
        }
        row["mixture_minus_single_matched"] = (
            row["rmse_mixture_proxy"] - row["rmse_single_matched_family"]
        )
        row["mixture_minus_tpg_v6"] = row["rmse_mixture_proxy"] - row["rmse_tpg_v6"]
        row["mixture_minus_mond"] = row["rmse_mixture_proxy"] - row["rmse_mond"]
        row["mixture_beats_single_matched"] = row["mixture_minus_single_matched"] < 0
        row["mixture_beats_tpg_v6"] = row["mixture_minus_tpg_v6"] < 0
        row["mixture_beats_mond"] = row["mixture_minus_mond"] < 0
        rows.append(row)
    scores = pd.DataFrame(rows).sort_values(["split", "galaxy"])
    summary_rows = []
    for split, sub in scores.groupby("split"):
        summary_rows.append(
            {
                "split": split,
                "n_galaxies": int(len(sub)),
                "mixture_beats_single_matched_fraction": float(
                    sub["mixture_beats_single_matched"].mean()
                ),
                "mixture_beats_tpg_v6_fraction": float(sub["mixture_beats_tpg_v6"].mean()),
                "mixture_beats_mond_fraction": float(sub["mixture_beats_mond"].mean()),
                "mean_mixture_minus_single_matched": float(
                    sub["mixture_minus_single_matched"].mean()
                ),
                "median_mixture_minus_single_matched": float(
                    sub["mixture_minus_single_matched"].median()
                ),
                "mean_mixture_minus_tpg_v6": float(sub["mixture_minus_tpg_v6"].mean()),
                "median_mixture_minus_tpg_v6": float(sub["mixture_minus_tpg_v6"].median()),
                "mean_mixture_minus_mond": float(sub["mixture_minus_mond"].mean()),
                "median_mixture_minus_mond": float(sub["mixture_minus_mond"].median()),
            }
        )
    return scores, pd.DataFrame(summary_rows)


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


def write_report(weights: pd.DataFrame, scores: pd.DataFrame, summary: pd.DataFrame) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    lines = [
        "# Readout-Mixture Proxy Endpoint",
        "",
        "This diagnostic keeps the same concrete bridge formula kernels as the",
        "source-native endpoint, but replaces hard morphology-family selection by",
        "a residual-blind proxy mixture over readout components. It is not an",
        "accepted Tau-side readout state and not a final endpoint.",
        "",
        "## Holdout Verdict",
        "",
        f"- Holdout galaxies: {int(holdout['n_galaxies'])}",
        f"- Mixture beats hard matched family: {holdout['mixture_beats_single_matched_fraction']:.3f}",
        f"- Mixture beats TPG/v6: {holdout['mixture_beats_tpg_v6_fraction']:.3f}",
        f"- Mixture beats MOND: {holdout['mixture_beats_mond_fraction']:.3f}",
        f"- Mean mixture-minus-hard-family RMSE: {holdout['mean_mixture_minus_single_matched']:.6g}",
        f"- Mean mixture-minus-TPG/v6 RMSE: {holdout['mean_mixture_minus_tpg_v6']:.6g}",
        f"- Mean mixture-minus-MOND RMSE: {holdout['mean_mixture_minus_mond']:.6g}",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Mixture Weight Counts",
        "",
        markdown_table(
            weights.groupby(["split", "dominant_mixture_family"])
            .size()
            .reset_index(name="n_galaxies")
        ),
        "",
        "## Claim Boundary",
        "",
        "This is not an accepted Tau-side readout state.",
        "The weights are available-data morphology proxies. They are not inferred",
        "from endpoint residuals, but they are also not accepted Tau-side readout",
        "states. A future run must replace them with residual-blind source-native",
        "readout-state or morphology-memory observables.",
    ]
    (REPORTS / "readout_mixture_proxy_endpoint.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, labels = source_native.load_points()
    points = source_native.add_bridge_formula_kernels(points)
    amplitudes = source_native.fit_amplitudes(points)
    single_scored = source_native.add_predictions(points, amplitudes)
    weights = build_weight_table(labels)
    scored = add_mixture_predictions(single_scored, amplitudes, weights)
    scores, summary = score_galaxies(scored)

    weights.to_csv(DATA / "readout_mixture_proxy_weights.csv", index=False)
    scores.to_csv(DATA / "readout_mixture_proxy_scores_by_galaxy.csv", index=False)
    summary.to_csv(DATA / "readout_mixture_proxy_endpoint_summary.csv", index=False)
    write_report(weights, scores, summary)
    print("PAPER8_READOUT_MIXTURE_PROXY_ENDPOINT_COMPLETE")


if __name__ == "__main__":
    main()
