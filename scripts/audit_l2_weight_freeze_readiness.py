#!/usr/bin/env python3
"""Audit whether L2 weight-intake candidates can be frozen for endpoint use.

The preceding endpoint preflight showed that source-intake weights are not yet
globally better than the older L2 mixture proxy.  This audit turns that result
into a gate: which components have residual-blind source support, which remain
proxy-only, and what blocks endpoint freeze?

No endpoint score is computed here.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "l2_weight_freeze_readiness_audit_not_endpoint"
FAMILIES = [
    "K_compact_finite",
    "K_scale_tail_spiral",
    "K_exponential_disk",
    "K_thick_flared",
]


def component_evidence(row: pd.Series, family: str) -> tuple[str, str]:
    if family == "K_scale_tail_spiral":
        if bool(row["sparc_hi_ready"]) or bool(row["dustpedia_hi_match"]):
            return "SOURCE_CANDIDATE_HI_TAIL_READY", "SPARC/DustPedia HI-tail source candidate"
        return "MISSING_SOURCE_SUPPORT", "no HI/tail source candidate"

    if family == "K_exponential_disk":
        if bool(row["s4g_scale_ready"]):
            return "SOURCE_CANDIDATE_S4G_SCALE_READY", "S4G scale-radius source candidate"
        return "MISSING_SOURCE_SUPPORT", "no S4G scale source candidate"

    if family == "K_compact_finite":
        if bool(row["s4g_compact_component_ready"]) or bool(row["dustpedia_physical_match"]):
            return "SOURCE_CANDIDATE_COMPACT_READY", "S4G/DustPedia compact source candidate"
        return "MISSING_SOURCE_SUPPORT", "no compact/core source candidate"

    if family == "K_thick_flared":
        if bool(row["phangs_muse_ready"]):
            return "SOURCE_CANDIDATE_VELOCITY_FIELD_READY", "PHANGS/MUSE velocity-field support"
        if bool(row["phangs_alma_ready"]) or bool(row["q_memory_candidate"]):
            return "PROXY_OR_PARTIAL_SOURCE_ONLY", "projection/memory proxy without accepted vertical source"
        return "MISSING_SOURCE_SUPPORT", "no thickness/flare/warp source candidate"

    raise ValueError(family)


def build_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    candidates = pd.read_csv(DATA / "morphology_information_gain_l2_weight_intake_candidates.csv")
    expansion = pd.read_csv(DATA / "morphology_information_gain_source_expansion.csv")
    table = candidates.merge(expansion, on=["galaxy", "split"], how="left", validate="one_to_one")
    norm_path = DATA / "tau_side_source_normalization_galaxy_rule.csv"
    normalization_candidates = set()
    if norm_path.exists():
        norm = pd.read_csv(norm_path)
        normalization_candidates = set(norm["galaxy"])
    orientation_path = DATA / "source_native_orientation_galaxy_gate.csv"
    orientation_gate = {}
    if orientation_path.exists():
        orientation = pd.read_csv(orientation_path)
        orientation_gate = dict(zip(orientation["galaxy"], orientation["orientation_gate_status"]))
    memory_projection_path = DATA / "memory_projection_acceptance_gate.csv"
    memory_projection_gate = {}
    if memory_projection_path.exists():
        memory_projection = pd.read_csv(memory_projection_path)
        memory_projection_gate = dict(
            zip(memory_projection["galaxy"], memory_projection["memory_projection_gate_status"])
        )

    rows = []
    component_rows = []
    for _, row in table.iterrows():
        nonzero_families = [family for family in FAMILIES if float(row[f"w_{family}"]) > 0.0]
        statuses = {}
        proxy_or_missing = []
        source_supported = []
        for family in nonzero_families:
            status, reason = component_evidence(row, family)
            statuses[family] = status
            component_rows.append(
                {
                    "galaxy": row["galaxy"],
                    "split": row["split"],
                    "component_family": family,
                    "component_weight": float(row[f"w_{family}"]),
                    "component_evidence_status": status,
                    "component_evidence_reason": reason,
                    "endpoint_freeze_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            if status.startswith("SOURCE_CANDIDATE"):
                source_supported.append(family)
            else:
                proxy_or_missing.append(family)

        if row["galaxy"] in normalization_candidates:
            normalization_status = "FORMULA_CONDITIONAL_NORMALIZATION_CANDIDATE_PRESENT_NOT_ACCEPTED"
        else:
            normalization_status = "MISSING_TAU_SIDE_SOURCE_NORMALIZATION_RULE"
        proxy_gate_status = "RESOLVED_DERIVED_COARSE_GRID_PROXY_ADMISSION_PRODUCT"
        orientation_status = orientation_gate.get(
            row["galaxy"],
            "BLOCKED_SOURCE_NATIVE_ORIENTATION_PROMOTION_REQUIRED",
        )
        memory_status = (
            "MEMORY_PROXY_AVAILABLE_NOT_ACCEPTED"
            if bool(row["q_memory_candidate"])
            else "MEMORY_SOURCE_MISSING"
        )
        memory_projection_status = memory_projection_gate.get(
            row["galaxy"], "BLOCKED_MEMORY_PROJECTION_GATE_NOT_RUN"
        )
        dominant_status = statuses.get(row["dominant_intake_family"], "MISSING_SOURCE_SUPPORT")

        if normalization_status.startswith("MISSING"):
            freeze_status = "FREEZE_BLOCKED_NORMALIZATION_MISSING"
        elif "BLOCKED" in orientation_status:
            freeze_status = "FREEZE_BLOCKED_ORIENTATION_PROMOTION_NOT_ACCEPTED"
        elif memory_projection_status == "BLOCKED_PROJECTION_ACCEPTANCE":
            freeze_status = "FREEZE_BLOCKED_PROJECTION_ACCEPTANCE_NOT_ACCEPTED"
        elif memory_projection_status == "BLOCKED_MEMORY_HISTORY_ACCEPTANCE":
            freeze_status = "FREEZE_BLOCKED_MEMORY_PROJECTION_NOT_ACCEPTED"
        elif memory_projection_status == "MEMORY_PROJECTION_READY_CANDIDATE":
            freeze_status = "FREEZE_BLOCKED_QI_AND_NORMALIZATION_ACCEPTANCE_NOT_ACCEPTED"
        elif memory_projection_status.startswith("BLOCKED"):
            freeze_status = "FREEZE_BLOCKED_MEMORY_PROJECTION_NOT_ACCEPTED"
        elif proxy_or_missing:
            freeze_status = "FREEZE_BLOCKED_PROXY_OR_MISSING_COMPONENT"
        else:
            freeze_status = "FREEZE_READY_AFTER_PROTOCOL_LOCK"

        if proxy_or_missing:
            component_gate = "COMPONENT_PROXY_OR_MISSING"
        elif source_supported:
            component_gate = "SOURCE_CANDIDATES_PRESENT"
        else:
            component_gate = "NO_COMPONENT_SIGNAL"

        rows.append(
            {
                "galaxy": row["galaxy"],
                "split": row["split"],
                "coarse_formula_family": row["coarse_formula_family"],
                "dominant_intake_family": row["dominant_intake_family"],
                "dominant_evidence_status": dominant_status,
                "n_nonzero_source_components": int(row["n_nonzero_source_components"]),
                "source_supported_components": ";".join(source_supported),
                "proxy_or_missing_components": ";".join(proxy_or_missing),
                "component_gate": component_gate,
                "normalization_status": normalization_status,
                "normalization_candidate_present": row["galaxy"] in normalization_candidates,
                "proxy_gate_status": proxy_gate_status,
                "orientation_status": orientation_status,
                "memory_status": memory_status,
                "memory_projection_status": memory_projection_status,
                "freeze_status": freeze_status,
                "endpoint_scores_computed": False,
                "endpoint_freeze_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    audit = pd.DataFrame(rows).sort_values(["split", "galaxy"])
    component_audit = pd.DataFrame(component_rows).sort_values(
        ["split", "galaxy", "component_family"]
    )
    return audit, component_audit


def summarize(audit: pd.DataFrame, component_audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, sub in audit.groupby("split"):
        comp = component_audit.loc[component_audit["split"] == split]
        rows.append(
            {
                "split": split,
                "n_galaxies": int(len(sub)),
                "freeze_allowed_count": int(sub["endpoint_freeze_allowed"].sum()),
                "blocked_normalization_count": int(
                    sub["freeze_status"].str.startswith("FREEZE_BLOCKED_NORMALIZATION").sum()
                ),
                "blocked_orientation_count": int(
                    sub["freeze_status"].eq("FREEZE_BLOCKED_ORIENTATION_PROMOTION_NOT_ACCEPTED").sum()
                ),
                "orientation_ready_count": int(
                    sub["orientation_status"].eq(
                        "ORIENTATION_PROMOTION_READY_FOR_ACTIVE_COMPONENTS"
                    ).sum()
                ),
                "orientation_blocked_count": int(
                    sub["orientation_status"].str.contains("BLOCKED").sum()
                ),
                "blocked_memory_projection_count": int(
                    sub["freeze_status"].eq("FREEZE_BLOCKED_MEMORY_PROJECTION_NOT_ACCEPTED").sum()
                ),
                "blocked_projection_acceptance_count": int(
                    sub["freeze_status"].eq("FREEZE_BLOCKED_PROJECTION_ACCEPTANCE_NOT_ACCEPTED").sum()
                ),
                "blocked_qi_normalization_acceptance_count": int(
                    sub["freeze_status"].eq(
                        "FREEZE_BLOCKED_QI_AND_NORMALIZATION_ACCEPTANCE_NOT_ACCEPTED"
                    ).sum()
                ),
                "blocked_proxy_or_missing_component_count": int(
                    sub["freeze_status"].eq("FREEZE_BLOCKED_PROXY_OR_MISSING_COMPONENT").sum()
                ),
                "proxy_gate_resolved_count": int(
                    sub["proxy_gate_status"].eq(
                        "RESOLVED_DERIVED_COARSE_GRID_PROXY_ADMISSION_PRODUCT"
                    ).sum()
                ),
                "normalization_candidate_present_count": int(
                    sub["normalization_candidate_present"].sum()
                ),
                "component_proxy_or_missing_count": int(
                    sub["component_gate"].eq("COMPONENT_PROXY_OR_MISSING").sum()
                ),
                "source_candidates_present_count": int(
                    sub["component_gate"].eq("SOURCE_CANDIDATES_PRESENT").sum()
                ),
                "dominant_source_candidate_count": int(
                    sub["dominant_evidence_status"].str.startswith("SOURCE_CANDIDATE").sum()
                ),
                "dominant_proxy_or_partial_count": int(
                    sub["dominant_evidence_status"].eq("PROXY_OR_PARTIAL_SOURCE_ONLY").sum()
                ),
                "dominant_missing_source_count": int(
                    sub["dominant_evidence_status"].eq("MISSING_SOURCE_SUPPORT").sum()
                ),
                "nonzero_source_candidate_components": int(
                    comp["component_evidence_status"].str.startswith("SOURCE_CANDIDATE").sum()
                ),
                "nonzero_proxy_or_partial_components": int(
                    comp["component_evidence_status"].eq("PROXY_OR_PARTIAL_SOURCE_ONLY").sum()
                ),
                "nonzero_missing_components": int(
                    comp["component_evidence_status"].eq("MISSING_SOURCE_SUPPORT").sum()
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    summary = pd.DataFrame(rows)
    all_row = {
        "split": "all",
        "n_galaxies": int(len(audit)),
        "freeze_allowed_count": int(audit["endpoint_freeze_allowed"].sum()),
        "blocked_normalization_count": int(
            audit["freeze_status"].str.startswith("FREEZE_BLOCKED_NORMALIZATION").sum()
        ),
        "blocked_orientation_count": int(
            audit["freeze_status"].eq("FREEZE_BLOCKED_ORIENTATION_PROMOTION_NOT_ACCEPTED").sum()
        ),
        "orientation_ready_count": int(
            audit["orientation_status"].eq("ORIENTATION_PROMOTION_READY_FOR_ACTIVE_COMPONENTS").sum()
        ),
        "orientation_blocked_count": int(audit["orientation_status"].str.contains("BLOCKED").sum()),
        "blocked_memory_projection_count": int(
            audit["freeze_status"].eq("FREEZE_BLOCKED_MEMORY_PROJECTION_NOT_ACCEPTED").sum()
        ),
        "blocked_projection_acceptance_count": int(
            audit["freeze_status"].eq("FREEZE_BLOCKED_PROJECTION_ACCEPTANCE_NOT_ACCEPTED").sum()
        ),
        "blocked_qi_normalization_acceptance_count": int(
            audit["freeze_status"].eq(
                "FREEZE_BLOCKED_QI_AND_NORMALIZATION_ACCEPTANCE_NOT_ACCEPTED"
            ).sum()
        ),
        "blocked_proxy_or_missing_component_count": int(
            audit["freeze_status"].eq("FREEZE_BLOCKED_PROXY_OR_MISSING_COMPONENT").sum()
        ),
        "proxy_gate_resolved_count": int(
            audit["proxy_gate_status"].eq("RESOLVED_DERIVED_COARSE_GRID_PROXY_ADMISSION_PRODUCT").sum()
        ),
        "normalization_candidate_present_count": int(
            audit["normalization_candidate_present"].sum()
        ),
        "component_proxy_or_missing_count": int(
            audit["component_gate"].eq("COMPONENT_PROXY_OR_MISSING").sum()
        ),
        "source_candidates_present_count": int(
            audit["component_gate"].eq("SOURCE_CANDIDATES_PRESENT").sum()
        ),
        "dominant_source_candidate_count": int(
            audit["dominant_evidence_status"].str.startswith("SOURCE_CANDIDATE").sum()
        ),
        "dominant_proxy_or_partial_count": int(
            audit["dominant_evidence_status"].eq("PROXY_OR_PARTIAL_SOURCE_ONLY").sum()
        ),
        "dominant_missing_source_count": int(
            audit["dominant_evidence_status"].eq("MISSING_SOURCE_SUPPORT").sum()
        ),
        "nonzero_source_candidate_components": int(
            component_audit["component_evidence_status"].str.startswith("SOURCE_CANDIDATE").sum()
        ),
        "nonzero_proxy_or_partial_components": int(
            component_audit["component_evidence_status"].eq("PROXY_OR_PARTIAL_SOURCE_ONLY").sum()
        ),
        "nonzero_missing_components": int(
            component_audit["component_evidence_status"].eq("MISSING_SOURCE_SUPPORT").sum()
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return pd.concat([pd.DataFrame([all_row]), summary], ignore_index=True)


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


def write_report(audit: pd.DataFrame, component_audit: pd.DataFrame, summary: pd.DataFrame) -> None:
    full = summary.loc[summary["split"] == "all"].iloc[0]
    lines = [
        "# L2 Weight Freeze-Readiness Audit",
        "",
        "This audit checks whether the residual-blind L2 weight-intake candidates",
        "can be frozen for endpoint use. It computes no endpoint score.",
        "",
        "## Verdict",
        "",
        f"- Galaxies audited: {int(full['n_galaxies'])}",
        f"- Endpoint-freeze allowed: {int(full['freeze_allowed_count'])}",
        f"- Proxy-gate blocker resolved by derived coarse-grid E_tau product: {int(full['proxy_gate_resolved_count'])}",
        f"- Blocked by missing Tau-side normalization: {int(full['blocked_normalization_count'])}",
        f"- Source-native orientation ready after promotion gate: {int(full['orientation_ready_count'])}",
        f"- Blocked by source-native orientation promotion: {int(full['blocked_orientation_count'])}",
        f"- Blocked by projection acceptance after orientation: {int(full['blocked_projection_acceptance_count'])}",
        f"- Blocked by memory/history acceptance after orientation and projection: {int(full['blocked_memory_projection_count'])}",
        f"- Blocked by q_i/normalization acceptance after memory/projection: {int(full['blocked_qi_normalization_acceptance_count'])}",
        f"- Blocked by proxy-or-missing active components after orientation: {int(full['blocked_proxy_or_missing_component_count'])}",
        f"- Formula-conditional normalization candidates present: {int(full['normalization_candidate_present_count'])}",
        f"- Dominant components with source-candidate support: {int(full['dominant_source_candidate_count'])}",
        f"- Dominant components proxy/partial only: {int(full['dominant_proxy_or_partial_count'])}",
        f"- Dominant components missing source support: {int(full['dominant_missing_source_count'])}",
        "",
        "The endpoint remains blocked for every galaxy, but the blocker has",
        "changed. The proxy gate is no longer treated as a free protocol",
        "constant: it is resolved as the conservative coarse-grid E_tau product.",
        "The source-native orientation gate now partially promotes the",
        "theory-conditional orientation signs. The remaining blockers split",
        "into still-unpromoted orientation rows, projection caveats,",
        "morphology-memory/history acceptance, and the final accepted q_i plus",
        "normalization-law step. This is a protocol safeguard, not a negative",
        "empirical result.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Component Evidence Counts",
        "",
        markdown_table(
            component_audit.groupby(["component_family", "component_evidence_status"])
            .size()
            .reset_index(name="n_components")
        ),
        "",
        "## Claim Boundary",
        "",
        "This audit may identify source-supported candidate components, but it does",
        "not accept weights, does not launch the endpoint, and does not use",
        "rotation residuals. A later endpoint requires source-native orientation",
        "promotion, accepted per-galaxy evidence assignments, and an accepted",
        "morphology-memory/projection audit.",
    ]
    (REPORTS / "morphology_information_gain_l2_weight_freeze_readiness.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    audit, component_audit = build_audit()
    summary = summarize(audit, component_audit)
    audit.to_csv(DATA / "morphology_information_gain_l2_weight_freeze_readiness.csv", index=False)
    component_audit.to_csv(
        DATA / "morphology_information_gain_l2_weight_freeze_component_audit.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "morphology_information_gain_l2_weight_freeze_readiness_summary.csv",
        index=False,
    )
    write_report(audit, component_audit, summary)
    print("PAPER8_L2_WEIGHT_FREEZE_READINESS_AUDIT_COMPLETE")


if __name__ == "__main__":
    main()
