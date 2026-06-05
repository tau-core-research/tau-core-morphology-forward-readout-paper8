#!/usr/bin/env python3
"""Run diagnostic NGC4013 exponential-disk + warp/vertical-overlay readout."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "paper8_submission_source" / "figures"
CLAIM_BOUNDARY = "ngc4013_expdisk_warp_vertical_overlay_diagnostic_not_endpoint"

sys.path.insert(0, str(ROOT / "scripts"))
import run_ngc4013_warp_vertical_overlay_endpoint as wvo  # noqa: E402


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


def add_mixed_diagnostic(points: pd.DataFrame, manifest: pd.Series) -> pd.DataFrame:
    """Apply the frozen overlay kernel to the exponential-disk carrier."""
    sub = wvo.add_warp_vertical_overlay_readout(points, manifest)
    v2_exp = sub["v_K_exponential_disk"].to_numpy(dtype=float) ** 2
    attenuation = sub["wvo_attenuation"].to_numpy(dtype=float)
    v2_mixed = np.maximum(v2_exp * (1.0 - attenuation), 0.0)
    sub["delta_v2_expdisk_wvo"] = v2_mixed - v2_exp
    sub["v_expdisk_wvo_diagnostic"] = np.sqrt(v2_mixed)
    return sub


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    hypothesis = pd.read_csv(DATA / "ngc4013_expdisk_wvo_hypothesis_summary.csv").iloc[0]
    if not bool(hypothesis["diagnostic_scores_allowed"]):
        raise RuntimeError("mixed NGC4013 diagnostic gate is not diagnostic-score eligible")

    manifest = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_manifest.csv").iloc[0]
    points = add_mixed_diagnostic(wvo.build_generic_promoted_predictions(), manifest)

    scores = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "n_points": len(points),
                "rmse_newton": rmse(points["vobs"], points["vn"]),
                "rmse_tpg_v6": rmse(points["vobs"], points["v_v6"]),
                "rmse_mond": rmse(points["vobs"], points["v_mond"]),
                "rmse_exponential_disk": rmse(points["vobs"], points["v_K_exponential_disk"]),
                "rmse_warp_vertical_overlay": rmse(points["vobs"], points["v_wvo_endpoint"]),
                "rmse_expdisk_wvo_diagnostic": rmse(
                    points["vobs"], points["v_expdisk_wvo_diagnostic"]
                ),
                "mixed_minus_expdisk": rmse(points["vobs"], points["v_expdisk_wvo_diagnostic"])
                - rmse(points["vobs"], points["v_K_exponential_disk"]),
                "mixed_minus_wvo": rmse(points["vobs"], points["v_expdisk_wvo_diagnostic"])
                - rmse(points["vobs"], points["v_wvo_endpoint"]),
                "mixed_minus_tpg_v6": rmse(points["vobs"], points["v_expdisk_wvo_diagnostic"])
                - rmse(points["vobs"], points["v_v6"]),
                "formula_id": "NGC4013_EXPDISK_WVO_DIAGNOSTIC_V1",
                "overlay_formula_id": str(manifest["formula_id"]),
                "diagnostic_status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
                "endpoint_scores_allowed": False,
                "diagnostic_scores_allowed": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    points_out = points[
        [
            "galaxy",
            "r",
            "vobs",
            "errv",
            "vn",
            "v_v6",
            "v_mond",
            "v_K_exponential_disk",
            "v_wvo_endpoint",
            "K_wvo",
            "wvo_attenuation",
            "delta_v2_expdisk_wvo",
            "v_expdisk_wvo_diagnostic",
        ]
    ].copy()
    points_out["endpoint_scores_allowed"] = False
    points_out["diagnostic_scores_allowed"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    scores.to_csv(DATA / "ngc4013_expdisk_wvo_diagnostic_scores.csv", index=False)
    points_out.to_csv(DATA / "ngc4013_expdisk_wvo_diagnostic_points.csv", index=False)

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(7.2, 4.6))
        ax.errorbar(points["r"], points["vobs"], yerr=points["errv"], fmt="o", color="black", label="observed")
        ax.plot(points["r"], points["v_v6"], color="#356cb4", lw=1.6, label="TPG/v6 proxy")
        ax.plot(points["r"], points["v_K_exponential_disk"], color="#4f9d5d", lw=1.8, label="exponential-disk control")
        ax.plot(points["r"], points["v_wvo_endpoint"], color="#f28e2b", lw=2.2, label="warp/vertical-overlay endpoint")
        ax.plot(
            points["r"],
            points["v_expdisk_wvo_diagnostic"],
            color="#9467bd",
            lw=2.6,
            label="diagnostic expdisk + overlay",
        )
        ax.set_xlabel("R [kpc]")
        ax.set_ylabel("v [km/s]")
        ax.set_title("NGC4013 diagnostic mixed readout")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)
        fig.tight_layout()
        fig_path = FIGURES / "fig08_ngc4013_expdisk_wvo_diagnostic.png"
        fig.savefig(fig_path, dpi=180)
        plt.close(fig)
    except Exception as exc:  # pragma: no cover
        fig_path = None
        print(f"plotting skipped: {exc}")

    report = [
        "# NGC4013 Exponential-Disk + Warp/Vertical-Overlay Diagnostic",
        "",
        "This diagnostic applies the already frozen NGC4013 overlay kernel to the",
        "exponential-disk carrier. It is not an accepted endpoint because the mixed",
        "carrier was motivated by the wrong-family control audit.",
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Claim Boundary",
        "",
        "This is a diagnostic hypothesis test. It can motivate a future residual-blind",
        "mixed-readout source rule, but cannot validate or promote the mixed family.",
        "",
    ]
    if fig_path is not None:
        report.extend(["## Figure", "", str(fig_path.relative_to(ROOT)), ""])
    (REPORTS / "ngc4013_expdisk_wvo_diagnostic.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
