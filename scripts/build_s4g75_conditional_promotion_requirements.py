#!/usr/bin/env python3
"""Build family-specific promotion requirements for S4G75 conditional kernels.

The previous gate found conditional, not strict, kernel-ready rows.  This
script records what must be proven or measured before each conditional row can
be promoted to strict endpoint eligibility.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_conditional_promotion_requirements_not_endpoint"


PROMOTION_RULES = {
    "tail_inner_cutoff_candidate": {
        "promotion_gate": "TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION",
        "family_level_statement": (
            "SPARC HI extent can promote a scale-tail cutoff only if the HI "
            "extent is shown to constrain the same outer-disk transition, "
            "break, truncation, or tail-support radius used by the formula "
            "kernel."
        ),
        "direct_measurement_requirement": (
            "HI radial profile, outer-disk break radius, truncation radius, "
            "tail cutoff radius, or cited source-native transition radius"
        ),
        "theorem_requirement": (
            "prove residual-blind admissibility of RHI as a conservative "
            "upper cutoff for the scale-tail readout kernel, with a fixed "
            "transition rule independent of endpoint residuals"
        ),
        "promotion_pass_condition": (
            "R_tail_in and R_tail_cut are fixed by direct source-native "
            "transition evidence, or by a predeclared theorem that RHI bounds "
            "the tail kernel used by F_K"
        ),
        "promotion_fail_condition": (
            "RHI is used only because it exists as a generic gas extent while "
            "the actual transition profile remains unconstrained"
        ),
    },
    "compact_support_candidate": {
        "promotion_gate": "COMPACT-COMPONENT-SUPPORT-PROMOTION",
        "family_level_statement": (
            "A compact finite-source kernel can promote only if the source "
            "constrains the compact component support radius, not merely an "
            "effective light radius."
        ),
        "direct_measurement_requirement": (
            "bulge/component radius, compact light support, central component "
            "decomposition radius, or source-native compact mass-light support"
        ),
        "theorem_requirement": (
            "prove when Reff or a listed compact component is an admissible "
            "upper/lower support representative for the compact readout kernel"
        ),
        "promotion_pass_condition": (
            "R_compact is fixed by a source-native compact component measure, "
            "or by a predeclared support theorem that maps Reff/component "
            "evidence into the compact kernel"
        ),
        "promotion_fail_condition": (
            "SPARC Reff is substituted for compact support without component "
            "decomposition or a Tau-side support theorem"
        ),
    },
    "thickness_h_over_rs_candidate": {
        "promotion_gate": "EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION",
        "family_level_statement": (
            "An edge-disk component can promote a thick/flared kernel only if "
            "it constrains vertical scale height, flare, warp, or gas-plane "
            "thickness used by the formula kernel."
        ),
        "direct_measurement_requirement": (
            "vertical scale height, h/Rs, flare profile, warp radius, "
            "edge-on thickness measurement, or gas-plane thickness evidence"
        ),
        "theorem_requirement": (
            "prove when an S4G edge-disk component is an admissible "
            "conservative vertical-kernel representative, with fixed h/Rs or "
            "flare bounds not selected from endpoint residuals"
        ),
        "promotion_pass_condition": (
            "h/Rs or flare/warp kernel parameters are measured directly, or "
            "the edge-disk component is promoted through a residual-blind "
            "vertical-kernel theorem"
        ),
        "promotion_fail_condition": (
            "inclination, edge-on appearance, or S4G component naming is used "
            "without a measured vertical kernel parameter or theorem"
        ),
    },
}


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


def build_requirements() -> tuple[pd.DataFrame, pd.DataFrame]:
    gate = pd.read_csv(DATA / "s4g75_kernel_ready_promotion_gate.csv")
    conditional = gate.loc[gate["kernel_promotion_status"] == "KERNEL_READY_CONDITIONAL"].copy()
    rows = []
    for _, row in conditional.iterrows():
        rule = PROMOTION_RULES[row["observable_driver_type"]]
        rows.append(
            {
                "galaxy": row["galaxy"],
                "formula_family": row["formula_family"],
                "source_priority": row["source_priority"],
                "observable_driver_type": row["observable_driver_type"],
                "kernel_specific_source_status": row["kernel_specific_source_status"],
                "promotion_gate": rule["promotion_gate"],
                "family_level_statement": rule["family_level_statement"],
                "direct_measurement_requirement": rule["direct_measurement_requirement"],
                "theorem_requirement": rule["theorem_requirement"],
                "promotion_pass_condition": rule["promotion_pass_condition"],
                "promotion_fail_condition": rule["promotion_fail_condition"],
                "eligible_without_new_data": False,
                "endpoint_scores_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    requirements = pd.DataFrame(rows).sort_values(["promotion_gate", "source_priority", "galaxy"])
    summary = (
        requirements.groupby(
            [
                "promotion_gate",
                "formula_family",
                "observable_driver_type",
                "source_priority",
            ],
            as_index=False,
        )
        .agg(
            n_galaxies=("galaxy", "count"),
            galaxies=("galaxy", lambda values: ";".join(values)),
            direct_measurement_requirement=("direct_measurement_requirement", "first"),
            theorem_requirement=("theorem_requirement", "first"),
        )
    )
    summary["claim_boundary"] = CLAIM_BOUNDARY
    return requirements, summary


def write_report(requirements: pd.DataFrame, summary: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# S4G75 Conditional Kernel Promotion Requirements",
        "",
        "This report records what must be proven or measured before the eight "
        "conditional S4G75 kernel rows can become strict kernel-ready endpoint "
        "rows. It is a requirement map, not an endpoint.",
        "",
        "## Verdict",
        "",
        f"Conditional rows: {len(requirements)}.",
        f"Promotion gates: {requirements['promotion_gate'].nunique()}.",
        "",
        "No conditional row is endpoint-eligible without either direct "
        "source-native measurement or a residual-blind Tau-side promotion "
        "theorem for its kernel observable.",
        "",
        "## Family-Level Promotion Gates",
        "",
        markdown_table(summary),
        "",
        "## Galaxy-Level Requirements",
        "",
        markdown_table(
            requirements[
                [
                    "galaxy",
                    "formula_family",
                    "source_priority",
                    "promotion_gate",
                    "direct_measurement_requirement",
                    "theorem_requirement",
                    "eligible_without_new_data",
                    "endpoint_scores_allowed",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "These promotion requirements are residual-blind. They cannot be "
        "satisfied by endpoint improvement, best-fit family choice, or residual "
        "shape. The source must constrain the readout kernel itself, or the "
        "Tau-side bridge must prove the proxy admissible before endpoint use.",
        "",
    ]
    (REPORTS / "s4g75_conditional_promotion_requirements.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    requirements, summary = build_requirements()
    requirements.to_csv(DATA / "s4g75_conditional_promotion_requirements.csv", index=False)
    summary.to_csv(DATA / "s4g75_conditional_promotion_requirement_summary.csv", index=False)
    write_report(requirements, summary)
    print(f"wrote {DATA / 's4g75_conditional_promotion_requirements.csv'}")
    print(f"wrote {DATA / 's4g75_conditional_promotion_requirement_summary.csv'}")
    print(f"wrote {REPORTS / 's4g75_conditional_promotion_requirements.md'}")


if __name__ == "__main__":
    main()
