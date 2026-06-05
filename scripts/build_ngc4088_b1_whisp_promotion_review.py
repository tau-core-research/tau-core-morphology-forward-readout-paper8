#!/usr/bin/env python3
"""Review whether the NGC4088 WHISP frozen extraction can promote B1 evidence.

This is a source-side promotion review, not an endpoint score.  It closes the B1
warp-onset gate only in a caveated formula-freeze sense: the accepted value is
allowed as a residual-blind formula input, but the provenance caveat must travel
with it until a direct source-coordinate H I product is cached.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_b1_whisp_promotion_review_not_endpoint"


def bool_value(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    original = pd.read_csv(DATA / "ngc4088_b1_original_hi_data_acquisition_summary.csv").iloc[0]
    overview = pd.read_csv(DATA / "ngc4088_b1_whisp_overview_extraction_summary.csv").iloc[0]
    frozen = pd.read_csv(DATA / "ngc4088_b1_whisp_overview_frozen_extraction_summary.csv").iloc[0]
    response = pd.read_csv(DATA / "ngc4088_b1_whisp_overview_frozen_extraction_response.csv").iloc[0]
    components = pd.read_csv(DATA / "ngc4088_b1_whisp_overview_frozen_extraction_components.csv")

    selected = components[components["selected_for_response"].map(bool_value)]
    whisp_cached = bool_value(original["whisp_graphical_overview_cached"])
    direct_product_cached = bool_value(original["direct_source_native_product_cached"])
    agrees = bool_value(frozen["agrees_with_first_pass_within_tolerance"])
    no_endpoint_inputs = (
        not bool_value(frozen["uses_vobs_or_residual"])
        and not bool_value(response["uses_vobs_or_residual"])
    )
    two_sided = len(selected) == 2 and selected["component_side"].nunique() == 2

    source_consistency_promoted = whisp_cached and agrees and two_sided and no_endpoint_inputs
    formula_freeze_accepted = source_consistency_promoted
    endpoint_scores_allowed = False

    decision = (
        "B1_CAVEATED_XW_ACCEPTED_FOR_FORMULA_FREEZE_NOT_ENDPOINT"
        if source_consistency_promoted
        else "B1_PROMOTION_REVIEW_FAILED_OR_INCONCLUSIVE"
    )
    b1_resolution_status = (
        "B1_RESOLVED_CAVEATED_WHISP_GRAPHICAL_XW"
        if source_consistency_promoted
        else "B1_NOT_RESOLVED_WHISP_PROMOTION_REVIEW_FAILED"
    )

    review = pd.DataFrame(
        [
            {
                "review_gate": "WHISP_SOURCE_PRODUCT_AVAILABLE",
                "status": "PASS" if whisp_cached else "FAIL",
                "evidence": str(original.get("whisp_graphical_overview_url", "cached WHISP overview")),
            },
            {
                "review_gate": "DIRECT_SOURCE_NATIVE_PRODUCT",
                "status": "CAVEAT",
                "evidence": (
                    "direct FITS/source-coordinate H I product cached"
                    if direct_product_cached
                    else "no direct source-coordinate H I product cached; WHISP graphical overview is accepted only as caveated B1 input"
                ),
            },
            {
                "review_gate": "FROZEN_EXTRACTION_TWO_SIDED",
                "status": "PASS" if two_sided else "FAIL",
                "evidence": f"selected_components={len(selected)}, side_count={selected['component_side'].nunique() if len(selected) else 0}",
            },
            {
                "review_gate": "FIRST_PASS_AGREEMENT",
                "status": "PASS" if agrees else "FAIL",
                "evidence": (
                    f"x_w_review={float(frozen['x_w_review']):.6g}; "
                    f"first_pass_x_w={float(frozen['first_pass_x_w']):.6g}; "
                    f"tolerance={float(frozen['acceptance_tolerance_x_w']):.6g}"
                ),
            },
            {
                "review_gate": "RESIDUAL_BLINDNESS",
                "status": "PASS" if no_endpoint_inputs else "FAIL",
                "evidence": "frozen extraction and response declare uses_vobs_or_residual=false",
            },
            {
                "review_gate": "FORMULA_FREEZE_ACCEPTANCE",
                "status": "PASS_CAVEATED" if formula_freeze_accepted else "BLOCKED",
                "evidence": (
                    "x_w accepted for formula freeze from residual-blind WHISP graphical overview extraction; "
                    "provenance caveat remains until direct source-coordinate H I product is cached"
                    if formula_freeze_accepted
                    else "formula-freeze acceptance blocked"
                ),
            },
        ]
    )
    review["endpoint_scores_allowed"] = False
    review["uses_vobs_or_residual"] = False
    review["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "promotion_review_status": decision,
                "galaxy": "NGC4088",
                "b1_resolution_status": b1_resolution_status,
                "source_consistency_promoted": source_consistency_promoted,
                "x_w_source_consistency_value": float(frozen["x_w_review"]),
                "first_pass_x_w": float(frozen["first_pass_x_w"]),
                "agreement_delta_x_w": abs(float(frozen["x_w_review"]) - float(frozen["first_pass_x_w"])),
                "agreement_tolerance_x_w": float(frozen["acceptance_tolerance_x_w"]),
                "accepted_x_w_for_formula_freeze": formula_freeze_accepted,
                "formula_freeze_allowed_now": formula_freeze_accepted,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "uses_vobs_or_residual": False,
                "next_required_action": (
                    "carry the WHISP graphical-overview provenance caveat into formula freeze; "
                    "endpoint remains blocked until B2 and B3 close"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    review.to_csv(DATA / "ngc4088_b1_whisp_promotion_review_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4088_b1_whisp_promotion_review_summary.csv", index=False)

    report = [
        "# NGC4088 B1 WHISP Promotion Review",
        "",
        "This review evaluates whether the frozen WHISP overview extraction can promote",
        "the B1 warp-onset evidence. It is residual-blind and does not read endpoint",
        "rotation residuals. The result closes B1 only as a caveated formula-freeze",
        "input, not as an endpoint score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(review),
        "",
        "## Interpretation",
        "",
        "The cached WHISP overview and frozen extraction provide a reproducible,",
        "source-side agreement check for the first-pass warp-onset value. The review",
        "therefore accepts the WHISP-derived x_w as a caveated B1 formula-freeze",
        "input. The caveat is explicit: the source is a graphical overview rather",
        "than a direct source-coordinate H I product. This closes B1 but does not",
        "allow endpoint scoring; the NGC4088 endpoint remains blocked by B2/B3.",
        "",
    ]
    (REPORTS / "ngc4088_b1_whisp_promotion_review.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
