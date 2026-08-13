#!/usr/bin/env python3
"""Build the source-backed observer-channel collective probe atlas."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


def normalize_name(value: str) -> str:
    name = re.sub(r"[^A-Z0-9]", "", value.upper())
    match = re.fullmatch(r"NGC0*(\d+)", name)
    return f"NGC{int(match.group(1))}" if match else name


def read_names(path: Path, column: str) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {
        normalize_name(row[column]): row
        for row in rows
        if row.get(column, "").strip()
    }


def atlas_rows(
    phangs_sparc_overlap: list[str],
    phangs_muse_overlap: list[str],
    ghasp_overlap_count: int,
    ghasp_top_candidate: str,
    ngc3726_two_side_support: bool,
    ngc3726_odd_null_p: float,
    ngc4559_hr_null_p: float,
    ngc4559_lr_null_p: float,
) -> list[dict[str, object]]:
    overlap_text = ";".join(phangs_sparc_overlap) or "none"
    muse_text = ";".join(phangs_muse_overlap) or "none"
    return [
        {
            "probe_id": "OC-P01",
            "probe_family": "hi_side_parity",
            "operator_role": "physical_channel_candidate",
            "observable": "THINGS H I approaching/receding odd-even velocity-field decomposition",
            "independent_direction_target": "orientation-odd versus common even spectral response",
            "source_dataset": "THINGS NGC7331 natural and robust moment maps",
            "source_url": "https://arxiv.org/abs/0810.2125",
            "local_evidence": "source-frozen NGC7331 FITS products and parity diagnostic",
            "source_verified": True,
            "local_products": True,
            "same_object_cospatial": True,
            "endpoint_blind": True,
            "common_parent_transport": "single_object_only",
            "nonredundancy_status": "partial_parity_split_not_full_independent_probe",
            "radial_overlap": "outer_disk_available",
            "uncertainty_status": "partial_two_weighting_replication",
            "a_row_status": "not_constructed",
            "readiness": "DIAGNOSTIC_READY_SINGLE_GALAXY_NOT_A_MATRIX_ROW",
            "priority": 1,
            "next_action": "derive a source-blind path/parity A_p map before population use",
        },
        {
            "probe_id": "OC-P02",
            "probe_family": "hi_halpha_cospatial_kinematics",
            "operator_role": "physical_tracer_probe_candidate",
            "observable": "co-spatial H I and Halpha velocity fields with matched radial bins",
            "independent_direction_target": "neutral-gas versus ionized-gas access while holding source geometry fixed",
            "source_dataset": "THINGS/SPARC H I plus GHASP Halpha cubes and velocity fields",
            "source_url": "https://arxiv.org/abs/0808.0132",
            "local_evidence": f"alias-aware GHASP VI+VII/SPARC overlap={ghasp_overlap_count}; source-only top candidate={ghasp_top_candidate}; NGC3726 zero-null p={ngc3726_odd_null_p:.4f}; prospective NGC4559 HR/LR p={ngc4559_hr_null_p:.4f}/{ngc4559_lr_null_p:.4f}",
            "source_verified": True,
            "local_products": ngc3726_two_side_support,
            "same_object_cospatial": False,
            "endpoint_blind": True,
            "common_parent_transport": "open",
            "nonredundancy_status": "candidate_strong_if_cospatial",
            "radial_overlap": "to_be_measured",
            "uncertainty_status": "open_beam_smearing_extinction_non_circular_motion",
            "a_row_status": "not_constructed",
            "readiness": "TWO_SOURCE_RANKED_TRACER_TESTS_ZERO_NULL_NOT_REJECTED",
            "priority": 1,
            "next_action": "preserve two negative tests; acquire the next source-ranked independent H I side route without retuning the statistic",
        },
        {
            "probe_id": "OC-P03",
            "probe_family": "co_halpha_cospatial_kinematics",
            "operator_role": "physical_tracer_probe_candidate",
            "observable": "PHANGS CO(2-1) and MUSE ionized-gas velocity fields",
            "independent_direction_target": "molecular-gas versus ionized-gas channel access",
            "source_dataset": "PHANGS-ALMA and PHANGS-MUSE public releases",
            "source_url": "https://www.phangs.org/data",
            "local_evidence": f"PHANGS-ALMA/SPARC overlap={overlap_text}; overlap with MUSE flag={muse_text}",
            "source_verified": True,
            "local_products": True,
            "same_object_cospatial": False,
            "endpoint_blind": True,
            "common_parent_transport": "open_no_current_sparc_muse_overlap",
            "nonredundancy_status": "candidate_strong_but_shared_gas_systematics",
            "radial_overlap": "primarily_inner_star_forming_disk",
            "uncertainty_status": "open_streaming_beam_smearing_pressure_support",
            "a_row_status": "not_constructed",
            "readiness": "SOURCE_EXISTS_DIRECT_SPARC_PILOT_BLOCKED",
            "priority": 2,
            "next_action": "seek external Halpha fields for NGC2903 and NGC3521 or use a non-SPARC common-parent pilot",
        },
        {
            "probe_id": "OC-P04",
            "probe_family": "gas_stellar_kinematics",
            "operator_role": "physical_tracer_probe_candidate",
            "observable": "ionized-gas velocity plus stellar velocity and dispersion",
            "independent_direction_target": "collisional gas versus collisionless stellar response",
            "source_dataset": "DiskMass Survey",
            "source_url": "https://arxiv.org/abs/1307.8130",
            "local_evidence": "no local DiskMass-SPARC crossmatch or source-frozen cubes",
            "source_verified": True,
            "local_products": False,
            "same_object_cospatial": True,
            "endpoint_blind": True,
            "common_parent_transport": "open",
            "nonredundancy_status": "candidate_strong_with_dynamical_model_dependence",
            "radial_overlap": "reported_to_about_three_disk_scale_lengths",
            "uncertainty_status": "open_asymmetric_drift_vertical_structure_inclination",
            "a_row_status": "not_constructed",
            "readiness": "PRIORITY_2_CROSSMATCH_AND_MODEL_AUDIT",
            "priority": 2,
            "next_action": "build DiskMass identity crossmatch and freeze the asymmetric-drift control model",
        },
        {
            "probe_id": "OC-P05",
            "probe_family": "hi_imaging_weight_replication",
            "operator_role": "pipeline_control_not_physical_probe",
            "observable": "THINGS natural versus robust image weighting",
            "independent_direction_target": "instrumental/reduction robustness only",
            "source_dataset": "THINGS NGC7331",
            "source_url": "https://arxiv.org/abs/0810.2125",
            "local_evidence": "both products frozen and scored in parity diagnostic",
            "source_verified": True,
            "local_products": True,
            "same_object_cospatial": True,
            "endpoint_blind": True,
            "common_parent_transport": "not_applicable_same_physical_channel",
            "nonredundancy_status": "failed_as_independent_physical_probe",
            "radial_overlap": "matched",
            "uncertainty_status": "useful_pipeline_replication",
            "a_row_status": "not_a_physical_row",
            "readiness": "CONTROL_READY_DO_NOT_COUNT_TOWARD_INJECTIVITY",
            "priority": 0,
            "next_action": "retain as robustness control only",
        },
        {
            "probe_id": "OC-P06",
            "probe_family": "spectral_centroid_width_multiline",
            "operator_role": "physical_channel_probe_candidate",
            "observable": "matched H I, CO, and optical-line centroid, width, and profile asymmetry",
            "independent_direction_target": "frequency transfer versus local turbulence/radiative-transfer response",
            "source_dataset": "THINGS plus PHANGS-ALMA/MUSE or GHASP",
            "source_url": "https://almascience.eso.org/alma-data/lp/PHANGS/",
            "local_evidence": "NGC7331 H I moments local; no frozen multiline same-pixel packet",
            "source_verified": True,
            "local_products": False,
            "same_object_cospatial": False,
            "endpoint_blind": True,
            "common_parent_transport": "open",
            "nonredundancy_status": "candidate_high_value_for_clock_vs_gas_systematics",
            "radial_overlap": "to_be_measured",
            "uncertainty_status": "open_line_formation_optical_depth_turbulence",
            "a_row_status": "not_constructed",
            "readiness": "PRIORITY_1_MULTILINE_PACKET_REQUIRED",
            "priority": 1,
            "next_action": "freeze same-pixel line centroids and widths before any rotation residual comparison",
        },
        {
            "probe_id": "OC-P07",
            "probe_family": "morphology_onset_body_coordinate",
            "operator_role": "body_coordinate_control_not_channel_probe",
            "observable": "S4G disk break, radial m=1 onset, H I warp onset",
            "independent_direction_target": "body-side mode coordinate and onset localization",
            "source_dataset": "S4G and H I morphology products",
            "source_url": "https://irsa.ipac.caltech.edu/data/SPITZER/S4G/overview.html",
            "local_evidence": "disk-break small-n and lopsidedness coverage audits exist",
            "source_verified": True,
            "local_products": True,
            "same_object_cospatial": True,
            "endpoint_blind": True,
            "common_parent_transport": "body_side_only",
            "nonredundancy_status": "not_independent_channel_direction",
            "radial_overlap": "partial_small_n",
            "uncertainty_status": "partial",
            "a_row_status": "not_a_channel_row",
            "readiness": "BODY_CALIBRATION_CONTROL_DO_NOT_COUNT_TOWARD_A_INJECTIVITY",
            "priority": 0,
            "next_action": "use to define body coordinates, not to claim channel independence",
        },
        {
            "probe_id": "OC-P08",
            "probe_family": "dynamics_weak_lensing",
            "operator_role": "cross_readout_probe_candidate",
            "observable": "rotation/dynamics versus galaxy-galaxy weak-lensing shear",
            "independent_direction_target": "kinematic versus null-geodesic mass/readout response",
            "source_dataset": "SPARC plus an independently selected weak-lensing lens sample",
            "source_url": "https://ui.adsabs.harvard.edu/abs/2016AJ....152..157L/abstract",
            "local_evidence": "no object-level common-parent SPARC lensing packet",
            "source_verified": False,
            "local_products": False,
            "same_object_cospatial": False,
            "endpoint_blind": True,
            "common_parent_transport": "blocked_stack_statistics_not_same_object_operator",
            "nonredundancy_status": "potentially_strong_if_transport_proved",
            "radial_overlap": "different_scales",
            "uncertainty_status": "open_shear_calibration_halo_environment_stacking",
            "a_row_status": "not_constructed",
            "readiness": "THEORY_HIGH_VALUE_EMPIRICALLY_BLOCKED",
            "priority": 3,
            "next_action": "identify an object-matched or rigorously transported dynamics-lensing sample",
        },
        {
            "probe_id": "OC-P09",
            "probe_family": "multipath_time_delay",
            "operator_role": "architecture_analogue_not_current_galaxy_probe",
            "observable": "multiple lensed images and measured inter-image time delays",
            "independent_direction_target": "distinct null paths to one variable source",
            "source_dataset": "H0LiCOW/COSMOGRAIL",
            "source_url": "https://arxiv.org/abs/1607.00017",
            "local_evidence": "no shared SPARC disk-rotation parent system",
            "source_verified": True,
            "local_products": False,
            "same_object_cospatial": False,
            "endpoint_blind": True,
            "common_parent_transport": "blocked_different_source_deflector_architecture",
            "nonredundancy_status": "multiple_paths_real_but_not_current_K_body",
            "radial_overlap": "not_applicable",
            "uncertainty_status": "lens_model_line_of_sight_mass_sheet",
            "a_row_status": "not_current_matrix_row",
            "readiness": "ARCHITECTURE_CONTROL_NOT_PAPER8_PROBE",
            "priority": 3,
            "next_action": "use to constrain path-law form, not to stack with SPARC",
        },
        {
            "probe_id": "OC-P10",
            "probe_family": "strong_lensing_stellar_kinematics",
            "operator_role": "cross_readout_probe_candidate",
            "observable": "strong-lens image/time-delay model plus deflector stellar dispersion",
            "independent_direction_target": "lensing-path versus stellar dynamical parent response",
            "source_dataset": "H0LiCOW/TDCOSMO",
            "source_url": "https://arxiv.org/abs/1607.01403",
            "local_evidence": "common deflector exists in source studies but no disk-rotation/SPARC transport",
            "source_verified": True,
            "local_products": False,
            "same_object_cospatial": True,
            "endpoint_blind": True,
            "common_parent_transport": "open_cross_domain",
            "nonredundancy_status": "partial_model_coupled",
            "radial_overlap": "lens_aperture_specific",
            "uncertainty_status": "mass_sheet_anisotropy_environment",
            "a_row_status": "not_constructed",
            "readiness": "CROSS_DOMAIN_METHOD_CANDIDATE_NOT_PAPER8_ROW",
            "priority": 3,
            "next_action": "derive common-parent transport before any Tau stacking claim",
        },
        {
            "probe_id": "OC-P11",
            "probe_family": "distance_inclination_systematics",
            "operator_role": "nuisance_control_not_physical_probe",
            "observable": "distance, inclination, beam, warp, and asymmetric-drift perturbations",
            "independent_direction_target": "conventional-systematics null space",
            "source_dataset": "SPARC and source-specific geometry records",
            "source_url": "https://astroweb.case.edu/SPARC/",
            "local_evidence": "SPARC quality and geometry fields available",
            "source_verified": True,
            "local_products": True,
            "same_object_cospatial": True,
            "endpoint_blind": True,
            "common_parent_transport": "nuisance_layer",
            "nonredundancy_status": "mandatory_control_not_positive_A_row",
            "radial_overlap": "full_curve_where_available",
            "uncertainty_status": "partial",
            "a_row_status": "not_a_physical_row",
            "readiness": "CONTROL_REQUIRED_DO_NOT_COUNT_TOWARD_INJECTIVITY",
            "priority": 0,
            "next_action": "propagate into K_stack uncertainty N",
        },
        {
            "probe_id": "OC-P12",
            "probe_family": "proper_motion_transverse_kinematics",
            "operator_role": "physical_kinematic_probe_candidate",
            "observable": "proper-motion transverse velocity versus line-of-sight Doppler velocity",
            "independent_direction_target": "angular/time astrometry versus spectral frequency shift",
            "source_dataset": "Gaia/HST Local Group astrometry",
            "source_url": "https://www.cosmos.esa.int/web/gaia/data-release-3",
            "local_evidence": "no local same-object resolved disk packet or SPARC population route",
            "source_verified": True,
            "local_products": False,
            "same_object_cospatial": False,
            "endpoint_blind": True,
            "common_parent_transport": "open_local_group_only",
            "nonredundancy_status": "potentially_strong_different_measurement_principle",
            "radial_overlap": "sparse",
            "uncertainty_status": "distance_internal_motion_reference_frame",
            "a_row_status": "not_constructed",
            "readiness": "LONG_HORIZON_CANDIDATE",
            "priority": 4,
            "next_action": "identify one resolved Local Group disk with matched radial Doppler and astrometric constraints",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, object]]) -> str:
    columns = ["probe_id", "probe_family", "operator_role", "readiness", "priority"]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def main() -> None:
    phangs = read_names(DATA / "p0_phangs_public_sample.csv", "Name")
    sparc = read_names(DATA / "external_sparc_master_table.csv", "Galaxy")
    overlap_keys = sorted(set(phangs) & set(sparc))
    overlap = [sparc[key]["Galaxy"] for key in overlap_keys]
    muse_overlap = [
        sparc[key]["Galaxy"]
        for key in overlap_keys
        if phangs[key].get("VLT/MUSE", "").upper() == "TRUE"
    ]
    ghasp = json.loads(
        (DATA / "ghasp_sparc_source_only_candidate_federation_v01.json").read_text(
            encoding="utf-8"
        )
    )
    ghasp_legacy = json.loads(
        (DATA / "ghasp_sparc_probe_crossmatch_v01.json").read_text(encoding="utf-8")
    )
    whisp = json.loads(
        (DATA / "ugc06787_whisp_hi_source_v01.json").read_text(encoding="utf-8")
    )
    whisp_preflight = json.loads(
        (DATA / "ugc06787_whisp_graphical_velocity_preflight_v01.json").read_text(
            encoding="utf-8"
        )
    )
    angular_gate = json.loads(
        (DATA / "ugc06787_common_angular_transport_gate_v01.json").read_text(
            encoding="utf-8"
        )
    )
    angular_axis = json.loads(
        (DATA / "ugc06787_whisp_angular_axis_preflight_v01.json").read_text(
            encoding="utf-8"
        )
    )
    ngc3726_whisp = json.loads(
        (DATA / "ngc3726_whisp_hi_source_v01.json").read_text(encoding="utf-8")
    )
    ngc3726_preflight = json.loads(
        (DATA / "ngc3726_whisp_graphical_side_preflight_v01.json").read_text(
            encoding="utf-8"
        )
    )
    ngc3726_channel = json.loads(
        (DATA / "ngc3726_hi_halpha_channel_preflight_v01.json").read_text(
            encoding="utf-8"
        )
    )
    ngc4559_halogas = json.loads(
        (DATA / "ngc4559_halogas_moment_sources_v01.json").read_text(
            encoding="utf-8"
        )
    )
    ngc4559_replication = json.loads(
        (DATA / "ngc4559_halogas_hi_halpha_replication_v01.json").read_text(
            encoding="utf-8"
        )
    )
    ngc3893_eligibility = json.loads(
        (DATA / "ngc3893_replication_eligibility_v01.json").read_text(
            encoding="utf-8"
        )
    )
    rows = atlas_rows(
        overlap,
        muse_overlap,
        ghasp["sparc_overlap_galaxies"],
        ghasp["top_source_only_candidate"],
        ngc3726_preflight["both_hi_velocity_sides_present"]
        and ngc3726_preflight["both_halpha_sides_present"],
        ngc3726_channel["primary_odd_contrast"]["chi2_zero_p"],
        ngc4559_replication["maps"]["HR"]["summary"]["chi2_zero_p"],
        ngc4559_replication["maps"]["LR"]["summary"]["chi2_zero_p"],
    )

    actual_rows = [row for row in rows if row["a_row_status"] == "constructed"]
    physical_candidates = [row for row in rows if "candidate" in str(row["operator_role"])]
    controls = [row for row in rows if "control" in str(row["operator_role"])]
    summary = {
        "schema": "observer_channel_collective_probe_atlas_v01",
        "status": "COLLECTIVE_PROBE_ATLAS_BUILT_NO_INJECTIVE_A_MATRIX",
        "n_rows": len(rows),
        "n_physical_candidates": len(physical_candidates),
        "n_controls_or_body_coordinates": len(controls),
        "n_constructed_a_rows": len(actual_rows),
        "phangs_alma_sparc_overlap": overlap,
        "phangs_muse_sparc_overlap": muse_overlap,
        "ghasp_sparc_overlap_count": ghasp["sparc_overlap_galaxies"],
        "ghasp_both_side_overlap_count": ghasp["both_side_overlap_galaxies"],
        "ghasp_whisp_overview_overlap_count": ghasp["whisp_overview_overlap_galaxies"],
        "ghasp_top_source_only_candidate": ghasp["top_source_only_candidate"],
        "ghasp_top_source_only_candidates": ghasp["top_source_only_candidates"],
        "ghasp_legacy_exact_primary_name_overlap": ghasp_legacy["overlap_galaxies"],
        "ngc3726_whisp_graphical_hi_acquired": ngc3726_whisp[
            "graphical_velocity_field_acquired"
        ],
        "ngc3726_whisp_fits_acquired": ngc3726_whisp[
            "source_coordinate_fits_acquired"
        ],
        "ngc3726_hi_halpha_two_side_source_support": ngc3726_preflight[
            "both_hi_velocity_sides_present"
        ]
        and ngc3726_preflight["both_halpha_sides_present"],
        "ngc3726_odd_contrast_zero_null_p": ngc3726_channel[
            "primary_odd_contrast"
        ]["chi2_zero_p"],
        "ngc3726_odd_contrast_gls_mean_km_s": ngc3726_channel[
            "primary_odd_contrast"
        ]["gls_mean_km_s"],
        "ngc3726_observer_channel_detected": ngc3726_channel[
            "observer_channel_detected"
        ],
        "ngc4559_halogas_moment_products_acquired": ngc4559_halogas["n_products"],
        "ngc4559_halogas_pixels_opened": ngc4559_halogas["pixel_values_opened"],
        "ngc4559_replication_all_gates_pass": ngc4559_replication[
            "all_replication_gates_pass"
        ],
        "ngc4559_hr_odd_contrast_zero_null_p": ngc4559_replication["maps"]["HR"][
            "summary"
        ]["chi2_zero_p"],
        "ngc4559_lr_odd_contrast_zero_null_p": ngc4559_replication["maps"]["LR"][
            "summary"
        ]["chi2_zero_p"],
        "ngc3893_primary_replication_eligible": ngc3893_eligibility[
            "primary_replication_eligible"
        ],
        "ngc3893_control_role": ngc3893_eligibility["role"],
        "ngc3893_counts_as_negative_channel_test": ngc3893_eligibility[
            "counts_as_negative_channel_test"
        ],
        "next_clean_source_candidate": ngc3893_eligibility["next_clean_candidate"],
        "ugc06787_whisp_graphical_hi_acquired": whisp["graphical_velocity_field_acquired"],
        "ugc06787_whisp_fits_acquired": whisp["source_coordinate_fits_acquired"],
        "ugc06787_whisp_graphical_digitization_ready": whisp_preflight[
            "both_hi_velocity_sides_present"
        ],
        "ugc06787_hi_halpha_world_transport_ready": whisp_preflight[
            "halpha_common_radial_transport_ready"
        ],
        "ugc06787_angular_first_transport_rule_frozen": angular_gate[
            "transport_rule"
        ],
        "ugc06787_distance_spread_max_over_min": angular_gate[
            "distance_spread_max_over_min"
        ],
        "ugc06787_source_axis_proxy_ready": angular_axis["source_axis_proxy_ready"],
        "ugc06787_formal_wcs_ready": angular_axis["formal_wcs_ready"],
        "ugc06787_possible_angular_support_overlap": angular_axis[
            "ghasp_support_inside_both_hi_proxy_maxima"
        ],
        "collective_injectivity_test_allowed": False,
        "sigma_min_a_available": False,
        "priority_1": [row["probe_id"] for row in rows if row["priority"] == 1],
        "claim_boundary": "source-backed candidate atlas only; no physical A_p rows, common transported K_body, injectivity result, channel detection, or Tau Core validation",
    }

    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    csv_path = DATA / "observer_channel_collective_probe_atlas_v01.csv"
    json_path = DATA / "observer_channel_collective_probe_atlas_v01.json"
    report_path = REPORTS / "observer_channel_collective_probe_atlas_v01.md"
    write_csv(csv_path, rows)
    json_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(
        f"""# Observer-Channel Collective Probe Atlas v0.1

**Status:** `{summary['status']}`

## Verdict

The atlas separates physical probe candidates, body-coordinate inputs,
pipeline/nuisance controls, and cross-domain architecture candidates. No row
yet supplies a constructed physical `A_p`, so `ker A`, `sigma_min(A)`, and
collective injectivity cannot be evaluated.

The first `OC-P02` angular statistic is frozen and evaluated on source-ranked
NGC3726, then prospectively replicated with HR/LR HALOGAS maps on NGC4559.
Neither galaxy rejects zero odd contrast, while the two NGC4559 resolutions
agree internally. Source-ranked NGC3893 is blocked as a primary replication
because its dedicated source reports interaction, non-circular motions, and a
symmetry-targeted curve construction; it remains a disturbed control and does
not count as a third negative test. The immediate route continues with the
clean-candidate audit of UGC08490, without retuning the statistic. It is
followed by `OC-P06` (same-pixel
multi-line centroid/width) and the source-blind path map needed to promote
`OC-P01` beyond a single-galaxy diagnostic.

## Atlas

{markdown_table(rows)}

## Concrete Coverage Audit

```text
PHANGS-ALMA public sample x SPARC overlap: {overlap}
PHANGS-MUSE flag inside that overlap:       {muse_overlap}
GHASP VI+VII alias-aware x SPARC overlap:    {ghasp['sparc_overlap_galaxies']}
GHASP overlaps with both Halpha sides:       {ghasp['both_side_overlap_galaxies']}
Top residual-blind source candidate:         {ghasp['top_source_only_candidate']}
NGC3726 H I and Halpha two-side support:      {ngc3726_preflight['both_hi_velocity_sides_present'] and ngc3726_preflight['both_halpha_sides_present']}
NGC3726 odd-contrast zero-null p:              {ngc3726_channel['primary_odd_contrast']['chi2_zero_p']:.4f}
NGC3726 observer channel detected:             {ngc3726_channel['observer_channel_detected']}
NGC4559 HALOGAS moment products acquired:      {ngc4559_halogas['n_products']}
NGC4559 HALOGAS pixels opened:                  {ngc4559_halogas['pixel_values_opened']}
NGC4559 HR/LR zero-null p:                      {ngc4559_replication['maps']['HR']['summary']['chi2_zero_p']:.4f} / {ngc4559_replication['maps']['LR']['summary']['chi2_zero_p']:.4f}
NGC4559 replication positive:                   {ngc4559_replication['all_replication_gates_pass']}
NGC3893 primary replication eligible:           {ngc3893_eligibility['primary_replication_eligible']}
NGC3893 role:                                    {ngc3893_eligibility['role']}
Next clean source candidate:                     {ngc3893_eligibility['next_clean_candidate']}
UGC06787 WHISP graphical H I acquired:      {whisp['graphical_velocity_field_acquired']}
UGC06787 formal WCS ready:                   {angular_axis['formal_wcs_ready']}
```

The current local tables therefore do not provide an immediate PHANGS
CO-Halpha-SPARC pilot. NGC2903 and NGC3521 are the two ALMA/SPARC overlaps,
but neither carries the MUSE flag in the frozen public sample table.

## Rules

```text
natural vs robust weighting is a pipeline replication, not a new physical row;
morphology onset is a body-coordinate input, not a channel row;
distance/inclination variations enter the uncertainty N, not positive rank;
different galaxies may be stacked only after common-parent transport;
lensing/time-delay systems constrain architecture but are not SPARC rows;
no endpoint residual may select the tracer, radial support, sign, or weighting.
```

## Claim Boundary

This is a source-backed acquisition and identifiability worklist. It does not
construct the physical probe matrix, prove `ker A=0`, estimate
`sigma_min(A)`, detect an observer-time channel, or validate Tau Core.
""",
        encoding="utf-8",
    )
    print(summary["status"])
    print(csv_path)
    print(json_path)
    print(report_path)


if __name__ == "__main__":
    main()
