#!/usr/bin/env python3
"""Endpoint fit diagnostic for the NGC4088 Tau Core readout preflight profile.

This script intentionally scores against observed velocities. It is therefore
an endpoint diagnostic, not a source-bound derivation or validation claim.
The generated Tau candidates are read from the residual-blind preflight table.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_endpoint_fit_diagnostic_not_validation"
OUTER_THRESHOLD = 0.5


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


def score_points(points: pd.DataFrame) -> dict[str, float | int]:
    residual = points["vpred_kms"].astype(float) - points["vobs_kms"].astype(float)
    outer = points[points["x_R_over_RHI"].astype(float) >= OUTER_THRESHOLD]
    inner = points[points["x_R_over_RHI"].astype(float) < OUTER_THRESHOLD]
    outer_residual = outer["vpred_kms"].astype(float) - outer["vobs_kms"].astype(float)
    inner_residual = inner["vpred_kms"].astype(float) - inner["vobs_kms"].astype(float)
    return {
        "n_points": int(len(points)),
        "n_inner_points": int(len(inner)),
        "n_outer_points": int(len(outer)),
        "rmse_kms": float(np.sqrt(np.mean(residual**2))),
        "mae_kms": float(np.mean(np.abs(residual))),
        "bias_kms": float(np.mean(residual)),
        "inner_rmse_kms": float(np.sqrt(np.mean(inner_residual**2))) if len(inner) else np.nan,
        "outer_rmse_kms": float(np.sqrt(np.mean(outer_residual**2))) if len(outer) else np.nan,
    }


def velocity_from_delta(profile: pd.DataFrame, branch_id: str, multiplier: float) -> pd.Series:
    delta_column = f"delta_v2_warp_candidate_{branch_id}"
    v2 = profile["vn"].astype(float) ** 2 + profile[delta_column].astype(float) * multiplier
    return np.sqrt(np.maximum(v2, 0.0))


def add_model_points(
    rows: list[dict[str, object]],
    profile: pd.DataFrame,
    *,
    model_id: str,
    model_family: str,
    vpred: pd.Series,
    branch_id: str = "",
    epsilon_cross: float | None = None,
    lambda_multiplier: float | None = None,
    scenario_role: str,
    endpoint_selected: bool,
) -> None:
    for _, row in profile.iterrows():
        rows.append(
            {
                "galaxy": GALAXY,
                "model_id": model_id,
                "model_family": model_family,
                "branch_id": branch_id,
                "epsilon_cross": epsilon_cross,
                "lambda_multiplier": lambda_multiplier,
                "scenario_role": scenario_role,
                "endpoint_selected": endpoint_selected,
                "r_kpc": float(row["r"]),
                "x_R_over_RHI": float(row["x_R_over_RHI"]),
                "vobs_kms": float(row["vobs"]),
                "vpred_kms": float(vpred.loc[row.name]),
                "residual_kms": float(vpred.loc[row.name] - row["vobs"]),
                "uses_vobs_for_generation": False,
                "uses_vobs_for_scoring": True,
                "validation_claim_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )


def build_endpoint_diagnostic() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    profile = pd.read_csv(DATA / "s4g75_ngc4088_readout_preflight_profile.csv")
    scenarios = pd.read_csv(DATA / "s4g75_ngc4088_epsilon_cross_readout_sensitivity_scenarios.csv")
    profile = profile.reset_index(drop=True)

    point_rows: list[dict[str, object]] = []
    add_model_points(
        point_rows,
        profile,
        model_id="NEWTONIAN_vn",
        model_family="Newtonian",
        vpred=profile["vn"].astype(float),
        scenario_role="baseline",
        endpoint_selected=False,
    )
    add_model_points(
        point_rows,
        profile,
        model_id="TPG_V6_v_v6",
        model_family="TPG_v6_proxy",
        vpred=profile["v_v6"].astype(float),
        scenario_role="baseline",
        endpoint_selected=False,
    )
    add_model_points(
        point_rows,
        profile,
        model_id="MOND_v_mond",
        model_family="MOND_proxy",
        vpred=profile["v_mond"].astype(float),
        scenario_role="baseline",
        endpoint_selected=False,
    )

    for branch_id in ["p1", "p2"]:
        add_model_points(
            point_rows,
            profile,
            model_id=f"TAU_WARP_{branch_id}_eps0",
            model_family="TauCore_warp_preflight",
            branch_id=branch_id,
            epsilon_cross=0.0,
            lambda_multiplier=1.0,
            vpred=velocity_from_delta(profile, branch_id, 1.0),
            scenario_role="predeclared_fixed_epsilon_zero",
            endpoint_selected=False,
        )

    for _, scenario in scenarios.iterrows():
        branch_id = str(scenario["branch_id"])
        epsilon = float(scenario["epsilon_cross_scenario"])
        multiplier = float(scenario["lambda_multiplier"])
        model_id = f"TAU_WARP_{branch_id}_eps_{epsilon:+.6f}"
        if abs(epsilon) < 1e-12:
            continue
        add_model_points(
            point_rows,
            profile,
            model_id=model_id,
            model_family="TauCore_warp_bounded_sensitivity",
            branch_id=branch_id,
            epsilon_cross=epsilon,
            lambda_multiplier=multiplier,
            vpred=velocity_from_delta(profile, branch_id, multiplier),
            scenario_role="bounded_epsilon_cross_sensitivity",
            endpoint_selected=False,
        )

    points = pd.DataFrame(point_rows)
    score_rows = []
    group_columns = [
        "model_id",
        "model_family",
        "branch_id",
        "epsilon_cross",
        "lambda_multiplier",
        "scenario_role",
        "endpoint_selected",
    ]
    for group_values, model_points in points.groupby(group_columns, dropna=False):
        row = dict(zip(group_columns, group_values, strict=True))
        row.update(score_points(model_points))
        row["uses_vobs_for_generation"] = False
        row["uses_vobs_for_scoring"] = True
        row["validation_claim_allowed"] = False
        row["claim_boundary"] = CLAIM_BOUNDARY
        score_rows.append(row)
    scores = pd.DataFrame(score_rows).sort_values("rmse_kms").reset_index(drop=True)

    tau_scores = scores[scores["model_family"].astype(str).str.startswith("TauCore")].copy()
    fixed_tau = tau_scores[tau_scores["scenario_role"] == "predeclared_fixed_epsilon_zero"].copy()
    baselines = scores[scores["scenario_role"] == "baseline"].copy()
    best_tau_any = tau_scores.sort_values("rmse_kms").iloc[0]
    best_tau_fixed = fixed_tau.sort_values("rmse_kms").iloc[0]
    best_baseline = baselines.sort_values("rmse_kms").iloc[0]
    newton = scores[scores["model_id"] == "NEWTONIAN_vn"].iloc[0]
    tpg = scores[scores["model_id"] == "TPG_V6_v_v6"].iloc[0]
    mond = scores[scores["model_id"] == "MOND_v_mond"].iloc[0]

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "diagnostic_id": "NGC4088_ENDPOINT_FIT_DIAGNOSTIC",
                "n_points": int(len(profile)),
                "outer_threshold_x_R_over_RHI": OUTER_THRESHOLD,
                "best_baseline_model": best_baseline["model_id"],
                "best_baseline_rmse_kms": float(best_baseline["rmse_kms"]),
                "best_fixed_tau_model": best_tau_fixed["model_id"],
                "best_fixed_tau_rmse_kms": float(best_tau_fixed["rmse_kms"]),
                "fixed_tau_minus_best_baseline_rmse_kms": float(
                    best_tau_fixed["rmse_kms"] - best_baseline["rmse_kms"]
                ),
                "best_bounded_tau_model": best_tau_any["model_id"],
                "best_bounded_tau_rmse_kms": float(best_tau_any["rmse_kms"]),
                "bounded_tau_minus_best_baseline_rmse_kms": float(
                    best_tau_any["rmse_kms"] - best_baseline["rmse_kms"]
                ),
                "newton_rmse_kms": float(newton["rmse_kms"]),
                "tpg_v6_rmse_kms": float(tpg["rmse_kms"]),
                "mond_rmse_kms": float(mond["rmse_kms"]),
                "fixed_tau_beats_newton": bool(best_tau_fixed["rmse_kms"] < newton["rmse_kms"]),
                "fixed_tau_beats_tpg_v6": bool(best_tau_fixed["rmse_kms"] < tpg["rmse_kms"]),
                "fixed_tau_beats_mond": bool(best_tau_fixed["rmse_kms"] < mond["rmse_kms"]),
                "bounded_tau_beats_newton": bool(best_tau_any["rmse_kms"] < newton["rmse_kms"]),
                "bounded_tau_beats_tpg_v6": bool(best_tau_any["rmse_kms"] < tpg["rmse_kms"]),
                "bounded_tau_beats_mond": bool(best_tau_any["rmse_kms"] < mond["rmse_kms"]),
                "endpoint_selected_best_is_diagnostic_only": True,
                "uses_vobs_for_generation": False,
                "uses_vobs_for_scoring": True,
                "validation_claim_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return points, scores, summary


def write_report(points: pd.DataFrame, scores: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    figure_path = REPORTS / "s4g75_ngc4088_endpoint_fit_diagnostic.png"
    selected_columns = [
        "model_id",
        "scenario_role",
        "rmse_kms",
        "mae_kms",
        "bias_kms",
        "inner_rmse_kms",
        "outer_rmse_kms",
    ]
    profile_columns = [
        "model_id",
        "r_kpc",
        "x_R_over_RHI",
        "vobs_kms",
        "vpred_kms",
        "residual_kms",
    ]
    fixed_rows = scores[
        scores["scenario_role"].isin(["baseline", "predeclared_fixed_epsilon_zero"])
    ].sort_values("rmse_kms")
    best_tau_id = str(summary.iloc[0]["best_bounded_tau_model"])
    best_tau_points = points[points["model_id"] == best_tau_id].copy()
    plot_models(points, best_tau_id, figure_path)
    lines = [
        "# NGC4088 Endpoint Fit Diagnostic",
        "",
        "This diagnostic scores generated readout profiles against the observed",
        "rotation curve. It is useful for fit inspection, but it is not a",
        "source-bound derivation and does not authorize a validation claim.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Figure",
        "",
        f"![NGC4088 endpoint fit diagnostic]({figure_path})",
        "",
        "## Fixed Models",
        "",
        markdown_table(fixed_rows[selected_columns]),
        "",
        "## Bounded Tau Sensitivity Scores",
        "",
        markdown_table(scores[scores["model_family"].astype(str).str.startswith("TauCore")][selected_columns]),
        "",
        "## Best Bounded Tau Profile",
        "",
        markdown_table(best_tau_points[profile_columns]),
        "",
        "## Claim Boundary",
        "",
        "The bounded Tau best row is endpoint-selected from predeclared sensitivity",
        "scenarios. It is a diagnostic of where the generated morphology readout can",
        "move the curve, not proof that the galaxy validates Tau Core.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_endpoint_fit_diagnostic.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def plot_models(points: pd.DataFrame, best_tau_id: str, figure_path: Path) -> None:
    model_order = [
        ("NEWTONIAN_vn", "Newtonian", "#444444", "--"),
        ("TPG_V6_v_v6", "TPG/v6", "#1f77b4", ":"),
        ("MOND_v_mond", "MOND", "#d62728", ":"),
        ("TAU_WARP_p1_eps0", "Tau p1 fixed", "#2ca02c", "-"),
        ("TAU_WARP_p2_eps0", "Tau p2 fixed", "#9467bd", "-"),
        (best_tau_id, "Tau bounded best", "#ff7f0e", "-"),
    ]
    first_model = points[points["model_id"] == "NEWTONIAN_vn"].sort_values("r_kpc")
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.scatter(
        first_model["r_kpc"],
        first_model["vobs_kms"],
        color="black",
        s=34,
        label="Observed",
        zorder=10,
    )
    for model_id, label, color, linestyle in model_order:
        model_points = points[points["model_id"] == model_id].sort_values("r_kpc")
        if model_points.empty:
            continue
        linewidth = 2.6 if model_id == best_tau_id else 1.8
        ax.plot(
            model_points["r_kpc"],
            model_points["vpred_kms"],
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
            label=label,
        )
    ax.set_title("NGC4088 endpoint fit diagnostic")
    ax.set_xlabel("r [kpc]")
    ax.set_ylabel("circular speed [km/s]")
    ax.grid(alpha=0.25)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    points, scores, summary = build_endpoint_diagnostic()
    points.to_csv(DATA / "s4g75_ngc4088_endpoint_fit_diagnostic_points.csv", index=False)
    scores.to_csv(DATA / "s4g75_ngc4088_endpoint_fit_diagnostic_scores.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_endpoint_fit_diagnostic_summary.csv", index=False)
    write_report(points, scores, summary)
    print(summary.to_string(index=False))
    print(scores.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
