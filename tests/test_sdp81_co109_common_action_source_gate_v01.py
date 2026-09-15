from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_sdp81_co109_common_action_source_gate_v01 import (  # noqa: E402
    validate_terminal_registration,
)


def test_co109_protocol_is_sealed_and_not_independent_replication() -> None:
    protocol = json.loads(
        (ROOT / "data/protocols/sdp81_co109_common_action_confirmatory_protocol_v01.json").read_text()
    )
    assert protocol["status"] == "SOURCE_PROTOCOL_FROZEN_ENDPOINT_SEALED"
    assert protocol["held_out_scope"]["repository_unopened_transition"] is True
    assert protocol["held_out_scope"]["independent_source_replication"] is False
    assert protocol["sealed_endpoint"]["fits_data_array_read_before_physical_gate"] is False
    assert protocol["endpoint_score_contract"]["no_post_endpoint_retuning"] is True


def test_preserved_co109_gate_is_fail_closed_without_pixel_access() -> None:
    gate = json.loads(
        (ROOT / "data/derived/sdp81_co109_common_action_source_gate_v01.json").read_text()
    )
    assert gate["status"] == "FORMULA_FREEZE_PROTOCOL_READY_PHYSICAL_SOURCE_BLOCKED"
    assert gate["static_checks_passed"] == gate["static_checks_total"] == 19
    assert gate["static_checks"][
        "endpoint_blind_alma_visibility_source_route_frozen"
    ] is True
    assert gate["static_checks"][
        "resource_bounded_full_arc_negative_result_preserved"
    ] is True
    assert gate["static_checks"][
        "resource_bounded_reference_image_source_route_frozen"
    ] is True
    assert gate["physical_requirements_materialized"] == 0
    assert gate["physical_requirements_total"] == 7
    assert gate["transition_readiness_materialized"] == 1
    assert gate["transition_readiness_total"] == 6
    assert gate["transition_readiness_requirements"][
        "blind_pdr_integrated_amplitude_prior_available"
    ] is True
    assert gate["fits_header_read"] is False
    assert gate["fits_data_array_read"] is False
    assert gate["endpoint_authorized"] is False


def test_source_blind_pdr_preflight_is_partial_and_endpoint_sealed() -> None:
    audit = json.loads(
        (ROOT / "data/derived/sdp81_rybak2020_source_blind_pdr_preflight_v01.json").read_text()
    )
    assert audit["data"]["all_five_tracer_pixels"] == 288
    assert audit["fit_summary"]["well_fit_chi2red_below_5_pixels"] == 80
    assert audit["endpoint_access"] == {
        "co109_header_read": False,
        "co109_pixels_read": False,
    }
    assert audit["checks"]["all_source_hashes_match"] is True
    assert audit["checks"]["channelwise_spectral_registration_available"] is False
    assert audit["endpoint_authorized"] is False


def test_unsafe_open_transition_profile_inheritance_is_rejected() -> None:
    gate = json.loads(
        (ROOT / "data/derived/sdp81_co109_common_action_source_gate_v01.json").read_text()
    )
    assert gate["static_checks"][
        "unsafe_open_transition_profile_inheritance_rejected"
    ] is True


def test_self_asserted_terminal_registration_fails_formula_gate() -> None:
    valid, checks = validate_terminal_registration(
        {
            "schema": "tau-core.paper8.sdp81-co109-parent-terminal-registration.v01",
            "status": "PHYSICAL_PARENT_TO_CO109_TERMINAL_REGISTRATION_FROZEN",
            "source_owned": True,
            "endpoint_pixel_read": False,
            "mode_dimension": 5,
            "orientation_and_permutation_fixed": True,
            "source_overlap_certificate_pass": True,
        }
    )
    assert valid is False
    assert checks["four_path_pullback_formulas_reproduced"] is False
    assert checks["source_provenance_hashes_valid"] is False


def test_complete_synthetic_pullback_packet_passes_structure_gate() -> None:
    protocol = json.loads(
        (ROOT / "data/protocols/sdp81_co109_common_action_confirmatory_protocol_v01.json").read_text()
    )
    provenance = protocol["static_source_inputs"][0]
    basis = np.zeros((6, 5))
    for column in range(5):
        norm = np.sqrt((column + 1) * (column + 2))
        basis[: column + 1, column] = 1.0 / norm
        basis[column + 1, column] = -(column + 1) / norm
    response = np.diag([0.2, 0.3, 0.4, 0.5, 0.6])
    packet = {
        "schema": "tau-core.paper8.sdp81-co109-parent-terminal-registration.v01",
        "status": "PHYSICAL_PARENT_TO_CO109_TERMINAL_REGISTRATION_FROZEN",
        "source_owned": True,
        "endpoint_pixel_read": False,
        "mode_dimension": 5,
        "orientation_and_permutation_fixed": True,
        "mode_orientation_rule": "first nonzero source-overlap component positive",
        "mode_permutation_rule": "decreasing whitened singular value",
        "source_overlap_certificate_pass": True,
        "source_overlap_min_singular_value": 0.2,
        "source_provenance": [provenance],
        "source_action_jet": {
            "H_Z": np.eye(5).tolist(),
            "B_ZC": (-response).tolist(),
            "K_C": np.eye(5).tolist(),
        },
        "conditional_parent_gas_response": {
            "H_xi": np.eye(5).tolist(),
            "B_xiZ": (-np.eye(5)).tolist(),
            "P": np.eye(5).tolist(),
            "bridge_origin": "four_dimensional_mediator",
            "environment_tangent_dimension": 5,
            "D_Z_e": np.eye(5).tolist(),
            "B_xi_e": (-np.eye(5)).tolist(),
            "environment_descriptor_is_gauge_quotiented": True,
            "no_direct_Z_xi_mixed_derivative": True,
            "baseline_gas_state": np.zeros(5).tolist(),
            "post_body_response_frozen_before_gas_solve": True,
            "source_owned": True,
        },
        "path_calibrations": [
            {
                "path_id": f"q1_path_{index}",
                "radiative_lens_instrument_forward": {
                    "baseline_flux": np.ones(6).tolist(),
                    "centered_channel_basis": basis.tolist(),
                    "gas_to_flux_jacobian": basis.tolist(),
                    "raw_flux_jacobian": basis.tolist(),
                },
                "calibration": {
                    "centered_log_covariance": np.eye(5).tolist(),
                    "composite_parent_to_terminal_jacobian": response.tolist(),
                    "whitened_operator": response.tolist(),
                },
            }
            for index in range(1, 5)
        ],
    }
    valid, checks = validate_terminal_registration(packet)
    assert valid is True
    assert all(value for key, value in checks.items() if key != "path_formula_details")
    assert len(checks["path_formula_details"]) == 4

    gas = packet["conditional_parent_gas_response"]
    gas["bridge_origin"] = "direct_conditional_cross_derivative"
    gas["direct_cross_derivative_source_owned"] = True
    for key in (
        "environment_tangent_dimension",
        "D_Z_e",
        "B_xi_e",
        "environment_descriptor_is_gauge_quotiented",
        "no_direct_Z_xi_mixed_derivative",
    ):
        gas.pop(key)
    direct_valid, direct_checks = validate_terminal_registration(packet)
    assert direct_valid is True
    assert direct_checks["parent_gas_bridge_origin_reproduced"] is True
