#!/usr/bin/env python3
"""Audit the sealed SDP.81 CO(10-9) source gate without opening FITS payloads."""

from __future__ import annotations

import hashlib
import json
import tarfile
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data/protocols/sdp81_co109_common_action_confirmatory_protocol_v01.json"
OUT = ROOT / "data/derived/sdp81_co109_common_action_source_gate_v01.json"
REPORT = ROOT / "reports/sdp81_co109_common_action_source_gate_v01.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_artifact(record: dict) -> bool:
    path = ROOT / record["artifact"]
    return path.is_file() and sha256(path) == record["sha256"]


def load_optional(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _matrix(payload: dict, name: str, shape: tuple[int, int]) -> np.ndarray | None:
    try:
        value = np.asarray(payload[name], dtype=float)
    except (KeyError, TypeError, ValueError):
        return None
    return value if value.shape == shape and np.all(np.isfinite(value)) else None


def _finite_matrix(payload: dict, name: str) -> np.ndarray | None:
    try:
        value = np.asarray(payload[name], dtype=float)
    except (KeyError, TypeError, ValueError):
        return None
    return value if value.ndim == 2 and np.all(np.isfinite(value)) else None


def _positive(matrix: np.ndarray | None) -> bool:
    return bool(
        matrix is not None
        and np.allclose(matrix, matrix.T)
        and np.linalg.eigvalsh(matrix).min() > 0.0
    )


def validate_terminal_registration(registration: dict, root: Path = ROOT) -> tuple[bool, dict]:
    """Validate a source-derived calibration packet, not self-asserted labels."""
    jet = registration.get("source_action_jet") or {}
    h_z = _matrix(jet, "H_Z", (5, 5))
    b_zc = _matrix(jet, "B_ZC", (5, 5))
    k_c = _matrix(jet, "K_C", (5, 5))

    gas = registration.get("conditional_parent_gas_response") or {}
    h_xi = _matrix(gas, "H_xi", (5, 5))
    b_xi_z = _matrix(gas, "B_xiZ", (5, 5))
    declared_bridge = _matrix(gas, "P", (5, 5))
    try:
        gas_baseline = np.asarray(gas["baseline_gas_state"], dtype=float)
    except (KeyError, TypeError, ValueError):
        gas_baseline = np.asarray([])
    derived_bridge = None
    gas_response_valid = False
    bridge_origin_valid = False
    if _positive(h_xi) and b_xi_z is not None and declared_bridge is not None:
        derived_bridge = -np.linalg.solve(h_xi, b_xi_z)
        bridge_origin = gas.get("bridge_origin")
        if bridge_origin == "direct_conditional_cross_derivative":
            bridge_origin_valid = gas.get("direct_cross_derivative_source_owned") is True
        elif bridge_origin == "four_dimensional_mediator":
            d_z_e = _finite_matrix(gas, "D_Z_e")
            b_xi_e = _finite_matrix(gas, "B_xi_e")
            environment_dimension = gas.get("environment_tangent_dimension")
            bridge_origin_valid = bool(
                isinstance(environment_dimension, int)
                and environment_dimension >= 5
                and d_z_e is not None
                and d_z_e.shape == (environment_dimension, 5)
                and b_xi_e is not None
                and b_xi_e.shape == (5, environment_dimension)
                and gas.get("environment_descriptor_is_gauge_quotiented") is True
                and gas.get("no_direct_Z_xi_mixed_derivative") is True
                and np.allclose(b_xi_z, b_xi_e @ d_z_e, rtol=1e-9, atol=1e-11)
            )
        gas_response_valid = bool(
            gas.get("post_body_response_frozen_before_gas_solve") is True
            and gas.get("source_owned") is True
            and bridge_origin_valid
            and gas_baseline.shape == (5,)
            and np.all(np.isfinite(gas_baseline))
            and np.allclose(declared_bridge, derived_bridge, rtol=1e-9, atol=1e-11)
            and np.linalg.matrix_rank(derived_bridge, tol=1e-10) == 5
        )

    provenance = registration.get("source_provenance") or []
    provenance_valid = bool(provenance) and all(
        isinstance(item, dict)
        and (root / item.get("artifact", "__missing__")).is_file()
        and item.get("sha256") == sha256(root / item["artifact"])
        for item in provenance
    )
    path_records = registration.get("path_calibrations") or []
    expected_path_ids = {f"q1_path_{index}" for index in range(1, 5)}
    formula_results = []
    if _positive(h_z) and b_zc is not None and _positive(k_c) and gas_response_valid:
        response = -np.linalg.solve(h_z, b_zc)
        src_values, src_vectors = np.linalg.eigh(k_c)
        src_inv_sqrt = src_vectors @ np.diag(src_values ** -0.5) @ src_vectors.T
        for record in path_records:
            forward = record.get("radiative_lens_instrument_forward") or {}
            calibration = record.get("calibration") or {}
            basis = _matrix(forward, "centered_channel_basis", (6, 5))
            raw_jacobian = _matrix(forward, "raw_flux_jacobian", (6, 5))
            gas_jacobian = _matrix(forward, "gas_to_flux_jacobian", (6, 5))
            covariance = _matrix(calibration, "centered_log_covariance", (5, 5))
            composite = _matrix(
                calibration, "composite_parent_to_terminal_jacobian", (5, 5)
            )
            whitened = _matrix(calibration, "whitened_operator", (5, 5))
            try:
                flux = np.asarray(forward["baseline_flux"], dtype=float)
            except (KeyError, TypeError, ValueError):
                flux = np.asarray([])
            valid = False
            gas_factorization_valid = False
            simple = False
            minimum_singular_value = 0.0
            if (
                basis is not None
                and raw_jacobian is not None
                and gas_jacobian is not None
                and _positive(covariance)
                and composite is not None
                and whitened is not None
                and flux.shape == (6,)
                and np.all(flux > 0.0)
                and np.allclose(basis.T @ basis, np.eye(5))
                and np.allclose(basis.T @ np.ones(6), 0.0)
            ):
                expected_raw_jacobian = gas_jacobian @ derived_bridge
                gas_factorization_valid = bool(
                    np.allclose(
                        raw_jacobian,
                        expected_raw_jacobian,
                        rtol=1e-9,
                        atol=1e-11,
                    )
                )
                j_log = basis.T @ np.diag(1.0 / flux) @ raw_jacobian
                expected_composite = j_log @ response
                cov_values, cov_vectors = np.linalg.eigh(covariance)
                cov_inv_sqrt = cov_vectors @ np.diag(cov_values ** -0.5) @ cov_vectors.T
                expected_whitened = cov_inv_sqrt @ expected_composite @ src_inv_sqrt
                valid = bool(
                    gas_factorization_valid
                    and np.allclose(composite, expected_composite, rtol=1e-9, atol=1e-11)
                    and np.allclose(whitened, expected_whitened, rtol=1e-9, atol=1e-11)
                )
                singular = np.linalg.svd(expected_whitened, compute_uv=False)
                minimum_singular_value = float(singular.min())
                simple = bool(
                    minimum_singular_value > 1e-10
                    and np.min(np.abs(np.diff(singular))) > 1e-8
                )
            formula_results.append(
                {
                    "path_id": record.get("path_id"),
                    "formula_valid": valid,
                    "gas_factorization_valid": gas_factorization_valid,
                    "simple_full_rank": simple,
                    "minimum_whitened_singular_value": minimum_singular_value,
                }
            )
    path_ids = {item["path_id"] for item in formula_results}
    formula_valid = bool(
        len(formula_results) == 4
        and path_ids == expected_path_ids
        and all(item["formula_valid"] for item in formula_results)
    )
    simple_full_rank = bool(
        formula_results and all(item["simple_full_rank"] for item in formula_results)
    )
    all_gas_factorizations_valid = bool(
        formula_results
        and all(item["gas_factorization_valid"] for item in formula_results)
    )
    computed_overlap = min(
        (item["minimum_whitened_singular_value"] for item in formula_results),
        default=0.0,
    )

    checks = {
        "typed_header": registration.get("schema")
        == "tau-core.paper8.sdp81-co109-parent-terminal-registration.v01"
        and registration.get("status")
        == "PHYSICAL_PARENT_TO_CO109_TERMINAL_REGISTRATION_FROZEN",
        "source_owned_and_endpoint_blind": registration.get("source_owned") is True
        and registration.get("endpoint_pixel_read") is False,
        "five_mode_orientation_rules_declared": registration.get("mode_dimension") == 5
        and registration.get("orientation_and_permutation_fixed") is True
        and bool(registration.get("mode_orientation_rule"))
        and bool(registration.get("mode_permutation_rule")),
        "source_provenance_hashes_valid": provenance_valid,
        "ordered_conditional_parent_gas_response_reproduced": gas_response_valid,
        "parent_gas_bridge_origin_reproduced": bridge_origin_valid,
        "all_path_jacobians_factor_through_gas_bridge": all_gas_factorizations_valid,
        "four_path_pullback_formulas_reproduced": formula_valid,
        "all_paths_full_rank_simple_whitened_modes": simple_full_rank,
        "source_overlap_certificate_numeric": registration.get(
            "source_overlap_certificate_pass"
        )
        is True
        and computed_overlap > 0.0
        and np.isclose(
            float(registration.get("source_overlap_min_singular_value", 0.0)),
            computed_overlap,
            rtol=1e-9,
            atol=1e-11,
        ),
    }
    checks["path_formula_details"] = formula_results
    return all(value for name, value in checks.items() if name != "path_formula_details"), checks


def main() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    sealed = protocol["sealed_endpoint"]
    archive = ROOT / sealed["archive"]
    with tarfile.open(archive, mode="r:gz") as bundle:
        # getnames reads only the tar inventory; extractfile/extract are forbidden here.
        member_names = bundle.getnames()
    exact_member_count = member_names.count(sealed["member"])
    extracted_member = archive.parent / sealed["member"]
    standard_factor_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_standard_path_radiative_factorization_v01.json"
            )
        ),
        {},
    )
    standard_factor = load_optional(
        ROOT / standard_factor_record.get("artifact", "__missing__")
    )
    standard_factor_valid = bool(
        standard_factor.get("schema")
        == "tau-core.paper8.sdp81-standard-path-radiative-factorization.v01"
        and standard_factor.get("status")
        == "STANDARD_PATH_FUNCTIONAL_DERIVED_RADIATIVE_MIXED_JET_OPEN"
        and standard_factor.get("rank") == 4
        and standard_factor.get("per_channel_spatial_nullity") == 45
        and (standard_factor.get("separable_source_control") or {}).get(
            "all_paths_reduce_to_identity"
        )
        is True
        and (standard_factor.get("spatial_spectral_countermodel") or {}).get(
            "parent_loss_present"
        )
        is False
        and (standard_factor.get("checks") or {}).get(
            "no_spectral_or_velocity_endpoint_read"
        )
        is True
        and (standard_factor.get("checks") or {}).get(
            "no_co109_header_or_pixel_read"
        )
        is True
    )
    radiative_rank_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_radiative_mixed_jet_minimal_rank_v01.json"
            )
        ),
        {},
    )
    radiative_rank = load_optional(
        ROOT / radiative_rank_record.get("artifact", "__missing__")
    )
    radiative_rank_valid = bool(
        radiative_rank.get("schema")
        == "tau-core.paper8.sdp81-radiative-mixed-jet-minimal-rank.v01"
        and radiative_rank.get("status")
        == "RADIATIVE_BASIS_EXISTS_TWO_LINE_OPACITY_PROFILE_UNIDENTIFIED"
        and radiative_rank.get("uniform_slab_centered_log_rank", 6) <= 3
        and radiative_rank.get("optically_thin_uniform_slab_rank", 6) <= 2
        and radiative_rank.get("two_component_centered_log_rank") == 5
        and radiative_rank.get("coincident_component_control_rank", 5) < 5
        and radiative_rank.get("two_line_opacity_profile_identified") is False
        and radiative_rank.get("physical_parent_to_gas_bridge_selected") is False
        and all((radiative_rank.get("checks") or {}).values())
    )
    parent_gas_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_parent_gas_conditional_response_v01.json"
            )
        ),
        {},
    )
    parent_gas = load_optional(ROOT / parent_gas_record.get("artifact", "__missing__"))
    parent_gas_proof_checks = {
        key: value
        for key, value in (parent_gas.get("checks") or {}).items()
        if key != "physical_mixed_derivative_selected"
    }
    parent_gas_valid = bool(
        parent_gas.get("schema")
        == "tau-core.paper8.sdp81-parent-gas-conditional-response.v01"
        and parent_gas.get("status")
        == "CONDITIONAL_PARENT_GAS_RESPONSE_DERIVED_PHYSICAL_MIXED_JET_OPEN"
        and parent_gas.get("derived_bridge_rank") == 5
        and parent_gas.get("mixed_derivative_rank") == 5
        and parent_gas.get("backreaction_frobenius_norm", 0.0) > 0.0
        and parent_gas.get("physical_mixed_derivative_selected") is False
        and parent_gas_proof_checks
        and all(parent_gas_proof_checks.values())
        and (parent_gas.get("checks") or {}).get("no_spectral_endpoint_read") is True
        and (parent_gas.get("checks") or {}).get("no_co109_header_or_pixel_read") is True
    )
    symmetry_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_parent_gas_equivariant_intertwiner_v01.json"
            )
        ),
        {},
    )
    symmetry_audit = load_optional(
        ROOT / symmetry_record.get("artifact", "__missing__")
    )
    symmetry_no_go_valid = bool(
        symmetry_audit.get("schema")
        == "tau-core.paper8.sdp81-parent-gas-equivariant-intertwiner.v01"
        and symmetry_audit.get("status")
        == "SYMMETRY_INTERTWINER_SHAPE_DERIVED_CURRENT_SYMMETRIES_NONSELECTING"
        and symmetry_audit.get("p6_reflection_intertwiner_dimension") == 13
        and symmetry_audit.get("hypothetical_s6_commutant_dimension") == 1
        and symmetry_audit.get("two_component_swap_fixed_radiative_rank", 5) < 5
        and symmetry_audit.get("physical_common_representation_owned") is False
        and symmetry_audit.get("physical_susceptibility_anchor_owned") is False
        and all((symmetry_audit.get("checks") or {}).values())
    )
    mediator_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_parent_gas_4d_mediator_factorization_v01.json"
            )
        ),
        {},
    )
    mediator_audit = load_optional(
        ROOT / mediator_record.get("artifact", "__missing__")
    )
    mediator_boundary_valid = bool(
        mediator_audit.get("schema")
        == "tau-core.paper8.sdp81-parent-gas-4d-mediator-factorization.v01"
        and mediator_audit.get("status")
        == "FOUR_D_MEDIATOR_FACTORIZATION_DERIVED_DIRECT_REMAINDER_AND_PHYSICAL_DESCENT_OPEN"
        and mediator_audit.get("mediator_jacobian_rank") == 5
        and mediator_audit.get("derived_bridge_rank") == 5
        and mediator_audit.get("physical_D_Z_e_owned") is False
        and mediator_audit.get("no_direct_coupling_certificate_owned") is False
        and mediator_audit.get("endpoint_authorized") is False
        and all((mediator_audit.get("checks") or {}).values())
    )
    coframe_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_g4d_coframe_parent_gas_mediator_compiler_v01.json"
            )
        ),
        {},
    )
    coframe_audit = load_optional(
        ROOT / coframe_record.get("artifact", "__missing__")
    )
    coframe_compiler_valid = bool(
        coframe_audit.get("schema")
        == "tau-core.paper8.sdp81-g4d-coframe-parent-gas-mediator-compiler.v01"
        and coframe_audit.get("status")
        == "OPACITY_SHAPE_SURVIVAL_DERIVED_SOURCE_PROFILE_OPEN"
        and coframe_audit.get("coframe_metric_rank") == 10
        and coframe_audit.get("coframe_metric_gauge_nullity") == 6
        and coframe_audit.get("D_Z_metric_rank") == 5
        and coframe_audit.get("parent_gas_bridge_rank") == 5
        and coframe_audit.get("B_AZ_rank") == 5
        and coframe_audit.get("I_ZA_rank") == 5
        and coframe_audit.get("schur_backreaction_norm", 0.0) > 0.0
        and coframe_audit.get("current_AORS_D_A_rank") == 4
        and coframe_audit.get("current_AORS_D_Z_metric_rank") == 4
        and coframe_audit.get("minimal_independent_scalar_enrichment_rank") == 5
        and coframe_audit.get("natural_common_volume_enrichment_rank") == 5
        and coframe_audit.get("standard_cold_matter_volume_coupling_nonzero") is True
        and coframe_audit.get("conditional_opacity_shape_terminal_survival_derived") is True
        and coframe_audit.get("physical_channel_opacity_profile_owned") is False
        and coframe_audit.get("physical_I_ZA_owned") is False
        and coframe_audit.get("physical_gas_metric_response_owned") is False
        and coframe_audit.get("endpoint_authorized") is False
        and all((coframe_audit.get("checks") or {}).values())
    )

    pdr_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_rybak2020_source_blind_pdr_preflight_v01.json"
            )
        ),
        {},
    )
    pdr_audit = load_optional(ROOT / pdr_record.get("artifact", "__missing__"))
    pdr_amplitude_prior_valid = bool(
        pdr_audit.get("schema")
        == "tau-core.paper8.sdp81-rybak2020-source-blind-pdr-preflight.v01"
        and pdr_audit.get("status")
        == "SOURCE_ACQUIRED_PDR_AMPLITUDE_PARTIAL_SPECTRAL_REGISTRATION_BLOCKED"
        and (pdr_audit.get("endpoint_access") or {}).get("co109_header_read") is False
        and (pdr_audit.get("endpoint_access") or {}).get("co109_pixels_read") is False
        and (pdr_audit.get("checks") or {}).get("all_source_hashes_match") is True
        and (pdr_audit.get("checks") or {}).get("model_prediction_positive") is True
        and (pdr_audit.get("checks") or {}).get("at_least_one_well_fit_source_pixel") is True
        and (pdr_audit.get("checks") or {}).get(
            "channelwise_spectral_registration_available"
        )
        is False
        and pdr_audit.get("endpoint_authorized") is False
    )

    profile_lift_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_open_transition_profile_lift_gate_v01.json"
            )
        ),
        {},
    )
    profile_lift_audit = load_optional(
        ROOT / profile_lift_record.get("artifact", "__missing__")
    )
    unsafe_profile_inheritance_rejected = bool(
        profile_lift_audit.get("schema")
        == "tau-core.paper8.sdp81-open-transition-profile-lift-gate.v01"
        and profile_lift_audit.get("status")
        == "INHERITED_CO87_PROFILE_LIFT_REJECTED_NEW_SOURCE_SPECTROSCOPY_REQUIRED"
        and profile_lift_audit.get("profile_lift_authorized") is False
        and profile_lift_audit.get("endpoint_authorized") is False
        and (profile_lift_audit.get("checks") or {}).get(
            "official_open_source_maps_have_no_spectral_axis"
        )
        is True
        and (profile_lift_audit.get("checks") or {}).get(
            "three_path_to_fourth_path_transfer_not_established"
        )
        is True
        and (profile_lift_audit.get("checks") or {}).get("co109_header_not_read")
        is True
        and (profile_lift_audit.get("checks") or {}).get("co109_pixels_not_read")
        is True
    )

    visibility_route_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_alma_visibility_source_route_v01.json"
            )
        ),
        {},
    )
    visibility_route = load_optional(
        ROOT / visibility_route_record.get("artifact", "__missing__")
    )
    endpoint_blind_visibility_route_frozen = bool(
        visibility_route.get("schema")
        == "sdp81_alma_visibility_source_route_v01"
        and visibility_route.get("status")
        == "RAW_VISIBILITY_SOURCE_ROUTE_IDENTIFIED_ACQUISITION_NOT_EXECUTED"
        and visibility_route.get("allowed_execution_count") == 21
        and visibility_route.get("allowed_content_length_bytes") == 211709114368
        and visibility_route.get("acquisition_executed") is False
        and visibility_route.get("source_cube_reconstructed") is False
        and visibility_route.get("transition_readiness_increment") == 0
        and visibility_route.get("endpoint_authorized") is False
        and all((visibility_route.get("checks") or {}).values())
    )

    reference_image_route_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_reference_image_source_route_v01.json"
            )
        ),
        {},
    )
    reference_image_route = load_optional(
        ROOT / reference_image_route_record.get("artifact", "__missing__")
    )
    resource_bounded_reference_image_route_frozen = bool(
        reference_image_route.get("schema")
        == "tau-core.paper8.sdp81-reference-image-source-route.v01"
        and reference_image_route.get("status")
        == "LOCAL_REFERENCE_IMAGE_ROUTE_AVAILABLE_DEVELOPMENT_ONLY"
        and reference_image_route.get("total_bytes") == 395928000
        and reference_image_route.get("source_reconstruction_completed") is False
        and reference_image_route.get("transition_readiness_increment") == 0
        and reference_image_route.get("endpoint_authorized") is False
        and all((reference_image_route.get("checks") or {}).values())
    )

    full_arc_inverse_record = next(
        (
            record
            for record in protocol["static_source_inputs"]
            if record["artifact"].endswith(
                "sdp81_full_arc_regularized_source_inversion_v02.json"
            )
        ),
        {},
    )
    full_arc_inverse = load_optional(
        ROOT / full_arc_inverse_record.get("artifact", "__missing__")
    )
    resource_bounded_full_arc_negative_preserved = bool(
        full_arc_inverse.get("schema")
        == "tau-core.paper8.sdp81-full-arc-regularized-source-inversion.v02"
        and full_arc_inverse.get("status")
        == "FULL_ARC_REFERENCE_IMAGE_INVERSION_NOT_PROMOTED"
        and full_arc_inverse.get("development_source_profile_promoted") is False
        and full_arc_inverse.get("transition_readiness_increment") == 0
        and full_arc_inverse.get("co109_header_read") is False
        and full_arc_inverse.get("co109_pixels_read") is False
        and full_arc_inverse.get("endpoint_authorized") is False
        and full_arc_inverse.get(
            "median_held_path_squared_residual_improvement", 1.0
        )
        < 0.05
        and full_arc_inverse.get("matched_minus_wrong_median_improvement", 1.0)
        < 0.01
    )

    static_checks = {
        "protocol_status_is_sealed": protocol["status"]
        == "SOURCE_PROTOCOL_FROZEN_ENDPOINT_SEALED",
        "archive_hash_matches_freeze": sha256(archive) == sealed["archive_sha256"],
        "exact_co109_member_listed_once": exact_member_count == 1,
        "co109_member_not_extracted": not extracted_member.exists(),
        "all_static_source_hashes_match": all(
            valid_artifact(record) for record in protocol["static_source_inputs"]
        ),
        "standard_path_radiative_factorization_valid": standard_factor_valid,
        "radiative_mixed_jet_minimal_rank_audit_valid": radiative_rank_valid,
        "parent_gas_conditional_response_audit_valid": parent_gas_valid,
        "current_symmetries_do_not_select_parent_gas_bridge": symmetry_no_go_valid,
        "four_dimensional_mediator_boundary_audit_valid": mediator_boundary_valid,
        "g4d_coframe_mediator_compiler_boundary_valid": coframe_compiler_valid,
        "source_blind_pdr_amplitude_preflight_valid": pdr_amplitude_prior_valid,
        "unsafe_open_transition_profile_inheritance_rejected": unsafe_profile_inheritance_rejected,
        "endpoint_blind_alma_visibility_source_route_frozen": endpoint_blind_visibility_route_frozen,
        "resource_bounded_reference_image_source_route_frozen": resource_bounded_reference_image_route_frozen,
        "resource_bounded_full_arc_negative_result_preserved": resource_bounded_full_arc_negative_preserved,
        "same_system_not_mislabelled_independent_replication": protocol[
            "held_out_scope"
        ]["independent_source_replication"]
        is False,
        "fits_header_not_read_by_this_gate": True,
        "fits_data_array_not_read_by_this_gate": True,
    }

    dynamic = protocol["required_dynamic_source_inputs"]
    parent_manifest_path = ROOT / dynamic["physical_parent_manifest"]
    parent_gate = load_optional(ROOT / dynamic["parent_path_gate"])
    common_model = load_optional(ROOT / dynamic["common_action_forward_model"])
    terminal_registration = load_optional(ROOT / dynamic["co109_terminal_registration"])
    header_freeze = load_optional(ROOT / dynamic["co109_header_freeze"])

    terminal_registration_valid, terminal_registration_checks = (
        validate_terminal_registration(terminal_registration)
    )
    header_freeze_valid = bool(
        header_freeze.get("schema")
        == "tau-core.paper8.sdp81-co109-header-only-freeze.v01"
        and header_freeze.get("status") == "HEADER_ONLY_EXTRACTION_RULE_FROZEN"
        and header_freeze.get("fits_data_array_read") is False
        and header_freeze.get("velocity_window_rule")
        and header_freeze.get("rebin_rule")
        and header_freeze.get("blank_covariance_rule")
    )
    parent_physical_requirements = parent_gate.get("physical_requirements") or {
        "physical_manifest_header_valid": False,
        "physical_parent_packet_key": False,
        "independent_nature_occupation_evidence": False,
        "typed_parent_hessian_and_projection_packet": False,
        "fiber_basicness_certificate": False,
        "four_occupied_lifts_with_projection_certificates": False,
        "at_least_one_authorization_route_complete": False,
    }
    transition_requirements = {
        "common_action_model_authorized": common_model.get("endpoint_authorized") is True
        and len(common_model.get("compiled_paths", [])) == 4,
        "transfer_semantics_frozen": common_model.get("transfer_semantics")
        in {"fixed_lift_key", "responsive_lift_coordinate"},
        "all_loo_folds_identifiable": (
            common_model.get("leave_one_path_out_identifiability") or {}
        ).get("all_folds_identifiable")
        is True,
        "physical_co109_terminal_registration_frozen": terminal_registration_valid,
        "co109_header_only_extraction_rule_frozen": header_freeze_valid,
        "blind_pdr_integrated_amplitude_prior_available": pdr_amplitude_prior_valid,
    }
    endpoint_authorized = (
        parent_manifest_path.is_file()
        and parent_gate.get("endpoint_authorized") is True
        and all(static_checks.values())
        and all(parent_physical_requirements.values())
        and all(transition_requirements.values())
    )
    result = {
        "schema": "tau-core.paper8.sdp81-co109-common-action-source-gate.v01",
        "status": (
            "SOURCE_FROZEN_CO109_ENDPOINT_AUTHORIZED"
            if endpoint_authorized
            else "FORMULA_FREEZE_PROTOCOL_READY_PHYSICAL_SOURCE_BLOCKED"
        ),
        "scientific_role": "pre-pixel held-out-transition source and physical gate",
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "protocol_sha256": sha256(PROTOCOL),
        "archive_inventory": member_names,
        "sealed_member": sealed["member"],
        "static_checks": static_checks,
        "static_checks_passed": sum(static_checks.values()),
        "static_checks_total": len(static_checks),
        "physical_parent_manifest_present": parent_manifest_path.is_file(),
        "physical_requirements": parent_physical_requirements,
        "physical_requirements_materialized": sum(parent_physical_requirements.values()),
        "physical_requirements_total": len(parent_physical_requirements),
        "transition_readiness_requirements": transition_requirements,
        "terminal_registration_formula_checks": terminal_registration_checks,
        "transition_readiness_materialized": sum(transition_requirements.values()),
        "transition_readiness_total": len(transition_requirements),
        "fits_header_read": False,
        "fits_data_array_read": False,
        "endpoint_authorized": endpoint_authorized,
        "next_permitted_action": (
            "run a separate CO(10-9) endpoint extractor"
            if endpoint_authorized
            else "derive/freeze the physical common-action packet and obtain an author-reduced or independently reconstructed visibility-plane CO(5-4)/CO(8-7) source spectral cube with covariance; the 395.928-MB restored-image full-arc route failed promotion (2.07 percent median LOO improvement, only 0.46 percentage-point matched-minus-reflection separation), while the 211.709-GB raw route remains a later fallback; keep every Band-7/CO(10-9) execution sealed"
        ),
        "claim_boundary": protocol["claim_boundary"],
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 CO(10-9) common-action source gate v01\n\n"
        f"Status: `{result['status']}`. Endpoint authorized: "
        f"`{result['endpoint_authorized']}`.\n\n"
        f"Static sealed-source checks: `{result['static_checks_passed']}/"
        f"{result['static_checks_total']}`. Physical requirements: "
        f"`{result['physical_requirements_materialized']}/"
        f"{result['physical_requirements_total']}`. Transition readiness: "
        f"`{result['transition_readiness_materialized']}/"
        f"{result['transition_readiness_total']}`. Neither the FITS header nor "
        "data array was opened.\n\n"
        f"Next permitted action: {result['next_permitted_action']}.\n\n"
        f"{result['claim_boundary']}\n",
        encoding="utf-8",
    )
    print(result["status"])


if __name__ == "__main__":
    main()
