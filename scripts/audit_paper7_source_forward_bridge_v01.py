#!/usr/bin/env python3
"""Audit whether Paper 8 can supply Paper 7's source-forward time handoff."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"
REPORT = ROOT / "reports/paper7_source_forward_bridge_audit_v01.md"
OUT_JSON = DATA / "paper7_source_forward_bridge_audit_v01.json"
OUT_CSV = DATA / "paper7_source_forward_bridge_fields_v01.csv"

PAPER7_SYSTEMS = {
    "DES J0408-5354",
    "WGD 2038-4008",
    "HE 0435-1223",
    "RXJ 1131-1231",
    "WFI 2033-4723",
}


def load_json(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def main() -> None:
    accepted_path = DATA / "accepted_morphology_manifest.csv"
    coming_path = DATA / "coming_multicoordinate_source_descriptor_v01.csv"
    paper8_objects: set[str] = set()
    for path in (accepted_path, coming_path):
        with path.open(newline="", encoding="utf-8") as handle:
            paper8_objects.update(
                row["galaxy"].strip() for row in csv.DictReader(handle) if row.get("galaxy")
            )

    geometry = load_json("sdp81_lens_operator_geometry_validation_v01.json")
    registration = load_json("sdp81_image_g_wcs_registration_v01.json")
    covector = load_json("sdp81_common_source_covector_audit_v01.json")
    extended_source = load_json("sdp81_exact_ray_source_reconstruction_v02.json")
    spectral_transfer = load_json("sdp81_spectral_leave_one_path_out_v01.json")
    continuum_registration = load_json(
        "sdp81_continuum_path_registration_v02.json"
    )
    velocity_operator = load_json("sdp81_velocity_field_operator_v02.json")
    two_component_spatial = load_json(
        "sdp81_two_component_spatial_operator_v01.json"
    )
    centroid = load_json("sdp81_q1_multipath_centroid_v02.json")
    rank = load_json("sdp81_q1_cross_transition_rank_v02.json")
    innovation = load_json("sdp81_q1_projected_innovation_v03.json")

    overlap = sorted(paper8_objects & PAPER7_SYSTEMS)
    fields = [
        {
            "field_id": "SFH_01_BODY_CLOCK",
            "materialized": False,
            "evidence": "No numeric Theta_M exists for a Paper 7 lens system.",
        },
        {
            "field_id": "SFH_02_RELATIVE_MORPHOLOGY",
            "materialized": False,
            "evidence": (
                "Paper 8 has source-frozen galaxy descriptors, but no object overlaps "
                "the Paper 7 lens-system set. SDP.81 has a supported common exact-ray "
                "extended-source morphology, but it is not a Paper 7 time-delay target."
            ),
        },
        {
            "field_id": "SFH_03_PATH_PULLBACK",
            "materialized": False,
            "evidence": (
                "SDP.81 relative image geometry and the image-G WCS anchor are "
                "operational, but the ray-traced body-covector pullback remains open."
            ),
        },
        {
            "field_id": "SFH_04_TIME_COVECTOR",
            "materialized": False,
            "evidence": "No quotient-basic numeric a_O has been derived from Theta_M and Phi_M.",
        },
        {
            "field_id": "SFH_07_RANK_REPAIR_AUXILIARY",
            "materialized": False,
            "evidence": (
                "SDP.81 provides four paths and two transitions, but the independent "
                "second mode lacks beam/lens covariance significance."
            ),
        },
    ]

    summary = {
        "schema": "tau_core.paper8.paper7-source-forward-bridge-audit.v01",
        "paper8_numeric_object_count": len(paper8_objects),
        "paper7_target_systems": sorted(PAPER7_SYSTEMS),
        "direct_object_overlap": overlap,
        "direct_object_overlap_count": len(overlap),
        "sdp81": {
            "same_source_path_count": centroid["path_count"],
            "transition_count": 2,
            "relative_lens_geometry_reproduced": bool(
                geometry["multiplicity_pass"] and geometry["published_configuration_pass"]
            ),
            "absolute_wcs_registration_complete": geometry[
                "image_G_wcs_registration_complete"
            ],
            "absolute_wcs_registration_operational": registration[
                "absolute_wcs_registration_operational"
            ],
            "cross_transition_centered_path_cosine": rank["nominal"][
                "centered_path_cosine"
            ],
            "orthogonal_energy_fraction": innovation["nominal"][
                "orthogonal_energy_fraction"
            ],
            "shared_parent_lens_mode_supported": innovation[
                "shared_parent_lens_mode_supported"
            ],
            "independent_auxiliary_mode_detected": innovation[
                "projected_channel_innovation_detected"
            ],
            "minimal_common_source_covector_promoted": covector[
                "common_covector_promoted"
            ],
            "minimal_covector_relative_residual_range": covector[
                "relative_residual_range"
            ],
            "exact_ray_common_extended_source_supported": extended_source[
                "common_extended_source_promoted"
            ],
            "exact_ray_common_source_relative_residual": extended_source[
                "common_source_relative_residual"
            ],
            "exact_ray_common_vs_independent_squared_residual_excess": extended_source[
                "common_vs_independent_squared_residual_excess"
            ],
            "spectral_leave_one_path_out_promoted": spectral_transfer[
                "transferable_common_source_dynamics_promoted"
            ],
            "spectral_leave_one_path_out_median_r2": spectral_transfer[
                "predictive_r2_median"
            ],
            "spectral_leave_one_path_out_positive_folds": spectral_transfer[
                "positive_fold_count"
            ],
            "continuum_registration_boundary_count": continuum_registration[
                "boundary_selection_count"
            ],
            "continuum_registration_usable_for_band6": continuum_registration[
                "registration_freeze_usable_for_band6"
            ],
            "full_window_velocity_operator_promoted": velocity_operator[
                "velocity_field_operator_promoted"
            ],
            "full_window_velocity_gradient_norm": velocity_operator[
                "velocity_parameters"
            ]["gradient_norm_km_s_per_arcsec"],
            "two_component_spatial_source_promoted": two_component_spatial[
                "two_component_spatial_source_promoted"
            ],
            "two_component_spatial_predictive_positive_paths": (
                two_component_spatial["predictive_positive_path_count"]
            ),
            "two_component_spatial_predictive_median_improvement": (
                two_component_spatial[
                    "predictive_median_squared_residual_improvement"
                ]
            ),
        },
        "fields": fields,
        "source_forward_h_tau_materialized": all(
            row["materialized"] for row in fields[:4]
        ),
        "rank_repair_authorized": fields[4]["materialized"],
        "time_score_authorized": False,
        "verdict": (
            "NO_DIRECT_PAPER8_PAPER7_OBJECT_BRIDGE__"
            "SDP81_IS_A_RANK_REPAIR_CANDIDATE_NOT_YET_AN_AUTHORIZED_AUXILIARY"
        ),
        "next_finite_action": (
            "Do not further enrich the SDP.81 spatial inverse family: its "
            "two-component leave-one-path-out audit failed. Construct a source-frozen "
            "morphology descriptor for one actual Paper 7 lens target."
        ),
        "claim_boundary": (
            "Coverage and bridge-readiness audit only; no time distortion, channel "
            "innovation, or Tau Core detection."
        ),
    }

    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=("field_id", "materialized", "evidence"), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(fields)

    REPORT.write_text(
        "# Paper 7 source-forward bridge audit v01\n\n"
        f"Verdict: `{summary['verdict']}`\n\n"
        f"Paper 8 numeric-object count: `{len(paper8_objects)}`. "
        f"Direct overlap with the five Paper 7 target lenses: `{len(overlap)}`.\n\n"
        "SDP.81 is the strongest existing bridge candidate: it supplies four paths "
        "and two transitions, and both relative smooth-lens geometry and an "
        "operational image-G WCS anchor are available. It does not yet supply an "
        "authorized rank-repair observable because the body-covector pullback and "
        "independent beam/lens-covariance significance for the second mode remain "
        "open.\n\n"
        "No observer-time score is authorized.\n",
        encoding="utf-8",
    )
    print(summary["verdict"])


if __name__ == "__main__":
    main()
