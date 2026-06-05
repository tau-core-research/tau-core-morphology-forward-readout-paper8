#!/usr/bin/env python3
"""Build a consolidated NGC4088 formula-freeze readiness dashboard.

The earlier NGC4088 scripts split the fourth-endpoint candidate into B1/B2/B3
blockers.  This script keeps those blocker states in one reproducible ledger so
the paper and bridge hub can say, without ambiguity, whether endpoint scoring is
allowed.  It is a status synthesis only: it reads no observed residuals and does
not score a rotation curve.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_formula_freeze_readiness_dashboard_not_endpoint"


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


def bool_value(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    plan = pd.read_csv(
        DATA / "ngc4088_mixed_formula_freeze_blocker_resolution_summary.csv"
    ).iloc[0]
    b1 = pd.read_csv(DATA / "ngc4088_independent_xw_digitization_review_summary.csv").iloc[0]
    b1_repeat = pd.read_csv(DATA / "ngc4088_b1_frozen_image_repeat_summary.csv").iloc[0]
    b1_calibration = pd.read_csv(
        DATA / "ngc4088_b1_source_native_radial_calibration_summary.csv"
    ).iloc[0]
    b1_original_data = pd.read_csv(
        DATA / "ngc4088_b1_original_hi_data_acquisition_summary.csv"
    ).iloc[0]
    b1_whisp_overview = pd.read_csv(
        DATA / "ngc4088_b1_whisp_overview_extraction_summary.csv"
    ).iloc[0]
    b1_whisp_frozen = pd.read_csv(
        DATA / "ngc4088_b1_whisp_overview_frozen_extraction_summary.csv"
    ).iloc[0]
    b1_whisp_promotion = pd.read_csv(
        DATA / "ngc4088_b1_whisp_promotion_review_summary.csv"
    ).iloc[0]
    b2 = pd.read_csv(DATA / "ngc4088_b2_physical_normalization_synthesis_summary.csv").iloc[0]
    b3 = pd.read_csv(DATA / "ngc4088_b3_scale_uniqueness_synthesis_summary.csv").iloc[0]
    freeze_path = DATA / "ngc4088_warp_history_formula_freeze_summary.csv"
    freeze = pd.read_csv(freeze_path).iloc[0] if freeze_path.exists() else None
    b1_resolved_for_formula_freeze = bool_value(
        b1_whisp_promotion["accepted_x_w_for_formula_freeze"]
    )
    b2_resolved_for_formula_freeze = bool(freeze is not None) and str(
        freeze["b2_protocol_status"]
    ) == "B2_PROTOCOL_FORMULA_FREEZE_READY_LAW_LEVEL_OPEN"
    b3_resolved_for_formula_freeze = bool(freeze is not None) and str(
        freeze["b3_protocol_status"]
    ) == "B3_PROTOCOL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_OPEN"
    formula_freeze_gate_ready = bool(freeze is not None) and bool_value(
        freeze["formula_frozen_before_endpoint_scoring"]
    )

    blocker_rows = [
        {
            "blocker_id": "B1_INDEPENDENT_XW_DIGITIZATION_REVIEW",
            "current_status": str(b1_whisp_promotion["b1_resolution_status"]),
            "resolved_for_formula_freeze": b1_resolved_for_formula_freeze,
            "why_still_blocking": (
                "resolved with caveat: WHISP graphical overview frozen extraction agrees with first-pass; "
                "direct source-coordinate H I product remains missing"
                if b1_resolved_for_formula_freeze
                else (
                    "independent side-by-side x_w review response is still pending; "
                    f"frozen image repeat status is {b1_repeat['b1_resolution_status']}; "
                    f"radial calibration status is {b1_calibration['b1_resolution_status']}; "
                    f"original-data route status is {b1_original_data['b1_resolution_status']}; "
                    f"WHISP overview extraction status is {b1_whisp_overview['b1_resolution_status']}; "
                    f"frozen WHISP extraction status is {b1_whisp_frozen['b1_resolution_status']}; "
                    f"WHISP promotion review status is {b1_whisp_promotion['b1_resolution_status']}"
                )
            ),
            "next_required_action": (
                "carry WHISP graphical-overview provenance caveat into formula freeze; cache direct source-coordinate H I product when available"
                if b1_resolved_for_formula_freeze
                else (
                    "complete an independent B1 promotion response, add calibrated frozen-image radial ticks, "
                    "or cache a direct source-coordinate H I product"
                )
            ),
            "supporting_summary_file": "ngc4088_b1_whisp_promotion_review_summary.csv",
        },
        {
            "blocker_id": "B2_PHYSICAL_NORMALIZATION_LAW",
            "current_status": (
                str(freeze["b2_protocol_status"])
                if b2_resolved_for_formula_freeze
                else str(b2["b2_synthesis_status"])
            ),
            "resolved_for_formula_freeze": b2_resolved_for_formula_freeze,
            "why_still_blocking": (
                "resolved only at protocol formula-freeze level; law-level physical normalization remains open"
                if b2_resolved_for_formula_freeze
                else str(b2["law_quality"])
            ),
            "next_required_action": (
                "use the frozen protocol manifest for any later accepted endpoint gate; keep B2 law-level caveat attached"
                if b2_resolved_for_formula_freeze
                else str(b2["next_required_action"])
            ),
            "supporting_summary_file": (
                "ngc4088_warp_history_formula_freeze_summary.csv"
                if b2_resolved_for_formula_freeze
                else "ngc4088_b2_physical_normalization_synthesis_summary.csv"
            ),
        },
        {
            "blocker_id": "B3_SCALE_UNIQUENESS",
            "current_status": (
                str(freeze["b3_protocol_status"])
                if b3_resolved_for_formula_freeze
                else str(b3["b3_synthesis_status"])
            ),
            "resolved_for_formula_freeze": b3_resolved_for_formula_freeze,
            "why_still_blocking": (
                "resolved only at protocol formula-freeze level; law-level uniqueness remains open"
                if b3_resolved_for_formula_freeze
                else "conditional uniqueness is resolved, but law-level uniqueness is still open"
            ),
            "next_required_action": (
                "use CURRENT_XW_VFLAT2 from the frozen manifest for any later accepted endpoint gate; keep B3 law-level caveat attached"
                if b3_resolved_for_formula_freeze
                else str(b3["next_required_action"])
            ),
            "supporting_summary_file": (
                "ngc4088_warp_history_formula_freeze_summary.csv"
                if b3_resolved_for_formula_freeze
                else "ngc4088_b3_scale_uniqueness_synthesis_summary.csv"
            ),
        },
    ]
    blockers = pd.DataFrame(blocker_rows)
    blockers["endpoint_scores_allowed"] = False
    blockers["uses_vobs_or_residual"] = False
    blockers["claim_boundary"] = CLAIM_BOUNDARY

    n_local_blockers = len(blockers)
    n_resolved = int(blockers["resolved_for_formula_freeze"].sum())
    formula_freeze_allowed = n_resolved == n_local_blockers and formula_freeze_gate_ready
    endpoint_scores_allowed = False

    summary = pd.DataFrame(
        [
            {
                "dashboard_status": "NGC4088_FORMULA_FREEZE_READINESS_DASHBOARD_CREATED",
                "galaxy": "NGC4088",
                "candidate_readout": str(plan["candidate_readout"]),
                "b1_status": str(b1["b1_resolution_status"]),
                "b1_formula_freeze_status": str(
                    b1_whisp_promotion["b1_resolution_status"]
                ),
                "b1_repeat_status": str(b1_repeat["repeat_attempt_status"]),
                "b1_radial_calibration_status": str(
                    b1_calibration["radial_calibration_acceptance_status"]
                ),
                "b1_original_data_route_status": str(
                    b1_original_data["original_hi_data_audit_status"]
                ),
                "b1_whisp_overview_extraction_status": str(
                    b1_whisp_overview["whisp_overview_extraction_status"]
                ),
                "b1_whisp_frozen_extraction_status": str(
                    b1_whisp_frozen["frozen_extraction_attempt_status"]
                ),
                "b1_whisp_frozen_x_w_review": float(b1_whisp_frozen["x_w_review"]),
                "b1_whisp_frozen_agrees_with_first_pass": bool_value(
                    b1_whisp_frozen["agrees_with_first_pass_within_tolerance"]
                ),
                "b1_whisp_promotion_status": str(
                    b1_whisp_promotion["promotion_review_status"]
                ),
                "b1_source_consistency_promoted": bool_value(
                    b1_whisp_promotion["source_consistency_promoted"]
                ),
                "b1_x_w_source_consistency_value": float(
                    b1_whisp_promotion["x_w_source_consistency_value"]
                ),
                "b1_accepted_x_w_for_formula_freeze": bool_value(
                    b1_whisp_promotion["accepted_x_w_for_formula_freeze"]
                ),
                "b2_status": str(b2["b2_synthesis_status"]),
                "b3_status": str(b3["b3_synthesis_status"]),
                "warp_history_formula_freeze_status": (
                    str(freeze["formula_freeze_status"])
                    if freeze is not None
                    else "NGC4088_WARP_HISTORY_FORMULA_FREEZE_NOT_RUN"
                ),
                "warp_history_lambda_w_km2_s2": (
                    float(freeze["lambda_w_km2_s2"]) if freeze is not None else float("nan")
                ),
                "warp_history_turn_on_power_frozen": (
                    float(freeze["turn_on_power_frozen"]) if freeze is not None else float("nan")
                ),
                "b2_law_level_open": True,
                "b3_law_level_open": True,
                "n_local_blockers": n_local_blockers,
                "n_resolved_local_blockers": n_resolved,
                "formula_freeze_allowed_now": formula_freeze_allowed,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "uses_vobs_or_residual": False,
                "readiness_decision": (
                    "FORMULA_FREEZE_READY_ENDPOINT_GATE_REQUIRED"
                    if formula_freeze_allowed
                    else (
                        "B1_CLOSED_B2_B3_BLOCKED_PREFLIGHT_READY"
                        if b1_resolved_for_formula_freeze
                        else "PROMOTION_BLOCKED_PREFLIGHT_READY"
                    )
                ),
                "next_required_action": (
                    "build a separate accepted endpoint gate and scoring script that reads the frozen NGC4088 manifest unchanged"
                    if formula_freeze_allowed
                    else (
                        "close B2 Tau-side physical-normalization law and B3 law-level uniqueness; preserve the B1 WHISP graphical-overview caveat"
                        if b1_resolved_for_formula_freeze
                        else (
                            "resolve B1 independent x_w review or source-native H I data route; close B2 Tau-side physical-normalization "
                            "law; close B3 law-level uniqueness through the B2 carrier/closure derivation"
                        )
                    )
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    blockers.to_csv(DATA / "ngc4088_formula_freeze_readiness_dashboard.csv", index=False)
    summary.to_csv(DATA / "ngc4088_formula_freeze_readiness_summary.csv", index=False)

    report = [
        "# NGC4088 Formula-Freeze Readiness Dashboard",
        "",
        "This dashboard consolidates the B1/B2/B3 formula-freeze blockers for the",
        "NGC4088 warp/history-coupled candidate. It is a preflight status synthesis,",
        "not an endpoint score and not an empirical validation claim.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Local Blockers",
        "",
        markdown_table(blockers),
        "",
        "## Interpretation",
        "",
        "The NGC4088 lane now has a coherent residual-blind formula-freeze path.",
        "B1 is closed with an explicit provenance caveat: the accepted x_w comes",
        "from a residual-blind WHISP graphical-overview extraction rather than a",
        "direct source-coordinate H I product. B2 and B3 are closed only at the",
        "protocol formula-freeze level: the physical-normalization law and",
        "law-level uniqueness remain open. Therefore the formula may be treated as",
        "frozen for the next accepted-endpoint gate, but endpoint scoring still",
        "requires a separate gate and script.",
        "",
    ]
    (REPORTS / "ngc4088_formula_freeze_readiness_dashboard.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
