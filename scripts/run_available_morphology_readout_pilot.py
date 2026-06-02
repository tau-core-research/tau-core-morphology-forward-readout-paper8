#!/usr/bin/env python3
"""Run the currently available Paper 8 empirical-prep pilot.

This is not the final Paper 8 morphology-matched endpoint. It audits the data
that are already available locally and separates:

1. a 143-galaxy component-derived FixedTPG/Tau-like specificity stress table,
2. an older morphology-decomposition Tau proxy versus TPG/v6 runner,
3. a six-galaxy gallery with a combined RMOND/MOND comparator,
4. blocked status for the real morphology-family endpoint.

The script intentionally refuses to promote residual-inferred flags into
residual-blind morphology labels.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

ARCHIVE = Path(
    "/Users/jolcsak/Projects/"
    "sparc-taucore-residual-signal-paper3_archive_20260518_180830/"
    "untracked/studies/sparc_taucore_residual_signal_v01/packet_v01_seed"
)
TPG_RESULTS = Path("/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1")
TPG_FIGURES = Path("/Users/jolcsak/Projects/TPG/docs/figures/hdda_dtl_parent")


def rms(values: pd.Series) -> float:
    return float((values.pow(2).mean()) ** 0.5)


def load_wide_specificity() -> pd.DataFrame:
    path = ARCHIVE / "paper3_tau_signal_sparc_rotmod_wide_specificity_v02.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    needed = {
        "GalaxyName",
        "FixedTPGRMS",
        "RARRMS",
        "MONDRMS",
        "NewtonianRMS",
        "RotmodSpecificityFlagV02",
        "Guardrail",
    }
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"wide specificity missing columns: {sorted(missing)}")
    return df


def wide_specificity_outputs(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    models = ["FixedTPGRMS", "RARRMS", "MONDRMS", "NewtonianRMS"]
    long = df.melt(
        id_vars=["GalaxyName", "RotmodSpecificityFlagV02"],
        value_vars=models,
        var_name="model",
        value_name="rms_log10",
    )
    long["model"] = long["model"].str.replace("RMS", "", regex=False)
    long["is_v02_core_like"] = long["RotmodSpecificityFlagV02"].eq("v02_core_like")

    rows = []
    for group_name, group in long.groupby("is_v02_core_like"):
        label = "v02_core_like_proxy" if group_name else "not_v02_core_like"
        for model, sub in group.groupby("model"):
            rows.append(
                {
                    "sample": label,
                    "model": model,
                    "n_galaxies": int(sub["GalaxyName"].nunique()),
                    "mean_rms_log10": float(sub["rms_log10"].mean()),
                    "median_rms_log10": float(sub["rms_log10"].median()),
                    "pooled_rms_log10": rms(sub["rms_log10"]),
                }
            )
    summary = pd.DataFrame(rows).sort_values(["sample", "mean_rms_log10"])

    # Per-galaxy rank of FixedTPG against the available conventional baselines.
    rank_rows = []
    for _, row in df.iterrows():
        scores = {
            "FixedTPG": row["FixedTPGRMS"],
            "RAR": row["RARRMS"],
            "MOND": row["MONDRMS"],
            "Newtonian": row["NewtonianRMS"],
        }
        ordered = sorted(scores.items(), key=lambda item: item[1])
        rank_rows.append(
            {
                "GalaxyName": row["GalaxyName"],
                "RotmodSpecificityFlagV02": row["RotmodSpecificityFlagV02"],
                "FixedTPG_rank_1_best": [m for m, _ in ordered].index("FixedTPG") + 1,
                "best_model": ordered[0][0],
                "FixedTPG_minus_best_conventional": row["FixedTPGRMS"]
                - min(row["RARRMS"], row["MONDRMS"], row["NewtonianRMS"]),
                "FixedTPG_beats_RAR": bool(row["FixedTPGRMS"] < row["RARRMS"]),
                "FixedTPG_beats_MOND": bool(row["FixedTPGRMS"] < row["MONDRMS"]),
                "FixedTPG_beats_Newtonian": bool(row["FixedTPGRMS"] < row["NewtonianRMS"]),
            }
        )
    ranks = pd.DataFrame(rank_rows)

    rank_summary = (
        ranks.groupby("RotmodSpecificityFlagV02", dropna=False)
        .agg(
            n_galaxies=("GalaxyName", "count"),
            fixed_tpg_rank1_fraction=("FixedTPG_rank_1_best", lambda s: float((s == 1).mean())),
            fixed_tpg_beats_rar_fraction=("FixedTPG_beats_RAR", "mean"),
            fixed_tpg_beats_mond_fraction=("FixedTPG_beats_MOND", "mean"),
            fixed_tpg_beats_newtonian_fraction=("FixedTPG_beats_Newtonian", "mean"),
            median_fixed_minus_best_conventional=("FixedTPG_minus_best_conventional", "median"),
            mean_fixed_minus_best_conventional=("FixedTPG_minus_best_conventional", "mean"),
        )
        .reset_index()
        .sort_values("n_galaxies", ascending=False)
    )
    return summary, ranks, rank_summary


def morphology_decomposition_outputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    path = TPG_RESULTS / "tau_sparc_morphology_decomposition_control_runner_v0.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    holdout = df.loc[df["split"] == "holdout"].copy()
    holdout["tau_proxy_improves_over_tpg_v6"] = holdout["delta_tau_minus_v6"] < 0
    summary = (
        holdout.groupby(["ybulge", "group_key"])
        .agg(
            n_groups=("group", "count"),
            total_points=("n_points", "sum"),
            mean_delta_tau_minus_v6=("delta_tau_minus_v6", "mean"),
            median_delta_tau_minus_v6=("delta_tau_minus_v6", "median"),
            improvement_fraction=("tau_proxy_improves_over_tpg_v6", "mean"),
        )
        .reset_index()
        .sort_values(["ybulge", "group_key"])
    )
    return holdout, summary


def full_sparc_proxy_outputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    runner_path = TPG_RESULTS / "tau_rotation_curve_frozen_proxy_runner_v0_galaxies.csv"
    meta_path = TPG_RESULTS / "tau_rotation_curve_projection_metadata_control_v0.csv"
    if not runner_path.exists():
        raise FileNotFoundError(runner_path)
    if not meta_path.exists():
        raise FileNotFoundError(meta_path)

    runner = pd.read_csv(runner_path)
    meta = pd.read_csv(meta_path)[["galaxy", "type_bin", "inc_bin", "distance_quality"]]
    df = runner.merge(meta, on="galaxy", how="left")
    df["tau_proxy_beats_tpg_v6"] = df["rmse_tau_proxy"] < df["rmse_v6"]
    df["tau_proxy_beats_mond"] = df["rmse_tau_proxy"] < df["rmse_mond"]
    df["tpg_v6_beats_mond"] = df["rmse_v6"] < df["rmse_mond"]
    df["tau_minus_tpg_v6"] = df["rmse_tau_proxy"] - df["rmse_v6"]
    df["tau_minus_mond"] = df["rmse_tau_proxy"] - df["rmse_mond"]

    def summarize(group_cols: list[str]) -> pd.DataFrame:
        return (
            df.groupby(group_cols, dropna=False)
            .agg(
                n_galaxies=("galaxy", "count"),
                mean_tau_minus_tpg_v6=("tau_minus_tpg_v6", "mean"),
                median_tau_minus_tpg_v6=("tau_minus_tpg_v6", "median"),
                tau_beats_tpg_v6_fraction=("tau_proxy_beats_tpg_v6", "mean"),
                mean_tau_minus_mond=("tau_minus_mond", "mean"),
                median_tau_minus_mond=("tau_minus_mond", "median"),
                tau_beats_mond_fraction=("tau_proxy_beats_mond", "mean"),
                tpg_v6_beats_mond_fraction=("tpg_v6_beats_mond", "mean"),
                mean_rmse_tau_proxy=("rmse_tau_proxy", "mean"),
                mean_rmse_tpg_v6=("rmse_v6", "mean"),
                mean_rmse_mond=("rmse_mond", "mean"),
            )
            .reset_index()
        )

    overall = summarize(["split"])
    by_type = summarize(["split", "type_bin"])
    return df, overall, by_type


def paper1_baseline_outputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    path = Path(
        "/Users/jolcsak/Projects/sparc-residual-disturbance-paper1/"
        "studies/sparc_residual_coherence_test_v01/paper_packet_v06_distance_balanced/"
        "baseline_score_by_galaxy.csv"
    )
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    pivot = df.pivot_table(
        index=["GalaxyName", "Class", "NPoints"],
        columns="Score",
        values="RmsLog",
        aggfunc="first",
    ).reset_index()
    tau_scores = [c for c in pivot.columns if str(c).startswith("tau_core_s_")]
    baselines = ["projection_fixed", "newtonian_baryonic", "mond_simple_mu", "rar_mcgaugh"]
    rows = []
    for tau in tau_scores:
        for base in baselines:
            if tau not in pivot.columns or base not in pivot.columns:
                continue
            diff = pivot[tau] - pivot[base]
            rows.append(
                {
                    "tau_score": tau,
                    "baseline": base,
                    "n_galaxies": int(diff.notna().sum()),
                    "mean_tau_minus_baseline": float(diff.mean()),
                    "median_tau_minus_baseline": float(diff.median()),
                    "tau_beats_baseline_fraction": float((diff < 0).mean()),
                }
            )
    summary = pd.DataFrame(rows).sort_values(["tau_score", "baseline"])
    class_rows = []
    for cls, sub in pivot.groupby("Class", dropna=False):
        for tau in tau_scores:
            for base in baselines:
                if tau not in sub.columns or base not in sub.columns:
                    continue
                diff = sub[tau] - sub[base]
                class_rows.append(
                    {
                        "class": cls,
                        "tau_score": tau,
                        "baseline": base,
                        "n_galaxies": int(diff.notna().sum()),
                        "median_tau_minus_baseline": float(diff.median()),
                        "tau_beats_baseline_fraction": float((diff < 0).mean()),
                    }
                )
    class_summary = pd.DataFrame(class_rows).sort_values(["class", "tau_score", "baseline"])
    return pivot, summary, class_summary


def limited_rmond_gallery_output() -> pd.DataFrame:
    path = TPG_FIGURES / "fig5_sparc_rotation_gallery_summary.csv"
    if not path.exists():
        return pd.DataFrame(
            [
                {
                    "status": "BLOCKED",
                    "reason": "six-galaxy RMOND/MOND gallery summary not found",
                }
            ]
        )
    df = pd.read_csv(path)
    df["hdda_dtl_better_than_rmond_mond"] = (
        df["rmse_hdda_dtl_log_km_s"] < df["rmse_rmond_mond_km_s"]
    )
    df["hdda_dtl_better_than_newton"] = df["rmse_hdda_dtl_log_km_s"] < df["rmse_newton_km_s"]
    df["status"] = "LIMITED_GALLERY_ONLY"
    return df


def availability_rows() -> pd.DataFrame:
    rows = [
        {
            "layer": "real_paper8_morphology_family_endpoint",
            "status": "BLOCKED",
            "available_data": "morphology_family_registry only",
            "limitation": "no residual-blind galaxy->K manifest and no per-family delta_g^K scored table",
            "allowed_claim": "not runnable yet as the final Paper 8 endpoint",
        },
        {
            "layer": "wide_fixed_tpg_component_proxy",
            "status": "RUNNABLE_PROXY",
            "available_data": "paper3_tau_signal_sparc_rotmod_wide_specificity_v02.csv",
            "limitation": "uses FixedTPG/Tau-like specificity flag, not full Paper 8 morphology-family labels",
            "allowed_claim": "stress test of Tau-like proxy group versus Newton/MOND/RAR",
        },
        {
            "layer": "morphology_decomposition_tau_proxy_vs_tpg",
            "status": "RUNNABLE_PROXY",
            "available_data": "tau_sparc_morphology_decomposition_control_runner_v0.csv",
            "limitation": "compares Tau proxy to TPG/v6 only; no MOND/RAR/Newton columns",
            "allowed_claim": "morphology split sensitivity check against TPG/v6",
        },
        {
            "layer": "rmond_full_sample_comparator",
            "status": "BLOCKED",
            "available_data": "paper3_rmond_bridge_audit says no frozen V_RMOND(R)",
            "limitation": "RMOND is not a pointwise residual comparator in current packet",
            "allowed_claim": "RMOND cannot enter primary Paper 8 endpoint yet",
        },
        {
            "layer": "limited_rmond_mond_gallery",
            "status": "LIMITED_PROXY",
            "available_data": "six-galaxy gallery with rmse_rmond_mond_km_s",
            "limitation": "combined RMOND/MOND comparator, different metric units, not full SPARC endpoint",
            "allowed_claim": "illustrative sanity check only",
        },
    ]
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda x: f"{x:.6g}")
        else:
            display[col] = display[col].astype(str)
    headers = list(display.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def write_report(
    wide_summary: pd.DataFrame,
    rank_summary: pd.DataFrame,
    morph_summary: pd.DataFrame,
    rmond_gallery: pd.DataFrame,
    full_overall: pd.DataFrame,
    full_by_type: pd.DataFrame,
    paper1_summary: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)

    core = rank_summary.loc[rank_summary["RotmodSpecificityFlagV02"] == "v02_core_like"]
    if not core.empty:
        core_row = core.iloc[0].to_dict()
        core_text = (
            f"v02_core_like has n={int(core_row['n_galaxies'])}, "
            f"FixedTPG rank-1 fraction={core_row['fixed_tpg_rank1_fraction']:.3f}, "
            f"beats RAR fraction={core_row['fixed_tpg_beats_rar_fraction']:.3f}, "
            f"beats MOND fraction={core_row['fixed_tpg_beats_mond_fraction']:.3f}, "
            f"beats Newtonian fraction={core_row['fixed_tpg_beats_newtonian_fraction']:.3f}."
        )
    else:
        core_text = "No v02_core_like rows found."

    morph_best = morph_summary.sort_values("mean_delta_tau_minus_v6").head(3)
    full_holdout = full_overall.loc[full_overall["split"] == "holdout"]
    if not full_holdout.empty:
        holdout_row = full_holdout.iloc[0].to_dict()
        full_text = (
            f"175-galaxy proxy runner holdout: n={int(holdout_row['n_galaxies'])}, "
            f"Tau-proxy beats TPG/v6 fraction={holdout_row['tau_beats_tpg_v6_fraction']:.3f}, "
            f"mean Tau-TPG delta={holdout_row['mean_tau_minus_tpg_v6']:.6g}, "
            f"Tau-proxy beats MOND fraction={holdout_row['tau_beats_mond_fraction']:.3f}."
        )
    else:
        full_text = "175-galaxy proxy runner holdout row unavailable."
    best_paper1 = paper1_summary.sort_values("median_tau_minus_baseline").head(8)
    rmond_fraction = None
    if "hdda_dtl_better_than_rmond_mond" in rmond_gallery.columns:
        rmond_fraction = float(rmond_gallery["hdda_dtl_better_than_rmond_mond"].mean())

    lines = [
        "# Available-data Morphology Readout Pilot",
        "",
        "This report audits what can be checked today from existing local data.",
        "It is not the final Paper 8 MORPHOLOGY-MATCHED-FORWARD-READOUT-GATE",
        "because residual-blind morphology-family labels and per-family",
        "forward `delta_g^K` score tables are not yet available.",
        "",
        "## Main Verdict",
        "",
        "- The full Paper 8 morphology-family endpoint is still blocked.",
        "- The available 143-galaxy component proxy supports a narrower statement:",
        "  the v02_core_like Tau-like/FixedTPG proxy group beats RAR, MOND, and",
        "  Newtonian within that residual-guardrailed proxy group.",
        "- This is not yet evidence that morphology-selected Tau Core families beat",
        "  TGP, because the proxy group uses FixedTPG itself rather than distinct",
        "  Paper 8 morphology-family formula outputs.",
        "- The morphology-decomposition runner is mixed: some morphology splits improve",
        "  over TPG/v6, others do not.",
        "- The 175-galaxy Tau-proxy runner gives a larger-sample check against TPG/v6",
        "  and MOND, but it is still a proxy family rather than the final Paper 8",
        "  morphology-family readout.",
        "- Full-sample RMOND comparison is blocked until a frozen pointwise",
        "  `V_RMOND(R)` prescription exists.",
        "",
        "## Key Proxy Result",
        "",
        core_text,
        "",
        "## Larger-Sample 175-Galaxy Proxy Runner",
        "",
        full_text,
        "",
        "Best type-bin holdout rows by mean Tau-minus-TPG/v6 delta:",
        "",
        markdown_table(
            full_by_type.loc[full_by_type["split"] == "holdout"]
            .sort_values("mean_tau_minus_tpg_v6")
            .head(8)
        ),
        "",
        "## 73-Galaxy Paper 1 Full-Baseline Layer",
        "",
        "This layer contains Newtonian, MOND, RAR, projection, and several",
        "Tau-core S_tau score variants, but it is an A/B/C residual-disturbance",
        "sample rather than a Paper 8 morphology-family endpoint.",
        "",
        markdown_table(best_paper1),
        "",
        "## Best Morphology-Decomposition Holdout Rows",
        "",
        markdown_table(morph_best),
        "",
    ]
    if rmond_fraction is not None:
        lines.extend(
            [
                "## Limited RMOND/MOND Gallery",
                "",
                f"HDDA/DTL is better than the combined RMOND/MOND comparator in {rmond_fraction:.3f} of the six gallery objects.",
                "This is only an illustrative mixed-unit gallery check, not a Paper 8 endpoint.",
                "",
            ]
        )
    lines.extend(
        [
            "## Required Next Action",
            "",
            "Create `morphology_labels_predeclared.csv` and a per-family scored table",
            "`matched_wrong_family_scores.csv` where each galaxy is evaluated under",
            "all candidate morphology families. Only then can Paper 8 answer the",
            "main question directly: matched Tau Core family versus wrong families,",
            "shuffled labels, TGP, RMOND, MOND, RAR, and Newtonian.",
            "",
            "## Wide Proxy Summary",
            "",
            markdown_table(wide_summary),
        ]
    )
    (REPORTS / "available_morphology_readout_pilot.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    availability = availability_rows()
    wide = load_wide_specificity()
    wide_summary, ranks, rank_summary = wide_specificity_outputs(wide)
    morph_holdout, morph_summary = morphology_decomposition_outputs()
    full_proxy, full_overall, full_by_type = full_sparc_proxy_outputs()
    paper1_pivot, paper1_summary, paper1_class_summary = paper1_baseline_outputs()
    rmond_gallery = limited_rmond_gallery_output()

    availability.to_csv(DATA / "available_data_morphology_readout_availability.csv", index=False)
    wide_summary.to_csv(DATA / "available_data_wide_fixed_tpg_proxy_summary.csv", index=False)
    ranks.to_csv(DATA / "available_data_wide_fixed_tpg_proxy_ranks.csv", index=False)
    rank_summary.to_csv(DATA / "available_data_wide_fixed_tpg_proxy_rank_summary.csv", index=False)
    morph_holdout.to_csv(DATA / "available_data_morphology_decomposition_holdout.csv", index=False)
    morph_summary.to_csv(DATA / "available_data_morphology_decomposition_summary.csv", index=False)
    full_proxy.to_csv(DATA / "available_data_full_sparc_tau_proxy_galaxies.csv", index=False)
    full_overall.to_csv(DATA / "available_data_full_sparc_tau_proxy_overall.csv", index=False)
    full_by_type.to_csv(DATA / "available_data_full_sparc_tau_proxy_by_type.csv", index=False)
    paper1_pivot.to_csv(DATA / "available_data_paper1_73_galaxy_baseline_pivot.csv", index=False)
    paper1_summary.to_csv(DATA / "available_data_paper1_73_galaxy_tau_baseline_summary.csv", index=False)
    paper1_class_summary.to_csv(
        DATA / "available_data_paper1_73_galaxy_tau_baseline_by_class.csv", index=False
    )
    rmond_gallery.to_csv(DATA / "available_data_limited_rmond_gallery.csv", index=False)

    write_report(
        wide_summary,
        rank_summary,
        morph_summary,
        rmond_gallery,
        full_overall,
        full_by_type,
        paper1_summary,
    )
    print("PAPER8_AVAILABLE_MORPHOLOGY_READOUT_PILOT_COMPLETE")


if __name__ == "__main__":
    main()
