#!/usr/bin/env python3
"""Build a projection/scale repair audit for inclusion-lane galaxies.

This audit is residual-blind.  It does not score endpoints and does not change
any lane.  It identifies which projection/scale blockers are likely repairable
from existing source layers and which require new external review.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "projection_scale_repair_audit_not_endpoint"


def split_parts(text: object) -> list[str]:
    value = str(text or "")
    if not value or value == "nan" or value == "none":
        return []
    return [part for part in value.split(";") if part and part != "none"]


def repair_class(row: pd.Series) -> tuple[str, str]:
    if row.get("projection_status_x") == "PROJECTION_ACCEPTANCE_READY_RESIDUAL_BLIND":
        return "NO_PROJECTION_SCALE_REPAIR_REQUIRED", "projection/scale gate is already clean"
    reasons = set(split_parts(row["projection_reason"]))
    if not reasons:
        return "NO_PROJECTION_SCALE_REPAIR_REQUIRED", "projection/scale gate is already clean"
    if "vertical_geometry_proxy_only" in reasons:
        return (
            "NEEDS_VERTICAL_GEOMETRY_SOURCE",
            "requires vertical thickness, flare, warp, or velocity-field source evidence",
        )
    if "low_inclination" in reasons:
        return (
            "NEEDS_INCLINATION_PROJECTION_REVIEW",
            "requires residual-blind inclination/projection audit",
        )
    if "large_distance_error" in reasons:
        if bool(row.get("s4g_scale_ready", False)):
            return (
                "REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT",
                "S4G/SPARC scale source exists; distance/scale uncertainty still needs review",
            )
        return (
            "NEEDS_DISTANCE_SCALE_SOURCE",
            "distance/scale quality is blocking and no S4G scale source is ready",
        )
    if "low_manifest_confidence" in reasons:
        return (
            "NEEDS_MANIFEST_CONFIDENCE_REVIEW",
            "manifest confidence is below acceptance threshold",
        )
    return "NEEDS_PROJECTION_SCALE_REVIEW", ";".join(sorted(reasons))


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    lanes = pd.read_csv(DATA / "inclusion_lane_expansion_audit.csv")
    mp = pd.read_csv(DATA / "memory_projection_acceptance_gate.csv")
    expansion = pd.read_csv(DATA / "morphology_information_gain_source_expansion.csv")
    table = lanes.merge(
        mp[
            [
                "galaxy",
                "split",
                "projection_status",
                "projection_reason",
                "manifest_confidence",
                "manifest_caveat",
                "inclination_deg",
                "distance_frac_error",
            ]
        ],
        on=["galaxy", "split"],
        how="left",
        validate="one_to_one",
    ).merge(
        expansion[
            [
                "galaxy",
                "sparc_hi_ready",
                "s4g_scale_ready",
                "phangs_muse_ready",
                "phangs_alma_ready",
                "l4_velocity_field_candidate",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    )

    rows = []
    for _, row in table.iterrows():
        status, reason = repair_class(row)
        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "formula_family": row["formula_family"],
                "inclusion_lane": row["inclusion_lane"],
                "allowed_use": row["allowed_use"],
                "projection_status": row["projection_status_x"],
                "projection_reason": row["projection_reason"],
                "repair_status": status,
                "repair_reason": reason,
                "has_s4g_scale_source": bool(row.get("s4g_scale_ready", False)),
                "has_hi_source": bool(row.get("sparc_hi_ready", False)),
                "has_velocity_field_source": bool(row.get("l4_velocity_field_candidate", False))
                or bool(row.get("phangs_muse_ready", False)),
                "manifest_confidence": row["manifest_confidence"],
                "manifest_caveat": row["manifest_caveat"],
                "inclination_deg": row["inclination_deg"],
                "distance_frac_error": row["distance_frac_error"],
                "endpoint_scores_computed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    audit = pd.DataFrame(rows).sort_values(["split", "inclusion_lane", "repair_status", "galaxy"])
    summary = summarize(audit)
    return audit, summary


def summarize(audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, sub in audit.groupby("split"):
        rows.extend(summary_rows(split, sub))
    rows.extend(summary_rows("all", audit))
    return pd.DataFrame(rows).sort_values(["split", "repair_status"])


def summary_rows(split: str, sub: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    for status, group in sub.groupby("repair_status"):
        rows.append(
            {
                "split": split,
                "repair_status": status,
                "n_galaxies": int(len(group)),
                "n_holdout": int(group["split"].eq("holdout").sum()) if split == "all" else pd.NA,
                "n_caution": int(group["inclusion_lane"].eq("CAUTION_READY_PROXY_SUPPORTED").sum()),
                "n_acquisition": int(group["inclusion_lane"].eq("ACQUISITION_REQUIRED").sum()),
                "n_existing_s4g_scale": int(group["has_s4g_scale_source"].sum()),
                "n_velocity_field_source": int(group["has_velocity_field_source"].sum()),
                "endpoint_scores_computed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


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
    all_summary = summary.loc[summary["split"] == "all"]
    lines = [
        "# Projection / Scale Repair Audit",
        "",
        "This audit identifies projection and scale-quality repair targets using",
        "only residual-blind source and manifest fields. It computes no endpoint",
        "scores and changes no lane assignment.",
        "",
        "## Verdict",
        "",
        markdown_table(all_summary),
        "",
        "## Holdout Projection-Caveat Rows",
        "",
        markdown_table(
            audit.loc[
                (audit["split"] == "holdout")
                & (audit["allowed_use"] == "support_lane_projection_caveat"),
                [
                    "galaxy",
                    "formula_family",
                    "repair_status",
                    "projection_reason",
                    "has_s4g_scale_source",
                    "inclination_deg",
                    "distance_frac_error",
                ],
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This is a source-acquisition and repair map, not an empirical validation",
        "result. Repairable means source-side repairable, not endpoint-improving.",
    ]
    (REPORTS / "projection_scale_repair_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    audit, summary = build_audit()
    audit.to_csv(DATA / "projection_scale_repair_audit.csv", index=False)
    summary.to_csv(DATA / "projection_scale_repair_summary.csv", index=False)
    write_report(audit, summary)
    print("PAPER8_PROJECTION_SCALE_REPAIR_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
