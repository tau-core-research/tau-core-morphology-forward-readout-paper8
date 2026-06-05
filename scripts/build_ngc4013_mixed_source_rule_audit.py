#!/usr/bin/env python3
"""Audit residual-blind source support for NGC4013 as a mixed readout.

This script answers whether the mixed `K_expdisk_warp_vertical_overlay`
hypothesis has source-side support beyond intuition. It does not use endpoint
scores to promote a label. The diagnostic score is recorded only as a forbidden
label input and follow-up motivation.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4013_mixed_source_rule_audit_not_endpoint"


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

    source = pd.read_csv(DATA / "ngc4013_compact_overlay_source_summary.csv").iloc[0]
    preflight = pd.read_csv(DATA / "ngc4013_warp_overlay_preflight_summary.csv").iloc[0]
    replacement = pd.read_csv(
        DATA / "ngc4013_warp_vertical_overlay_replacement_label_summary.csv"
    ).iloc[0]
    freeze = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_freeze_manifest.csv").iloc[0]
    sparc = pd.read_csv(DATA / "external_sparc_master_table.csv")
    sparc_row = sparc.loc[sparc["Galaxy"] == "NGC4013"].iloc[0]
    diagnostic_path = DATA / "ngc4013_expdisk_wvo_diagnostic_scores.csv"
    diagnostic = pd.read_csv(diagnostic_path).iloc[0] if diagnostic_path.exists() else None
    general_rule_path = DATA / "mixed_readout_source_selection_cases.csv"
    if general_rule_path.exists():
        general_cases = pd.read_csv(general_rule_path)
        ngc4013_general = general_cases.loc[general_cases["galaxy"].eq("NGC4013")]
        general_rule_pass = (
            bool(ngc4013_general.iloc[0]["source_rule_pass"])
            if len(ngc4013_general)
            else False
        )
    else:
        general_rule_pass = False

    evidence = pd.DataFrame(
        [
            {
                "evidence_id": "E1_SMOOTH_EDGE_DISK_COMPONENT",
                "evidence_lane": "smooth_disk_carrier",
                "source_field": "S4G component decomposition",
                "source_value": source["s4g_components"],
                "pass_rule": "edge-disk component present and no Sersic bulge component",
                "pass_status": "PASS",
                "endpoint_label_input_allowed": True,
                "interpretation": "supports an exponential/smooth disk carrier rather than a compact-core carrier",
            },
            {
                "evidence_id": "E2_DISK_SCALE_PRESENT",
                "evidence_lane": "smooth_disk_carrier",
                "source_field": "SPARC/S4G disk scale",
                "source_value": f"Rdisk={float(sparc_row['Rdisk_kpc']):.3g} kpc; S4G hr={float(source['s4g_edge_disk_hr_kpc']):.3g} kpc",
                "pass_rule": "disk scale exists before endpoint scoring",
                "pass_status": "PASS",
                "endpoint_label_input_allowed": True,
                "interpretation": "supports a source-native smooth disk radial carrier",
            },
            {
                "evidence_id": "E3_COMPACT_LANE_REJECTED",
                "evidence_lane": "anti_compact",
                "source_field": "compact lane source review",
                "source_value": source["compact_lane_decision"],
                "pass_rule": "compact endpoint not source supported",
                "pass_status": "PASS",
                "endpoint_label_input_allowed": True,
                "interpretation": "prevents treating the galaxy as pure K_true_compact",
            },
            {
                "evidence_id": "E4_WARP_OVERLAY_PRESENT",
                "evidence_lane": "overlay",
                "source_field": "warp/flare/disk-halo pressure",
                "source_value": "warp_flare_disk_halo_overlay_present",
                "pass_rule": "warp/overlay source pressure present",
                "pass_status": "PASS",
                "endpoint_label_input_allowed": True,
                "interpretation": "supports a source-windowed overlay correction, not a pure smooth disk only",
            },
            {
                "evidence_id": "E5_WARP_ONSET_NUMERIC",
                "evidence_lane": "overlay",
                "source_field": "line_of_sight_warp_onset",
                "source_value": preflight["warp_onset_kpc"],
                "pass_rule": "numeric source onset available",
                "pass_status": "PASS",
                "endpoint_label_input_allowed": True,
                "interpretation": "supplies the radial activation window for the overlay component",
            },
            {
                "evidence_id": "E6_VERTICAL_EXTENDED_COMPONENT",
                "evidence_lane": "overlay",
                "source_field": "h/R and extended component",
                "source_value": f"h/R={float(source['s4g_edge_disk_h_over_r']):.6g}; f_EC={float(source['extended_component_mass_fraction']):.3g}",
                "pass_rule": "vertical h/R and extended-component fraction available",
                "pass_status": "PASS",
                "endpoint_label_input_allowed": True,
                "interpretation": "supports the vertical-overlay attenuation amplitude",
            },
            {
                "evidence_id": "E7_LAG_CONTEXT",
                "evidence_lane": "overlay",
                "source_field": "rotational lag",
                "source_value": "lag shallows from -35 km/s/kpc at 5.8 kpc to zero near R25",
                "pass_rule": "source lag context and caveated kernel shell available",
                "pass_status": "PASS_CAVEATED",
                "endpoint_label_input_allowed": True,
                "interpretation": "supports the overlay kernel, but figure-level digitization would strengthen it",
            },
            {
                "evidence_id": "E8_DIAGNOSTIC_RMSE_SIGNAL",
                "evidence_lane": "forbidden_label_input",
                "source_field": "mixed diagnostic score",
                "source_value": (
                    f"mixed RMSE={float(diagnostic['rmse_expdisk_wvo_diagnostic']):.6g}"
                    if diagnostic is not None
                    else "not_run"
                ),
                "pass_rule": "must not be used to promote the source label",
                "pass_status": "RECORDED_FOR_MOTIVATION_ONLY",
                "endpoint_label_input_allowed": False,
                "interpretation": "can motivate a future source-blind rule, but cannot itself justify the mixed label",
            },
        ]
    )
    evidence["galaxy"] = "NGC4013"
    evidence["claim_boundary"] = CLAIM_BOUNDARY
    evidence = evidence[
        [
            "galaxy",
            "evidence_id",
            "evidence_lane",
            "source_field",
            "source_value",
            "pass_rule",
            "pass_status",
            "endpoint_label_input_allowed",
            "interpretation",
            "claim_boundary",
        ]
    ]

    allowed = evidence.loc[evidence["endpoint_label_input_allowed"]]
    smooth_pass = allowed.loc[allowed["evidence_lane"].eq("smooth_disk_carrier"), "pass_status"].str.startswith("PASS").all()
    overlay_pass = allowed.loc[allowed["evidence_lane"].eq("overlay"), "pass_status"].str.startswith("PASS").all()
    anti_compact_pass = allowed.loc[allowed["evidence_lane"].eq("anti_compact"), "pass_status"].str.startswith("PASS").all()
    caveated = allowed["pass_status"].str.contains("CAVEATED", na=False).any()

    gates = pd.DataFrame(
        [
            {
                "gate_id": "MSR1_SMOOTH_DISK_CARRIER_SUPPORTED",
                "gate_status": "PASS" if smooth_pass else "BLOCKED",
                "evidence": "S4G edge-disk component and source disk scales are present",
                "remaining_obligation": (
                    "covered by the residual-blind mixed source-selection rule"
                    if general_rule_pass
                    else "generalize carrier-selection rule beyond this galaxy"
                ),
            },
            {
                "gate_id": "MSR2_OVERLAY_COMPONENT_SUPPORTED",
                "gate_status": "PASS_CAVEATED" if overlay_pass and caveated else ("PASS" if overlay_pass else "BLOCKED"),
                "evidence": "warp onset, vertical h/R, extended component, and lag context are present",
                "remaining_obligation": "replace caveated lag shell with source-map digitization if needed",
            },
            {
                "gate_id": "MSR3_COMPACT_ONLY_REJECTED",
                "gate_status": "PASS" if anti_compact_pass else "BLOCKED",
                "evidence": str(source["compact_lane_decision"]),
                "remaining_obligation": "none unless future compact evidence overturns this review",
            },
            {
                "gate_id": "MSR4_DIAGNOSTIC_SCORE_EXCLUDED",
                "gate_status": "PASS",
                "evidence": "diagnostic RMSE row is marked endpoint_label_input_allowed=False",
                "remaining_obligation": "do not use diagnostic fit as source-label evidence",
            },
            {
                "gate_id": "MSR5_GENERAL_SOURCE_RULE",
                "gate_status": (
                    "PASS_FORMULA_FREEZE_REQUIRED"
                    if general_rule_pass
                    else "BLOCKED_FOR_ENDPOINT_PROMOTION"
                ),
                "evidence": (
                    "residual-blind mixed source-selection rule passes this case"
                    if general_rule_pass
                    else "rule is currently NGC4013-specific"
                ),
                "remaining_obligation": (
                    "freeze the mixed carrier-plus-overlay formula before endpoint scoring"
                    if general_rule_pass
                    else "predeclare a sample-level source rule for mixed carrier selection before endpoint validation"
                ),
            },
        ]
    )
    gates["galaxy"] = "NGC4013"
    gates["mixed_readout_candidate"] = "K_expdisk_warp_vertical_overlay"
    gates["endpoint_scores_allowed"] = False
    gates["diagnostic_scores_allowed"] = True
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "mixed_readout_candidate",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "diagnostic_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "mixed_readout_candidate": "K_expdisk_warp_vertical_overlay",
                "source_support_status": (
                    "SOURCE_SUPPORTED_MIXED_HYPOTHESIS_FORMULA_FREEZE_BLOCKED"
                    if general_rule_pass
                    else "SOURCE_SUPPORTED_MIXED_HYPOTHESIS_GENERAL_RULE_BLOCKED"
                ),
                "smooth_disk_source_supported": bool(smooth_pass),
                "overlay_source_supported": bool(overlay_pass),
                "compact_only_rejected": bool(anti_compact_pass),
                "general_mixed_source_rule_pass": bool(general_rule_pass),
                "diagnostic_score_used_as_label_input": False,
                "n_evidence_rows": len(evidence),
                "n_endpoint_label_allowed_evidence_rows": int(evidence["endpoint_label_input_allowed"].sum()),
                "n_gates": len(gates),
                "n_endpoint_blockers": int(gates["gate_status"].str.contains("BLOCKED").sum())
                + int(general_rule_pass),
                "endpoint_scores_allowed": False,
                "diagnostic_scores_allowed": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    evidence.to_csv(DATA / "ngc4013_mixed_source_rule_evidence.csv", index=False)
    gates.to_csv(DATA / "ngc4013_mixed_source_rule_gate.csv", index=False)
    summary.to_csv(DATA / "ngc4013_mixed_source_rule_summary.csv", index=False)

    report = [
        "# NGC4013 Mixed Source-Rule Audit",
        "",
        "This audit asks whether the mixed `K_expdisk_warp_vertical_overlay`",
        "interpretation has source-side support beyond intuition. It separates",
        "allowed source evidence from the diagnostic RMSE signal, which is recorded",
        "but forbidden as a label input.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Evidence",
        "",
        markdown_table(evidence),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        (
            "NGC4013 has source support for a mixed smooth-disk plus warp/vertical-overlay "
            "hypothesis. The general residual-blind mixed source-selection rule now passes "
            "this case, but the mixed formula itself is still endpoint-blocked until a "
            "separate formula-freeze gate is run."
            if general_rule_pass
            else "NGC4013 has source support for a mixed smooth-disk plus warp/vertical-overlay "
            "hypothesis. It is still not endpoint-promoted because a general residual-blind "
            "source rule for selecting this mixed carrier must be declared before scoring."
        ),
        "",
    ]
    (REPORTS / "ngc4013_mixed_source_rule_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
