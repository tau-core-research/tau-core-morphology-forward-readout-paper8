#!/usr/bin/env python3
"""Analyze existing endpoint diagnostics by inclusion lane.

This script does not select a model and does not create a new endpoint.  It
joins pre-existing score tables to the strict/caution/acquisition lanes so that
the current inclusion policy can be audited without changing the claim boundary.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "inclusion_lane_endpoint_analysis_not_validation"


def load_lanes() -> pd.DataFrame:
    lanes = pd.read_csv(DATA / "inclusion_lane_expansion_audit.csv")
    lanes["lane_group"] = lanes["inclusion_lane"]
    return lanes[
        [
            "galaxy",
            "split",
            "formula_family",
            "inclusion_lane",
            "allowed_use",
            "strict_ready",
            "caution_ready",
            "acquisition_required",
            "minimal_acquisition_need",
        ]
    ]


def normalize_source_native() -> pd.DataFrame:
    df = pd.read_csv(DATA / "source_native_readout_formula_scores_by_galaxy.csv")
    return pd.DataFrame(
        {
            "galaxy": df["galaxy"],
            "split": df["split"],
            "score_layer": "source_native_hard_family",
            "score_role": "matched_vs_wrong_and_baselines",
            "rmse_prediction": df["rmse_matched_family"],
            "rmse_wrong_family_mean": df["rmse_wrong_family_mean"],
            "rmse_tpg_v6": df["rmse_tpg_v6"],
            "rmse_mond": df["rmse_mond"],
            "minus_wrong_mean": df["matched_minus_wrong_mean"],
            "minus_tpg_v6": df["matched_minus_tpg_v6"],
            "minus_mond": df["matched_minus_mond"],
            "beats_wrong_mean": df["matched_beats_wrong_mean"],
            "beats_tpg_v6": df["matched_beats_tpg_v6"],
            "beats_mond": df["matched_beats_mond"],
            "claim_boundary": "source_native_formula_endpoint_preflight_not_validation",
        }
    )


def normalize_tau_evidence() -> pd.DataFrame:
    df = pd.read_csv(DATA / "tau_side_evidence_measure_l2_endpoint_scores.csv")
    return pd.DataFrame(
        {
            "galaxy": df["galaxy"],
            "split": df["split"],
            "score_layer": "tau_side_evidence_measure_l2",
            "score_role": "source_normalized_l2_vs_baselines",
            "rmse_prediction": df["rmse_tau_source_normalized_l2"],
            "rmse_wrong_family_mean": float("nan"),
            "rmse_tpg_v6": df["rmse_tpg_v6"],
            "rmse_mond": df["rmse_mond"],
            "minus_wrong_mean": float("nan"),
            "minus_tpg_v6": df["source_norm_minus_tpg_v6"],
            "minus_mond": df["source_norm_minus_mond"],
            "beats_wrong_mean": float("nan"),
            "beats_tpg_v6": df["source_norm_beats_tpg_v6"],
            "beats_mond": df["source_norm_beats_mond"],
            "claim_boundary": "tau_side_evidence_measure_l2_endpoint_preflight_not_validation",
        }
    )


def normalize_information_gain() -> pd.DataFrame:
    df = pd.read_csv(DATA / "morphology_information_gain_scores_by_galaxy.csv")
    rows = []
    for _, row in df.iterrows():
        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "score_layer": row["information_level"],
                "score_role": row["level_name"],
                "rmse_prediction": row["rmse_level_prediction"],
                "rmse_wrong_family_mean": row["rmse_wrong_family_mean"],
                "rmse_tpg_v6": row["rmse_tpg_v6"],
                "rmse_mond": row["rmse_mond"],
                "minus_wrong_mean": row["level_minus_wrong_mean"],
                "minus_tpg_v6": row["level_minus_tpg_v6"],
                "minus_mond": row["level_minus_mond"],
                "beats_wrong_mean": row["level_beats_wrong_mean"],
                "beats_tpg_v6": row["level_beats_tpg_v6"],
                "beats_mond": row["level_beats_mond"],
                "claim_boundary": "morphology_information_gain_test_not_validation",
            }
        )
    return pd.DataFrame(rows)


def all_scores() -> pd.DataFrame:
    return pd.concat(
        [normalize_source_native(), normalize_tau_evidence(), normalize_information_gain()],
        ignore_index=True,
    )


def maybe_mean(series: pd.Series) -> float | pd.NA:
    valid = series.dropna()
    if len(valid) == 0:
        return pd.NA
    return float(valid.astype(float).mean())


def maybe_median(series: pd.Series) -> float | pd.NA:
    valid = pd.to_numeric(series, errors="coerce").dropna()
    if len(valid) == 0:
        return pd.NA
    return float(valid.median())


def summarize(joined: pd.DataFrame) -> pd.DataFrame:
    rows = []
    groups = []
    for (layer, split, lane), sub in joined.groupby(["score_layer", "split", "inclusion_lane"]):
        groups.append((layer, split, lane, sub))
    for (layer, split), sub in joined.loc[
        joined["strict_ready"] | joined["caution_ready"]
    ].groupby(["score_layer", "split"]):
        groups.append((layer, split, "STRICT_PLUS_CAUTION", sub))
    for (layer, split), sub in joined.groupby(["score_layer", "split"]):
        groups.append((layer, split, "ALL_ROWS", sub))

    for layer, split, lane, sub in groups:
        rows.append(
            {
                "score_layer": layer,
                "split": split,
                "inclusion_lane": lane,
                "n_galaxies": int(len(sub)),
                "median_rmse_prediction": maybe_median(sub["rmse_prediction"]),
                "median_minus_wrong_mean": maybe_median(sub["minus_wrong_mean"]),
                "median_minus_tpg_v6": maybe_median(sub["minus_tpg_v6"]),
                "median_minus_mond": maybe_median(sub["minus_mond"]),
                "beats_wrong_fraction": maybe_mean(sub["beats_wrong_mean"]),
                "beats_tpg_v6_fraction": maybe_mean(sub["beats_tpg_v6"]),
                "beats_mond_fraction": maybe_mean(sub["beats_mond"]),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows).sort_values(["score_layer", "split", "inclusion_lane"])


def summarize_allowed_use(joined: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (layer, split, inclusion_lane, allowed_use), sub in joined.groupby(
        ["score_layer", "split", "inclusion_lane", "allowed_use"]
    ):
        rows.append(
            {
                "score_layer": layer,
                "split": split,
                "inclusion_lane": inclusion_lane,
                "allowed_use": allowed_use,
                "n_galaxies": int(len(sub)),
                "median_rmse_prediction": maybe_median(sub["rmse_prediction"]),
                "median_minus_wrong_mean": maybe_median(sub["minus_wrong_mean"]),
                "median_minus_tpg_v6": maybe_median(sub["minus_tpg_v6"]),
                "median_minus_mond": maybe_median(sub["minus_mond"]),
                "beats_wrong_fraction": maybe_mean(sub["beats_wrong_mean"]),
                "beats_tpg_v6_fraction": maybe_mean(sub["beats_tpg_v6"]),
                "beats_mond_fraction": maybe_mean(sub["beats_mond"]),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["score_layer", "split", "inclusion_lane", "allowed_use"]
    )


def transitions(joined: pd.DataFrame) -> pd.DataFrame:
    info = joined.loc[joined["score_layer"].isin(["L0", "L1", "L2", "L3"])].copy()
    order = ["L0", "L1", "L2", "L3"]
    rows = []
    for split in sorted(info["split"].unique()):
        for lane_name, lane_filter in [
            ("STRICT_PLUS_CAUTION", info["strict_ready"] | info["caution_ready"]),
            ("ACQUISITION_REQUIRED", info["acquisition_required"]),
            ("ALL_ROWS", pd.Series(True, index=info.index)),
        ]:
            sub = info.loc[(info["split"] == split) & lane_filter]
            for prev, curr in zip(order, order[1:]):
                a = sub.loc[sub["score_layer"] == prev, ["galaxy", "rmse_prediction"]]
                b = sub.loc[sub["score_layer"] == curr, ["galaxy", "rmse_prediction"]]
                merged = a.merge(b, on="galaxy", suffixes=("_prev", "_curr"))
                delta = merged["rmse_prediction_curr"] - merged["rmse_prediction_prev"]
                rows.append(
                    {
                        "split": split,
                        "inclusion_lane": lane_name,
                        "transition": f"{prev}_to_{curr}",
                        "n_galaxies": int(len(merged)),
                        "median_delta_rmse_curr_minus_prev": float(delta.median())
                        if len(delta)
                        else pd.NA,
                        "improved_fraction": float((delta < 0).mean()) if len(delta) else pd.NA,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return pd.DataFrame(rows)


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


def write_report(
    summary: pd.DataFrame, allowed_use_summary: pd.DataFrame, transition_table: pd.DataFrame
) -> None:
    holdout = summary.loc[summary["split"] == "holdout"]
    focus = holdout.loc[
        (holdout["score_layer"] == "tau_side_evidence_measure_l2")
        & (holdout["inclusion_lane"] == "STRICT_PLUS_CAUTION")
    ].iloc[0]
    source_native = holdout.loc[
        (holdout["score_layer"] == "source_native_hard_family")
        & (holdout["inclusion_lane"] == "STRICT_PLUS_CAUTION")
    ].iloc[0]
    subgroup_focus = allowed_use_summary.loc[
        (allowed_use_summary["split"] == "holdout")
        & (allowed_use_summary["score_layer"] == "source_native_hard_family")
        & (allowed_use_summary["inclusion_lane"] == "CAUTION_READY_PROXY_SUPPORTED")
    ]
    tau_subgroup_focus = allowed_use_summary.loc[
        (allowed_use_summary["split"] == "holdout")
        & (allowed_use_summary["score_layer"] == "tau_side_evidence_measure_l2")
        & (allowed_use_summary["inclusion_lane"] == "CAUTION_READY_PROXY_SUPPORTED")
    ]
    lines = [
        "# Inclusion-Lane Endpoint Analysis",
        "",
        "This analysis slices existing score tables by the strict/caution/acquisition",
        "lanes. It does not select a new endpoint, does not tune a model, and does",
        "not turn caution rows into accepted evidence.",
        "",
        "## Holdout Strict+Caution Reading",
        "",
        f"- Tau evidence L2 rows: {int(focus['n_galaxies'])}",
        f"- Tau evidence L2 beats TPG/v6: {focus['beats_tpg_v6_fraction']:.3f}",
        f"- Tau evidence L2 beats MOND: {focus['beats_mond_fraction']:.3f}",
        f"- Tau evidence L2 median minus TPG/v6 RMSE: {focus['median_minus_tpg_v6']:.6g}",
        f"- Tau evidence L2 median minus MOND RMSE: {focus['median_minus_mond']:.6g}",
        f"- Source-native hard-family rows: {int(source_native['n_galaxies'])}",
        f"- Source-native hard-family beats wrong mean: {source_native['beats_wrong_fraction']:.3f}",
        f"- Source-native hard-family beats TPG/v6: {source_native['beats_tpg_v6_fraction']:.3f}",
        f"- Source-native hard-family beats MOND: {source_native['beats_mond_fraction']:.3f}",
        "",
        "The strict+caution lane increases usable holdout coverage to the",
        "orientation-ready rows, but remains a support lane. Baseline comparison",
        "numbers from this lane are diagnostic, not validation.",
        "",
        "## Caution Sub-Lanes",
        "",
        "The caution lane is not homogeneous. Projection-caveated and",
        "memory-history-proxy rows are reported separately so that weak baseline",
        "behavior is not hidden inside a single support bucket.",
        "",
        markdown_table(subgroup_focus),
        "",
        markdown_table(tau_subgroup_focus),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Allowed-Use Summary",
        "",
        markdown_table(allowed_use_summary),
        "",
        "## Information-Gain Transitions",
        "",
        markdown_table(transition_table),
        "",
        "## Claim Boundary",
        "",
        "The caution lane is not accepted evidence. Any positive or negative",
        "baseline comparison here is a preparation diagnostic for future",
        "residual-blind source acquisition and endpoint predeclaration.",
    ]
    (REPORTS / "inclusion_lane_endpoint_analysis.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    lanes = load_lanes()
    scores = all_scores()
    joined = scores.merge(lanes, on=["galaxy", "split"], how="left", validate="many_to_one")
    joined["claim_boundary"] = CLAIM_BOUNDARY
    summary = summarize(joined)
    transition_table = transitions(joined)
    joined.to_csv(DATA / "inclusion_lane_endpoint_scores.csv", index=False)
    summary.to_csv(DATA / "inclusion_lane_endpoint_summary.csv", index=False)
    allowed_use_summary = summarize_allowed_use(joined)
    allowed_use_summary.to_csv(
        DATA / "inclusion_lane_endpoint_allowed_use_summary.csv", index=False
    )
    transition_table.to_csv(DATA / "inclusion_lane_information_gain_transitions.csv", index=False)
    write_report(summary, allowed_use_summary, transition_table)
    print("PAPER8_INCLUSION_LANE_ENDPOINT_ANALYSIS_COMPLETE")


if __name__ == "__main__":
    main()
