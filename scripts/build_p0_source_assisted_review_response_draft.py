#!/usr/bin/env python3
"""Build a source-assisted P0 review response draft.

The draft fills review-response fields with residual-blind source evidence
where available and explicit review-required blockers where evidence remains
insufficient. It is not an accepted morphology manifest and is not consumed by
the promotion gate as an accepted label source.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_source_assisted_response_draft_not_label_not_endpoint"
REVIEWER_ID = "SOURCE_ASSISTED_AUTOMATION_NOT_HUMAN_REVIEW"
REVIEW_TIMESTAMP = "2026-06-03T00:00:00Z"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def yes_no(condition: bool, yes: str, no: str) -> str:
    return yes if condition else no


def build_draft() -> pd.DataFrame:
    template = pd.read_csv(DATA / "p0_visual_review_response_template.csv")
    queue = pd.read_csv(DATA / "morphology_inspection_queue.csv").set_index("galaxy")
    source_summary = pd.read_csv(DATA / "p0_external_source_evidence_summary.csv").set_index("galaxy")
    hi = pd.read_csv(DATA / "p0_hi_source_evidence.csv").set_index("galaxy")
    phangs = pd.read_csv(DATA / "p0_phangs_source_matches.csv").set_index("galaxy")
    rows = []
    for _, item in template.iterrows():
        galaxy = item["galaxy"]
        q = queue.loc[galaxy]
        src = source_summary.loc[galaxy]
        hi_row = hi.loc[galaxy]
        phangs_row = phangs.loc[galaxy]
        s4g_components = str(q.get("s4g_model_components", ""))
        is_barred = "BAR" in s4g_components.split(";")
        is_edge = "Z" in s4g_components.split(";") or "edge_on_projection" in str(q["inspection_focus"])
        has_dustpedia = src["dustpedia_status"] == "MATCHED_SOURCE_EVIDENCE"
        has_hi = hi_row["match_status"] == "HI_SOURCE_EVIDENCE_READY"
        phangs_covered = phangs_row["match_status"] == "MATCHED_SOURCE_EVIDENCE"
        row = item.to_dict()
        row.update(
            {
                "reviewer_id": REVIEWER_ID,
                "review_timestamp_utc": REVIEW_TIMESTAMP,
                "present_day_morphology_label": (
                    "SOURCE_DRAFT_S4G_DISK_COMPONENT_SUPPORT_REVIEW_REQUIRED"
                ),
                "outer_disk_lsb_tail_evidence": (
                    "SOURCE_DRAFT_OUTER_DISK_REVIEW_REQUIRED; "
                    + yes_no(
                        has_dustpedia,
                        "DustPedia direct match present",
                        "no direct DustPedia match",
                    )
                    + "; "
                    + yes_no(
                        has_hi,
                        f"SPARC HI radius {hi_row['rhi_kpc']} kpc available",
                        "HI radius missing",
                    )
                ),
                "hi_extent_or_asymmetry_evidence": (
                    f"SOURCE_DRAFT_HI_MASS_RADIUS_READY_NOT_ASYMMETRY_CLASSIFICATION; "
                    f"MHI={hi_row['mhi_1e9_msun']}e9Msun; RHI={hi_row['rhi_kpc']}kpc; "
                    f"refs={hi_row['sparc_ref']}; {hi_row['dustpedia_hi_status']}"
                ),
                "bar_m2_evidence": (
                    "SOURCE_DRAFT_S4G_BAR_COMPONENT_PRESENT; PHANGS_NO_SAMPLE_COVERAGE"
                    if is_barred
                    else "SOURCE_DRAFT_NO_S4G_BAR_COMPONENT; PHANGS_NO_SAMPLE_COVERAGE"
                    if not phangs_covered
                    else "SOURCE_DRAFT_PHANGS_AVAILABLE_REVIEW_REQUIRED"
                ),
                "edge_projection_caveat": (
                    "SOURCE_DRAFT_PROJECTION_CAVEAT_REQUIRED"
                    if is_edge or str(q["manifest_caveat"]) != "none"
                    else "SOURCE_DRAFT_NO_STRONG_PROJECTION_CAVEAT_FROM_CURRENT_SOURCE_PASS"
                ),
                "vertical_flare_warp_evidence": (
                    "SOURCE_DRAFT_VERTICAL_OR_WARP_REVIEW_REQUIRED_FROM_HI_AND_EDGE_CONTEXT"
                    if is_edge
                    else "SOURCE_DRAFT_VERTICAL_FLARE_WARP_NOT_RESOLVED_BY_SOURCE_PASS"
                ),
                "compact_bulge_evidence": (
                    "SOURCE_DRAFT_COMPACT_BULGE_NOT_RESOLVED_BY_SOURCE_PASS"
                ),
                "ring_resonance_evidence": (
                    "SOURCE_DRAFT_RING_RESONANCE_NOT_RESOLVED_BY_SOURCE_PASS"
                ),
                "morphological_memory_history_proxy_judgment": (
                    "SOURCE_DRAFT_MEMORY_HISTORY_REVIEW_REQUIRED; "
                    f"{q['memory_history_proxy_class']}; "
                    "current-shape/readout-history mismatch remains hypothesis-layer only"
                ),
                "review_confidence": "SOURCE_DRAFT_NOT_HUMAN_REVIEW_CONFIDENCE_NOT_ASSIGNED",
                "residual_blind_family_recommendation": (
                    "REVIEWER_REQUIRED_NOT_ACCEPTED_LABEL"
                ),
                "review_sources_used": (
                    "S4G Pipeline4; SPARC HI mass/radius; DustPedia VizieR; "
                    "PHANGS public sample; SkyView/NED/SIMBAD review links"
                ),
                "review_notes": (
                    "Source-assisted draft only. Do not promote as accepted label. "
                    f"DustPedia={src['dustpedia_status']}; "
                    f"PHANGS={src['phangs_status']}; HI={src['hi_status']}."
                ),
                "draft_status": "SOURCE_ASSISTED_DRAFT_REVIEW_REQUIRED",
                "accepted_manifest_promotion_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        rows.append(row)
    return pd.DataFrame(rows).sort_values("galaxy").reset_index(drop=True)


def build_validation(draft: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in draft.iterrows():
        blockers = [
            "human_residual_blind_reviewer_missing",
            "accepted_family_label_not_created",
            "independent_manifest_audit_not_run",
        ]
        if "PHANGS_NO_SAMPLE_COVERAGE" in row["bar_m2_evidence"] and row["galaxy"] == "NGC0247":
            blockers.append("ngc0247_phangs_velocity_field_not_available")
        if "no direct DustPedia match" in row["outer_disk_lsb_tail_evidence"]:
            blockers.append("dustpedia_direct_match_missing")
        rows.append(
            {
                "galaxy": row["galaxy"],
                "draft_validation_status": "BLOCKED_DRAFT_NOT_ACCEPTED_REVIEW",
                "n_blockers": len(blockers),
                "blockers": ";".join(blockers),
                "accepted_manifest_promotion_allowed": False,
                "accepted_labels_created": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def write_report(draft: pd.DataFrame, validation: pd.DataFrame) -> None:
    lines = [
        "# P0 Source-Assisted Review Response Draft",
        "",
        "This report fills a source-assisted draft response using residual-blind",
        "external source evidence. It is not a human visual review response, not an accepted morphology manifest, and not an endpoint score.",
        "",
        "## Verdict",
        "",
        "A draft response now exists for all four P0 galaxies, but every row remains",
        "blocked from accepted-label promotion because a human residual-blind review",
        "and independent accepted-manifest audit are still missing.",
        "",
        "## Draft Validation",
        "",
        markdown_table(validation),
        "",
        "## Draft Response Extract",
        "",
        markdown_table(
            draft[
                [
                    "galaxy",
                    "present_day_morphology_label",
                    "hi_extent_or_asymmetry_evidence",
                    "bar_m2_evidence",
                    "residual_blind_family_recommendation",
                    "draft_status",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This draft may help a reviewer complete the P0 response. It cannot create",
        "accepted labels, cannot open the endpoint launch guard, and cannot be used",
        "as Tau Core validation evidence.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_source_assisted_review_response_draft.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    draft = build_draft()
    validation = build_validation(draft)
    draft.to_csv(DATA / "p0_source_assisted_review_response_draft.csv", index=False)
    validation.to_csv(
        DATA / "p0_source_assisted_review_response_validation.csv", index=False
    )
    write_report(draft, validation)
    print("PAPER8_P0_SOURCE_ASSISTED_REVIEW_RESPONSE_DRAFT_COMPLETE")


if __name__ == "__main__":
    main()
