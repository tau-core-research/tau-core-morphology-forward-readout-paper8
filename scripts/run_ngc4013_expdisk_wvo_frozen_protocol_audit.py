#!/usr/bin/env python3
"""Score the frozen NGC4013 mixed-readout protocol as non-retroactive audit.

The readout construction is loaded from
ngc4013_expdisk_wvo_formula_freeze_manifest.csv and does not inspect observed
velocities. Observed velocities are read only in the scoring block. The result
is recorded as a frozen-protocol audit, not as a retroactive accepted endpoint.
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
CLAIM_BOUNDARY = "ngc4013_expdisk_wvo_frozen_protocol_audit_not_endpoint"

sys.path.insert(0, str(ROOT / "scripts"))
import run_ngc4013_warp_vertical_overlay_endpoint as wvo  # noqa: E402


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


def add_frozen_mixed_readout(points: pd.DataFrame, manifest: pd.Series) -> pd.DataFrame:
    """Apply the frozen mixed formula. This function does not inspect vobs."""
    sub = points.sort_values("r").reset_index(drop=True).copy()
    r = sub["r"].to_numpy(dtype=float)
    r_warp = float(manifest["r_warp_kpc"])
    r_outer = float(manifest["r_outer_kpc"])
    r_lag_start = float(manifest["r_lag_start_kpc"])
    r_lag_zero = float(manifest["r_lag_zero_kpc"])
    r_s = float(manifest["r_s_kpc"])
    z_ec = float(manifest["z_ec_kpc"])
    gamma = float(manifest["gamma_overlay_upper"])
    omega_z = float(manifest["omega_z"])
    omega_ec = float(manifest["omega_ec"])
    omega_lag = float(manifest["omega_lag"])

    w_warp = smoothstep((r - r_warp) / max(r_outer - r_warp, 1.0e-9))
    k_z = 1.0 / (1.0 + r / max(r_s, 1.0e-9))
    k_ec = 1.0 / (1.0 + r / max(z_ec, 1.0e-9))
    k_lag = np.clip((r_lag_zero - r) / max(r_lag_zero - r_lag_start, 1.0e-9), 0.0, 1.0)
    k_wvo = w_warp * (omega_z * k_z + omega_ec * k_ec + omega_lag * k_lag)
    attenuation = np.clip(gamma * k_wvo, 0.0, 0.95)

    carrier_col = str(manifest["carrier"])
    v2_carrier = sub[carrier_col].to_numpy(dtype=float) ** 2
    v2_mix = np.maximum(v2_carrier * (1.0 - attenuation), 0.0)

    sub["W_warp"] = w_warp
    sub["K_z"] = k_z
    sub["K_EC"] = k_ec
    sub["K_lag"] = k_lag
    sub["K_wvo"] = k_wvo
    sub["mixed_attenuation"] = attenuation
    sub["delta_v2_expdisk_wvo_frozen"] = v2_mix - v2_carrier
    sub["v_expdisk_wvo_frozen"] = np.sqrt(v2_mix)
    return sub


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    freeze = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_summary.csv").iloc[0]
    if not bool(freeze["prospective_endpoint_protocol_ready"]):
        raise RuntimeError("NGC4013 mixed frozen protocol is not prospective-ready")
    if bool(freeze["retrospective_endpoint_scores_allowed"]):
        raise RuntimeError("retroactive endpoint scoring should remain disabled")

    manifest = pd.read_csv(DATA / "ngc4013_expdisk_wvo_formula_freeze_manifest.csv").iloc[0]
    if bool(manifest["uses_vobs_or_residual_in_construction"]):
        raise RuntimeError("frozen mixed manifest is not endpoint-blind")

    wvo_manifest = pd.read_csv(
        DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_manifest.csv"
    ).iloc[0]
    points = wvo.add_warp_vertical_overlay_readout(
        wvo.build_generic_promoted_predictions(), wvo_manifest
    )
    points = add_frozen_mixed_readout(points, manifest)

    # Scoring starts here. vobs is not used in add_frozen_mixed_readout.
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
                "rmse_expdisk_wvo_frozen_protocol": rmse(
                    points["vobs"], points["v_expdisk_wvo_frozen"]
                ),
                "frozen_minus_expdisk": rmse(points["vobs"], points["v_expdisk_wvo_frozen"])
                - rmse(points["vobs"], points["v_K_exponential_disk"]),
                "frozen_minus_wvo": rmse(points["vobs"], points["v_expdisk_wvo_frozen"])
                - rmse(points["vobs"], points["v_wvo_endpoint"]),
                "frozen_minus_tpg_v6": rmse(points["vobs"], points["v_expdisk_wvo_frozen"])
                - rmse(points["vobs"], points["v_v6"]),
                "formula_id": str(manifest["formula_id"]),
                "formula_freeze_status": str(freeze["formula_freeze_status"]),
                "retrospective_endpoint_scores_allowed": False,
                "prospective_endpoint_protocol_ready": True,
                "protocol_audit_status": "FROZEN_PROTOCOL_SCORE_RECORDED_NOT_RETROACTIVE_ENDPOINT",
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
            "W_warp",
            "K_z",
            "K_EC",
            "K_lag",
            "K_wvo",
            "mixed_attenuation",
            "delta_v2_expdisk_wvo_frozen",
            "v_expdisk_wvo_frozen",
        ]
    ].copy()
    points_out["retrospective_endpoint_scores_allowed"] = False
    points_out["prospective_endpoint_protocol_ready"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    scores.to_csv(DATA / "ngc4013_expdisk_wvo_frozen_protocol_scores.csv", index=False)
    points_out.to_csv(DATA / "ngc4013_expdisk_wvo_frozen_protocol_points.csv", index=False)

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(7.2, 4.6))
        ax.errorbar(points["r"], points["vobs"], yerr=points["errv"], fmt="o", color="black", label="observed")
        ax.plot(points["r"], points["v_v6"], color="#356cb4", lw=1.6, label="TPG/v6 proxy")
        ax.plot(points["r"], points["v_K_exponential_disk"], color="#4f9d5d", lw=1.8, label="exponential-disk carrier")
        ax.plot(
            points["r"],
            points["v_expdisk_wvo_frozen"],
            color="#9467bd",
            lw=2.6,
            label="frozen mixed protocol",
        )
        ax.set_xlabel("R [kpc]")
        ax.set_ylabel("v [km/s]")
        ax.set_title("NGC4013 frozen mixed-readout protocol audit")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)
        fig.tight_layout()
        fig_path = FIGURES / "fig09_ngc4013_expdisk_wvo_frozen_protocol.png"
        fig.savefig(fig_path, dpi=180)
        plt.close(fig)
    except Exception as exc:  # pragma: no cover
        fig_path = None
        print(f"plotting skipped: {exc}")

    report = [
        "# NGC4013 Frozen Mixed-Readout Protocol Audit",
        "",
        "This audit scores the frozen mixed formula manifest. The construction does",
        "not read observed velocities, but the score is not a retroactive accepted",
        "endpoint because the NGC4013 mixed branch had already been inspected as a",
        "diagnostic after wrong-family controls.",
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Claim Boundary",
        "",
        "The curve is now generated by a frozen prospective mixed-readout protocol.",
        "The numerical score is recorded for continuity and future protocol",
        "comparison, not as accepted endpoint validation.",
        "",
    ]
    if fig_path is not None:
        report.extend(["## Figure", "", str(fig_path.relative_to(ROOT)), ""])
    (REPORTS / "ngc4013_expdisk_wvo_frozen_protocol_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
