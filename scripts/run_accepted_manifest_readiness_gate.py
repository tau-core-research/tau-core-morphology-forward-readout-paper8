#!/usr/bin/env python3
"""Evaluate whether an accepted-observable manifest may enter the blind endpoint."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


GATE_DEFINITIONS = [
    {
        "gate": "row_identity_and_geometry_ready",
        "required_status": "PASS",
        "field_group": "galaxy; inclination_deg; distance_frac_error",
        "decision_rule": "all rows have identifiers and pre-scoring geometry fields",
    },
    {
        "gate": "residual_blind_family_labels_ready",
        "required_status": "PASS",
        "field_group": "formula_family",
        "decision_rule": "all rows have accepted residual-blind family labels",
    },
    {
        "gate": "quality_and_caveat_ready",
        "required_status": "PASS",
        "field_group": "manifest_confidence; manifest_caveat",
        "decision_rule": "all rows have pre-scoring confidence and caveat fields",
    },
    {
        "gate": "active_kernel_observables_ready",
        "required_status": "PASS",
        "field_group": "scale_radius_kpc; tail_inner_radius_kpc; tail_cutoff_radius_kpc; compact_support_radius_kpc; thickness_h_over_rs",
        "decision_rule": "all active-family rows have required source-native kernel observables",
    },
    {
        "gate": "provenance_ready",
        "required_status": "PASS",
        "field_group": "observable_provenance",
        "decision_rule": "all accepted observables have dataset/method/pre-scoring provenance",
    },
    {
        "gate": "optional_non_axisymmetric_not_promoted",
        "required_status": "PASS_OR_CAVEATED",
        "field_group": "ring_radius_kpc; bar_m2_strength; lopsided_m1_strength",
        "decision_rule": "optional branches are either supplied from external support or kept out of primary 1D endpoint",
    },
]


def field_status(validation: pd.DataFrame, fields: list[str]) -> pd.DataFrame:
    return validation[validation["field"].isin(fields)]


def evaluate_gate(validation: pd.DataFrame, definition: dict[str, str]) -> dict[str, object]:
    fields = [field.strip() for field in definition["field_group"].split(";")]
    subset = field_status(validation, fields)
    required_subset = subset[subset["required"]]
    blocked = required_subset[
        required_subset["template_validation_status"]
        == "blocked_missing_required_accepted_source"
    ]
    missing_rows = int(blocked["n_missing_rows"].sum())
    if missing_rows == 0:
        status = "PASS"
    else:
        status = "BLOCKED"
    if definition["required_status"] == "PASS_OR_CAVEATED":
        optional_problem = subset[
            subset["template_validation_status"]
            == "optional_missing_or_caveated"
        ]
        status = "PASS_OR_CAVEATED" if optional_problem.empty else "CAVEATED"
    return {
        "gate": definition["gate"],
        "required_status": definition["required_status"],
        "field_group": definition["field_group"],
        "gate_status": status,
        "blocked_missing_rows": missing_rows,
        "decision_rule": definition["decision_rule"],
        "next_action": (
            "ready for blind endpoint precheck"
            if status in {"PASS", "PASS_OR_CAVEATED"}
            else "populate accepted residual-blind fields before endpoint scoring"
        ),
    }


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    decision = summary["endpoint_readiness_decision"].iloc[0]
    blocked = gates[gates["gate_status"] == "BLOCKED"]
    lines = [
        "# Accepted Manifest Readiness Gate",
        "",
        "This gate decides whether a populated accepted-observable manifest may enter",
        "the frozen blind endpoint protocol. It is a data-readiness gate, not an",
        "endpoint score and not an empirical validation claim.",
        "",
        "This gate is not an endpoint score.",
        "",
        "## Verdict",
        "",
        f"Endpoint readiness decision: `{decision}`.",
        f"Blocked gates: {len(blocked)}.",
        "",
        "The current empty accepted manifest template is correctly blocked. This",
        "preserves the claim boundary: the proxy manifest cannot be silently used as",
        "a discovery input.",
        "",
        "## Gate Status",
        "",
        markdown_table(gates),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "A PASS here would only authorize running the frozen endpoint protocol on",
        "accepted residual-blind inputs. It would not by itself imply that Tau Core",
        "fits better than MOND, RAR, TGP, or Newtonian baselines.",
    ]
    (REPORTS / "accepted_manifest_readiness_gate.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    validation = pd.read_csv(DATA / "accepted_observable_manifest_template_validation.csv")
    gates = pd.DataFrame([evaluate_gate(validation, item) for item in GATE_DEFINITIONS])
    blocked = gates[gates["gate_status"] == "BLOCKED"]
    decision = (
        "READY_FOR_FROZEN_BLIND_ENDPOINT"
        if blocked.empty
        else "BLOCKED_ACCEPTED_OBSERVABLES_MISSING"
    )
    summary = pd.DataFrame(
        [
            {
                "endpoint_readiness_decision": decision,
                "n_gates": len(gates),
                "n_blocked_gates": len(blocked),
                "n_blocked_missing_rows_total": int(blocked["blocked_missing_rows"].sum()),
                "claim_status": "data_ready_only" if blocked.empty else "not_endpoint_ready",
            }
        ]
    )
    gates.to_csv(DATA / "accepted_manifest_readiness_gates.csv", index=False)
    summary.to_csv(DATA / "accepted_manifest_readiness_summary.csv", index=False)
    write_report(gates, summary)
    print("PAPER8_ACCEPTED_MANIFEST_READINESS_GATE_COMPLETE")


if __name__ == "__main__":
    main()
