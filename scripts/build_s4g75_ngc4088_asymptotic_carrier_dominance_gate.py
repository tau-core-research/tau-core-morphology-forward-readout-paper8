#!/usr/bin/env python3
"""Audit the NGC4088 asymptotic-carrier dominance obligation.

This is a subgate of the Tau-side scale derivation chain.  It asks whether
Vflat^2 is derived as the asymptotic readout carrier, rather than merely used as
a convenient residual-blind catalog scale.  It does not use endpoint velocities,
residuals, or scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "s4g75_ngc4088_asymptotic_carrier_dominance_gate_not_endpoint"


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
    constants = pd.read_csv(DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_constants.csv")
    selection_gate = pd.read_csv(DATA / "s4g75_ngc4088_tau_side_scale_selection_gate.csv")

    constants_by_name = {
        row["constant_name"]: row
        for _, row in constants.iterrows()
    }
    vflat2 = float(constants_by_name["velocity_scale_candidate"]["constant_value"])
    vflat_unit = constants_by_name["velocity_scale_candidate"]["unit"]
    vflat_status = constants_by_name["velocity_scale_candidate"]["proof_status"]

    selected = selection_gate[
        selection_gate["selection_gate_status"]
        == "SELECTED_BY_MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE"
    ].iloc[0]

    carrier = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "carrier_id": "VFLAT2_ASYMPTOTIC_CARRIER_CANDIDATE",
                "source_constant": "velocity_scale_candidate",
                "selected_scale_id": selected["scale_id"],
                "carrier_value_km2_s2": vflat2,
                "unit": vflat_unit,
                "source_status": vflat_status,
                "current_interpretation": "SOURCE_CATALOG_SCALE_CANDIDATE_NOT_DERIVED_CARRIER",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "A1_CATALOG_ASYMPTOTIC_SCALE_AVAILABLE",
                "gate_status": "PASS",
                "evidence": "Vflat^2 is available as a residual-blind source/catalog velocity-squared scale",
                "remaining_obligation": "none at availability level",
            },
            {
                "gate_id": "A2_DIMENSIONAL_CARRIER",
                "gate_status": "PASS" if vflat_unit == "km2_s2" else "BLOCKED",
                "evidence": "Vflat^2 has the required delta-v-squared dimension",
                "remaining_obligation": "none at dimensional level",
            },
            {
                "gate_id": "A3_POINT_SAMPLED_MEDIANS_REJECTED",
                "gate_status": "PASS",
                "evidence": "selection gate rejects x_w * median_r(v_n^2) and x_w * median_r(v_v6^2)",
                "remaining_obligation": "derive why point-sampled curve statistics are not Tau-side carriers",
            },
            {
                "gate_id": "A4_EXTERNAL_COMPARATOR_REJECTED",
                "gate_status": "PASS",
                "evidence": "selection gate rejects the v_v6 normalizer as an external TPG-like comparator",
                "remaining_obligation": "derive comparator autonomy from the closure/readout architecture",
            },
            {
                "gate_id": "A5_ASYMPTOTIC_READOUT_INTERPRETATION",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "Vflat^2 can be read as an outer/asymptotic source carrier in the current formula shell",
                "remaining_obligation": "show that this interpretation is forced by Tau-side readout geometry",
            },
            {
                "gate_id": "A6_TAU_CLOSURE_DERIVES_VFLAT",
                "gate_status": "BLOCKED",
                "evidence": "no Tau-side closure functional currently solves for Vflat^2 as the preferred carrier",
                "remaining_obligation": "derive the asymptotic carrier from a closure/readout functional",
            },
            {
                "gate_id": "A7_UNIQUENESS_AGAINST_OTHER_ASYMPTOTIC_CARRIERS",
                "gate_status": "BLOCKED",
                "evidence": "other source-native asymptotic carriers could exist but have not been enumerated for a sample",
                "remaining_obligation": "audit Vflat^2 against predeclared alternatives such as HI widths or outer-source speeds",
            },
            {
                "gate_id": "A8_POPULATION_TRANSFER",
                "gate_status": "BLOCKED",
                "evidence": "current carrier-dominance audit is NGC4088-specific",
                "remaining_obligation": "test the same residual-blind carrier rule on a predeclared warp/asymmetry population",
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
                "carrier_id": "VFLAT2_ASYMPTOTIC_CARRIER_CANDIDATE",
                "selected_scale_id": selected["scale_id"],
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "dominance_status": "ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED",
                "law_status": "VFLAT2_SOURCE_CANDIDATE_NOT_TAU_SIDE_CARRIER_PROOF",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return carrier, gates, summary


def write_report(carrier: pd.DataFrame, gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Asymptotic-Carrier Dominance Gate",
        "",
        "This subgate asks whether `Vflat^2` is a derived asymptotic Tau-side",
        "readout carrier, rather than merely a residual-blind catalog scale.",
        "",
        "## Verdict",
        "",
        "`Vflat^2` passes availability and dimensional checks, and the selection",
        "protocol rejects point-sampled medians and external TPG-like comparators.",
        "However, asymptotic-carrier dominance is not derived: a Tau-side",
        "closure/readout functional and population transfer remain blocked.",
        "",
        "## Carrier",
        "",
        markdown_table(carrier),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "This audit preserves the distinction between a source-catalog carrier",
        "candidate and a derived Tau-side carrier. It uses no endpoint residuals",
        "or observed rotation velocities.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_asymptotic_carrier_dominance_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    carrier, gates, summary = build_gate()
    carrier.to_csv(DATA / "s4g75_ngc4088_asymptotic_carrier_candidate.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_asymptotic_carrier_dominance_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_asymptotic_carrier_dominance_summary.csv", index=False)
    write_report(carrier, gates, summary)
    print("PAPER8_NGC4088_ASYMPTOTIC_CARRIER_DOMINANCE_GATE_COMPLETE")


if __name__ == "__main__":
    main()
