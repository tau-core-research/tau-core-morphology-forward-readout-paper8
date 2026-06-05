#!/usr/bin/env python3
"""Build the NGC4088 mixed formula-freeze blocker resolution plan.

This is a source-side planning gate. It consumes the existing residual-blind
NGC4088 ledgers and separates:

- already usable protocol-bound ingredients,
- blockers that must be resolved before a fourth mixed formula freeze,
- blockers that only affect population-level claims.

It does not score rotations and does not promote an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_mixed_formula_freeze_blocker_resolution_not_endpoint"


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


def as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    expansion = pd.read_csv(DATA / "mixed_readout_population_expansion_summary.csv").iloc[0]
    expansion_candidates = pd.read_csv(DATA / "mixed_readout_population_expansion_candidates.csv")
    candidate = expansion_candidates.loc[expansion_candidates["galaxy"].eq("NGC4088")].iloc[0]
    promotion_gate = pd.read_csv(DATA / "s4g75_ngc4088_readout_promotion_gate.csv")
    promotion_summary = pd.read_csv(DATA / "s4g75_ngc4088_readout_promotion_summary.csv").iloc[0]
    physical_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_physical_normalization_law_summary.csv"
    ).iloc[0]
    scale_summary = pd.read_csv(DATA / "s4g75_ngc4088_scale_uniqueness_summary.csv").iloc[0]
    scale_audit = pd.read_csv(DATA / "s4g75_ngc4088_scale_uniqueness_audit.csv")
    scale_selection = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_selection_summary.csv"
    ).iloc[0]
    scale_derivation = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_derivation_summary.csv"
    ).iloc[0]
    xw_summary = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_summary.csv").iloc[0]
    independent_review = pd.read_csv(
        DATA / "s4g75_ngc4088_source_response_independent_review_summary.csv"
    ).iloc[0]
    bi_rule = pd.read_csv(DATA / "s4g75_ngc4088_bi_coefficient_rule_summary.csv").iloc[0]
    epsilon_review = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_input_review_summary.csv"
    ).iloc[0]
    breakthrough = pd.read_csv(DATA / "ngc4088_breakthrough_promotion_summary.csv").iloc[0]

    scale_ids = ";".join(scale_audit["scale_id"].astype(str).tolist())
    current_scale = str(scale_summary["current_scale_id"])

    blockers = pd.DataFrame(
        [
            {
                "blocker_id": "B1_INDEPENDENT_XW_DIGITIZATION_REVIEW",
                "blocker_scope": "formula_freeze",
                "current_status": "BLOCKED",
                "current_evidence": (
                    f"x_w conversion status={xw_summary['xw_conversion_decision']}; "
                    f"accepted_for_mapping_rule={as_bool(xw_summary['accepted_for_mapping_rule'])}"
                ),
                "resolution_condition": (
                    "obtain independent residual-blind channel-map digitization review or "
                    "freeze a reproducible image-analysis extraction for x_w"
                ),
                "source_files": (
                    "s4g75_ngc4088_xw_conversion_summary.csv;"
                    "s4g75_ngc4088_readout_promotion_gate.csv"
                ),
                "endpoint_scores_allowed_after_this_alone": False,
            },
            {
                "blocker_id": "B2_PHYSICAL_NORMALIZATION_LAW",
                "blocker_scope": "formula_freeze",
                "current_status": str(physical_summary["law_status"]),
                "current_evidence": (
                    "candidate prefactor "
                    f"{float(physical_summary['normalization_prefactor_km2_s2']):.6g} km2/s2; "
                    "formula is dimensionally consistent but Tau-side law is not derived"
                ),
                "resolution_condition": (
                    "derive or explicitly predeclare the Tau-side mapping from the "
                    "dimensionless closure-source basis to delta v^2"
                ),
                "source_files": (
                    "s4g75_ngc4088_physical_normalization_law_summary.csv;"
                    "s4g75_ngc4088_physical_normalization_law_gate.csv"
                ),
                "endpoint_scores_allowed_after_this_alone": False,
            },
            {
                "blocker_id": "B3_SCALE_UNIQUENESS",
                "blocker_scope": "formula_freeze",
                "current_status": str(scale_summary["scale_uniqueness_decision"]),
                "current_evidence": (
                    f"{int(scale_summary['n_scale_candidates'])} residual-blind candidate "
                    f"scales exist; current conditional choice={current_scale}; "
                    f"candidate_ids={scale_ids}"
                ),
                "resolution_condition": (
                    "freeze a residual-blind theory criterion selecting one scale before "
                    "endpoint scoring, or demote the lane to sensitivity analysis"
                ),
                "source_files": (
                    "s4g75_ngc4088_scale_uniqueness_summary.csv;"
                    "s4g75_ngc4088_scale_uniqueness_audit.csv;"
                    "s4g75_ngc4088_tau_side_scale_selection_summary.csv;"
                    "s4g75_ngc4088_tau_side_scale_derivation_summary.csv"
                ),
                "endpoint_scores_allowed_after_this_alone": False,
            },
            {
                "blocker_id": "B4_POPULATION_GENERALIZATION",
                "blocker_scope": "population_claim",
                "current_status": "BLOCKED_FOR_POPULATION_CLAIMS",
                "current_evidence": (
                    "NGC4088 is one source-filled warp/history lane; the three-case "
                    "mixed control is promising but small-N"
                ),
                "resolution_condition": (
                    "repeat the same source-side freeze protocol on a predeclared "
                    "source-rich warp/history sample before making population claims"
                ),
                "source_files": (
                    "s4g75_ngc4088_readout_promotion_summary.csv;"
                    "mixed_readout_population_expansion_summary.csv"
                ),
                "endpoint_scores_allowed_after_this_alone": False,
            },
        ]
    )
    blockers["claim_boundary"] = CLAIM_BOUNDARY

    supports = pd.DataFrame(
        [
            {
                "support_id": "S1_BREAKTHROUGH_PROTOCOL_CHAIN",
                "support_status": str(breakthrough["breakthrough_status"]),
                "evidence": (
                    f"x_w={float(breakthrough['x_warp_onset']):.6g}; "
                    f"q_warp={float(breakthrough['q_warp']):.6g}; "
                    f"m_history={float(breakthrough['m_history_warp']):.6g}; "
                    f"|epsilon_cross|<={float(breakthrough['epsilon_cross_bound']):.6g}"
                ),
                "why_it_is_not_enough": (
                    "protocol-bound ingredients exist, but accepted endpoint use still "
                    "requires formula-freeze blockers to close"
                ),
            },
            {
                "support_id": "S2_Q_MEMORY_AND_BI_REVIEW",
                "support_status": "PROTOCOL_BOUND_READY",
                "evidence": (
                    f"source_review={independent_review['source_review_status']}; "
                    f"bi_rule={bi_rule['coefficient_rule_status']}; "
                    f"epsilon_review={epsilon_review['input_review_status']}"
                ),
                "why_it_is_not_enough": (
                    "these pass the epsilon-cross bound protocol, but do not derive "
                    "the velocity normalization law or select a unique scale"
                ),
            },
            {
                "support_id": "S3_EXPANSION_GATE_PRIORITY",
                "support_status": str(expansion["expansion_gate_status"]),
                "evidence": (
                    f"next_primary={expansion['next_primary_galaxy']}; "
                    f"candidate_readout={candidate['candidate_readout']}; "
                    f"uses_vobs_or_residual_in_selection={as_bool(candidate['uses_vobs_or_residual_in_selection'])}"
                ),
                "why_it_is_not_enough": (
                    "candidate priority is not endpoint authorization; it only says "
                    "where the next residual-blind source work should focus"
                ),
            },
        ]
    )
    supports["claim_boundary"] = CLAIM_BOUNDARY

    hard_freeze_blockers = blockers.loc[blockers["blocker_scope"].eq("formula_freeze")]
    all_hard_resolved = hard_freeze_blockers["current_status"].eq("RESOLVED").all()
    summary = pd.DataFrame(
        [
            {
                "resolution_plan_status": "NGC4088_FORMULA_FREEZE_BLOCKER_RESOLUTION_PLAN_CREATED",
                "galaxy": "NGC4088",
                "candidate_readout": str(candidate["candidate_readout"]),
                "n_formula_freeze_blockers": len(hard_freeze_blockers),
                "n_population_claim_blockers": int(
                    blockers["blocker_scope"].eq("population_claim").sum()
                ),
                "n_protocol_ready_supports": len(supports),
                "all_formula_freeze_blockers_resolved": bool(all_hard_resolved),
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "promotion_decision_now": str(promotion_summary["readout_promotion_decision"]),
                "scale_selection_status": str(scale_selection["selection_status"]),
                "scale_derivation_status": str(scale_derivation["derivation_status"]),
                "next_required_action": (
                    "resolve B1, B2, and B3 residual-blind; keep B4 as a population-claim "
                    "caveat unless a population test is launched"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    blockers.to_csv(
        DATA / "ngc4088_mixed_formula_freeze_blocker_resolution_plan.csv", index=False
    )
    supports.to_csv(
        DATA / "ngc4088_mixed_formula_freeze_protocol_supports.csv", index=False
    )
    summary.to_csv(
        DATA / "ngc4088_mixed_formula_freeze_blocker_resolution_summary.csv", index=False
    )

    report = [
        "# NGC4088 Mixed Formula-Freeze Blocker Resolution Plan",
        "",
        "This report is a source-side planning gate. It does not score the",
        "rotation curve, does not promote an endpoint, and does not use the",
        "previous NGC4088 diagnostic curve as evidence.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Formula-Freeze And Population Blockers",
        "",
        markdown_table(blockers),
        "",
        "## Protocol-Ready Supports",
        "",
        markdown_table(supports),
        "",
        "## Interpretation",
        "",
        "NGC4088 remains the closest fourth mixed-readout candidate, but the",
        "formula-freeze path is still blocked by three local source-side issues:",
        "independent x_w digitization review, a Tau-side physical normalization",
        "law, and a unique residual-blind scale-selection rule. Population",
        "generalization is tracked separately: it blocks broad claims, but it is",
        "not a substitute for the three local formula-freeze obligations.",
        "",
    ]
    (REPORTS / "ngc4088_mixed_formula_freeze_blocker_resolution_plan.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
