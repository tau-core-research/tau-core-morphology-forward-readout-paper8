#!/usr/bin/env python3
"""Write theorem skeletons for the S4G75 conditional promotion gates.

The skeletons are deliberately conditional.  They separate what follows from
definitions from what still requires direct source-native evidence or a
Tau-side promotion theorem.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "s4g75_promotion_theorem_skeletons_not_endpoint"


THEOREMS = [
    {
        "promotion_gate": "TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION",
        "formula_family": "K_scale_tail_spiral",
        "theorem_id": "TAIL-HI-EXTENT-PROMOTION-LEMMA-001",
        "formal_claim": (
            "Let R_HI be a residual-blind source-native gas-extent observable. "
            "Let F_tail use kernel parameters R_tail_in and R_tail_cut. If a "
            "fixed residual-blind transition rule maps R_HI and disk-scale "
            "source data to R_tail_in and R_tail_cut, and if R_tail_cut "
            "constrains the same outer-disk/tail support class used by F_tail, "
            "then the HI extent proxy is admissible as a conditional scale-tail "
            "kernel observable."
        ),
        "minimal_corrected_statement": (
            "R_HI can be promoted to a scale-tail cutoff only under a "
            "predeclared transition/support rule; generic HI extent alone is "
            "partial support, not strict kernel readiness."
        ),
        "proof_status": "CONDITIONAL_INCOMPLETE",
        "verdict": "Plausible but not proven for endpoint use",
        "weakest_step": (
            "Showing that R_HI constrains the same outer-disk transition kernel "
            "rather than merely bounding generic gas extent."
        ),
        "hidden_assumptions": (
            "monotone outer support; no endpoint-selected transition constant; "
            "R_HI is measured consistently across galaxies; gas extent is a "
            "valid readout support proxy for the stellar/morphological tail"
        ),
        "edge_cases": (
            "gas disk extends beyond stellar tail; disturbed HI without a "
            "stellar tail; compact HI cutoff but broad stellar tail; low "
            "inclination or distance uncertainty"
        ),
        "proof_sketch": (
            "By definition, strict kernel readiness requires source evidence "
            "for the actual kernel observable. If a predeclared rule fixes "
            "R_tail_cut from R_HI and proves support compatibility with the "
            "tail kernel, then the source constrains F_tail's cutoff parameter. "
            "Without support compatibility, R_HI remains only a proxy."
        ),
    },
    {
        "promotion_gate": "COMPACT-COMPONENT-SUPPORT-PROMOTION",
        "formula_family": "K_compact_finite",
        "theorem_id": "COMPACT-SUPPORT-PROMOTION-LEMMA-001",
        "formal_claim": (
            "Let R_c be a residual-blind compact component support observable "
            "from a source-native decomposition. Let F_compact use a finite "
            "compact support kernel. If R_c bounds or represents the compact "
            "component support used by the kernel, with the bound selected "
            "before endpoint scoring, then R_c is admissible as a strict "
            "compact finite-source kernel observable."
        ),
        "minimal_corrected_statement": (
            "A compact component radius can promote the compact kernel if it "
            "constrains compact support; Reff alone is conditional unless a "
            "support theorem maps it to the compact component."
        ),
        "proof_status": "CONDITIONAL_INCOMPLETE",
        "verdict": "Definition-level proof after support evidence; incomplete for Reff-only rows",
        "weakest_step": (
            "Proving that Reff or a listed component is the compact support "
            "used by F_compact, rather than a global half-light proxy."
        ),
        "hidden_assumptions": (
            "decomposition separates compact and disk components; component "
            "radius has stable physical meaning; compact support radius is not "
            "chosen from rotation residuals"
        ),
        "edge_cases": (
            "bar radius confused with compact support; diffuse bulge; no "
            "component radius; Reff dominated by disk light; multi-component "
            "central structure"
        ),
        "proof_sketch": (
            "The compact kernel is finite-source by construction. If a "
            "residual-blind source provides the support radius or a proven "
            "bound for that finite source, then the same source constrains the "
            "kernel parameter. If only Reff exists, the conclusion requires an "
            "additional theorem connecting Reff to compact support."
        ),
    },
    {
        "promotion_gate": "EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION",
        "formula_family": "K_thick_flared",
        "theorem_id": "EDGE-DISK-VERTICAL-PROMOTION-LEMMA-001",
        "formal_claim": (
            "Let E_Z be a residual-blind edge-disk or vertical-structure source "
            "observable. Let F_thick use a vertical kernel parameter h/Rs, "
            "flare radius, warp radius, or gas-plane thickness. If E_Z "
            "provides a measured value or fixed conservative bound for that "
            "vertical kernel parameter, independent of endpoint residuals, then "
            "E_Z is admissible as a conditional thick/flared kernel observable."
        ),
        "minimal_corrected_statement": (
            "Edge-disk evidence can promote thick/flared only when it "
            "constrains the vertical kernel parameter; an edge-on label or "
            "inclination proxy alone is not strict kernel readiness."
        ),
        "proof_status": "CONDITIONAL_INCOMPLETE",
        "verdict": "Plausible for direct h/Rs or flare measurements; incomplete for component-label-only evidence",
        "weakest_step": (
            "Showing that edge-disk/component evidence yields a measured or "
            "bounded vertical kernel parameter rather than only a projection "
            "caveat."
        ),
        "hidden_assumptions": (
            "vertical component is physically tied to the solved readout kernel; "
            "h/Rs or flare bounds are residual-blind; projection effects are "
            "not mistaken for thickness"
        ),
        "edge_cases": (
            "edge-on projection without thick disk; warp misread as flare; "
            "gas-plane thickness differs from stellar thickness; uncertain "
            "inclination; multiple vertical components"
        ),
        "proof_sketch": (
            "The thick/flared formula uses a vertical geometry parameter. If "
            "source evidence fixes or bounds that same parameter, the source "
            "constrains the kernel. If the source only says edge-disk or high "
            "inclination, the evidence marks a review caveat but does not yet "
            "supply the kernel observable."
        ),
    },
]


ASSUMPTIONS = [
    {
        "promotion_gate": "TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION",
        "assumption_id": "T1",
        "assumption": "R_HI is measured residual-blind and not selected from endpoint residuals.",
        "status": "DATA_DEPENDENT",
    },
    {
        "promotion_gate": "TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION",
        "assumption_id": "T2",
        "assumption": "A fixed transition rule maps R_HI and disk scale to R_tail_in and R_tail_cut.",
        "status": "THEOREM_OR_PROTOCOL_REQUIRED",
    },
    {
        "promotion_gate": "TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION",
        "assumption_id": "T3",
        "assumption": "The mapped cutoff constrains the same outer-disk/tail support class used by F_tail.",
        "status": "WEAKEST_STEP",
    },
    {
        "promotion_gate": "COMPACT-COMPONENT-SUPPORT-PROMOTION",
        "assumption_id": "C1",
        "assumption": "A source-native component decomposition identifies a compact component.",
        "status": "DATA_DEPENDENT",
    },
    {
        "promotion_gate": "COMPACT-COMPONENT-SUPPORT-PROMOTION",
        "assumption_id": "C2",
        "assumption": "A compact support radius or bound is available before endpoint scoring.",
        "status": "DATA_OR_THEOREM_REQUIRED",
    },
    {
        "promotion_gate": "COMPACT-COMPONENT-SUPPORT-PROMOTION",
        "assumption_id": "C3",
        "assumption": "Reff is not used as compact support unless a support theorem justifies the map.",
        "status": "CLAIM_BOUNDARY_RULE",
    },
    {
        "promotion_gate": "EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION",
        "assumption_id": "V1",
        "assumption": "The source identifies vertical structure rather than only projection or inclination.",
        "status": "DATA_DEPENDENT",
    },
    {
        "promotion_gate": "EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION",
        "assumption_id": "V2",
        "assumption": "A measured or bounded h/Rs, flare, warp, or gas-plane thickness parameter is supplied.",
        "status": "DATA_OR_THEOREM_REQUIRED",
    },
    {
        "promotion_gate": "EDGE-DISK-TO-VERTICAL-KERNEL-PROMOTION",
        "assumption_id": "V3",
        "assumption": "Projection effects are not promoted to vertical kernel parameters without a theorem.",
        "status": "CLAIM_BOUNDARY_RULE",
    },
]


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def build_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    theorems = pd.DataFrame(THEOREMS)
    assumptions = pd.DataFrame(ASSUMPTIONS)
    requirements = pd.read_csv(DATA / "s4g75_conditional_promotion_requirements.csv")
    mapping = (
        requirements.groupby(["promotion_gate", "formula_family"], as_index=False)
        .agg(
            n_waiting_galaxies=("galaxy", "count"),
            waiting_galaxies=("galaxy", lambda values: ";".join(values)),
            source_priorities=("source_priority", lambda values: ";".join(sorted(set(values)))),
        )
        .merge(theorems[["promotion_gate", "theorem_id", "proof_status", "weakest_step"]])
    )
    for table in [theorems, assumptions, mapping]:
        table["claim_boundary"] = CLAIM_BOUNDARY
    return theorems, assumptions, mapping


def write_report(
    theorems: pd.DataFrame,
    assumptions: pd.DataFrame,
    mapping: pd.DataFrame,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# S4G75 Promotion Theorem Skeletons",
        "",
        "These are conditional theorem skeletons for the three S4G75 promotion "
        "gates. They are not endpoint results and not full physical proofs. "
        "They state the minimal corrected claims needed before conditional "
        "kernel rows can become strict kernel-ready rows.",
        "",
        "## Verdict",
        "",
        "All three promotion claims are conditional. The conclusion follows only "
        "after the missing source-support assumption or Tau-side promotion "
        "theorem is supplied. Endpoint improvement cannot supply that missing "
        "assumption.",
        "",
        "## Theorem Skeletons",
        "",
        markdown_table(
            theorems[
                [
                    "theorem_id",
                    "promotion_gate",
                    "formula_family",
                    "minimal_corrected_statement",
                    "proof_status",
                    "verdict",
                    "weakest_step",
                ]
            ]
        ),
        "",
        "## Formal Claims",
        "",
    ]
    for _, row in theorems.iterrows():
        lines.extend(
            [
                f"### {row['theorem_id']}",
                "",
                "**Formal claim**",
                "",
                row["formal_claim"],
                "",
                "**Proof sketch**",
                "",
                row["proof_sketch"],
                "",
                "**Hidden assumptions**",
                "",
                row["hidden_assumptions"],
                "",
                "**Edge cases**",
                "",
                row["edge_cases"],
                "",
            ]
        )
    lines.extend(
        [
            "## Assumption Audit",
            "",
            markdown_table(assumptions),
            "",
            "## Waiting Conditional Rows",
            "",
            markdown_table(mapping),
            "",
            "## Claim Boundary",
            "",
            "These theorem skeletons do not prove that the S4G75 conditional rows "
            "are endpoint-eligible. They define what must be proven or measured "
            "before promotion. The corrected claim is: source-rich proxy rows "
            "become strict kernel-ready rows only when the source constrains the "
            "same kernel observable used by the formula family, or when a "
            "residual-blind Tau-side theorem proves that the proxy is an "
            "admissible representative of that kernel.",
            "",
        ]
    )
    (REPORTS / "s4g75_promotion_theorem_skeletons.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    theorems, assumptions, mapping = build_tables()
    theorems.to_csv(DATA / "s4g75_promotion_theorem_skeletons.csv", index=False)
    assumptions.to_csv(DATA / "s4g75_promotion_theorem_assumptions.csv", index=False)
    mapping.to_csv(DATA / "s4g75_promotion_theorem_waiting_rows.csv", index=False)
    write_report(theorems, assumptions, mapping)
    print(f"wrote {DATA / 's4g75_promotion_theorem_skeletons.csv'}")
    print(f"wrote {DATA / 's4g75_promotion_theorem_assumptions.csv'}")
    print(f"wrote {DATA / 's4g75_promotion_theorem_waiting_rows.csv'}")
    print(f"wrote {REPORTS / 's4g75_promotion_theorem_skeletons.md'}")


if __name__ == "__main__":
    main()
