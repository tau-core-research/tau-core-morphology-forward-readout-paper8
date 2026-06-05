#!/usr/bin/env python3
"""Build a residual-blind THINGS q_warp measurement worksheet for NGC7331.

The worksheet fixes source-native map geometry and declares the fields needed
to measure q_warp, sigma_warp, and epsilon_cross from cached THINGS H I moment
maps. It does not fill the measurements and does not score the rotation curve.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC7331"
CLAIM_BOUNDARY = "ngc7331_things_qwarp_measurement_worksheet_not_endpoint"


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

    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    onset_summary = pd.read_csv(DATA / "ngc7331_fractional_warp_onset_source_summary.csv").iloc[0]
    audit_summary = pd.read_csv(DATA / "ngc7331_things_hi_product_audit_summary.csv").iloc[0]
    manifest = pd.read_csv(DATA / "ngc7331_things_hi_product_manifest.csv")
    na_mom0_path = Path(
        manifest.loc[manifest["product_id"].eq("NA_MOM0"), "local_cache_path"].iloc[0]
    )
    header = fits.getheader(na_mom0_path)
    row = sparc.loc[sparc["Galaxy"].eq(GALAXY)].iloc[0]

    distance_mpc = float(row["D_Mpc"])
    rdisk_kpc = float(row["Rdisk_kpc"])
    rhi_kpc = float(row["RHI_kpc"])
    inc_deg = float(row["Inc_deg"])
    x_w = float(onset_summary["approx_warp_onset_over_RHI"])
    onset_kpc = x_w * rhi_kpc
    arcsec_per_pixel = abs(float(header["CDELT2"])) * 3600.0
    kpc_per_arcsec = distance_mpc * 1000.0 * math.pi / (180.0 * 3600.0)
    kpc_per_pixel = arcsec_per_pixel * kpc_per_arcsec

    geometry = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "geometry_id": "N7331_THINGS_GEOM_V1",
                "reference_product": "NGC_7331_NA_MOM0_THINGS.FITS",
                "crpix1": float(header["CRPIX1"]),
                "crpix2": float(header["CRPIX2"]),
                "crval1_deg": float(header["CRVAL1"]),
                "crval2_deg": float(header["CRVAL2"]),
                "arcsec_per_pixel": arcsec_per_pixel,
                "kpc_per_pixel": kpc_per_pixel,
                "rdisk_kpc": rdisk_kpc,
                "rhi_kpc": rhi_kpc,
                "x_warp_onset_over_rhi": x_w,
                "warp_onset_kpc": onset_kpc,
                "rdisk_pix": rdisk_kpc / kpc_per_pixel,
                "rhi_pix": rhi_kpc / kpc_per_pixel,
                "warp_onset_pix": onset_kpc / kpc_per_pixel,
                "inclination_deg": inc_deg,
                "inner_disk_pa_deg": pd.NA,
                "pa_status": "PENDING_SOURCE_MEASUREMENT_OR_LITERATURE_VALUE",
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    worksheet = pd.DataFrame(
        [
            {
                "target_id": "N7331_QW1_INNER_DISK_PA",
                "target_class": "orientation_reference",
                "source_product": "NA_MOM1;RO_MOM1;literature_PA_profile",
                "measurement": "inner_disk_pa_deg",
                "unit": "deg",
                "accepted_value": pd.NA,
                "measurement_rule": "freeze inner disk line-of-nodes/major-axis PA before measuring ridge offsets",
                "status": "MEASUREMENT_PENDING",
            },
            {
                "target_id": "N7331_QW2_OUTER_RIDGE_OFFSET_SIDE_A",
                "target_class": "q_warp_strength",
                "source_product": "NA_MOM0;RO_MOM0",
                "measurement": "outer_ridge_offset_side_a_pix",
                "unit": "pixel",
                "accepted_value": pd.NA,
                "measurement_rule": "measure residual-blind outer H I ridge displacement from inner disk reference on side A",
                "status": "MEASUREMENT_PENDING",
            },
            {
                "target_id": "N7331_QW3_OUTER_RIDGE_OFFSET_SIDE_B",
                "target_class": "q_warp_strength",
                "source_product": "NA_MOM0;RO_MOM0",
                "measurement": "outer_ridge_offset_side_b_pix",
                "unit": "pixel",
                "accepted_value": pd.NA,
                "measurement_rule": "measure residual-blind outer H I ridge displacement from inner disk reference on side B",
                "status": "MEASUREMENT_PENDING",
            },
            {
                "target_id": "N7331_QW4_LOCAL_REFERENCE_EXTENT",
                "target_class": "q_warp_normalization",
                "source_product": "NA_MOM0;RO_MOM0",
                "measurement": "local_disk_reference_extent_pix",
                "unit": "pixel",
                "accepted_value": pd.NA,
                "measurement_rule": "use same map frame; default reference candidates are warp_onset_pix to rhi_pix",
                "status": "MEASUREMENT_PENDING",
            },
            {
                "target_id": "N7331_QW5_SIDE_RELIABILITY_WEIGHTS",
                "target_class": "q_warp_weighting",
                "source_product": "NA_MOM0;RO_MOM0;source_quality_review",
                "measurement": "side_a_weight;side_b_weight",
                "unit": "dimensionless",
                "accepted_value": pd.NA,
                "measurement_rule": "assign side weights from source quality only, not from rotation residuals",
                "status": "MEASUREMENT_PENDING",
            },
            {
                "target_id": "N7331_QW6_SIGMA_WARP_SIGN",
                "target_class": "sign_rule",
                "source_product": "NA_MOM1;RO_MOM1;Bosma tilted-ring context",
                "measurement": "sigma_warp_sign",
                "unit": "sign_or_enum",
                "accepted_value": pd.NA,
                "measurement_rule": "decide added-readout vs attenuation from source-side orientation/readout geometry",
                "status": "MEASUREMENT_PENDING",
            },
            {
                "target_id": "N7331_QW7_EPSILON_CROSS_BOUND",
                "target_class": "cross_term_bound",
                "source_product": "NA_MOM0;NA_MOM1;RO_MOM0;RO_MOM1;context_sources",
                "measurement": "epsilon_cross_bound_or_interval",
                "unit": "dimensionless",
                "accepted_value": pd.NA,
                "measurement_rule": "bound orientation, side-asymmetry, history/context, and locality cross terms",
                "status": "MEASUREMENT_PENDING",
            },
        ]
    )
    worksheet["galaxy"] = GALAXY
    worksheet["endpoint_scores_allowed"] = False
    worksheet["uses_vobs_or_residual"] = False
    worksheet["claim_boundary"] = CLAIM_BOUNDARY
    worksheet = worksheet[
        [
            "galaxy",
            "target_id",
            "target_class",
            "source_product",
            "measurement",
            "unit",
            "accepted_value",
            "measurement_rule",
            "status",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    response = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "response_id": "N7331_THINGS_QWARP_RESPONSE_V1",
                "inner_disk_pa_deg": pd.NA,
                "outer_ridge_offset_side_a_pix": pd.NA,
                "outer_ridge_offset_side_b_pix": pd.NA,
                "local_disk_reference_extent_pix": pd.NA,
                "side_a_weight": pd.NA,
                "side_b_weight": pd.NA,
                "q_warp_measured": pd.NA,
                "q_warp_uncertainty": pd.NA,
                "sigma_warp_sign": pd.NA,
                "epsilon_cross_bound_or_interval": pd.NA,
                "response_status": "RESPONSE_EMPTY_MEASUREMENT_PENDING",
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_QWG1_THINGS_PRODUCTS_AUDITED",
                "gate_status": "PASS" if bool(audit_summary["worksheet_ready"]) else "BLOCKED",
                "evidence": str(audit_summary["things_hi_product_audit_status"]),
                "remaining_obligation": "none at product-audit level",
            },
            {
                "gate_id": "N7331_QWG2_GEOMETRY_SCALES_DEFINED",
                "gate_status": "PASS",
                "evidence": f"Rdisk={rdisk_kpc:.3f} kpc, RHI={rhi_kpc:.3f} kpc, x_w={x_w:.6g}",
                "remaining_obligation": "none at scalar geometry level",
            },
            {
                "gate_id": "N7331_QWG3_PA_REFERENCE",
                "gate_status": "BLOCKED_MEASUREMENT_PENDING",
                "evidence": "inner_disk_pa_deg is not frozen in this worksheet",
                "remaining_obligation": "measure from THINGS MOM1/MOM0 or cite source PA profile",
            },
            {
                "gate_id": "N7331_QWG4_Q_WARP_RESPONSE",
                "gate_status": "BLOCKED_MEASUREMENT_PENDING",
                "evidence": "q_warp response fields are empty",
                "remaining_obligation": "fill ridge offsets, reference extent, and side weights",
            },
            {
                "gate_id": "N7331_QWG5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS",
                "evidence": "worksheet uses map geometry and source products only",
                "remaining_obligation": "do not score until formula freeze passes",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "qwarp_worksheet_status": "NGC7331_THINGS_QWARP_WORKSHEET_READY_MEASUREMENT_PENDING",
                "n_measurement_targets": len(worksheet),
                "n_gates": len(gates),
                "n_pass": int(gates["gate_status"].eq("PASS").sum()),
                "n_blocked": int(gates["gate_status"].str.startswith("BLOCKED").sum()),
                "things_products_audited": bool(audit_summary["worksheet_ready"]),
                "geometry_defined": True,
                "pa_reference_frozen": False,
                "q_warp_measurement_ready": False,
                "sigma_warp_sign_ready": False,
                "epsilon_cross_bound_ready": False,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "population_claim_allowed": False,
                "next_required_action": "fill inner PA, ridge offsets, side weights, sign, and cross-term response fields",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    geometry.to_csv(DATA / "ngc7331_things_qwarp_measurement_geometry.csv", index=False)
    worksheet.to_csv(DATA / "ngc7331_things_qwarp_measurement_worksheet.csv", index=False)
    response.to_csv(DATA / "ngc7331_things_qwarp_measurement_response_template.csv", index=False)
    gates.to_csv(DATA / "ngc7331_things_qwarp_measurement_gate.csv", index=False)
    summary.to_csv(DATA / "ngc7331_things_qwarp_measurement_summary.csv", index=False)

    report = [
        "# NGC7331 THINGS q_warp Measurement Worksheet",
        "",
        "This worksheet fixes the source-native THINGS map geometry and declares",
        "the residual-blind measurements needed for q_warp, sigma_warp, and",
        "epsilon_cross. It does not fill those measurements and does not score",
        "the rotation curve.",
        "",
        "## Geometry",
        "",
        markdown_table(geometry),
        "",
        "## Worksheet",
        "",
        markdown_table(worksheet),
        "",
        "## Response Template",
        "",
        markdown_table(response),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
    ]
    (REPORTS / "ngc7331_things_qwarp_measurement_worksheet.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
