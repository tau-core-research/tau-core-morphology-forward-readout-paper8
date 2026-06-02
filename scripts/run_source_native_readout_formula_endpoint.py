#!/usr/bin/env python3
"""Run bridge-formula readout shells as a Paper 8 available-data preflight.

This script uses the concrete Tau Core bridge formula shells as executable
`delta v^2` readout kernels:

- scale-tail n=2: delta v^2 = A I_2(R) / R
- exponential disk: delta v^2 = Sigma_C0 R_s y^2 (I0K0-I1K1)
- compact finite: delta v^2 = B_c / R outside compact support
- thick/flared disk: damped Fourier-Bessel exponential-disk shell

The endpoint remains a preflight because the morphology scales are still
available-data proxies. The formula shapes themselves are the bridge shells;
the source-native morphology parameters are not yet fully available.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import special


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
TPG_RESULTS = Path("/Users/jolcsak/Projects/TPG/results/tau_core_projection_v1")
SHUFFLE_SEED = 31415
N_SHUFFLES = 1000

FORMULA_FAMILIES = [
    "K_compact_finite",
    "K_scale_tail_spiral",
    "K_exponential_disk",
    "K_thick_flared",
]

FORMULA_SOURCES = {
    "K_scale_tail_spiral": "tau_core_gravity_rmond_scale_tail_spiral_readout_formula_001:n=2",
    "K_exponential_disk": "tau_core_gravity_rmond_exponential_disk_readout_formula_001:Freeman_Bessel",
    "K_compact_finite": "tau_core_gravity_rmond_compact_finite_source_readout_formula_001",
    "K_thick_flared": "tau_core_gravity_rmond_thick_flared_disk_readout_formula_001:constant_h_exponential_vertical",
}


def assign_formula_family(row: pd.Series) -> str:
    if row["mean_bulge"] >= 0.10 or row["type_bin"] == "early_T_le_2":
        return "K_compact_finite"
    if row["type_bin"] == "irregular_T_ge_9" or (
        row["mean_gas"] >= 0.35 and row["mean_log_sbdisk"] <= 0.90
    ):
        return "K_scale_tail_spiral"
    if row["type_bin"] == "late_T_6_8":
        return "K_exponential_disk"
    return "K_thick_flared"


def load_points() -> tuple[pd.DataFrame, pd.DataFrame]:
    points_path = TPG_RESULTS / "tau_rotation_curve_frozen_proxy_runner_v0_points.csv"
    meta_path = TPG_RESULTS / "tau_rotation_curve_projection_metadata_control_v0.csv"
    if not points_path.exists():
        raise FileNotFoundError(points_path)
    if not meta_path.exists():
        raise FileNotFoundError(meta_path)

    points = pd.read_csv(points_path)
    meta = pd.read_csv(meta_path)
    labels = (
        points.groupby("galaxy")
        .agg(
            n_points=("r", "size"),
            r_median=("r", "median"),
            r_max=("r", "max"),
            mean_gas=("total_gas_fraction", "mean"),
            mean_bulge=("bulge_frac", "mean"),
            mean_log_sbdisk=("log_sbdisk", "mean"),
            peak_sb=("log_sb_peak", "max"),
        )
        .reset_index()
        .merge(
            meta[["galaxy", "split", "role", "type_bin", "inc_bin", "hub_type"]],
            on="galaxy",
            how="left",
        )
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


def freeman_bessel_shape(y: pd.Series | np.ndarray) -> np.ndarray:
    values = np.asarray(y, dtype=float)
    clipped = np.clip(values, 1.0e-5, 80.0)
    combo = special.iv(0, clipped) * special.kv(0, clipped) - special.iv(1, clipped) * special.kv(1, clipped)
    shape = clipped * clipped * combo
    return np.nan_to_num(shape, nan=0.0, posinf=0.0, neginf=0.0)


def tail_i2_over_r(r: np.ndarray, r_in: float, r_cut: float, m: float = 2.0, s: float = 2.0) -> np.ndarray:
    """Numerically evaluate I_2(R)/R for the n=2 scale-tail formula."""
    safe_r = np.maximum(r, 1.0e-6)
    grid_max = max(float(np.max(safe_r)), r_cut * 1.05, r_in * 2.0, 1.0e-3)
    grid = np.linspace(0.0, grid_max, 512)
    grid[0] = 1.0e-8
    w_in = (grid / r_in) ** m / (1.0 + (grid / r_in) ** m)
    w_cut = 1.0 / (1.0 + (grid / r_cut) ** s)
    integrand = w_in * w_cut
    cumulative = np.zeros_like(grid)
    cumulative[1:] = np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(grid))
    return np.interp(safe_r, grid, cumulative) / safe_r


def thick_damped_shape(x: np.ndarray, h_over_rs: np.ndarray) -> np.ndarray:
    """Constant-h damped Fourier-Bessel shell for an exponential thick disk."""
    u = np.linspace(1.0e-4, 80.0, 900)
    base = u / np.power(1.0 + u * u, 1.5)
    rows = []
    for xi, hi in zip(x, h_over_rs):
        damping = 1.0 / (1.0 + u * hi)
        integrand = base * special.j1(u * xi) * damping
        rows.append(0.5 * xi * np.trapezoid(integrand, u))
    return np.nan_to_num(np.asarray(rows), nan=0.0, posinf=0.0, neginf=0.0)


def add_bridge_formula_kernels(points: pd.DataFrame) -> pd.DataFrame:
    out = points.copy()
    eps = 1.0e-6
    r = out["r"].clip(lower=eps)
    r_med = out["r_median"].clip(lower=eps)
    r_max = out["r_max"].clip(lower=r_med + eps)
    gas = out["mean_gas"].clip(lower=0.0)
    bulge = out["mean_bulge"].clip(lower=0.0)

    # Available-data scale proxies. These are the weak link in this preflight,
    # not the formula shells themselves.
    r_s = (r_med / 1.678).clip(lower=eps)
    y = r / (2.0 * r_s)
    out["kernel_K_exponential_disk"] = r_s * freeman_bessel_shape(y)

    out["kernel_K_compact_finite"] = 0.0
    for galaxy, idx in out.groupby("galaxy").groups.items():
        sub = out.loc[idx]
        rc = max(float(sub["r_median"].iloc[0]) * (1.0 + float(sub["mean_bulge"].iloc[0])), eps)
        rr = sub["r"].clip(lower=eps).to_numpy()
        kernel = np.where(rr < rc, rr * rr / (rc ** 3), 1.0 / rr)
        out.loc[idx, "kernel_K_compact_finite"] = kernel

    out["kernel_K_scale_tail_spiral"] = 0.0
    for galaxy, idx in out.groupby("galaxy").groups.items():
        sub = out.loc[idx]
        rin = max(float(sub["r_median"].iloc[0]) * 0.35, eps)
        rcut = max(float(sub["r_max"].iloc[0]) * (1.0 + 0.5 * float(sub["mean_gas"].iloc[0])), rin * 2.0)
        out.loc[idx, "kernel_K_scale_tail_spiral"] = tail_i2_over_r(sub["r"].to_numpy(), rin, rcut)

    x = (r / r_s).to_numpy()
    h_over_rs = np.clip(0.08 + 0.45 * gas.to_numpy(), 0.05, 0.75)
    out["kernel_K_thick_flared"] = r_s.to_numpy() * thick_damped_shape(x, h_over_rs)
    return out


def fit_amplitudes(points: pd.DataFrame) -> pd.DataFrame:
    train = points.loc[points["split"] == "train"].copy()
    target = train["vobs"].pow(2) - train["v_v6"].pow(2)
    rows = []
    for family in FORMULA_FAMILIES:
        sub = train.loc[train["formula_family"] == family]
        sub_target = target.loc[sub.index]
        kernel = sub[f"kernel_{family}"]
        den = kernel.pow(2).sum()
        beta = float((sub_target * kernel).sum() / den) if den else 0.0
        rows.append(
            {
                "formula_family": family,
                "beta_delta_v2_amplitude": beta,
                "n_train_points": int(len(sub)),
                "n_train_galaxies": int(sub["galaxy"].nunique()),
                "kernel": f"kernel_{family}",
                "formula_source": FORMULA_SOURCES[family],
                "fit_policy": "least_squares_train_only_on_vobs2_minus_v6_2_over_bridge_formula_kernel",
            }
        )
    return pd.DataFrame(rows)


def add_predictions(points: pd.DataFrame, amplitudes: pd.DataFrame) -> pd.DataFrame:
    beta_map = dict(zip(amplitudes["formula_family"], amplitudes["beta_delta_v2_amplitude"]))
    out = points.copy()
    base_v2 = out["v_v6"].pow(2)
    for family in FORMULA_FAMILIES:
        pred_v2 = base_v2 + beta_map[family] * out[f"kernel_{family}"]
        out[f"v_{family}"] = np.sqrt(np.maximum(pred_v2, 0.0))
    return out


def rmse(df: pd.DataFrame, pred_col: str) -> float:
    return float(((df[pred_col] - df["vobs"]).pow(2).mean()) ** 0.5)


def score_galaxies(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
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
    return galaxy_scores, summary, by_family


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


def run_shuffled_label_null(galaxy_scores: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
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
        for shuffle_id in range(N_SHUFFLES):
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
        "# Source-Native Bridge Readout Formula Endpoint",
        "",
        "This preflight uses the concrete Tau Core bridge morphology formulas as",
        "`delta v^2` readout kernels. It is not yet the final Paper 8 endpoint,",
        "because the morphology scale parameters are still available-data proxies.",
        "",
        "## Holdout Verdict",
        "",
        f"- Holdout galaxies: {int(holdout['n_galaxies'])}",
        f"- Matched bridge formula beats wrong-formula mean: {holdout['matched_beats_wrong_fraction']:.3f}",
        f"- Matched bridge formula rank-1 fraction: {holdout['matched_rank1_fraction']:.3f}",
        f"- Matched bridge formula beats TPG/v6: {holdout['matched_beats_tpg_v6_fraction']:.3f}",
        f"- Matched bridge formula beats MOND: {holdout['matched_beats_mond_fraction']:.3f}",
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
        "## Bridge Formula Amplitudes",
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
        "This is a source-native formula-shape preflight, not empirical validation.",
        "The weak link is the available-data morphology scale proxy, not the bridge",
        "formula registry itself. A final endpoint requires source-native",
        "morphology scale extraction and a nonleaky amplitude policy.",
    ]
    (REPORTS / "source_native_readout_formula_endpoint.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, labels = load_points()
    points = add_bridge_formula_kernels(points)
    amplitudes = fit_amplitudes(points)
    scored = add_predictions(points, amplitudes)
    galaxy_scores, summary, by_family = score_galaxies(scored)
    shuffled, shuffled_summary = run_shuffled_label_null(galaxy_scores)

    labels.to_csv(DATA / "source_native_readout_formula_labels.csv", index=False)
    amplitudes.to_csv(DATA / "source_native_readout_formula_amplitudes.csv", index=False)
    galaxy_scores.to_csv(DATA / "source_native_readout_formula_scores_by_galaxy.csv", index=False)
    summary.to_csv(DATA / "source_native_readout_formula_endpoint_summary.csv", index=False)
    by_family.to_csv(DATA / "source_native_readout_formula_endpoint_by_family.csv", index=False)
    shuffled.to_csv(DATA / "source_native_readout_formula_shuffled_null.csv", index=False)
    shuffled_summary.to_csv(DATA / "source_native_readout_formula_shuffled_null_summary.csv", index=False)
    write_report(labels, amplitudes, summary, by_family, shuffled_summary)
    print("PAPER8_SOURCE_NATIVE_READOUT_FORMULA_ENDPOINT_COMPLETE")


if __name__ == "__main__":
    main()
