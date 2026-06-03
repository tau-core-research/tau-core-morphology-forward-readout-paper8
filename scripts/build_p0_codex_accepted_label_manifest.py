#!/usr/bin/env python3
"""Build a P0 Codex-source-reviewed label manifest.

This manifest is deliberately narrow. It records the four P0 labels that passed
the Codex/source review response and promotion gate, but it does not promote the
full 175-galaxy endpoint manifest and does not compute endpoint scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_codex_accepted_labels_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def build_manifest() -> tuple[pd.DataFrame, pd.DataFrame]:
    response = pd.read_csv(DATA / "p0_codex_source_review_response.csv")
    validation = pd.read_csv(DATA / "p0_codex_source_review_validation.csv")
    promotion = pd.read_csv(DATA / "p0_response_to_manifest_promotion_summary.csv").iloc[0]
    validation = validation.set_index("galaxy")

    rows = []
    for _, row in response.iterrows():
        galaxy = row["galaxy"]
        validation_status = validation.loc[galaxy, "validation_status"]
        pass_review = (
            validation_status == "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
            and promotion["promotion_gate_decision"]
            == "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
        )
        rows.append(
            {
                "galaxy": galaxy,
                "accepted_label_status": (
                    "P0_CODEX_SOURCE_REVIEW_ACCEPTED_FOR_AUDIT"
                    if pass_review
                    else "BLOCKED_P0_CODEX_SOURCE_REVIEW"
                ),
                "accepted_formula_family": row["residual_blind_family_recommendation"]
                if pass_review
                else "BLOCKED",
                "present_day_morphology_label": row["present_day_morphology_label"],
                "review_confidence": row["review_confidence"],
                "manifest_caveat": row.get("manifest_caveat", "none"),
                "reviewer_id": row["reviewer_id"],
                "review_sources_used": row["review_sources_used"],
                "source_basis": (
                    "S4G/SPARC/DustPedia/PHANGS/NED/SIMBAD/SkyView source-side "
                    "review; no endpoint residuals used"
                ),
                "full_endpoint_manifest_row_created": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    manifest = pd.DataFrame(rows).sort_values("galaxy").reset_index(drop=True)
    summary = pd.DataFrame(
        [
            {
                "p0_label_manifest_decision": (
                    "P0_CODEX_SOURCE_REVIEW_LABELS_CREATED_NOT_ENDPOINT"
                    if manifest["accepted_label_status"]
                    .eq("P0_CODEX_SOURCE_REVIEW_ACCEPTED_FOR_AUDIT")
                    .all()
                    else "BLOCKED_P0_CODEX_SOURCE_REVIEW_LABELS"
                ),
                "n_galaxies": len(manifest),
                "n_p0_codex_source_review_accepted": int(
                    manifest["accepted_label_status"]
                    .eq("P0_CODEX_SOURCE_REVIEW_ACCEPTED_FOR_AUDIT")
                    .sum()
                ),
                "n_blocked": int(
                    (
                        manifest["accepted_label_status"]
                        != "P0_CODEX_SOURCE_REVIEW_ACCEPTED_FOR_AUDIT"
                    ).sum()
                ),
                "full_endpoint_manifest_rows_created": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return manifest, summary


def write_outputs(manifest: pd.DataFrame, summary: pd.DataFrame) -> None:
    manifest.to_csv(DATA / "p0_codex_accepted_label_manifest.csv", index=False)
    summary.to_csv(DATA / "p0_codex_accepted_label_manifest_summary.csv", index=False)
    lines = [
        "# P0 Codex Source-Reviewed Label Manifest",
        "",
        "This manifest records the four P0 labels that passed the Codex/source",
        "review response and response-to-manifest gate. It is a P0 audit manifest",
        "only. It does not create full endpoint-manifest rows and does not compute",
        "endpoint scores.",
        "",
        "P0 audit manifest only.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Manifest",
        "",
        markdown_table(
            manifest[
                [
                    "galaxy",
                    "accepted_label_status",
                    "accepted_formula_family",
                    "review_confidence",
                    "manifest_caveat",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "These labels are residual-blind source-review labels for the P0 audit lane.",
        "They are not empirical validation, not a MOND/RAR/TGP/Newtonian comparison,",
        "and not a launch of the frozen 175-galaxy endpoint.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_codex_accepted_label_manifest.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    manifest, summary = build_manifest()
    write_outputs(manifest, summary)
    print("PAPER8_P0_CODEX_ACCEPTED_LABEL_MANIFEST_COMPLETE")


if __name__ == "__main__":
    main()
