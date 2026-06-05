#!/usr/bin/env python3
"""Audit residual-blind source readiness for an NGC4183 mixed-overlay endpoint.

This is a source-acquisition/preflight artifact only.  It records which
NGC4183 observables are already source-native, which are only contextual, and
which still need an independent review before any formula freeze or endpoint
score is allowed.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
LITERATURE = ROOT / "data" / "external" / "literature"
CLAIM_BOUNDARY = "ngc4183_mixed_overlay_source_audit_not_endpoint"
GALAXY = "NGC4183"


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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_excerpt(text: str, needle: str, before: int = 4, after: int = 8) -> str:
    lines = text.splitlines()
    hits = [idx for idx, line in enumerate(lines) if needle.lower() in line.lower()]
    if not hits:
        return ""
    idx = hits[-1]
    lo = max(0, idx - before)
    hi = min(len(lines), idx + after + 1)
    return " / ".join(line.strip() for line in lines[lo:hi] if line.strip())


def ngc4183_block(text: str) -> str:
    match = re.search(
        r"Observing parameters for NGC 4183(?P<block>.*?)(?:Observing parameters for NGC 4217|N4183)",
        text,
        flags=re.DOTALL,
    )
    if not match:
        return source_excerpt(text, "N4183", before=30, after=80)
    block = match.group("block")
    return " / ".join(line.strip() for line in block.splitlines() if line.strip())


def compact_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().replace("/", " "))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    sparc_row = sparc.loc[sparc["Galaxy"].eq(GALAXY)].iloc[0]

    manifest = pd.read_csv(DATA / "readout_subfamily_accepted_manifest_audit.csv")
    manifest_row = manifest.loc[manifest["galaxy"].eq(GALAXY)].iloc[0]

    worklist = pd.read_csv(DATA / "mixed_overlay_future_protocol_worklist.csv")
    worklist_row = worklist.loc[worklist["galaxy"].eq(GALAXY)].iloc[0]

    whisp_context_path = LITERATURE / "ngc4183_whisp_lopsidedness_context_2011.txt"
    ursa_major_path = LITERATURE / "2001_verheijen_sancisi_ursa_major_hi.txt"
    whisp_context = read_text(whisp_context_path)
    ursa_major = read_text(ursa_major_path)
    ursa_block = ngc4183_block(ursa_major)

    has_ngc4183_ursa = "NGC 4183" in ursa_major or "N4183" in ursa_major
    has_ngc4183_whisp = "NGC4183" in whisp_context or "NGC 4183" in whisp_context
    compact_ursa_block = compact_text(ursa_block)
    warp_statement_present = (
        "slightly warped" in compact_ursa_block
        and "outer regions" in compact_ursa_block
    )
    high_inclination_statement_present = (
        "inclination" in compact_ursa_block
        and "too high" in compact_ursa_block
    )

    sources = pd.DataFrame(
        [
            {
                "source_id": "SPARC_MASTER",
                "source_path": str(DATA / "external_sparc_master_table.csv"),
                "source_role": "rotation_curve_and_global_baryonic_metadata",
                "ngc4183_specific": True,
                "source_status": "SOURCE_NATIVE_ACCEPTED",
                "usable_for_freeze": True,
                "evidence_summary": (
                    f"T={sparc_row['T']}; Inc={sparc_row['Inc_deg']}; "
                    f"Rdisk={sparc_row['Rdisk_kpc']}; RHI={sparc_row['RHI_kpc']}; "
                    f"Vflat={sparc_row['Vflat_kms']}; Q={sparc_row['Q']}"
                ),
            },
            {
                "source_id": "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "source_path": str(ursa_major_path),
                "source_role": "source_native_hi_orientation_projection_and_warp_context",
                "ngc4183_specific": has_ngc4183_ursa,
                "source_status": "GALAXY_SPECIFIC_SOURCE_PRESENT_REVIEW_REQUIRED",
                "usable_for_freeze": False,
                "evidence_summary": source_excerpt(ursa_major, "Observing parameters for NGC 4183", before=0, after=70),
            },
            {
                "source_id": "VANEYMEREN_2011_WHISP_LOPSIDEDNESS_CONTEXT",
                "source_path": str(whisp_context_path),
                "source_role": "method_and_population_context_only",
                "ngc4183_specific": has_ngc4183_whisp,
                "source_status": "CONTEXT_ONLY_NOT_FREEZE_INPUT",
                "usable_for_freeze": False,
                "evidence_summary": "WHISP lopsidedness context is cached, but current manifest treats it as context-only.",
            },
        ]
    )

    fields = pd.DataFrame(
        [
            {
                "field_id": "disk_scale_Rdisk_kpc",
                "value": float(sparc_row["Rdisk_kpc"]),
                "unit": "kpc",
                "source_id": "SPARC_MASTER",
                "field_status": "ACCEPTED_NUMERIC_RESIDUAL_BLIND",
                "freeze_usable": True,
                "notes": "SPARC disk scale field; does not use vobs residuals.",
            },
            {
                "field_id": "RHI_kpc",
                "value": float(sparc_row["RHI_kpc"]),
                "unit": "kpc",
                "source_id": "SPARC_MASTER",
                "field_status": "ACCEPTED_NUMERIC_RESIDUAL_BLIND",
                "freeze_usable": True,
                "notes": "SPARC H I radius is nonzero and can support a source-window denominator.",
            },
            {
                "field_id": "Vflat_km_s",
                "value": float(sparc_row["Vflat_kms"]),
                "unit": "km/s",
                "source_id": "SPARC_MASTER",
                "field_status": "ACCEPTED_NUMERIC_RESIDUAL_BLIND",
                "freeze_usable": True,
                "notes": "Global velocity scale only; not a residual fit.",
            },
            {
                "field_id": "inclination_deg_sparc",
                "value": float(sparc_row["Inc_deg"]),
                "unit": "deg",
                "source_id": "SPARC_MASTER",
                "field_status": "ACCEPTED_NUMERIC_EDGE_ON_CAVEATED",
                "freeze_usable": True,
                "notes": "High inclination supports a projection/overlay caveat.",
            },
            {
                "field_id": "hi_position_angle_deg_source_native",
                "value": 347.0 if "347" in ursa_block else pd.NA,
                "unit": "deg",
                "source_id": "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "field_status": "SOURCE_PRESENT_REVIEW_REQUIRED",
                "freeze_usable": False,
                "notes": "OCR block reports total H I map position angle; needs independent review before freezing.",
            },
            {
                "field_id": "hi_inclination_deg_source_native",
                "value": 83.0 if "83" in ursa_block else pd.NA,
                "unit": "deg",
                "source_id": "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "field_status": "SOURCE_PRESENT_REVIEW_REQUIRED",
                "freeze_usable": False,
                "notes": "OCR block reports total H I map inclination; source-native but still review-gated.",
            },
            {
                "field_id": "hi_diameter_arcmin_source_native",
                "value": 6.1 if "6.1" in ursa_block else pd.NA,
                "unit": "arcmin",
                "source_id": "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "field_status": "SOURCE_PRESENT_REVIEW_REQUIRED",
                "freeze_usable": False,
                "notes": "Potential direct support radius proxy; must be converted/reviewed before formula freeze.",
            },
            {
                "field_id": "outer_warp_context",
                "value": "slightly warped in the outer regions" if warp_statement_present else pd.NA,
                "unit": "context",
                "source_id": "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "field_status": "ACCEPTED_CONTEXT_CAVEATED",
                "freeze_usable": False,
                "notes": "Supports mixed-overlay/projection review, but is not yet a numeric warp kernel.",
            },
            {
                "field_id": "edge_on_projection_context",
                "value": "optical-axis inclination likely too high" if high_inclination_statement_present else pd.NA,
                "unit": "context",
                "source_id": "VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI",
                "field_status": "ACCEPTED_CONTEXT_CAVEATED",
                "freeze_usable": False,
                "notes": "Supports projection/overlay lane, not standalone added-source scoring.",
            },
            {
                "field_id": "bar_core_history_overlay_observables",
                "value": pd.NA,
                "unit": "mixed",
                "source_id": "PENDING",
                "field_status": "BLOCKED_REQUIRED_FIELD_MISSING",
                "freeze_usable": False,
                "notes": "Needed by current NGC4183 mixed-overlay worklist before formula freeze.",
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4183_G1_RESIDUAL_BLIND_SOURCE_AUDIT",
                "gate_status": "PASS",
                "evidence": "uses SPARC metadata and cached literature, not endpoint residuals",
                "endpoint_scores_allowed": False,
                "remaining_obligation": "none for source-audit scope",
            },
            {
                "gate_id": "N4183_G2_GALAXY_SPECIFIC_HI_SOURCE",
                "gate_status": "PASS_REVIEW_REQUIRED",
                "evidence": "Verheijen & Sancisi 2001 NGC4183 H I block is locally cached",
                "endpoint_scores_allowed": False,
                "remaining_obligation": "independent review of PA/inc/HI diameter and usable kernel inputs",
            },
            {
                "gate_id": "N4183_G3_MIXED_OVERLAY_FREEZE_INPUTS",
                "gate_status": "BLOCKED",
                "evidence": "bar/core/projection/history overlay observables remain missing",
                "endpoint_scores_allowed": False,
                "remaining_obligation": "build galaxy-specific overlay observable sheet before formula freeze",
            },
            {
                "gate_id": "N4183_G4_FORMULA_FREEZE",
                "gate_status": "BLOCKED",
                "evidence": "source-native numeric overlay kernel is not frozen",
                "endpoint_scores_allowed": False,
                "remaining_obligation": "freeze lane, carrier, kernel, amplitude rule after source review",
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "source_audit_status": "NGC4183_MIXED_OVERLAY_SOURCE_AUDIT_LOCAL_SOURCE_PRESENT_REVIEW_REQUIRED_NOT_FREEZE_READY",
                "galaxy": GALAXY,
                "candidate_lane": str(worklist_row["candidate_lane"]),
                "candidate_readout": str(worklist_row["candidate_readout"]),
                "manifest_status_before_audit": str(manifest_row["audit_decision"]),
                "n_sources": len(sources),
                "n_freeze_usable_numeric_fields": int(fields["freeze_usable"].sum()),
                "has_galaxy_specific_hi_source": bool(has_ngc4183_ursa),
                "has_outer_warp_context": bool(warp_statement_present),
                "has_projection_context": bool(high_inclination_statement_present),
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "next_gate": "independent_review_of_source_native_hi_fields_and_overlay_observable_sheet",
            }
        ]
    )

    sources.to_csv(DATA / "ngc4183_mixed_overlay_source_audit_sources.csv", index=False)
    fields.to_csv(DATA / "ngc4183_mixed_overlay_source_audit_fields.csv", index=False)
    gates.to_csv(DATA / "ngc4183_mixed_overlay_source_audit_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4183_mixed_overlay_source_audit_summary.csv", index=False)

    report = f"""# NGC4183 Mixed-Overlay Source Audit

Status: `{summary.iloc[0]["source_audit_status"]}`

This is a residual-blind source-acquisition/preflight audit, not an endpoint
score.  It checks whether NGC4183 has enough source-native morphology/readout
information to advance from the mixed-overlay future worklist toward a formula
freeze.

## Summary

{markdown_table(summary)}

## Sources

{markdown_table(sources[["source_id", "source_role", "ngc4183_specific", "source_status", "usable_for_freeze"]])}

## Field Audit

{markdown_table(fields[["field_id", "value", "unit", "source_id", "field_status", "freeze_usable", "notes"]])}

## Gates

{markdown_table(gates[["gate_id", "gate_status", "evidence", "remaining_obligation"]])}

## Local H I Source Excerpt

`VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI` contains a galaxy-specific NGC4183 block.
The OCR is usable for preflight but must be independently reviewed before any
numeric formula freeze:

> {ursa_block[:1800]}

## Verdict

NGC4183 is strengthened from a purely context-only mixed-overlay candidate to a
local-source-present candidate.  The source-native H I block supports an
edge-on/projection and slight-outer-warp review path.  It does not yet authorize
formula freeze or endpoint scoring because the mixed-overlay kernel observables
and coefficient rules are still not independently frozen.
"""
    (REPORTS / "ngc4183_mixed_overlay_source_audit.md").write_text(report, encoding="utf-8")

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
