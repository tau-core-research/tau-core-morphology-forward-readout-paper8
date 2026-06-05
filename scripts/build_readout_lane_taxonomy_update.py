#!/usr/bin/env python3
"""Build a readout-lane taxonomy update after the split-B2 holdout audit.

The existing subfamily registry distinguishes projected morphology families.
This update adds the higher-level readout lane distinction needed by the
NGC7331/NGC5907 split-B2 contrast:

    - added source/readout lane,
    - bounded projection/attenuation lane,
    - mixed smooth-carrier + overlay lane,
    - clean carrier lane.

No endpoint is scored here and no formula is tuned.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "readout_lane_taxonomy_update_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    subfamily_registry = pd.read_csv(DATA / "readout_subfamily_registry.csv")
    accepted_audit = pd.read_csv(DATA / "readout_subfamily_accepted_manifest_audit.csv")
    split_synthesis = pd.read_csv(DATA / "split_b2_lane_specificity_summary.csv").iloc[0]
    split_cases = pd.read_csv(DATA / "split_b2_lane_specificity_cases.csv")
    ngc5907_failure = pd.read_csv(DATA / "ngc5907_split_b2_failure_mode_summary.csv").iloc[0]

    lanes = pd.DataFrame(
        [
            {
                "readout_lane": "L_added_source",
                "core_interpretation": (
                    "morphology/history source adds a velocity-squared response on top of a carrier"
                ),
                "typical_formula_shell": (
                    "v_readout^2 = v_carrier^2 + lambda_K K(R)"
                ),
                "required_residual_blind_evidence": (
                    "warp/history source activation; source-load rule; bounded support or tail window; sign rule"
                ),
                "positive_reference": "NGC7331 diagnostic only; NGC4088 targeted warp/history diagnostics",
                "negative_reference": "NGC5907 split-B2 caveated holdout",
                "current_status": "LANE_CANDIDATE_NOT_UNIVERSAL",
            },
            {
                "readout_lane": "L_projection_attenuation",
                "core_interpretation": (
                    "observed 4D readout is dominated by projection/deprojection/attenuation of a carrier"
                ),
                "typical_formula_shell": (
                    "v_readout^2 = v_carrier^2 (1 - gamma_K K_proj(R))"
                ),
                "required_residual_blind_evidence": (
                    "edge-on/projection geometry; warp window; vertical or dust/projection context; velocity-field sanity"
                ),
                "positive_reference": "NGC5907 projection accepted endpoint context",
                "negative_reference": "standalone added split-B2 fails on NGC5907",
                "current_status": "SUPPORTED_FOR_NGC5907_CONTEXT_NOT_POPULATION_VALIDATED",
            },
            {
                "readout_lane": "L_mixed_overlay",
                "core_interpretation": (
                    "smooth carrier remains active while an overlay source-window modifies the readout"
                ),
                "typical_formula_shell": (
                    "v_mix^2 = v_smooth^2 +/or * overlay(K_source)"
                ),
                "required_residual_blind_evidence": (
                    "smooth disk/decomposition scale plus warp/projection/vertical/bar/history overlay observables"
                ),
                "positive_reference": "NGC5907 mixed projection context; NGC4013 mixed reference path",
                "negative_reference": "requires anti-residual source rule before scoring",
                "current_status": "PROTOCOL_READY_FOR_SOURCE_RULE_CASES",
            },
            {
                "readout_lane": "L_clean_carrier",
                "core_interpretation": (
                    "baseline-like carrier already captures the readout when morphology is regular/stable"
                ),
                "typical_formula_shell": "v_readout = v_carrier",
                "required_residual_blind_evidence": (
                    "low disturbance evidence; no strong projection/history/overlay activation; stable present morphology"
                ),
                "positive_reference": "baseline-strong galaxies in Paper 8 controls",
                "negative_reference": "fails where source-windowed overlay evidence is strong",
                "current_status": "OPEN_CONTROL_LANE",
            },
        ]
    )
    lanes["endpoint_scores_allowed"] = False
    lanes["claim_boundary"] = CLAIM_BOUNDARY

    subfamily_lane_map = pd.DataFrame(
        [
            {
                "subfamily": "K_warp_history_coupled",
                "primary_lane": "L_added_source",
                "secondary_lane": "L_mixed_overlay",
                "selection_rule": (
                    "use added lane only when source fields imply a real source-load/history term; "
                    "otherwise treat as mixed/blocked"
                ),
            },
            {
                "subfamily": "K_projection_dominated",
                "primary_lane": "L_projection_attenuation",
                "secondary_lane": "L_mixed_overlay",
                "selection_rule": (
                    "projection evidence selects bounded attenuation, not added source ramp"
                ),
            },
            {
                "subfamily": "K_expdisk_overlay",
                "primary_lane": "L_mixed_overlay",
                "secondary_lane": "L_clean_carrier",
                "selection_rule": (
                    "smooth disk carrier plus overlay evidence; reject if overlay has no source field"
                ),
            },
            {
                "subfamily": "K_clean_expdisk",
                "primary_lane": "L_clean_carrier",
                "secondary_lane": "L_mixed_overlay",
                "selection_rule": (
                    "clean carrier unless source-blind overlay/projection/history evidence is present"
                ),
            },
            {
                "subfamily": "K_thick_regular",
                "primary_lane": "L_clean_carrier",
                "secondary_lane": "L_projection_attenuation",
                "selection_rule": (
                    "regular vertical thickness is carrier-like unless edge-on/projection caveat dominates"
                ),
            },
            {
                "subfamily": "K_flared_outer_disk",
                "primary_lane": "L_mixed_overlay",
                "secondary_lane": "L_projection_attenuation",
                "selection_rule": (
                    "outer flare modifies carrier; projection lane if geometry dominates source fields"
                ),
            },
            {
                "subfamily": "K_smooth_n2_tail",
                "primary_lane": "L_added_source",
                "secondary_lane": "L_clean_carrier",
                "selection_rule": (
                    "tail/source support may add a TGP-like term if source window and amplitude are frozen"
                ),
            },
            {
                "subfamily": "K_disturbed_outer_tail",
                "primary_lane": "L_added_source",
                "secondary_lane": "L_mixed_overlay",
                "selection_rule": (
                    "disturbed tails require asymmetry/history source evidence and bounded support"
                ),
            },
            {
                "subfamily": "K_true_compact",
                "primary_lane": "L_clean_carrier",
                "secondary_lane": "L_mixed_overlay",
                "selection_rule": (
                    "compact lane only with source-supported compact support; otherwise compact+disk overlay"
                ),
            },
            {
                "subfamily": "K_compact_plus_disk",
                "primary_lane": "L_mixed_overlay",
                "secondary_lane": "L_clean_carrier",
                "selection_rule": (
                    "compact and disk supports both active; freeze decomposition before scoring"
                ),
            },
        ]
    )
    subfamily_lane_map["endpoint_scores_allowed"] = False
    subfamily_lane_map["claim_boundary"] = CLAIM_BOUNDARY

    case_updates = pd.DataFrame(
        [
            {
                "galaxy": "NGC7331",
                "new_lane_status": "SAME_CURVE_ADDED_SOURCE_DIAGNOSTIC_ONLY",
                "assigned_lane_for_claims": "L_added_source_diagnostic_not_endpoint",
                "evidence": (
                    "split-B2 unit-load improves q-role diagnostic but branch was identified on same curve"
                ),
                "claim_allowed": (
                    "diagnostic q-role/source-load repair; not independent validation"
                ),
            },
            {
                "galaxy": "NGC5907",
                "new_lane_status": "PROJECTION_LANE_FAVORED_ADDED_SOURCE_REJECTED",
                "assigned_lane_for_claims": "L_projection_attenuation",
                "evidence": str(ngc5907_failure["primary_interpretation"]),
                "claim_allowed": (
                    "negative split-B2 control plus projection/TPG-like lane preference"
                ),
            },
            {
                "galaxy": "NGC4013",
                "new_lane_status": "MIXED_ANALOGUE_REQUIRES_FRESH_SOURCE_FREEZE",
                "assigned_lane_for_claims": "L_mixed_overlay_pending",
                "evidence": (
                    "existing mixed reference path is retrospective; needs fresh residual-blind source freeze"
                ),
                "claim_allowed": "secondary analogue only, not clean holdout yet",
            },
            {
                "galaxy": "NGC4183",
                "new_lane_status": "SOURCE_ACQUISITION_REQUIRED",
                "assigned_lane_for_claims": "lane_unassigned",
                "evidence": (
                    "SPARC RHI/Vflat available but galaxy-specific activation fields missing"
                ),
                "claim_allowed": "none before source acquisition",
            },
        ]
    )
    case_updates["endpoint_scores_allowed"] = False
    case_updates["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "RLTU_G1_SPLIT_B2_UNIVERSALITY",
                "gate_status": str(split_synthesis["universal_split_b2_rule_status"]),
                "evidence": "NGC7331 positive diagnostic and NGC5907 negative holdout",
                "consequence": "do not use split-B2 as a universal forward readout formula",
            },
            {
                "gate_id": "RLTU_G2_LANE_SPECIFICITY",
                "gate_status": str(split_synthesis["lane_specificity_status"]),
                "evidence": "same evidence supports lane-specific interpretation",
                "consequence": "freeze readout lane before formula scoring",
            },
            {
                "gate_id": "RLTU_G3_PROJECTION_VS_ADDED_SEPARATION",
                "gate_status": "PASS",
                "evidence": (
                    "NGC5907 projection/TPG-like readouts are strong while added split-B2 is weak"
                ),
                "consequence": (
                    "projection-dominated source evidence should veto standalone added-ramp transfer"
                ),
            },
            {
                "gate_id": "RLTU_G4_SUBFAMILY_LINK",
                "gate_status": "PASS_CAVEATED",
                "evidence": (
                    "subfamily registry mapped to lane taxonomy; source rules still incomplete"
                ),
                "consequence": "subfamily acceptance must now also declare a readout lane",
            },
            {
                "gate_id": "RLTU_G5_ENDPOINT_USE",
                "gate_status": "BLOCKED",
                "evidence": "taxonomy update only; no new endpoint protocol frozen",
                "consequence": "future scoring requires lane freeze plus formula freeze",
            },
        ]
    )
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    merged_registry = subfamily_registry.merge(
        subfamily_lane_map[
            ["subfamily", "primary_lane", "secondary_lane", "selection_rule"]
        ],
        on="subfamily",
        how="left",
    )
    merged_registry["lane_mapping_status"] = merged_registry["primary_lane"].map(
        lambda value: "MAPPED" if isinstance(value, str) and value else "MISSING"
    )
    merged_registry["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "taxonomy_update_status": "READOUT_LANE_TAXONOMY_UPDATE_COMPLETE_NOT_ENDPOINT",
                "n_lanes": len(lanes),
                "n_subfamilies_mapped": int(
                    merged_registry["lane_mapping_status"].eq("MAPPED").sum()
                ),
                "universal_split_b2_rule_status": str(
                    split_synthesis["universal_split_b2_rule_status"]
                ),
                "lane_specificity_status": str(split_synthesis["lane_specificity_status"]),
                "endpoint_scores_allowed": False,
                "formula_tuned": False,
                "recommended_next_gate": (
                    "readout-lane freeze gate for each candidate galaxy before formula scoring"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    lanes.to_csv(DATA / "readout_lane_taxonomy_lanes.csv", index=False)
    subfamily_lane_map.to_csv(DATA / "readout_lane_taxonomy_subfamily_map.csv", index=False)
    merged_registry.to_csv(DATA / "readout_lane_taxonomy_registry_update.csv", index=False)
    case_updates.to_csv(DATA / "readout_lane_taxonomy_case_updates.csv", index=False)
    gates.to_csv(DATA / "readout_lane_taxonomy_gates.csv", index=False)
    summary.to_csv(DATA / "readout_lane_taxonomy_summary.csv", index=False)

    report = f"""# Readout-Lane Taxonomy Update

Status: `{summary.iloc[0]['taxonomy_update_status']}`

This update adds a readout-lane layer above the existing morphology subfamily
registry. It incorporates the NGC7331/NGC5907 split-B2 contrast without tuning
any formula.

## Summary

{markdown_table(summary)}

## Readout Lanes

{markdown_table(lanes)}

## Subfamily to Lane Map

{markdown_table(subfamily_lane_map)}

## Case Updates

{markdown_table(case_updates)}

## Gates

{markdown_table(gates)}

## Interpretation

The taxonomy now separates source-added readouts from projection/attenuation
readouts. This is the main lesson of the split-B2 audit: NGC7331 supports a
same-curve source-load diagnostic, while NGC5907 rejects the added split-B2
lane and favors projection/TPG-like behavior. Therefore future endpoint work
must freeze the readout lane before freezing the formula.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    (REPORTS / "readout_lane_taxonomy_update.md").write_text(report, encoding="utf-8")

    print(summary.to_string(index=False))
    print(case_updates[["galaxy", "new_lane_status", "assigned_lane_for_claims"]].to_string(index=False))


if __name__ == "__main__":
    main()
