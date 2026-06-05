#!/usr/bin/env python3
"""Run the Paper 8 morphology-information-gain preflight.

This script does not fit a new morphology model. It assembles existing
residual-blind endpoint layers into a single information-level diagnostic:

L0 coarse K_obs shell proxy
L1 source-native formula shells
L2 readout-state vector proxy
L3 source-native formulas with train-selected normalization
L4 enriched velocity-field / HI / history data gate

The endpoint is a preparation diagnostic, not validation.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
EXTERNAL = ROOT / "data" / "external"
REPORTS = ROOT / "reports"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def normalize_common_scores(df: pd.DataFrame, level_id: str, level_name: str, score_source: str) -> pd.DataFrame:
    out = df.copy()
    out.insert(0, "information_level", level_id)
    out.insert(1, "level_name", level_name)
    out["score_source"] = score_source
    out["rmse_level_prediction"] = out["rmse_matched_family"]
    out["level_minus_wrong_mean"] = out["matched_minus_wrong_mean"]
    out["level_beats_wrong_mean"] = out["matched_beats_wrong_mean"]
    out["level_minus_tpg_v6"] = out["matched_minus_tpg_v6"]
    out["level_minus_mond"] = out["matched_minus_mond"]
    out["level_beats_tpg_v6"] = out["matched_beats_tpg_v6"]
    out["level_beats_mond"] = out["matched_beats_mond"]
    return out[
        [
            "information_level",
            "level_name",
            "score_source",
            "galaxy",
            "split",
            "formula_family",
            "n_points",
            "rmse_level_prediction",
            "rmse_wrong_family_mean",
            "rmse_tpg_v6",
            "rmse_mond",
            "matched_family_rank",
            "level_minus_wrong_mean",
            "level_beats_wrong_mean",
            "level_minus_tpg_v6",
            "level_minus_mond",
            "level_beats_tpg_v6",
            "level_beats_mond",
        ]
    ]


def normalize_mixture_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.insert(0, "information_level", "L2")
    out.insert(1, "level_name", "readout_state_vector_proxy")
    out["score_source"] = "readout_mixture_proxy_scores_by_galaxy.csv"
    out["rmse_level_prediction"] = out["rmse_mixture_proxy"]
    out["rmse_wrong_family_mean"] = np.nan
    out["matched_family_rank"] = np.nan
    out["level_minus_wrong_mean"] = np.nan
    out["level_beats_wrong_mean"] = np.nan
    out["level_minus_tpg_v6"] = out["mixture_minus_tpg_v6"]
    out["level_minus_mond"] = out["mixture_minus_mond"]
    out["level_beats_tpg_v6"] = out["mixture_beats_tpg_v6"]
    out["level_beats_mond"] = out["mixture_beats_mond"]
    return out[
        [
            "information_level",
            "level_name",
            "score_source",
            "galaxy",
            "split",
            "formula_family",
            "n_points",
            "rmse_level_prediction",
            "rmse_wrong_family_mean",
            "rmse_tpg_v6",
            "rmse_mond",
            "matched_family_rank",
            "level_minus_wrong_mean",
            "level_beats_wrong_mean",
            "level_minus_tpg_v6",
            "level_minus_mond",
            "level_beats_tpg_v6",
            "level_beats_mond",
        ]
    ]


def build_scores() -> pd.DataFrame:
    l0 = normalize_common_scores(
        read_csv(DATA / "morphology_formula_shell_proxy_scores_by_galaxy.csv"),
        "L0",
        "coarse_K_obs_formula_shell_proxy",
        "morphology_formula_shell_proxy_scores_by_galaxy.csv",
    )
    l1 = normalize_common_scores(
        read_csv(DATA / "source_native_readout_formula_scores_by_galaxy.csv"),
        "L1",
        "source_reviewed_K_readout_source_native_formulas",
        "source_native_readout_formula_scores_by_galaxy.csv",
    )
    l2 = normalize_mixture_scores(read_csv(DATA / "readout_mixture_proxy_scores_by_galaxy.csv"))

    shrink = read_csv(DATA / "amplitude_shrinkage_path_scores_by_galaxy.csv")
    l3_raw = shrink.loc[shrink["amplitude_path_id"] == "shrink_family_weight_0.40"].copy()
    l3 = normalize_common_scores(
        l3_raw,
        "L3",
        "source_native_scales_with_train_selected_normalization",
        "amplitude_shrinkage_path_scores_by_galaxy.csv:shrink_family_weight_0.40",
    )

    return pd.concat([l0, l1, l2, l3], ignore_index=True)


def summarize_scores(scores: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for (level, split), sub in scores.groupby(["information_level", "split"]):
        rows.append(
            {
                "information_level": level,
                "level_name": sub["level_name"].iloc[0],
                "split": split,
                "n_galaxies": int(sub["galaxy"].nunique()),
                "median_rmse_level_prediction": float(sub["rmse_level_prediction"].median()),
                "mean_rmse_level_prediction": float(sub["rmse_level_prediction"].mean()),
                "matched_beats_wrong_fraction": maybe_mean(sub["level_beats_wrong_mean"]),
                "matched_rank1_fraction": maybe_rank1(sub["matched_family_rank"]),
                "beats_tpg_v6_fraction": maybe_mean(sub["level_beats_tpg_v6"]),
                "beats_mond_fraction": maybe_mean(sub["level_beats_mond"]),
                "median_minus_wrong": maybe_median(sub["level_minus_wrong_mean"]),
                "median_minus_tpg_v6": maybe_median(sub["level_minus_tpg_v6"]),
                "median_minus_mond": maybe_median(sub["level_minus_mond"]),
                "claim_boundary": "information_gain_preflight_not_validation",
            }
        )
    summary = pd.DataFrame(rows).sort_values(["split", "information_level"])

    improvement_rows = []
    ordered = ["L0", "L1", "L2", "L3"]
    for split in sorted(scores["split"].unique()):
        split_scores = scores.loc[scores["split"] == split]
        for prev, curr in zip(ordered[:-1], ordered[1:]):
            a = split_scores.loc[split_scores["information_level"] == prev, ["galaxy", "rmse_level_prediction"]]
            b = split_scores.loc[split_scores["information_level"] == curr, ["galaxy", "rmse_level_prediction"]]
            joined = a.merge(b, on="galaxy", suffixes=("_prev", "_curr"))
            delta = joined["rmse_level_prediction_curr"] - joined["rmse_level_prediction_prev"]
            improvement_rows.append(
                {
                    "split": split,
                    "transition": f"{prev}_to_{curr}",
                    "n_common_galaxies": int(len(joined)),
                    "improvement_fraction": float((delta < 0).mean()) if len(joined) else pd.NA,
                    "median_delta_rmse_curr_minus_prev": float(delta.median()) if len(joined) else pd.NA,
                    "mean_delta_rmse_curr_minus_prev": float(delta.mean()) if len(joined) else pd.NA,
                    "interpretation": interpret_transition(prev, curr, delta),
                    "claim_boundary": "transition_diagnostic_not_monotonicity_proof",
                }
            )
    transitions = pd.DataFrame(improvement_rows)
    return summary, transitions


def maybe_mean(series: pd.Series):
    clean = series.dropna()
    if clean.empty:
        return pd.NA
    return float(clean.astype(bool).mean())


def maybe_rank1(series: pd.Series):
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return pd.NA
    return float((clean == 1).mean())


def maybe_median(series: pd.Series):
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return pd.NA
    return float(clean.median())


def interpret_transition(prev: str, curr: str, delta: pd.Series) -> str:
    if delta.empty:
        return "no_common_galaxies"
    frac = float((delta < 0).mean())
    median = float(delta.median())
    if frac >= 0.6 and median < 0:
        return f"{prev}->{curr}_supports_information_gain"
    if frac <= 0.45 and median > 0:
        return f"{prev}->{curr}_negative_or_overfit_proxy_warning"
    return f"{prev}->{curr}_mixed_information_gain_signal"


def build_level_manifest() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "information_level": "L0",
                "level_name": "coarse_K_obs_formula_shell_proxy",
                "input_layer": "coarse residual-blind metadata family label",
                "required_data": "SPARC metadata and available proxy morphology bins",
                "current_status": "RUNNABLE_PROXY",
                "main_output": "morphology_formula_shell_proxy_scores_by_galaxy.csv",
                "claim_boundary": "coarse_proxy_not_final_readout_state",
            },
            {
                "information_level": "L1",
                "level_name": "source_reviewed_K_readout_source_native_formulas",
                "input_layer": "source-native bridge kernels with proxy morphology parameters",
                "required_data": "SPARC radii plus proxy scale/tail/core/thickness parameters",
                "current_status": "RUNNABLE_PROXY_STRONG_SPECIFICITY",
                "main_output": "source_native_readout_formula_scores_by_galaxy.csv",
                "claim_boundary": "source_native_formula_shells_not_accepted_full_morphology",
            },
            {
                "information_level": "L2",
                "level_name": "readout_state_vector_proxy",
                "input_layer": "low-dimensional readout-state vector weights",
                "required_data": "accepted tail, compact, thickness, bar, memory, and regularity observables",
                "current_status": "RUNNABLE_PROXY_NEGATIVE_CURRENTLY",
                "main_output": "readout_mixture_proxy_scores_by_galaxy.csv",
                "claim_boundary": "mixture_weights_proxy_only_not_endpoint",
            },
            {
                "information_level": "L3",
                "level_name": "source_native_scales_with_train_selected_normalization",
                "input_layer": "source-native kernels plus train-selected normalization policy",
                "required_data": "accepted scale/amplitude normalizers and residual-blind closure/readout scale",
                "current_status": "RUNNABLE_PROXY_NORMALIZATION_GATE",
                "main_output": "amplitude_shrinkage_path_scores_by_galaxy.csv:shrink_family_weight_0.40",
                "claim_boundary": "train_selected_policy_not_tau_side_normalization_law",
            },
            {
                "information_level": "L4",
                "level_name": "velocity_field_HI_history_enriched",
                "input_layer": "enriched morphology/kinematic evidence",
                "required_data": "velocity fields, HI maps, decompositions, history indicators",
                "current_status": "BLOCKED_DATA_NOT_ASSEMBLED",
                "main_output": "none",
                "claim_boundary": "future_endpoint_only",
            },
        ]
    )


def build_data_acquisition_summary() -> pd.DataFrame:
    rows = []
    sparc = read_csv(DATA / "external_sparc_master_table.csv")
    rows.append(source_row("SPARC", "external_sparc_master_table.csv", len(sparc), "ACQUIRED_FULL_175"))

    s4g = read_csv(DATA / "external_s4g_sparc_observable_candidates.csv")
    rows.append(
        source_row(
            "S4G",
            "external_s4g_sparc_observable_candidates.csv",
            int((s4g["candidate_observable_status"] == "ACQUIRED_S4G_SPARC_DERIVED").sum()),
            "PARTIAL_SCALE_RADIUS_CANDIDATES",
        )
    )

    expansion_summary_path = DATA / "morphology_information_gain_source_expansion_summary.csv"
    if expansion_summary_path.exists():
        expansion_summary = read_csv(expansion_summary_path)
        source_counts = dict(
            zip(expansion_summary["coverage_field"], expansion_summary["n_galaxies"])
        )
        rows.append(
            source_row(
                "DustPedia",
                "morphology_information_gain_source_expansion.csv",
                int(source_counts.get("dustpedia_any_match", 0)),
                "FULL_SAMPLE_SOURCE_CANDIDATES",
            )
        )
        rows.append(
            source_row(
                "HI_surveys",
                "morphology_information_gain_source_expansion.csv",
                int(source_counts.get("sparc_hi_ready", 0)),
                "FULL_SAMPLE_SPARC_HI_READY",
            )
        )
        rows.append(
            source_row(
                "PHANGS",
                "morphology_information_gain_source_expansion.csv",
                int(source_counts.get("phangs_sample_match", 0)),
                "FULL_SAMPLE_PUBLIC_SAMPLE_MATCHES",
            )
        )
        rows.append(
            source_row(
                "L2_tail_candidates",
                "morphology_information_gain_source_expansion.csv",
                int(source_counts.get("q_tail_candidate", 0)),
                "SOURCE_CANDIDATE_NOT_ACCEPTED_WEIGHT",
            )
        )
        rows.append(
            source_row(
                "L2_compact_candidates",
                "morphology_information_gain_source_expansion.csv",
                int(source_counts.get("q_compact_candidate", 0)),
                "SOURCE_CANDIDATE_NOT_ACCEPTED_WEIGHT",
            )
        )
        rows.append(
            source_row(
                "L2_bar_candidates",
                "morphology_information_gain_source_expansion.csv",
                int(source_counts.get("q_bar_candidate", 0)),
                "SOURCE_CANDIDATE_NOT_ACCEPTED_WEIGHT",
            )
        )
        rows.append(
            source_row(
                "L4_velocity_field_candidates",
                "morphology_information_gain_source_expansion.csv",
                int(source_counts.get("l4_velocity_field_candidate", 0)),
                "BLOCKED_NO_MUSE_READY_MATCHES",
            )
        )
    else:
        rows.append(source_row("DustPedia", "p0_dustpedia_source_matches.csv", 0, "NOT_RUN_FULL_SAMPLE"))
        rows.append(source_row("HI_surveys", "p0_hi_source_evidence.csv", 0, "NOT_RUN_FULL_SAMPLE"))
        rows.append(source_row("PHANGS", "p0_phangs_source_matches.csv", 0, "NOT_RUN_FULL_SAMPLE"))

    vector_gap = read_csv(DATA / "readout_state_vector_gap_audit.csv")
    endpoint_ready = int(vector_gap["endpoint_ready_component"].astype(bool).sum())
    proxy_only = int(vector_gap["proxy_only_component"].astype(bool).sum())
    rows.append(
        {
            "source_family": "readout_state_vector_components",
            "local_artifact": "readout_state_vector_gap_audit.csv",
            "available_count": endpoint_ready,
            "status": "ENDPOINT_READY_COMPONENTS_MISSING",
            "notes": f"{proxy_only} proxy-only components; accepted L2 weights still blocked",
            "claim_boundary": "source_availability_not_endpoint_validation",
        }
    )
    return pd.DataFrame(rows)


def source_row(source: str, artifact: str, count: int, status: str) -> dict[str, object]:
    return {
        "source_family": source,
        "local_artifact": artifact,
        "available_count": count,
        "status": status,
        "notes": "residual-blind source layer; not a rotation endpoint score",
        "claim_boundary": "source_availability_not_endpoint_validation",
    }


def write_report(
    level_manifest: pd.DataFrame,
    summary: pd.DataFrame,
    transitions: pd.DataFrame,
    acquisition: pd.DataFrame,
) -> None:
    holdout_summary = summary.loc[summary["split"] == "holdout"].copy()
    holdout_transitions = transitions.loc[transitions["split"] == "holdout"].copy()
    lines = [
        "# Morphology Information Gain Test",
        "",
        "This report assembles existing residual-blind Paper 8 endpoint layers into",
        "a first information-gain diagnostic. It does not fit a new morphology",
        "model and it is not an empirical validation claim.",
        "",
        "## Information Levels",
        "",
        markdown_table(level_manifest),
        "",
        "## Holdout Summary",
        "",
        markdown_table(holdout_summary),
        "",
        "## Holdout Transition Diagnostics",
        "",
        markdown_table(holdout_transitions),
        "",
        "## Data Acquisition Status",
        "",
        markdown_table(acquisition),
        "",
        "## Current Verdict",
        "",
        "The available layers show a strong L0->L1 specificity gain when moving from",
        "naive formula shells to source-native bridge kernels. The current L2",
        "mixture/readout-state proxy is not yet an improvement, which supports the",
        "data-gate interpretation: mixture weights require accepted morphology-memory",
        "and source-native observables rather than coarse present-day proxies.",
        "",
        "## Claim Boundary",
        "",
        "This is a morphology-information-gain preflight. It is useful only if all",
        "information levels remain residual-blind. Any improvement caused by choosing",
        "labels, scales, weights, or gates from rotation residuals is forbidden.",
    ]
    (REPORTS / "morphology_information_gain_test.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda x: "" if pd.isna(x) else f"{x:.6g}")
        else:
            display[col] = display[col].map(lambda x: "" if pd.isna(x) else str(x))
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    level_manifest = build_level_manifest()
    scores = build_scores()
    summary, transitions = summarize_scores(scores)
    acquisition = build_data_acquisition_summary()

    level_manifest.to_csv(DATA / "morphology_information_gain_level_manifest.csv", index=False)
    scores.to_csv(DATA / "morphology_information_gain_scores_by_galaxy.csv", index=False)
    summary.to_csv(DATA / "morphology_information_gain_summary.csv", index=False)
    transitions.to_csv(DATA / "morphology_information_gain_transitions.csv", index=False)
    acquisition.to_csv(DATA / "morphology_information_gain_data_acquisition.csv", index=False)
    write_report(level_manifest, summary, transitions, acquisition)
    print("PAPER8_MORPHOLOGY_INFORMATION_GAIN_TEST_COMPLETE")


if __name__ == "__main__":
    main()
