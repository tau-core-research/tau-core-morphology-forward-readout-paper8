#!/usr/bin/env python3
"""Build a multi-galaxy endpoint fit-inspection atlas.

This diagnostic reuses the existing source-native bridge-formula pipeline and
selects galaxies with available SPARC rotation points plus morphology-manifest
inputs. It scores against vobs, so it is an endpoint diagnostic only.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
sys.path.insert(0, str(ROOT / "scripts"))
import run_source_native_readout_formula_endpoint as src  # noqa: E402


CLAIM_BOUNDARY = "multigalaxy_fit_inspection_atlas_endpoint_diagnostic_not_validation"
SELECTED_GALAXIES = [
    "IC2574",
    "UGC05716",
    "NGC4183",
    "UGC12506",
    "IC4202",
    "NGC4013",
    "NGC5907",
    "NGC7331",
    "NGC4088",
]
MODEL_COLUMNS = {
    "NEWTONIAN_vn": "vn",
    "TPG_V6": "v_v6",
    "MOND": "v_mond",
}
MODEL_COLORS = {
    "NEWTONIAN_vn": "#555555",
    "TPG_V6": "#1f77b4",
    "MOND": "#d62728",
    "TAU_MATCHED": "#2ca02c",
    "TAU_BEST_FAMILY": "#ff7f0e",
}


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def rmse(values: pd.Series, observed: pd.Series) -> float:
    residual = values.astype(float) - observed.astype(float)
    return float(np.sqrt(np.mean(residual**2)))


def mae(values: pd.Series, observed: pd.Series) -> float:
    residual = values.astype(float) - observed.astype(float)
    return float(np.mean(np.abs(residual)))


def build_scored_points() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    points, labels = src.load_points()
    points = src.add_bridge_formula_kernels(points)
    amplitudes = src.fit_amplitudes(points)
    scored = src.add_predictions(points, amplitudes)
    return scored, labels, amplitudes


def add_long_point_rows(scored: pd.DataFrame, galaxies: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for galaxy in galaxies:
        sub = scored[scored["galaxy"] == galaxy].sort_values("r")
        if sub.empty:
            continue
        matched_family = str(sub["formula_family"].iloc[0])
        family_scores = {
            family: rmse(sub[f"v_{family}"], sub["vobs"])
            for family in src.FORMULA_FAMILIES
        }
        best_family = min(src.FORMULA_FAMILIES, key=lambda family: family_scores[family])
        model_map = {
            **MODEL_COLUMNS,
            "TAU_MATCHED": f"v_{matched_family}",
            "TAU_BEST_FAMILY": f"v_{best_family}",
        }
        for model_id, column in model_map.items():
            for _, row in sub.iterrows():
                rows.append(
                    {
                        "galaxy": galaxy,
                        "split": row["split"],
                        "formula_family": matched_family,
                        "best_family": best_family,
                        "model_id": model_id,
                        "prediction_column": column,
                        "r_kpc": float(row["r"]),
                        "vobs_kms": float(row["vobs"]),
                        "vpred_kms": float(row[column]),
                        "residual_kms": float(row[column] - row["vobs"]),
                        "uses_vobs_for_generation": False,
                        "uses_vobs_for_scoring": True,
                        "validation_claim_allowed": False,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return pd.DataFrame(rows)


def build_scores(points_long: pd.DataFrame, labels: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    score_rows = []
    for (galaxy, model_id), sub in points_long.groupby(["galaxy", "model_id"]):
        residual = sub["vpred_kms"].astype(float) - sub["vobs_kms"].astype(float)
        score_rows.append(
            {
                "galaxy": galaxy,
                "model_id": model_id,
                "split": sub["split"].iloc[0],
                "formula_family": sub["formula_family"].iloc[0],
                "best_family": sub["best_family"].iloc[0],
                "n_points": int(len(sub)),
                "rmse_kms": float(np.sqrt(np.mean(residual**2))),
                "mae_kms": float(np.mean(np.abs(residual))),
                "bias_kms": float(np.mean(residual)),
                "uses_vobs_for_generation": False,
                "uses_vobs_for_scoring": True,
                "validation_claim_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    scores = pd.DataFrame(score_rows)
    matched = scores[scores["model_id"] == "TAU_MATCHED"][
        ["galaxy", "rmse_kms"]
    ].rename(columns={"rmse_kms": "rmse_tau_matched"})
    baseline_best = (
        scores[scores["model_id"].isin(["NEWTONIAN_vn", "TPG_V6", "MOND"])]
        .sort_values("rmse_kms")
        .groupby("galaxy")
        .first()
        .reset_index()[["galaxy", "model_id", "rmse_kms"]]
        .rename(columns={"model_id": "best_baseline_model", "rmse_kms": "rmse_best_baseline"})
    )
    best_any = (
        scores.sort_values("rmse_kms")
        .groupby("galaxy")
        .first()
        .reset_index()[["galaxy", "model_id", "rmse_kms"]]
        .rename(columns={"model_id": "best_overall_model", "rmse_kms": "rmse_best_overall"})
    )
    availability_columns = [
        "galaxy",
        "formula_family",
        "manifest_confidence",
        "manifest_caveat",
        "type_bin",
        "inc_bin",
        "distance_quality",
        "inclination_deg",
        "n_points",
    ]
    availability = labels[labels["galaxy"].isin(SELECTED_GALAXIES)][availability_columns].copy()
    availability["has_sparc_rotation_points"] = availability["n_points"].astype(int) > 0
    availability["has_morphology_manifest_row"] = True
    availability["endpoint_scores_allowed_for_validation"] = False
    availability["claim_boundary"] = CLAIM_BOUNDARY
    summary = (
        availability.merge(matched, on="galaxy", how="left")
        .merge(baseline_best, on="galaxy", how="left")
        .merge(best_any, on="galaxy", how="left")
    )
    summary["tau_matched_minus_best_baseline_rmse"] = (
        summary["rmse_tau_matched"] - summary["rmse_best_baseline"]
    )
    summary["tau_matched_beats_best_baseline"] = (
        summary["tau_matched_minus_best_baseline_rmse"] < 0
    )
    return scores.sort_values(["galaxy", "rmse_kms"]), summary.sort_values("galaxy")


def plot_atlas(points_long: pd.DataFrame, summary: pd.DataFrame) -> Path:
    figure_path = REPORTS / "multigalaxy_fit_inspection_atlas.png"
    n = len(summary)
    ncols = 3
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 4.2 * nrows), squeeze=False)
    for ax, (_, row) in zip(axes.flat, summary.iterrows(), strict=False):
        galaxy = row["galaxy"]
        sub = points_long[points_long["galaxy"] == galaxy].sort_values(["model_id", "r_kpc"])
        observed = sub[sub["model_id"] == "NEWTONIAN_vn"].sort_values("r_kpc")
        ax.scatter(observed["r_kpc"], observed["vobs_kms"], color="black", s=22, label="Observed", zorder=10)
        for model_id, label, style in [
            ("NEWTONIAN_vn", "Newtonian", "--"),
            ("TPG_V6", "TPG/v6", ":"),
            ("MOND", "MOND", ":"),
            ("TAU_MATCHED", "Tau matched", "-"),
            ("TAU_BEST_FAMILY", "Tau best family", "-"),
        ]:
            model = sub[sub["model_id"] == model_id].sort_values("r_kpc")
            if model.empty:
                continue
            lw = 2.4 if model_id in {"TAU_MATCHED", "TAU_BEST_FAMILY"} else 1.5
            alpha = 0.85 if model_id != "TAU_BEST_FAMILY" else 0.95
            ax.plot(
                model["r_kpc"],
                model["vpred_kms"],
                linestyle=style,
                color=MODEL_COLORS[model_id],
                linewidth=lw,
                alpha=alpha,
                label=label,
            )
        title = f"{galaxy}: {row['formula_family']}"
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("r [kpc]")
        ax.set_ylabel("v [km/s]")
        ax.grid(alpha=0.2)
    for ax in axes.flat[n:]:
        ax.axis("off")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=6, fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)
    return figure_path


def write_report(summary: pd.DataFrame, scores: pd.DataFrame, figure_path: Path) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    ngc4088_warp_summary_path = DATA / "s4g75_ngc4088_endpoint_fit_diagnostic_summary.csv"
    ngc4088_warp_note = []
    if ngc4088_warp_summary_path.exists():
        warp = pd.read_csv(ngc4088_warp_summary_path).iloc[0]
        ngc4088_warp_note = [
            "## NGC4088 Warp/History Cross-Check",
            "",
            "NGC4088 is intentionally included as a stress case. In the generic",
            "source-native family atlas it is treated as the current thick/flared",
            "proxy row, and that generic row is not the good fit. The separate",
            "targeted warp/history diagnostic is different: it uses the source-built",
            "warp branches p1/p2 and the bounded epsilon_cross modulation.",
            "",
            markdown_table(
                pd.DataFrame(
                    [
                        {
                            "galaxy": "NGC4088",
                            "generic_family_atlas_tau_rmse": float(
                                summary.loc[
                                    summary["galaxy"] == "NGC4088",
                                    "rmse_tau_matched",
                                ].iloc[0]
                            ),
                            "targeted_warp_fixed_tau_rmse": float(
                                warp["best_fixed_tau_rmse_kms"]
                            ),
                            "targeted_warp_bounded_tau_rmse": float(
                                warp["best_bounded_tau_rmse_kms"]
                            ),
                            "interpretation": "correct_readout_subfamily_matters",
                        }
                    ]
                )
            ),
            "",
        ]
    overview = pd.DataFrame(
        [
            {
                "diagnostic_id": "MULTIGALAXY_FIT_INSPECTION_ATLAS",
                "n_selected_galaxies": int(summary["galaxy"].nunique()),
                "n_families": int(summary["formula_family"].nunique()),
                "n_tau_matched_beats_best_baseline": int(summary["tau_matched_beats_best_baseline"].sum()),
                "selection_policy": "predeclared_diverse_available_data_examples_plus_stress_cases",
                "uses_vobs_for_generation": False,
                "uses_vobs_for_scoring": True,
                "validation_claim_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    score_pivot = scores.pivot_table(
        index="galaxy", columns="model_id", values="rmse_kms", aggfunc="first"
    ).reset_index()
    lines = [
        "# Multi-Galaxy Fit Inspection Atlas",
        "",
        "This diagnostic inspects several galaxies with available SPARC rotation",
        "points and morphology-manifest inputs. It reuses the source-native bridge",
        "formula pipeline and scores against observed rotation curves. It is an",
        "endpoint diagnostic only, not a validation endpoint.",
        "",
        "## Overview",
        "",
        markdown_table(overview),
        "",
        "## Atlas",
        "",
        f"![Multi-galaxy fit inspection atlas]({figure_path})",
        "",
        "## Selected Galaxies and Availability",
        "",
        markdown_table(
            summary[
                [
                    "galaxy",
                    "formula_family",
                    "type_bin",
                    "inc_bin",
                    "manifest_confidence",
                    "manifest_caveat",
                    "n_points",
                    "best_baseline_model",
                    "tau_matched_beats_best_baseline",
                ]
            ]
        ),
        "",
        "## RMSE by Model",
        "",
        markdown_table(score_pivot),
        "",
        *ngc4088_warp_note,
        "## Claim Boundary",
        "",
        "The selected set deliberately mixes encouraging rows and stress rows.",
        "The diagnostic answers whether the current executable readout curves look",
        "plausible across varied available-data cases. It does not prove population",
        "superiority over TPG/MOND/Newton and does not replace the frozen endpoint",
        "protocol.",
        "",
    ]
    (REPORTS / "multigalaxy_fit_inspection_atlas.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    scored, labels, amplitudes = build_scored_points()
    missing = sorted(set(SELECTED_GALAXIES) - set(scored["galaxy"].unique()))
    if missing:
        raise SystemExit(f"selected galaxies missing from scored points: {missing}")
    points_long = add_long_point_rows(scored, SELECTED_GALAXIES)
    scores, summary = build_scores(points_long, labels)
    figure_path = plot_atlas(points_long, summary)
    points_long.to_csv(DATA / "multigalaxy_fit_inspection_points.csv", index=False)
    scores.to_csv(DATA / "multigalaxy_fit_inspection_scores.csv", index=False)
    summary.to_csv(DATA / "multigalaxy_fit_inspection_summary.csv", index=False)
    amplitudes.to_csv(DATA / "multigalaxy_fit_inspection_amplitudes.csv", index=False)
    write_report(summary, scores, figure_path)
    print(summary.to_string(index=False))
    print(scores.head(30).to_string(index=False))


if __name__ == "__main__":
    main()
