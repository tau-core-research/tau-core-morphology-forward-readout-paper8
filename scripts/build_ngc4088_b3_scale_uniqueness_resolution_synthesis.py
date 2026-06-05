#!/usr/bin/env python3
"""Synthesize the NGC4088 B3 scale-uniqueness status.

B3 asks whether the NGC4088 warp/history lane has a unique residual-blind scale
before endpoint scoring.  The existing selection gate conditionally chooses
CURRENT_XW_VFLAT2, but the law-level reason for the selection is still tied to
B2 obligations.  This synthesis records that distinction explicitly.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_b3_scale_uniqueness_resolution_synthesis_not_endpoint"


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

    audit = pd.read_csv(DATA / "s4g75_ngc4088_scale_uniqueness_audit.csv")
    audit_summary = pd.read_csv(DATA / "s4g75_ngc4088_scale_uniqueness_summary.csv").iloc[0]
    selection = pd.read_csv(DATA / "s4g75_ngc4088_tau_side_scale_selection_gate.csv")
    selection_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_selection_summary.csv"
    ).iloc[0]
    b2 = pd.read_csv(DATA / "ngc4088_b2_physical_normalization_synthesis_summary.csv").iloc[0]

    merged = audit.merge(
        selection[
            [
                "scale_id",
                "n_selection_criteria_passed",
                "failed_criteria",
                "selection_gate_status",
            ]
        ],
        on="scale_id",
        how="left",
    )
    selected = merged.loc[
        merged["selection_gate_status"].eq(
            "SELECTED_BY_MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE"
        )
    ]

    candidates = merged[
        [
            "galaxy",
            "scale_id",
            "scale_formula",
            "scale_value_km2_s2",
            "current_prefactor_ratio",
            "source_status",
            "selection_gate_status",
            "n_selection_criteria_passed",
            "failed_criteria",
            "tau_side_obligation",
            "uses_vobs_or_residual",
        ]
    ].copy()
    candidates["endpoint_scores_allowed"] = False
    candidates["claim_boundary"] = CLAIM_BOUNDARY

    obligations = pd.DataFrame(
        [
            {
                "obligation_id": "B3O1_PROTOCOL_SELECTION_RULE_FROZEN",
                "obligation_status": "CONDITIONAL_PASS",
                "requirement": "use the minimal source-onset asymptotic-carrier rule before endpoint scoring",
                "current_evidence": str(selection_summary["selection_status"]),
                "why_not_final": "the rule is conditional until B2 derives the carrier principle",
            },
            {
                "obligation_id": "B3O2_REJECT_BARYONIC_MEDIAN_CARRIER",
                "obligation_status": "CONDITIONAL_PASS",
                "requirement": "reject x_w * median_r(v_n^2) as a local baryonic readout statistic",
                "current_evidence": "fails C3_ASYMPTOTIC_READOUT_CARRIER",
                "why_not_final": "requires the asymptotic-carrier theorem from B2",
            },
            {
                "obligation_id": "B3O3_REJECT_EXTERNAL_TPG_COMPARATOR",
                "obligation_status": "CONDITIONAL_PASS",
                "requirement": "reject x_w * median_r(v_v6^2) as an external comparator normalizer",
                "current_evidence": "fails C3_ASYMPTOTIC_READOUT_CARRIER and C4_NO_EXTERNAL_CLOSURE_COMPARATOR",
                "why_not_final": "requires comparator-autonomy derivation, not only protocol exclusion",
            },
            {
                "obligation_id": "B3O4_REJECT_CLOSURE_FRACTION_COMPOSITES",
                "obligation_status": "CONDITIONAL_PASS",
                "requirement": "reject c_g and x_w*c_g composite scales unless Tau-side theory derives extra factors",
                "current_evidence": "fails C2 or C5 depending on candidate",
                "why_not_final": "requires minimal-source-factor theorem or explicit source-factor coupling law",
            },
            {
                "obligation_id": "B3O5_LAW_LEVEL_UNIQUENESS",
                "obligation_status": "OPEN",
                "requirement": "derive why only CURRENT_XW_VFLAT2 survives as a Tau-side scale law",
                "current_evidence": str(b2["law_quality"]),
                "why_not_final": "B2 closure functional and asymptotic-carrier theorem remain open",
            },
        ]
    )
    obligations["endpoint_scores_allowed"] = False
    obligations["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "b3_synthesis_status": "B3_CONDITIONAL_UNIQUE_SCALE_SELECTED_LAW_LEVEL_UNIQUENESS_OPEN",
                "initial_uniqueness_decision": str(audit_summary["scale_uniqueness_decision"]),
                "selection_principle": str(selection_summary["selection_principle"]),
                "n_initial_residual_blind_scales": int(audit_summary["n_scale_candidates"]),
                "n_selected_by_protocol_rule": len(selected),
                "selected_scale_ids": ";".join(selected["scale_id"]) if len(selected) else "none",
                "conditional_uniqueness_resolved": len(selected) == 1,
                "law_level_uniqueness_resolved": False,
                "formula_freeze_allowed_now": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "close B2 asymptotic-carrier and closure-functional obligations, "
                    "or keep B3 as protocol-conditional only"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    candidates.to_csv(DATA / "ngc4088_b3_scale_uniqueness_candidate_resolution.csv", index=False)
    obligations.to_csv(DATA / "ngc4088_b3_scale_uniqueness_obligations.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b3_scale_uniqueness_synthesis_summary.csv", index=False)

    report = [
        "# NGC4088 B3 Scale-Uniqueness Resolution Synthesis",
        "",
        "This report separates protocol-level uniqueness from law-level uniqueness.",
        "The minimal source-onset asymptotic-carrier rule selects one scale, but",
        "that rule is still conditional on B2. No endpoint score is used.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Candidate Resolution",
        "",
        markdown_table(candidates),
        "",
        "## Remaining Obligations",
        "",
        markdown_table(obligations),
        "",
        "## Interpretation",
        "",
        "B3 is no longer an unstructured multiple-scale problem: under the frozen",
        "conditional selection rule, CURRENT_XW_VFLAT2 is the only selected scale.",
        "However, law-level scale uniqueness remains open because the rule depends",
        "on the B2 asymptotic-carrier and closure-functional derivations. Thus B3",
        "remains endpoint-blocking until B2 is closed or the lane is explicitly",
        "demoted to a sensitivity-only formula shell.",
        "",
    ]
    (REPORTS / "ngc4088_b3_scale_uniqueness_resolution_synthesis.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
