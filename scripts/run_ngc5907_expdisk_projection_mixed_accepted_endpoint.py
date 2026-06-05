#!/usr/bin/env python3
"""Score the accepted NGC5907 exponential-disk + projection mixed endpoint."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "paper8_submission_source" / "figures"
CLAIM_BOUNDARY = "ngc5907_expdisk_projection_mixed_accepted_endpoint_preliminary_control"

sys.path.insert(0, str(ROOT / "scripts"))
import run_mixed_readout_population_control_audit as control  # noqa: E402
import run_mixed_readout_population_endpoint as endpoint  # noqa: E402


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    accepted_manifest = pd.read_csv(
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_manifest.csv"
    ).iloc[0]
    if not bool(accepted_manifest["endpoint_scores_allowed"]):
        raise RuntimeError("NGC5907 mixed accepted endpoint gate is not score-eligible")

    points = endpoint.build_generic_predictions()
    manifests = {
        "NGC4013": pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_manifest.csv").iloc[0],
        "NGC5907": accepted_manifest,
        "NGC7331": pd.read_csv(
            DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_formula_freeze_manifest.csv"
        ).iloc[0],
    }

    matched_points = endpoint.add_ngc5907_mixed(points, manifests["NGC5907"])
    wrong_4013 = control.apply_formula_to_galaxy(points, "NGC5907", "NGC4013", manifests["NGC4013"])
    wrong_7331 = control.apply_formula_to_galaxy(points, "NGC5907", "NGC7331", manifests["NGC7331"])

    matched_rmse = rmse(matched_points["vobs"], matched_points["v_mixed_population"])
    score_rows = [
        {
            "galaxy": "NGC5907",
            "model_id": "TAU_NGC5907_EXPDISK_PROJECTION_MIXED_ACCEPTED",
            "model_role": "matched_frozen_mixed_readout",
            "n_points": len(matched_points),
            "rmse_km_s": matched_rmse,
            "mae_km_s": float(
                np.mean(np.abs(matched_points["v_mixed_population"] - matched_points["vobs"]))
            ),
            "construction_used_vobs": False,
            "scoring_used_vobs": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC5907",
            "model_id": "NEWTONIAN_vn",
            "model_role": "baseline",
            "n_points": len(matched_points),
            "rmse_km_s": rmse(matched_points["vobs"], matched_points["vn"]),
            "mae_km_s": float(np.mean(np.abs(matched_points["vn"] - matched_points["vobs"]))),
            "construction_used_vobs": False,
            "scoring_used_vobs": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC5907",
            "model_id": "TPG_V6_v_v6",
            "model_role": "baseline",
            "n_points": len(matched_points),
            "rmse_km_s": rmse(matched_points["vobs"], matched_points["v_v6"]),
            "mae_km_s": float(np.mean(np.abs(matched_points["v_v6"] - matched_points["vobs"]))),
            "construction_used_vobs": False,
            "scoring_used_vobs": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC5907",
            "model_id": "MOND_v_mond",
            "model_role": "baseline",
            "n_points": len(matched_points),
            "rmse_km_s": rmse(matched_points["vobs"], matched_points["v_mond"]),
            "mae_km_s": float(
                np.mean(np.abs(matched_points["v_mond"] - matched_points["vobs"]))
            ),
            "construction_used_vobs": False,
            "scoring_used_vobs": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC5907",
            "model_id": "EXPONENTIAL_DISK_CARRIER",
            "model_role": "baseline",
            "n_points": len(matched_points),
            "rmse_km_s": rmse(
                matched_points["vobs"], matched_points["v_K_exponential_disk"]
            ),
            "mae_km_s": float(
                np.mean(
                    np.abs(matched_points["v_K_exponential_disk"] - matched_points["vobs"])
                )
            ),
            "construction_used_vobs": False,
            "scoring_used_vobs": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC5907",
            "model_id": "WRONG_MIXED_NGC4013_WVO",
            "model_role": "wrong_mixed_family_control",
            "n_points": len(wrong_4013),
            "rmse_km_s": rmse(wrong_4013["vobs"], wrong_4013["v_mixed_population"]),
            "mae_km_s": float(
                np.mean(np.abs(wrong_4013["v_mixed_population"] - wrong_4013["vobs"]))
            ),
            "construction_used_vobs": False,
            "scoring_used_vobs": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC5907",
            "model_id": "WRONG_MIXED_NGC7331_VOW",
            "model_role": "wrong_mixed_family_control",
            "n_points": len(wrong_7331),
            "rmse_km_s": rmse(wrong_7331["vobs"], wrong_7331["v_mixed_population"]),
            "mae_km_s": float(
                np.mean(np.abs(wrong_7331["v_mixed_population"] - wrong_7331["vobs"]))
            ),
            "construction_used_vobs": False,
            "scoring_used_vobs": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    scores = pd.DataFrame(score_rows).sort_values("rmse_km_s").reset_index(drop=True)

    baselines = scores.loc[scores["model_role"].eq("baseline")]
    wrong = scores.loc[scores["model_role"].eq("wrong_mixed_family_control")]
    summary = pd.DataFrame(
        [
            {
                "endpoint_status": "ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT",
                "galaxy": "NGC5907",
                "formula_id": str(accepted_manifest["formula_id"]),
                "n_points": len(matched_points),
                "rmse_mixed_accepted": matched_rmse,
                "best_baseline_model": str(baselines.sort_values("rmse_km_s")["model_id"].iloc[0]),
                "best_baseline_rmse_km_s": float(baselines["rmse_km_s"].min()),
                "wrong_mixed_mean_rmse_km_s": float(wrong["rmse_km_s"].mean()),
                "wrong_mixed_best_rmse_km_s": float(wrong["rmse_km_s"].min()),
                "matched_minus_best_baseline_rmse_km_s": matched_rmse
                - float(baselines["rmse_km_s"].min()),
                "matched_minus_wrong_mixed_mean_rmse_km_s": matched_rmse
                - float(wrong["rmse_km_s"].mean()),
                "matched_minus_best_wrong_mixed_rmse_km_s": matched_rmse
                - float(wrong["rmse_km_s"].min()),
                "matched_rank_among_all_models": int(
                    scores["rmse_km_s"].rank(method="min").loc[
                        scores["model_id"].eq(
                            "TAU_NGC5907_EXPDISK_PROJECTION_MIXED_ACCEPTED"
                        )
                    ].iloc[0]
                ),
                "matched_beats_all_baselines": bool(matched_rmse < baselines["rmse_km_s"].min()),
                "matched_beats_all_wrong_mixed_families": bool(
                    matched_rmse < wrong["rmse_km_s"].min()
                ),
                "previous_projection_endpoint_used_as_mixed_evidence": False,
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_scores_allowed": True,
                "claim_boundary": CLAIM_BOUNDARY,
                "claim_status": (
                    "accepted single-galaxy mixed control endpoint; not population validation"
                ),
            }
        ]
    )

    points_out = matched_points[
        [
            "galaxy",
            "r",
            "vobs",
            "errv",
            "vn",
            "v_v6",
            "v_mond",
            "v_K_exponential_disk",
            "mixed_kernel",
            "mixed_attenuation",
            "v_mixed_population",
        ]
    ].copy()
    points_out["endpoint_scores_allowed"] = True
    points_out["construction_used_vobs"] = False
    points_out["scoring_used_vobs"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    points_out.to_csv(
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_points.csv",
        index=False,
    )
    scores.to_csv(DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_scores.csv", index=False)
    summary.to_csv(
        DATA / "ngc5907_expdisk_projection_mixed_accepted_endpoint_summary.csv",
        index=False,
    )

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(7.2, 4.6))
        ax.errorbar(
            matched_points["r"],
            matched_points["vobs"],
            yerr=matched_points["errv"],
            fmt="o",
            color="black",
            label="observed",
        )
        ax.plot(matched_points["r"], matched_points["vn"], color="0.55", lw=1.5, label="Newtonian")
        ax.plot(matched_points["r"], matched_points["v_v6"], color="#356cb4", lw=1.8, label="TPG/v6")
        ax.plot(matched_points["r"], matched_points["v_mond"], color="#c43d3d", lw=1.8, label="MOND")
        ax.plot(
            matched_points["r"],
            matched_points["v_K_exponential_disk"],
            color="#4f9d5d",
            lw=1.8,
            label="exponential carrier",
        )
        ax.plot(
            matched_points["r"],
            matched_points["v_mixed_population"],
            color="#f28e2b",
            lw=2.8,
            label="accepted mixed readout",
        )
        ax.set_xlabel("R [kpc]")
        ax.set_ylabel("v [km/s]")
        ax.set_title("NGC5907 accepted mixed endpoint")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)
        fig.tight_layout()
        fig_path = FIGURES / "fig11_ngc5907_expdisk_projection_mixed_accepted_endpoint.png"
        fig.savefig(fig_path, dpi=180)
        plt.close(fig)
    except Exception as exc:  # pragma: no cover
        fig_path = None
        print(f"plotting skipped: {exc}")

    report = [
        "# NGC5907 Exponential-Disk + Projection Mixed Accepted Endpoint",
        "",
        "This run scores the frozen NGC5907 mixed endpoint protocol. The formula",
        "is read from the accepted endpoint manifest unchanged. Observed",
        "velocities enter only in the scoring block.",
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
        "This is an accepted single-galaxy mixed control endpoint. The earlier",
        "projection endpoint is not used as mixed-label evidence, and this result",
        "is not a population validation.",
        "",
    ]
    if fig_path is not None:
        report.extend(["## Figure", "", str(fig_path.relative_to(ROOT)), ""])
    (REPORTS / "ngc5907_expdisk_projection_mixed_accepted_endpoint.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
