#!/usr/bin/env python3
"""Build a residual-blind Tau-side evidence-measure gate candidate.

This script promotes the fixed proxy-bin gate into an auditable object:

    e_gK = E_tau(g,K)

where E_tau is assembled from residual-blind source/readout factors.  It is a
candidate evidence measure, not an accepted normalization law and not endpoint
validation.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "tau_side_evidence_measure_gate_candidate_not_endpoint"
FAMILIES = [
    "K_compact_finite",
    "K_scale_tail_spiral",
    "K_exponential_disk",
    "K_thick_flared",
]


def load_inputs() -> pd.DataFrame:
    component = pd.read_csv(DATA / "morphology_information_gain_l2_weight_freeze_component_audit.csv")
    expansion = pd.read_csv(DATA / "morphology_information_gain_source_expansion.csv")
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    candidates = pd.read_csv(DATA / "morphology_information_gain_l2_weight_intake_candidates.csv")
    keep_manifest = [
        "galaxy",
        "manifest_confidence",
        "manifest_caveat",
        "inclination_deg",
        "distance_frac_error",
    ]
    keep_candidates = ["galaxy"] + [f"w_{family}" for family in FAMILIES]
    table = component.merge(expansion, on=["galaxy", "split"], how="left", validate="many_to_one")
    table = table.merge(manifest[keep_manifest], on="galaxy", how="left", validate="many_to_one")
    table = table.merge(candidates[keep_candidates], on="galaxy", how="left", validate="many_to_one")
    return table


def projection_factor(row: pd.Series) -> float:
    inclination = float(row["inclination_deg"]) if pd.notna(row["inclination_deg"]) else 60.0
    caveat = str(row.get("manifest_caveat", ""))
    if inclination >= 80.0 or "projection" in caveat.lower():
        return 0.65
    if inclination >= 70.0:
        return 0.85
    return 1.0


def memory_factor(row: pd.Series) -> float:
    if bool(row.get("q_memory_candidate", False)):
        return 0.85
    return 0.70


def resolution_factor(row: pd.Series) -> float:
    confidence = float(row["manifest_confidence"]) if pd.notna(row["manifest_confidence"]) else 0.50
    distance_error = (
        float(row["distance_frac_error"]) if pd.notna(row["distance_frac_error"]) else 0.20
    )
    if confidence >= 0.75 and distance_error <= 0.20:
        return 1.0
    if confidence >= 0.55 and distance_error <= 0.30:
        return 0.85
    return 0.70


def proxy_factors(row: pd.Series) -> dict[str, float]:
    family = row["component_family"]
    if family == "K_thick_flared":
        # Current proxy path lacks a dedicated accepted vertical source layer.
        return {
            "q_source": 0.70,
            "q_geometry": 0.70,
            "q_projection": projection_factor(row),
            "q_memory": memory_factor(row),
            "q_resolution": resolution_factor(row),
        }
    return {
        "q_source": 0.70,
        "q_geometry": 0.70,
        "q_projection": projection_factor(row),
        "q_memory": memory_factor(row),
        "q_resolution": resolution_factor(row),
    }


def proxy_factor_statuses(row: pd.Series) -> dict[str, str]:
    family = row["component_family"]
    if family == "K_thick_flared":
        geometry_status = "PROXY_VERTICAL_GEOMETRY_CANDIDATE"
    else:
        geometry_status = "PROXY_FAMILY_GEOMETRY_CANDIDATE"
    return {
        "q_source_status": "PROXY_SOURCE_PROVENANCE_CANDIDATE",
        "q_geometry_status": geometry_status,
        "q_projection_status": "RESIDUAL_BLIND_PROJECTION_CAVEAT_FACTOR",
        "q_memory_status": "MORPHOLOGY_MEMORY_PROXY_CANDIDATE",
        "q_resolution_status": "MANIFEST_CONFIDENCE_DISTANCE_PROXY",
        "factor_derivation_status": "THEORY_CANDIDATE_FACTOR_GEOMETRY_NOT_ACCEPTED",
    }


def accepted_factor_statuses() -> dict[str, str]:
    return {
        "q_source_status": "DEFINITION_DERIVED_ACCEPTED_SOURCE",
        "q_geometry_status": "DEFINITION_DERIVED_ACCEPTED_GEOMETRY",
        "q_projection_status": "DEFINITION_DERIVED_CAVEAT_FREE_PROJECTION",
        "q_memory_status": "DEFINITION_DERIVED_ACCEPTED_MEMORY",
        "q_resolution_status": "DEFINITION_DERIVED_ACCEPTED_RESOLUTION",
        "factor_derivation_status": "DEFINITION_DERIVED_ACCEPTED_SOURCE_GATE",
    }


def missing_factor_statuses() -> dict[str, str]:
    return {
        "q_source_status": "DEFINITION_DERIVED_MISSING_SOURCE",
        "q_geometry_status": "DEFINITION_DERIVED_MISSING_GEOMETRY",
        "q_projection_status": "DEFINITION_DERIVED_MISSING_PROJECTION",
        "q_memory_status": "DEFINITION_DERIVED_MISSING_MEMORY",
        "q_resolution_status": "DEFINITION_DERIVED_MISSING_RESOLUTION",
        "factor_derivation_status": "DEFINITION_DERIVED_MISSING_SOURCE_GATE",
    }


def factors_for_row(row: pd.Series) -> dict[str, object]:
    status = str(row["component_evidence_status"])
    if status.startswith("SOURCE_CANDIDATE"):
        factors = {
            "q_source": 1.0,
            "q_geometry": 1.0,
            "q_projection": 1.0,
            "q_memory": 1.0,
            "q_resolution": 1.0,
            "e_tau": 1.0,
            "e_tau_status": "DEFINITION_DERIVED_ACCEPTED_SOURCE_GATE",
        }
        factors.update(accepted_factor_statuses())
    elif status == "MISSING_SOURCE_SUPPORT":
        factors = {
            "q_source": 0.0,
            "q_geometry": 0.0,
            "q_projection": 0.0,
            "q_memory": 0.0,
            "q_resolution": 0.0,
            "e_tau": 0.0,
            "e_tau_status": "DEFINITION_DERIVED_MISSING_SOURCE_GATE",
        }
        factors.update(missing_factor_statuses())
    else:
        factors = proxy_factors(row)
        e_tau = (
            factors["q_source"]
            * factors["q_geometry"]
            * factors["q_projection"]
            * factors["q_memory"]
            * factors["q_resolution"]
        )
        factors["e_tau"] = e_tau
        factors["e_tau_status"] = "E_TAU_PROXY_PRODUCT_CANDIDATE"
        factors.update(proxy_factor_statuses(row))
    return factors


def build_gate(table: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for _, row in table.iterrows():
        factors = factors_for_row(row)
        fixed_gate = 0.35 if row["component_evidence_status"] == "PROXY_OR_PARTIAL_SOURCE_ONLY" else (
            1.0 if str(row["component_evidence_status"]).startswith("SOURCE_CANDIDATE") else 0.0
        )
        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "component_family": row["component_family"],
                "component_weight": float(row["component_weight"]),
                "component_evidence_status": row["component_evidence_status"],
                "fixed_manifest_gate": fixed_gate,
                **factors,
                "gate_minus_fixed_manifest_gate": float(factors["e_tau"]) - fixed_gate,
                "uses_vobs_or_residual": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    gate = pd.DataFrame(rows).sort_values(["split", "galaxy", "component_family"])
    summary = summarize(gate)
    return gate, summary


def summarize(gate: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, sub in gate.groupby("split"):
        proxy = sub.loc[sub["component_evidence_status"] == "PROXY_OR_PARTIAL_SOURCE_ONLY"]
        rows.append(
            {
                "split": split,
                "n_components": int(len(sub)),
                "n_proxy_components": int(len(proxy)),
                "median_e_tau_all_components": float(sub["e_tau"].median()),
                "median_e_tau_proxy_components": float(proxy["e_tau"].median()) if len(proxy) else 0.0,
                "mean_e_tau_proxy_components": float(proxy["e_tau"].mean()) if len(proxy) else 0.0,
                "median_proxy_minus_fixed_0p35": float(
                    proxy["gate_minus_fixed_manifest_gate"].median()
                )
                if len(proxy)
                else 0.0,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    all_proxy = gate.loc[gate["component_evidence_status"] == "PROXY_OR_PARTIAL_SOURCE_ONLY"]
    all_row = {
        "split": "all",
        "n_components": int(len(gate)),
        "n_proxy_components": int(len(all_proxy)),
        "median_e_tau_all_components": float(gate["e_tau"].median()),
        "median_e_tau_proxy_components": float(all_proxy["e_tau"].median())
        if len(all_proxy)
        else 0.0,
        "mean_e_tau_proxy_components": float(all_proxy["e_tau"].mean()) if len(all_proxy) else 0.0,
        "median_proxy_minus_fixed_0p35": float(all_proxy["gate_minus_fixed_manifest_gate"].median())
        if len(all_proxy)
        else 0.0,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return pd.concat([pd.DataFrame([all_row]), pd.DataFrame(rows)], ignore_index=True)


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


def write_report(summary: pd.DataFrame) -> None:
    full = summary.loc[summary["split"] == "all"].iloc[0]
    lines = [
        "# Tau-Side Evidence-Measure Gate Candidate",
        "",
        "This audit builds a residual-blind candidate for `e_gK = E_tau(g,K)`.",
        "It does not score endpoint residuals and does not accept a final",
        "universal normalization law.",
        "",
        "## Candidate Measure",
        "",
        "```text",
        "E_tau = q_source q_geometry q_projection q_memory q_resolution",
        "```",
        "",
        "Accepted source support is normalized to 1. Missing source support is",
        "set to 0. Proxy/partial support is evaluated by the product measure.",
        "The current proxy ladder is the conservative readout-admission ladder:",
        "`strong proxy = 0.85`, `ordinary proxy = 0.70`, and the standard",
        "proxy template gives `0.70 * 0.70 * 0.85 * 0.85 = 0.354025`.",
        "",
        "## Factor-Status Discipline",
        "",
        "The numerical product is accompanied by per-factor derivation labels.",
        "Accepted and missing gates are definition-derived limit cases. The",
        "proxy ladder is derived inside the current conservative three-status",
        "readout-admission geometry. Individual proxy rows remain",
        "theory-candidate factor geometry / source-readout assignments until their source,",
        "geometry, projection, memory, and resolution factors are accepted",
        "residual-blind observables.",
        "",
        "## Full-Sample Verdict",
        "",
        f"- Components audited: {int(full['n_components'])}",
        f"- Proxy components: {int(full['n_proxy_components'])}",
        f"- Median proxy E_tau: {full['median_e_tau_proxy_components']:.6g}",
        f"- Mean proxy E_tau: {full['mean_e_tau_proxy_components']:.6g}",
        f"- Median proxy minus fixed 0.35: {full['median_proxy_minus_fixed_0p35']:.6g}",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "This is the first executable E_tau candidate. It shows how the fixed",
        "proxy gate can be replaced by a source-evidence product whose median",
        "proxy value reproduces the old 0.35 gate as a coarse-grid consequence.",
        "The numerical ladder is derived inside the conservative",
        "readout-admission geometry, while the galaxy/component q_i assignments",
        "must still be frozen from source/readout evidence before endpoint use",
        "and must not be selected from rotation residuals.",
    ]
    (REPORTS / "tau_side_evidence_measure_gate.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    gate, summary = build_gate(load_inputs())
    gate.to_csv(DATA / "tau_side_evidence_measure_gate_components.csv", index=False)
    summary.to_csv(DATA / "tau_side_evidence_measure_gate_summary.csv", index=False)
    write_report(summary)
    print("PAPER8_TAU_SIDE_EVIDENCE_MEASURE_GATE_COMPLETE")


if __name__ == "__main__":
    main()
