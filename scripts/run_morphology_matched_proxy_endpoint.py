#!/usr/bin/env python3
"""Run a first morphology-matched Tau-proxy endpoint on the 175-galaxy packet.

This is still a proxy endpoint, not the final Paper 8 formula-family result.
It does, however, answer the next practical question more directly than the
generic Tau-proxy runner:

    morphology label K_g -> family amplitude beta_K -> forward score

The morphology labels are assigned from metadata, and beta_K is learned on the
pre-existing train split only. Holdout scoring evaluates the matched family
against wrong families, TPG/v6, and MOND.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
TPG_RESULTS = Path("/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1")


def assign_family(row: pd.Series) -> str:
    """Residual-blind proxy label from SPARC metadata and baryonic morphology proxies."""
    if row["mean_bulge"] >= 0.10 or row["type_bin"] == "early_T_le_2":
        return "K_compact_bulge"
    if row["type_bin"] == "irregular_T_ge_9" or (
        row["mean_gas"] >= 0.35 and row["mean_log_sbdisk"] <= 0.90
    ):
        return "K_diffuse_scale_tail"
    if row["type_bin"] == "late_T_6_8":
        return "K_late_exponential"
    return "K_mid_regular"


def load_points() -> tuple[pd.DataFrame, pd.DataFrame]:
    points_path = TPG_RESULTS / "tau_rotation_curve_frozen_proxy_runner_v0_points.csv"
    meta_path = TPG_RESULTS / "tau_rotation_curve_projection_metadata_control_v0.csv"
    if not points_path.exists():
        raise FileNotFoundError(points_path)
    if not meta_path.exists():
        raise FileNotFoundError(meta_path)

    points = pd.read_csv(points_path)
    meta = pd.read_csv(meta_path)
    features = (
        points.groupby("galaxy")
        .agg(
            n_points=("r", "size"),
            mean_gas=("total_gas_fraction", "mean"),
            mean_bulge=("bulge_frac", "mean"),
            max_bulge=("bulge_frac", "max"),
            mean_log_sbdisk=("log_sbdisk", "mean"),
            peak_sb=("log_sb_peak", "max"),
            mean_abs_rparent=("rparent_cd", lambda s: s.abs().mean()),
        )
        .reset_index()
    )
    labels = features.merge(
        meta[["galaxy", "split", "role", "type_bin", "inc_bin", "hub_type"]],
        on="galaxy",
        how="left",
    )
    labels["morphology_family"] = labels.apply(assign_family, axis=1)
    labels["label_source"] = (
        "metadata_proxy:type_bin+bulge_frac+gas_fraction+surface_brightness;no residual endpoints"
    )

    points = points.merge(labels[["galaxy", "morphology_family"]], on="galaxy", how="left")
    return points, labels


def fit_family_betas(points: pd.DataFrame) -> pd.DataFrame:
    train = points.loc[points["split"] == "train"].copy()
    rows = []
    global_num = ((train["vobs"] - train["v_v6"]) * train["rparent_cd"]).sum()
    global_den = train["rparent_cd"].pow(2).sum()
    global_beta = float(global_num / global_den)
    for family, sub in train.groupby("morphology_family"):
        den = sub["rparent_cd"].pow(2).sum()
        beta = float(((sub["vobs"] - sub["v_v6"]) * sub["rparent_cd"]).sum() / den) if den else 0.0
        rows.append(
            {
                "morphology_family": family,
                "beta": beta,
                "n_train_points": int(len(sub)),
                "n_train_galaxies": int(sub["galaxy"].nunique()),
                "fit_policy": "least_squares_train_only_on_vobs_minus_v6_over_rparent_cd",
            }
        )
    rows.append(
        {
            "morphology_family": "K_global_tau_proxy",
            "beta": global_beta,
            "n_train_points": int(len(train)),
            "n_train_galaxies": int(train["galaxy"].nunique()),
            "fit_policy": "global_train_only_reference",
        }
    )
    return pd.DataFrame(rows).sort_values("morphology_family")


def score_family(points: pd.DataFrame, beta: float) -> pd.Series:
    return points["v_v6"] + beta * points["rparent_cd"]


def rmse(df: pd.DataFrame, pred_col: str) -> float:
    return float(((df[pred_col] - df["vobs"]).pow(2).mean()) ** 0.5)


def score_all(
    points: pd.DataFrame, betas: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    beta_map = dict(zip(betas["morphology_family"], betas["beta"]))
    families = [f for f in beta_map if f != "K_global_tau_proxy"]
    scored = points.copy()
    for family in families + ["K_global_tau_proxy"]:
        scored[f"v_{family}"] = score_family(scored, beta_map[family])

    rows = []
    for galaxy, sub in scored.groupby("galaxy"):
        matched_family = sub["morphology_family"].iloc[0]
        base = {
            "galaxy": galaxy,
            "split": sub["split"].iloc[0],
            "morphology_family": matched_family,
            "n_points": int(len(sub)),
            "rmse_tpg_v6": rmse(sub, "v_v6"),
            "rmse_mond": rmse(sub, "v_mond"),
            "rmse_global_tau_proxy": rmse(sub, "v_K_global_tau_proxy"),
        }
        family_scores = {}
        for family in families:
            value = rmse(sub, f"v_{family}")
            family_scores[f"rmse_{family}"] = value
        matched = family_scores[f"rmse_{matched_family}"]
        wrong_values = [v for k, v in family_scores.items() if k != f"rmse_{matched_family}"]
        base.update(family_scores)
        base["rmse_matched_family"] = matched
        base["rmse_wrong_family_mean"] = float(sum(wrong_values) / len(wrong_values))
        base["best_family"] = min(families, key=lambda f: family_scores[f"rmse_{f}"])
        base["matched_family_rank"] = (
            sorted(families, key=lambda f: family_scores[f"rmse_{f}"]).index(matched_family) + 1
        )
        base["matched_minus_wrong_mean"] = base["rmse_matched_family"] - base["rmse_wrong_family_mean"]
        base["matched_minus_tpg_v6"] = base["rmse_matched_family"] - base["rmse_tpg_v6"]
        base["matched_minus_mond"] = base["rmse_matched_family"] - base["rmse_mond"]
        base["matched_beats_wrong_mean"] = base["matched_minus_wrong_mean"] < 0
        base["matched_beats_tpg_v6"] = base["matched_minus_tpg_v6"] < 0
        base["matched_beats_mond"] = base["matched_minus_mond"] < 0
        rows.append(base)

    galaxy_scores = pd.DataFrame(rows).sort_values(["split", "galaxy"])
    summary_rows = []
    for split, sub in galaxy_scores.groupby("split"):
        summary_rows.append(
            {
                "split": split,
                "n_galaxies": int(len(sub)),
                "matched_beats_wrong_fraction": float(sub["matched_beats_wrong_mean"].mean()),
                "matched_rank1_fraction": float((sub["matched_family_rank"] == 1).mean()),
                "matched_beats_tpg_v6_fraction": float(sub["matched_beats_tpg_v6"].mean()),
                "matched_beats_mond_fraction": float(sub["matched_beats_mond"].mean()),
                "mean_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].mean()),
                "median_matched_minus_wrong": float(sub["matched_minus_wrong_mean"].median()),
                "mean_matched_minus_tpg_v6": float(sub["matched_minus_tpg_v6"].mean()),
                "median_matched_minus_tpg_v6": float(sub["matched_minus_tpg_v6"].median()),
                "mean_matched_minus_mond": float(sub["matched_minus_mond"].mean()),
                "median_matched_minus_mond": float(sub["matched_minus_mond"].median()),
            }
        )
    summary = pd.DataFrame(summary_rows)

    by_family = (
        galaxy_scores.groupby(["split", "morphology_family"])
        .agg(
            n_galaxies=("galaxy", "count"),
            matched_beats_wrong_fraction=("matched_beats_wrong_mean", "mean"),
            matched_rank1_fraction=("matched_family_rank", lambda s: float((s == 1).mean())),
            matched_beats_tpg_v6_fraction=("matched_beats_tpg_v6", "mean"),
            matched_beats_mond_fraction=("matched_beats_mond", "mean"),
            median_matched_minus_wrong=("matched_minus_wrong_mean", "median"),
            median_matched_minus_tpg_v6=("matched_minus_tpg_v6", "median"),
            median_matched_minus_mond=("matched_minus_mond", "median"),
        )
        .reset_index()
        .sort_values(["split", "morphology_family"])
    )
    return scored, galaxy_scores, summary, by_family


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda x: f"{x:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def write_report(labels: pd.DataFrame, betas: pd.DataFrame, summary: pd.DataFrame, by_family: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    lines = [
        "# Morphology-Matched Tau-Proxy Endpoint",
        "",
        "This is the first proxy implementation of the Paper 8 matched-family idea:",
        "galaxy morphology metadata selects a Tau-proxy family, family amplitudes",
        "are fit on the train split only, and the holdout split is scored against",
        "wrong families, TPG/v6, and MOND.",
        "",
        "It is not the final Paper 8 endpoint because the families are still proxy",
        "families built from the available `rparent_cd` channel rather than the",
        "final morphology-specific `delta_g^K` formula shells.",
        "",
        "## Holdout Verdict",
        "",
        f"- Holdout galaxies: {int(holdout['n_galaxies'])}",
        f"- Matched family beats wrong-family mean: {holdout['matched_beats_wrong_fraction']:.3f}",
        f"- Matched family rank-1 fraction: {holdout['matched_rank1_fraction']:.3f}",
        f"- Matched family beats TPG/v6: {holdout['matched_beats_tpg_v6_fraction']:.3f}",
        f"- Matched family beats MOND: {holdout['matched_beats_mond_fraction']:.3f}",
        f"- Mean matched-minus-wrong RMSE: {holdout['mean_matched_minus_wrong']:.6g}",
        f"- Mean matched-minus-TPG/v6 RMSE: {holdout['mean_matched_minus_tpg_v6']:.6g}",
        f"- Mean matched-minus-MOND RMSE: {holdout['mean_matched_minus_mond']:.6g}",
        "",
        "## Family Amplitudes",
        "",
        markdown_table(betas),
        "",
        "## Holdout By Family",
        "",
        markdown_table(by_family.loc[by_family["split"] == "holdout"]),
        "",
        "## Label Counts",
        "",
        markdown_table(
            labels.groupby(["split", "morphology_family"]).size().reset_index(name="n_galaxies")
        ),
        "",
        "## Claim Boundary",
        "",
        "A positive matched-vs-wrong result here would be a useful preflight signal.",
        "It is not a claim that final Tau Core morphology readout formulas beat",
        "TGP/RMOND/MOND/Newtonian. RMOND and Newtonian are not both available in",
        "this 175-galaxy point-level runner.",
    ]
    (REPORTS / "morphology_matched_tau_proxy_endpoint.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, labels = load_points()
    betas = fit_family_betas(points)
    _, galaxy_scores, summary, by_family = score_all(points, betas)

    labels.to_csv(DATA / "morphology_labels_predeclared_proxy.csv", index=False)
    betas.to_csv(DATA / "morphology_matched_proxy_family_betas.csv", index=False)
    galaxy_scores.to_csv(DATA / "morphology_matched_proxy_scores_by_galaxy.csv", index=False)
    summary.to_csv(DATA / "morphology_matched_proxy_endpoint_summary.csv", index=False)
    by_family.to_csv(DATA / "morphology_matched_proxy_endpoint_by_family.csv", index=False)
    write_report(labels, betas, summary, by_family)
    print("PAPER8_MORPHOLOGY_MATCHED_PROXY_ENDPOINT_COMPLETE")


if __name__ == "__main__":
    main()
