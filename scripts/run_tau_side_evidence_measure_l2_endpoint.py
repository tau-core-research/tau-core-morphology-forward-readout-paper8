#!/usr/bin/env python3
"""Run an endpoint stress test with E_tau source-evidence gates.

This is a preflight comparison against the fixed proxy-bin source-normalized
candidate.  It uses the same residual-blind readout weights, signs, source
scales, and kernels, but replaces fixed source-evidence gates by the
component-specific E_tau gate built upstream.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

import run_tau_side_source_normalized_l2_endpoint as base


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "tau_side_evidence_measure_l2_endpoint_preflight_not_validation"


def build_component_rule_with_e_tau(
    weights: pd.DataFrame, scales: pd.DataFrame, component_audit: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    orientation_sign, _, proof_status = base.load_normalization_constants()
    e_tau = pd.read_csv(DATA / "tau_side_evidence_measure_gate_components.csv")
    e_map = {
        (row["galaxy"], row["component_family"]): row
        for _, row in e_tau.iterrows()
    }
    evidence = base.component_evidence_map(component_audit)
    table = weights.merge(scales, on="galaxy", how="left", validate="one_to_one")
    component_rows = []
    galaxy_rows = []
    for _, row in table.iterrows():
        active_strengths = {}
        for family in base.FAMILIES:
            status = evidence.get((row["galaxy"], family), "MISSING_SOURCE_SUPPORT")
            e_row = e_map.get((row["galaxy"], family))
            gate = float(e_row["e_tau"]) if e_row is not None else 0.0
            e_tau_status = e_row["e_tau_status"] if e_row is not None else "MISSING_E_TAU_COMPONENT"
            weight = float(row[f"w_{family}"])
            signed_strength = (
                orientation_sign[family]
                * gate
                * weight
                * float(row["closure_fraction_c"])
                * float(row["source_vn2_median"])
            )
            beta = signed_strength / float(row[f"kernel_scale_{family}"])
            active_strengths[family] = signed_strength
            component_rows.append(
                {
                    "galaxy": row["galaxy"],
                    "split": row["split"],
                    "component_family": family,
                    "intake_weight": weight,
                    "component_evidence_status": status,
                    "e_tau_gate": gate,
                    "e_tau_status": e_tau_status,
                    "orientation_sign": orientation_sign[family],
                    "orientation_sign_proof_status": proof_status[family],
                    "closure_fraction_c": float(row["closure_fraction_c"]),
                    "source_vn2_median": float(row["source_vn2_median"]),
                    "kernel_scale": float(row[f"kernel_scale_{family}"]),
                    "signed_source_strength_v2": signed_strength,
                    "beta_source_normalized": beta,
                    "uses_vobs_or_residual": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        galaxy_rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "dominant_intake_family": row["dominant_intake_family"],
                "closure_fraction_c": float(row["closure_fraction_c"]),
                "source_vn2_median": float(row["source_vn2_median"]),
                "net_signed_source_strength_v2": float(sum(active_strengths.values())),
                "positive_component_strength_v2": float(
                    sum(value for value in active_strengths.values() if value > 0.0)
                ),
                "negative_component_strength_v2": float(
                    sum(value for value in active_strengths.values() if value < 0.0)
                ),
                "normalization_rule_status": "E_TAU_EVIDENCE_MEASURE_PREFLIGHT",
                "endpoint_freeze_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(component_rows), pd.DataFrame(galaxy_rows)


def write_report(summary: pd.DataFrame) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].iloc[0]
    lines = [
        "# Tau-Side E_tau L2 Endpoint Preflight",
        "",
        "This preflight replaces the fixed proxy-bin source-evidence gate with",
        "the residual-blind E_tau(g,K) evidence-measure candidate. It is not a",
        "model-selection step and not validation.",
        "",
        "## Holdout Verdict",
        "",
        f"- Holdout galaxies: {int(holdout['n_galaxies'])}",
        f"- Beats old L2 intake endpoint: {holdout['beats_old_l2_intake_fraction']:.3f}",
        f"- Beats TPG/v6: {holdout['beats_tpg_v6_fraction']:.3f}",
        f"- Beats MOND: {holdout['beats_mond_fraction']:.3f}",
        f"- Median E_tau-minus-old-L2 RMSE: {holdout['median_source_norm_minus_old_l2_intake']:.6g}",
        "",
        "## Summary",
        "",
        base.markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "This test uses E_tau as a candidate evidence measure. The conservative",
        "proxy-bin ladder is derived inside the current Tau-side",
        "readout-admission geometry, but the per-galaxy and per-component q_i",
        "assignments are not yet accepted source-native observables. A better",
        "or worse endpoint result must not be used to choose the evidence",
        "measure or the q_i assignments.",
    ]
    (REPORTS / "tau_side_evidence_measure_l2_endpoint.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, weights, component_audit = base.load_inputs()
    scales = base.source_scales(points)
    component_rule, galaxy_rule = build_component_rule_with_e_tau(weights, scales, component_audit)
    scored = base.add_predictions(points, component_rule)
    scores, summary = base.score(scored)
    scores["claim_boundary"] = CLAIM_BOUNDARY
    summary["claim_boundary"] = CLAIM_BOUNDARY
    component_rule.to_csv(DATA / "tau_side_evidence_measure_l2_component_rule.csv", index=False)
    galaxy_rule.to_csv(DATA / "tau_side_evidence_measure_l2_galaxy_rule.csv", index=False)
    scores.to_csv(DATA / "tau_side_evidence_measure_l2_endpoint_scores.csv", index=False)
    summary.to_csv(DATA / "tau_side_evidence_measure_l2_endpoint_summary.csv", index=False)
    write_report(summary)
    print("PAPER8_TAU_SIDE_EVIDENCE_MEASURE_L2_ENDPOINT_COMPLETE")


if __name__ == "__main__":
    main()
