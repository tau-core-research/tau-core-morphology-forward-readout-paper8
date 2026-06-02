#!/usr/bin/env python3
"""Run a morphology-specific formula-shell proxy endpoint.

This is one step closer to the final Paper 8 endpoint than the single-channel
`rparent_cd` Tau-proxy test. Each morphology family receives a different
predeclared radial shell feature, but the features are still available-data
proxies rather than source-native Tau Core 4D readout formulas.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
TPG_RESULTS = Path("/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1")
SHUFFLE_SEED = 2718
N_SHUFFLES = 1000


FORMULA_FAMILIES = [
    "K_compact_finite",
    "K_scale_tail_spiral",
    "K_exponential_disk",
    "K_thick_flared",
]


def load_points() -> pd.DataFrame:
    points_path = TPG_RESULTS / "tau_rotation_curve_frozen_proxy_runner_v0_points.csv"
    meta_path = TPG_RESULTS / "tau_core_projection_metadata_control_v0.csv"
    fallback_meta_path = TPG_RESULTS / "tau_rotation_curve_projection_metadata_control_v0.csv"
    if not points_path.exists():
        raise FileNotFoundError(points_path)
    meta_path = meta_path if meta_path.exists() else fallback_meta_path
    if not meta_path.exists():
        raise FileNotFoundError(meta_path)

    points = pd.read_csv(points_path)
    meta = pd.read_csv(meta_path)
    galaxy_stats = (
        points.groupby("galaxy")
        .agg(
            n_points=("r", "size"),
            r_median=("r", "median"),
            r_max=("r", "max"),
            mean_gas=("total_gas_fraction", "mean"),
            mean_bulge=("bulge_frac", "mean"),
            mean_log_sbdisk=("log_sbdisk", "mean"),
            peak_sb=("log_sb_peak", "max"),
            mean_abs_rparent=("rparent_cd", lambda s: float(s.abs().mean())),
        )
        .reset_index()
    )
    labels = galaxy_stats.merge(
        meta[["galaxy", "split", "role", "type_bin", "inc_bin", "hub_type"]],
        on="galaxy",
        how="left",
    )
    labels["formula_family"] = labels.apply(assign_formula_family, axis=1)
    labels["label_source"] = (
        "metadata_proxy:type_bin+bulge_frac+gas_fraction+surface_brightness;no residual endpoints"
    )
    points = points.merge(
        labels[
            [
                "galaxy",
                "formula_family",
                "r_median",
                "r_max",
                "mean_gas",
                "mean_bulge",
                "mean_log_sbdisk",
            ]
        ],
        on="galaxy",
        how="left",
    )
    return points, labels


def assign_formula_family(row: pd.Series) -> str:
    """Residual-blind available-data family assignment."""
    if row["mean_bulge"] >= 0.10 or row["type_bin"] == "early_T_le_2":
        return "K_compact_finite"
    if row["type_bin"] == "irregular_T_ge_9" or (
        row["mean_gas"] >= 0.35 and row["mean_log_sbdisk"] <= 0.90
    ):
        return "K_scale_tail_spiral"
    if row["type_bin"] == "late_T_6_8":
        return "K_exponential_disk"
    return "K_thick_flared"


def add_shell_features(points: pd.DataFrame) -> pd.DataFrame:
    """Add predeclared dimensionless radial shell features."""
    out = points.copy()
    eps = 1.0e-9
    rc = out["r_median"].clip(lower=eps)
    x = (out["r"] / rc).clip(lower=0.0)
    gas = out["mean_gas"].clip(lower=0.0)
    bulge = out["mean_bulge"].clip(lower=0.0)
    sb = out["log_sbdisk"].fillna(out["mean_log_sbdisk"]).fillna(0.0)
    sb_norm = sb - sb.groupby(out["galaxy"]).transform("mean")

    # These are formula-shell proxies, not physical velocity laws. The fitted
    # amplitude carries velocity units; the shell feature is dimensionless.
    out["shell_K_scale_tail_spiral"] = np.log1p(x) / (1.0 + 0.45 * x)
    out["shell_K_exponential_disk"] = x * np.exp(-x)
    out["shell_K_compact_finite"] = (1.0 + bulge) / (1.0 + x).pow(2)
    out["shell_K_thick_flared"] = np.sqrt(x + eps) / (1.0 + x) * (1.0 + 0.5 * gas)

    # Preserve a mild morphology-gradient proxy for disk families, but keep it
    # centered per galaxy so it cannot behave like a free offset.
    out["shell_K_exponential_disk"] *= 1.0 + 0.05 * sb_norm.clip(lower=-3.0, upper=3.0)
    out["shell_K_scale_tail_spiral"] *= 1.0 + 0.25 * gas
    return out


def fit_shell_amplitudes(points: pd.DataFrame) -> pd.DataFrame:
    train = points.loc[points["split"] == "train"].copy()
    rows = []
    for family in FORMULA_FAMILIES:
        sub = train.loc[train["formula_family"] == family]
        feature = f"shell_{family}"
        den = sub[feature].pow(2).sum()
        beta = float(((sub["vobs"] - sub["v_v6"]) * sub[feature]).sum() / den) if den else 0.0
        rows.append(
            {
                "formula_family": family,
                "beta": beta,
                "n_train_points": int(len(sub)),
                "n_train_galaxies": int(sub["galaxy"].nunique()),
                "feature": feature,
                "fit_policy": "least_squares_train_only_on_vobs_minus_v6_over_predeclared_shell_feature",
            }
        )
    return pd.DataFrame(rows)


def rmse(df: pd.DataFrame, pred_col: str) -> float:
    return float(((df[pred_col] - df["vobs"]).pow(2).mean()) ** 0.5)


def score_all(
    points: pd.DataFrame, amplitudes: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    beta_map = dict(zip(amplitudes["formula_family"], amplitudes["beta"]))
    scored = points.copy()
    for family in FORMULA_FAMILIES:
        scored[f"v_{family}"] = scored["v_v6"] + beta_map[family] * scored[f"shell_{family}"]

    rows = []
    for galaxy, sub in scored.groupby("galaxy"):
        matched_family = sub["formula_family"].iloc[0]
        family_scores = {family: rmse(sub, f"v_{family}") for family in FORMULA_FAMILIES}
        matched = family_scores[matched_family]
        wrong_values = [value for family, value in family_scores.items() if family != matched_family]
        row = {
            "galaxy": galaxy,
            "split": sub["split"].iloc[0],
            "formula_family": matched_family,
            "n_points": int(len(sub)),
            "rmse_tpg_v6": rmse(sub, "v_v6"),
            "rmse_mond": rmse(sub, "v_mond"),
            "rmse_matched_family": matched,
            "rmse_wrong_family_mean": float(sum(wrong_values) / len(wrong_values)),
            "best_family": min(FORMULA_FAMILIES, key=lambda family: family_scores[family]),
            "matched_family_rank": (
                sorted(FORMULA_FAMILIES, key=lambda family: family_scores[family]).index(matched_family)
                + 1
            ),
        }
        for family, value in family_scores.items():
            row[f"rmse_{family}"] = value
        row["matched_minus_wrong_mean"] = row["rmse_matched_family"] - row["rmse_wrong_family_mean"]
        row["matched_minus_tpg_v6"] = row["rmse_matched_family"] - row["rmse_tpg_v6"]
        row["matched_minus_mond"] = row["rmse_matched_family"] - row["rmse_mond"]
        row["matched_beats_wrong_mean"] = row["matched_minus_wrong_mean"] < 0
        row["matched_beats_tpg_v6"] = row["matched_minus_tpg_v6"] < 0
        row["matched_beats_mond"] = row["matched_minus_mond"] < 0
        rows.append(row)

    galaxy_scores = pd.DataFrame(rows).sort_values(["split", "galaxy"])
    summary = summarize_scores(galaxy_scores)
    by_family = (
        galaxy_scores.groupby(["split", "formula_family"])
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
        .sort_values(["split", "formula_family"])
    )
    return scored, galaxy_scores, summary, by_family


def summarize_scores(galaxy_scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, sub in galaxy_scores.groupby("split"):
        rows.append(
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
    return pd.DataFrame(rows)


def run_shuffled_label_null(
    galaxy_scores: pd.DataFrame, n_shuffles: int = N_SHUFFLES
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(SHUFFLE_SEED)
    rows = []
    for split, sub in galaxy_scores.groupby("split"):
        sub = sub.reset_index(drop=True)
        true_labels = sub["formula_family"].to_numpy()
        observed = {
            "mean_minus_wrong": float(sub["matched_minus_wrong_mean"].mean()),
            "beats_wrong_fraction": float(sub["matched_beats_wrong_mean"].mean()),
            "rank1_fraction": float((sub["matched_family_rank"] == 1).mean()),
        }
        for shuffle_id in range(n_shuffles):
            shuffled = rng.permutation(true_labels)
            minus_wrong = []
            beats_wrong = []
            ranks = []
            for row_idx, family in enumerate(shuffled):
                scores = {
                    candidate: float(sub.loc[row_idx, f"rmse_{candidate}"])
                    for candidate in FORMULA_FAMILIES
                }
                selected = scores[family]
                wrong = [value for candidate, value in scores.items() if candidate != family]
                wrong_mean = float(sum(wrong) / len(wrong))
                minus_wrong.append(selected - wrong_mean)
                beats_wrong.append(selected < wrong_mean)
                ranks.append(sorted(FORMULA_FAMILIES, key=lambda candidate: scores[candidate]).index(family) + 1)
            rows.append(
                {
                    "split": split,
                    "shuffle_id": shuffle_id,
                    "seed": SHUFFLE_SEED,
                    "n_galaxies": int(len(sub)),
                    "mean_shuffled_minus_wrong": float(np.mean(minus_wrong)),
                    "shuffled_beats_wrong_fraction": float(np.mean(beats_wrong)),
                    "shuffled_rank1_fraction": float(np.mean(np.array(ranks) == 1)),
                    "observed_mean_minus_wrong": observed["mean_minus_wrong"],
                    "observed_beats_wrong_fraction": observed["beats_wrong_fraction"],
                    "observed_rank1_fraction": observed["rank1_fraction"],
                }
            )
    shuffled = pd.DataFrame(rows)
    summary_rows = []
    for split, sub in shuffled.groupby("split"):
        observed = sub.iloc[0]
        n = len(sub)
        summary_rows.append(
            {
                "split": split,
                "n_shuffles": int(n),
                "seed": SHUFFLE_SEED,
                "observed_mean_minus_wrong": float(observed["observed_mean_minus_wrong"]),
                "null_mean_minus_wrong_mean": float(sub["mean_shuffled_minus_wrong"].mean()),
                "null_mean_minus_wrong_median": float(sub["mean_shuffled_minus_wrong"].median()),
                "p_mean_minus_wrong_at_least_as_good": float(
                    (1 + (sub["mean_shuffled_minus_wrong"] <= observed["observed_mean_minus_wrong"]).sum())
                    / (n + 1)
                ),
                "observed_beats_wrong_fraction": float(observed["observed_beats_wrong_fraction"]),
                "null_beats_wrong_fraction_mean": float(sub["shuffled_beats_wrong_fraction"].mean()),
                "null_beats_wrong_fraction_median": float(sub["shuffled_beats_wrong_fraction"].median()),
                "p_beats_wrong_fraction_at_least_as_good": float(
                    (
                        1
                        + (
                            sub["shuffled_beats_wrong_fraction"]
                            >= observed["observed_beats_wrong_fraction"]
                        ).sum()
                    )
                    / (n + 1)
                ),
                "observed_rank1_fraction": float(observed["observed_rank1_fraction"]),
                "null_rank1_fraction_mean": float(sub["shuffled_rank1_fraction"].mean()),
                "null_rank1_fraction_median": float(sub["shuffled_rank1_fraction"].median()),
                "p_rank1_fraction_at_least_as_good": float(
                    (1 + (sub["shuffled_rank1_fraction"] >= observed["observed_rank1_fraction"]).sum())
                    / (n + 1)
                ),
            }
        )
    return shuffled, pd.DataFrame(summary_rows)


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


def write_report(
    labels: pd.DataFrame,
    amplitudes: pd.DataFrame,
    summary: pd.DataFrame,
    by_family: pd.DataFrame,
    shuffled_summary: pd.DataFrame,
) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    holdout_null = shuffled_summary.loc[shuffled_summary["split"] == "holdout"].iloc[0]
    lines = [
        "# Morphology Formula-Shell Proxy Endpoint",
        "",
        "This is an available-data preflight for morphology-specific formula shells.",
        "It is closer to the final Paper 8 target than the single-channel Tau proxy,",
        "but it is still not the final endpoint because the shell features are",
        "dimensionless radial proxies built from available SPARC-like metadata.",
        "",
        "## Holdout Verdict",
        "",
        f"- Holdout galaxies: {int(holdout['n_galaxies'])}",
        f"- Matched shell beats wrong-shell mean: {holdout['matched_beats_wrong_fraction']:.3f}",
        f"- Matched shell rank-1 fraction: {holdout['matched_rank1_fraction']:.3f}",
        f"- Matched shell beats TPG/v6: {holdout['matched_beats_tpg_v6_fraction']:.3f}",
        f"- Matched shell beats MOND: {holdout['matched_beats_mond_fraction']:.3f}",
        f"- Mean matched-minus-wrong RMSE: {holdout['mean_matched_minus_wrong']:.6g}",
        f"- Mean matched-minus-TPG/v6 RMSE: {holdout['mean_matched_minus_tpg_v6']:.6g}",
        f"- Mean matched-minus-MOND RMSE: {holdout['mean_matched_minus_mond']:.6g}",
        "",
        "## Shuffled-Label Null",
        "",
        f"- Shuffles: {int(holdout_null['n_shuffles'])}",
        f"- Seed: {int(holdout_null['seed'])}",
        f"- Holdout observed mean matched-minus-wrong: {holdout_null['observed_mean_minus_wrong']:.6g}",
        f"- Holdout shuffled-null mean: {holdout_null['null_mean_minus_wrong_mean']:.6g}",
        f"- P(null at least as good; mean-minus-wrong): {holdout_null['p_mean_minus_wrong_at_least_as_good']:.4f}",
        f"- Holdout observed beats-wrong fraction: {holdout_null['observed_beats_wrong_fraction']:.3f}",
        f"- Holdout shuffled beats-wrong mean: {holdout_null['null_beats_wrong_fraction_mean']:.3f}",
        f"- P(null at least as good; beats-wrong fraction): {holdout_null['p_beats_wrong_fraction_at_least_as_good']:.4f}",
        f"- Holdout observed rank-1 fraction: {holdout_null['observed_rank1_fraction']:.3f}",
        f"- Holdout shuffled rank-1 mean: {holdout_null['null_rank1_fraction_mean']:.3f}",
        f"- P(null at least as good; rank-1 fraction): {holdout_null['p_rank1_fraction_at_least_as_good']:.4f}",
        "",
        "## Shell Amplitudes",
        "",
        markdown_table(amplitudes),
        "",
        "## Holdout By Family",
        "",
        markdown_table(by_family.loc[by_family["split"] == "holdout"]),
        "",
        "## Label Counts",
        "",
        markdown_table(labels.groupby(["split", "formula_family"]).size().reset_index(name="n_galaxies")),
        "",
        "## Claim Boundary",
        "",
        "This is a preparation endpoint, not empirical validation. A strong final",
        "Paper 8 result still requires source-native morphology labels, physically",
        "audited 4D readout shells, dimensional checks, and baseline comparisons",
        "including Newtonian/RAR layers where available.",
    ]
    (REPORTS / "morphology_formula_shell_proxy_endpoint.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, labels = load_points()
    points = add_shell_features(points)
    amplitudes = fit_shell_amplitudes(points)
    _, galaxy_scores, summary, by_family = score_all(points, amplitudes)
    shuffled, shuffled_summary = run_shuffled_label_null(galaxy_scores)

    labels.to_csv(DATA / "morphology_formula_shell_proxy_labels.csv", index=False)
    amplitudes.to_csv(DATA / "morphology_formula_shell_proxy_amplitudes.csv", index=False)
    galaxy_scores.to_csv(DATA / "morphology_formula_shell_proxy_scores_by_galaxy.csv", index=False)
    summary.to_csv(DATA / "morphology_formula_shell_proxy_endpoint_summary.csv", index=False)
    by_family.to_csv(DATA / "morphology_formula_shell_proxy_endpoint_by_family.csv", index=False)
    shuffled.to_csv(DATA / "morphology_formula_shell_proxy_shuffled_null.csv", index=False)
    shuffled_summary.to_csv(DATA / "morphology_formula_shell_proxy_shuffled_null_summary.csv", index=False)
    write_report(labels, amplitudes, summary, by_family, shuffled_summary)
    print("PAPER8_MORPHOLOGY_FORMULA_SHELL_PROXY_ENDPOINT_COMPLETE")


if __name__ == "__main__":
    main()
