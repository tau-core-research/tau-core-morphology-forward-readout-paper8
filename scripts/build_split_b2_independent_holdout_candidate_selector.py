#!/usr/bin/env python3
"""Select independent split-B2 holdout candidates after the NGC7331 diagnostic.

This script does not score endpoints and does not read observed velocities.
It records which galaxies can serve as residual-blind tests for the split-B2
unit-load repair, and which source fields still block them.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "split_b2_independent_holdout_candidate_selector_not_endpoint"


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


def read_optional_csv(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def sparc_row(sparc: pd.DataFrame, galaxy: str) -> dict[str, object]:
    rows = sparc[sparc["Galaxy"].astype(str).str.upper() == galaxy.upper()]
    if rows.empty:
        return {
            "sparc_vflat_km_s": pd.NA,
            "sparc_rhi_kpc": pd.NA,
            "sparc_rdisk_kpc": pd.NA,
            "sparc_inc_deg": pd.NA,
            "sparc_status": "MISSING_SPARC_ROW",
        }
    row = rows.iloc[0]
    rhi = float(row["RHI_kpc"])
    vflat = float(row["Vflat_kms"])
    status = "SPARC_VFLAT_RHI_READY"
    if vflat <= 0 and rhi <= 0:
        status = "SPARC_VFLAT_AND_RHI_MISSING"
    elif vflat <= 0:
        status = "SPARC_VFLAT_MISSING"
    elif rhi <= 0:
        status = "SPARC_RHI_MISSING_OR_ZERO"
    return {
        "sparc_vflat_km_s": vflat,
        "sparc_rhi_kpc": rhi,
        "sparc_rdisk_kpc": float(row["Rdisk_kpc"]),
        "sparc_inc_deg": float(row["Inc_deg"]),
        "sparc_status": status,
    }


def first_row_value(df: pd.DataFrame, column: str, default: object = pd.NA) -> object:
    if df.empty or column not in df.columns:
        return default
    return df.iloc[0][column]


def candidate_from_sources(
    galaxy: str,
    exact: pd.DataFrame,
    queue: pd.DataFrame,
    sparc: pd.DataFrame,
) -> dict[str, object]:
    exact_row = exact[exact["galaxy"].astype(str).str.upper() == galaxy.upper()]
    queue_row = queue[queue["galaxy"].astype(str).str.upper() == galaxy.upper()]
    srow = sparc_row(sparc, galaxy)

    exact_status = first_row_value(exact_row, "candidate_status", "NO_EXACT_B2_ROW")
    queue_priority = first_row_value(queue_row, "candidate_priority", "NO_QUEUE_ROW")
    queue_role = first_row_value(queue_row, "candidate_role", "NO_QUEUE_ROW")
    mixed_readout = first_row_value(queue_row, "candidate_mixed_readout", "NO_QUEUE_ROW")
    source_observables = first_row_value(queue_row, "source_observable_names", "")
    citations = first_row_value(queue_row, "source_citation_keys", "")
    next_gate = first_row_value(queue_row, "required_next_gate", "")
    notes = first_row_value(queue_row, "blocking_or_caution_notes", "")
    source_rule_candidate = bool(first_row_value(queue_row, "source_rule_candidate", False))
    has_numeric_warp = bool(first_row_value(queue_row, "has_numeric_warp_activation", False))
    has_overlay_context = bool(first_row_value(queue_row, "has_overlay_context", False))

    independent_status = "UNRANKED"
    endpoint_allowed = False
    reason = ""
    blockers = []
    recommended_action = ""
    denominator_policy = "UNSET"

    if galaxy == "NGC7331":
        independent_status = "EXCLUDED_DIAGNOSTIC_ORIGIN"
        reason = "Split-B2 repair was identified on this galaxy after the exact-transfer failure."
        blockers.append("same_curve_post_failure_branch")
        recommended_action = "do not use as split-B2 holdout; keep only diagnostic comparison"
    elif galaxy == "NGC4088":
        independent_status = "REFERENCE_ONLY_NOT_HOLDOUT"
        reason = "Original B2 reference case; useful for recovery limits, not independent transfer."
        blockers.append("reference_case")
        recommended_action = "use only as protocol reference and limit check"
    elif galaxy == "NGC5907":
        independent_status = "P0_PREDECLARED_SPLIT_B2_HOLDOUT_CANDIDATE_RHI_BLOCKED_OR_CAVEATED"
        reason = (
            "Strong residual-blind warp/projection evidence and accepted source fields exist, "
            "but SPARC RHI is zero/missing for the split-B2 normalized radial coordinate."
        )
        if srow["sparc_status"] == "SPARC_RHI_MISSING_OR_ZERO":
            blockers.append("sparc_rhi_missing_or_zero")
        if not has_numeric_warp:
            blockers.append("numeric_warp_activation_missing")
        if not source_rule_candidate:
            blockers.append("source_rule_candidate_false")
        denominator_policy = (
            "Acquire source-native HI/support radius, or predeclare a caveated optical-warp "
            "support denominator from the Sasaki 13.3-24.0 kpc source window before scoring."
        )
        recommended_action = (
            "build NGC5907 split-B2 denominator gate; if source-native denominator passes, "
            "freeze split-B2 formula before any scoring"
        )
    elif galaxy == "NGC4013":
        independent_status = "P1_RETROSPECTIVE_ANALOGUE_HAS_RHI_NOT_CLEAN_HOLDOUT"
        reason = (
            "Has SPARC RHI/Vflat and warp/vertical context, but current state is a reference/"
            "retrospective mixed case rather than a fresh independent split-B2 holdout."
        )
        blockers.extend(["retrospective_or_reference_case", "exact_b2_fields_incomplete"])
        recommended_action = "use as secondary analogue after a fresh residual-blind source freeze"
        denominator_policy = "SPARC_RHI_AVAILABLE"
    elif galaxy == "NGC4183":
        independent_status = "P1_SOURCE_ACQUISITION_REQUIRED_HAS_SPARC_RHI_VFLAT"
        reason = (
            "SPARC RHI/Vflat are available, but galaxy-specific warp/history source fields are "
            "not frozen."
        )
        blockers.extend(["source_acquisition_required", "numeric_warp_activation_missing"])
        recommended_action = "acquire source-native warp/history observables before formula freeze"
        denominator_policy = "SPARC_RHI_AVAILABLE_AFTER_SOURCE_GATE"
    else:
        independent_status = "P2_OR_UNASSESSED_BULK_CANDIDATE"
        reason = "Bulk candidate or unassessed row; not enough split-B2-specific source evidence."
        blockers.append("not_split_b2_prioritized")
        recommended_action = "route through source acquisition before split-B2 consideration"

    if not blockers and independent_status.startswith("P0"):
        endpoint_allowed = False
        blockers.append("formula_not_frozen_for_split_b2_holdout")

    return {
        "galaxy": galaxy,
        "split_b2_holdout_status": independent_status,
        "endpoint_scores_allowed": endpoint_allowed,
        "uses_vobs_or_residual_in_selection": False,
        "exact_b2_candidate_status": exact_status,
        "queue_priority": queue_priority,
        "candidate_role": queue_role,
        "candidate_mixed_readout": mixed_readout,
        "source_rule_candidate": source_rule_candidate,
        "has_numeric_warp_activation": has_numeric_warp,
        "has_overlay_context": has_overlay_context,
        **srow,
        "source_observable_names": source_observables,
        "source_citation_keys": citations,
        "blocking_or_caution_notes": notes,
        "split_b2_blockers": ";".join(blockers) if blockers else "none",
        "denominator_policy": denominator_policy,
        "reason": reason,
        "required_next_gate": next_gate,
        "recommended_next_action": recommended_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    exact = pd.read_csv(DATA / "ngc4088_b2_exact_transfer_candidates.csv")
    queue = pd.read_csv(DATA / "mixed_readout_candidate_acquisition_queue.csv")
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")

    galaxies = ["NGC5907", "NGC4013", "NGC4183", "NGC4088", "NGC7331"]
    candidates = pd.DataFrame(
        [candidate_from_sources(galaxy, exact, queue, sparc) for galaxy in galaxies]
    )

    rank_order = {
        "P0_PREDECLARED_SPLIT_B2_HOLDOUT_CANDIDATE_RHI_BLOCKED_OR_CAVEATED": 1,
        "P1_RETROSPECTIVE_ANALOGUE_HAS_RHI_NOT_CLEAN_HOLDOUT": 2,
        "P1_SOURCE_ACQUISITION_REQUIRED_HAS_SPARC_RHI_VFLAT": 3,
        "REFERENCE_ONLY_NOT_HOLDOUT": 4,
        "EXCLUDED_DIAGNOSTIC_ORIGIN": 5,
    }
    candidates["selector_rank"] = candidates["split_b2_holdout_status"].map(rank_order)
    candidates = candidates.sort_values(["selector_rank", "galaxy"]).reset_index(drop=True)

    summary = pd.DataFrame(
        [
            {
                "selector_status": "SPLIT_B2_INDEPENDENT_HOLDOUT_SELECTOR_COMPLETE_NOT_ENDPOINT",
                "n_candidates_reviewed": len(candidates),
                "top_candidate": str(candidates.iloc[0]["galaxy"]),
                "top_candidate_status": str(candidates.iloc[0]["split_b2_holdout_status"]),
                "top_blocker": str(candidates.iloc[0]["split_b2_blockers"]),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_selection": False,
                "recommended_next_gate": (
                    "NGC5907 split-B2 denominator/source-radius gate before formula freeze"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    action_items = pd.DataFrame(
        [
            {
                "priority": "P0",
                "galaxy": "NGC5907",
                "action": "resolve denominator",
                "details": (
                    "SPARC RHI is zero/missing; acquire source-native HI/support radius or "
                    "predeclare caveated optical-warp support denominator from 13.3-24.0 kpc."
                ),
                "endpoint_scores_allowed_after_action": False,
                "next_gate_after_action": "split-B2 formula freeze gate if denominator passes",
            },
            {
                "priority": "P1",
                "galaxy": "NGC4013",
                "action": "fresh residual-blind source freeze",
                "details": (
                    "Has RHI/Vflat but is not a clean split-B2 holdout until exact source fields "
                    "are re-frozen without using prior mixed endpoint information."
                ),
                "endpoint_scores_allowed_after_action": False,
                "next_gate_after_action": "secondary analogue freeze gate",
            },
            {
                "priority": "P1",
                "galaxy": "NGC4183",
                "action": "source acquisition",
                "details": (
                    "Has RHI/Vflat but lacks galaxy-specific warp/history activation fields."
                ),
                "endpoint_scores_allowed_after_action": False,
                "next_gate_after_action": "source acquisition and preflight gate",
            },
        ]
    )
    action_items["claim_boundary"] = CLAIM_BOUNDARY

    candidates.to_csv(DATA / "split_b2_independent_holdout_candidates.csv", index=False)
    summary.to_csv(DATA / "split_b2_independent_holdout_candidate_summary.csv", index=False)
    action_items.to_csv(DATA / "split_b2_independent_holdout_action_items.csv", index=False)

    report = f"""# Split-B2 Independent Holdout Candidate Selector

Status: `{summary.iloc[0]['selector_status']}`

This selector is a residual-blind candidate gate. It does not read observed
velocities, does not score endpoints, and does not promote the NGC7331
split-B2 repair as a same-curve result.

## Summary

{markdown_table(summary)}

## Candidate Ranking

{markdown_table(candidates[[
    'galaxy',
    'split_b2_holdout_status',
    'sparc_status',
    'sparc_vflat_km_s',
    'sparc_rhi_kpc',
    'has_numeric_warp_activation',
    'split_b2_blockers',
    'recommended_next_action',
]])}

## Action Items

{markdown_table(action_items)}

## Interpretation

NGC5907 is the best next split-B2 holdout candidate because it has strong
source-supported warp/projection evidence and a pre-existing mixed-readout
source-rule lane. It is not score-ready because the SPARC master row has
`RHI_kpc=0.0`, while the split-B2 normalized radial coordinate needs a frozen
outer support denominator.

NGC4013 is useful as a secondary analogue but is not a clean independent
holdout in the current state. NGC4183 is scientifically useful because SPARC
RHI and Vflat are available, but it needs galaxy-specific source acquisition.

NGC4088 remains the reference case. NGC7331 remains the diagnostic origin of
the split-B2 repair and must not be counted as an independent holdout endpoint.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    (REPORTS / "split_b2_independent_holdout_candidate_selector.md").write_text(
        report, encoding="utf-8"
    )

    print(summary.iloc[0]["selector_status"])
    print(candidates[["galaxy", "split_b2_holdout_status", "split_b2_blockers"]])


if __name__ == "__main__":
    main()
