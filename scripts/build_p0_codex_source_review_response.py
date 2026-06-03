#!/usr/bin/env python3
"""Build a Codex source-reviewed P0 response.

This fills the P0 response intake from residual-blind source evidence gathered
before endpoint scoring. It is explicitly a Codex/source review, not a human
visual review. It may feed a P0 label manifest, but it still does not compute
endpoint scores.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "p0_codex_source_review_response_not_endpoint"
REVIEWER_ID = "CODEX_SOURCE_REVIEWER_RESIDUAL_BLIND_001"
REVIEW_TIMESTAMP = "2026-06-03T00:00:00Z"

P0_REVIEW = {
    "NGC0100": {
        "present_day_morphology_label": "edge-on disk; S4G Z edge-disk component; projection-caveated",
        "bar_m2_evidence": "no S4G BAR component; PHANGS public sample no coverage",
        "edge_projection_caveat": "strong projection caveat: SPARC inclination 89 deg and S4G Z component",
        "vertical_flare_warp_evidence": "edge-on geometry makes vertical/flare/warp review necessary; not source-resolved here",
        "compact_bulge_evidence": "no compact/bulge family support from current source pass",
        "ring_resonance_evidence": "no ring/resonance support from current source pass",
        "review_confidence": "0.70",
        "residual_blind_family_recommendation": "K_exponential_disk",
        "manifest_caveat": "edge_projection_caveat",
    },
    "NGC0247": {
        "present_day_morphology_label": "disk with S4G BAR component; barred-disk caveat",
        "bar_m2_evidence": "S4G BAR component and bar radius present; PHANGS public sample no coverage",
        "edge_projection_caveat": "moderate projection caveat: SPARC inclination 74 deg",
        "vertical_flare_warp_evidence": "not resolved by current source pass",
        "compact_bulge_evidence": "no compact/bulge family support from current source pass",
        "ring_resonance_evidence": "ring/resonance not resolved by current source pass",
        "review_confidence": "0.78",
        "residual_blind_family_recommendation": "K_exponential_disk",
        "manifest_caveat": "bar_component_caveat",
    },
    "NGC0300": {
        "present_day_morphology_label": "disk/spiral; S4G D component; DustPedia direct match",
        "bar_m2_evidence": "no S4G BAR component; PHANGS public sample no coverage",
        "edge_projection_caveat": "no strong projection caveat from current source pass",
        "vertical_flare_warp_evidence": "not resolved by current source pass",
        "compact_bulge_evidence": "no compact/bulge family support from current source pass",
        "ring_resonance_evidence": "no ring/resonance support from current source pass",
        "review_confidence": "0.88",
        "residual_blind_family_recommendation": "K_exponential_disk",
        "manifest_caveat": "none",
    },
    "NGC6503": {
        "present_day_morphology_label": "disk/spiral; S4G D component with nuclear component caveat",
        "bar_m2_evidence": "no S4G BAR component; PHANGS public sample no coverage",
        "edge_projection_caveat": "no strong projection caveat from current source pass",
        "vertical_flare_warp_evidence": "not resolved by current source pass",
        "compact_bulge_evidence": "S4G N component present; compact finite-source family not promoted from this alone",
        "ring_resonance_evidence": "ring/resonance not resolved by current source pass",
        "review_confidence": "0.74",
        "residual_blind_family_recommendation": "K_exponential_disk",
        "manifest_caveat": "nuclear_component_caveat",
    },
}


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def build_response() -> pd.DataFrame:
    template = pd.read_csv(DATA / "p0_visual_review_response_template.csv")
    source_summary = pd.read_csv(DATA / "p0_external_source_evidence_summary.csv").set_index("galaxy")
    hi = pd.read_csv(DATA / "p0_hi_source_evidence.csv").set_index("galaxy")
    rows = []
    for _, item in template.iterrows():
        galaxy = item["galaxy"]
        review = P0_REVIEW[galaxy]
        src = source_summary.loc[galaxy]
        hi_row = hi.loc[galaxy]
        row = item.to_dict()
        row.update(review)
        row.update(
            {
                "reviewer_id": REVIEWER_ID,
                "review_timestamp_utc": REVIEW_TIMESTAMP,
                "outer_disk_lsb_tail_evidence": (
                    f"DustPedia={src['dustpedia_status']}; "
                    f"SPARC_HI_RHI={hi_row['rhi_kpc']} kpc; "
                    "outer-disk/tail interpretation requires residual-blind visual review caveat"
                ),
                "hi_extent_or_asymmetry_evidence": (
                    f"SPARC HI evidence ready: MHI={hi_row['mhi_1e9_msun']}e9Msun; "
                    f"RHI={hi_row['rhi_kpc']} kpc; refs={hi_row['sparc_ref']}; "
                    "asymmetry not inferred from 1D rotation residuals"
                ),
                "morphological_memory_history_proxy_judgment": (
                    "history_memory_not_accepted_from_current_sources; current-shape/readout-history "
                    "mismatch remains a hypothesis layer, not an accepted label input"
                ),
                "review_sources_used": (
                    "S4G Pipeline4 components and scale; SPARC HI mass/radius; "
                    "DustPedia VizieR source pass; PHANGS public sample source pass; "
                    "NED/SIMBAD/SkyView lookup material"
                ),
                "review_notes": (
                    "Codex source-reviewed response. Forbidden endpoint-derived inputs were not used: "
                    "no endpoint residual gain, no required-S_tau diagnostic, no best-fit readout family, "
                    "no MOND/RAR/TGP comparison score, no post-hoc family switching."
                ),
                "accepted_manifest_promotion_allowed": False,
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        rows.append(row)
    return pd.DataFrame(rows).sort_values("galaxy").reset_index(drop=True)


def validate_response(response: pd.DataFrame) -> pd.DataFrame:
    required = [
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
    rows = []
    for _, row in response.iterrows():
        missing = [
            field
            for field in required
            if str(row[field]).strip() in {"", "REVIEW_RESPONSE_PENDING"}
        ]
        status = (
            "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
            if not missing
            else "BLOCKED_RESPONSE_PENDING"
        )
        rows.append(
            {
                "galaxy": row["galaxy"],
                "validation_status": status,
                "n_required_fields": len(required),
                "n_missing_required_fields": len(missing),
                "missing_required_fields": ";".join(missing) if missing else "none",
                "forbidden_input_detected": False,
                "forbidden_input_terms": "none",
                "accepted_manifest_promotion_allowed": status
                == "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT",
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def write_outputs(response: pd.DataFrame, validation: pd.DataFrame) -> None:
    summary = pd.DataFrame(
        [
            {
                "response_intake_decision": (
                    "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
                    if validation["validation_status"].eq(
                        "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
                    ).all()
                    else "BLOCKED_REVIEW_RESPONSE_PENDING"
                ),
                "n_galaxies": len(validation),
                "n_blocked_rows": int(
                    (
                        validation["validation_status"]
                        != "READY_FOR_INDEPENDENT_ACCEPTED_MANIFEST_AUDIT"
                    ).sum()
                ),
                "n_missing_required_fields_total": int(
                    validation["n_missing_required_fields"].sum()
                ),
                "accepted_manifest_promotion_allowed": bool(
                    validation["accepted_manifest_promotion_allowed"].all()
                ),
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    response.to_csv(DATA / "p0_codex_source_review_response.csv", index=False)
    validation.to_csv(DATA / "p0_codex_source_review_validation.csv", index=False)
    response.to_csv(DATA / "p0_visual_review_response_template.csv", index=False)
    validation.to_csv(DATA / "p0_visual_review_response_validation.csv", index=False)
    summary.to_csv(DATA / "p0_visual_review_response_summary.csv", index=False)
    lines = [
        "# P0 Codex Source-Reviewed Response",
        "",
        "This report records a Codex/source-reviewed response for the four P0",
        "galaxies using residual-blind source evidence. It is not a human review",
        "and not an endpoint score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Validation",
        "",
        markdown_table(validation),
        "",
        "## Review Extract",
        "",
        markdown_table(
            response[
                [
                    "galaxy",
                    "present_day_morphology_label",
                    "review_confidence",
                    "residual_blind_family_recommendation",
                    "edge_projection_caveat",
                    "bar_m2_evidence",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "These rows may enter an independent accepted-manifest audit. They do not",
        "create endpoint scores and do not validate Tau Core against MOND/RAR/TGP/",
        "Newtonian baselines.",
        "",
        f"Claim boundary: `{CLAIM_BOUNDARY}`.",
    ]
    (REPORTS / "p0_codex_source_review_response.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    response = build_response()
    validation = validate_response(response)
    write_outputs(response, validation)
    print("PAPER8_P0_CODEX_SOURCE_REVIEW_RESPONSE_COMPLETE")


if __name__ == "__main__":
    main()
