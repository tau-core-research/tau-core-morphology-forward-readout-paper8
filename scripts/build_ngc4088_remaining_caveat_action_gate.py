#!/usr/bin/env python3
"""Build the NGC4088 remaining-caveat action gate.

This synthesis separates three different notions that are easy to conflate:

1. caveated endpoint readiness, which is already present;
2. provenance upgrade, which would replace graphical WHISP x_w by direct H I;
3. law-level derivation, which is still open for B2/B3.

The gate does not score a curve and does not change endpoint status.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_remaining_caveat_action_gate_not_endpoint"


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


def row(path: str) -> pd.Series:
    file = DATA / path
    if not file.exists():
        raise FileNotFoundError(file)
    table = pd.read_csv(file)
    if table.empty:
        raise ValueError(f"{file} is empty")
    return table.iloc[0]


def b(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    b1 = row("ngc4088_b1_whisp_promotion_review_summary.csv")
    b1_direct = row("ngc4088_b1_original_hi_data_acquisition_summary.csv")
    b2 = row("ngc4088_b2_physical_normalization_synthesis_summary.csv")
    b2_conditional = row("ngc4088_b2_closure_asymptotic_summary.csv")
    b3 = row("ngc4088_b3_scale_uniqueness_synthesis_summary.csv")
    freeze = row("ngc4088_warp_history_formula_freeze_summary.csv")
    readiness = row("ngc4088_formula_freeze_readiness_summary.csv")
    accepted_gate = row("ngc4088_warp_history_accepted_endpoint_gate_summary.csv")
    endpoint = row("ngc4088_warp_history_accepted_endpoint_summary.csv")

    endpoint_ready = b(accepted_gate["endpoint_scores_allowed"])
    endpoint_scored = (
        str(endpoint["endpoint_status"])
        == "CAVEATED_ACCEPTED_ENDPOINT_PRELIMINARY_CONTROL_RESULT"
    )
    b1_formula_closed = b(b1["accepted_x_w_for_formula_freeze"])
    direct_hi_cached = (
        str(b1_direct["original_hi_data_audit_status"])
        == "DIRECT_SOURCE_COORDINATE_HI_PRODUCT_CACHED"
    )
    b2_protocol_ready = str(freeze["b2_protocol_status"]) == (
        "B2_PROTOCOL_FORMULA_FREEZE_READY_LAW_LEVEL_OPEN"
    )
    b3_protocol_ready = str(freeze["b3_protocol_status"]) == (
        "B3_PROTOCOL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_OPEN"
    )
    b2_law_closed = not b(freeze["b2_law_level_open"])
    b3_law_closed = not b(freeze["b3_law_level_open"])

    actions = pd.DataFrame(
        [
            {
                "action_id": "A1_DIRECT_HI_PROVENANCE_UPGRADE",
                "caveat_layer": "B1_PROVENANCE",
                "current_status": str(b1["b1_resolution_status"]),
                "formula_freeze_blocking_now": False,
                "endpoint_blocking_now": False,
                "law_level_blocking_now": False,
                "closed_or_reduced": b1_formula_closed,
                "remaining_caveat": (
                    "direct source-coordinate H I/FITS product not cached; WHISP graphical overview caveat travels"
                    if not direct_hi_cached
                    else "direct source-coordinate product cached"
                ),
                "next_action": (
                    "optional provenance upgrade: cache a direct source-coordinate H I product when available"
                    if not direct_hi_cached
                    else "none"
                ),
            },
            {
                "action_id": "A2_B2_CLOSURE_FUNCTIONAL_DERIVATION",
                "caveat_layer": "B2_LAW_LEVEL",
                "current_status": str(b2_conditional["b2_conditional_derivation_status"]),
                "formula_freeze_blocking_now": False,
                "endpoint_blocking_now": False,
                "law_level_blocking_now": True,
                "closed_or_reduced": b2_protocol_ready,
                "remaining_caveat": (
                    "physical normalization is algebraically derived from a conditional source-load closure functional; Vflat^2 has a frozen-protocol conditional carrier theorem, while Tau-side source-load origin, final carrier law/population transfer, and separability/cross-term proof remain open"
                    if not b2_law_closed
                    else "law-level physical normalization closed"
                ),
                "next_action": str(b2_conditional["next_required_action"]),
            },
            {
                "action_id": "A3_B3_LAW_LEVEL_UNIQUENESS",
                "caveat_layer": "B3_LAW_LEVEL",
                "current_status": str(b3["b3_synthesis_status"]),
                "formula_freeze_blocking_now": False,
                "endpoint_blocking_now": False,
                "law_level_blocking_now": True,
                "closed_or_reduced": b3_protocol_ready,
                "remaining_caveat": (
                    "scale uniqueness is protocol-conditional; law-level uniqueness depends on B2"
                    if not b3_law_closed
                    else "law-level scale uniqueness closed"
                ),
                "next_action": "derive why CURRENT_XW_VFLAT2 is uniquely selected by Tau-side law-level closure",
            },
            {
                "action_id": "A4_POPULATION_TRANSFER",
                "caveat_layer": "GENERALIZATION",
                "current_status": "SINGLE_GALAXY_CAVEATED_CONTROL_ENDPOINT",
                "formula_freeze_blocking_now": False,
                "endpoint_blocking_now": False,
                "law_level_blocking_now": False,
                "closed_or_reduced": endpoint_scored,
                "remaining_caveat": "single-galaxy result; not population validation",
                "next_action": "run source-selected population replay after law/provenance caveat policy is frozen",
            },
        ]
    )
    actions["endpoint_scores_allowed"] = False
    actions["uses_vobs_or_residual"] = False
    actions["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "action_gate_status": "NGC4088_REMAINING_CAVEAT_ACTION_GATE_BUILT_NOT_ENDPOINT",
                "galaxy": "NGC4088",
                "endpoint_ready": endpoint_ready,
                "endpoint_scored": endpoint_scored,
                "endpoint_status": str(endpoint["endpoint_status"]),
                "matched_rmse_km_s": float(endpoint["rmse_warp_history_accepted"]),
                "best_baseline_rmse_km_s": float(endpoint["best_baseline_rmse_km_s"]),
                "matched_beats_all_baselines": b(endpoint["matched_beats_all_baselines"]),
                "matched_beats_all_wrong_families": b(
                    endpoint["matched_beats_all_wrong_families"]
                ),
                "b1_formula_freeze_closed_caveated": b1_formula_closed,
                "b1_direct_hi_product_cached": direct_hi_cached,
                "b2_protocol_ready_law_level_open": b2_protocol_ready and not b2_law_closed,
                "b2_conditional_derivation_status": str(
                    b2_conditional["b2_conditional_derivation_status"]
                ),
                "b2_formula_freeze_alignment_pass": b(
                    b2_conditional["formula_freeze_alignment_pass"]
                ),
                "b2_conditional_law_level_closed": b(b2_conditional["law_level_closed"]),
                "b3_protocol_unique_law_level_open": b3_protocol_ready and not b3_law_closed,
                "formula_freeze_allowed_now": b(readiness["formula_freeze_allowed_now"]),
                "endpoint_scores_allowed_by_this_gate": False,
                "endpoint_status_changed": False,
                "endpoint_scores_recomputed": False,
                "uses_vobs_or_residual": False,
                "next_recommended_caveat_action": "B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    actions.to_csv(DATA / "ngc4088_remaining_caveat_actions.csv", index=False)
    summary.to_csv(DATA / "ngc4088_remaining_caveat_action_summary.csv", index=False)

    report = [
        "# NGC4088 Remaining Caveat Action Gate",
        "",
        "This gate separates endpoint readiness from provenance and law-level caveats.",
        "It does not score a curve and does not change the accepted endpoint status.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Actions",
        "",
        markdown_table(actions),
        "",
        "## Interpretation",
        "",
        "NGC4088 is already a caveated accepted single-galaxy control endpoint. The",
        "remaining scientific work is not another endpoint score. B1 is closed for",
        "formula freeze only with a WHISP graphical-overview provenance caveat; a",
        "direct source-coordinate H I product would be a provenance upgrade. The",
        "primary theory action is B2: derive the Tau-side source-load origin,",
        "final carrier law/population transfer, and cross-term bound that make the",
        "conditional closure functional internal rather than formula-conditional.",
        "The frozen Vflat^2 carrier theorem already narrows that task, but does not",
        "close the final Tau-side law. B3 then becomes the law-level uniqueness",
        "corollary.",
        "",
    ]
    (REPORTS / "ngc4088_remaining_caveat_action_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
