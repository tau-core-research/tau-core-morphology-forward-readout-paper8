#!/usr/bin/env python3
"""Score the frozen NGC4088 warp-class law on UGC03580/UGC3580."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from warp_class_transfer_common_v01 import (
    circular_block_bootstrap_delta,
    fit_halo,
    load_sparc_endpoint,
    markdown_table,
    metric_row,
    sha256,
    warp_prediction,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "paper8_submission_source" / "figures"

MANIFEST = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_freeze_v01.json"
MANIFEST_SHA = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_freeze_v01.sha256"
ENDPOINT = ROOT / "data" / "external" / "sparc" / "UGC03580_rotmod.dat"

POINTS_OUT = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01_points.csv"
SCORES_OUT = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01_scores.csv"
ZONE_SCORES_OUT = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01_zone_scores.csv"
SUMMARY_OUT = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01.json"
REPORT_OUT = REPORTS / "ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01.md"
FIGURE_OUT = FIGURES / "fig_ugc03580_ugc3580_ngc4088_class_transfer_v01.png"

CLAIM_BOUNDARY = "retrospective_class_replication_negative_not_tau_falsification"
NGC4088_XW_CONTROL = 0.2983326403051493
UGC08490_XW_CONTROL = 0.4508762999054615
BOOTSTRAP_SEED = 3580


def verify_freeze() -> dict[str, object]:
    expected = MANIFEST_SHA.read_text(encoding="utf-8").split()[0]
    actual = sha256(MANIFEST)
    if actual != expected:
        raise RuntimeError("freeze manifest hash mismatch")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["freeze_status"] != "RETROSPECTIVE_SOURCE_FROZEN_CLASS_TRANSFER_READY_NOT_SCORED":
        raise RuntimeError("unexpected freeze status")
    if manifest["formula"]["post_freeze_retuning_allowed"]:
        raise RuntimeError("post-freeze retuning is forbidden")
    if manifest["source_selection"]["selection_uses_pointwise_vobs_or_residual"]:
        raise RuntimeError("target selection used the endpoint")
    return manifest


def score_predictions(
    points: pd.DataFrame,
    predictions: dict[str, np.ndarray],
    specs: dict[str, tuple[str, int, int]],
) -> pd.DataFrame:
    rows = [
        metric_row(
            points,
            model_id,
            specs[model_id][0],
            prediction,
            endpoint_fit_parameters=specs[model_id][1],
            imported_summary_scalars=specs[model_id][2],
        )
        for model_id, prediction in predictions.items()
    ]
    return pd.DataFrame(rows).sort_values(
        ["valid_full_endpoint", "rmse_km_s"], ascending=[False, True]
    )


def main() -> None:
    manifest = verify_freeze()
    points = load_sparc_endpoint(ENDPOINT)
    frozen = manifest["derived_frozen_values"]
    source = manifest["frozen_source_inputs"]
    formula = manifest["formula"]

    r_hi = float(source["r_hi_kpc"])
    vflat = float(source["vflat_km_s_primary"])
    x_w = float(frozen["x_w_primary_sparc_rhi"])
    lambda_primary = float(frozen["lambda_w_primary_km2_s2"])
    lambda_source_speed = float(frozen["lambda_w_source_speed_sensitivity_km2_s2"])
    x_w_source_hi = float(frozen["x_w_source_hi_denominator_sensitivity"])
    lambda_source_hi = float(frozen["lambda_w_source_hi_denominator_sensitivity_km2_s2"])
    power = float(formula["turn_on_power"])

    primary, primary_kernel, primary_v2 = warp_prediction(
        points, r_hi_kpc=r_hi, x_w=x_w, lambda_w=lambda_primary, power=power
    )
    source_speed, _, _ = warp_prediction(
        points, r_hi_kpc=r_hi, x_w=x_w, lambda_w=lambda_source_speed, power=power
    )
    source_hi_sensitivity, _, _ = warp_prediction(
        points,
        r_hi_kpc=r_hi,
        x_w=x_w_source_hi,
        lambda_w=lambda_source_hi,
        power=power,
    )
    p2, _, _ = warp_prediction(
        points, r_hi_kpc=r_hi, x_w=x_w, lambda_w=lambda_primary, power=2.0
    )
    wrong_ngc4088, _, _ = warp_prediction(
        points,
        r_hi_kpc=r_hi,
        x_w=NGC4088_XW_CONTROL,
        lambda_w=NGC4088_XW_CONTROL * vflat**2,
        power=1.0,
    )
    wrong_ugc08490, _, _ = warp_prediction(
        points,
        r_hi_kpc=r_hi,
        x_w=UGC08490_XW_CONTROL,
        lambda_w=UGC08490_XW_CONTROL * vflat**2,
        power=1.0,
    )
    wrong_sign, _, wrong_sign_v2 = warp_prediction(
        points,
        r_hi_kpc=r_hi,
        x_w=x_w,
        lambda_w=lambda_primary,
        power=power,
        sign=-1.0,
    )
    nfw, nfw_params = fit_halo(points, "NFW")
    piso, piso_params = fit_halo(points, "PSEUDO_ISOTHERMAL")

    predictions = {
        "TAU_WARP_TRANSFER_PRIMARY": primary,
        "TAU_WARP_TRANSFER_SOURCE_SPEED_SENSITIVITY": source_speed,
        "TAU_WARP_TRANSFER_SOURCE_HI_DENOMINATOR_SENSITIVITY": source_hi_sensitivity,
        "NEWTONIAN_BARYONIC": points["vn_km_s"].to_numpy(dtype=float),
        "TPG_V6_FIXED": points["v_tpg_v6_km_s"].to_numpy(dtype=float),
        "MOND_FIXED_A0": points["v_mond_km_s"].to_numpy(dtype=float),
        "CONTROL_WRONG_NGC4088_ONSET": wrong_ngc4088,
        "CONTROL_WRONG_UGC08490_ONSET": wrong_ugc08490,
        "CONTROL_WRONG_P2": p2,
        "CONTROL_WRONG_SIGN": wrong_sign,
        "NFW_TWO_PARAMETER_ENDPOINT_FIT": nfw,
        "PSEUDO_ISOTHERMAL_TWO_PARAMETER_ENDPOINT_FIT": piso,
    }
    specs = {
        "TAU_WARP_TRANSFER_PRIMARY": ("matched_frozen_transfer", 0, 2),
        "TAU_WARP_TRANSFER_SOURCE_SPEED_SENSITIVITY": ("predeclared_sensitivity", 0, 1),
        "TAU_WARP_TRANSFER_SOURCE_HI_DENOMINATOR_SENSITIVITY": ("predeclared_sensitivity", 0, 2),
        "NEWTONIAN_BARYONIC": ("fixed_standard_comparator", 0, 0),
        "TPG_V6_FIXED": ("fixed_standard_comparator", 0, 0),
        "MOND_FIXED_A0": ("fixed_standard_comparator", 0, 0),
        "CONTROL_WRONG_NGC4088_ONSET": ("morphology_control", 0, 2),
        "CONTROL_WRONG_UGC08490_ONSET": ("morphology_control", 0, 2),
        "CONTROL_WRONG_P2": ("morphology_control", 0, 2),
        "CONTROL_WRONG_SIGN": ("morphology_control", 0, 2),
        "NFW_TWO_PARAMETER_ENDPOINT_FIT": ("fit_aided_standard_comparator", 2, 0),
        "PSEUDO_ISOTHERMAL_TWO_PARAMETER_ENDPOINT_FIT": ("fit_aided_standard_comparator", 2, 0),
    }
    scores = score_predictions(points, predictions, specs)
    scores["claim_boundary"] = CLAIM_BOUNDARY

    points_out = points.copy()
    points_out["x_R_over_RHI"] = points_out["r_kpc"] / r_hi
    points_out["x_w_frozen"] = x_w
    points_out["warp_kernel_frozen"] = primary_kernel
    points_out["primary_total_v2_km2_s2"] = primary_v2
    points_out["wrong_sign_total_v2_km2_s2"] = wrong_sign_v2
    for model_id, prediction in predictions.items():
        points_out[f"pred_{model_id}"] = prediction
        points_out[f"resid_{model_id}"] = prediction - points_out["vobs_km_s"]
    points_out["construction_used_pointwise_vobs_or_residual"] = False
    points_out["scoring_used_vobs"] = True
    points_out["claim_boundary"] = CLAIM_BOUNDARY

    zones = {
        "pre_onset": points_out["x_R_over_RHI"] <= x_w,
        "onset_to_RHI": (points_out["x_R_over_RHI"] > x_w)
        & (points_out["x_R_over_RHI"] <= 1.0),
        "beyond_RHI": points_out["x_R_over_RHI"] > 1.0,
        "within_RHI_all": points_out["x_R_over_RHI"] <= 1.0,
    }
    zone_rows: list[dict[str, object]] = []
    zone_models = [
        "TAU_WARP_TRANSFER_PRIMARY",
        "TAU_WARP_TRANSFER_SOURCE_HI_DENOMINATOR_SENSITIVITY",
        "CONTROL_WRONG_NGC4088_ONSET",
        "CONTROL_WRONG_UGC08490_ONSET",
        "NEWTONIAN_BARYONIC",
        "MOND_FIXED_A0",
        "TPG_V6_FIXED",
    ]
    for zone_name, mask in zones.items():
        zone = points.loc[mask].reset_index(drop=True)
        if zone.empty:
            continue
        for model_id in zone_models:
            pred = predictions[model_id][mask.to_numpy()]
            row = metric_row(zone, model_id, "radial_zone_diagnostic", pred)
            row["zone"] = zone_name
            zone_rows.append(row)
    zone_scores = pd.DataFrame(zone_rows)

    obs = points["vobs_km_s"].to_numpy(dtype=float)
    within = zones["within_RHI_all"].to_numpy()
    boot_full_mond = circular_block_bootstrap_delta(
        (primary - obs) ** 2,
        (predictions["MOND_FIXED_A0"] - obs) ** 2,
        seed=BOOTSTRAP_SEED,
    )
    boot_full_wrong = circular_block_bootstrap_delta(
        (primary - obs) ** 2,
        (predictions["CONTROL_WRONG_UGC08490_ONSET"] - obs) ** 2,
        seed=BOOTSTRAP_SEED + 1,
    )
    boot_within_mond = circular_block_bootstrap_delta(
        (primary[within] - obs[within]) ** 2,
        (predictions["MOND_FIXED_A0"][within] - obs[within]) ** 2,
        seed=BOOTSTRAP_SEED + 2,
    )

    # Endpoint-informed scan retained only as an audit of how far the source
    # onset lies from the onset preferred by this already-open target.
    scan_rows = []
    for trial_x in np.linspace(0.05, 0.98, 373):
        trial, _, _ = warp_prediction(
            points,
            r_hi_kpc=r_hi,
            x_w=float(trial_x),
            lambda_w=float(trial_x) * vflat**2,
            power=1.0,
        )
        scan_rows.append(
            {"x_w": float(trial_x), "rmse_km_s": float(np.sqrt(np.mean((trial - obs) ** 2)))}
        )
    preferred = pd.DataFrame(scan_rows).sort_values("rmse_km_s").iloc[0]

    def score(model_id: str) -> pd.Series:
        return scores.loc[scores["model_id"].eq(model_id)].iloc[0]

    primary_score = score("TAU_WARP_TRANSFER_PRIMARY")
    mond_score = score("MOND_FIXED_A0")
    wrong_score = score("CONTROL_WRONG_UGC08490_ONSET")
    newton_score = score("NEWTONIAN_BARYONIC")
    within_primary = zone_scores.loc[
        zone_scores["zone"].eq("within_RHI_all")
        & zone_scores["model_id"].eq("TAU_WARP_TRANSFER_PRIMARY")
    ].iloc[0]
    within_mond = zone_scores.loc[
        zone_scores["zone"].eq("within_RHI_all")
        & zone_scores["model_id"].eq("MOND_FIXED_A0")
    ].iloc[0]

    primary_beats_mond_full = bool(primary_score["rmse_km_s"] < mond_score["rmse_km_s"])
    primary_beats_wrong_full = bool(primary_score["rmse_km_s"] < wrong_score["rmse_km_s"])
    primary_beats_newton_full = bool(primary_score["rmse_km_s"] < newton_score["rmse_km_s"])
    primary_beats_mond_within = bool(within_primary["rmse_km_s"] < within_mond["rmse_km_s"])

    status = (
        "RETROSPECTIVE_CLASS_TRANSFER_PASS"
        if primary_beats_mond_full and primary_beats_wrong_full and primary_beats_mond_within
        else "RETROSPECTIVE_CLASS_TRANSFER_REJECTS_UNCAPPED_UNIVERSAL_LAW"
    )
    summary = {
        "schema": "tau_core_ugc03580_ugc3580_ngc4088_class_transfer_endpoint_v01",
        "status": status,
        "galaxy": "UGC03580",
        "alias": "UGC3580",
        "formula_id": manifest["formula_id"],
        "endpoint_sha256": sha256(ENDPOINT),
        "freeze_manifest_sha256": sha256(MANIFEST),
        "n_points": len(points),
        "n_pre_onset": int(zones["pre_onset"].sum()),
        "n_onset_to_rhi": int(zones["onset_to_RHI"].sum()),
        "n_beyond_rhi": int(zones["beyond_RHI"].sum()),
        "x_w_frozen": x_w,
        "primary_rmse_full_km_s": float(primary_score["rmse_km_s"]),
        "primary_rmse_within_rhi_km_s": float(within_primary["rmse_km_s"]),
        "newtonian_rmse_full_km_s": float(newton_score["rmse_km_s"]),
        "fixed_mond_rmse_full_km_s": float(mond_score["rmse_km_s"]),
        "fixed_mond_rmse_within_rhi_km_s": float(within_mond["rmse_km_s"]),
        "wrong_ugc08490_onset_rmse_full_km_s": float(wrong_score["rmse_km_s"]),
        "best_fit_halo_rmse_km_s": float(
            scores.loc[scores["role"].eq("fit_aided_standard_comparator"), "rmse_km_s"].min()
        ),
        "primary_beats_newtonian_full": primary_beats_newton_full,
        "primary_beats_fixed_mond_full": primary_beats_mond_full,
        "primary_beats_wrong_onset_full": primary_beats_wrong_full,
        "primary_beats_fixed_mond_within_rhi": primary_beats_mond_within,
        "endpoint_informed_preferred_x_w_diagnostic": float(preferred["x_w"]),
        "endpoint_informed_preferred_x_w_rmse_km_s": float(preferred["rmse_km_s"]),
        "bootstrap_full_primary_vs_mond": boot_full_mond,
        "bootstrap_full_primary_vs_wrong_ugc08490_onset": boot_full_wrong,
        "bootstrap_within_rhi_primary_vs_mond": boot_within_mond,
        "halo_fit_parameters": {"NFW": nfw_params, "PSEUDO_ISOTHERMAL": piso_params},
        "interpretation": (
            "The source-correct UGC03580 onset does not replicate the NGC4088 class-law "
            "success. It improves the Newtonian comparison inside R_HI only modestly, "
            "loses to fixed MOND there, loses to earlier wrong-onset controls, and the "
            "unchanged uncapped kernel overshoots beyond R_HI. This rejects the current "
            "one-component uncapped law as a universal warp-class rotation law; it does "
            "not reject source-native warp morphology or Tau Core in general."
        ),
        "construction_used_pointwise_vobs_or_residual": False,
        "scoring_used_vobs": True,
        "historical_endpoint_exposure": True,
        "prospective_blind_endpoint": False,
        "post_endpoint_repair_performed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    points_out.to_csv(POINTS_OUT, index=False)
    scores.to_csv(SCORES_OUT, index=False)
    zone_scores.to_csv(ZONE_SCORES_OUT, index=False)
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    try:
        import matplotlib.pyplot as plt

        fig, (ax, axr) = plt.subplots(
            2, 1, figsize=(8.0, 7.2), sharex=True, height_ratios=[2.2, 1.0]
        )
        ax.errorbar(
            points["r_kpc"],
            points["vobs_km_s"],
            yerr=points["errv_km_s"],
            fmt="o",
            color="black",
            ms=3.5,
            lw=0.8,
            label="SPARC observed",
            zorder=10,
        )
        ax.plot(points["r_kpc"], points["vn_km_s"], color="0.55", label="Newtonian baryonic")
        ax.plot(points["r_kpc"], points["v_mond_km_s"], color="#356cb4", label="fixed MOND")
        ax.plot(points["r_kpc"], primary, color="#f28e2b", lw=2.5, label="source-correct transfer")
        ax.plot(points["r_kpc"], wrong_ugc08490, color="#8c564b", ls="--", label="wrong earlier onset")
        ax.plot(points["r_kpc"], piso, color="#2ca02c", ls=":", lw=2.0, label="2-parameter pseudo-isothermal")
        ax.axvline(x_w * r_hi, color="#f28e2b", alpha=0.55, lw=1.2)
        ax.axvline(r_hi, color="0.25", alpha=0.45, lw=1.0, ls=":")
        ax.set_ylabel("velocity [km/s]")
        ax.set_title("UGC03580 / UGC3580: unchanged NGC4088 warp-law transfer")
        ax.legend(fontsize=7.3, ncol=2)
        ax.grid(alpha=0.2)
        axr.axhline(0.0, color="0.4", lw=0.8)
        axr.plot(points["r_kpc"], primary - obs, color="#f28e2b", label="source-correct")
        axr.plot(points["r_kpc"], predictions["MOND_FIXED_A0"] - obs, color="#356cb4", label="MOND")
        axr.axvline(x_w * r_hi, color="#f28e2b", alpha=0.55, lw=1.2)
        axr.axvline(r_hi, color="0.25", alpha=0.45, lw=1.0, ls=":")
        axr.set_xlabel("R [kpc]")
        axr.set_ylabel("model - data")
        axr.grid(alpha=0.2)
        fig.tight_layout()
        fig.savefig(FIGURE_OUT, dpi=190)
        plt.close(fig)
    except Exception as exc:  # pragma: no cover
        print(f"plot skipped: {exc}")

    report = [
        "# UGC03580 / UGC3580 unchanged NGC4088-class transfer endpoint v01",
        "",
        f"Status: `{status}`",
        "",
        "The Jozsa warp onset and unchanged NGC4088 formula were frozen by a",
        "separate script before this scorer opened the local pointwise endpoint.",
        "Because UGC03580 was used in earlier repository endpoint analyses, this is",
        "a retrospective replication rather than a prospective blind prediction.",
        "",
        "## Full-endpoint scores",
        "",
        markdown_table(
            scores[
                [
                    "model_id",
                    "role",
                    "valid_full_endpoint",
                    "rmse_km_s",
                    "bias_km_s",
                    "chi2_per_point",
                    "endpoint_fit_parameters",
                    "imported_summary_scalars",
                ]
            ]
        ),
        "",
        "## Radial-zone scores",
        "",
        markdown_table(
            zone_scores[
                ["zone", "model_id", "n_points", "rmse_km_s", "bias_km_s"]
            ]
        ),
        "",
        "## Decisive checks",
        "",
        f"- source-frozen onset: `x_w={x_w:.6f}` or `{x_w*r_hi:.3f} kpc`;",
        f"- endpoint-informed preferred onset (diagnostic only): `x_w={float(preferred['x_w']):.6f}`;",
        f"- primary full RMSE: `{float(primary_score['rmse_km_s']):.4f} km/s`;",
        f"- primary within-R_HI RMSE: `{float(within_primary['rmse_km_s']):.4f} km/s`;",
        f"- Newtonian full RMSE: `{float(newton_score['rmse_km_s']):.4f} km/s`;",
        f"- fixed MOND full/within-R_HI RMSE: `{float(mond_score['rmse_km_s']):.4f}` / `{float(within_mond['rmse_km_s']):.4f} km/s`;",
        f"- wrong UGC08490-onset full RMSE: `{float(wrong_score['rmse_km_s']):.4f} km/s`;",
        f"- best two-parameter halo RMSE: `{float(summary['best_fit_halo_rmse_km_s']):.4f} km/s`.",
        "",
        "## Verdict",
        "",
        summary["interpretation"],
        "The three points beyond the catalog R_HI expose an additional structural",
        "failure: the unchanged linear kernel is uncapped and grows without a",
        "source-supported outer saturation rule. Adding a cap now would be a new",
        "law, not a repair of this endpoint. It must be derived source-side and then",
        "tested on another target.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
