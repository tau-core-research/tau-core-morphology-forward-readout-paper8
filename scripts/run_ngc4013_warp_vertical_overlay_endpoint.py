#!/usr/bin/env python3
"""Run the caveated NGC4013 warp/vertical-overlay endpoint.

The construction is read from the source-frozen manifest and replacement-label
gate. Observed velocities are used only after the readout curve is constructed.
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
CLAIM_BOUNDARY = "ngc4013_warp_vertical_overlay_caveated_preliminary_endpoint"

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
    return scored.loc[scored["galaxy"] == "NGC4013"].copy()


def add_warp_vertical_overlay_readout(points: pd.DataFrame, manifest: pd.Series) -> pd.DataFrame:
    """Apply the frozen source-side NGC4013 readout. This function does not inspect vobs."""
    sub = points.sort_values("r").reset_index(drop=True).copy()
    r = sub["r"].to_numpy(dtype=float)
    r_warp = float(manifest["r_warp_kpc"])
    r_outer = float(manifest["r_outer_kpc"])
    r25 = float(manifest["r25_kpc"])
    r_lag_start = float(manifest["r_lag_start_kpc"])
    r_s = float(manifest["r_s_kpc"])
    z_ec = float(manifest["z_ec_kpc"])
    gamma = float(manifest["gamma_overlay_upper"])
    omega_z = float(manifest["omega_z"])
    omega_ec = float(manifest["omega_ec"])
    omega_lag = float(manifest["omega_lag"])

    w_warp = smoothstep((r - r_warp) / max(r_outer - r_warp, 1.0e-9))
    k_z = 1.0 / (1.0 + r / max(r_s, 1.0e-9))
    k_ec = 1.0 / (1.0 + r / max(z_ec, 1.0e-9))
    k_lag = np.clip((r25 - r) / max(r25 - r_lag_start, 1.0e-9), 0.0, 1.0)
    k_wvo = w_warp * (omega_z * k_z + omega_ec * k_ec + omega_lag * k_lag)
    attenuation = np.clip(gamma * k_wvo, 0.0, 0.95)
    v2_tpg = sub["v_v6"].to_numpy(dtype=float) ** 2
    v2_wvo = np.maximum(v2_tpg * (1.0 - attenuation), 0.0)

    sub["W_warp"] = w_warp
    sub["K_z"] = k_z
    sub["K_EC"] = k_ec
    sub["K_lag"] = k_lag
    sub["K_wvo"] = k_wvo
    sub["wvo_attenuation"] = attenuation
    sub["delta_v2_wvo"] = v2_wvo - v2_tpg
    sub["v_wvo_endpoint"] = np.sqrt(v2_wvo)
    return sub


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    label = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_replacement_label_summary.csv").iloc[0]
    if not bool(label["endpoint_scores_allowed"]):
        raise RuntimeError("NGC4013 replacement label gate is not endpoint-score eligible")
    manifest = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_manifest.csv").iloc[0]
    if bool(manifest["uses_vobs_or_residual_in_construction"]):
        raise RuntimeError("frozen NGC4013 formula is not endpoint-blind")

    sub = add_warp_vertical_overlay_readout(build_generic_promoted_predictions(), manifest)

    # Scoring starts here. The observed curve is not used by the construction above.
    scores = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "n_points": len(sub),
                "rmse_newton": rmse(sub["vobs"], sub["vn"]),
                "rmse_tpg_v6": rmse(sub["vobs"], sub["v_v6"]),
                "rmse_mond": rmse(sub["vobs"], sub["v_mond"]),
                "rmse_original_compact_family": rmse(sub["vobs"], sub["v_K_compact_finite"]),
                "rmse_wrong_family_mean": float(
                    np.mean(
                        [
                            rmse(sub["vobs"], sub["v_K_compact_finite"]),
                            rmse(sub["vobs"], sub["v_K_scale_tail_spiral"]),
                            rmse(sub["vobs"], sub["v_K_exponential_disk"]),
                            rmse(sub["vobs"], sub["v_K_thick_flared"]),
                        ]
                    )
                ),
                "rmse_warp_vertical_overlay": rmse(sub["vobs"], sub["v_wvo_endpoint"]),
                "wvo_minus_tpg_v6": rmse(sub["vobs"], sub["v_wvo_endpoint"])
                - rmse(sub["vobs"], sub["v_v6"]),
                "wvo_minus_mond": rmse(sub["vobs"], sub["v_wvo_endpoint"])
                - rmse(sub["vobs"], sub["v_mond"]),
                "wvo_minus_original_compact": rmse(sub["vobs"], sub["v_wvo_endpoint"])
                - rmse(sub["vobs"], sub["v_K_compact_finite"]),
                "formula_id": str(manifest["formula_id"]),
                "gamma_overlay_upper": float(manifest["gamma_overlay_upper"]),
                "label_promotion_status": str(label["label_promotion_status"]),
                "endpoint_scores_allowed": True,
                "endpoint_status": "CAVEATED_ENDPOINT_PRELIMINARY_CONTROL_RESULT",
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
            "v_K_compact_finite",
            "v_K_scale_tail_spiral",
            "v_K_exponential_disk",
            "v_K_thick_flared",
            "W_warp",
            "K_z",
            "K_EC",
            "K_lag",
            "K_wvo",
            "wvo_attenuation",
            "delta_v2_wvo",
            "v_wvo_endpoint",
        ]
    ].copy()
    points_out["endpoint_scores_allowed"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    points_out.to_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_points.csv", index=False)
    scores.to_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_scores.csv", index=False)

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(7.2, 4.6))
        ax.errorbar(sub["r"], sub["vobs"], yerr=sub["errv"], fmt="o", color="black", label="observed")
        ax.plot(sub["r"], sub["vn"], color="0.55", lw=1.5, label="Newtonian baryonic")
        ax.plot(sub["r"], sub["v_v6"], color="#356cb4", lw=1.8, label="TPG/v6 proxy")
        ax.plot(sub["r"], sub["v_mond"], color="#c43d3d", lw=1.8, label="MOND proxy")
        ax.plot(sub["r"], sub["v_K_compact_finite"], color="#7f7f7f", lw=1.7, ls="--", label="rejected compact family")
        ax.plot(
            sub["r"],
            sub["v_wvo_endpoint"],
            color="#f28e2b",
            lw=2.8,
            label="caveated warp/vertical-overlay readout",
        )
        ax.set_xlabel("R [kpc]")
        ax.set_ylabel("v [km/s]")
        ax.set_title("NGC4013 caveated warp/vertical-overlay endpoint")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)
        fig.tight_layout()
        fig_path = FIGURES / "fig07_ngc4013_warp_vertical_overlay_endpoint.png"
        fig.savefig(fig_path, dpi=180)
        plt.close(fig)
    except Exception as exc:  # pragma: no cover
        fig_path = None
        print(f"plotting skipped: {exc}")

    report = [
        "# NGC4013 Warp/Vertical-Overlay Caveated Endpoint",
        "",
        "This run scores the source-frozen NGC4013 warp/vertical-overlay readout",
        "after caveated replacement-label promotion. The observed rotation curve is",
        "used only in the scoring block.",
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Claim Boundary",
        "",
        "This is a caveated single-galaxy preliminary endpoint. It does not validate",
        "Tau Core and should be read as a replacement-label control after compact",
        "lane rejection.",
        "",
    ]
    if fig_path is not None:
        report.extend(["## Figure", "", str(fig_path.relative_to(ROOT)), ""])
    (REPORTS / "ngc4013_warp_vertical_overlay_endpoint.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
