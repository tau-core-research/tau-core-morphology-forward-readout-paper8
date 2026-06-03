#!/usr/bin/env python3
"""Audit where baseline models succeed and what morphology proxies say.

This diagnostic asks a negative/control question for Paper 8:

If TPG/MOND/Newton/RAR already fit a galaxy well, what kind of structure does
that galaxy appear to have, and what Tau Core readout-state interpretation is
suggested?

The audit is descriptive.  It does not retune any model and does not claim that
Tau Core, TPG, MOND, RAR, or Newtonian baselines are validated.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "baseline_success_morphology_audit_not_endpoint_not_validation"


def tau_core_readout_interpretation(row: pd.Series) -> str:
    winner = str(row["winner_tau_tpg_mond"])
    family = str(row["formula_family"])
    memory_match = bool(row["matches_current_proxy_family"])
    flags = str(row["source_memory_proxy_flags"])
    type_bin = str(row["type_bin"])
    caveat = str(row["manifest_caveat"])

    if winner == "tau_matched" and memory_match:
        return "current_morphology_readout_regular_candidate"
    if winner == "tau_matched":
        return "tau_formula_specificity_with_possible_memory_caveat"
    if winner == "tpg_v6" and not memory_match:
        if family == "K_scale_tail_spiral" or type_bin == "irregular_T_ge_9":
            return "tpg_success_possible_smooth_tail_or_memory_integrated_readout"
        return "tpg_success_possible_closure_like_regularization_of_mismatched_proxy"
    if winner == "mond":
        if "low_surface_brightness_or_diffuse" in flags or type_bin in {"late_T_6_8", "irregular_T_ge_9"}:
            return "mond_success_possible_effective_radial_scaling_or_diffuse_disk_regime"
        return "mond_success_possible_simple_radial_low_acceleration_regime"
    if "low_inclination" in caveat:
        return "baseline_success_projection_caveat"
    return "baseline_success_unclassified_tau_readout_state"


def build_primary_audit() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    scores = pd.read_csv(DATA / "source_native_readout_formula_scores_by_galaxy.csv")
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    memory = pd.read_csv(DATA / "morphological_memory_history_proxy.csv")
    df = (
        scores.merge(manifest, on=["galaxy", "split", "formula_family"], how="left", validate="one_to_one")
        .merge(
            memory[
                [
                    "galaxy",
                    "rotation_inferred_family",
                    "rotation_inferred_confidence",
                    "matches_current_proxy_family",
                    "memory_history_proxy_class",
                    "source_memory_proxy_flags",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
    )
    df["winner_tau_tpg_mond"] = df[
        ["rmse_matched_family", "rmse_tpg_v6", "rmse_mond"]
    ].idxmin(axis=1).map(
        {
            "rmse_matched_family": "tau_matched",
            "rmse_tpg_v6": "tpg_v6",
            "rmse_mond": "mond",
        }
    )
    df["baseline_success_class"] = df.apply(tau_core_readout_interpretation, axis=1)
    df["claim_boundary"] = CLAIM_BOUNDARY

    summary = (
        df.groupby(["split", "winner_tau_tpg_mond"], as_index=False)
        .agg(
            n_galaxies=("galaxy", "count"),
            mean_manifest_confidence=("manifest_confidence", "mean"),
            mean_gas=("mean_gas", "mean"),
            mean_bulge=("mean_bulge", "mean"),
            mean_log_sbdisk=("mean_log_sbdisk", "mean"),
            mean_inclination_deg=("inclination_deg", "mean"),
            current_memory_match_fraction=("matches_current_proxy_family", "mean"),
            low_inclination_fraction=("manifest_caveat", lambda s: float(s.str.contains("low_inclination").mean())),
            large_distance_error_fraction=("manifest_caveat", lambda s: float(s.str.contains("large_distance_error").mean())),
        )
        .sort_values(["split", "winner_tau_tpg_mond"])
    )
    by_family = (
        df.groupby(["split", "formula_family", "winner_tau_tpg_mond"], as_index=False)
        .size()
        .rename(columns={"size": "n_galaxies"})
        .sort_values(["split", "formula_family", "winner_tau_tpg_mond"])
    )
    return df, summary, by_family


def build_conventional_baseline_audit(primary: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    wide_path = DATA / "available_data_wide_fixed_tpg_proxy_ranks.csv"
    paper1_path = DATA / "available_data_paper1_73_galaxy_baseline_pivot.csv"
    rows = []

    if wide_path.exists():
        wide = pd.read_csv(wide_path).rename(columns={"GalaxyName": "galaxy"})
        joined = wide.merge(
            primary[
                [
                    "galaxy",
                    "split",
                    "formula_family",
                    "type_bin",
                    "manifest_confidence",
                    "manifest_caveat",
                    "matches_current_proxy_family",
                    "memory_history_proxy_class",
                    "source_memory_proxy_flags",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        for _, row in joined.iterrows():
            rows.append(
                {
                    "audit_source": "wide_fixed_tpg_proxy_ranks",
                    "galaxy": row["galaxy"],
                    "available_best_model": row["best_model"],
                    "split": row.get("split"),
                    "formula_family": row.get("formula_family"),
                    "type_bin": row.get("type_bin"),
                    "manifest_confidence": row.get("manifest_confidence"),
                    "manifest_caveat": row.get("manifest_caveat"),
                    "matches_current_proxy_family": row.get("matches_current_proxy_family"),
                    "memory_history_proxy_class": row.get("memory_history_proxy_class"),
                    "source_memory_proxy_flags": row.get("source_memory_proxy_flags"),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    if paper1_path.exists():
        paper1 = pd.read_csv(paper1_path).rename(columns={"GalaxyName": "galaxy"})
        baseline_cols = ["mond_simple_mu", "newtonian_baryonic", "projection_fixed", "rar_mcgaugh"]
        paper1["available_best_model"] = paper1[baseline_cols].idxmin(axis=1)
        joined = paper1.merge(
            primary[
                [
                    "galaxy",
                    "split",
                    "formula_family",
                    "type_bin",
                    "manifest_confidence",
                    "manifest_caveat",
                    "matches_current_proxy_family",
                    "memory_history_proxy_class",
                    "source_memory_proxy_flags",
                ]
            ],
            on="galaxy",
            how="left",
            validate="one_to_one",
        )
        for _, row in joined.iterrows():
            rows.append(
                {
                    "audit_source": "paper1_73_baseline_pivot",
                    "galaxy": row["galaxy"],
                    "available_best_model": row["available_best_model"],
                    "split": row.get("split"),
                    "formula_family": row.get("formula_family"),
                    "type_bin": row.get("type_bin"),
                    "manifest_confidence": row.get("manifest_confidence"),
                    "manifest_caveat": row.get("manifest_caveat"),
                    "matches_current_proxy_family": row.get("matches_current_proxy_family"),
                    "memory_history_proxy_class": row.get("memory_history_proxy_class"),
                    "source_memory_proxy_flags": row.get("source_memory_proxy_flags"),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    audit = pd.DataFrame(rows)
    if audit.empty:
        return audit, pd.DataFrame()
    summary = (
        audit.groupby(["audit_source", "available_best_model"], as_index=False)
        .agg(
            n_galaxies=("galaxy", "count"),
            joined_to_primary_175=("formula_family", lambda s: int(s.notna().sum())),
            current_memory_match_fraction=("matches_current_proxy_family", "mean"),
        )
        .sort_values(["audit_source", "available_best_model"])
    )
    return audit, summary


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
    primary_summary: pd.DataFrame,
    primary_by_family: pd.DataFrame,
    conventional_summary: pd.DataFrame,
) -> None:
    holdout = primary_summary.loc[primary_summary["split"] == "holdout"]
    lines = [
        "# Baseline Success Morphology Audit",
        "",
        "This audit asks where TPG/MOND/Newton/RAR-style baselines succeed and",
        "what those success zones suggest in Tau Core morphology/readout language.",
        "It is descriptive only: no model is refit and no endpoint claim is made.",
        "",
        "## 175-Galaxy TPG/MOND/Tau Holdout Summary",
        "",
        markdown_table(holdout),
        "",
        "## 175-Galaxy Family x Winner Counts",
        "",
        markdown_table(primary_by_family.loc[primary_by_family["split"] == "holdout"]),
        "",
        "## Available Conventional Baseline Summary",
        "",
        markdown_table(conventional_summary) if not conventional_summary.empty else "No conventional baseline summary available.",
        "",
        "## Interpretation",
        "",
        "In the current holdout split, TPG/v6 success is concentrated in",
        "scale-tail/irregular rows with low current-vs-readout agreement. Tau Core",
        "language reads this as a possible smooth closure-like or memory-integrated",
        "readout regime rather than a direct present-day morphology match.",
        "",
        "MOND success is more compatible with simple radial/low-acceleration or",
        "diffuse-disk effective scaling regimes. Newtonian success, where visible",
        "in the smaller conventional tables, should be interpreted as a quiet or",
        "regular baryonic-readout regime, not as evidence against morphology",
        "specificity in other regimes.",
        "",
        "The next scientific step is to predeclare these success zones as controls:",
        "regular/current-readout-consistent galaxies should not require a strong",
        "Tau residual, while memory/projection/tail cases should be tested with",
        "source-native readout-state observables.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "baseline_success_morphology_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    primary, primary_summary, primary_by_family = build_primary_audit()
    conventional, conventional_summary = build_conventional_baseline_audit(primary)
    primary.to_csv(DATA / "baseline_success_morphology_audit.csv", index=False)
    primary_summary.to_csv(DATA / "baseline_success_morphology_summary.csv", index=False)
    primary_by_family.to_csv(DATA / "baseline_success_morphology_by_family.csv", index=False)
    conventional.to_csv(DATA / "baseline_success_conventional_available_audit.csv", index=False)
    conventional_summary.to_csv(
        DATA / "baseline_success_conventional_available_summary.csv", index=False
    )
    write_report(primary_summary, primary_by_family, conventional_summary)
    print("PAPER8_BASELINE_SUCCESS_MORPHOLOGY_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
