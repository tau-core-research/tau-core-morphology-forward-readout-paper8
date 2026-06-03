#!/usr/bin/env python3
"""Run a narrow P0 pilot on Codex/source-reviewed labels.

This pilot consumes only the four P0 Codex/source-reviewed audit labels. It is
not the frozen endpoint: the full accepted residual-blind observable manifest is
still blocked, and no discovery-style 175-galaxy endpoint is launched.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

PRIMARY_POLICY = "leave_one_galaxy_out_beta_all13"
CLAIM_BOUNDARY = "p0_codex_source_review_pilot_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    labels = pd.read_csv(DATA / "p0_codex_accepted_label_manifest.csv")
    expdisk = pd.read_csv(DATA / "exponential_disk_narrow_dry_run_scores_by_galaxy.csv")
    formula_shell = pd.read_csv(DATA / "morphology_formula_shell_proxy_scores_by_galaxy.csv")
    source_native = pd.read_csv(DATA / "source_native_readout_formula_scores_by_galaxy.csv")
    labels = labels[
        labels["accepted_label_status"] == "P0_CODEX_SOURCE_REVIEW_ACCEPTED_FOR_AUDIT"
    ].copy()
    if labels.empty:
        raise RuntimeError("No P0 Codex/source-reviewed labels available for pilot.")
    if not labels["accepted_formula_family"].eq("K_exponential_disk").all():
        raise RuntimeError("This pilot is currently defined only for P0 K_exponential_disk labels.")
    return labels, expdisk, formula_shell, source_native


def build_scores() -> pd.DataFrame:
    labels, expdisk, formula_shell, source_native = load_inputs()
    primary_rmse = f"rmse_tau_exp_disk_{PRIMARY_POLICY}"
    primary_tpg_delta = f"tau_exp_disk_{PRIMARY_POLICY}_minus_tpg_v6"
    primary_mond_delta = f"tau_exp_disk_{PRIMARY_POLICY}_minus_mond"
    primary_beats_tpg = f"tau_exp_disk_{PRIMARY_POLICY}_beats_tpg_v6"
    primary_beats_mond = f"tau_exp_disk_{PRIMARY_POLICY}_beats_mond"

    merged = labels.merge(
        expdisk[
            [
                "galaxy",
                "n_points",
                "narrow_dry_run_lane",
                "scale_radius_kpc",
                "rmse_tpg_v6",
                "rmse_mond",
                primary_rmse,
                primary_tpg_delta,
                primary_mond_delta,
                primary_beats_tpg,
                primary_beats_mond,
                "rmse_tau_exp_disk_pool_fit_beta_all13",
                "tau_exp_disk_pool_fit_beta_all13_minus_tpg_v6",
                "tau_exp_disk_pool_fit_beta_all13_minus_mond",
                "tau_exp_disk_pool_fit_beta_all13_beats_tpg_v6",
                "tau_exp_disk_pool_fit_beta_all13_beats_mond",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )
    missing = merged[primary_rmse].isna()
    if missing.any():
        missing_names = ", ".join(merged.loc[missing, "galaxy"].astype(str))
        raise RuntimeError(f"P0 galaxies missing from expdisk dry-run scores: {missing_names}")

    formula = formula_shell[
        [
            "galaxy",
            "rmse_matched_family",
            "rmse_wrong_family_mean",
            "matched_minus_wrong_mean",
            "matched_minus_tpg_v6",
            "matched_minus_mond",
            "matched_beats_wrong_mean",
            "matched_beats_tpg_v6",
            "matched_beats_mond",
            "best_family",
            "matched_family_rank",
        ]
    ].rename(
        columns={
            "rmse_matched_family": "formula_shell_rmse_matched_family",
            "rmse_wrong_family_mean": "formula_shell_rmse_wrong_family_mean",
            "matched_minus_wrong_mean": "formula_shell_matched_minus_wrong_mean",
            "matched_minus_tpg_v6": "formula_shell_matched_minus_tpg_v6",
            "matched_minus_mond": "formula_shell_matched_minus_mond",
            "matched_beats_wrong_mean": "formula_shell_matched_beats_wrong_mean",
            "matched_beats_tpg_v6": "formula_shell_matched_beats_tpg_v6",
            "matched_beats_mond": "formula_shell_matched_beats_mond",
            "best_family": "formula_shell_best_family",
            "matched_family_rank": "formula_shell_matched_family_rank",
        }
    )
    native = source_native[
        [
            "galaxy",
            "rmse_matched_family",
            "rmse_wrong_family_mean",
            "matched_minus_wrong_mean",
            "matched_minus_tpg_v6",
            "matched_minus_mond",
            "matched_beats_wrong_mean",
            "matched_beats_tpg_v6",
            "matched_beats_mond",
            "best_family",
            "matched_family_rank",
        ]
    ].rename(
        columns={
            "rmse_matched_family": "source_native_rmse_matched_family",
            "rmse_wrong_family_mean": "source_native_rmse_wrong_family_mean",
            "matched_minus_wrong_mean": "source_native_matched_minus_wrong_mean",
            "matched_minus_tpg_v6": "source_native_matched_minus_tpg_v6",
            "matched_minus_mond": "source_native_matched_minus_mond",
            "matched_beats_wrong_mean": "source_native_matched_beats_wrong_mean",
            "matched_beats_tpg_v6": "source_native_matched_beats_tpg_v6",
            "matched_beats_mond": "source_native_matched_beats_mond",
            "best_family": "source_native_best_family",
            "matched_family_rank": "source_native_matched_family_rank",
        }
    )
    merged = merged.merge(formula, on="galaxy", how="left", validate="one_to_one")
    merged = merged.merge(native, on="galaxy", how="left", validate="one_to_one")
    merged["primary_amplitude_policy"] = PRIMARY_POLICY
    merged["primary_tau_rmse"] = merged[primary_rmse]
    merged["primary_tau_minus_tpg_v6"] = merged[primary_tpg_delta]
    merged["primary_tau_minus_mond"] = merged[primary_mond_delta]
    merged["primary_tau_beats_tpg_v6"] = merged[primary_beats_tpg]
    merged["primary_tau_beats_mond"] = merged[primary_beats_mond]
    merged["endpoint_scores_computed"] = False
    merged["full_endpoint_manifest_row_created"] = False
    merged["claim_boundary"] = CLAIM_BOUNDARY
    return merged.sort_values("galaxy").reset_index(drop=True)


def build_summary(scores: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "pilot_decision": "P0_CODEX_SOURCE_REVIEW_PILOT_COMPLETE_NOT_ENDPOINT",
                "n_galaxies": len(scores),
                "primary_amplitude_policy": PRIMARY_POLICY,
                "primary_beats_tpg_v6_fraction": float(scores["primary_tau_beats_tpg_v6"].mean()),
                "primary_beats_mond_fraction": float(scores["primary_tau_beats_mond"].mean()),
                "primary_median_tau_minus_tpg_v6": float(
                    scores["primary_tau_minus_tpg_v6"].median()
                ),
                "primary_median_tau_minus_mond": float(
                    scores["primary_tau_minus_mond"].median()
                ),
                "formula_shell_beats_wrong_fraction": float(
                    scores["formula_shell_matched_beats_wrong_mean"].mean()
                ),
                "formula_shell_beats_tpg_v6_fraction": float(
                    scores["formula_shell_matched_beats_tpg_v6"].mean()
                ),
                "formula_shell_beats_mond_fraction": float(
                    scores["formula_shell_matched_beats_mond"].mean()
                ),
                "source_native_beats_wrong_fraction": float(
                    scores["source_native_matched_beats_wrong_mean"].mean()
                ),
                "source_native_beats_tpg_v6_fraction": float(
                    scores["source_native_matched_beats_tpg_v6"].mean()
                ),
                "source_native_beats_mond_fraction": float(
                    scores["source_native_matched_beats_mond"].mean()
                ),
                "full_endpoint_manifest_rows_created": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def write_report(scores: pd.DataFrame, summary: pd.DataFrame) -> None:
    row = summary.iloc[0]
    readout_proxy_path = DATA / "p0_readout_relevant_morphology_proxy_summary.csv"
    if readout_proxy_path.exists():
        readout_proxy = pd.read_csv(readout_proxy_path)
        readout_proxy_section = [
            "## Readout-Relevant Proxy Context",
            "",
            markdown_table(readout_proxy),
            "",
            "The pilot above intentionally tests the direct apparent 4D",
            "`K_exponential_disk` handle. The readout-relevant proxy layer records",
            "which rows should later receive projection, bar, or compact-core",
            "corrections before any stronger endpoint claim is attempted.",
            "",
        ]
    else:
        readout_proxy_section = []
    lines = [
        "# P0 Codex Source-Reviewed Pilot",
        "",
        "This pilot runs the four P0 Codex/source-reviewed audit labels through",
        "the already available exponential-disk and formula-shell score layers. It",
        "is intentionally narrow: it does not launch the frozen 175-galaxy endpoint",
        "and does not claim validation against MOND/RAR/TGP/Newtonian baselines.",
        "",
        "## Verdict",
        "",
        f"Pilot decision: `{row['pilot_decision']}`.",
        "",
        "Under the primary leave-one-galaxy-out all13 exponential-disk policy,",
        f"the P0 Tau readout beats TPG/v6 in {row['primary_beats_tpg_v6_fraction']:.3f}",
        f"of cases and beats MOND in {row['primary_beats_mond_fraction']:.3f} of cases.",
        "The formula-shell proxy slice is stronger against TPG/v6 on this P0 set,",
        "but MOND remains a hard baseline. This is a useful pilot signal, not an",
        "endpoint result.",
        "This is not an endpoint result.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        *readout_proxy_section,
        "## P0 Scores",
        "",
        markdown_table(
            scores[
                [
                    "galaxy",
                    "accepted_formula_family",
                    "review_confidence",
                    "manifest_caveat",
                    "narrow_dry_run_lane",
                    "rmse_tpg_v6",
                    "rmse_mond",
                    "primary_tau_rmse",
                    "primary_tau_minus_tpg_v6",
                    "primary_tau_minus_mond",
                    "primary_tau_beats_tpg_v6",
                    "primary_tau_beats_mond",
                    "formula_shell_matched_beats_wrong_mean",
                    "formula_shell_matched_beats_tpg_v6",
                    "formula_shell_matched_beats_mond",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This pilot consumes P0 source-reviewed labels only. It does not create full",
        "endpoint-manifest rows, does not run the frozen endpoint, and does not",
        "validate Tau Core. The frozen endpoint launch guard remains authoritative.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_codex_source_review_pilot.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    scores = build_scores()
    summary = build_summary(scores)
    scores.to_csv(DATA / "p0_codex_source_review_pilot_scores.csv", index=False)
    summary.to_csv(DATA / "p0_codex_source_review_pilot_summary.csv", index=False)
    write_report(scores, summary)
    print("PAPER8_P0_CODEX_SOURCE_REVIEW_PILOT_COMPLETE")


if __name__ == "__main__":
    main()
