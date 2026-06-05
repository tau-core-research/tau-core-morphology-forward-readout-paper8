#!/usr/bin/env python3
"""Build the NGC4088 Tau-side scale derivation gate.

The preceding scale-selection gate conditionally selects x_w * Vflat^2 from
residual-blind alternatives.  This script records what would be needed to turn
that conditional selection rule into a derived Tau-side closure/readout law.
It deliberately does not use endpoint velocities, residuals, or scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_tau_side_scale_derivation_gate_not_endpoint"


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


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    selection_summary = pd.read_csv(
        DATA / "s4g75_ngc4088_tau_side_scale_selection_summary.csv"
    ).iloc[0]
    selected_scale = selection_summary["selected_scale_ids"]

    skeleton = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "selected_scale_id": selected_scale,
                "conditional_statement": (
                    "If the Tau-side warp/asymmetry closure readout is local at "
                    "the source onset, asymptotically carried by the catalog "
                    "flat-speed scale, autonomous from external closure "
                    "comparators, and minimal in source factors, then the "
                    "dimensionful carrier reduces to x_w * Vflat^2."
                ),
                "derived_formula_if_all_gates_pass": (
                    "delta_v2_warp(R;p) = sigma_warp q_warp x_w Vflat^2 "
                    "C_warp(R/R_HI; x_w, p)"
                ),
                "current_status": "DERIVATION_SKELETON_NOT_PROOF",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "G1_DIMENSIONAL_LIMIT",
                "gate_status": "PASS",
                "evidence": "x_w and C_warp are dimensionless; Vflat^2 carries km^2/s^2",
                "remaining_obligation": "none at dimensional level",
            },
            {
                "gate_id": "G2_SOURCE_ONSET_LOCALITY",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "x_w is residual-blind and source-measured from the WHISP channel-map protocol",
                "remaining_obligation": "derive why the source onset enters linearly in the Tau-side readout scale",
            },
            {
                "gate_id": "G3_ASYMPTOTIC_CARRIER_DOMINANCE",
                "gate_status": "BLOCKED",
                "evidence": "the rule selects Vflat^2, but no Tau-side closure functional yet proves asymptotic carrier dominance",
                "remaining_obligation": "derive Vflat^2 as the asymptotic readout carrier rather than a catalog convenience",
            },
            {
                "gate_id": "G4_EXTERNAL_COMPARATOR_AUTONOMY",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "the selection rule rejects v_v6 and other TPG-like comparator normalizers",
                "remaining_obligation": "derive comparator autonomy from Tau-side readout closure, not just by protocol choice",
            },
            {
                "gate_id": "G5_MINIMAL_SOURCE_FACTOR_RULE",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "the rule rejects composite x_w * c_g * median(v_n^2)-type carriers",
                "remaining_obligation": "derive minimal single-source-factor preference or state it as a Tau-side axiom",
            },
            {
                "gate_id": "G6_TAU_SIDE_CLOSURE_FUNCTIONAL",
                "gate_status": "BLOCKED",
                "evidence": "no variational or closure-readout functional has yet generated the selected carrier",
                "remaining_obligation": "construct the Tau-side closure functional whose solved scale is x_w * Vflat^2",
            },
            {
                "gate_id": "G7_POPULATION_TRANSFER",
                "gate_status": "BLOCKED",
                "evidence": "the gate is currently one-galaxy NGC4088-specific",
                "remaining_obligation": "repeat the same residual-blind derivation gate on a predeclared warp/asymmetry sample",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    status_counts = gates["gate_status"].value_counts().to_dict()
    summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "selected_scale_id": selected_scale,
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "derivation_status": "DERIVATION_BLOCKED_SELECTION_RULE_AUDITED",
                "law_status_after_derivation_gate": "NOT_DERIVED_TAU_SIDE_LAW",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return skeleton, gates, summary


def write_report(skeleton: pd.DataFrame, gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Tau-Side Scale Derivation Gate",
        "",
        "This gate records the missing derivation behind the conditional",
        "`MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE`. It is not an endpoint",
        "test and not a proof of a final 4D readout law.",
        "",
        "## Verdict",
        "",
        "The selected `x_w * Vflat^2` carrier has dimensional support and a",
        "residual-blind onset input, but the Tau-side physical law remains",
        "blocked. The missing pieces are asymptotic carrier dominance, a",
        "closure/readout functional, and population transfer.",
        "",
        "## Conditional Skeleton",
        "",
        markdown_table(skeleton),
        "",
        "## Derivation Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "This derivation gate preserves the negative result: a conditional",
        "selection rule has been audited, but the Tau-side law has not been",
        "derived. No observed rotation velocities or endpoint residuals are used.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_tau_side_scale_derivation_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    skeleton, gates, summary = build_gate()
    skeleton.to_csv(DATA / "s4g75_ngc4088_tau_side_scale_derivation_skeleton.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_tau_side_scale_derivation_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_tau_side_scale_derivation_summary.csv", index=False)
    write_report(skeleton, gates, summary)
    print("PAPER8_NGC4088_TAU_SIDE_SCALE_DERIVATION_GATE_COMPLETE")


if __name__ == "__main__":
    main()
