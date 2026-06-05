#!/usr/bin/env python3
"""Build a residual-blind acquisition queue for additional mixed readouts.

The mixed population gate currently has one frozen prospective case. This
script identifies the next candidates from source-side evidence only. It does
not score rotations, does not read observed velocities, and does not promote an
endpoint label.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "mixed_readout_candidate_acquisition_queue_not_endpoint"


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


def safe_read(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value)


def first_value(df: pd.DataFrame, column: str, default: object = "") -> object:
    if df.empty or column not in df.columns:
        return default
    values = df[column].dropna()
    if values.empty:
        return default
    return values.iloc[0]


def has_positive_disk_scale(galaxy: str, sparc: pd.DataFrame, manifest: pd.DataFrame) -> tuple[bool, object]:
    sparc_rows = sparc.loc[sparc["Galaxy"].eq(galaxy)] if not sparc.empty else pd.DataFrame()
    if not sparc_rows.empty and "Rdisk_kpc" in sparc_rows.columns:
        value = sparc_rows.iloc[0]["Rdisk_kpc"]
        if pd.notna(value) and float(value) > 0:
            return True, float(value)

    manifest_rows = manifest.loc[manifest["galaxy"].eq(galaxy)] if not manifest.empty else pd.DataFrame()
    if not manifest_rows.empty and "scale_radius_proxy_kpc" in manifest_rows.columns:
        value = manifest_rows.iloc[0]["scale_radius_proxy_kpc"]
        if pd.notna(value) and float(value) > 0:
            return True, float(value)
    return False, ""


def values_for_galaxy(observables: pd.DataFrame, galaxy: str) -> pd.DataFrame:
    if observables.empty:
        return pd.DataFrame()
    return observables.loc[observables["galaxy"].eq(galaxy)].copy()


def audit_for_galaxy(audit: pd.DataFrame, galaxy: str) -> pd.Series | None:
    if audit.empty:
        return None
    rows = audit.loc[audit["galaxy"].eq(galaxy)]
    if rows.empty:
        return None
    return rows.iloc[0]


def source_rows_for_galaxy(ledger: pd.DataFrame, galaxy: str) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    return ledger.loc[ledger["galaxy"].eq(galaxy)].copy()


def obs_names(rows: pd.DataFrame) -> set[str]:
    if rows.empty or "observable_name" not in rows.columns:
        return set()
    return set(rows["observable_name"].dropna().astype(str))


def accepted_numeric_names(rows: pd.DataFrame) -> set[str]:
    if rows.empty:
        return set()
    status = rows["extraction_status"].astype(str) if "extraction_status" in rows.columns else ""
    mask = status.str.contains("ACCEPTED_NUMERIC", na=False)
    return set(rows.loc[mask, "observable_name"].dropna().astype(str))


def accepted_context_names(rows: pd.DataFrame) -> set[str]:
    if rows.empty:
        return set()
    status = rows["extraction_status"].astype(str) if "extraction_status" in rows.columns else ""
    mask = status.str.contains("ACCEPTED_CONTEXT|CAVEAT_CONTEXT", na=False)
    return set(rows.loc[mask, "observable_name"].dropna().astype(str))


def numeric_value(rows: pd.DataFrame, observable_name: str) -> object:
    selected = rows.loc[rows["observable_name"].astype(str).eq(observable_name)]
    return first_value(selected, "numeric_value", "")


def source_keys(rows: pd.DataFrame) -> str:
    if rows.empty or "citation_key" not in rows.columns:
        return ""
    return ";".join(rows["citation_key"].dropna().astype(str).unique())


def build_curated_candidate(
    galaxy: str,
    candidate_mixed_readout: str,
    candidate_priority: str,
    candidate_role: str,
    required_next_gate: str,
    observables: pd.DataFrame,
    audit: pd.DataFrame,
    ledger: pd.DataFrame,
    sparc: pd.DataFrame,
    manifest: pd.DataFrame,
    rationale: str,
    caution: str,
) -> dict[str, object]:
    rows = values_for_galaxy(observables, galaxy)
    audit_row = audit_for_galaxy(audit, galaxy)
    source_rows = source_rows_for_galaxy(ledger, galaxy)
    names = obs_names(rows)
    numeric_names = accepted_numeric_names(rows)
    context_names = accepted_context_names(rows)
    has_disk_scale, disk_scale = has_positive_disk_scale(galaxy, sparc, manifest)

    has_warp_numeric = bool(
        numeric_names
        & {
            "line_of_sight_warp_onset",
            "optical_warp_radial_range",
            "optical_warp_max_displacement",
            "x_warp_onset_value",
        }
    )
    has_vertical_numeric = bool(
        numeric_names
        & {
            "final_hi_scaleheight_central",
            "molecular_scaleheight_range",
            "edge_on_projected_hwhm",
        }
    )
    has_overlay_context = bool(
        context_names
        & {
            "rotational_lag_profile",
            "interaction_warp_context",
            "edge_on_vertical_structure_source",
            "possible_outer_warp_caveat",
            "whisp_lopsidedness_context",
        }
    )
    has_reclassification_pressure = bool(
        (audit_row is not None)
        and "reclassification" in text(audit_row.get("audit_decision", "")).lower()
    )

    source_rule_candidate = has_disk_scale and (has_warp_numeric or has_vertical_numeric) and (
        has_overlay_context or has_reclassification_pressure or has_warp_numeric
    )
    if galaxy == "NGC4013":
        source_rule_candidate = True

    blockers = []
    if not has_disk_scale:
        blockers.append("smooth_carrier_disk_scale_missing")
    if not (has_warp_numeric or has_vertical_numeric):
        blockers.append("numeric_overlay_activation_missing")
    if not (has_overlay_context or has_reclassification_pressure or has_warp_numeric):
        blockers.append("overlay_context_or_reclassification_missing")
    if galaxy == "NGC5907":
        blockers.append("already_projection_endpoint_requires_fresh_mixed_freeze")
    if galaxy == "NGC7331":
        blockers.append("outer_warp_caveat_requires_HI_projection_review")
    if galaxy == "NGC4183":
        blockers.append("context_only_not_galaxy_specific")
    if galaxy == "NGC4088":
        blockers.append("q_memory_epsilon_cross_review_not_accepted")

    audit_decision = text(audit_row.get("audit_decision", "NO_AUDIT_ROW")) if audit_row is not None else "NO_AUDIT_ROW"
    accepted = text(audit_row.get("accepted_observables", "")) if audit_row is not None else ""

    return {
        "galaxy": galaxy,
        "candidate_priority": candidate_priority,
        "candidate_role": candidate_role,
        "candidate_mixed_readout": candidate_mixed_readout,
        "source_rule_candidate": bool(source_rule_candidate),
        "has_smooth_disk_scale": bool(has_disk_scale),
        "disk_scale_kpc": disk_scale,
        "has_numeric_warp_activation": bool(has_warp_numeric),
        "has_numeric_vertical_activation": bool(has_vertical_numeric),
        "has_overlay_context": bool(has_overlay_context),
        "has_reclassification_pressure": bool(has_reclassification_pressure),
        "audit_decision": audit_decision,
        "accepted_or_support_observables": accepted,
        "source_observable_names": ";".join(sorted(names)),
        "source_citation_keys": source_keys(source_rows),
        "required_next_gate": required_next_gate,
        "blocking_or_caution_notes": ";".join(blockers) if blockers else caution,
        "endpoint_scores_allowed": False,
        "uses_vobs_or_residual_in_selection": False,
        "rationale": rationale,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_s4g75_acquisition_rows(
    s4g75: pd.DataFrame,
    sparc: pd.DataFrame,
    manifest: pd.DataFrame,
    already_listed: set[str],
) -> list[dict[str, object]]:
    if s4g75.empty:
        return []
    rows = []
    for _, row in s4g75.iterrows():
        galaxy = text(row["galaxy"])
        if galaxy in already_listed:
            continue
        family = text(row["formula_family"])
        driver = text(row["observable_driver_type"])
        source_priority = text(row["source_priority"])
        has_disk_scale, disk_scale = has_positive_disk_scale(galaxy, sparc, manifest)
        if "P0" not in source_priority:
            continue
        if "K_thick_flared" in family:
            candidate = "K_expdisk_thick_flared_overlay_review"
            role = "bulk_vertical_or_flare_mixed_acquisition_candidate"
        elif "K_scale_tail_spiral" in family:
            candidate = "K_expdisk_tail_or_outer_disk_overlay_review"
            role = "bulk_tail_or_outer_disk_mixed_acquisition_candidate"
        else:
            candidate = f"{family}_mixed_review"
            role = "bulk_mixed_acquisition_candidate"
        rows.append(
            {
                "galaxy": galaxy,
                "candidate_priority": "P2_BULK_SOURCE_ACQUISITION_REQUIRED",
                "candidate_role": role,
                "candidate_mixed_readout": candidate,
                "source_rule_candidate": False,
                "has_smooth_disk_scale": bool(has_disk_scale),
                "disk_scale_kpc": disk_scale,
                "has_numeric_warp_activation": False,
                "has_numeric_vertical_activation": False,
                "has_overlay_context": False,
                "has_reclassification_pressure": False,
                "audit_decision": "S4G75_DIRECT_SOURCE_NATIVE_ACQUISITION_ROW",
                "accepted_or_support_observables": "",
                "source_observable_names": text(row["required_observables"]),
                "source_citation_keys": text(row["required_source_families"]),
                "required_next_gate": "source_acquisition_and_extraction_before_formula_freeze",
                "blocking_or_caution_notes": text(row["endpoint_blocker"]),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_selection": False,
                "rationale": (
                    "P0 direct-source-native acquisition target; may become a mixed "
                    "candidate only after source-native overlay observables are acquired."
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    observables = safe_read(DATA / "readout_subfamily_extracted_observables.csv")
    audit = safe_read(DATA / "readout_subfamily_accepted_manifest_audit.csv")
    ledger = safe_read(DATA / "readout_subfamily_source_citation_ledger.csv")
    sparc = safe_read(DATA / "external_sparc_master_table.csv")
    manifest = safe_read(DATA / "morphology_parameter_manifest.csv")
    s4g75 = safe_read(DATA / "s4g75_direct_source_native_acquisition_manifest.csv")

    curated = [
        (
            "NGC4013",
            "K_expdisk_warp_vertical_overlay",
            "P0_REFERENCE_FROZEN_PROSPECTIVE_PROTOCOL",
            "already_frozen_mixed_reference_case_not_population_validation",
            "prospective_population_holdout_or_new_case_replication",
            "The existing source rule and formula freeze provide the mixed-readout reference case.",
            "not_retroactive_endpoint",
        ),
        (
            "NGC5907",
            "K_expdisk_projection_warp_vertical_overlay_review",
            "P0_FORMULA_FREEZE_CANDIDATE_REVIEW_REQUIRED",
            "strong_source_supported_projection_warp_candidate",
            "derive_fresh_mixed_formula_freeze_without_reusing_projection_endpoint_score",
            "Source evidence includes disk truncation/scale information, optical-warp geometry, interaction/warp context, and vertical/projection context.",
            "fresh_mixed_protocol_required",
        ),
        (
            "NGC7331",
            "K_expdisk_thick_outer_warp_overlay_review",
            "P1_CAVEATED_VERTICAL_OVERLAY_CANDIDATE",
            "vertical_thick_case_with_outer_warp_caveat",
            "resolve_outer_warp_caveat_and_map_h_over_Rs_before_freeze",
            "Source evidence gives vertical scale/thickness and inclination review, but an outer-warp caveat blocks unconditional promotion.",
            "caveated_vertical_case",
        ),
        (
            "NGC4183",
            "K_expdisk_bar_core_projection_history_overlay_review",
            "P1_SOURCE_ACQUISITION_REQUIRED",
            "context_only_projection_overlay_candidate",
            "acquire_galaxy_specific_overlay_observables",
            "Current WHISP source is method/context-level rather than a galaxy-specific NGC4183 extraction.",
            "source_specific_extraction_missing",
        ),
        (
            "NGC4088",
            "K_expdisk_warp_history_coupled_mixed_review",
            "P1_REVIEW_BLOCKED_HISTORY_WARP_CANDIDATE",
            "warp_history_case_with_unaccepted_q_memory_fields",
            "complete_independent_q_memory_epsilon_review_before_mixed_use",
            "Warp/history evidence is promising but the accepted endpoint-safe q, memory, and epsilon-cross fields remain blocked.",
            "q_memory_review_required",
        ),
    ]

    candidate_rows = [
        build_curated_candidate(
            galaxy,
            candidate,
            priority,
            role,
            next_gate,
            observables,
            audit,
            ledger,
            sparc,
            manifest,
            rationale,
            caution,
        )
        for galaxy, candidate, priority, role, next_gate, rationale, caution in curated
    ]
    listed = {row["galaxy"] for row in candidate_rows}
    candidate_rows.extend(build_s4g75_acquisition_rows(s4g75, sparc, manifest, listed))
    queue = pd.DataFrame(candidate_rows)

    priority_order = {
        "P0_REFERENCE_FROZEN_PROSPECTIVE_PROTOCOL": 0,
        "P0_FORMULA_FREEZE_CANDIDATE_REVIEW_REQUIRED": 1,
        "P1_CAVEATED_VERTICAL_OVERLAY_CANDIDATE": 2,
        "P1_SOURCE_ACQUISITION_REQUIRED": 3,
        "P1_REVIEW_BLOCKED_HISTORY_WARP_CANDIDATE": 4,
        "P2_BULK_SOURCE_ACQUISITION_REQUIRED": 5,
    }
    queue["_sort"] = queue["candidate_priority"].map(priority_order).fillna(99)
    queue = queue.sort_values(["_sort", "galaxy"]).drop(columns=["_sort"]).reset_index(drop=True)

    requirements = pd.DataFrame(
        [
            {
                "requirement_id": "MCAQ1_SOURCE_ONLY",
                "definition": "candidate ranking uses source ledgers, morphology manifests, SPARC scale metadata, and acquisition worklists only",
                "forbidden_inputs": "vobs; rotation residuals; RMSE ranks; required S_tau diagnostic family",
                "status": "PASS_BY_CONSTRUCTION",
            },
            {
                "requirement_id": "MCAQ2_FRESH_MIXED_FREEZE",
                "definition": "a candidate with a previous non-mixed endpoint must receive a fresh mixed formula-freeze before any mixed scoring",
                "forbidden_inputs": "reusing previous endpoint success as mixed-label evidence",
                "status": "REQUIRED_FOR_NGC5907_AND_ANY_SIMILAR_CASE",
            },
            {
                "requirement_id": "MCAQ3_MIN_POPULATION_CASES",
                "definition": "population validation requires at least three independent prospective mixed protocols",
                "forbidden_inputs": "counting retrospective diagnostic scores as prospective endpoints",
                "status": "CURRENTLY_BLOCKED",
            },
        ]
    )
    requirements["claim_boundary"] = CLAIM_BOUNDARY

    n_source_candidates = int(queue["source_rule_candidate"].sum())
    n_formula_candidates = int(
        queue["candidate_priority"].eq("P0_FORMULA_FREEZE_CANDIDATE_REVIEW_REQUIRED").sum()
    )
    n_reference = int(queue["candidate_priority"].eq("P0_REFERENCE_FROZEN_PROSPECTIVE_PROTOCOL").sum())
    n_needed_after_reference = max(0, 3 - n_reference)
    summary = pd.DataFrame(
        [
            {
                "queue_status": "MIXED_CANDIDATE_QUEUE_CREATED_NOT_ENDPOINT",
                "n_queue_rows": len(queue),
                "n_frozen_reference_cases": n_reference,
                "n_source_rule_candidate_rows": n_source_candidates,
                "n_p0_formula_freeze_candidates": n_formula_candidates,
                "min_prospective_mixed_protocols_required": 3,
                "additional_prospective_protocols_needed_after_reference": n_needed_after_reference,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_selection": False,
                "next_recommended_case": "NGC5907",
                "next_required_action": "build a fresh residual-blind mixed formula-freeze gate for NGC5907, or acquire/promote another source-rule-positive mixed candidate",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    queue.to_csv(DATA / "mixed_readout_candidate_acquisition_queue.csv", index=False)
    requirements.to_csv(DATA / "mixed_readout_candidate_acquisition_requirements.csv", index=False)
    summary.to_csv(DATA / "mixed_readout_candidate_acquisition_summary.csv", index=False)

    report = [
        "# Mixed Readout Candidate Acquisition Queue",
        "",
        "This report converts the mixed-population blocker into a residual-blind",
        "work queue. It does not score rotation curves, does not read observed",
        "velocity residuals, and does not promote endpoint labels.",
        "",
        "## Requirements",
        "",
        markdown_table(requirements),
        "",
        "## Candidate Queue",
        "",
        markdown_table(queue),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "NGC4013 remains the single frozen prospective mixed protocol and is not",
        "retrospective population validation. NGC5907 is the strongest next",
        "candidate because source-side evidence already contains disk-scale,",
        "warp/projection, and vertical/context information. Its prior projection",
        "endpoint cannot be reused as mixed evidence; it needs a fresh mixed",
        "formula-freeze gate before scoring. NGC7331 is useful but caveated,",
        "while NGC4183 and the S4G75 rows primarily define source-acquisition",
        "work rather than endpoint-ready cases.",
    ]
    (REPORTS / "mixed_readout_candidate_acquisition_queue.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
