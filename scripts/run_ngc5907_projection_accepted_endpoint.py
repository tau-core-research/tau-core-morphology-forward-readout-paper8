#!/usr/bin/env python3
"""Run the accepted NGC5907 projection endpoint after freeze-gate promotion.

The construction is read from ngc5907_projection_accepted_endpoint_manifest.csv.
Observed velocities are used only in the scoring block.
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
CLAIM_BOUNDARY = "ngc5907_projection_accepted_endpoint_preliminary_control"

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


def add_frozen_projection_readout(points: pd.DataFrame, manifest: pd.Series) -> pd.DataFrame:
    """Apply the frozen manifest. This function does not inspect vobs."""
    sub = points.sort_values("r").reset_index(drop=True).copy()
    r = sub["r"].to_numpy(dtype=float)
    r_in = float(manifest["r_in_kpc"])
    r_out = float(manifest["r_out_kpc"])
    truncation_contrast = float(manifest["truncation_contrast"])
    gamma = float(manifest["gamma_projection"])

    x = (r - r_in) / max(r_out - r_in, 1.0e-9)
    warp_window = smoothstep(x)
    truncation_window = smoothstep(x)
    kernel = warp_window * (1.0 + truncation_contrast * truncation_window) / (
        1.0 + truncation_contrast
    )
    attenuation = np.clip(gamma * kernel, 0.0, 0.95)
    v2_projection = np.maximum(sub["v_v6"].to_numpy(dtype=float) ** 2 * (1.0 - attenuation), 0.0)

    sub["projection_kernel"] = kernel
    sub["projection_attenuation"] = attenuation
    sub["delta_v2_projection"] = v2_projection - sub["v_v6"].to_numpy(dtype=float) ** 2
    sub["v_projection_accepted"] = np.sqrt(v2_projection)
    return sub


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(DATA / "ngc5907_projection_accepted_endpoint_manifest.csv").iloc[0]
    if not bool(manifest["endpoint_scores_allowed"]):
        raise RuntimeError("NGC5907 accepted endpoint gate is not score-eligible")

    sub = add_frozen_projection_readout(build_generic_promoted_predictions(), manifest)

    # Scoring starts here. Observed rotation values are not used by the frozen
    # readout construction above.
    scores = pd.DataFrame(
        [
            {
                "galaxy": "NGC5907",
                "n_points": len(sub),
                "rmse_newton": rmse(sub["vobs"], sub["vn"]),
                "rmse_tpg_v6": rmse(sub["vobs"], sub["v_v6"]),
                "rmse_mond": rmse(sub["vobs"], sub["v_mond"]),
                "rmse_generic_promoted_thick_flared": rmse(sub["vobs"], sub["v_K_thick_flared"]),
                "rmse_projection_accepted": rmse(sub["vobs"], sub["v_projection_accepted"]),
                "projection_minus_tpg_v6": rmse(sub["vobs"], sub["v_projection_accepted"])
                - rmse(sub["vobs"], sub["v_v6"]),
                "projection_minus_mond": rmse(sub["vobs"], sub["v_projection_accepted"])
                - rmse(sub["vobs"], sub["v_mond"]),
                "projection_minus_generic_promoted": rmse(sub["vobs"], sub["v_projection_accepted"])
                - rmse(sub["vobs"], sub["v_K_thick_flared"]),
                "formula_id": str(manifest["formula_id"]),
                "gamma_projection": float(manifest["gamma_projection"]),
                "endpoint_scores_allowed": True,
                "accepted_endpoint_status": "ACCEPTED_ENDPOINT_PRELIMINARY_CONTROL_RESULT",
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
            "v_projection_accepted",
        ]
    ].copy()
    points_out["endpoint_scores_allowed"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    points_out.to_csv(DATA / "ngc5907_projection_accepted_endpoint_points.csv", index=False)
    scores.to_csv(DATA / "ngc5907_projection_accepted_endpoint_scores.csv", index=False)

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
            sub["v_projection_accepted"],
            color="#f28e2b",
            lw=2.8,
            label="accepted frozen projection readout",
        )
        ax.set_xlabel("R [kpc]")
        ax.set_ylabel("v [km/s]")
        ax.set_title("NGC5907 accepted frozen projection endpoint")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)
        fig.tight_layout()
        fig_path = FIGURES / "fig06_ngc5907_projection_accepted_endpoint.png"
        fig.savefig(fig_path, dpi=180)
        plt.close(fig)
    except Exception as exc:  # pragma: no cover
        fig_path = None
        print(f"plotting skipped: {exc}")

    report = [
        "# NGC5907 Projection Accepted Endpoint",
        "",
        "This run scores the frozen projection-dominated NGC5907 endpoint protocol.",
        "The formula is read from the accepted endpoint manifest and is not changed",
        "after observing the endpoint residuals.",
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Claim Boundary",
        "",
        "This is an accepted single-galaxy preliminary control endpoint, not a",
        "population validation of Tau Core. The accepted status applies to the",
        "endpoint-blind formula freeze, not to universal physical validation.",
        "",
    ]
    if fig_path is not None:
        report.extend(["## Figure", "", str(fig_path.relative_to(ROOT)), ""])
    (REPORTS / "ngc5907_projection_accepted_endpoint.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
