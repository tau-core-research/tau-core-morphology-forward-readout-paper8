#!/usr/bin/env python3
"""Synthesize the NGC4183 pre-endpoint decision state."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4183_preendpoint_decision_synthesis_not_endpoint"
GALAXY = "NGC4183"


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


def read_summary(path: str) -> pd.Series:
    return pd.read_csv(DATA / path).iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    source = read_summary("ngc4183_mixed_overlay_source_audit_summary.csv")
    observable = read_summary("ngc4183_mixed_overlay_observable_sheet_summary.csv")
    label = read_summary("ngc4183_projection_outer_warp_label_summary.csv")
    formula = read_summary("ngc4183_projection_outer_warp_formula_summary.csv")
    gamma = read_summary("ngc4183_projection_gamma_coefficient_summary.csv")
    tilted = read_summary("ngc4183_tilted_ring_orientation_profile_summary.csv")
    upper = read_summary("ngc4183_projection_gamma_upper_bound_summary.csv")

    chain = pd.DataFrame(
        [
            {
                "stage": "source_audit",
                "status": source["source_audit_status"],
                "allowed_next": "observable_sheet",
                "endpoint_scores_allowed": False,
                "main_message": "galaxy-specific H I source is present",
            },
            {
                "stage": "observable_sheet",
                "status": observable["observable_sheet_status"],
                "allowed_next": "label_narrowing",
                "endpoint_scores_allowed": False,
                "main_message": "RHI and projection observables are available; broad overlay fields missing",
            },
            {
                "stage": "label_gate",
                "status": label["label_gate_status"],
                "allowed_next": "formula_derivation",
                "endpoint_scores_allowed": False,
                "main_message": "narrow projection/outer-warp caveated label supported for derivation",
            },
            {
                "stage": "formula_derivation",
                "status": formula["formula_derivation_status"],
                "allowed_next": "coefficient_gate",
                "endpoint_scores_allowed": False,
                "main_message": "projection attenuation shell derived; coefficient blocked",
            },
            {
                "stage": "gamma_coefficient_gate",
                "status": gamma["gamma_gate_status"],
                "allowed_next": "tilted_ring_profile_review",
                "endpoint_scores_allowed": False,
                "main_message": "no source-blind gamma coefficient frozen",
            },
            {
                "stage": "tilted_ring_profile",
                "status": tilted["tilted_ring_profile_status"],
                "allowed_next": "upper_bound_or_independent_review",
                "endpoint_scores_allowed": False,
                "main_message": "source profile extracted; nearly constant orientation",
            },
            {
                "stage": "gamma_upper_bound",
                "status": upper["upper_bound_gate_status"],
                "allowed_next": "weak_control_or_more_data",
                "endpoint_scores_allowed": False,
                "main_message": "source-side projection bound is very small",
            },
        ]
    )

    decisions = pd.DataFrame(
        [
            {
                "decision_id": "D1_STRONG_ENDPOINT",
                "decision": "REJECT_FOR_NOW",
                "evidence": f"gamma upper bound {upper['gamma_projection_upper_bound']:.6g}",
                "consequence": "do not run NGC4183 as a strong projection endpoint from current sources",
            },
            {
                "decision_id": "D2_WEAK_PROJECTION_CONTROL",
                "decision": "PROMOTE_AS_CONTROL_CANDIDATE",
                "evidence": "source-native H I profile supports edge-on/projection caveat but weak radial orientation drift",
                "consequence": "NGC4183 can test whether the protocol correctly predicts a near-carrier result",
            },
            {
                "decision_id": "D3_MORE_DATA_ROUTE",
                "decision": "OPTIONAL_ACQUIRE",
                "evidence": "OCR profile needs independent review; no numeric warp onset/amplitude",
                "consequence": "machine-readable tilted-ring or velocity-field source could reopen endpoint path",
            },
            {
                "decision_id": "D4_NO_RESIDUAL_PATCHING",
                "decision": "PASS_GUARDRAIL",
                "evidence": "all gates keep endpoint_scores_allowed=False",
                "consequence": "do not tune gamma_proj using observed rotation residuals",
            },
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "preendpoint_decision_status": "NGC4183_PREENDPOINT_SYNTHESIS_WEAK_PROJECTION_CONTROL_NOT_ENDPOINT",
                "galaxy": GALAXY,
                "current_role": "WEAK_PROJECTION_CONTROL_CANDIDATE",
                "strong_endpoint_supported": False,
                "gamma_projection_upper_bound": float(upper["gamma_projection_upper_bound"]),
                "max_abs_pa_drift_deg": float(tilted["max_abs_pa_drift_deg"]),
                "max_abs_inclination_drift_deg": float(tilted["max_abs_inclination_drift_deg"]),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "either_independent_source_review_then_null_control_freeze_or_acquire_better_velocity_field",
            }
        ]
    )

    chain.to_csv(DATA / "ngc4183_preendpoint_decision_chain.csv", index=False)
    decisions.to_csv(DATA / "ngc4183_preendpoint_decisions.csv", index=False)
    summary.to_csv(DATA / "ngc4183_preendpoint_decision_summary.csv", index=False)

    report = f"""# NGC4183 Pre-Endpoint Decision Synthesis

Status: `{summary.iloc[0]["preendpoint_decision_status"]}`

This synthesis combines the NGC4183 source audit, observable sheet, label gate,
formula derivation, coefficient gate, tilted-ring extraction, and projection
upper-bound gate.  It does not score an endpoint.

## Summary

{markdown_table(summary)}

## Gate Chain

{markdown_table(chain)}

## Decisions

{markdown_table(decisions)}

## Scientific Interpretation

NGC4183 is no longer merely a context-only candidate: it has source-native H I
geometry, a strong edge-on projection observable, and a consistent H I support
radius.  However, the extracted tilted-ring orientation profile is almost flat:
the PA drift is only about 3 degrees and the inclination drift is zero in the
current extraction.  The resulting source-side projection coefficient bound is
therefore tiny.

This is useful.  It means the pipeline should not force NGC4183 into a strong
Tau Core projection endpoint.  With the present sources it is better treated as
a weak-projection control candidate: the protocol predicts that a large
projection correction is not source-supported.  A stronger endpoint route would
require better source-native velocity-field or tilted-ring data, not residual
tuning.
"""
    (REPORTS / "ngc4183_preendpoint_decision_synthesis.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
