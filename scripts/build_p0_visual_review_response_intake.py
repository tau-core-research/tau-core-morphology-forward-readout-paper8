#!/usr/bin/env python3
"""Build and validate the P0 visual-review response intake template.

This is the reviewer-response contract between the handoff package and any
future accepted morphology manifest.  It remains residual-blind: it does not
classify images, promote accepted labels, or compute endpoint scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

PENDING = "REVIEW_RESPONSE_PENDING"
CLAIM_BOUNDARY = "p0_visual_review_response_intake_not_label_not_endpoint"

REQUIRED_FIELDS = [
    "reviewer_id",
    "review_timestamp_utc",
    "present_day_morphology_label",
    "outer_disk_lsb_tail_evidence",
    "hi_extent_or_asymmetry_evidence",
    "bar_m2_evidence",
    "edge_projection_caveat",
    "vertical_flare_warp_evidence",
    "compact_bulge_evidence",
    "ring_resonance_evidence",
    "morphological_memory_history_proxy_judgment",
    "review_confidence",
    "residual_blind_family_recommendation",
    "review_sources_used",
]

OPTIONAL_FIELDS = ["review_notes"]

FORBIDDEN_INPUTS = [
    "endpoint residual gain",
    "required-S_tau diagnostic as a label input",
    "best-fit Tau Core readout family",
    "MOND/RAR/TGP comparison score",
    "post-hoc family switching after endpoint scoring",
]


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def build_response_template(handoff: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in handoff.iterrows():
        output = {
            "galaxy": row["galaxy"],
            "review_status_from_handoff": row["review_status"],
            "allowed_sources": row["allowed_sources"],
            "forbidden_inputs": row["forbidden_inputs"],
            "accepted_manifest_promotion_allowed": False,
            "endpoint_scores_computed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for field in REQUIRED_FIELDS + OPTIONAL_FIELDS:
            output[field] = PENDING
        rows.append(output)
    return pd.DataFrame(rows).sort_values("galaxy").reset_index(drop=True)


def build_schema() -> pd.DataFrame:
    rows = []
    for field in REQUIRED_FIELDS:
        rows.append(
            {
                "field": field,
                "required_for_visual_review_completion": True,
                "initial_value": PENDING,
                "may_use_endpoint_scores": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for field in OPTIONAL_FIELDS:
        rows.append(
            {
                "field": field,
                "required_for_visual_review_completion": False,
                "initial_value": PENDING,
                "may_use_endpoint_scores": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def validate_response(row: pd.Series) -> dict[str, object]:
    missing = [field for field in REQUIRED_FIELDS if str(row[field]).strip() == PENDING]
    forbidden_present = [
        item for item in FORBIDDEN_INPUTS if item.lower() in str(row.get("review_notes", "")).lower()
    ]
    if forbidden_present:
        status = "BLOCKED_FORBIDDEN_INPUT_PRESENT"
    elif missing:
        status = "BLOCKED_RESPONSE_PENDING"
    else:
        status = "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
    return {
        "galaxy": row["galaxy"],
        "validation_status": status,
        "n_required_fields": len(REQUIRED_FIELDS),
        "n_missing_required_fields": len(missing),
        "missing_required_fields": ";".join(missing) if missing else "none",
        "forbidden_input_detected": bool(forbidden_present),
        "forbidden_input_terms": ";".join(forbidden_present) if forbidden_present else "none",
        "accepted_manifest_promotion_allowed": status
        == "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT",
        "endpoint_scores_computed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_report(validation: pd.DataFrame, summary: pd.DataFrame) -> None:
    compact = validation[
        [
            "galaxy",
            "validation_status",
            "n_missing_required_fields",
            "accepted_manifest_promotion_allowed",
            "endpoint_scores_computed",
            "claim_boundary",
        ]
    ]
    lines = [
        "# P0 Visual Review Response Intake",
        "",
        "This report defines and validates the residual-blind reviewer-response",
        "intake template for the four P0 galaxies. It is the contract for filling",
        "human review evidence after the handoff package. It is not an accepted",
        "morphology manifest, not an image classification, and not an endpoint",
        "score.",
        "",
        "This is a reviewer-response contract, not an accepted morphology manifest and not an endpoint score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Validation",
        "",
        markdown_table(compact),
        "",
        "## Forbidden Inputs",
        "",
        "\n".join(f"- {item}" for item in FORBIDDEN_INPUTS),
        "",
        "## Claim Boundary",
        "",
        "A completed response intake would only authorize an independent",
        "accepted-manifest audit. It would not itself promote labels, compute",
        "endpoint scores, or compare Tau Core against MOND/RAR/TGP/Newtonian",
        "baselines.",
        "",
        "A completed response intake only opens an independent accepted-manifest audit.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_visual_review_response_intake.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    handoff = pd.read_csv(DATA / "p0_visual_review_handoff_tasks.csv")
    response = build_response_template(handoff)
    schema = build_schema()
    validation = pd.DataFrame([validate_response(row) for _, row in response.iterrows()])
    blocked = validation[
        validation["validation_status"].isin(
            {"BLOCKED_RESPONSE_PENDING", "BLOCKED_FORBIDDEN_INPUT_PRESENT"}
        )
    ]
    decision = (
        "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
        if blocked.empty
        else "BLOCKED_REVIEW_RESPONSE_PENDING"
    )
    summary = pd.DataFrame(
        [
            {
                "response_intake_decision": decision,
                "n_galaxies": len(validation),
                "n_blocked_rows": len(blocked),
                "n_missing_required_fields_total": int(
                    validation["n_missing_required_fields"].sum()
                ),
                "accepted_manifest_promotion_allowed": blocked.empty,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    response.to_csv(DATA / "p0_visual_review_response_template.csv", index=False)
    schema.to_csv(DATA / "p0_visual_review_response_schema.csv", index=False)
    validation.to_csv(DATA / "p0_visual_review_response_validation.csv", index=False)
    summary.to_csv(DATA / "p0_visual_review_response_summary.csv", index=False)
    write_report(validation, summary)
    print("PAPER8_P0_VISUAL_REVIEW_RESPONSE_INTAKE_COMPLETE")


if __name__ == "__main__":
    main()
