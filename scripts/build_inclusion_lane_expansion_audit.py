#!/usr/bin/env python3
"""Build strict/caution/acquisition inclusion lanes for Paper 8.

The purpose is to include more galaxies without weakening the accepted-lane
claim boundary.  Strict rows are the only acceptance-ready candidates.  Caution
rows can be used for support/sensitivity diagnostics only.  Acquisition rows
identify the residual-blind source data needed before inclusion.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "inclusion_lane_expansion_audit_not_endpoint"


def split_reasons(value: object) -> list[str]:
    text = str(value or "")
    if not text or text == "nan":
        return []
    return [part for part in text.split(";") if part and part != "none"]


def acquisition_need(row: pd.Series, blocked_components: list[str]) -> str:
    needs: list[str] = []
    if row["orientation_gate_status"] != "ORIENTATION_PROMOTION_READY_FOR_ACTIVE_COMPONENTS":
        if "K_thick_flared" in blocked_components:
            needs.append("needs_vertical_velocity_field_or_warp_flare_source")
        else:
            needs.append("needs_source_native_orientation_component_evidence")
    if row["projection_status"] == "PROJECTION_BLOCKED_RESIDUAL_BLIND_CAVEAT":
        for reason in split_reasons(row["projection_reason"]):
            if reason == "low_inclination":
                needs.append("needs_projection_or_inclination_audit")
            elif reason == "large_distance_error":
                needs.append("needs_distance_quality_or_scale_audit")
            elif reason in {"projection_caveat", "vertical_geometry_proxy_only"}:
                needs.append("needs_projection_geometry_source_review")
            elif reason == "low_manifest_confidence":
                needs.append("needs_manifest_confidence_review")
    if row["memory_status"] != "MEMORY_NOT_REQUIRED_CURRENT_READOUT_CONSISTENT":
        if row["memory_status"] == "MEMORY_BLOCKED_INVERSE_DIAGNOSTIC_NOT_ACCEPTED":
            needs.append("needs_residual_blind_memory_history_source")
        elif row["memory_status"] == "MEMORY_CAUTION_CURRENT_READOUT_CONSISTENT_WITH_SOURCE_FLAGS":
            needs.append("needs_source_memory_flag_resolution")
        else:
            needs.append("needs_memory_history_acceptance")
    if not needs:
        needs.append("needs_accepted_q_i_assignment_and_normalization_law")
    return ";".join(sorted(set(needs)))


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    gate = pd.read_csv(DATA / "memory_projection_acceptance_gate.csv")
    components = pd.read_csv(DATA / "source_native_orientation_component_gate.csv")
    blocked = (
        components.loc[
            components["component_orientation_status"].str.startswith("BLOCKED")
        ]
        .groupby("galaxy")["component_family"]
        .apply(lambda values: sorted(set(values)))
        .to_dict()
    )

    rows = []
    for _, row in gate.iterrows():
        orientation_ready = (
            row["orientation_gate_status"] == "ORIENTATION_PROMOTION_READY_FOR_ACTIVE_COMPONENTS"
        )
        projection_ready = row["projection_status"] == "PROJECTION_ACCEPTANCE_READY_RESIDUAL_BLIND"
        memory_strict = row["memory_status"] == "MEMORY_NOT_REQUIRED_CURRENT_READOUT_CONSISTENT"
        blocked_components = blocked.get(row["galaxy"], [])

        if row["memory_projection_gate_status"] == "MEMORY_PROJECTION_READY_CANDIDATE":
            lane = "STRICT_READY_CANDIDATE"
            lane_use = "strict_preendpoint_freeze_candidate"
        elif orientation_ready:
            lane = "CAUTION_READY_PROXY_SUPPORTED"
            if projection_ready:
                lane_use = "support_lane_memory_history_proxy"
            else:
                lane_use = "support_lane_projection_caveat"
        else:
            lane = "ACQUISITION_REQUIRED"
            lane_use = "source_acquisition_or_review_queue"

        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "formula_family": row["formula_family"],
                "inclusion_lane": lane,
                "allowed_use": lane_use,
                "orientation_gate_status": row["orientation_gate_status"],
                "projection_status": row["projection_status"],
                "memory_status": row["memory_status"],
                "memory_projection_gate_status": row["memory_projection_gate_status"],
                "blocked_orientation_components": ";".join(blocked_components) or "none",
                "minimal_acquisition_need": acquisition_need(row, blocked_components),
                "strict_ready": lane == "STRICT_READY_CANDIDATE",
                "caution_ready": lane == "CAUTION_READY_PROXY_SUPPORTED",
                "acquisition_required": lane == "ACQUISITION_REQUIRED",
                "endpoint_scores_computed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    audit = pd.DataFrame(rows).sort_values(["split", "inclusion_lane", "galaxy"])
    summary = summarize(audit)
    return audit, summary


def summarize(audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, sub in audit.groupby("split"):
        rows.append(summary_row(split, sub))
    return pd.concat([pd.DataFrame([summary_row("all", audit)]), pd.DataFrame(rows)], ignore_index=True)


def summary_row(split: str, sub: pd.DataFrame) -> dict[str, object]:
    return {
        "split": split,
        "n_galaxies": int(len(sub)),
        "strict_ready_count": int(sub["strict_ready"].sum()),
        "caution_ready_count": int(sub["caution_ready"].sum()),
        "analysis_includable_count": int((sub["strict_ready"] | sub["caution_ready"]).sum()),
        "acquisition_required_count": int(sub["acquisition_required"].sum()),
        "orientation_required_count": int(
            sub["minimal_acquisition_need"].str.contains(
                "needs_vertical_velocity_field_or_warp_flare_source|needs_source_native_orientation_component_evidence"
            ).sum()
        ),
        "projection_required_count": int(
            sub["minimal_acquisition_need"].str.contains(
                "needs_projection_or_inclination_audit|needs_distance_quality_or_scale_audit|needs_projection_geometry_source_review"
            ).sum()
        ),
        "memory_required_count": int(
            sub["minimal_acquisition_need"].str.contains(
                "needs_residual_blind_memory_history_source|needs_source_memory_flag_resolution|needs_memory_history_acceptance"
            ).sum()
        ),
        "endpoint_scores_computed": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: f"{value:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def write_report(audit: pd.DataFrame, summary: pd.DataFrame) -> None:
    full = summary.loc[summary["split"] == "all"].iloc[0]
    lane_counts = (
        audit.groupby(["inclusion_lane", "allowed_use"])
        .size()
        .reset_index(name="n_galaxies")
        .sort_values(["inclusion_lane", "allowed_use"])
    )
    need_counts = (
        audit.assign(need=audit["minimal_acquisition_need"].str.split(";"))
        .explode("need")
        .groupby("need")
        .size()
        .reset_index(name="n_galaxies")
        .sort_values("n_galaxies", ascending=False)
    )
    lines = [
        "# Inclusion Lane Expansion Audit",
        "",
        "This audit increases usable sample coverage without weakening the",
        "accepted-lane claim boundary. Strict rows are the only preendpoint",
        "freeze candidates. Caution rows may be used only as support or",
        "sensitivity lanes. Acquisition rows identify missing residual-blind",
        "source data.",
        "",
        "## Verdict",
        "",
        f"- Strict-ready candidates: {int(full['strict_ready_count'])}/175",
        f"- Caution/proxy-supported rows: {int(full['caution_ready_count'])}/175",
        f"- Analysis-includable strict+caution rows: {int(full['analysis_includable_count'])}/175",
        f"- Acquisition-required rows: {int(full['acquisition_required_count'])}/175",
        f"- Rows needing orientation source evidence: {int(full['orientation_required_count'])}/175",
        f"- Rows needing projection/scale review: {int(full['projection_required_count'])}/175",
        f"- Rows needing memory/history source review: {int(full['memory_required_count'])}/175",
        "",
        "The strict lane remains tiny. The practical expansion is the caution lane:",
        "it keeps orientation-ready rows available for non-claim support analyses",
        "while explicitly preserving their projection or memory/history caveats.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Lane Counts",
        "",
        markdown_table(lane_counts),
        "",
        "## Acquisition Need Counts",
        "",
        markdown_table(need_counts),
        "",
        "## Claim Boundary",
        "",
        "This audit computes no endpoint scores and uses no rotation residuals.",
        "Caution rows are not accepted evidence. They are only a way to avoid",
        "throwing away informative galaxies while keeping the final endpoint claim",
        "restricted to strict accepted lanes.",
    ]
    (REPORTS / "inclusion_lane_expansion_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    audit, summary = build_audit()
    audit.to_csv(DATA / "inclusion_lane_expansion_audit.csv", index=False)
    summary.to_csv(DATA / "inclusion_lane_expansion_summary.csv", index=False)
    write_report(audit, summary)
    print("PAPER8_INCLUSION_LANE_EXPANSION_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
