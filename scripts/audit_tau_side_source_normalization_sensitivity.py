#!/usr/bin/env python3
"""Audit sensitivity of the Tau-side source-normalization candidate.

The source-normalized L2 rule is theory-conditional because the orientation
signs still need source-native promotion and the proxy-evidence gate value still
needs an independent Tau-side evidence-measure derivation.
This script runs predeclared variants of those assumptions.  It is an audit,
not a model-selection step.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

import run_tau_side_source_normalized_l2_endpoint as base


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "tau_side_source_normalization_sensitivity_not_model_selection"

def variants_from_manifest() -> list[dict[str, object]]:
    primary_signs, evidence_gate, _ = base.load_normalization_constants()
    proxy_gate = evidence_gate["PROXY_OR_PARTIAL_SOURCE_ONLY"]
    missing_gate = evidence_gate["MISSING_SOURCE_SUPPORT"]
    return [
        {
            "variant_id": "primary_proxy_gate_0p35",
            "variant_role": "primary_formula_conditional_candidate_from_derivation_manifest",
            "signs": primary_signs,
            "proxy_gate": proxy_gate,
            "missing_gate": missing_gate,
        },
        {
            "variant_id": "no_proxy_gate_0p00",
            "variant_role": "accepted_source_only_control",
            "signs": primary_signs,
            "proxy_gate": 0.0,
            "missing_gate": missing_gate,
        },
        {
            "variant_id": "weak_proxy_gate_0p20",
            "variant_role": "proxy_gate_sensitivity",
            "signs": primary_signs,
            "proxy_gate": 0.20,
            "missing_gate": missing_gate,
        },
        {
            "variant_id": "strong_proxy_gate_0p50",
            "variant_role": "proxy_gate_sensitivity",
            "signs": primary_signs,
            "proxy_gate": 0.50,
            "missing_gate": missing_gate,
        },
        {
            "variant_id": "full_proxy_gate_1p00",
            "variant_role": "proxy_gate_stress_control",
            "signs": primary_signs,
            "proxy_gate": 1.0,
            "missing_gate": missing_gate,
        },
        {
            "variant_id": "all_positive_orientation",
            "variant_role": "orientation_control",
            "signs": {family: 1.0 for family in base.FAMILIES},
            "proxy_gate": proxy_gate,
            "missing_gate": missing_gate,
        },
        {
            "variant_id": "all_negative_orientation",
            "variant_role": "orientation_control",
            "signs": {family: -1.0 for family in base.FAMILIES},
            "proxy_gate": proxy_gate,
            "missing_gate": missing_gate,
        },
    ]


def gate_for_status(status: str, proxy_gate: float, missing_gate: float) -> float:
    if str(status).startswith("SOURCE_CANDIDATE"):
        return 1.0
    if status == "PROXY_OR_PARTIAL_SOURCE_ONLY":
        return proxy_gate
    return missing_gate


def build_component_rule_variant(
    weights: pd.DataFrame,
    scales: pd.DataFrame,
    component_audit: pd.DataFrame,
    variant: dict[str, object],
) -> pd.DataFrame:
    evidence = base.component_evidence_map(component_audit)
    table = weights.merge(scales, on="galaxy", how="left", validate="one_to_one")
    rows = []
    signs = variant["signs"]
    proxy_gate = float(variant["proxy_gate"])
    missing_gate = float(variant["missing_gate"])
    for _, row in table.iterrows():
        for family in base.FAMILIES:
            status = evidence.get((row["galaxy"], family), "MISSING_SOURCE_SUPPORT")
            gate = gate_for_status(status, proxy_gate, missing_gate)
            weight = float(row[f"w_{family}"])
            signed_strength = (
                float(signs[family])
                * gate
                * weight
                * float(row["closure_fraction_c"])
                * float(row["source_vn2_median"])
            )
            rows.append(
                {
                    "variant_id": variant["variant_id"],
                    "galaxy": row["galaxy"],
                    "split": row["split"],
                    "component_family": family,
                    "intake_weight": weight,
                    "component_evidence_status": status,
                    "evidence_gate": gate,
                    "orientation_sign": float(signs[family]),
                    "closure_fraction_c": float(row["closure_fraction_c"]),
                    "source_vn2_median": float(row["source_vn2_median"]),
                    "kernel_scale": float(row[f"kernel_scale_{family}"]),
                    "signed_source_strength_v2": signed_strength,
                    "beta_source_normalized": signed_strength
                    / float(row[f"kernel_scale_{family}"]),
                    "uses_vobs_or_residual": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def run_variant(
    points: pd.DataFrame,
    weights: pd.DataFrame,
    scales: pd.DataFrame,
    component_audit: pd.DataFrame,
    variant: dict[str, object],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    component_rule = build_component_rule_variant(weights, scales, component_audit, variant)
    scored = base.add_predictions(points, component_rule)
    scores, summary = base.score(scored)
    scores.insert(0, "variant_id", variant["variant_id"])
    summary.insert(0, "variant_id", variant["variant_id"])
    scores["claim_boundary"] = CLAIM_BOUNDARY
    summary["claim_boundary"] = CLAIM_BOUNDARY
    component_rule["variant_role"] = variant["variant_role"]
    return component_rule, scores, summary


def variant_manifest(variants: list[dict[str, object]]) -> pd.DataFrame:
    rows = []
    for variant in variants:
        signs = variant["signs"]
        rows.append(
            {
                "variant_id": variant["variant_id"],
                "variant_role": variant["variant_role"],
                "proxy_gate": variant["proxy_gate"],
                "missing_gate": variant["missing_gate"],
                "sign_K_compact_finite": signs["K_compact_finite"],
                "sign_K_scale_tail_spiral": signs["K_scale_tail_spiral"],
                "sign_K_exponential_disk": signs["K_exponential_disk"],
                "sign_K_thick_flared": signs["K_thick_flared"],
                "selection_policy": "predeclared_sensitivity_audit_not_endpoint_selection",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


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


def write_report(manifest: pd.DataFrame, summary: pd.DataFrame) -> None:
    holdout = summary.loc[summary["split"] == "holdout"].copy()
    primary = holdout.loc[holdout["variant_id"] == "primary_proxy_gate_0p35"].iloc[0]
    lines = [
        "# Tau-Side Source-Normalization Sensitivity Audit",
        "",
        "This audit varies only the theory-gated orientation signs and",
        "source-evidence gates. It does not choose a winning variant and it does",
        "not promote the normalization rule to an accepted Tau-side law.",
        "",
        "## Primary Holdout Reference",
        "",
        f"- Beats old L2 intake endpoint: {primary['beats_old_l2_intake_fraction']:.3f}",
        f"- Beats TPG/v6: {primary['beats_tpg_v6_fraction']:.3f}",
        f"- Beats MOND: {primary['beats_mond_fraction']:.3f}",
        f"- Median minus old L2 RMSE: {primary['median_source_norm_minus_old_l2_intake']:.6g}",
        "",
        "## Variant Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Holdout Sensitivity",
        "",
        markdown_table(
            holdout[
                [
                    "variant_id",
                    "beats_old_l2_intake_fraction",
                    "beats_tpg_v6_fraction",
                    "beats_mond_fraction",
                    "median_source_norm_minus_old_l2_intake",
                    "median_source_norm_minus_tpg_v6",
                    "median_source_norm_minus_mond",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "The sensitivity table is an audit of the weakest conditional step. A",
        "better-looking variant must not be selected for the paper endpoint unless",
        "its signs and gates are independently derived before endpoint scoring.",
    ]
    (REPORTS / "tau_side_source_normalization_sensitivity.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    points, weights, component_audit = base.load_inputs()
    scales = base.source_scales(points)
    variants = variants_from_manifest()
    manifest = variant_manifest(variants)
    all_components = []
    all_scores = []
    all_summary = []
    for variant in variants:
        components, scores, summary = run_variant(points, weights, scales, component_audit, variant)
        all_components.append(components)
        all_scores.append(scores)
        all_summary.append(summary)
    components_df = pd.concat(all_components, ignore_index=True)
    scores_df = pd.concat(all_scores, ignore_index=True)
    summary_df = pd.concat(all_summary, ignore_index=True)
    manifest.to_csv(DATA / "tau_side_source_normalization_sensitivity_manifest.csv", index=False)
    components_df.to_csv(DATA / "tau_side_source_normalization_sensitivity_components.csv", index=False)
    scores_df.to_csv(DATA / "tau_side_source_normalization_sensitivity_scores.csv", index=False)
    summary_df.to_csv(DATA / "tau_side_source_normalization_sensitivity_summary.csv", index=False)
    write_report(manifest, summary_df)
    print("PAPER8_TAU_SIDE_SOURCE_NORMALIZATION_SENSITIVITY_COMPLETE")


if __name__ == "__main__":
    main()
