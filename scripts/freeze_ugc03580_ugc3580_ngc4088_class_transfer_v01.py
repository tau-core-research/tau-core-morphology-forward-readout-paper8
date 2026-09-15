#!/usr/bin/env python3
"""Freeze the unchanged NGC4088 warp law for UGC03580/UGC3580."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from warp_class_transfer_common_v01 import sha256


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
SOURCE_BODY = DATA / "ugc03580_ugc3580_warp_body_v01.json"
SPARC_MASTER = DATA / "external_sparc_master_table.csv"
MANIFEST = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_freeze_v01.json"
MANIFEST_SHA = DATA / "ugc03580_ugc3580_ngc4088_class_transfer_freeze_v01.sha256"
REPORT = REPORTS / "ugc03580_ugc3580_ngc4088_class_transfer_freeze_v01.md"

FORMULA_ID = "NGC4088_WARP_HISTORY_CLASS_V1__UGC03580_TRANSFER_V01"
CLAIM_BOUNDARY = "retrospective_source_frozen_class_transfer_not_tau_validation"


def read_sparc_row() -> dict[str, str]:
    with SPARC_MASTER.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row["Galaxy"] == "UGC03580"]
    if len(rows) != 1:
        raise RuntimeError(f"expected one UGC03580 SPARC master row, found {len(rows)}")
    return rows[0]


def main() -> None:
    body = json.loads(SOURCE_BODY.read_text(encoding="utf-8"))
    master = read_sparc_row()
    if body.get("endpoint_values_used_for_body_construction") is not False:
        raise RuntimeError("source body is not endpoint-independent")
    if body.get("status") != "SOURCE_NATIVE_OUTER_WARP_BODY_PROMOTED_WITH_SIGNIFICANCE_CAVEAT":
        raise RuntimeError("unexpected source-body state")

    distance_mpc = float(master["D_Mpc"])
    r_hi_kpc = float(master["RHI_kpc"])
    vflat_km_s = float(master["Vflat_kms"])
    onset_arcsec = float(body["warp_onset"]["radius_arcsec"])
    source_hi_arcsec = float(body["source_hi_radius"]["radius_arcsec"])

    onset_kpc_harmonized = onset_arcsec * distance_mpc * 1000.0 / 206265.0
    x_w = onset_kpc_harmonized / r_hi_kpc

    # The class-law sign, binary activation, and linear turn-on are copied
    # unchanged from the NGC4088 construction.
    q_warp = 1.0
    sigma_warp = 1.0
    turn_on_power = 1.0
    lambda_w = sigma_warp * q_warp * x_w * vflat_km_s**2

    source_outer_speed = (
        float(body["source_rotation_rise_inner_km_s"])
        + float(body["source_rotation_rise_delta_km_s"])
    )
    lambda_source_speed = sigma_warp * q_warp * x_w * source_outer_speed**2

    # Predeclared denominator sensitivity. It is not the primary unchanged law:
    # it only records the source paper's own angular R_HI definition.
    x_w_source_hi = onset_arcsec / source_hi_arcsec
    lambda_source_hi = sigma_warp * q_warp * x_w_source_hi * vflat_km_s**2

    manifest = {
        "schema": "tau_core_ugc03580_ugc3580_ngc4088_class_transfer_freeze_v01",
        "freeze_date": "2026-08-30",
        "freeze_status": "RETROSPECTIVE_SOURCE_FROZEN_CLASS_TRANSFER_READY_NOT_SCORED",
        "formula_id": FORMULA_ID,
        "galaxy": "UGC03580",
        "alias": "UGC3580",
        "source_body": str(SOURCE_BODY.relative_to(ROOT)),
        "source_body_sha256": sha256(SOURCE_BODY),
        "source_selection": {
            "criterion": "same Jozsa symmetric-warp source class as UGC08490",
            "selection_uses_pointwise_vobs_or_residual": False,
            "target_endpoint_opened_in_prior_repo_analyses": True,
            "prospective_blind_endpoint": False,
            "epistemic_role": "retrospective unchanged-law replication",
        },
        "formula": {
            "readout": "v_readout^2(R)=v_Newtonian_baryonic^2(R)+lambda_w*C_warp(R/R_HI;x_w,p)",
            "kernel": "C_warp(x;x_w,p)=q_warp*max(0,(x-x_w)/(1-x_w))^p",
            "amplitude": "lambda_w=sigma_warp*q_warp*x_w*Vflat^2",
            "q_warp": q_warp,
            "sigma_warp": sigma_warp,
            "turn_on_power": turn_on_power,
            "kernel_is_uncapped_for_x_gt_1": True,
            "post_freeze_retuning_allowed": False,
        },
        "frozen_source_inputs": {
            "warp_onset_arcsec": onset_arcsec,
            "distance_mpc": distance_mpc,
            "distance_error_mpc": float(master["e_D_Mpc"]),
            "r_hi_kpc": r_hi_kpc,
            "vflat_km_s_primary": vflat_km_s,
            "vflat_error_km_s": float(master["e_Vflat_kms"]),
            "source_hi_radius_arcsec": source_hi_arcsec,
            "source_terminal_radius_arcsec": float(body["source_terminal_radius"]["radius_arcsec"]),
            "source_outer_rotation_speed_km_s_sensitivity": source_outer_speed,
            "inner_outer_mutual_inclination_deg": float(body["inner_outer_mean_mutual_inclination_deg"]),
            "source_rotation_rise_fraction": float(body["source_rotation_rise_fraction"]),
            "source_warp_significance_caveat": True,
        },
        "derived_frozen_values": {
            "warp_onset_kpc_distance_harmonized": onset_kpc_harmonized,
            "x_w_primary_sparc_rhi": x_w,
            "lambda_w_primary_km2_s2": lambda_w,
            "lambda_w_source_speed_sensitivity_km2_s2": lambda_source_speed,
            "x_w_source_hi_denominator_sensitivity": x_w_source_hi,
            "lambda_w_source_hi_denominator_sensitivity_km2_s2": lambda_source_hi,
        },
        "independence_audit": {
            "pointwise_endpoint_curve_read_by_freeze_script": False,
            "vobs_or_residual_used_to_choose_x_w_q_sigma_p": False,
            "historical_human_exposure_to_target_endpoint": True,
            "observed_catalog_summary_Vflat_used": True,
            "observed_catalog_summary_RHI_used": True,
            "fully_kinematically_independent_amplitude_prediction": False,
        },
        "predeclared_controls": {
            "primary_normalization": "SPARC_master_Vflat_and_RHI",
            "normalization_sensitivity": "Jozsa_TiRiFiC_outer_rotation_speed",
            "denominator_sensitivity": "Jozsa_source_RHI_angular_ratio",
            "standard_comparators": ["Newtonian_baryonic", "MOND_RAR", "TPG_v6"],
            "morphology_controls": [
                "no_warp_q0",
                "wrong_onset_NGC4088_xw",
                "wrong_onset_UGC08490_xw",
                "wrong_turn_on_p2",
                "wrong_sign_sigma_minus1",
            ],
            "radial_diagnostics": ["pre_onset", "onset_to_RHI", "beyond_RHI"],
        },
        "formula_frozen_before_current_scoring_script": True,
        "endpoint_scores_allowed_in_this_step": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    manifest_digest = sha256(MANIFEST)
    MANIFEST_SHA.write_text(f"{manifest_digest}  {MANIFEST.name}\n", encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# UGC03580 / UGC3580 unchanged NGC4088-class transfer freeze v01",
                "",
                "Status: `RETROSPECTIVE_SOURCE_FROZEN_CLASS_TRANSFER_READY_NOT_SCORED`",
                "",
                "The NGC4088 formula is copied without changing its sign, binary warp",
                "activation, or linear turn-on. The UGC03580 onset comes from the Jozsa",
                "tilted-ring source; `R_HI` and primary `Vflat` come from the published",
                "SPARC master row. This freeze script does not open the pointwise curve.",
                "",
                "## Frozen values",
                "",
                f"- harmonized warp onset: `{onset_kpc_harmonized:.6f} kpc`;",
                f"- primary `x_w={x_w:.9f}`;",
                f"- primary `lambda_w={lambda_w:.6f} km^2/s^2`;",
                f"- source-speed sensitivity `lambda_w={lambda_source_speed:.6f} km^2/s^2`;",
                f"- source-native angular-denominator sensitivity `x_w={x_w_source_hi:.6f}`;",
                "- `q_warp=1`, `sigma_warp=+1`, and `p=1` remain unchanged.",
                "",
                "## Boundary",
                "",
                "This is not prospective: UGC03580 has appeared in earlier repository",
                "endpoint analyses. The source-selected class membership and parameters",
                "remain residual-independent, but the result can only test retrospective",
                "unchanged-law replication. The source itself calls this warp less",
                "significant than NGC2541 and NGC5204.",
                "",
                f"Manifest SHA-256: `{manifest_digest}`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(manifest["derived_frozen_values"], indent=2))
    print(f"manifest_sha256={manifest_digest}")


if __name__ == "__main__":
    main()
