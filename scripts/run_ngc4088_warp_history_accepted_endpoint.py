#!/usr/bin/env python3
"""Score the caveated accepted NGC4088 warp/history endpoint.

The frozen readout curve is read from
ngc4088_warp_history_formula_freeze_kernel_grid.csv.  Observed velocities are
used only in the scoring block after the accepted endpoint gate has passed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "paper8_submission_source" / "figures"
CLAIM_BOUNDARY = "ngc4088_warp_history_accepted_endpoint_preliminary_control"

sys.path.insert(0, str(ROOT / "scripts"))
import run_source_native_readout_formula_endpoint as src  # noqa: E402
import run_s4g75_promoted_kernel_endpoint_stress_test as promoted  # noqa: E402


def rmse(obs: pd.Series, pred: pd.Series) -> float:
    return float(np.sqrt(np.mean(np.square(pred.to_numpy() - obs.to_numpy()))))


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


def build_generic_predictions() -> pd.DataFrame:
    points, _labels = src.load_points()
    points = promoted.apply_promoted_observables(points)
    points = src.add_bridge_formula_kernels(points)
    amplitudes = src.fit_amplitudes(points)
    return src.add_predictions(points, amplitudes)


def score_row(points: pd.DataFrame, pred_col: str, label: str, role: str) -> dict[str, object]:
    residual = points[pred_col].astype(float) - points["vobs"].astype(float)
    inner = points[points["x_R_over_RHI"].astype(float) <= points["x_w_formula_freeze"].astype(float)]
    outer = points[points["x_R_over_RHI"].astype(float) > points["x_w_formula_freeze"].astype(float)]
    return {
        "galaxy": "NGC4088",
        "model_id": label,
        "model_role": role,
        "n_points": len(points),
        "rmse_km_s": rmse(points["vobs"], points[pred_col]),
        "mae_km_s": float(np.mean(np.abs(residual))),
        "bias_km_s": float(np.mean(residual)),
        "inner_rmse_km_s": rmse(inner["vobs"], inner[pred_col]) if len(inner) else np.nan,
        "outer_rmse_km_s": rmse(outer["vobs"], outer[pred_col]) if len(outer) else np.nan,
        "construction_used_vobs": False,
        "scoring_used_vobs": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(DATA / "ngc4088_warp_history_accepted_endpoint_manifest.csv").iloc[0]
    if not bool(manifest["endpoint_scores_allowed"]):
        raise RuntimeError("NGC4088 accepted endpoint gate is not score-eligible")

    frozen = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_kernel_grid.csv")
    if "vobs" in frozen.columns:
        raise RuntimeError("frozen kernel grid must not contain vobs")
    profile = pd.read_csv(DATA / "s4g75_ngc4088_readout_preflight_profile.csv")
    generic = build_generic_predictions()
    generic = generic.loc[generic["galaxy"].eq("NGC4088")].copy()

    points = profile[
        ["galaxy", "split", "r", "x_R_over_RHI", "vobs", "vn", "v_v6", "v_mond"]
    ].merge(
        frozen[
            [
                "r_kpc",
                "x_w_formula_freeze",
                "kernel_warp_history",
                "lambda_w_km2_s2",
                "delta_v2_warp_history_km2_s2",
                "v_warp_history_formula_freeze_km_s",
            ]
        ],
        left_on="r",
        right_on="r_kpc",
        how="inner",
        validate="one_to_one",
    )
    points = points.merge(
        generic[
            [
                "r",
                "v_K_compact_finite",
                "v_K_scale_tail_spiral",
                "v_K_exponential_disk",
                "v_K_thick_flared",
            ]
        ],
        on="r",
        how="left",
        validate="one_to_one",
    )
    points = points.sort_values("r").reset_index(drop=True)

    score_specs = [
        ("vn", "NEWTONIAN_vn", "baseline"),
        ("v_v6", "TPG_V6_v_v6", "baseline"),
        ("v_mond", "MOND_v_mond", "baseline"),
        ("v_K_compact_finite", "WRONG_K_compact_finite", "wrong_family_control"),
        ("v_K_scale_tail_spiral", "WRONG_K_scale_tail_spiral", "wrong_family_control"),
        ("v_K_exponential_disk", "WRONG_K_exponential_disk", "wrong_family_control"),
        ("v_K_thick_flared", "WRONG_K_thick_flared", "wrong_family_control"),
        (
            "v_warp_history_formula_freeze_km_s",
            "TAU_NGC4088_WARP_HISTORY_ACCEPTED",
            "matched_frozen_readout",
        ),
    ]
    scores = pd.DataFrame(
        [score_row(points, pred_col, label, role) for pred_col, label, role in score_specs]
    ).sort_values("rmse_km_s")

    matched_rmse = float(
        scores.loc[
            scores["model_id"].eq("TAU_NGC4088_WARP_HISTORY_ACCEPTED"), "rmse_km_s"
        ].iloc[0]
    )
    wrong = scores[scores["model_role"].eq("wrong_family_control")]
    baselines = scores[scores["model_role"].eq("baseline")]
    summary = pd.DataFrame(
        [
            {
                "endpoint_status": "CAVEATED_ACCEPTED_ENDPOINT_PRELIMINARY_CONTROL_RESULT",
                "galaxy": "NGC4088",
                "formula_id": str(manifest["formula_id"]),
                "n_points": len(points),
                "rmse_warp_history_accepted": matched_rmse,
                "best_baseline_model": str(baselines.sort_values("rmse_km_s")["model_id"].iloc[0]),
                "best_baseline_rmse_km_s": float(baselines["rmse_km_s"].min()),
                "wrong_family_mean_rmse_km_s": float(wrong["rmse_km_s"].mean()),
                "wrong_family_best_rmse_km_s": float(wrong["rmse_km_s"].min()),
                "matched_minus_best_baseline_rmse_km_s": matched_rmse
                - float(baselines["rmse_km_s"].min()),
                "matched_minus_wrong_family_mean_rmse_km_s": matched_rmse
                - float(wrong["rmse_km_s"].mean()),
                "matched_minus_best_wrong_family_rmse_km_s": matched_rmse
                - float(wrong["rmse_km_s"].min()),
                "matched_rank_among_all_models": int(
                    scores["rmse_km_s"].rank(method="min").loc[
                        scores["model_id"].eq("TAU_NGC4088_WARP_HISTORY_ACCEPTED")
                    ].iloc[0]
                ),
                "matched_beats_all_baselines": bool(matched_rmse < baselines["rmse_km_s"].min()),
                "matched_beats_all_wrong_families": bool(matched_rmse < wrong["rmse_km_s"].min()),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_scores_allowed": True,
                "claim_boundary": CLAIM_BOUNDARY,
                "claim_status": "single-galaxy caveated control endpoint; not population validation",
            }
        ]
    )

    points_out = points.copy()
    for col in [
        "vn",
        "v_v6",
        "v_mond",
        "v_K_compact_finite",
        "v_K_scale_tail_spiral",
        "v_K_exponential_disk",
        "v_K_thick_flared",
        "v_warp_history_formula_freeze_km_s",
    ]:
        points_out[f"residual_{col}"] = points_out[col].astype(float) - points_out[
            "vobs"
        ].astype(float)
    points_out["construction_used_vobs"] = False
    points_out["scoring_used_vobs"] = True
    points_out["endpoint_scores_allowed"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    points_out.to_csv(DATA / "ngc4088_warp_history_accepted_endpoint_points.csv", index=False)
    scores.to_csv(DATA / "ngc4088_warp_history_accepted_endpoint_scores.csv", index=False)
    summary.to_csv(DATA / "ngc4088_warp_history_accepted_endpoint_summary.csv", index=False)

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(7.2, 4.6))
        ax.scatter(points["r"], points["vobs"], color="black", s=34, label="observed", zorder=10)
        ax.plot(points["r"], points["vn"], color="0.55", lw=1.5, label="Newtonian baryonic")
        ax.plot(points["r"], points["v_v6"], color="#356cb4", lw=1.6, label="TPG/v6 proxy")
        ax.plot(points["r"], points["v_mond"], color="#c43d3d", lw=1.6, label="MOND proxy")
        ax.plot(
            points["r"],
            points["v_K_exponential_disk"],
            color="#9467bd",
            lw=1.5,
            ls="--",
            label="wrong-family expdisk",
        )
        ax.plot(
            points["r"],
            points["v_warp_history_formula_freeze_km_s"],
            color="#f28e2b",
            lw=2.8,
            label="frozen warp/history readout",
        )
        ax.axvline(
            float(manifest["x_w_formula_freeze"]) * max(points["r"] / points["x_R_over_RHI"]),
            color="#f28e2b",
            alpha=0.25,
            lw=1.2,
            label="frozen onset",
        )
        ax.set_xlabel("R [kpc]")
        ax.set_ylabel("v [km/s]")
        ax.set_title("NGC4088 caveated accepted warp/history endpoint")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)
        fig.tight_layout()
        fig_path = FIGURES / "fig10_ngc4088_warp_history_accepted_endpoint.png"
        fig.savefig(fig_path, dpi=180)
        plt.close(fig)
    except Exception as exc:  # pragma: no cover
        fig_path = None
        print(f"plotting skipped: {exc}")

    report = [
        "# NGC4088 Warp/History Accepted Endpoint",
        "",
        "This run scores the caveated accepted NGC4088 warp/history endpoint from",
        "the unchanged frozen formula-freeze manifest. Observed velocities are read",
        "only in this scoring script.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Claim Boundary",
        "",
        "This is a single-galaxy caveated preliminary control endpoint. It is not a",
        "population validation and it does not close the B2/B3 law-level caveats.",
        "",
    ]
    if fig_path is not None:
        report.extend(["## Figure", "", str(fig_path.relative_to(ROOT)), ""])
    (REPORTS / "ngc4088_warp_history_accepted_endpoint.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
