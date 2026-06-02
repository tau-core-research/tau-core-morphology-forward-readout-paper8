#!/usr/bin/env python3
"""Build a claim-bounded predeclaration protocol sheet for Paper 8."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


PROTOCOL_ROWS = [
    {
        "protocol_layer": "primary_endpoint_lane",
        "predeclared_choice": "no_low_inclination",
        "rule": "Exclude galaxies with manifest caveat low_inclination before endpoint scoring.",
        "purpose": "Balance morphology-specific shuffled-null support and baseline competitiveness.",
        "source": "endpoint_decision_matrix.csv",
        "forbidden_inputs": "vobs endpoint residual gain; required_S_tau; posthoc gate choice",
        "claim_status": "candidate_primary_endpoint",
    },
    {
        "protocol_layer": "fuller_sample_support_lane",
        "predeclared_choice": "all",
        "rule": "Run the same endpoint on all available holdout galaxies as support and stress test.",
        "purpose": "Preserve larger-sample morphology-label specificity evidence.",
        "source": "quality_gate_shuffled_null_summary.csv",
        "forbidden_inputs": "posthoc exclusion after endpoint scoring",
        "claim_status": "specificity_support_not_baseline_claim",
    },
    {
        "protocol_layer": "baseline_secondary_lane",
        "predeclared_choice": "no_large_distance_error",
        "rule": "Exclude galaxies with manifest caveat large_distance_error before endpoint scoring.",
        "purpose": "Stress baseline competitiveness under a broader observability rule.",
        "source": "endpoint_decision_matrix.csv",
        "forbidden_inputs": "baseline-driven posthoc filtering",
        "claim_status": "secondary_endpoint_candidate",
    },
    {
        "protocol_layer": "amplitude_policy",
        "predeclared_choice": "train_selected_family_to_global_shrinkage_0_40",
        "rule": "Use family_weight=0.40 selected from train split metrics only.",
        "purpose": "Avoid choosing the amplitude shrinkage weight directly from holdout.",
        "source": "train_selected_shrinkage_selection.csv",
        "forbidden_inputs": "holdout-selected amplitude; per-galaxy endpoint amplitude tuning",
        "claim_status": "diagnostic_policy_pending_tau_side_normalization",
    },
    {
        "protocol_layer": "morphology_family_assignment",
        "predeclared_choice": "residual_blind_manifest_formula_family",
        "rule": "Assign K_g from the morphology manifest before scoring.",
        "purpose": "Prevent formula-family labels from using residual endpoints.",
        "source": "morphology_parameter_manifest.csv",
        "forbidden_inputs": "vobs residual shape; required_S_tau; family choice by fit quality",
        "claim_status": "required_for_tau_core_specificity",
    },
    {
        "protocol_layer": "primary_specificity_metric",
        "predeclared_choice": "matched_beats_wrong_fraction_and_mean_matched_minus_wrong",
        "rule": "Compare matched family against wrong-family mean and shuffled-family null.",
        "purpose": "Test Tau Core morphology-family specificity, not merely lower residuals.",
        "source": "quality_gate_shuffled_null_summary.csv",
        "forbidden_inputs": "dropping wrong families after seeing scores",
        "claim_status": "primary_claim_metric",
    },
    {
        "protocol_layer": "baseline_metrics",
        "predeclared_choice": "TPG_v6_and_MOND_win_fractions",
        "rule": "Report matched-family win fractions against TPG/v6 and MOND comparators.",
        "purpose": "Keep standard baseline comparison visible without overclaiming.",
        "source": "predeclared_quality_gate_diagnostics.csv",
        "forbidden_inputs": "baseline replacement claim from diagnostic-only results",
        "claim_status": "secondary_comparator_metric",
    },
    {
        "protocol_layer": "caveated_rows",
        "predeclared_choice": "preserve_as_limited_observability_evidence",
        "rule": "Do not discard caveated rows from the package; report them in support/control lanes.",
        "purpose": "Preserve negative and limited-observability evidence.",
        "source": "family_observable_quality_diagnostics.csv",
        "forbidden_inputs": "silent removal of difficult galaxies",
        "claim_status": "claim_boundary_requirement",
    },
]


def load_decision_matrix() -> pd.DataFrame:
    path = DATA / "endpoint_decision_matrix.csv"
    if not path.exists():
        raise FileNotFoundError(f"{path} is missing; run scripts/run_endpoint_decision_matrix.py")
    return pd.read_csv(path)


def build_protocol() -> pd.DataFrame:
    protocol = pd.DataFrame(PROTOCOL_ROWS)
    decision = load_decision_matrix()
    lookup = decision.set_index("quality_gate").to_dict(orient="index")
    for gate in ["no_low_inclination", "all", "no_large_distance_error"]:
        if gate not in lookup:
            raise ValueError(f"Expected decision-matrix gate missing: {gate}")
    metric_rows = []
    for layer, gate in [
        ("primary_endpoint_lane", "no_low_inclination"),
        ("fuller_sample_support_lane", "all"),
        ("baseline_secondary_lane", "no_large_distance_error"),
    ]:
        row = lookup[gate]
        metric_rows.append(
            {
                "protocol_layer": f"{layer}_current_metrics",
                "predeclared_choice": gate,
                "rule": (
                    f"n={int(row['n_galaxies'])}; "
                    f"matched_vs_wrong={row['matched_beats_wrong_fraction']:.3f}; "
                    f"TPG_v6={row['matched_beats_tpg_v6_fraction']:.3f}; "
                    f"MOND={row['matched_beats_mond_fraction']:.3f}; "
                    f"p_beats_wrong={row['p_beats_wrong_fraction_at_least_as_good']:.4f}; "
                    f"p_mean={row['p_mean_minus_wrong_at_least_as_good']:.4f}"
                ),
                "purpose": "Record current preparation-state metrics for this lane.",
                "source": "endpoint_decision_matrix.csv",
                "forbidden_inputs": "interpreting preparation metrics as final validation",
                "claim_status": row["recommended_endpoint_role"],
            }
        )
    return pd.concat([protocol, pd.DataFrame(metric_rows)], ignore_index=True)


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def write_report(protocol: pd.DataFrame) -> None:
    lines = [
        "# Predeclared Endpoint Protocol",
        "",
        "This protocol sheet records the current preparation-state endpoint lanes",
        "that should be predeclared before any future Paper 8 endpoint scoring.",
        "It is not a discovery claim and does not prove Tau Core.",
        "",
        "## Protocol Rows",
        "",
        markdown_table(protocol),
        "",
        "## Pass/Fail Interpretation",
        "",
        "- A primary pass requires the primary lane to preserve matched-vs-wrong",
        "  morphology specificity against shuffled labels while remaining visible",
        "  against TPG/v6 and MOND comparators.",
        "- A secondary pass can support baseline competitiveness or fuller-sample",
        "  specificity, but cannot replace the primary lane on its own.",
        "- A failure must be preserved as evidence against the current manifest,",
        "  formula family, amplitude policy, or quality-gate choice.",
        "",
        "## Claim Boundary",
        "",
        "This is a predeclaration aid. The next endpoint run must freeze these",
        "choices before endpoint scoring, and must not silently drop caveated or",
        "negative rows after seeing the residual scores.",
    ]
    (REPORTS / "predeclared_endpoint_protocol.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    protocol = build_protocol()
    protocol.to_csv(DATA / "predeclared_endpoint_protocol.csv", index=False)
    write_report(protocol)
    print("PAPER8_PREDECLARED_ENDPOINT_PROTOCOL_COMPLETE")


if __name__ == "__main__":
    main()
