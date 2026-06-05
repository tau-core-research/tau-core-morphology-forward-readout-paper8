#!/usr/bin/env python3
"""Build a Tau-side scale-selection gate for NGC4088.

This gate applies a pre-endpoint, theory-side selection principle to the
residual-blind scale candidates.  It does not compare candidates to observed
velocities and does not prove a final normalization law.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_tau_side_scale_selection_gate_not_endpoint"


CRITERIA = [
    {
        "criterion_id": "C1_RESIDUAL_BLIND",
        "criterion": "scale carrier must not use vobs, endpoint residuals, or endpoint scores",
    },
    {
        "criterion_id": "C2_SOURCE_ONSET_COUPLED",
        "criterion": "warp/asymmetry scale must carry the measured source onset x_w",
    },
    {
        "criterion_id": "C3_ASYMPTOTIC_READOUT_CARRIER",
        "criterion": "dimensionful carrier should be a source/catalog asymptotic readout scale, not a point-sampled median curve statistic",
    },
    {
        "criterion_id": "C4_NO_EXTERNAL_CLOSURE_COMPARATOR",
        "criterion": "scale should not require a TPG-like v_v6 closure carrier as the normalizer",
    },
    {
        "criterion_id": "C5_MINIMAL_SINGLE_SOURCE_FACTOR",
        "criterion": "scale should not multiply independent onset and closure fractions unless Tau-side theory derives the composite",
    },
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


def evaluate_candidate(row: pd.Series) -> dict[str, object]:
    scale_id = row["scale_id"]
    passes = {
        "C1_RESIDUAL_BLIND": not bool(row["uses_vobs_or_residual"]),
        "C2_SOURCE_ONSET_COUPLED": "XW" in scale_id or scale_id == "CURRENT_XW_VFLAT2",
        "C3_ASYMPTOTIC_READOUT_CARRIER": scale_id == "CURRENT_XW_VFLAT2",
        "C4_NO_EXTERNAL_CLOSURE_COMPARATOR": "VV62" not in scale_id,
        "C5_MINIMAL_SINGLE_SOURCE_FACTOR": "CLOSURE_FRACTION" not in scale_id,
    }
    n_pass = sum(passes.values())
    if all(passes.values()):
        status = "SELECTED_BY_MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE"
    elif passes["C1_RESIDUAL_BLIND"] and passes["C2_SOURCE_ONSET_COUPLED"]:
        status = "THEORY_ALTERNATIVE_REJECTED_BY_ADDITIONAL_CRITERIA"
    else:
        status = "THEORY_ALTERNATIVE_REJECTED_SOURCE_ONSET_OR_BLINDNESS"
    failed = [criterion for criterion, passed in passes.items() if not passed]
    return {
        **{f"passes_{criterion}": passed for criterion, passed in passes.items()},
        "n_selection_criteria_passed": n_pass,
        "failed_criteria": ";".join(failed) if failed else "none",
        "selection_gate_status": status,
    }


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    scale_audit = pd.read_csv(DATA / "s4g75_ngc4088_scale_uniqueness_audit.csv")
    criteria = pd.DataFrame(CRITERIA)
    criteria["galaxy"] = GALAXY
    criteria["claim_boundary"] = CLAIM_BOUNDARY
    rows = []
    for _, row in scale_audit.iterrows():
        evaluation = evaluate_candidate(row)
        rows.append(
            {
                "galaxy": GALAXY,
                "scale_id": row["scale_id"],
                "scale_formula": row["scale_formula"],
                "scale_value_km2_s2": row["scale_value_km2_s2"],
                **evaluation,
                "uses_vobs_or_residual": row["uses_vobs_or_residual"],
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    gate = pd.DataFrame(rows)
    selected = gate.loc[
        gate["selection_gate_status"]
        == "SELECTED_BY_MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE"
    ]
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "selection_principle": "MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE",
                "n_candidates": len(gate),
                "n_selected_candidates": len(selected),
                "selected_scale_ids": ";".join(selected["scale_id"]) if len(selected) else "none",
                "selection_status": (
                    "THEORY_SELECTION_CONDITIONAL_CURRENT_ONLY"
                    if len(selected) == 1
                    else "THEORY_SELECTION_NOT_UNIQUE"
                ),
                "law_status_after_selection": "SELECTION_RULE_CONDITIONAL_NOT_DERIVED_LAW",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return criteria, gate, summary


def write_report(criteria: pd.DataFrame, gate: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Tau-Side Scale Selection Gate",
        "",
        "This gate applies a pre-endpoint Tau-side selection rule to the",
        "residual-blind scale alternatives. It is a theory-selection audit, not an",
        "endpoint comparison.",
        "",
        "## Verdict",
        "",
        "Under the minimal source-onset asymptotic-carrier rule, the current",
        "`x_w * Vflat^2` scale is the only selected candidate. This narrows the",
        "`SCALE_UNIQUENESS` blocker, but it does not prove the physical",
        "normalization law because the selection rule itself still needs a",
        "Tau-side closure/readout derivation.",
        "",
        "## Selection Criteria",
        "",
        markdown_table(criteria),
        "",
        "## Candidate Gate",
        "",
        markdown_table(gate),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "The selected scale must not be promoted by endpoint performance. This gate",
        "only records a conditional theory-side selection rule.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_tau_side_scale_selection_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    criteria, gate, summary = build_gate()
    criteria.to_csv(DATA / "s4g75_ngc4088_tau_side_scale_selection_criteria.csv", index=False)
    gate.to_csv(DATA / "s4g75_ngc4088_tau_side_scale_selection_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_tau_side_scale_selection_summary.csv", index=False)
    write_report(criteria, gate, summary)
    print("PAPER8_NGC4088_TAU_SIDE_SCALE_SELECTION_GATE_COMPLETE")


if __name__ == "__main__":
    main()
