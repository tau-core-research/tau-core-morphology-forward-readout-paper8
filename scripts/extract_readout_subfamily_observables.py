#!/usr/bin/env python3
"""Extract residual-blind observables from cached readout-subfamily sources.

This is a source-review extraction layer. It records concrete observables,
units, line references into local text caches, and promotion status. It does
not use endpoint residuals and does not promote accepted morphology labels.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
LITERATURE = ROOT / "data" / "external" / "literature"
CLAIM_BOUNDARY = "source_extraction_not_endpoint_label_acceptance"


EXTRACTIONS = [
    {
        "galaxy": "IC2574",
        "proposed_readout_subfamily": "K_disturbed_outer_tail",
        "evidence_id": "hi_asymmetry_map",
        "observable_name": "extended_hi_envelope_present",
        "observable_value": "true",
        "observable_unit": "boolean",
        "numeric_value": "",
        "source_file": "ic2574_deblok_2020_m81_hi_survey.txt",
        "source_line_refs": "20-29;392-395;544-545",
        "source_extraction": "Deep HI observations map an extended HI envelope around IC2574.",
        "extraction_status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
        "acceptance_use": "supports disturbed-gas/envelope review; not a complete tail-transition radius",
    },
    {
        "galaxy": "IC2574",
        "proposed_readout_subfamily": "K_disturbed_outer_tail",
        "evidence_id": "outer_tail_transition",
        "observable_name": "hi_cloud_connection_or_tail_context",
        "observable_value": "HIJASS_J1021+68_clouds_connected_to_IC2574_envelope",
        "observable_unit": "categorical",
        "numeric_value": "",
        "source_file": "ic2574_deblok_2020_m81_hi_survey.txt",
        "source_line_refs": "20-29;1017-1027",
        "source_extraction": "The HI complex is interpreted as clouds stripped from or falling onto the IC2574 envelope.",
        "extraction_status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
        "acceptance_use": "supports morphology-history/tail context; exact transition radius still missing",
    },
    {
        "galaxy": "IC2574",
        "proposed_readout_subfamily": "K_disturbed_outer_tail",
        "evidence_id": "outer_tail_transition",
        "observable_name": "outer_tail_transition_radius",
        "observable_value": "not_reported_in_extracted_text",
        "observable_unit": "kpc",
        "numeric_value": "",
        "source_file": "ic2574_deblok_2020_m81_hi_survey.txt",
        "source_line_refs": "20-29",
        "source_extraction": "The source supports an extended envelope but does not give the subfamily tail-onset radius in the extracted text.",
        "extraction_status": "BLOCKED_NEEDS_MEASUREMENT",
        "acceptance_use": "needs map/profile extraction before numeric kernel use",
    },
    {
        "galaxy": "IC2574",
        "proposed_readout_subfamily": "K_disturbed_outer_tail",
        "evidence_id": "environment_history",
        "observable_name": "hi_holes_shells_count",
        "observable_value": "48",
        "observable_unit": "count",
        "numeric_value": "48",
        "source_file": "ic2574_walter_brinks_1999_hi_holes_shells.txt",
        "source_line_refs": "17-29",
        "source_extraction": "VLA HI observations report 48 mostly expanding HI shells and holes.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports morphology-memory/disturbed-ISM source layer",
    },
    {
        "galaxy": "IC2574",
        "proposed_readout_subfamily": "K_disturbed_outer_tail",
        "evidence_id": "environment_history",
        "observable_name": "hi_layer_scaleheight",
        "observable_value": "350",
        "observable_unit": "pc",
        "numeric_value": "350",
        "source_file": "ic2574_walter_brinks_1999_hi_holes_shells.txt",
        "source_line_refs": "47-49",
        "source_extraction": "The HI layer scaleheight is reported at about 350 pc.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports disturbed/thick gas context, not by itself a tail label",
    },
    {
        "galaxy": "IC2574",
        "proposed_readout_subfamily": "K_disturbed_outer_tail",
        "evidence_id": "outer_tail_transition",
        "observable_name": "sided_hole_age_asymmetry",
        "observable_value": "receding_and_approaching_age_distributions_differ",
        "observable_unit": "categorical",
        "numeric_value": "",
        "source_file": "ic2574_sanchez_salcedo_hidalgo_gamez_2002_holes.html",
        "source_line_refs": "html-meta-description",
        "source_extraction": "The source reports asymmetric hole ages, photometric properties, and HI mass between the two sides.",
        "extraction_status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
        "acceptance_use": "supports asymmetry context; no radius extracted",
    },
    {
        "galaxy": "NGC4013",
        "proposed_readout_subfamily": "K_true_compact",
        "evidence_id": "disk_overlay_check",
        "observable_name": "compact_only_overlay_flag",
        "observable_value": "warp_flare_disk_halo_overlay_present",
        "observable_unit": "categorical",
        "numeric_value": "",
        "source_file": "ngc4013_zschaechner_rand_2015_hi_kinematics.txt",
        "source_line_refs": "13-23;126-128;170-172",
        "source_extraction": "NGC4013 is described as distinctly/substantially warped with disk-halo activity.",
        "extraction_status": "RECLASSIFICATION_PRESSURE_SOURCE_FIELD",
        "acceptance_use": "warns that K_true_compact needs overlay or rejection before endpoint use",
    },
    {
        "galaxy": "NGC4013",
        "proposed_readout_subfamily": "K_true_compact",
        "evidence_id": "disk_overlay_check",
        "observable_name": "line_of_sight_warp_onset",
        "observable_value": "10",
        "observable_unit": "kpc",
        "numeric_value": "10",
        "source_file": "ngc4013_zschaechner_rand_2015_hi_kinematics.txt",
        "source_line_refs": "406-409",
        "source_extraction": "The line-of-sight warp component begins near 1.2 arcmin, about 10 kpc.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports disk/warp overlay review",
    },
    {
        "galaxy": "NGC4013",
        "proposed_readout_subfamily": "K_true_compact",
        "evidence_id": "disk_overlay_check",
        "observable_name": "final_hi_scaleheight_central",
        "observable_value": "210",
        "observable_unit": "pc",
        "numeric_value": "210",
        "source_file": "ngc4013_zschaechner_rand_2015_hi_kinematics.txt",
        "source_line_refs": "430-439",
        "source_extraction": "Final models use a central scale height of about 3 arcsec, or 210 pc.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports thin/flaring disk overlay review",
    },
    {
        "galaxy": "NGC4013",
        "proposed_readout_subfamily": "K_true_compact",
        "evidence_id": "disk_overlay_check",
        "observable_name": "rotational_lag_profile",
        "observable_value": "lag_shallows_radially_from_minus35_to_zero_near_R25",
        "observable_unit": "km/s/kpc profile",
        "numeric_value": "",
        "source_file": "ngc4013_zschaechner_rand_2015_hi_kinematics.txt",
        "source_line_refs": "13-20;474-480;527-528",
        "source_extraction": "The HI lag is detected and becomes shallower with radius.",
        "extraction_status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
        "acceptance_use": "supports disk-halo/vertical-flow overlay review",
    },
    {
        "galaxy": "NGC5907",
        "proposed_readout_subfamily": "K_projection_dominated",
        "evidence_id": "projection_geometry",
        "observable_name": "optical_warp_radial_range",
        "observable_value": "13.3-24.0",
        "observable_unit": "kpc",
        "numeric_value": "13.3;24.0",
        "source_file": "ngc5907_sasaki_1987_surface_photometry_warp.txt",
        "source_line_refs": "9-23",
        "source_extraction": "The optical warp is reported over projected distances 13.3-24.0 kpc.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports projection/warp geometry review",
    },
    {
        "galaxy": "NGC5907",
        "proposed_readout_subfamily": "K_projection_dominated",
        "evidence_id": "projection_geometry",
        "observable_name": "optical_warp_max_displacement",
        "observable_value": "1.7",
        "observable_unit": "kpc",
        "numeric_value": "1.7",
        "source_file": "ngc5907_sasaki_1987_surface_photometry_warp.txt",
        "source_line_refs": "15-23",
        "source_extraction": "The maximum optical-warp displacement is reported at about 1.7 kpc.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports projection/warp amplitude review",
    },
    {
        "galaxy": "NGC5907",
        "proposed_readout_subfamily": "K_projection_dominated",
        "evidence_id": "projection_geometry",
        "observable_name": "disk_truncation_scale_lengths",
        "observable_value": "main_disk_4.92_kpc;corrected_4.70_kpc;outer_truncated_1.23_kpc",
        "observable_unit": "kpc",
        "numeric_value": "4.92;4.70;1.23",
        "source_file": "ngc5907_sasaki_1987_surface_photometry_warp.txt",
        "source_line_refs": "9-15",
        "source_extraction": "The main disk and truncated outer portion have distinct scale lengths.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports projection/truncation review",
    },
    {
        "galaxy": "NGC5907",
        "proposed_readout_subfamily": "K_projection_dominated",
        "evidence_id": "velocity_field_sanity",
        "observable_name": "interaction_warp_context",
        "observable_value": "warp_and_dwarf_interaction_context_present",
        "observable_unit": "categorical",
        "numeric_value": "",
        "source_file": "ngc5907_shang_1998_ring_warp_interaction.txt",
        "source_line_refs": "title/abstract source",
        "source_extraction": "The source frames NGC5907 as a ring/warp interaction case with dwarf-galaxy context.",
        "extraction_status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
        "acceptance_use": "supports projection/history review",
    },
    {
        "galaxy": "NGC5907",
        "proposed_readout_subfamily": "K_projection_dominated",
        "evidence_id": "vertical_or_warp_source",
        "observable_name": "edge_on_vertical_structure_source",
        "observable_value": "CO_HI_Spitzer_vertical_structure_study_present",
        "observable_unit": "categorical",
        "numeric_value": "",
        "source_file": "ngc5907_wiegert_2015_edge_on_ism.txt",
        "source_line_refs": "14-23;52-59",
        "source_extraction": "The source studies vertical gas and stellar structure using CO, HI, and Spitzer data.",
        "extraction_status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
        "acceptance_use": "supports vertical/projection sanity; exact extracted h/Rs still pending",
    },
    {
        "galaxy": "NGC7331",
        "proposed_readout_subfamily": "K_thick_regular",
        "evidence_id": "vertical_scale_or_thickness",
        "observable_name": "molecular_scaleheight_range",
        "observable_value": "100-200",
        "observable_unit": "pc",
        "numeric_value": "100;200",
        "source_file": "ngc7331_patra_2018_molecular_scale_height.txt",
        "source_line_refs": "16-24;715-721;984-986",
        "source_extraction": "The molecular gas scaleheight is reported in the 100-200 pc range, depending on radius and velocity dispersion.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports K_thick_regular vertical-scale evidence",
    },
    {
        "galaxy": "NGC7331",
        "proposed_readout_subfamily": "K_thick_regular",
        "evidence_id": "vertical_scale_or_thickness",
        "observable_name": "edge_on_projected_hwhm",
        "observable_value": "500",
        "observable_unit": "pc",
        "numeric_value": "500",
        "source_file": "ngc7331_patra_2018_molecular_scale_height.txt",
        "source_line_refs": "23-26;955-981;1033-1037",
        "source_extraction": "The projected edge-on molecular disk HWHM is reported at about 500 pc.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports K_thick_regular observable thickness",
    },
    {
        "galaxy": "NGC7331",
        "proposed_readout_subfamily": "K_thick_regular",
        "evidence_id": "projection_safety",
        "observable_name": "inclination_review_range",
        "observable_value": "72-80;adopted_76",
        "observable_unit": "deg",
        "numeric_value": "72;80;76",
        "source_file": "ngc7331_patra_2018_molecular_scale_height.txt",
        "source_line_refs": "108-110;864-867;960-965;1028-1031",
        "source_extraction": "The source explores inclinations 72-80 degrees and adopts 76 degrees.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports projection-safety context for NGC7331",
    },
    {
        "galaxy": "NGC7331",
        "proposed_readout_subfamily": "K_thick_regular",
        "evidence_id": "low_warp_asymmetry",
        "observable_name": "possible_outer_warp_caveat",
        "observable_value": "possible_extra_outer_emission_from_warp",
        "observable_unit": "categorical",
        "numeric_value": "",
        "source_file": "ngc7331_patra_2018_molecular_scale_height.txt",
        "source_line_refs": "960-968",
        "source_extraction": "The source notes that extra edge emission could be produced by an outer-disk warp.",
        "extraction_status": "CAVEAT_CONTEXT_SOURCE_FIELD",
        "acceptance_use": "prevents unconditional low-warp acceptance without HI/projection review",
    },
    {
        "galaxy": "NGC4183",
        "proposed_readout_subfamily": "K_expdisk_overlay",
        "evidence_id": "bar_core_projection_history_overlay",
        "observable_name": "whisp_lopsidedness_context",
        "observable_value": "whisp_kinematic_lopsidedness_method_context",
        "observable_unit": "categorical",
        "numeric_value": "",
        "source_file": "ngc4183_whisp_lopsidedness_context_2011.txt",
        "source_line_refs": "23-36;103-128;907-923",
        "source_extraction": "The source provides WHISP lopsidedness methodology and sample context, but not a direct NGC4183 extracted row here.",
        "extraction_status": "CONTEXT_ONLY_NOT_GALAXY_SPECIFIC",
        "acceptance_use": "needs primary table/galaxy-specific extraction before subfamily acceptance",
    },
    {
        "galaxy": "NGC4088",
        "proposed_readout_subfamily": "K_warp_history_coupled",
        "evidence_id": "warp_onset_asymmetry",
        "observable_name": "orientation_mismatch_first_pass",
        "observable_value": "90",
        "observable_unit": "deg",
        "numeric_value": "90",
        "source_file": "internal:s4g75_ngc4088_epsilon_cross_source_observables.csv",
        "source_line_refs": "O1_ORIENTATION_MISMATCH",
        "source_extraction": "The source-bound protocol records a first-pass outer/inner orientation mismatch of 90 degrees from the NGC4088 channel-map digitization response.",
        "extraction_status": "PRELIMINARY_SOURCE_FIELD_REVIEW_REQUIRED",
        "acceptance_use": "supports warp/history review only; independent source review still required before numeric bound use",
    },
    {
        "galaxy": "NGC4088",
        "proposed_readout_subfamily": "K_warp_history_coupled",
        "evidence_id": "warp_onset_asymmetry",
        "observable_name": "side_asymmetry_first_pass",
        "observable_value": "0.40",
        "observable_unit": "arcmin",
        "numeric_value": "0.40",
        "source_file": "internal:s4g75_ngc4088_epsilon_cross_source_observables.csv",
        "source_line_refs": "O2_SIDE_ASYMMETRY",
        "source_extraction": "The source-bound protocol records a first-pass side-asymmetry proxy of 0.40 arcmin from the channel-map digitization response.",
        "extraction_status": "PRELIMINARY_SOURCE_FIELD_REVIEW_REQUIRED",
        "acceptance_use": "supports asymmetry review only; independent source review still required before numeric bound use",
    },
    {
        "galaxy": "NGC4088",
        "proposed_readout_subfamily": "K_warp_history_coupled",
        "evidence_id": "warp_onset_asymmetry",
        "observable_name": "x_warp_onset_value",
        "observable_value": "not_extracted",
        "observable_unit": "dimensionless_RHI_fraction",
        "numeric_value": "",
        "source_file": "internal:s4g75_ngc4088_warp_onset_status.csv",
        "source_line_refs": "WARP_PRESENT_ONSET_NOT_EXTRACTED",
        "source_extraction": "The current best source status records a qualitative warp plus global HI geometry, but no source-native radial onset or PA/theta profile has been extracted.",
        "extraction_status": "BLOCKED_NEEDS_MEASUREMENT",
        "acceptance_use": "requires radial PA profile, radial warp-angle profile, or channel-map digitization before accepted subfamily use",
    },
    {
        "galaxy": "NGC4088",
        "proposed_readout_subfamily": "K_warp_history_coupled",
        "evidence_id": "hi_disturbance",
        "observable_name": "q_warp_measured_first_pass",
        "observable_value": "1.0",
        "observable_unit": "dimensionless",
        "numeric_value": "1.0",
        "source_file": "internal:s4g75_ngc4088_qwarp_first_pass_response.csv",
        "source_line_refs": "QWARP_FIRST_PASS_SOURCE_RESPONSE_V1",
        "source_extraction": "A first-pass source response records q_warp_measured=1.0 from 23 panel measurements, with review still required.",
        "extraction_status": "PRELIMINARY_SOURCE_FIELD_REVIEW_REQUIRED",
        "acceptance_use": "cannot be used as an accepted numeric bound until independently reviewed",
    },
    {
        "galaxy": "NGC4088",
        "proposed_readout_subfamily": "K_warp_history_coupled",
        "evidence_id": "interaction_history",
        "observable_name": "h4_interaction_context",
        "observable_value": "1.0",
        "observable_unit": "dimensionless",
        "numeric_value": "1.0",
        "source_file": "internal:s4g75_ngc4088_h4_interaction_context_review_summary.csv",
        "source_line_refs": "H4_INTERACTION_CONTEXT_ACCEPTED_SOURCE_REVIEWED",
        "source_extraction": "The H4 interaction-context source review accepts the interaction/history context for protocol-bound use.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports interaction/history context for K_warp_history_coupled, but does not by itself accept the subfamily",
    },
    {
        "galaxy": "NGC4088",
        "proposed_readout_subfamily": "K_warp_history_coupled",
        "evidence_id": "interaction_history",
        "observable_name": "m_history_warp_first_pass",
        "observable_value": "1.0",
        "observable_unit": "dimensionless",
        "numeric_value": "1.0",
        "source_file": "internal:s4g75_ngc4088_memory_history_first_pass_response.csv",
        "source_line_refs": "PARTIAL_FIRST_PASS_SOURCE_FILLED_REVIEW_REQUIRED",
        "source_extraction": "A first-pass memory/history response records m_history_warp=1.0, but one required component remains unaccepted and review is required.",
        "extraction_status": "PRELIMINARY_SOURCE_FIELD_REVIEW_REQUIRED",
        "acceptance_use": "supports memory/history review only; not accepted for numeric endpoint or bound use",
    },
    {
        "galaxy": "NGC4088",
        "proposed_readout_subfamily": "K_warp_history_coupled",
        "evidence_id": "epsilon_cross_bound",
        "observable_name": "epsilon_cross_numeric_bound",
        "observable_value": "blocked_until_q_and_memory_ready",
        "observable_unit": "dimensionless",
        "numeric_value": "",
        "source_file": "internal:s4g75_ngc4088_epsilon_cross_source_bound_summary.csv",
        "source_line_refs": "SYMBOLIC_UNBOUNDED_UNTIL_Q_AND_MEMORY_READY",
        "source_extraction": "The epsilon_cross source-bound protocol has a partial source-bound state, but numeric bound use remains blocked until q_warp and memory/history are accepted.",
        "extraction_status": "BLOCKED_NEEDS_MEASUREMENT",
        "acceptance_use": "blocks endpoint-safe epsilon_cross use for K_warp_history_coupled",
    },
    {
        "galaxy": "UGC05716",
        "proposed_readout_subfamily": "K_disturbed_outer_tail",
        "evidence_id": "hi_asymmetry_map",
        "observable_name": "hi_rotation_context",
        "observable_value": "rotation_dominated_HI_velocity_field",
        "observable_unit": "categorical",
        "numeric_value": "",
        "source_file": "ugc05716_swaters_2009_late_type_dwarf_rotation_shapes.txt",
        "source_line_refs": "634-659",
        "source_extraction": "D500-2/UGC5716 is described as rotation dominated with a fitted HI disk.",
        "extraction_status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
        "acceptance_use": "supports HI source availability; not a disturbed-tail acceptance",
    },
    {
        "galaxy": "UGC05716",
        "proposed_readout_subfamily": "K_disturbed_outer_tail",
        "evidence_id": "hi_asymmetry_map",
        "observable_name": "ugc05716_kinematic_inclination",
        "observable_value": "57",
        "observable_unit": "deg",
        "numeric_value": "57",
        "source_file": "ugc05716_swaters_2009_late_type_dwarf_rotation_shapes.txt",
        "source_line_refs": "640-659",
        "source_extraction": "The kinematic inclination is reported at about 57 degrees with a 6 degree uncertainty.",
        "extraction_status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
        "acceptance_use": "supports projection context; not HI asymmetry",
    },
    {
        "galaxy": "UGC05716",
        "proposed_readout_subfamily": "K_disturbed_outer_tail",
        "evidence_id": "hi_asymmetry_map",
        "observable_name": "hi_asymmetry_or_tail_measurement",
        "observable_value": "not_extracted",
        "observable_unit": "categorical",
        "numeric_value": "",
        "source_file": "ugc05716_swaters_2009_late_type_dwarf_rotation_shapes.txt",
        "source_line_refs": "634-659",
        "source_extraction": "The extracted section supports rotation/inclination, not a resolved HI asymmetry or tail transition.",
        "extraction_status": "BLOCKED_NEEDS_MEASUREMENT",
        "acceptance_use": "needs HI map/asymmetry extraction before K_disturbed_outer_tail acceptance",
    },
]


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


def main() -> None:
    rows = pd.DataFrame(EXTRACTIONS)
    rows["source_path"] = rows["source_file"].map(
        lambda name: str(DATA / name.removeprefix("internal:"))
        if str(name).startswith("internal:")
        else str(LITERATURE / name)
    )
    rows["source_exists"] = rows["source_path"].map(lambda path: Path(path).exists())
    rows["accepted_label_promoted"] = False
    rows["endpoint_scores_allowed"] = False
    rows["claim_boundary"] = CLAIM_BOUNDARY
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    rows.to_csv(DATA / "readout_subfamily_extracted_observables.csv", index=False)

    status_summary = (
        rows.groupby(["galaxy", "extraction_status"], as_index=False)
        .agg(n_observables=("observable_name", "size"))
        .sort_values(["galaxy", "extraction_status"])
    )
    status_summary.to_csv(
        DATA / "readout_subfamily_extracted_observables_summary.csv", index=False
    )
    acceptance_summary = (
        rows.assign(
            source_accepted=rows["extraction_status"].str.startswith("ACCEPTED")
        )
        .groupby(["galaxy", "proposed_readout_subfamily"], as_index=False)
        .agg(
            n_extracted=("observable_name", "size"),
            n_source_accepted=("source_accepted", "sum"),
            n_blocked=("extraction_status", lambda s: int(s.str.contains("BLOCKED").sum())),
            n_caveat=("extraction_status", lambda s: int(s.str.contains("CAVEAT|RECLASSIFICATION|CONTEXT_ONLY_NOT").sum())),
        )
        .sort_values(["galaxy", "proposed_readout_subfamily"])
    )
    acceptance_summary.to_csv(
        DATA / "readout_subfamily_extraction_acceptance_summary.csv", index=False
    )

    report_lines = [
        "# Readout-Subfamily Observable Extraction",
        "",
        "This report extracts residual-blind observables from cached literature",
        "sources. It records source fields only: no endpoint residual, required-S_tau",
        "diagnostic, or best-fit readout family is used to promote a label.",
        "",
        "## Acceptance Summary",
        "",
        markdown_table(acceptance_summary),
        "",
        "## Status Summary",
        "",
        markdown_table(status_summary),
        "",
        "## Extracted Observable Ledger",
        "",
        markdown_table(
            rows[
                [
                    "galaxy",
                    "proposed_readout_subfamily",
                    "evidence_id",
                    "observable_name",
                    "observable_value",
                    "observable_unit",
                    "source_line_refs",
                    "extraction_status",
                    "acceptance_use",
                    "claim_boundary",
                ]
            ]
        ),
        "",
        "## Remaining Blockers",
        "",
        "- IC2574 still lacks a numeric outer-tail transition radius.",
        "- UGC05716 has HI rotation/projection context but no extracted HI asymmetry or tail measurement.",
        "- NGC4183 currently has WHISP-method context, not a direct galaxy-specific overlay measurement.",
        "- NGC7331 has vertical-scale support, but low-warp acceptance remains caveated by possible outer-warp emission.",
        "- NGC4013 source evidence pressures the current compact-only subfamily toward an overlay/warp review.",
        "- NGC4088 has residual-blind first-pass warp/history fields, but x_warp, q_warp, memory/history, and epsilon_cross still need independent promotion before subfamily acceptance.",
        "",
    ]
    (REPORTS / "readout_subfamily_observable_extraction.md").write_text(
        "\n".join(report_lines), encoding="utf-8"
    )
    print(acceptance_summary.to_string(index=False))


if __name__ == "__main__":
    main()
