#!/usr/bin/env python3
"""Freeze an unchanged NGC4088 warp/history-law transfer to UGC08490.

This source-side step must run before the pointwise UGC08490 rotation endpoint
is read by the companion scorer.  It consumes only the promoted TiRiFiC warp
body and the published SPARC master-table summary row.  The target endpoint is
known to have been opened in earlier, different tracer analyses, so this is a
retrospective class-transfer freeze rather than a prospective blind endpoint.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

SOURCE_BODY = DATA / "ugc08490_ngc5204_warp_body_v01.json"
SPARC_MASTER = DATA / "external_sparc_master_table.csv"
MANIFEST = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_freeze_v01.json"
MANIFEST_SHA = DATA / "ugc08490_ngc5204_ngc4088_class_transfer_freeze_v01.sha256"
REPORT = REPORTS / "ugc08490_ngc5204_ngc4088_class_transfer_freeze_v01.md"

FORMULA_ID = "NGC4088_WARP_HISTORY_CLASS_V1__UGC08490_TRANSFER_V01"
CLAIM_BOUNDARY = "retrospective_source_frozen_class_transfer_not_tau_validation"


def read_sparc_row() -> dict[str, str]:
    with SPARC_MASTER.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row["Galaxy"] == "UGC08490"]
    if len(rows) != 1:
        raise RuntimeError(f"expected one UGC08490 SPARC master row, found {len(rows)}")
    return rows[0]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    body = json.loads(SOURCE_BODY.read_text(encoding="utf-8"))
    master = read_sparc_row()

    if body.get("endpoint_values_used_for_body_construction") is not False:
        raise RuntimeError("source warp body is not certified endpoint-independent")
    if body.get("status") != "SOURCE_NATIVE_TWO_PLANE_WARP_BODY_PROMOTED_OUTER_MODE_ONLY":
        raise RuntimeError("unexpected UGC08490 source-body promotion state")

    distance_mpc = float(master["D_Mpc"])
    r_hi_kpc = float(master["RHI_kpc"])
    vflat_km_s = float(master["Vflat_kms"])
    onset_arcsec = float(body["warp_onset"]["radius_arcsec"])

    # Put the angular source onset and the catalog R_HI on one distance scale.
    onset_kpc_harmonized = onset_arcsec * distance_mpc * 1000.0 / 206265.0
    x_w = onset_kpc_harmonized / r_hi_kpc

    # These three choices are copied unchanged from the NGC4088 class law.
    q_warp = 1.0
    sigma_warp = 1.0
    turn_on_power = 1.0
    lambda_w = sigma_warp * q_warp * x_w * vflat_km_s**2

    # Predeclared normalization sensitivity from the independent TiRiFiC source.
    source_outer_speed = (
        float(body["source_rotation_rise_inner_km_s"])
        + float(body["source_rotation_rise_delta_km_s"])
    )
    lambda_source_speed = sigma_warp * q_warp * x_w * source_outer_speed**2

    manifest = {
        "schema": "tau_core_ugc08490_ngc5204_ngc4088_class_transfer_freeze_v01",
        "freeze_date": "2026-08-30",
        "freeze_status": "RETROSPECTIVE_SOURCE_FROZEN_CLASS_TRANSFER_READY_NOT_SCORED",
        "formula_id": FORMULA_ID,
        "galaxy": "UGC08490",
        "alias": "NGC5204",
        "source_body": str(SOURCE_BODY.relative_to(ROOT)),
        "source_body_sha256": sha256(SOURCE_BODY),
        "source_selection": {
            "criterion": "promoted source-native outer two-plane warp plus public SPARC endpoint",
            "selection_uses_pointwise_vobs_or_residual": False,
            "target_endpoint_opened_in_prior_other_analysis": True,
            "prospective_blind_endpoint": False,
            "epistemic_role": "retrospective unchanged-law class transfer",
        },
        "formula": {
            "readout": "v_readout^2(R)=v_Newtonian_baryonic^2(R)+lambda_w*C_warp(R/R_HI;x_w,p)",
            "kernel": "C_warp(x;x_w,p)=q_warp*max(0,(x-x_w)/(1-x_w))^p",
            "amplitude": "lambda_w=sigma_warp*q_warp*x_w*Vflat^2",
            "q_warp": q_warp,
            "sigma_warp": sigma_warp,
            "turn_on_power": turn_on_power,
            "post_freeze_retuning_allowed": False,
        },
        "frozen_source_inputs": {
            "warp_onset_arcsec": onset_arcsec,
            "distance_mpc": distance_mpc,
            "r_hi_kpc": r_hi_kpc,
            "vflat_km_s_primary": vflat_km_s,
            "vflat_error_km_s": float(master["e_Vflat_kms"]),
            "source_outer_rotation_speed_km_s_sensitivity": source_outer_speed,
            "inner_outer_mutual_inclination_deg": float(
                body["inner_outer_mean_mutual_inclination_deg"]
            ),
            "source_rotation_rise_fraction": float(body["source_rotation_rise_fraction"]),
        },
        "derived_frozen_values": {
            "warp_onset_kpc_distance_harmonized": onset_kpc_harmonized,
            "x_w": x_w,
            "lambda_w_primary_km2_s2": lambda_w,
            "lambda_w_source_speed_sensitivity_km2_s2": lambda_source_speed,
        },
        "independence_audit": {
            "pointwise_endpoint_curve_read_by_freeze": False,
            "vobs_or_residual_used_to_choose_x_w_q_sigma_p": False,
            "observed_catalog_summary_Vflat_used": True,
            "observed_catalog_summary_RHI_used": True,
            "fully_kinematically_independent_amplitude_prediction": False,
            "note": (
                "Vflat and RHI are published SPARC summary inputs. The transfer tests the "
                "unchanged morphology-conditioned radial law, not a zero-information "
                "prediction of its complete dimensional amplitude."
            ),
        },
        "predeclared_controls": {
            "primary_normalization": "SPARC_master_Vflat",
            "normalization_sensitivity": "Jozsa_TiRiFiC_outer_rotation_speed",
            "standard_comparators": ["Newtonian_baryonic", "MOND_RAR"],
            "morphology_controls": [
                "no_warp_q0",
                "wrong_onset_NGC4088_xw",
                "wrong_turn_on_p2",
                "wrong_sign_sigma_minus1",
            ],
            "score": "error-weighted_chi2_and_unweighted_RMSE",
            "radial_diagnostics": ["pre_onset", "post_onset"],
        },
        "formula_frozen_before_current_endpoint_scoring": True,
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
                "# UGC08490 / NGC5204 unchanged NGC4088-class transfer freeze v01",
                "",
                "Status: `RETROSPECTIVE_SOURCE_FROZEN_CLASS_TRANSFER_READY_NOT_SCORED`",
                "",
                "The NGC4088 warp/history formula is copied without changing its sign,",
                "binary warp activation, or linear turn-on. The UGC08490-specific onset",
                "comes from the promoted TiRiFiC two-plane warp body; `R_HI` and the",
                "primary `Vflat` come from the published SPARC master row. No pointwise",
                "`vobs` value or endpoint residual is read by this freeze step.",
                "",
                "## Frozen values",
                "",
                f"- harmonized warp onset: `{onset_kpc_harmonized:.6f} kpc`;",
                f"- `x_w = {x_w:.9f}`;",
                f"- primary `Vflat = {vflat_km_s:.3f} km/s`;",
                f"- primary `lambda_w = {lambda_w:.6f} km^2/s^2`;",
                f"- predeclared external-source sensitivity `V = {source_outer_speed:.3f} km/s`,",
                f"  giving `lambda_w = {lambda_source_speed:.6f} km^2/s^2`;",
                "- `q_warp=1`, `sigma_warp=+1`, and `p=1` are unchanged class-law choices.",
                "",
                "## Epistemic boundary",
                "",
                "This is not a prospective blind endpoint: UGC08490 was opened in earlier,",
                "different tracer analyses. It is nevertheless a valid frozen-formula",
                "retrospective transfer check because the current pointwise endpoint and",
                "its residuals did not select the transfer parameters. The use of catalog",
                "`Vflat` means this is not a fully kinematically independent amplitude",
                "prediction; it primarily tests whether the source-selected warp onset and",
                "unchanged radial law transfer.",
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
