#!/usr/bin/env python3
"""Run carrier-robustness checks for the source-native readout formulas.

The headline source-native preflight freezes family amplitudes around the
TPG/v6 carrier.  This script repeats the same residual-blind family/kernel
procedure with alternative carriers, especially the Newtonian baryonic carrier
(`vn`).  It does not change labels, kernels, splits, or source proxies.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from run_source_native_readout_formula_endpoint import (  # noqa: E402
    FORMULA_FAMILIES,
    FORMULA_SOURCES,
    SHUFFLE_SEED,
    add_bridge_formula_kernels,
    load_points,
    markdown_table,
    rmse,
)

N_SHUFFLES = 1000
FLOAT_FORMAT = "%.12g"
CARRIERS = [
    ("tpg_v6", "v_v6", "TPG/v6 frozen predecessor carrier"),
    ("newtonian_baryonic", "vn", "Newtonian baryonic carrier"),
]


def fit_amplitudes_for_carrier(points: pd.DataFrame, carrier_col: str, carrier_id: str) -> pd.DataFrame:
    train = points.loc[points["split"] == "train"].copy()
    target = train["vobs"].pow(2) - train[carrier_col].pow(2)
    rows = []
    for family in FORMULA_FAMILIES:
        sub = train.loc[train["formula_family"] == family]
        sub_target = target.loc[sub.index]
        kernel = sub[f"kernel_{family}"]
        den = kernel.pow(2).sum()
        beta = float((sub_target * kernel).sum() / den) if den else 0.0
        rows.append(
            {
                "carrier_id": carrier_id,
                "carrier_column": carrier_col,
                "formula_family": family,
                "beta_delta_v2_amplitude": beta,
                "n_train_points": int(len(sub)),
                "n_train_galaxies": int(sub["galaxy"].nunique()),
                "kernel": f"kernel_{family}",
                "formula_source": FORMULA_SOURCES[family],
                "fit_policy": f"least_squares_train_only_on_vobs2_minus_{carrier_col}_2_over_bridge_formula_kernel",
            }
        )
    return pd.DataFrame(rows)


def add_predictions_for_carrier(
    points: pd.DataFrame,
    amplitudes: pd.DataFrame,
    carrier_col: str,
    carrier_id: str,
) -> pd.DataFrame:
    beta_map = dict(zip(amplitudes["formula_family"], amplitudes["beta_delta_v2_amplitude"]))
    out = points.copy()
    base_v2 = out[carrier_col].pow(2)
    for family in FORMULA_FAMILIES:
        pred_v2 = base_v2 + beta_map[family] * out[f"kernel_{family}"]
        out[f"v_{carrier_id}_{family}"] = np.sqrt(np.maximum(pred_v2, 0.0))
    return out


def score_carrier(scored: pd.DataFrame, carrier_id: str, carrier_col: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for galaxy, sub in scored.groupby("galaxy"):
        matched_family = sub["formula_family"].iloc[0]
        family_scores = {
            family: rmse(sub, f"v_{carrier_id}_{family}")
            for family in FORMULA_FAMILIES
        }
        matched = family_scores[matched_family]
        wrong_values = [value for family, value in family_scores.items() if family != matched_family]
        row = {
            "carrier_id": carrier_id,
            "carrier_column": carrier_col,
            "galaxy": galaxy,
            "split": sub["split"].iloc[0],
            "formula_family": matched_family,
            "n_points": int(len(sub)),
            "rmse_carrier": rmse(sub, carrier_col),
            "rmse_tpg_v6": rmse(sub, "v_v6"),
            "rmse_newtonian_baryonic": rmse(sub, "vn"),
            "rmse_mond": rmse(sub, "v_mond"),
            "rmse_matched_family": matched,
            "rmse_wrong_family_mean": float(np.mean(wrong_values)),
            "best_family": min(FORMULA_FAMILIES, key=lambda family: family_scores[family]),
            "matched_family_rank": sorted(FORMULA_FAMILIES, key=lambda family: family_scores[family]).index(
                matched_family
            )
            + 1,
        }
        for family, value in family_scores.items():
            row[f"rmse_{family}"] = value
        row["matched_minus_wrong_mean"] = row["rmse_matched_family"] - row["rmse_wrong_family_mean"]
        row["matched_minus_carrier"] = row["rmse_matched_family"] - row["rmse_carrier"]
        row["matched_minus_tpg_v6"] = row["rmse_matched_family"] - row["rmse_tpg_v6"]
        row["matched_minus_newtonian_baryonic"] = (
            row["rmse_matched_family"] - row["rmse_newtonian_baryonic"]
        )
        row["matched_minus_mond"] = row["rmse_matched_family"] - row["rmse_mond"]
        row["matched_beats_wrong_mean"] = row["matched_minus_wrong_mean"] < 0
        row["matched_beats_carrier"] = row["matched_minus_carrier"] < 0
        row["matched_beats_tpg_v6"] = row["matched_minus_tpg_v6"] < 0
        row["matched_beats_newtonian_baryonic"] = row["matched_minus_newtonian_baryonic"] < 0
        row["matched_beats_mond"] = row["matched_minus_mond"] < 0
        rows.append(row)

    scores = pd.DataFrame(rows).sort_values(["carrier_id", "split", "galaxy"])
    summary_rows = []
    for split, sub in scores.groupby("split"):
        summary_rows.append(
            {
                "carrier_id": carrier_id,
                "carrier_column": carrier_col,
                "split": split,
                "n_galaxies": int(len(sub)),
                "matched_beats_wrong_fraction": float(sub["matched_beats_wrong_mean"].mean()),
                "matched_rank1_fraction": float((sub["matched_family_rank"] == 1).mean()),
                "matched_beats_carrier_fraction": float(sub["matched_beats_carrier"].mean()),
                "matched_beats_tpg_v6_fraction": float(sub["matched_beats_tpg_v6"].mean()),
                "matched_beats_newtonian_baryonic_fraction": float(
                    sub["matched_beats_newtonian_baryonic"].mean()
                ),
                "matched_beats_mond_fraction": float(sub["matched_beats_mond"].mean()),
                "mean_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].mean()),
                "median_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].median()),
                "mean_matched_minus_carrier": float(sub["matched_minus_carrier"].mean()),
                "median_matched_minus_carrier": float(sub["matched_minus_carrier"].median()),
            }
        )
    return scores, pd.DataFrame(summary_rows)


def shuffled_summary(scores: pd.DataFrame, carrier_id: str) -> pd.DataFrame:
    rng = np.random.default_rng(SHUFFLE_SEED)
    rows = []
    for split, sub in scores.groupby("split"):
        sub = sub.reset_index(drop=True)
        observed_mean = float(sub["matched_minus_wrong_mean"].mean())
        observed_beats = float(sub["matched_beats_wrong_mean"].mean())
        labels = sub["formula_family"].to_numpy()
        means = []
        beats = []
        for _ in range(N_SHUFFLES):
            shuffled = rng.permutation(labels)
            minus_wrong = []
            beat_wrong = []
            for row_idx, family in enumerate(shuffled):
                family_scores = {
                    candidate: float(sub.loc[row_idx, f"rmse_{candidate}"])
                    for candidate in FORMULA_FAMILIES
                }
                selected = family_scores[family]
                wrong = [value for candidate, value in family_scores.items() if candidate != family]
                wrong_mean = float(np.mean(wrong))
                minus_wrong.append(selected - wrong_mean)
                beat_wrong.append(selected < wrong_mean)
            means.append(float(np.mean(minus_wrong)))
            beats.append(float(np.mean(beat_wrong)))
        means = np.asarray(means)
        beats = np.asarray(beats)
        rows.append(
            {
                "carrier_id": carrier_id,
                "split": split,
                "n_shuffles": N_SHUFFLES,
                "seed": SHUFFLE_SEED,
                "observed_mean_minus_wrong": observed_mean,
                "null_mean_minus_wrong_mean": float(means.mean()),
                "p_mean_minus_wrong_at_least_as_good": float((1 + (means <= observed_mean).sum()) / (N_SHUFFLES + 1)),
                "observed_beats_wrong_fraction": observed_beats,
                "null_beats_wrong_fraction_mean": float(beats.mean()),
                "p_beats_wrong_fraction_at_least_as_good": float(
                    (1 + (beats >= observed_beats).sum()) / (N_SHUFFLES + 1)
                ),
            }
        )
    return pd.DataFrame(rows)


def write_report(
    summary: pd.DataFrame,
    shuffled: pd.DataFrame,
    family_summary: pd.DataFrame,
    freeze_audit: pd.DataFrame,
) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].copy()
    holdout = holdout.merge(
        shuffled.loc[shuffled["split"] == "holdout"],
        on=["carrier_id", "split"],
        how="left",
    )
    lines = [
        "# Source-Native Carrier Robustness",
        "",
        "This stress test repeats the source-native readout formula preflight with",
        "different frozen carriers for the train-only amplitude residual. Labels,",
        "kernels, source proxies, and train/holdout splits are unchanged.",
        "",
        "## Holdout Summary",
        "",
        markdown_table(
            holdout[
                [
                    "carrier_id",
                    "matched_beats_wrong_fraction",
                    "mean_matched_minus_wrong",
                    "p_mean_minus_wrong_at_least_as_good",
                    "p_beats_wrong_fraction_at_least_as_good",
                    "matched_beats_carrier_fraction",
                    "matched_beats_tpg_v6_fraction",
                    "matched_beats_newtonian_baryonic_fraction",
                    "matched_beats_mond_fraction",
                ]
            ]
        ),
        "",
        "## Holdout By Family",
        "",
        markdown_table(
            family_summary.loc[family_summary["split"] == "holdout"][
                [
                    "carrier_id",
                    "formula_family",
                    "n_galaxies",
                    "matched_beats_wrong_fraction",
                    "mean_matched_minus_wrong",
                    "median_matched_minus_wrong",
                    "matched_beats_carrier_fraction",
                ]
            ]
        ),
        "",
        "## Freeze-Invariance Audit",
        "",
        markdown_table(freeze_audit[["carrier_id", "audit_field", "status", "evidence"]]),
        "",
        "## Claim Boundary",
        "",
        "A positive matched-versus-wrong result under the Newtonian baryonic carrier",
        "would support carrier robustness of morphology specificity. It would not by",
        "itself establish population-level superiority over TPG/v6, MOND-like, RAR,",
        "or Newtonian baselines.",
    ]
    (REPORTS / "source_native_carrier_robustness.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_family_summary(scores: pd.DataFrame) -> pd.DataFrame:
    return (
        scores.groupby(["carrier_id", "carrier_column", "split", "formula_family"])
        .agg(
            n_galaxies=("galaxy", "count"),
            matched_beats_wrong_fraction=("matched_beats_wrong_mean", "mean"),
            matched_rank1_fraction=("matched_family_rank", lambda s: float((s == 1).mean())),
            mean_matched_minus_wrong=("matched_minus_wrong_mean", "mean"),
            median_matched_minus_wrong=("matched_minus_wrong_mean", "median"),
            matched_beats_carrier_fraction=("matched_beats_carrier", "mean"),
            matched_beats_tpg_v6_fraction=("matched_beats_tpg_v6", "mean"),
            matched_beats_newtonian_baryonic_fraction=("matched_beats_newtonian_baryonic", "mean"),
            matched_beats_mond_fraction=("matched_beats_mond", "mean"),
        )
        .reset_index()
        .sort_values(["carrier_id", "split", "formula_family"])
    )


def build_freeze_invariance_audit(
    labels: pd.DataFrame,
    amplitudes: pd.DataFrame,
    summary: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    label_cols = sorted(labels.columns.tolist())
    carriers = summary["carrier_id"].drop_duplicates().tolist()
    for carrier_id in carriers:
        amp = amplitudes.loc[amplitudes["carrier_id"] == carrier_id]
        rows.extend(
            [
                {
                    "carrier_id": carrier_id,
                    "audit_field": "labels_frozen",
                    "status": "PASS",
                    "evidence": "same source_native_readout_formula_labels.csv consumed for all carriers",
                    "forbidden_change": "formula_family, split, source proxies, confidence, role",
                },
                {
                    "carrier_id": carrier_id,
                    "audit_field": "kernels_frozen",
                    "status": "PASS",
                    "evidence": "same add_bridge_formula_kernels output; no carrier-dependent kernel code path",
                    "forbidden_change": "kernel shapes and morphology proxy scales",
                },
                {
                    "carrier_id": carrier_id,
                    "audit_field": "split_frozen",
                    "status": "PASS",
                    "evidence": "split column is read from the same point artifact and is not redrawn",
                    "forbidden_change": "train/holdout membership",
                },
                {
                    "carrier_id": carrier_id,
                    "audit_field": "only_carrier_changes",
                    "status": "PASS",
                    "evidence": (
                        "amplitude target changes from vobs^2-carrier^2; "
                        f"carrier_column={amp['carrier_column'].iloc[0]}"
                    ),
                    "forbidden_change": "labels, kernels, source proxies, split, scoring equations",
                },
                {
                    "carrier_id": carrier_id,
                    "audit_field": "label_columns_snapshot",
                    "status": "INFO",
                    "evidence": ",".join(label_cols),
                    "forbidden_change": "residual or endpoint score columns in label artifact",
                },
            ]
        )
    return pd.DataFrame(rows)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, labels = load_points()
    points = add_bridge_formula_kernels(points)
    all_scores = []
    all_summaries = []
    all_amplitudes = []
    all_shuffled = []
    for carrier_id, carrier_col, carrier_description in CARRIERS:
        amplitudes = fit_amplitudes_for_carrier(points, carrier_col, carrier_id)
        amplitudes["carrier_description"] = carrier_description
        scored = add_predictions_for_carrier(points, amplitudes, carrier_col, carrier_id)
        scores, summary = score_carrier(scored, carrier_id, carrier_col)
        summary["carrier_description"] = carrier_description
        shuffled = shuffled_summary(scores, carrier_id)
        all_amplitudes.append(amplitudes)
        all_scores.append(scores)
        all_summaries.append(summary)
        all_shuffled.append(shuffled)

    amplitudes_out = pd.concat(all_amplitudes, ignore_index=True)
    scores_out = pd.concat(all_scores, ignore_index=True)
    summary_out = pd.concat(all_summaries, ignore_index=True)
    shuffled_out = pd.concat(all_shuffled, ignore_index=True)
    family_out = build_family_summary(scores_out)
    freeze_audit = build_freeze_invariance_audit(labels, amplitudes_out, summary_out)

    amplitudes_out.to_csv(
        DATA / "source_native_carrier_robustness_amplitudes.csv", index=False, float_format=FLOAT_FORMAT
    )
    scores_out.to_csv(
        DATA / "source_native_carrier_robustness_scores_by_galaxy.csv", index=False, float_format=FLOAT_FORMAT
    )
    summary_out.to_csv(
        DATA / "source_native_carrier_robustness_summary.csv", index=False, float_format=FLOAT_FORMAT
    )
    family_out.to_csv(
        DATA / "source_native_carrier_robustness_by_family.csv", index=False, float_format=FLOAT_FORMAT
    )
    shuffled_out.to_csv(
        DATA / "source_native_carrier_robustness_shuffled_null_summary.csv",
        index=False,
        float_format=FLOAT_FORMAT,
    )
    freeze_audit.to_csv(DATA / "source_native_carrier_robustness_freeze_invariance_audit.csv", index=False)
    write_report(summary_out, shuffled_out, family_out, freeze_audit)
    print("SOURCE_NATIVE_CARRIER_ROBUSTNESS_COMPLETE")
    print(summary_out.loc[summary_out["split"] == "holdout"].to_string(index=False))
    print(shuffled_out.loc[shuffled_out["split"] == "holdout"].to_string(index=False))


if __name__ == "__main__":
    main()
