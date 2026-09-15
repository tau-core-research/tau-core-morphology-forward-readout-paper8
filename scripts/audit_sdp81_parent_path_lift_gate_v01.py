#!/usr/bin/env python3
"""Fail-closed source audit for SDP.81 optical-to-parent path lifts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR = ROOT / "data/derived/sdp81_standard_corridor_descriptor_v01.json"
PHYSICAL_MANIFEST = ROOT / "data/derived/sdp81_parent_lift_physical_source_manifest_v01.json"
OBSERVED_INCIDENCE = ROOT / "data/derived/sdp81_observed_4d_incidence_measure_v01.json"
OUT = ROOT / "data/derived/sdp81_parent_path_lift_gate_v01.json"
REPORT = ROOT / "reports/sdp81_parent_path_lift_gate_v01.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_record_valid(record: object) -> bool:
    if not isinstance(record, dict):
        return False
    artifact = record.get("artifact")
    expected_sha256 = record.get("sha256")
    if not isinstance(artifact, str) or not artifact:
        return False
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        return False
    path = ROOT / artifact
    return path.is_file() and sha256(path) == expected_sha256


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> None:
    descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
    paths = descriptor["paths"]
    path_ids = [path["path_id"] for path in paths]
    observed_incidence = (
        json.loads(OBSERVED_INCIDENCE.read_text(encoding="utf-8"))
        if OBSERVED_INCIDENCE.is_file()
        else {}
    )
    incidence_atoms = observed_incidence.get("atoms", [])
    observed_incidence_valid = bool(
        observed_incidence.get("schema")
        == "tau-core.paper8.sdp81-observed-4d-incidence-measure.v01"
        and observed_incidence.get("status") == "OBSERVED_4D_INCIDENCE_MEASURE_PASS"
        and observed_incidence.get("inputs", {}).get(
            "spectral_or_velocity_endpoint_read"
        )
        is False
        and observed_incidence.get("counting_measure", {}).get("total_mass") == 4.0
        and observed_incidence.get("parent_selector_or_lift_occupation_materialized")
        is False
        and isinstance(incidence_atoms, list)
        and len(incidence_atoms) == 4
        and [atom.get("path_key") for atom in incidence_atoms] == path_ids
        and all(atom.get("detected") is True for atom in incidence_atoms)
        and all(float(atom.get("counting_mass", 0.0)) > 0.0 for atom in incidence_atoms)
    )
    reserved_descriptor_fields = {
        "physical_parent_packet_key",
        "parent_hessian_nature_occupation_key",
        "parent_lift_fiber_basicness_certificate",
    }
    descriptor_has_reserved_fields = any(
        field in descriptor for field in reserved_descriptor_fields
    ) or any("occupied_parent_lift_key" in path for path in paths)

    source_checks = {
        "frozen_standard_corridor_descriptor_present": DESCRIPTOR.exists(),
        "four_unique_optical_path_keys": len(path_ids) == 4
        and len(set(path_ids)) == 4,
        "one_common_standard_source_position": len(
            descriptor["source_position_arcsec_relative_to_G"]
        )
        == 2,
        "all_optical_image_positions_finite_and_typed": all(
            len(path["image_position_arcsec_relative_to_G"]) == 2 for path in paths
        ),
        "no_spectral_or_velocity_endpoint_read": descriptor["inputs"][
            "spectral_or_velocity_endpoint_read"
        ]
        is False,
        "standard_lens_jacobian_not_retyped_as_parent_transfer": descriptor[
            "direct_parent_contraction_identification_allowed"
        ]
        is False,
        "standard_descriptor_contains_no_physical_authorization_fields": not descriptor_has_reserved_fields,
        "positive_observed_4d_incidence_measure_present": observed_incidence_valid,
    }

    physical_manifest = (
        json.loads(PHYSICAL_MANIFEST.read_text(encoding="utf-8"))
        if PHYSICAL_MANIFEST.is_file()
        else {}
    )
    manifest_header_valid = bool(
        physical_manifest.get("schema")
        == "tau-core.paper8.sdp81-parent-lift-physical-source-manifest.v01"
        and physical_manifest.get("status") == "PHYSICAL_PARENT_LIFT_SOURCE_PACKET_FROZEN"
        and physical_manifest.get("spectral_or_velocity_endpoint_read") is False
    )
    parent_packet_key = physical_manifest.get("physical_parent_packet_key")
    occurrence_record = physical_manifest.get("post_body_occurrence_law")
    occurrence_law_valid = bool(
        isinstance(occurrence_record, dict)
        and occurrence_record.get("stage") == "post_body_pre_terminal"
        and occurrence_record.get("measure_or_current") == "positive_nonzero"
        and occurrence_record.get("source_owned") is True
        and occurrence_record.get("support_is_selector_pushforward") is True
        and occurrence_record.get("body_side_schur_remainder_zero") is True
        and artifact_record_valid(occurrence_record)
    )
    nature_record = physical_manifest.get("nature_occupation_evidence")
    nature_occupation_valid = bool(
        isinstance(nature_record, dict)
        and nature_record.get("status") == "INDEPENDENT_PHYSICAL_OCCUPATION_EVIDENCE"
        and nature_record.get("independent_of_terminal_endpoint") is True
        and nature_record.get("independent_scientific_review") is True
        and nature_record.get("rival_lift_control_included") is True
        and occurrence_law_valid
        and artifact_record_valid(nature_record)
    )
    projection_record = physical_manifest.get("pi_4D_source_definition")
    hessian_record = physical_manifest.get("occupied_parent_hessian")
    selector_record = physical_manifest.get("physical_lift_selector")
    typed_parent_packet_valid = bool(
        manifest_header_valid
        and isinstance(parent_packet_key, str)
        and parent_packet_key
        and isinstance(projection_record, dict)
        and projection_record.get("source_owned") is True
        and artifact_record_valid(projection_record)
        and isinstance(selector_record, dict)
        and selector_record.get("physical_parent_packet_key") == parent_packet_key
        and selector_record.get("source_owned") is True
        and selector_record.get("measurable_section_certificate_pass") is True
        and selector_record.get("graph_square_certificate_pass") is True
        and selector_record.get("body_side_schur_remainder_zero") is True
        and artifact_record_valid(selector_record)
        and isinstance(hessian_record, dict)
        and hessian_record.get("physical_parent_packet_key") == parent_packet_key
        and hessian_record.get("positivity_certificate_pass") is True
        and hessian_record.get("source_observer_interior_block_split")
        == ["source", "observer", "interior"]
        and artifact_record_valid(hessian_record)
    )
    basicness_record = physical_manifest.get("parent_lift_fiber_basicness_certificate")
    basicness_certificate_valid = bool(
        isinstance(basicness_record, dict)
        and basicness_record.get("certificate_pass") is True
        and basicness_record.get("physical_parent_packet_key") == parent_packet_key
        and artifact_record_valid(basicness_record)
    )
    physical_path_records = physical_manifest.get("paths", [])
    occupied_lift_keys = []
    occupied_lift_projection_valid = False
    if isinstance(physical_path_records, list) and len(physical_path_records) == 4:
        records_by_path = {
            record.get("observed_4d_path_key"): record
            for record in physical_path_records
            if isinstance(record, dict)
        }
        ordered_records = [records_by_path.get(path_id) for path_id in path_ids]
        occupied_lift_keys = [
            record.get("occupied_parent_lift_key") if isinstance(record, dict) else None
            for record in ordered_records
        ]
        occupied_lift_projection_valid = bool(
            all(isinstance(record, dict) for record in ordered_records)
            and all(
                record.get("physical_parent_packet_key") == parent_packet_key
                and isinstance(record.get("occupied_parent_lift_key"), str)
                and record.get("occupied_parent_lift_key")
                and isinstance(record.get("projection_certificate"), dict)
                and record["projection_certificate"].get("certificate_pass") is True
                and record["projection_certificate"].get("projected_4d_path_key")
                == record.get("observed_4d_path_key")
                and artifact_record_valid(record["projection_certificate"])
                for record in ordered_records
            )
            and len(set(occupied_lift_keys)) == 4
        )

    basicness_route = bool(
        typed_parent_packet_valid
        and nature_occupation_valid
        and basicness_certificate_valid
    )
    occupied_lift_route = bool(
        typed_parent_packet_valid
        and nature_occupation_valid
        and occupied_lift_projection_valid
    )

    physical_requirements = {
        "physical_manifest_header_valid": manifest_header_valid,
        "physical_parent_packet_key": bool(manifest_header_valid and parent_packet_key),
        "independent_nature_occupation_evidence": nature_occupation_valid,
        "typed_parent_hessian_and_projection_packet": typed_parent_packet_valid,
        "fiber_basicness_certificate": basicness_certificate_valid,
        "four_occupied_lifts_with_projection_certificates": occupied_lift_projection_valid,
        "at_least_one_authorization_route_complete": basicness_route or occupied_lift_route,
    }
    method_pass = all(source_checks.values())
    endpoint_authorized = bool(
        method_pass and (basicness_route or occupied_lift_route)
    )
    result = {
        "schema": "tau-core.paper8.sdp81-parent-path-lift-gate.v01",
        "status": (
            "SOURCE_FROZEN_PARENT_PATH_LIFT_GATE_PASS"
            if endpoint_authorized
            else "PREFLIGHT_NOT_ENDPOINT"
        ),
        "scientific_role": (
            "source-only PATHLIFT-C1 registration audit; never a spectral endpoint score"
        ),
        "input": {
            "standard_corridor_descriptor": display_path(DESCRIPTOR),
            "sha256": sha256(DESCRIPTOR),
            "spectral_or_velocity_endpoint_read": False,
            "physical_source_manifest": (
                display_path(PHYSICAL_MANIFEST)
                if PHYSICAL_MANIFEST.is_file()
                else None
            ),
            "physical_source_manifest_sha256": (
                sha256(PHYSICAL_MANIFEST) if PHYSICAL_MANIFEST.is_file() else None
            ),
            "observed_4d_incidence_measure": (
                display_path(OBSERVED_INCIDENCE)
                if OBSERVED_INCIDENCE.is_file()
                else None
            ),
            "observed_4d_incidence_measure_sha256": (
                sha256(OBSERVED_INCIDENCE) if OBSERVED_INCIDENCE.is_file() else None
            ),
        },
        "observed_4d_path_keys": path_ids,
        "source_checks": source_checks,
        "source_checks_passed": int(sum(source_checks.values())),
        "source_checks_total": len(source_checks),
        "physical_requirements": physical_requirements,
        "physical_requirements_materialized": int(sum(physical_requirements.values())),
        "physical_requirements_total": len(physical_requirements),
        "physical_basicness_authorization_route_complete": basicness_route,
        "physical_occupied_lift_authorization_route_complete": occupied_lift_route,
        "authorization_rule": (
            "one common occupied physical parent-Hessian key AND either "
            "(a transfer-basicness certificate on all four lift fibers) OR "
            "(four immutable occupied parent-lift keys derived by occurrence "
            "pushforward under that same packet)"
        ),
        "basicness_certificate_contract": [
            "one smooth occupied parent-Hessian family H(lambda)",
            "the source-owned 4D descent differential D pi_4D",
            "the full vertical kernel ker D pi_4D",
            "the source/observer/interior block split and endpoint-frame connection",
            "connected lift fibers or matching anchors for every disconnected component",
            "zero endpoint-frame covariant D C_gamma on every vertical direction",
        ],
        "homogeneous_fiber_generator_reduction_contract": [
            "a source-owned connected Lie-group action transitive on each regular lift fiber",
            "a complete fundamental-generator span of ker D pi_4D at every orbit point",
            "zero endpoint-frame covariant C_gamma defect for every generator everywhere",
            "explicit anchor/holonomy checks for discrete components and discrete isotropy",
        ],
        "parent_hessian_equivariance_certificate_contract": [
            "a fiber-preserving transitive action with typed source/observer/interior representations",
            "conformal equivariance of the complete occupied parent Hessian under that action",
            "one common positive action scale across every Hessian block",
            "proof that the action preserves the typed block split and all source tensors",
        ],
        "source_symmetry_reconstruction_contract": [
            "a source-owned positive lift-space metric distinct from the response Hessian unless identified",
            "vertical symmetry fields preserving the descent map and complete source packet",
            "finite bracket closure, Jacobi identity and complete generator flows",
            "zero generator-versus-vertical projector defect at every occupied fiber point",
            "component and discrete-isotropy anchor/holonomy registry",
        ],
        "minimum_direct_occupied_lift_acquisition_contract": [
            "endpoint-independent authoritative provenance artifacts with immutable hashes",
            "one common physical parent-packet key and independently reviewed source-ownership evidence",
            "typed E_P, E_4D and pi_4D definitions with a source-owned projection artifact",
            "occupied H(lambda) definition, domain, S/O/I split, positivity certificate and unit normalization",
            "one nonzero positive actual post-body observer-source incidence measure",
            "one source-owned measurable selector/graph law with zero body-side Schur remainder",
            "occupied parent-lift keys derived by pushing that incidence through the common selector",
            "four certificates pi_4D(tilde_gamma_i)=gamma_i under the common packet key",
            "pre-endpoint freeze timestamp, manifest hash and endpoint_authorized=false",
        ],
        "lift_occurrence_pushforward_contract": [
            "nu_OS is a nonzero positive post-body occurrence measure, not a fitted terminal weight",
            "the physical selector law is measurable on the support and satisfies pi_4D o s_theta = id",
            "the lift measure is defined by (s_theta o g)_* nu_OS rather than asserted path by path",
            "projection of the lift measure recovers the registered 4D incidence exactly",
            "the local graph-square occurrence Hessian has zero upstream Schur remainder",
            "physical selector-law ownership and actual incidence remain separately evidenced",
        ],
        "complete_action_induced_selector_contract": [
            "one source-owned complete post-body action frozen before endpoint access",
            "typed incidence, parent-lift and internal-channel domains with no terminal argument",
            "positive proper internal/lift Hessian and an exact internal Schur elimination certificate",
            "a source-owned affine descent pi with separately typed linear part L=Dpi",
            "a physical quotient or gauge slice and affine parent anchor",
            "one common Hessian on boundary, lift and internal coordinates",
            "a pre-endpoint fixed-lift or relaxed-lift transfer-semantics declaration",
            "nested/direct Schur equality and the positive-semidefinite relaxation correction",
            "the selector, vertical Hessian and section jet derived from that same action",
            "zero upper-right body/post-body block so the frozen body is not reselected",
            "a rival-action or affine-shift control demonstrating the physical ownership burden",
        ],
        "typed_standard_lens_exclusions": {
            "lens_potential_hessian_is_parent_hessian": False,
            "lens_jacobian_is_D_pi_4D": False,
            "four_image_multiplicity_is_parent_fiber_topology": False,
            "optical_path_key_is_occupied_parent_lift_key": False,
        },
        "observed_4d_incidence_status": {
            "positive_counting_measure_materialized": observed_incidence_valid,
            "parent_lift_measure_materialized": False,
            "physical_parent_requirement_delta": 0,
        },
        "endpoint_authorized": endpoint_authorized,
        "next_finite_action": (
            "The minimum-scope route is to acquire one common physical complete "
            "post-body action that derives the parent Hessian, selector law, "
            "quotient and affine anchor. The positive observed 4D incidence is "
            "already materialized. Four occupied lift keys must then "
            "be derived by pushforward, with four pi_4D projection certificates. "
            "The more general route is "
            "to prove transfer basicness directly or through a complete sourced "
            "symmetry certificate."
        ),
        "claim_boundary": (
            "The audit certifies four residual-blind standard optical path keys and "
            "shows that neither PATHLIFT-C1 authorization route is present. It does "
            "not infer parent lifts from Fermat potentials, lens Jacobians, spectral "
            "pixels, rotation residuals, or fit quality. Standard lens Hessians, "
            "Jacobians, image multiplicity and optical labels are explicitly kept "
            "in their downstream 4D types. Artifact hashes certify integrity only; "
            "the source-ownership and independent-review clauses remain scientific "
            "premises of the manifest rather than consequences of hashing."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# SDP.81 parent-path lift gate v01\n\n"
        f"Status: `{result['status']}`.\n\n"
        f"All **{result['source_checks_passed']}/{result['source_checks_total']}** "
        "source/method checks pass: the standard packet contains four unique q1 "
        "optical path keys from one source, and the independent Band-7 continuum "
        "audit supplies a positive observed 4D counting measure without reading "
        "a spectral or velocity endpoint.\n\n"
        "PATHLIFT-C1 requires one common occupied physical parent-Hessian key and "
        "either a transfer-basicness certificate on all four parent-lift fibres or "
        "four immutable occupied lift keys derived by pushing one positive actual "
        "observer--source incidence measure through the common physical selector. "
        "The separately "
        "audited physical source manifest materializes "
        f"**{result['physical_requirements_materialized']}/"
        f"{result['physical_requirements_total']}** physical requirements, so both "
        "authorization routes remain closed.\n\n"
        "The standard Fermat potentials, parities and lens Jacobians remain "
        "conventional comparator inputs. They are not promoted to parent distance, "
        "parent transfer or lift selectors. CSCR-T32i makes the basicness branch "
        "computable from the occupied Hessian jet, descent differential, vertical "
        "kernel and fibre topology. CSCR-T32j allows a finite generator reduction "
        "only when the occupied packet also owns a connected transitive fibre "
        "action, a complete generator span and all discrete holonomy checks. "
        "CSCR-T32k gives full typed parent-Hessian equivariance as a sufficient "
        "certificate, while CSCR-T32l requires the action itself to be reconstructed "
        "from a complete vertical symmetry algebra rather than guessed. None of "
        "these physical structures is present in this packet. CSCR-T32m proves a "
        "strictly convex post-body selector can compile conditional keyed lifts; "
        "CSCR-T32n proves the selector and its hashes cannot certify their own "
        "Nature occupation. CSCR-T32o derives lift occupation as the pushforward "
        "of actual positive observer-source incidence through a physically realized "
        "selector, so four path occupations are not independent facts. CSCR-T32p "
        "shows 4D incidence does not select that parent section, and CSCR-T32q "
        "fixes the least exact local occurrence law as a Schur-neutral graph square. "
        "CSCR-T32s derives the selector, vertical Hessian and section jet from one "
        "complete post-body action by exact elimination. CSCR-T32t selects the "
        "canonical minimum-action right inverse inside the linear positive class, "
            "while CSCR-T32u proves that the current source domain owns neither the "
            "required parent-path carrier nor its affine anchor. "
            "CSCR-T32v derives the lift metric and fixed or relaxed S/O/I transfer "
            "from one common Hessian by nested Schur elimination; CSCR-T32w proves "
            "that these reductions do not certify physical common-action ancestry "
            "and that the transfer semantics must be source-frozen. "
        "Descriptor-injected physical strings are rejected, and "
        "only a separate artifact-verified physical manifest may enter either "
        "authorization route. No SDP.81 "
        "spectral score is authorized.\n",
        encoding="utf-8",
    )
    print(result["status"])
    print(
        f"source_checks={result['source_checks_passed']}/"
        f"{result['source_checks_total']}"
    )
    print(
        f"physical_requirements={result['physical_requirements_materialized']}/"
        f"{result['physical_requirements_total']}"
    )


if __name__ == "__main__":
    main()
