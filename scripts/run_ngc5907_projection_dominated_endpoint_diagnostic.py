#!/usr/bin/env python3
"""Run an explicit NGC5907 projection-dominated endpoint diagnostic.

This diagnostic consumes the residual-blind NGC5907 projection freeze gate and
turns it into a concrete solved-response readout formula. It is not an accepted
endpoint: it is a one-galaxy diagnostic of the newly frozen projection protocol.
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
CLAIM_BOUNDARY = "ngc5907_projection_endpoint_diagnostic_not_validation"

sys.path.insert(0, str(ROOT / "scripts"))
import run_source_native_readout_formula_endpoint as src  # noqa: E402
import run_s4g75_promoted_kernel_endpoint_stress_test as promoted  # noqa: E402


def rmse(obs: pd.Series, pred: pd.Series) -> float:
    return float(np.sqrt(np.mean(np.square(pred.to_numpy() - obs.to_numpy()))))


def smoothstep(x: np.ndarray) -> np.ndarray:
    clipped = np.clip(x, 0.0, 1.0)
    return clipped * clipped * (3.0 - 2.0 * clipped)


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


def build_generic_promoted_predictions() -> pd.DataFrame:
    points, _labels = src.load_points()
    points = promoted.apply_promoted_observables(points)
    points = src.add_bridge_formula_kernels(points)
    amplitudes = src.fit_amplitudes(points)
    scored = src.add_predictions(points, amplitudes)
    return scored.loc[scored["galaxy"] == "NGC5907"].copy()


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    freeze = pd.read_csv(DATA / "ngc5907_projection_freeze_summary.csv").iloc[0]
    sub = build_generic_promoted_predictions()
    sub = sub.sort_values("r").reset_index(drop=True)

    r = sub["r"].to_numpy(dtype=float)
    r_in = float(freeze["warp_r_inner_kpc"])
    r_out = float(freeze["warp_r_outer_kpc"])
    pi_projection = float(freeze["frozen_projection_bound"])
    h_over_r = float(freeze["thickness_h_over_rs"])
    truncation_contrast = float(freeze["truncation_contrast"])

    warp_window = smoothstep((r - r_in) / max(r_out - r_in, 1.0e-9))
    truncation_window = smoothstep((r - r_in) / max(r_out - r_in, 1.0e-9))
    kernel = warp_window * (1.0 + truncation_contrast * truncation_window) / (1.0 + truncation_contrast)

    # Projection-dominated readout is treated as attenuation, not as added
    # acceleration. The 1/2 factor is the first-order small-projection response
    # convention used here to keep the protocol bound conservative.
    gamma = 0.5 * pi_projection * h_over_r
    attenuation = np.clip(gamma * kernel, 0.0, 0.95)
    v2_projection = np.maximum(sub["v_v6"].to_numpy(dtype=float) ** 2 * (1.0 - attenuation), 0.0)
    sub["projection_kernel"] = kernel
    sub["projection_attenuation"] = attenuation
    sub["v_projection_dominated"] = np.sqrt(v2_projection)
    sub["delta_v2_projection"] = v2_projection - sub["v_v6"].to_numpy(dtype=float) ** 2
    sub["endpoint_scores_allowed"] = False
    sub["claim_boundary"] = CLAIM_BOUNDARY

    scores = pd.DataFrame(
        [
            {
                "galaxy": "NGC5907",
                "n_points": len(sub),
                "rmse_newton": rmse(sub["vobs"], sub["vn"]),
                "rmse_tpg_v6": rmse(sub["vobs"], sub["v_v6"]),
                "rmse_mond": rmse(sub["vobs"], sub["v_mond"]),
                "rmse_generic_promoted_thick_flared": rmse(sub["vobs"], sub["v_K_thick_flared"]),
                "rmse_projection_dominated": rmse(sub["vobs"], sub["v_projection_dominated"]),
                "projection_minus_tpg_v6": rmse(sub["vobs"], sub["v_projection_dominated"])
                - rmse(sub["vobs"], sub["v_v6"]),
                "projection_minus_mond": rmse(sub["vobs"], sub["v_projection_dominated"])
                - rmse(sub["vobs"], sub["v_mond"]),
                "projection_minus_generic_promoted": rmse(sub["vobs"], sub["v_projection_dominated"])
                - rmse(sub["vobs"], sub["v_K_thick_flared"]),
                "pi_projection_bound": pi_projection,
                "h_over_r": h_over_r,
                "gamma_projection": gamma,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    points_out = sub[
        [
            "galaxy",
            "r",
            "vobs",
            "errv",
            "vn",
            "v_v6",
            "v_mond",
            "v_K_thick_flared",
            "projection_kernel",
            "projection_attenuation",
            "delta_v2_projection",
            "v_projection_dominated",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ].copy()
    points_out.to_csv(DATA / "ngc5907_projection_endpoint_points.csv", index=False)
    scores.to_csv(DATA / "ngc5907_projection_endpoint_scores.csv", index=False)

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(7.2, 4.6))
        ax.errorbar(sub["r"], sub["vobs"], yerr=sub["errv"], fmt="o", color="black", label="observed")
        ax.plot(sub["r"], sub["vn"], color="0.55", lw=1.5, label="Newtonian baryonic")
        ax.plot(sub["r"], sub["v_v6"], color="#356cb4", lw=1.8, label="TPG/v6 proxy")
        ax.plot(sub["r"], sub["v_mond"], color="#c43d3d", lw=1.8, label="MOND proxy")
        ax.plot(sub["r"], sub["v_K_thick_flared"], color="#4f9d5d", lw=1.8, label="generic promoted thick/flared")
        ax.plot(
            sub["r"],
            sub["v_projection_dominated"],
            color="#f28e2b",
            lw=2.8,
            label="NGC5907 projection-dominated diagnostic",
        )
        ax.set_xlabel("R [kpc]")
        ax.set_ylabel("v [km/s]")
        ax.set_title("NGC5907 projection-dominated diagnostic endpoint")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)
        fig.tight_layout()
        fig_path = FIGURES / "fig05_ngc5907_projection_endpoint_diagnostic.png"
        fig.savefig(fig_path, dpi=180)
        plt.close(fig)
    except Exception as exc:  # pragma: no cover - plotting is diagnostic only
        fig_path = None
        print(f"plotting skipped: {exc}")

    report = [
        "# NGC5907 Projection-Dominated Endpoint Diagnostic",
        "",
        "This diagnostic runs an explicit projection-dominated solved-response",
        "formula from the NGC5907 projection freeze gate. It does not promote an",
        "accepted endpoint label and does not validate Tau Core.",
        "",
        "## Formula",
        "",
        "The diagnostic uses the source-frozen attenuation form",
        "",
        "`v_proj(R)^2 = v_TPG(R)^2 * (1 - gamma_proj K_proj(R))`,",
        "",
        "where `gamma_proj = 0.5 * Pi_projection * h/R`, and `K_proj(R)` is a",
        "smooth source-windowed warp/truncation kernel frozen by the NGC5907",
        "projection gate.",
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Claim Boundary",
        "",
        "This is a one-galaxy diagnostic endpoint. It is allowed only as a",
        "formula-inspection run; the accepted-manifest audit still keeps endpoint",
        "eligibility disabled.",
        "",
    ]
    if fig_path is not None:
        report.extend(["## Figure", "", str(fig_path.relative_to(ROOT)), ""])
    (REPORTS / "ngc5907_projection_endpoint_diagnostic.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
