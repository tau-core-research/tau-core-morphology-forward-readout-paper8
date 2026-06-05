#!/usr/bin/env python3
"""Audit memory/projection acceptance after the source-native orientation gate.

This gate does not score rotation curves.  It asks which galaxies are ready to
move beyond the orientation gate using only residual-blind projection and
memory/history evidence.  Rotation-inferred memory diagnostics are treated as
triage signals, not accepted evidence.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "memory_projection_acceptance_gate_not_endpoint"


def has_caveat(caveat: object, needle: str) -> bool:
    return needle in str(caveat or "").lower()


def projection_status(row: pd.Series) -> tuple[str, str]:
    caveat = row.get("manifest_caveat", "")
    inclination = float(row["inclination_deg"]) if pd.notna(row["inclination_deg"]) else 60.0
    distance_error = (
        float(row["distance_frac_error"]) if pd.notna(row["distance_frac_error"]) else 0.30
    )
    confidence = (
        float(row["manifest_confidence"]) if pd.notna(row["manifest_confidence"]) else 0.0
    )
    blockers: list[str] = []
    if has_caveat(caveat, "low_inclination") or inclination < 30.0:
        blockers.append("low_inclination")
    if has_caveat(caveat, "edge") or has_caveat(caveat, "projection"):
        blockers.append("projection_caveat")
    if has_caveat(caveat, "vertical_geometry_proxy_only"):
        blockers.append("vertical_geometry_proxy_only")
    if has_caveat(caveat, "large_distance_error") or distance_error > 0.25:
        blockers.append("large_distance_error")
    if confidence < 0.55:
        blockers.append("low_manifest_confidence")

    if blockers:
        return (
            "PROJECTION_BLOCKED_RESIDUAL_BLIND_CAVEAT",
            ";".join(sorted(set(blockers))),
        )
    return (
        "PROJECTION_ACCEPTANCE_READY_RESIDUAL_BLIND",
        "manifest confidence, inclination, and distance/projection caveats pass",
    )


def memory_status(row: pd.Series) -> tuple[str, str]:
    proxy_class = str(row.get("memory_history_proxy_class", ""))
    flags = str(row.get("source_memory_proxy_flags", ""))
    proxy_status = str(row.get("proxy_status", ""))

    if proxy_class == "current_readout_consistent_no_memory_proxy_flag":
        if flags == "none":
            return (
                "MEMORY_NOT_REQUIRED_CURRENT_READOUT_CONSISTENT",
                "current proxy and readout proxy are consistent and no memory flag is present",
            )
        return (
            "MEMORY_CAUTION_CURRENT_READOUT_CONSISTENT_WITH_SOURCE_FLAGS",
            "current/readout proxy is consistent but source-side caveats remain",
        )
    if "SOURCE_PLUS_INVERSE" in proxy_status:
        return (
            "MEMORY_BLOCKED_INVERSE_DIAGNOSTIC_NOT_ACCEPTED",
            "memory class uses rotation-inferred diagnostic and cannot be accepted",
        )
    return (
        "MEMORY_BLOCKED_PROXY_NOT_ACCEPTED",
        "memory/history proxy is not accepted source-native evidence",
    )


def memory_acceptance_ready(status: str) -> bool:
    return status == "MEMORY_NOT_REQUIRED_CURRENT_READOUT_CONSISTENT"


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame]:
    orientation = pd.read_csv(DATA / "source_native_orientation_galaxy_gate.csv")
    manifest = pd.read_csv(DATA / "morphology_parameter_manifest.csv")
    memory = pd.read_csv(DATA / "morphological_memory_history_proxy.csv")

    table = orientation.merge(
        manifest[
            [
                "galaxy",
                "formula_family",
                "manifest_confidence",
                "manifest_caveat",
                "inclination_deg",
                "distance_frac_error",
            ]
        ],
        on="galaxy",
        how="left",
        validate="one_to_one",
    ).merge(
        memory[
            [
                "galaxy",
                "memory_history_proxy_class",
                "source_memory_proxy_flags",
                "proxy_status",
                "claim_boundary",
            ]
        ].rename(columns={"claim_boundary": "memory_proxy_claim_boundary"}),
        on="galaxy",
        how="left",
        validate="one_to_one",
    )

    rows = []
    for _, row in table.iterrows():
        proj_status, proj_reason = projection_status(row)
        mem_status, mem_reason = memory_status(row)
        orientation_ready = (
            row["orientation_gate_status"] == "ORIENTATION_PROMOTION_READY_FOR_ACTIVE_COMPONENTS"
        )
        projection_ready = proj_status == "PROJECTION_ACCEPTANCE_READY_RESIDUAL_BLIND"
        memory_ready = memory_acceptance_ready(mem_status)

        if not orientation_ready:
            gate_status = "BLOCKED_ORIENTATION_NOT_READY"
        elif not projection_ready:
            gate_status = "BLOCKED_PROJECTION_ACCEPTANCE"
        elif not memory_ready:
            gate_status = "BLOCKED_MEMORY_HISTORY_ACCEPTANCE"
        else:
            gate_status = "MEMORY_PROJECTION_READY_CANDIDATE"

        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "formula_family": row["formula_family"],
                "orientation_gate_status": row["orientation_gate_status"],
                "projection_status": proj_status,
                "projection_reason": proj_reason,
                "memory_status": mem_status,
                "memory_reason": mem_reason,
                "memory_history_proxy_class": row["memory_history_proxy_class"],
                "source_memory_proxy_flags": row["source_memory_proxy_flags"],
                "manifest_confidence": row["manifest_confidence"],
                "manifest_caveat": row["manifest_caveat"],
                "inclination_deg": row["inclination_deg"],
                "distance_frac_error": row["distance_frac_error"],
                "memory_projection_gate_status": gate_status,
                "endpoint_scores_computed": False,
                "uses_vobs_or_residual": False,
                "endpoint_freeze_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    gate = pd.DataFrame(rows).sort_values(["split", "galaxy"])
    summary = summarize(gate)
    return gate, summary


def summarize(gate: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, sub in gate.groupby("split"):
        rows.append(summary_row(split, sub))
    return pd.concat([pd.DataFrame([summary_row("all", gate)]), pd.DataFrame(rows)], ignore_index=True)


def summary_row(split: str, sub: pd.DataFrame) -> dict[str, object]:
    return {
        "split": split,
        "n_galaxies": int(len(sub)),
        "orientation_ready_count": int(
            sub["orientation_gate_status"].eq(
                "ORIENTATION_PROMOTION_READY_FOR_ACTIVE_COMPONENTS"
            ).sum()
        ),
        "projection_ready_count": int(
            sub["projection_status"].eq("PROJECTION_ACCEPTANCE_READY_RESIDUAL_BLIND").sum()
        ),
        "memory_ready_or_not_required_count": int(
            sub["memory_status"].map(memory_acceptance_ready).sum()
        ),
        "memory_projection_ready_candidate_count": int(
            sub["memory_projection_gate_status"].eq("MEMORY_PROJECTION_READY_CANDIDATE").sum()
        ),
        "blocked_orientation_count": int(
            sub["memory_projection_gate_status"].eq("BLOCKED_ORIENTATION_NOT_READY").sum()
        ),
        "blocked_projection_count": int(
            sub["memory_projection_gate_status"].eq("BLOCKED_PROJECTION_ACCEPTANCE").sum()
        ),
        "blocked_memory_history_count": int(
            sub["memory_projection_gate_status"].eq("BLOCKED_MEMORY_HISTORY_ACCEPTANCE").sum()
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


def write_report(gate: pd.DataFrame, summary: pd.DataFrame) -> None:
    full = summary.loc[summary["split"] == "all"].iloc[0]
    lines = [
        "# Memory / Projection Acceptance Gate",
        "",
        "This residual-blind audit asks whether galaxies that pass the",
        "source-native orientation gate also pass projection and morphology-memory",
        "acceptance. It computes no endpoint scores and does not use rotation",
        "residuals.",
        "",
        "## Verdict",
        "",
        f"- Galaxies audited: {int(full['n_galaxies'])}",
        f"- Orientation-ready: {int(full['orientation_ready_count'])}",
        f"- Projection-ready: {int(full['projection_ready_count'])}",
        f"- Memory ready or not required: {int(full['memory_ready_or_not_required_count'])}",
        f"- Memory/projection ready candidates after orientation: {int(full['memory_projection_ready_candidate_count'])}",
        f"- Blocked by orientation: {int(full['blocked_orientation_count'])}",
        f"- Blocked by projection after orientation: {int(full['blocked_projection_count'])}",
        f"- Blocked by memory/history after orientation and projection: {int(full['blocked_memory_history_count'])}",
        "",
        "The existing morphology-memory proxy remains useful as a triage layer,",
        "but its rotation-inferred component is inverse diagnostic information.",
        "It is therefore not accepted as memory/history evidence. Rows marked",
        "ready here are readiness candidates only; endpoint freeze still requires",
        "accepted per-galaxy q_i assignments and an accepted normalization law.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gate Status Counts",
        "",
        markdown_table(
            gate.groupby("memory_projection_gate_status")
            .size()
            .reset_index(name="n_galaxies")
            .sort_values("memory_projection_gate_status")
        ),
        "",
        "## Memory Status Counts",
        "",
        markdown_table(
            gate.groupby("memory_status")
            .size()
            .reset_index(name="n_galaxies")
            .sort_values("memory_status")
        ),
        "",
        "## Projection Status Counts",
        "",
        markdown_table(
            gate.groupby("projection_status")
            .size()
            .reset_index(name="n_galaxies")
            .sort_values("projection_status")
        ),
        "",
        "## Claim Boundary",
        "",
        "This gate is not empirical validation, not a morphology label, and not",
        "endpoint scoring. Projection and memory/history acceptance must remain",
        "residual-blind; rotation-inferred morphology can only motivate future",
        "source acquisition.",
    ]
    (REPORTS / "memory_projection_acceptance_gate.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    gate, summary = build_gate()
    gate.to_csv(DATA / "memory_projection_acceptance_gate.csv", index=False)
    summary.to_csv(DATA / "memory_projection_acceptance_summary.csv", index=False)
    write_report(gate, summary)
    print("PAPER8_MEMORY_PROJECTION_ACCEPTANCE_GATE_COMPLETE")


if __name__ == "__main__":
    main()
