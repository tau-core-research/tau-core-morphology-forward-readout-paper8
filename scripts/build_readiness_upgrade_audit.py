#!/usr/bin/env python3
"""Summarize the upgraded Paper 8 preparation state after diagnostics."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


REQUIRED_FILES = {
    "source_native_formula_preflight": DATA / "source_native_readout_formula_endpoint_summary.csv",
    "train_selected_shrinkage": DATA / "train_selected_shrinkage_holdout.csv",
    "family_breakdown": DATA / "family_breakdown_diagnostics.csv",
    "observable_quality": DATA / "family_observable_quality_diagnostics.csv",
    "predeclared_quality_gates": DATA / "predeclared_quality_gate_diagnostics.csv",
    "quality_gate_shuffled_null": DATA / "quality_gate_shuffled_null_summary.csv",
    "endpoint_decision_matrix": DATA / "endpoint_decision_matrix.csv",
    "predeclared_endpoint_protocol": DATA / "predeclared_endpoint_protocol.csv",
}


def require_inputs() -> None:
    missing = [name for name, path in REQUIRED_FILES.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing readiness inputs: {', '.join(missing)}")


def metric(path: str, where: dict[str, object], column: str) -> object:
    df = pd.read_csv(DATA / path)
    mask = pd.Series(True, index=df.index)
    for key, value in where.items():
        mask &= df[key] == value
    return df.loc[mask, column].iloc[0]


def build_rows() -> pd.DataFrame:
    require_inputs()
    decision = pd.read_csv(DATA / "endpoint_decision_matrix.csv")
    protocol = pd.read_csv(DATA / "predeclared_endpoint_protocol.csv")
    primary = decision.loc[decision["recommended_endpoint_role"] == "primary_endpoint_candidate"].iloc[0]
    rows = [
        {
            "readiness_layer": "paper1_3_inheritance",
            "status": "ready",
            "evidence": "Paper 1-3 bridge path is explicit in manuscript and foundation audit.",
            "next_action": "Keep citations and claim boundary stable.",
        },
        {
            "readiness_layer": "source_native_formula_preflight",
            "status": "diagnostic_ready",
            "evidence": (
                "Concrete bridge formula kernels run on 175-galaxy proxy manifest; "
                "holdout matched-vs-wrong signal exists but baseline superiority is not claimed."
            ),
            "next_action": "Replace proxy manifest with accepted residual-blind morphology observables.",
        },
        {
            "readiness_layer": "amplitude_policy",
            "status": "diagnostic_ready",
            "evidence": "Train-only shrinkage selection chooses family_weight=0.40 and transfers to holdout.",
            "next_action": "Derive or justify Tau-side source normalization instead of treating shrinkage as physical law.",
        },
        {
            "readiness_layer": "family_failure_map",
            "status": "ready_for_modeling_triage",
            "evidence": "Family breakdown and observable-quality diagnostics identify quality-limited and current-best-case rows.",
            "next_action": "Prioritize morphology-observable extraction for quality-limited families.",
        },
        {
            "readiness_layer": "quality_gate_controls",
            "status": "diagnostic_ready",
            "evidence": "Predeclared quality gates and shuffled-family nulls expose baseline-vs-null-power tradeoff.",
            "next_action": "Predeclare the gate before any future endpoint scoring.",
        },
        {
            "readiness_layer": "primary_endpoint_candidate",
            "status": "predeclaration_ready",
            "evidence": (
                f"{primary['quality_gate']} is current primary candidate: "
                f"n={int(primary['n_galaxies'])}, "
                f"matched-vs-wrong={primary['matched_beats_wrong_fraction']:.3f}, "
                f"TPG/v6={primary['matched_beats_tpg_v6_fraction']:.3f}, "
                f"MOND={primary['matched_beats_mond_fraction']:.3f}, "
                f"p_beats={primary['p_beats_wrong_fraction_at_least_as_good']:.4f}, "
                f"p_mean={primary['p_mean_minus_wrong_at_least_as_good']:.4f}."
            ),
            "next_action": "Freeze this as a candidate endpoint lane only if the next run uses the same predeclared rule.",
        },
        {
            "readiness_layer": "predeclared_endpoint_protocol",
            "status": "ready",
            "evidence": f"{len(protocol)} protocol rows record lanes, metrics, forbidden inputs, and caveated-row handling.",
            "next_action": "Use the protocol as the next-run guardrail.",
        },
        {
            "readiness_layer": "empirical_discovery_claim",
            "status": "blocked",
            "evidence": "Current outputs are preparation diagnostics on available-data proxies, not a final external endpoint.",
            "next_action": "Do not claim Tau Core validation or baseline replacement.",
        },
        {
            "readiness_layer": "final_paper8_manuscript",
            "status": "not_started",
            "evidence": "Repository currently contains a proposal/preparation manuscript, not a full empirical Paper 8.",
            "next_action": "After accepted morphology observables and predeclared endpoint run, write final results paper.",
        },
    ]
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def write_report(df: pd.DataFrame) -> None:
    counts = df["status"].value_counts().to_dict()
    lines = [
        "# Paper 8 Readiness Upgrade Audit",
        "",
        "This audit summarizes the preparation state after the source-native",
        "formula, shrinkage, quality-gate, shuffled-null, decision-matrix, and",
        "predeclaration diagnostics. It does not claim empirical validation.",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            "## Readiness Rows",
            "",
            markdown_table(df),
            "",
            "## Verdict",
            "",
            "Paper 8 is now preparation-ready as a claim-bounded protocol and",
            "diagnostic package. It is not discovery-ready. The next scientific",
            "upgrade is to replace available-data proxy morphology observables with",
            "accepted residual-blind morphology inputs, then run the predeclared",
            "endpoint protocol without changing gates after seeing scores.",
        ]
    )
    (REPORTS / "paper8_readiness_upgrade_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    rows.to_csv(DATA / "paper8_readiness_upgrade_audit.csv", index=False)
    write_report(rows)
    print("PAPER8_READINESS_UPGRADE_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
