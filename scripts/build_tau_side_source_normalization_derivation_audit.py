#!/usr/bin/env python3
"""Build the Tau-side source-normalization derivation/audit manifest.

The source-normalized L2 rule has two theory-gated ingredients:

1. readout-orientation signs sigma_K;
2. source-evidence gates e_gK.

This script records the minimal proof status for those ingredients. It is a
derivation audit, not an endpoint scorer and not empirical validation.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "source_normalization_derivation_audit_not_endpoint"


ORIENTATION_ROWS = [
    {
        "constant_type": "orientation_sign",
        "constant_key": "K_compact_finite",
        "constant_value": 1.0,
        "tau_side_rationale": "compact finite support acts as an attractive finite-source residual in the current readout orientation",
        "proof_status": "THEORY_CONDITIONAL",
        "weakest_step": "finite-source orientation is bridge-derived but not yet promoted by a covariant Tau-side variational principle",
    },
    {
        "constant_type": "orientation_sign",
        "constant_key": "K_scale_tail_spiral",
        "constant_value": 1.0,
        "tau_side_rationale": "outer tail support carries a positive closure-source orientation in the n=2 tail readout",
        "proof_status": "THEORY_CONDITIONAL",
        "weakest_step": "tail-source orientation is bridge-derived under the current n=2 Poisson-like readout shell",
    },
    {
        "constant_type": "orientation_sign",
        "constant_key": "K_exponential_disk",
        "constant_value": -1.0,
        "tau_side_rationale": "regular exponential disk component is treated as a smoothing/counter-readout against over-strong closure residual",
        "proof_status": "THEORY_CONDITIONAL",
        "weakest_step": "counter-readout sign is bridge-derived as smoothing orientation but needs source-native slice promotion",
    },
    {
        "constant_type": "orientation_sign",
        "constant_key": "K_thick_flared",
        "constant_value": -1.0,
        "tau_side_rationale": "thick/flared vertical geometry is treated as a smoothing/projection attenuation channel",
        "proof_status": "THEORY_CONDITIONAL",
        "weakest_step": "vertical smoothing sign is bridge-derived as projection attenuation but needs source-native 3D/4D readout promotion",
    },
]


GATE_ROWS = [
    {
        "constant_type": "evidence_gate",
        "constant_key": "SOURCE_CANDIDATE_COMPACT_READY",
        "constant_value": 1.0,
        "tau_side_rationale": "source-candidate component is fully admitted into the prefreeze candidate rule",
        "proof_status": "DEFINITION_DEPENDENT",
        "weakest_step": "source candidate is not yet accepted endpoint evidence",
    },
    {
        "constant_type": "evidence_gate",
        "constant_key": "SOURCE_CANDIDATE_HI_TAIL_READY",
        "constant_value": 1.0,
        "tau_side_rationale": "source-candidate component is fully admitted into the prefreeze candidate rule",
        "proof_status": "DEFINITION_DEPENDENT",
        "weakest_step": "source candidate is not yet accepted endpoint evidence",
    },
    {
        "constant_type": "evidence_gate",
        "constant_key": "SOURCE_CANDIDATE_S4G_SCALE_READY",
        "constant_value": 1.0,
        "tau_side_rationale": "source-candidate component is fully admitted into the prefreeze candidate rule",
        "proof_status": "DEFINITION_DEPENDENT",
        "weakest_step": "source candidate is not yet accepted endpoint evidence",
    },
    {
        "constant_type": "evidence_gate",
        "constant_key": "SOURCE_CANDIDATE_VELOCITY_FIELD_READY",
        "constant_value": 1.0,
        "tau_side_rationale": "velocity-field supported source candidate is fully admitted into the prefreeze candidate rule",
        "proof_status": "DEFINITION_DEPENDENT",
        "weakest_step": "no full-sample velocity-field layer is assembled yet",
    },
    {
        "constant_type": "evidence_gate",
        "constant_key": "PROXY_OR_PARTIAL_SOURCE_ONLY",
        "constant_value": 0.35,
        "tau_side_rationale": "coarse executable representative of the conservative Tau-side proxy-admission product; exact median proxy E_tau is 0.354025",
        "proof_status": "DERIVED_COARSE_GRID_PROXY_ADMISSION_PRODUCT",
        "weakest_step": "derived inside the current conservative three-status readout-admission geometry; not a final universal evidence geometry",
    },
    {
        "constant_type": "evidence_gate",
        "constant_key": "MISSING_SOURCE_SUPPORT",
        "constant_value": 0.0,
        "tau_side_rationale": "missing source support contributes no candidate component",
        "proof_status": "DERIVED_FROM_GATE_DEFINITION",
        "weakest_step": "none for the candidate gate; absence of source is a zero candidate by definition",
    },
]


RULE_ROWS = [
    {
        "rule_component": "normalized_shape",
        "formula": "K_gK(r) / median_r |K_gK(r)|",
        "dimension_status": "dimensionless",
        "proof_status": "DEFINITION_DEPENDENT",
        "edge_case": "zero kernel median is guarded by unit fallback in code",
    },
    {
        "rule_component": "closure_fraction",
        "formula": "median_r max(v_v6^2 - v_n^2, 0) / median_r v_v6^2",
        "dimension_status": "dimensionless",
        "proof_status": "THEORY_CONDITIONAL",
        "edge_case": "vanishes in quiet Newtonian-like closure or where v_v6 does not exceed v_n",
    },
    {
        "rule_component": "source_strength",
        "formula": "c_g median_r(v_n^2)",
        "dimension_status": "velocity_squared",
        "proof_status": "THEORY_CONDITIONAL",
        "edge_case": "zero baryonic velocity scale suppresses the candidate residual",
    },
    {
        "rule_component": "component_delta_v2",
        "formula": "sigma_K e_gK w_gK c_g median_r(v_n^2) normalized_shape_gK(r)",
        "dimension_status": "velocity_squared",
        "proof_status": "THEORY_CONDITIONAL",
        "edge_case": "missing source support or zero weight suppresses component",
    },
]


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: f"{value:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def write_report(constants: pd.DataFrame, rule: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# Tau-Side Source-Normalization Derivation Audit",
        "",
        "This audit records the proof status of the source-normalized L2 rule.",
        "It does not compute endpoint scores and does not validate Tau Core.",
        "",
        "## Verdict",
        "",
        "The normalization rule is dimensionally consistent as a delta-v-squared",
        "candidate. Its orientation signs are THEORY-CONDITIONAL bridge",
        "derivations.",
        "The proxy evidence attenuation is no longer treated as a free protocol",
        "constant: the fixed 0.35 gate is the coarse executable representative",
        "of the conservative Tau-side readout-admission product",
        "`0.70 * 0.70 * 0.85 * 0.85 = 0.354025`.",
        "The remaining caveat is that this is derived inside the current",
        "minimal conservative evidence geometry, not as a final universal",
        "Tau-side evidence law.",
        "",
        "## Constants",
        "",
        markdown_table(constants),
        "",
        "## Rule Components",
        "",
        markdown_table(rule),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "A future endpoint may use these constants only after the theory-gated",
        "orientation and proxy-gate steps are independently derived or frozen by a",
        "pre-endpoint theory decision.",
        "They must not be selected from endpoint residuals.",
    ]
    (REPORTS / "tau_side_source_normalization_derivation_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    constants = pd.DataFrame(ORIENTATION_ROWS + GATE_ROWS)
    constants["claim_boundary"] = CLAIM_BOUNDARY
    rule = pd.DataFrame(RULE_ROWS)
    rule["claim_boundary"] = CLAIM_BOUNDARY
    summary = (
        constants.groupby(["constant_type", "proof_status"], as_index=False)
        .agg(n_constants=("constant_key", "count"))
        .sort_values(["constant_type", "proof_status"])
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY
    constants.to_csv(DATA / "tau_side_source_normalization_derivation_constants.csv", index=False)
    rule.to_csv(DATA / "tau_side_source_normalization_derivation_rule.csv", index=False)
    summary.to_csv(DATA / "tau_side_source_normalization_derivation_summary.csv", index=False)
    write_report(constants, rule, summary)
    print("PAPER8_TAU_SIDE_SOURCE_NORMALIZATION_DERIVATION_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
