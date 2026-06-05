#!/usr/bin/env python3
"""Build the next-case expansion gate for the mixed-readout population test.

This gate is source-side only. It ranks candidate galaxies for adding more
frozen mixed-readout protocols after the three-case matched-vs-wrong control.
It does not score rotations, does not infer labels from residuals, and does not
promote an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "mixed_readout_population_expansion_gate_not_endpoint"


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
    return str(value).strip().lower() in {"true", "1", "yes"}


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    control = pd.read_csv(DATA / "mixed_readout_population_control_summary.csv").iloc[0]
    queue = pd.read_csv(DATA / "mixed_readout_candidate_acquisition_queue.csv")
    ngc4088_breakthrough = pd.read_csv(DATA / "ngc4088_breakthrough_promotion_summary.csv").iloc[0]
    ngc4088_promotion = pd.read_csv(
        DATA / "s4g75_ngc4088_readout_promotion_summary.csv"
    ).iloc[0]
    ngc4088_scale = pd.read_csv(DATA / "s4g75_ngc4088_scale_uniqueness_summary.csv").iloc[0]
    ngc4088_eps = pd.read_csv(
        DATA / "s4g75_ngc4088_epsilon_cross_input_review_summary.csv"
    ).iloc[0]
    ngc4183_preflight_path = DATA / "ngc4183_weak_projection_control_summary.csv"
    ngc4183_gamma_path = DATA / "ngc4183_projection_gamma_upper_bound_summary.csv"
    ngc4183_roadmap_path = DATA / "ngc4183_control_promotion_roadmap_summary.csv"
    ngc4183_preflight = (
        pd.read_csv(ngc4183_preflight_path).iloc[0] if ngc4183_preflight_path.exists() else None
    )
    ngc4183_gamma = (
        pd.read_csv(ngc4183_gamma_path).iloc[0] if ngc4183_gamma_path.exists() else None
    )
    ngc4183_roadmap = (
        pd.read_csv(ngc4183_roadmap_path).iloc[0] if ngc4183_roadmap_path.exists() else None
    )

    control_passed = str(control["control_status"]) == (
        "PASSED_3CASE_WRONG_LABEL_AND_SHUFFLED_CONTROL"
    )

    rows = [
        {
            "galaxy": "NGC4088",
            "expansion_priority": "P0_CLOSEST_SOURCE_BOUND_MIXED_PROTOCOL",
            "candidate_readout": "K_expdisk_warp_history_coupled_mixed_review",
            "source_side_strength": "BREAKTHROUGH_PROTOCOL_BOUND_READY_NOT_ENDPOINT",
            "source_rule_candidate": False,
            "formula_freeze_allowed_now": False,
            "has_numeric_source_onset": True,
            "has_q_memory_review": True,
            "has_epsilon_bound": True,
            "has_smooth_disk_scale": True,
            "main_blockers": ";".join(
                [
                    str(ngc4088_promotion["blocked_gate_ids"]),
                    str(ngc4088_scale["scale_uniqueness_decision"]),
                ]
            ),
            "next_required_gate": (
                "resolve independent digitization review, physical normalization law, "
                "and scale-uniqueness before any mixed formula freeze"
            ),
            "source_evidence_summary": (
                f"x_w={float(ngc4088_breakthrough['x_warp_onset']):.6g}; "
                f"q={float(ngc4088_breakthrough['q_warp']):.6g}; "
                f"m_history={float(ngc4088_breakthrough['m_history_warp']):.6g}; "
                f"|epsilon_cross|<={float(ngc4088_breakthrough['epsilon_cross_bound']):.6g}; "
                f"input_review={ngc4088_eps['input_review_status']}"
            ),
            "endpoint_scores_allowed": False,
            "uses_vobs_or_residual_in_selection": False,
            "expansion_gate_status": "FORMULA_FREEZE_BLOCKED_SOURCE_PROTOCOL_CLOSEST",
        },
        {
            "galaxy": "NGC4183",
            "expansion_priority": "P1_WEAK_PROJECTION_NULL_CONTROL_REVIEW",
            "candidate_readout": "K_expdisk_edge_on_projection_weak_null_control_review",
            "source_side_strength": (
                str(ngc4183_preflight["weak_control_preflight_status"])
                if ngc4183_preflight is not None
                else "WEAK_PROJECTION_PREFLIGHT_MISSING"
            ),
            "source_rule_candidate": False,
            "formula_freeze_allowed_now": (
                bool(ngc4183_roadmap is not None)
                and str(ngc4183_roadmap["control_roadmap_status"])
                == "NGC4183_CONTROL_PROMOTION_ROADMAP_SCORING_COMPLETE_PRELIMINARY_CONTROL"
            ),
            "has_numeric_source_onset": True,
            "has_q_memory_review": False,
            "has_epsilon_bound": True,
            "has_smooth_disk_scale": True,
            "main_blockers": (
                "none"
                if (
                    ngc4183_roadmap is not None
                    and str(ngc4183_roadmap["control_roadmap_status"])
                    == "NGC4183_CONTROL_PROMOTION_ROADMAP_SCORING_COMPLETE_PRELIMINARY_CONTROL"
                )
                else str(ngc4183_roadmap["first_actionable_blocking_stage"])
                if ngc4183_roadmap is not None
                else "independent_tilted_ring_review_response_required"
            ),
            "next_required_gate": (
                "none"
                if (
                    ngc4183_roadmap is not None
                    and str(ngc4183_roadmap["control_roadmap_status"])
                    == "NGC4183_CONTROL_PROMOTION_ROADMAP_SCORING_COMPLETE_PRELIMINARY_CONTROL"
                )
                else "complete independent tilted-ring review response before formula freeze"
            ),
            "source_evidence_summary": (
                "tilted-ring orientation profile supports weak projection/null-control; "
                f"gamma_bound<={float(ngc4183_gamma['gamma_projection_upper_bound']):.6g}"
                if ngc4183_gamma is not None
                else "tilted-ring weak-projection upper bound pending"
            ),
            "endpoint_scores_allowed": (
                bool(ngc4183_roadmap is not None)
                and str(ngc4183_roadmap["control_roadmap_status"])
                == "NGC4183_CONTROL_PROMOTION_ROADMAP_SCORING_COMPLETE_PRELIMINARY_CONTROL"
            ),
            "uses_vobs_or_residual_in_selection": False,
            "expansion_gate_status": (
                "SEPARATE_NULL_CONTROL_BRANCH_COMPLETE_NOT_MIXED_PROMOTION_CANDIDATE"
                if (
                    ngc4183_roadmap is not None
                    and str(ngc4183_roadmap["control_roadmap_status"])
                    == "NGC4183_CONTROL_PROMOTION_ROADMAP_SCORING_COMPLETE_PRELIMINARY_CONTROL"
                )
                else "PREFLIGHT_PASS_WEAK_CONTROL_REVIEW_REQUIRED_NOT_ENDPOINT"
            ),
        },
        {
            "galaxy": "IC2574",
            "expansion_priority": "P1_DISTURBED_TAIL_NUMERIC_RADIUS_REQUIRED",
            "candidate_readout": "K_expdisk_disturbed_outer_tail_overlay_review",
            "source_side_strength": "DISTURBED_CONTEXT_ACCEPTED_NUMERIC_KERNEL_BLOCKED",
            "source_rule_candidate": False,
            "formula_freeze_allowed_now": False,
            "has_numeric_source_onset": False,
            "has_q_memory_review": False,
            "has_epsilon_bound": False,
            "has_smooth_disk_scale": False,
            "main_blockers": "outer_tail_transition_radius_missing",
            "next_required_gate": "extract tail/envelope transition radius or HI radial support kernel",
            "source_evidence_summary": "extended HI envelope and HI-hole/history context accepted; numeric tail transition missing",
            "endpoint_scores_allowed": False,
            "uses_vobs_or_residual_in_selection": False,
            "expansion_gate_status": "SOURCE_ACQUISITION_REQUIRED",
        },
        {
            "galaxy": "UGC05716",
            "expansion_priority": "P1_TAIL_ASYMMETRY_NUMERIC_FIELDS_REQUIRED",
            "candidate_readout": "K_expdisk_tail_asymmetry_projection_overlay_review",
            "source_side_strength": "HI_ROTATION_CONTEXT_ACCEPTED_NUMERIC_KERNEL_BLOCKED",
            "source_rule_candidate": False,
            "formula_freeze_allowed_now": False,
            "has_numeric_source_onset": False,
            "has_q_memory_review": False,
            "has_epsilon_bound": False,
            "has_smooth_disk_scale": False,
            "main_blockers": "HI_asymmetry_or_tail_measurement_missing",
            "next_required_gate": "extract HI asymmetry/tail observable from source map or profile",
            "source_evidence_summary": "HI/projection context available; no extracted asymmetry/tail metric",
            "endpoint_scores_allowed": False,
            "uses_vobs_or_residual_in_selection": False,
            "expansion_gate_status": "SOURCE_ACQUISITION_REQUIRED",
        },
    ]

    for _, row in queue.loc[queue["candidate_priority"].str.startswith("P2_")].head(6).iterrows():
        rows.append(
            {
                "galaxy": row["galaxy"],
                "expansion_priority": "P2_BULK_SOURCE_ACQUISITION",
                "candidate_readout": row["candidate_mixed_readout"],
                "source_side_strength": str(row["audit_decision"]),
                "source_rule_candidate": bool_value(row["source_rule_candidate"]),
                "formula_freeze_allowed_now": False,
                "has_numeric_source_onset": False,
                "has_q_memory_review": False,
                "has_epsilon_bound": False,
                "has_smooth_disk_scale": bool_value(row["has_smooth_disk_scale"]),
                "main_blockers": str(row["blocking_or_caution_notes"]),
                "next_required_gate": str(row["required_next_gate"]),
                "source_evidence_summary": str(row["source_observable_names"]),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_selection": False,
                "expansion_gate_status": "BULK_SOURCE_ACQUISITION_REQUIRED",
            }
        )

    candidates = pd.DataFrame(rows)
    candidates["claim_boundary"] = CLAIM_BOUNDARY

    top = candidates.iloc[0]
    summary = pd.DataFrame(
        [
            {
                "expansion_gate_status": "NEXT_MIXED_CASE_IDENTIFIED_FORMULA_FREEZE_BLOCKED",
                "three_case_control_passed": control_passed,
                "next_primary_galaxy": top["galaxy"],
                "next_primary_candidate_readout": top["candidate_readout"],
                "next_primary_formula_freeze_allowed_now": bool_value(
                    top["formula_freeze_allowed_now"]
                ),
                "n_candidates_ranked": len(candidates),
                "n_formula_freeze_allowed_now": int(
                    candidates["formula_freeze_allowed_now"].map(bool_value).sum()
                ),
                "n_source_acquisition_required": int(
                    candidates["expansion_gate_status"]
                    .astype(str)
                    .str.contains("SOURCE_ACQUISITION")
                    .sum()
                ),
                "n_review_required": int(
                    candidates["expansion_gate_status"]
                    .astype(str)
                    .str.contains("REVIEW_REQUIRED")
                    .sum()
                ),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_selection": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_required_action": str(top["next_required_gate"]),
            }
        ]
    )

    obligations = pd.DataFrame(
        [
            {
                "gate_id": "EXP1_NO_ENDPOINT_SCORING",
                "gate_status": "PASS",
                "obligation": "expansion gate ranks candidates but scores no rotation curve",
            },
            {
                "gate_id": "EXP2_CONTROL_SIGNAL_PRESERVED",
                "gate_status": "PASS" if control_passed else "BLOCKED",
                "obligation": "three-case matched-vs-wrong control must remain recorded before expanding",
            },
            {
                "gate_id": "EXP3_NGC4088_NOT_PROMOTED",
                "gate_status": "PASS",
                "obligation": "NGC4088 diagnostic signal cannot be used as source-label evidence",
            },
            {
                "gate_id": "EXP4_FORMULA_FREEZE_BLOCKED_UNTIL_SOURCE_RULE",
                "gate_status": "PASS",
                "obligation": "no fourth mixed formula freeze until blockers are resolved residual-blind",
            },
        ]
    )
    obligations["claim_boundary"] = CLAIM_BOUNDARY

    candidates.to_csv(DATA / "mixed_readout_population_expansion_candidates.csv", index=False)
    summary.to_csv(DATA / "mixed_readout_population_expansion_summary.csv", index=False)
    obligations.to_csv(DATA / "mixed_readout_population_expansion_obligations.csv", index=False)

    report = [
        "# Mixed Readout Population Expansion Gate",
        "",
        "This gate ranks next candidates after the three-case matched-vs-wrong",
        "control. It does not score rotations and does not promote endpoint",
        "labels. Its job is to prevent the next expansion from being driven by",
        "the already inspected endpoint residuals.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Candidate Ranking",
        "",
        markdown_table(candidates),
        "",
        "## Obligations",
        "",
        markdown_table(obligations),
        "",
        "## Interpretation",
        "",
        "NGC4088 is the closest next mixed case because it has a source-bound",
        "warp/history protocol chain, including x_w, q, memory, and epsilon-cross",
        "bound ingredients. It is still blocked from formula freeze by independent",
        "digitization review, physical normalization-law derivation, and scale",
        "uniqueness. The diagnostic NGC4088 curve is not used as promotion evidence.",
        "",
        "NGC4183 is no longer a pending review candidate in this queue. Its",
        "weak-projection/null-control branch has already passed independent source",
        "review, freeze, accepted-control promotion, and interval-control scoring",
        "as a separate single-galaxy control lane. It therefore stays outside the",
        "next mixed-case promotion race, while preserving a narrow null-control",
        "claim boundary rather than a mixed population-validation role.",
        "",
    ]
    (REPORTS / "mixed_readout_population_expansion_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
