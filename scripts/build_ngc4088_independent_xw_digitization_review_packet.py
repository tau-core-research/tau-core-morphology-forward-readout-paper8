#!/usr/bin/env python3
"""Build the independent NGC4088 x_w digitization review packet.

This gate prepares the residual-blind second-review route for B1.  It does not
change the first-pass x_w value, does not infer from rotation residuals, and
does not authorize endpoint scoring.  It specifies the acceptance rule for a
future independent reviewer or frozen image-analysis repeat.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_independent_xw_digitization_review_not_endpoint"

SOURCE_IMAGES = [
    "data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76_channel_maps_roi.png",
    "data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_76_channel_maps_roi_worksheet_overlay.png",
    "data/external/literature/2001_verheijen_sancisi_pages/ngc4088_page_77-077.png",
]


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
    response = pd.read_csv(
        DATA / "s4g75_ngc4088_channel_map_digitization_response_template.csv"
    ).iloc[0]
    protocol = pd.read_csv(DATA / "s4g75_ngc4088_channel_map_digitization_protocol.csv")

    first_pass_xw = float(xw["x_warp_onset"])
    first_pass_unc = float(xw["x_warp_uncertainty"])
    first_pass_onset_arcmin = float(xw["combined_onset_arcmin"])
    tolerance_xw = max(first_pass_unc, 0.05)
    tolerance_arcmin = float(xw["hi_radius_arcmin"]) * tolerance_xw

    packet = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "review_packet_id": "NGC4088_INDEPENDENT_XW_DIGITIZATION_REVIEW_PACKET_V1",
                "review_route": "INDEPENDENT_MANUAL_OR_FROZEN_IMAGE_ANALYSIS_REPEAT",
                "first_pass_digitizer_id": response["digitizer_id"],
                "first_pass_x_w": first_pass_xw,
                "first_pass_onset_arcmin": first_pass_onset_arcmin,
                "first_pass_uncertainty_x_w": first_pass_unc,
                "acceptance_tolerance_x_w": tolerance_xw,
                "acceptance_tolerance_arcmin": tolerance_arcmin,
                "source_images": ";".join(SOURCE_IMAGES),
                "forbidden_inputs": (
                    "vobs;rotation_residual;endpoint_score;best_fit_family;"
                    "required_S_tau_diagnostic"
                ),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    obligations = pd.DataFrame(
        [
            {
                "obligation_id": "XWREV1_SOURCE_LOCK",
                "obligation_status": "READY",
                "requirement": "reviewer must use only the frozen page-76 ROI, worksheet overlay, and page-77 cross-check image",
                "acceptance_condition": "source_images_used must be a subset of the packet source image list",
            },
            {
                "obligation_id": "XWREV2_INDEPENDENT_REVIEWER",
                "obligation_status": "PENDING",
                "requirement": "reviewer identity or frozen image-analysis method must differ from first_pass_digitizer_id",
                "acceptance_condition": "independent_reviewer_id != first_pass_digitizer_id OR method_id is a frozen script/hash",
            },
            {
                "obligation_id": "XWREV3_NO_ENDPOINT_INPUTS",
                "obligation_status": "READY",
                "requirement": "review notes and method must not use endpoint residuals, vobs, or fit ranks",
                "acceptance_condition": "forbidden_input_detected=False",
            },
            {
                "obligation_id": "XWREV4_SIDE_BY_SIDE_ONSET_REPEAT",
                "obligation_status": "PENDING",
                "requirement": "repeat side-A and side-B onset measurements under the frozen protocol",
                "acceptance_condition": "independent onset fields are numeric and side_combination_rule_applied is frozen",
            },
            {
                "obligation_id": "XWREV5_TOLERANCE_OR_ESCALATION",
                "obligation_status": "PENDING",
                "requirement": "compare independent x_w to the first-pass value before any endpoint use",
                "acceptance_condition": (
                    f"|x_w_independent - {first_pass_xw:.6g}| <= {tolerance_xw:.6g}; "
                    "otherwise freeze an uncertainty interval or mark x_w unresolved"
                ),
            },
        ]
    )
    obligations["endpoint_scores_allowed"] = False
    obligations["claim_boundary"] = CLAIM_BOUNDARY

    response_template = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "review_packet_id": packet.iloc[0]["review_packet_id"],
                "independent_reviewer_id": "PENDING_INDEPENDENT_REVIEW",
                "review_timestamp_utc": "PENDING_INDEPENDENT_REVIEW",
                "review_method_id": "PENDING_INDEPENDENT_REVIEW",
                "source_images_used": "PENDING_INDEPENDENT_REVIEW",
                "inner_disk_axis_pa_deg": "PENDING_INDEPENDENT_REVIEW",
                "outer_ridge_axis_side_a_pa_deg": "PENDING_INDEPENDENT_REVIEW",
                "outer_ridge_axis_side_b_pa_deg": "PENDING_INDEPENDENT_REVIEW",
                "onset_radius_side_a_arcmin": "PENDING_INDEPENDENT_REVIEW",
                "onset_radius_side_b_arcmin": "PENDING_INDEPENDENT_REVIEW",
                "side_combination_rule_applied": "PENDING_INDEPENDENT_REVIEW",
                "xw_combined_arcmin": "PENDING_INDEPENDENT_REVIEW",
                "uncertainty_arcmin": "PENDING_INDEPENDENT_REVIEW",
                "x_w_independent": "PENDING_INDEPENDENT_REVIEW",
                "review_notes": "PENDING_INDEPENDENT_REVIEW",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    protocol_digest = pd.DataFrame(
        [
            {
                "protocol_rule_count": len(protocol),
                "required_review_obligations": len(obligations),
                "ready_obligations": int(obligations["obligation_status"].eq("READY").sum()),
                "pending_obligations": int(
                    obligations["obligation_status"].eq("PENDING").sum()
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "review_status": "INDEPENDENT_XW_REVIEW_PACKET_READY_RESPONSE_PENDING",
                "b1_resolution_status": "B1_NOT_RESOLVED_INDEPENDENT_REVIEW_PENDING",
                "first_pass_x_w": first_pass_xw,
                "acceptance_tolerance_x_w": tolerance_xw,
                "n_pending_obligations": int(
                    obligations["obligation_status"].eq("PENDING").sum()
                ),
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    packet.to_csv(DATA / "ngc4088_independent_xw_digitization_review_packet.csv", index=False)
    obligations.to_csv(
        DATA / "ngc4088_independent_xw_digitization_review_obligations.csv", index=False
    )
    response_template.to_csv(
        DATA / "ngc4088_independent_xw_digitization_review_response_template.csv",
        index=False,
    )
    protocol_digest.to_csv(
        DATA / "ngc4088_independent_xw_digitization_review_protocol_digest.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ngc4088_independent_xw_digitization_review_summary.csv", index=False
    )

    report = [
        "# NGC4088 Independent x_w Digitization Review Packet",
        "",
        "This is the residual-blind second-review route for blocker B1. It prepares",
        "the independent review of the current first-pass x_w digitization. It does",
        "not change x_w, does not score rotations, and does not authorize endpoint",
        "use.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Review Packet",
        "",
        markdown_table(packet),
        "",
        "## Obligations",
        "",
        markdown_table(obligations),
        "",
        "## Response Template",
        "",
        markdown_table(response_template),
        "",
        "## Interpretation",
        "",
        "The current first-pass x_w value is protocol-usable for preflight mapping,",
        "but B1 remains unresolved. To close B1, an independent reviewer or frozen",
        "image-analysis repeat must reproduce the side-by-side onset measurement",
        "without endpoint inputs and must either agree within the frozen tolerance",
        "or explicitly widen/freeze the source-side uncertainty interval.",
        "",
    ]
    (REPORTS / "ngc4088_independent_xw_digitization_review_packet.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
