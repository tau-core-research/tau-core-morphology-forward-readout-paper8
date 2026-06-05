#!/usr/bin/env python3
"""Audit the NGC4088 physical normalization-law status.

The NGC4088 warp/asymmetry lane now has a source-filled closure basis and a
dimensionful delta-v-squared carrier.  This script separates formula-level
consistency from a derived Tau-side physical normalization law.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_ngc4088_physical_normalization_law_gate_not_endpoint"


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
    xw = pd.read_csv(DATA / "s4g75_ngc4088_xw_conversion_audit.csv").iloc[0]
    constants = pd.read_csv(DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_constants.csv")
    profile = pd.read_csv(DATA / "s4g75_ngc4088_kernel_to_velocity_normalization_profile.csv")
    preflight = pd.read_csv(DATA / "s4g75_ngc4088_readout_preflight_profile.csv")

    values = dict(zip(constants["constant_name"], constants["constant_value"]))
    units = dict(zip(constants["constant_name"], constants["unit"]))
    vflat2 = float(values["velocity_scale_candidate"])
    c_warp = float(values["c_warp_candidate"])
    prefactor = float(profile["normalization_prefactor_km2_s2"].iloc[0])
    expected_prefactor = c_warp * vflat2
    prefactor_ok = abs(prefactor - expected_prefactor) < 1.0e-9
    inner_zero = (
        profile.loc[
            profile["x_R_over_RHI"] <= profile["filled_x_warp_onset"] + 1.0e-12,
            "delta_v2_warp_candidate",
        ]
        .le(1.0e-12)
        .all()
    )
    nonnegative = profile["delta_v2_warp_candidate"].ge(-1.0e-12).all()
    residual_blind = (
        not preflight["uses_vobs_for_generation"].any()
        and not preflight["endpoint_scores_allowed"].any()
        and not preflight["endpoint_scores_computed"].any()
    )

    formula = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "formula_id": "NGC4088-WARP-DELTA-V2-CANDIDATE-001",
                "candidate_formula": (
                    "delta_v2_warp(R;p) = "
                    "sigma_warp q_warp x_w Vflat^2 C_warp(R/R_HI; x_w, p)"
                ),
                "expanded_prefactor": "sigma_warp=1, q_warp=1, x_w=0.282353, Vflat^2=29480.89 km2_s2",
                "normalization_prefactor_km2_s2": prefactor,
                "proof_status": "FORMULA_CONDITIONAL_NOT_TAU_SIDE_LAW",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "DIMENSIONAL_CONSISTENCY",
                "gate_status": "PASS" if units["velocity_scale_candidate"] == "km2_s2" else "BLOCKED",
                "evidence": "candidate maps a dimensionless source basis into delta v^2 units",
                "remaining_obligation": "none at dimensional-audit level",
            },
            {
                "gate_id": "PREFACTOR_REPRODUCED",
                "gate_status": "PASS" if prefactor_ok else "BLOCKED",
                "evidence": "normalization_prefactor = x_w * Vflat^2 for sigma=q=1",
                "remaining_obligation": "derive why this product is physically selected",
            },
            {
                "gate_id": "SOURCE_ONSET_SUPPRESSION",
                "gate_status": "PASS" if inner_zero else "BLOCKED",
                "evidence": "delta v^2 vanishes at and inside the measured source onset",
                "remaining_obligation": "independent onset review remains separate",
            },
            {
                "gate_id": "POSITIVE_WARP_ORIENTATION",
                "gate_status": "PASS" if nonnegative else "BLOCKED",
                "evidence": "candidate warp/asymmetry contribution is nonnegative in this orientation",
                "remaining_obligation": "derive orientation sign from Tau-side readout geometry",
            },
            {
                "gate_id": "RESIDUAL_BLIND_EXPORT",
                "gate_status": "PASS" if residual_blind else "BLOCKED",
                "evidence": "candidate profile generation uses no observed velocity or endpoint score",
                "remaining_obligation": "keep endpoint scoring in a separate frozen protocol",
            },
            {
                "gate_id": "FORMULA_LEVEL_CANDIDATE",
                "gate_status": "FORMULA_CONDITIONAL",
                "evidence": "candidate formula is executable and dimensionally consistent",
                "remaining_obligation": "not yet a Tau-side physical normalization law",
            },
            {
                "gate_id": "TAU_SIDE_VARIATIONAL_OR_CLOSURE_DERIVATION",
                "gate_status": "BLOCKED",
                "evidence": "no derivation yet selects x_w Vflat^2 as the unique closure-readout scale",
                "remaining_obligation": "derive from Tau-side closure/readout principle or predeclare as theory axiom",
            },
            {
                "gate_id": "SCALE_UNIQUENESS",
                "gate_status": "BLOCKED",
                "evidence": "other residual-blind scales could be considered without overfitting",
                "remaining_obligation": "show this scale beats alternatives by theory criteria before endpoint use",
            },
            {
                "gate_id": "POPULATION_TRANSFER",
                "gate_status": "BLOCKED",
                "evidence": "normalization is currently one-galaxy source-filled",
                "remaining_obligation": "repeat on a predeclared warp/asymmetry source-rich sample",
            },
        ]
    )
    gates["galaxy"] = "NGC4088"
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    status_counts = gates["gate_status"].value_counts().to_dict()
    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "n_gates": len(gates),
                "n_pass": int(status_counts.get("PASS", 0)),
                "n_formula_conditional": int(status_counts.get("FORMULA_CONDITIONAL", 0)),
                "n_blocked": int(status_counts.get("BLOCKED", 0)),
                "normalization_prefactor_km2_s2": prefactor,
                "law_status": "FORMULA_CONDITIONAL_PHYSICAL_LAW_BLOCKED",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return formula, gates, summary


def write_report(formula: pd.DataFrame, gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NGC4088 Physical Normalization-Law Gate",
        "",
        "This audit separates a formula-consistent NGC4088 warp/asymmetry",
        "normalization candidate from an accepted Tau-side physical readout law.",
        "",
        "## Verdict",
        "",
        "The candidate is dimensionally consistent and residual-blind, but it is",
        "only formula-conditional. The remaining law-level blockers are the",
        "Tau-side derivation of the scale, scale uniqueness, and population",
        "transfer.",
        "",
        "## Candidate Formula",
        "",
        markdown_table(formula),
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
        "This gate does not compare the candidate to observed velocities and does",
        "not authorize endpoint scoring. It only states that the current",
        "NGC4088 normalization is formula-conditional, not a derived final",
        "Tau-side readout law.",
        "",
    ]
    (REPORTS / "s4g75_ngc4088_physical_normalization_law_gate.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    formula, gates, summary = build_gate()
    formula.to_csv(DATA / "s4g75_ngc4088_physical_normalization_formula.csv", index=False)
    gates.to_csv(DATA / "s4g75_ngc4088_physical_normalization_law_gate.csv", index=False)
    summary.to_csv(DATA / "s4g75_ngc4088_physical_normalization_law_summary.csv", index=False)
    write_report(formula, gates, summary)
    print("PAPER8_NGC4088_PHYSICAL_NORMALIZATION_LAW_GATE_COMPLETE")


if __name__ == "__main__":
    main()
