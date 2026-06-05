#!/usr/bin/env python3
"""Audit extracted readout-subfamily observables for accepted-manifest use.

This gate promotes source fields only when they are residual-blind and concrete.
It may recommend a readout subfamily audit status, but it does not launch or
score rotation endpoints.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "readout_subfamily_accepted_manifest_audit_not_endpoint"


SUBFAMILY_RULES = {
    "K_disturbed_outer_tail": {
        "required": {"extended_hi_envelope_present", "outer_tail_transition_radius"},
        "support": {"hi_cloud_connection_or_tail_context", "sided_hole_age_asymmetry", "hi_holes_shells_count"},
        "fail_if_blocked": {"outer_tail_transition_radius", "hi_asymmetry_or_tail_measurement"},
        "accepted_label": "K_disturbed_outer_tail",
    },
    "K_projection_dominated": {
        "required": {"optical_warp_radial_range", "optical_warp_max_displacement"},
        "support": {"disk_truncation_scale_lengths", "interaction_warp_context", "edge_on_vertical_structure_source"},
        "fail_if_blocked": set(),
        "accepted_label": "K_projection_dominated",
    },
    "K_thick_regular": {
        "required": {"molecular_scaleheight_range", "edge_on_projected_hwhm", "inclination_review_range"},
        "support": set(),
        "caveat_if_present": {"possible_outer_warp_caveat"},
        "accepted_label": "K_thick_regular",
    },
    "K_expdisk_overlay": {
        "required": {"bar_core_projection_history_overlay"},
        "support": {"whisp_lopsidedness_context"},
        "fail_if_context_only": {"whisp_lopsidedness_context"},
        "accepted_label": "K_expdisk_overlay",
    },
    "K_true_compact": {
        "required": {"compact_support_radius", "bulge_core_decomposition"},
        "support": {"line_of_sight_warp_onset", "final_hi_scaleheight_central", "rotational_lag_profile"},
        "reclassification_pressure": {"compact_only_overlay_flag"},
        "accepted_label": "K_true_compact",
    },
    "K_warp_history_coupled": {
        "required": {
            "x_warp_onset_value",
            "q_warp_measured_first_pass",
            "m_history_warp_first_pass",
            "epsilon_cross_numeric_bound",
        },
        "support": {
            "orientation_mismatch_first_pass",
            "side_asymmetry_first_pass",
            "h4_interaction_context",
        },
        "fail_if_blocked": {"x_warp_onset_value", "epsilon_cross_numeric_bound"},
        "accepted_label": "K_warp_history_coupled",
    },
}


ACCEPTED_STATUSES = {
    "ACCEPTED_NUMERIC_SOURCE_FIELD",
    "ACCEPTED_CONTEXT_SOURCE_FIELD",
}


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def audit_group(group: pd.DataFrame) -> dict[str, object]:
    galaxy = group["galaxy"].iloc[0]
    subfamily = group["proposed_readout_subfamily"].iloc[0]
    rule = SUBFAMILY_RULES.get(subfamily, {})
    accepted = set(
        group.loc[group["extraction_status"].isin(ACCEPTED_STATUSES), "observable_name"]
    )
    caveat = set(group.loc[group["extraction_status"].str.contains("CAVEAT", na=False), "observable_name"])
    blocked = set(group.loc[group["extraction_status"].str.contains("BLOCKED", na=False), "observable_name"])
    context_only = set(
        group.loc[
            group["extraction_status"].str.contains("CONTEXT_ONLY_NOT_GALAXY_SPECIFIC", na=False),
            "observable_name",
        ]
    )
    reclass = set(
        group.loc[
            group["extraction_status"].str.contains("RECLASSIFICATION_PRESSURE", na=False),
            "observable_name",
        ]
    )
    required = set(rule.get("required", set()))
    support = set(rule.get("support", set()))
    missing_required = sorted(required - accepted)
    fail_blockers = sorted(blocked & set(rule.get("fail_if_blocked", set())))
    context_blockers = sorted(context_only & set(rule.get("fail_if_context_only", set())))
    caveat_hits = sorted(caveat | (accepted & set(rule.get("caveat_if_present", set()))))
    reclass_hits = sorted(reclass | (accepted & set(rule.get("reclassification_pressure", set()))))
    support_hits = sorted((accepted | context_only) & support)

    if reclass_hits:
        decision = "RECLASSIFICATION_REVIEW_REQUIRED"
        reason = "source evidence pressures the proposed subfamily toward an overlay/alternate readout review"
        accepted_label = False
        endpoint_eligible = False
    elif missing_required or fail_blockers or context_blockers:
        decision = "BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING"
        reason = "required subfamily observables are missing, blocked, or only method/context-level"
        accepted_label = False
        endpoint_eligible = False
    elif caveat_hits:
        decision = "CAVEATED_ACCEPTED_SOURCE_FIELDS_NOT_ENDPOINT_READY"
        reason = "required fields are present but caveats block unconditional subfamily acceptance"
        accepted_label = False
        endpoint_eligible = False
    else:
        decision = "ACCEPTED_SUBFAMILY_SOURCE_FIELDS_ENDPOINT_STILL_BLOCKED"
        reason = "required residual-blind source fields are present; endpoint remains blocked until frozen endpoint protocol"
        accepted_label = True
        endpoint_eligible = False

    return {
        "galaxy": galaxy,
        "proposed_readout_subfamily": subfamily,
        "accepted_label_candidate": rule.get("accepted_label", subfamily),
        "audit_decision": decision,
        "decision_reason": reason,
        "accepted_subfamily_label_promoted": accepted_label,
        "endpoint_eligible": endpoint_eligible,
        "accepted_observables": ";".join(sorted(accepted)),
        "support_observables": ";".join(support_hits),
        "missing_required_observables": ";".join(missing_required),
        "blocked_observables": ";".join(sorted(blocked)),
        "caveat_observables": ";".join(caveat_hits),
        "context_only_observables": ";".join(sorted(context_only)),
        "reclassification_pressure_observables": ";".join(reclass_hits),
        "n_extracted": len(group),
        "n_accepted_observables": len(accepted),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    extracted = pd.read_csv(DATA / "readout_subfamily_extracted_observables.csv")
    audit_rows = [
        audit_group(group)
        for _, group in extracted.groupby(["galaxy", "proposed_readout_subfamily"], sort=True)
    ]
    extracted_keys = {(row["galaxy"], row["proposed_readout_subfamily"]) for row in audit_rows}
    intake = pd.read_csv(DATA / "readout_subfamily_observable_intake_manifest.csv")
    for _, row in intake.iterrows():
        key = (row["galaxy"], row["proposed_readout_subfamily"])
        if key in extracted_keys:
            continue
        audit_rows.append(
            {
                "galaxy": row["galaxy"],
                "proposed_readout_subfamily": row["proposed_readout_subfamily"],
                "accepted_label_candidate": row["proposed_readout_subfamily"],
                "audit_decision": "NO_EXTRACTION_AVAILABLE",
                "decision_reason": "no cached-source observable extraction has been populated for this inspection row",
                "accepted_subfamily_label_promoted": False,
                "endpoint_eligible": False,
                "accepted_observables": "",
                "support_observables": "",
                "missing_required_observables": row.get("missing_for_acceptance", ""),
                "blocked_observables": "",
                "caveat_observables": "",
                "context_only_observables": "",
                "reclassification_pressure_observables": "",
                "n_extracted": 0,
                "n_accepted_observables": 0,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    audit = pd.DataFrame(
        audit_rows
    ).sort_values("galaxy")
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    audit.to_csv(DATA / "readout_subfamily_accepted_manifest_audit.csv", index=False)
    summary = (
        audit.groupby("audit_decision", as_index=False)
        .agg(
            n_galaxies=("galaxy", "size"),
            galaxies=("galaxy", lambda s: ";".join(s)),
            n_promoted=("accepted_subfamily_label_promoted", "sum"),
        )
        .sort_values("audit_decision")
    )
    summary.to_csv(DATA / "readout_subfamily_accepted_manifest_audit_summary.csv", index=False)
    report = [
        "# Readout-Subfamily Accepted-Manifest Audit",
        "",
        "This audit decides which extracted residual-blind source fields are strong",
        "enough for accepted-manifest use. It does not score endpoints and does not",
        "validate Tau Core.",
        "",
        "## Decision Summary",
        "",
        markdown_table(summary),
        "",
        "## Galaxy Decisions",
        "",
        markdown_table(
            audit[
                [
                    "galaxy",
                    "proposed_readout_subfamily",
                    "audit_decision",
                    "accepted_subfamily_label_promoted",
                    "accepted_observables",
                    "missing_required_observables",
                    "caveat_observables",
                    "reclassification_pressure_observables",
                    "claim_boundary",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "Accepted source fields are not endpoint validation. A promoted subfamily",
        "label in this audit only means that the required residual-blind source",
        "observables for that subfamily are present in the cached literature layer.",
        "Endpoint scoring remains blocked.",
        "",
    ]
    (REPORTS / "readout_subfamily_accepted_manifest_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
