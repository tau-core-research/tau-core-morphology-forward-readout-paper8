#!/usr/bin/env python3
"""Build the NGC4088 B1 source-native radial calibration packet.

B1 is not only an image-feature problem.  A warp-like bend must be converted to
a source-native onset radius before x_w can be accepted for formula freeze.  The
first-pass conversion is dimensionally valid, but the frozen image repeat is
still inconclusive because the machine repeat does not yet have an accepted
radial calibration.  This packet records the allowed calibration routes without
using endpoint residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_b1_source_native_radial_calibration_packet_not_endpoint"


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

    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    repeat = pd.read_csv(DATA / "ngc4088_b1_frozen_image_repeat_summary.csv").iloc[0]
    gate = pd.read_csv(DATA / "s4g75_ngc4088_warp_asymmetry_extraction_gate.csv").iloc[0]

    hi_radius_arcmin = float(xw["hi_radius_arcmin"])
    first_pass_onset_arcmin = float(xw["combined_onset_arcmin"])
    first_pass_xw = float(xw["x_warp_onset"])
    first_pass_uncertainty_arcmin = float(xw["x_warp_uncertainty"]) * hi_radius_arcmin

    formulas = pd.DataFrame(
        [
            {
                "quantity": "R_HI_arcmin",
                "formula": "0.5 * D_HI_arcmin",
                "value": hi_radius_arcmin,
                "unit": "arcmin",
                "source": "Verheijen-Sancisi HI diameter",
                "status": "SOURCE_NATIVE_READY",
            },
            {
                "quantity": "x_w",
                "formula": "R_warp_onset_arcmin / R_HI_arcmin",
                "value": first_pass_xw,
                "unit": "dimensionless",
                "source": "first-pass manual digitization plus HI radius",
                "status": "FIRST_PASS_DIMENSIONALLY_VALID_NOT_B1_ACCEPTED",
            },
            {
                "quantity": "Delta_x_w",
                "formula": "Delta_R_onset_arcmin / R_HI_arcmin",
                "value": first_pass_uncertainty_arcmin / hi_radius_arcmin,
                "unit": "dimensionless",
                "source": "frozen first-pass tolerance",
                "status": "FIRST_PASS_TOLERANCE_NOT_B1_ACCEPTED",
            },
        ]
    )
    formulas["endpoint_scores_allowed"] = False
    formulas["uses_vobs_or_residual"] = False
    formulas["claim_boundary"] = CLAIM_BOUNDARY

    routes = pd.DataFrame(
        [
            {
                "route_id": "RC1_INDEPENDENT_REVIEWER_DIRECT_ARCMIN",
                "route_status": "READY",
                "allowed_inputs": "page76 ROI; worksheet overlay; page77 cross-check; HI diameter",
                "required_output": "onset_radius_side_a_arcmin; onset_radius_side_b_arcmin; x_w_independent",
                "acceptance_condition": "numeric side onsets and |x_w_independent-first_pass_x_w| <= frozen tolerance",
                "why_not_currently_closed": "review response remains pending",
            },
            {
                "route_id": "RC2_FROZEN_IMAGE_REPEAT_WITH_RADIAL_TICK_CALIBRATION",
                "route_status": "OPEN",
                "allowed_inputs": "page76 ROI; worksheet grid; printed coordinate/radial ticks; HI diameter",
                "required_output": "arcmin_per_pixel_or_direct_radial_axis_mapping plus onset radius",
                "acceptance_condition": "calibration reproducibly maps image departure to arcmin before scoring",
                "why_not_currently_closed": "current image repeat detects PA departure but lacks accepted source-native radial calibration",
            },
            {
                "route_id": "RC3_ORIGINAL_CHANNEL_MAP_DATA_ROUTE",
                "route_status": "PREFERRED_OPEN_IF_AVAILABLE",
                "allowed_inputs": "original WHISP/FITS channel-map product or table with source-native coordinates",
                "required_output": "source-native warp onset radius with uncertainty",
                "acceptance_condition": "coordinate-calibrated source product reproduces or revises x_w without endpoint inputs",
                "why_not_currently_closed": "original data product is not yet cached in this package",
            },
            {
                "route_id": "RC4_FIRST_PASS_ONLY",
                "route_status": "NOT_ACCEPTABLE_FOR_FORMULA_FREEZE_ALONE",
                "allowed_inputs": "existing first-pass manual digitization",
                "required_output": "none",
                "acceptance_condition": "not applicable",
                "why_not_currently_closed": "dimensionally valid but not independent and not enough for B1 closure",
            },
        ]
    )
    routes["endpoint_scores_allowed"] = False
    routes["uses_vobs_or_residual"] = False
    routes["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "calibration_packet_status": "B1_SOURCE_NATIVE_RADIAL_CALIBRATION_PACKET_CREATED",
                "radial_calibration_acceptance_status": "RADIAL_CALIBRATION_NOT_ACCEPTED",
                "b1_resolution_status": "B1_NOT_RESOLVED_RADIAL_CALIBRATION_OPEN",
                "first_pass_x_w": first_pass_xw,
                "first_pass_onset_arcmin": first_pass_onset_arcmin,
                "first_pass_uncertainty_arcmin": first_pass_uncertainty_arcmin,
                "hi_diameter_arcmin": float(gate["source_native_hi_diameter_arcmin"]),
                "hi_radius_arcmin": hi_radius_arcmin,
                "image_repeat_status": str(repeat["repeat_attempt_status"]),
                "n_ready_routes": int(routes["route_status"].eq("READY").sum()),
                "n_open_routes": int(routes["route_status"].str.contains("OPEN").sum()),
                "accepted_x_w_for_formula_freeze": False,
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "complete RC1 independent reviewer response, or close RC2/RC3 "
                    "with source-native radial calibration before accepting x_w"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    formulas.to_csv(DATA / "ngc4088_b1_source_native_radial_calibration_formulas.csv", index=False)
    routes.to_csv(DATA / "ngc4088_b1_source_native_radial_calibration_routes.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b1_source_native_radial_calibration_summary.csv", index=False)

    report = [
        "# NGC4088 B1 Source-Native Radial Calibration Packet",
        "",
        "This packet separates warp-like image evidence from accepted source-native",
        "radial calibration. It does not use observed rotation residuals and does",
        "not authorize endpoint scoring.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Calibration Formula Ledger",
        "",
        markdown_table(formulas),
        "",
        "## Allowed Closure Routes",
        "",
        markdown_table(routes),
        "",
        "## Interpretation",
        "",
        "The first-pass x_w conversion is dimensionally valid, and the frozen image",
        "repeat detects a warp-like position-angle departure. B1 remains open",
        "because an accepted source-native radial calibration is still missing for",
        "the machine repeat, and the independent reviewer response is not filled.",
        "",
    ]
    (REPORTS / "ngc4088_b1_source_native_radial_calibration_packet.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
