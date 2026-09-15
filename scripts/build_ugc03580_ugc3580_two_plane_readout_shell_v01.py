#!/usr/bin/env python3
"""Derive an endpoint-blind bounded two-plane readout shell for UGC03580."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from two_plane_morphology_common_v01 import (
    fixed_inclination_projection_ratio_sq,
    plane_defect,
    slerp,
    two_plane_barycentric_kernel,
    unit_rows,
)


ROOT = Path(__file__).resolve().parents[1]
BODY_SUMMARY = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_body_v01.json"
BODY_POINTS = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_body_v01_points.csv"
POINTS_OUT = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_readout_shell_v01_points.csv"
SUMMARY_OUT = ROOT / "data" / "derived" / "ugc03580_ugc3580_two_plane_readout_shell_v01.json"
REPORT_OUT = ROOT / "reports" / "ugc03580_ugc3580_two_plane_readout_shell_v01.md"

EXPECTED_BODY_SUMMARY_SHA256 = "b9a831f1166b908c6df084a39fbb2183f7a9e7337142aa5d228c27e166bd0048"
EXPECTED_BODY_POINTS_SHA256 = "d196498ee6068a306a7391e0ec0fc58885c5536aa56fd68cd290a9094f4a5173"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonicalize_float_tree(value: object) -> object:
    """Remove sub-tolerance noise and stabilize serialized audit floats."""

    if isinstance(value, (float, np.floating)):
        scalar = float(value)
        if abs(scalar) < 1.0e-12:
            return 0.0
        return float(f"{scalar:.12g}")
    if isinstance(value, dict):
        return {key: canonicalize_float_tree(item) for key, item in value.items()}
    if isinstance(value, list):
        return [canonicalize_float_tree(item) for item in value]
    return value


def vector(record: dict[str, float]) -> np.ndarray:
    return np.array([record["n_w"], record["n_n"], record["n_los"]], dtype=float)


def solve_slerp_k1_level(
    left: np.ndarray,
    right: np.ndarray,
    inner: np.ndarray,
    outer: np.ndarray,
    target: float,
    *,
    tolerance: float = 1.0e-14,
    maximum_iterations: int = 160,
) -> tuple[float, np.ndarray, float]:
    """Locate a declared K1 level on one source-owned SLERP segment."""

    if not 0.0 < target < 1.0:
        raise ValueError("the audit target must lie strictly inside (0,1)")

    def residual(fraction: float) -> float:
        normal = slerp(left, right, fraction)
        value = float(
            two_plane_barycentric_kernel(
                normal[None, :], inner, outer, power=1.0
            )[0]
        )
        return value - target

    low = 0.0
    high = 1.0
    f_low = residual(low)
    f_high = residual(high)
    if f_low == 0.0:
        return low, slerp(left, right, low), 0.0
    if f_high == 0.0:
        return high, slerp(left, right, high), 0.0
    if f_low * f_high > 0.0:
        raise ValueError("the declared source segment does not bracket the K1 level")

    for _ in range(maximum_iterations):
        middle = 0.5 * (low + high)
        f_middle = residual(middle)
        if abs(f_middle) <= tolerance or high - low <= tolerance:
            normal = slerp(left, right, middle)
            return middle, normal, f_middle
        if f_low * f_middle <= 0.0:
            high = middle
        else:
            low = middle
            f_low = f_middle
    raise RuntimeError("K1 level solver did not converge")


def main() -> None:
    summary_hash = sha256(BODY_SUMMARY)
    points_hash = sha256(BODY_POINTS)
    if summary_hash != EXPECTED_BODY_SUMMARY_SHA256:
        raise RuntimeError("two-plane body summary hash mismatch")
    if points_hash != EXPECTED_BODY_POINTS_SHA256:
        raise RuntimeError("two-plane body points hash mismatch")

    body = json.loads(BODY_SUMMARY.read_text(encoding="utf-8"))
    points = pd.read_csv(BODY_POINTS)
    if body.get("status") != "SOURCE_ACQUISITION_ONLY":
        raise RuntimeError("unexpected body status")
    if body.get("endpoint_allowed") is not False:
        raise RuntimeError("upstream body must remain endpoint blocked")
    # A source-internal orientation reconstruction residual is a legitimate
    # geometry QA field.  Reject only terminal/rotation-bearing residuals and
    # explicit endpoint schemas here.
    forbidden = (
        "vobs",
        "vrot",
        "rotmod",
        "sparc",
        "velocity_residual",
        "rotation_residual",
        "terminal_residual",
        "empirical_residual",
    )
    contaminated = [
        column
        for column in points.columns
        if any(token in column.lower() for token in forbidden)
    ]
    if contaminated:
        raise RuntimeError(f"endpoint-bearing body columns are forbidden: {contaminated}")

    normals = points[["n_w_orientation", "n_n_orientation", "n_los_orientation"]].to_numpy(
        dtype=float
    )
    inner_record = body["construction"]["inner_reference_plane"]
    outer_record = body["construction"]["outer_mean_plane"]
    inner = vector(inner_record)
    outer = vector(outer_record)
    transverse = unit_rows(np.cross(inner, outer)[None, :])[0]
    d_inner = plane_defect(normals, inner)
    d_outer = plane_defect(normals, outer)
    signed_chirality = normals @ transverse
    anchor_gram = np.array([[1.0, inner @ outer], [inner @ outer, 1.0]], dtype=float)
    anchor_projections = np.column_stack((1.0 - d_inner, 1.0 - d_outer))
    chirality_sq_from_defects = 1.0 - np.einsum(
        "ni,ij,nj->n",
        anchor_projections,
        np.linalg.inv(anchor_gram),
        anchor_projections,
    )
    kernel_p1 = two_plane_barycentric_kernel(normals, inner, outer, power=1.0)
    kernel_p2 = two_plane_barycentric_kernel(normals, inner, outer, power=2.0)

    plane_defect_separation = 1.0 - float(np.clip(np.dot(inner, outer), -1.0, 1.0))
    geometric_amplitude = 0.5 * plane_defect_separation
    response_plus = 1.0 + geometric_amplitude * kernel_p1
    response_minus = 1.0 - geometric_amplitude * kernel_p1
    projection_ratio_sq = fixed_inclination_projection_ratio_sq(
        points["inclination_deg"].to_numpy(dtype=float),
        float(inner_record["inclination_deg"]),
    )
    reflected_normals = normals - 2.0 * signed_chirality[:, None] * transverse[None, :]
    reflected_normals = unit_rows(reflected_normals)
    mirror_projection_ratio_sq = (
        1.0 - reflected_normals[:, 2] ** 2
    ) / np.sin(np.deg2rad(float(inner_record["inclination_deg"]))) ** 2
    mirror_projection_difference = mirror_projection_ratio_sq - projection_ratio_sq
    mirror_projection_difference_analytic = (
        4.0
        * signed_chirality
        * transverse[2]
        * (normals[:, 2] - signed_chirality * transverse[2])
        / np.sin(np.deg2rad(float(inner_record["inclination_deg"]))) ** 2
    )

    # K1 is not merely incomplete on abstract mirror fibres.  The frozen
    # piecewise-SLERP source path itself revisits the same K1 level on two
    # disjoint radial segments.  The targets below are source-side sensitivity
    # controls fixed without reading any rotation endpoint.
    radius = points["radius_arcsec"].to_numpy(dtype=float)
    radius_index = {float(value): index for index, value in enumerate(radius)}
    collision_segments = ((210.0, 240.0), (270.0, 300.0))
    collision_targets = (0.900, 0.925, 0.950)
    collision_records = []
    for target in collision_targets:
        roots = []
        for radius_left, radius_right in collision_segments:
            index_left = radius_index[radius_left]
            index_right = radius_index[radius_right]
            fraction, normal, residual = solve_slerp_k1_level(
                normals[index_left],
                normals[index_right],
                inner,
                outer,
                target,
            )
            root_radius = radius_left + fraction * (radius_right - radius_left)
            root_projection = float(
                (1.0 - normal[2] ** 2)
                / np.sin(np.deg2rad(float(inner_record["inclination_deg"]))) ** 2
            )
            roots.append(
                {
                    "segment_arcsec": [radius_left, radius_right],
                    "fraction": fraction,
                    "radius_arcsec": root_radius,
                    "K1": target + residual,
                    "K1_residual": residual,
                    "chi": float(normal @ transverse),
                    "projection_ratio_sq": root_projection,
                }
            )
        collision_records.append(
            {
                "target_K1": target,
                "roots": roots,
                "radial_separation_arcsec": roots[1]["radius_arcsec"]
                - roots[0]["radius_arcsec"],
                "projection_difference": roots[1]["projection_ratio_sq"]
                - roots[0]["projection_ratio_sq"],
                "chi_difference": roots[1]["chi"] - roots[0]["chi"],
            }
        )
    collision_witness = next(
        record for record in collision_records if record["target_K1"] == 0.925
    )

    result_points = points[
        ["radius_arcsec", "radius_kpc_source", "zone", "within_source_terminal_support"]
    ].copy()
    result_points["defect_to_inner_plane"] = d_inner
    result_points["defect_to_outer_plane"] = d_outer
    result_points["signed_two_plane_chirality_control"] = signed_chirality
    result_points["chirality_sq_from_raw_defects"] = chirality_sq_from_defects
    result_points["kernel_p1_affine_defect_candidate"] = kernel_p1
    result_points["kernel_p2_counterfamily_control"] = kernel_p2
    result_points["geometry_only_response_factor_plus_candidate"] = response_plus
    result_points["geometry_only_response_factor_minus_candidate"] = response_minus
    result_points["fixed_inner_inclination_projection_ratio_sq_control"] = projection_ratio_sq
    result_points["mirror_reflected_n_los_control"] = reflected_normals[:, 2]
    result_points[
        "mirror_fixed_inner_inclination_projection_ratio_sq_control"
    ] = mirror_projection_ratio_sq
    result_points[
        "mirror_minus_source_projection_ratio_sq_control"
    ] = mirror_projection_difference
    result_points["endpoint_values_used"] = False

    supported = result_points["within_source_terminal_support"].to_numpy(dtype=bool)
    transition = result_points["zone"].eq("transition").to_numpy()
    p_witness = float(np.max(np.abs(kernel_p1[transition] - kernel_p2[transition])))
    sign_witness = float(np.max(response_plus[supported] - response_minus[supported]))
    supported_indices = np.flatnonzero(supported)
    mirror_witness_index = int(
        supported_indices[
            np.argmax(np.abs(mirror_projection_difference[supported]))
        ]
    )

    summary = {
        "schema": "tau_core_ugc03580_ugc3580_two_plane_readout_shell_v01",
        "status": "FORMULA_SHELL_DERIVED_ENDPOINT_BLOCKED",
        "galaxy": "UGC03580",
        "alias": "UGC3580",
        "upstream_body": {
            "summary_path": str(BODY_SUMMARY.relative_to(ROOT)),
            "summary_sha256": summary_hash,
            "points_path": str(BODY_POINTS.relative_to(ROOT)),
            "points_sha256": points_hash,
            "descriptor_type": body["descriptor_type"],
        },
        "derived_morphology_coordinate": {
            "plane_defects": "d_in=1-n_in dot n(R); d_out=1-n_out dot n(R)",
            "family": "K_p=d_in^p/(d_in^p+d_out^p), p>0",
            "primary_candidate": "K_1=d_in/(d_in+d_out)",
            "primary_candidate_status": "minimal affine-defect convention, not a physical selection",
            "bounds": "0<=K_p<=1",
            "inner_limit": "K_p(n_in)=0 for distinct reference planes",
            "outer_limit": "K_p(n_out)=1 for distinct reference planes",
            "plane_swap": "K_p(n;n_out,n_in)=1-K_p(n;n_in,n_out)",
            "coincident_plane_policy": "K_p=0: no active two-plane morphology",
        },
        "exact_registration_fibre": {
            "transverse_axis": "c=(n_in x n_out)/|n_in x n_out|",
            "signed_control": "chi(R)=c dot n(R)",
            "raw_fibre": "D=(d_in,d_out) generically identifies a two-point mirror pair with chi -> -chi",
            "identity": "chi^2=1-p^T G_anchor^{-1}p, p=(1-d_in,1-d_out)",
            "complete_oriented_descriptor": "D_hat=(d_in,d_out,chi)",
            "source_orientation_evidence": (
                "Jozsa (2007) Table 6 publishes the Cartesian components of "
                "the oriented spin normal (toward west, north, and the observer), and "
                "the UGC3580 captions identify the approaching side as southeast"
            ),
            "terminal_null_test": "every claimed terminal must be equal on exact mirror fibres before chi is quotiented",
            "complete_projection_stack_decision": "RETAIN_CHI",
            "projection_visibility_reason": (
                "the standard fixed-inner-inclination tilted-ring projection is not "
                "mirror-even on the source-supported fibre"
            ),
            "physical_boundary": (
                "source-owned kinematic orientation and projection visibility do not "
                "prove fundamental Parent handedness or a Tau-specific coupling to chi"
            ),
            "minimum_supported_chi": float(np.min(signed_chirality[supported])),
            "maximum_supported_chi": float(np.max(signed_chirality[supported])),
            "maximum_abs_chi_sq_identity_residual": float(
                np.max(np.abs(signed_chirality**2 - chirality_sq_from_defects))
            ),
            "supported_signs": sorted(
                int(value) for value in np.unique(np.sign(signed_chirality[supported]))
            ),
            "maximum_supported_abs_mirror_projection_difference": float(
                np.max(np.abs(mirror_projection_difference[supported]))
            ),
            "rms_supported_mirror_projection_difference": float(
                np.sqrt(np.mean(mirror_projection_difference[supported] ** 2))
            ),
            "maximum_abs_mirror_projection_identity_residual": float(
                np.max(
                    np.abs(
                        mirror_projection_difference
                        - mirror_projection_difference_analytic
                    )
                )
            ),
            "status": "EXACT_GEOMETRIC_FIBRE_CHI_RETAINED_FOR_COMPLETE_PROJECTION_STACK",
        },
        "scalar_registration_boundary": {
            "candidate": "K1=d_in/(d_in+d_out)",
            "complete_shared_descriptor": False,
            "generic_reason": (
                "K1 is constant on every raw-descriptor mirror pair while the declared "
                "standard projection is not"
            ),
            "source_path_reason": (
                "the frozen piecewise shortest-great-circle path revisits the same K1 "
                "level on radially disjoint segments with different chi and projection"
            ),
            "source_path_collision_segments_arcsec": [list(value) for value in collision_segments],
            "sensitivity_targets": collision_records,
            "selected_witness": collision_witness,
            "safe_current_handoff": (
                "retain D_hat, or an exactly fibre-equivalent descriptor, until a "
                "source-owned complete-terminal scalar factorization is proved"
            ),
            "alternative_scalar_or_rank_one_parent_response": "OPEN",
            "multicomponent_parent_coupling_occupied_by_nature": "OPEN",
            "status": "K1_REFUTED_AS_COMPLETE_SHARED_DESCRIPTOR",
        },
        "conditional_terminal_counterfamily": {
            "formula": "v_(p,a,s)^2=v_carrier^2*(1+s*a*K_p)",
            "domain": "p>0, 0<=a<=1, s in {-1,+1}, v_carrier^2>=0",
            "properties": [
                "dimensionally valid because K_p and a are dimensionless",
                "nonnegative for both signs on the declared amplitude interval",
                "K_p=0 or a=0 exactly recovers the carrier",
                "different p, a, or s generally give different terminal curves",
            ],
            "verdict": "the source body does not select p, a, s, or the carrier",
        },
        "source_action_specialization": {
            "local_response": "D_K Z_*=-H_Z^{-1} B_ZK",
            "terminal_tangent": "Gamma=-L_G H_Z^{-1} B_ZK",
            "general_linearized_law": "delta v_G^2(R)=[Gamma K](R)",
            "common_action_pullback": (
                "for the source-owned complete signed-descriptor registration I=iota(D_hat), "
                "B_ZDhat=B_ZI J_(I<-Dhat) and Gamma_Dhat=-L_G H_Z^{-1} B_ZI J_(I<-Dhat)"
            ),
            "schur_reduction": (
                "if Z=(g,phi), exact elimination of phi gives "
                "H_G_eff=H_gg-H_gphi H_phiphi^{-1} H_phig and "
                "B_GD_eff=B_gD-H_gphi H_phiphi^{-1} B_phiD"
            ),
            "gravity_terminal_condition": (
                "inside a frozen Einstein--Newton/observer completion, "
                "L_G=D_Z O_G is inherited from the circular-gravity terminal and is not "
                "an independent morphology gain"
            ),
            "scalar_shell_condition": (
                "the shell v_G^2=v_carrier^2*(1+s*a*K_p) is selected only if "
                "[Gamma K_p](R)/(v_carrier^2(R)*K_p(R)) is one source-frozen "
                "constant s*a wherever K_p is nonzero"
            ),
            "exponent_condition": (
                "p is exact only if the source-owned defect response is proportional to d^p "
                "on the full support; the first nonzero analytic jet selects only a local "
                "leading-order integer exponent"
            ),
            "carrier_condition": (
                "inside the same frozen completion v_carrier^2=O_G[Z_*(I=0)]; its "
                "baryonic source, transport, calibration and standard-limit recovery must "
                "still be frozen independently of the endpoint"
            ),
            "occupation_condition": "the selected source orbit must be physically occupied",
            "current_verdict": (
                "ACT-PCLOSE1 plus the selected JCSEL/BRAC and Einstein--Newton branches "
                "make B_ZDhat, L_G and the carrier derivatives/evaluations of one packet, "
                "but the current source does not supply the signed-descriptor-to-Parent-invariant "
                "registration, its exact exponent/profile, calibrated occupied galaxy "
                "packet or Nature-level completion selection"
            ),
        },
        "geometry_only_scale_convention": {
            "formula": "a_sep=(1-n_in dot n_out)/2=sin^2(Theta/2)",
            "value": geometric_amplitude,
            "response_envelope": "v_carrier^2*(1 +/- a_sep*K_1)",
            "status": "source-derived diagnostic envelope only; no physical coupling theorem",
        },
        "standard_projection_control": {
            "formula": "G_proj(R)=[sin i(R)/sin i_inner]^2",
            "mirror_formula": (
                "G_proj(R_c n)-G_proj(n)="
                "4*chi*(ell dot c)*[(ell dot n)-chi*(ell dot c)]/sin(i_inner)^2"
            ),
            "applicability": "only when a circular-ring line-of-sight terminal was reduced with fixed i_inner",
            "status": "standard tilted-ring geometry control, not Tau-specific",
            "mirror_even_on_supported_source_fibre": False,
            "minimum_supported": float(np.min(projection_ratio_sq[supported])),
            "maximum_supported": float(np.max(projection_ratio_sq[supported])),
            "maximum_supported_abs_mirror_difference": float(
                np.max(np.abs(mirror_projection_difference[supported]))
            ),
            "rms_supported_mirror_difference": float(
                np.sqrt(np.mean(mirror_projection_difference[supported] ** 2))
            ),
            "maximum_difference_witness": {
                "radius_arcsec": float(points.loc[mirror_witness_index, "radius_arcsec"]),
                "source_n_los": float(normals[mirror_witness_index, 2]),
                "mirror_n_los": float(reflected_normals[mirror_witness_index, 2]),
                "source_projection_ratio_sq": float(
                    projection_ratio_sq[mirror_witness_index]
                ),
                "mirror_projection_ratio_sq": float(
                    mirror_projection_ratio_sq[mirror_witness_index]
                ),
            },
        },
        "numerical_summary": {
            "n_supported_rings": int(np.sum(supported)),
            "plane_separation_deg": float(body["derived_geometry"]["inner_outer_plane_separation_deg"]),
            "plane_defect_separation": plane_defect_separation,
            "geometric_amplitude": geometric_amplitude,
            "minimum_supported_K1": float(np.min(kernel_p1[supported])),
            "maximum_supported_K1": float(np.max(kernel_p1[supported])),
            "maximum_transition_abs_K1_minus_K2": p_witness,
            "maximum_supported_plus_minus_response_factor_separation": sign_witness,
        },
        "theorem_audit": {
            "bounded_coordinate": "PROVEN",
            "plane_limit_and_swap_identities": "PROVEN",
            "raw_descriptor_mirror_fibre": "PROVEN",
            "one_signed_coordinate_completes_oriented_geometry": "PROVEN",
            "K1_unique_in_normalized_affine_two_anchor_class": "PROVEN_CONDITIONALLY",
            "normalized_affine_class_selected_by_physical_source": "OPEN",
            "source_owned_oriented_spin_normal_record": "PROVEN_FROM_FROZEN_SOURCE",
            "standard_projection_mirror_even": "REFUTED_ON_SOURCE_SUPPORT",
            "chi_retention_for_complete_projection_stack": "PROVEN",
            "K1_complete_shared_descriptor": "REFUTED",
            "K1_injective_on_frozen_continuous_source_path": "REFUTED",
            "minimal_complete_oriented_graph_registration_rank": "TWO_CONDITIONALLY",
            "single_radial_path_registration_pullback_rank": "AT_MOST_ONE",
            "scalar_brac_descendant_pointwise_rank": "AT_MOST_ONE",
            "alternative_source_selected_scalar_registration": "OPEN",
            "physical_multicomponent_parent_coupling": "OPEN",
            "fundamental_parent_handedness_or_tau_specific_chi_coupling": "OPEN",
            "terminal_nonidentifiability_from_body_alone": "PROVEN_BY_EXPLICIT_COUNTERFAMILY",
            "common_action_pullback_and_exact_schur_reduction": "PROVEN_CONDITIONALLY",
            "raw_defect_to_parent_invariant_registration": "OPEN",
            "physical_terminal_occupation": "OPEN",
        },
        "complete_registration_theory_boundary": {
            "status": "IMPORTED_CONDITIONAL_THEOREM_NOT_A_PAPER8_ENDPOINT_CHECK",
            "theorem": "MBA-2P-P6 / GOR-P1",
            "action": (
                "A_reg(N;D_hat)=1/2 <N-N(D_hat),"
                "K_reg[N-N(D_hat)]>, K_reg>0"
            ),
            "complete_oriented_register_rank": 2,
            "rank_domain": "PHYSICAL_DESCRIPTOR_TANGENT",
            "construction_scope": (
                "DECODER_EXPLICIT_EXISTENCE_AND_CONSISTENCY_NOT_DEEPER_SOURCE_SELECTION"
            ),
            "scalar_brac_descendant_pointwise_rank_upper_bound": 1,
            "one_radial_source_path_rank_upper_bound": 1,
            "theory_audit": "22/22",
            "physical_occupation": "OPEN",
        },
        "claim_ledger": {
            "facts": [
                "The upstream source body supplies two distinct mean plane normals and a radial normal field.",
                "The frozen source publishes oriented spin-normal components and an approaching-side convention.",
                "The standard fixed-inner-inclination projection differs on exact raw-descriptor mirror fibres.",
                "No endpoint-bearing column is read by this construction.",
            ],
            "definitions": [
                "K_1 is adopted as the minimal first-order affine-defect morphology coordinate.",
                "a_sep defines a geometry-only diagnostic envelope, not a force law.",
            ],
            "derived_results": [
                "K_p is bounded and obeys exact inner, outer, swap, and no-two-plane limits.",
                "The signed chi coordinate must be retained in the complete source-to-projection descriptor.",
                "K1 is not a complete descriptor: the continuous source path has two distinct radii with equal K1 and different chi and standard projection.",
                "Under the separate GOR-P1 graph-action candidate, the complete signed two-plane register has tangent rank two while a scalar descendant has pointwise rank at most one.",
                "A continuum of dimensionally valid bounded terminal laws shares the same source body.",
            ],
            "not_derived": [
                "Fundamental Parent handedness and a Tau-specific chi coupling remain unproved.",
                "No alternative scalar registration or physically occupied multicomponent Parent coupling is selected.",
                "GOR-P1 contains the exact decoder explicitly and therefore does not independently derive it from deeper Parent source primitives.",
                "The one-dimensional UGC03580 radial path cannot validate Nature-level rank-two registration occupation.",
                "The physical function from the complete register into the scalar JCSEL/BRAC invariant remains unselected.",
                "The terminal sign, amplitude, exponent, carrier, physical occupation, and Tau-specificity remain unselected.",
                "A constant scalar amplitude additionally requires radial rank-one factorization of the full source-to-terminal response operator.",
                "The standard projection control applies only after auditing how the endpoint was inclination-corrected.",
            ],
        },
        "endpoint_values_used": False,
        "terminal_formula_selected": False,
        "endpoint_allowed": False,
        "next_gate": (
            "retain the complete signed descriptor, derive whether the occupied "
            "JCSEL/BRAC response has a source-owned scalar factorization or genuinely "
            "multicomponent registration, "
            "freeze the Einstein--Newton/observer carrier and "
            "calibration, and derive the full radial response or any scalar factorization; "
            "then freeze them before choosing and opening a genuinely untouched target"
        ),
    }

    POINTS_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    numeric_columns = result_points.select_dtypes(include=[np.number]).columns
    result_points[numeric_columns] = result_points[numeric_columns].mask(
        result_points[numeric_columns].abs() < 1.0e-12,
        0.0,
    )
    # The source tables carry substantially less than nine significant digits.
    # Freezing the derived shell at nine digits keeps all source-supported
    # precision while preventing NumPy 1.x/2.x last-bit differences from
    # changing the byte-level reproducibility hash.
    result_points.to_csv(POINTS_OUT, index=False, float_format="%.9g")
    summary = canonicalize_float_tree(summary)
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    REPORT_OUT.write_text(
        "\n".join(
            [
                "# UGC03580 / UGC3580 bounded two-plane readout shell v01",
                "",
                "Status: `FORMULA_SHELL_DERIVED_ENDPOINT_BLOCKED`",
                "",
                "## Derived source coordinate",
                "",
                "For a ring normal `n(R)` and the source-defined inner and outer plane",
                "normals, define",
                "",
                "```text",
                "d_in(R)  = 1 - n_in dot n(R)",
                "d_out(R) = 1 - n_out dot n(R)",
                "K_p(R)   = d_in(R)^p / [d_in(R)^p + d_out(R)^p],   p>0.",
                "```",
                "",
                "Because both defects are nonnegative, `0<=K_p<=1`. For distinct",
                "reference planes it is exactly zero on the inner plane, exactly one",
                "on the outer plane, and changes to `1-K_p` when the plane labels are",
                "swapped. Coincident planes deactivate the construction and set `K_p=0`.",
                "The primary `p=1` coordinate is only the minimal affine-defect convention.",
                "",
                "## Exact mirror fibre of the raw descriptor",
                "",
                "The raw pair `(d_in,d_out)` fixes the projection of the ring normal into",
                "the span of the two reference normals but generically leaves a two-point",
                "mirror fibre. With `c=(n_in x n_out)/|n_in x n_out|`, the signed control",
                "`chi=c dot n` completes the oriented descriptor, while `chi^2` is already",
                "fixed by the raw defects. A local rank test misses this discrete ambiguity;",
                "quotienting it requires exact equality of every terminal on the mirror pair.",
                "Jozsa (2007) Table 6 publishes the oriented spin-normal components",
                "toward west, north, and the observer, while the UGC3580 captions identify",
                "the approaching side as southeast. Thus the signed record is source-owned.",
                "Moreover, the standard fixed-inner-inclination projection is not mirror-even:",
                "",
                "```text",
                "G_proj(R_c n)-G_proj(n)",
                "  = 4 chi (ell dot c)[(ell dot n)-chi(ell dot c)]/sin(i_inner)^2.",
                "```",
                "",
                f"On supported rings its maximum absolute difference is `{np.max(np.abs(mirror_projection_difference[supported])):.12f}`",
                f"and its RMS difference is `{np.sqrt(np.mean(mirror_projection_difference[supported] ** 2)):.12f}`.",
                "Therefore `chi` must be retained in the complete projection descriptor.",
                "This is representation correctness under a standard projection, not evidence",
                "for fundamental Parent handedness or a Tau-specific `chi` coupling.",
                "No endpoint is used in this control.",
                "",
                "## Scalar-registration boundary",
                "",
                "`K_1` cannot replace the complete signed descriptor. It is unchanged",
                "on every raw-descriptor mirror pair even though the standard projection",
                "can change. The source path supplies a stronger within-path witness:",
                f"the level `K_1=0.925` occurs at `{collision_witness['roots'][0]['radius_arcsec']:.9f}`",
                f"and `{collision_witness['roots'][1]['radius_arcsec']:.9f} arcsec`, while",
                f"the projection changes from `{collision_witness['roots'][0]['projection_ratio_sq']:.12f}`",
                f"to `{collision_witness['roots'][1]['projection_ratio_sq']:.12f}` and `chi`",
                "has opposite signs. The neighboring targets 0.900 and 0.950 reproduce",
                "the collision, so it is not a tuned level choice.",
                "",
                "This refutes `K_1` as a complete shared coordinate; it does not prove",
                "that every Parent action must couple to two independent components. A",
                "source-derived rank-one factorization through another signed scalar remains",
                "logically possible. Until it is proved, the safe action handoff retains",
                "`D_hat` or an exactly fibre-equivalent descriptor.",
                "",
                "## Complete registration versus scalar interaction",
                "",
                "The separate MBA-2P-P6 theory audit constructs the exact decoder",
                "",
                "$$",
                "\\mathcal N(\\widehat D)",
                "=A_{ab}^{-1}(1-d_{\\mathrm{in}},1-d_{\\mathrm{out}},\\chi)^T",
                "$$",
                "",
                "and a positive graph action whose unique zero is this decoder. On the",
                "complete signed two-plane descriptor surface the decoder differential",
                "restricted to the physical tangent has rank two. Because the decoder",
                "is explicit in the square, this proves conditional existence and",
                "consistency rather than deeper source selection. A later scalar",
                "invariant I_K=f(N) has pointwise rank at",
                "most one, so it is a partial interaction input rather than the complete",
                "orientation register.",
                "",
                "The UGC03580 radial path is one-dimensional and has registration",
                "pullback rank at most one. It can refute K_1 through the repeated fibre",
                "but cannot establish Nature-level rank-two occupation. The graph-action",
                "theory audit passes 22/22 checks and is not counted in the 62/62 Paper 8",
                "source-shell audit.",
                "",
                "## What the body does not determine",
                "",
                "For every `p>0`, `0<=a<=1`, and sign `s=+/-1`,",
                "",
                "```text",
                "v_(p,a,s)^2 = v_carrier^2 * [1 + s*a*K_p]",
                "```",
                "",
                "is dimensionally valid, bounded, nonnegative and has the same carrier",
                "recovery limit. Distinct choices give distinct curves. This explicit",
                "counterfamily proves that the two-plane body alone cannot select the",
                "terminal exponent, amplitude, sign or carrier.",
                "",
                "## Exact Parent-response specialization",
                "",
                "After the body has been solved and frozen, a regular post-body action gives",
                "",
                "```text",
                "D_K Z_* = -H_Z^{-1} B_ZK,",
                "Gamma   = -L_G H_Z^{-1} B_ZK,",
                "delta v_G^2(R) = [Gamma K](R).",
                "```",
                "",
                "Positive `H_Z` guarantees a regular stable response, but it does not fix",
                "the sign or scale of the mixed block or the physical terminal covector.",
                "The scalar shell with one constant `a` follows only if the complete radial",
                "operator factorizes so that `[Gamma K_p]/(v_carrier^2 K_p)=s*a` is constant",
                "where `K_p` is nonzero. The current source packet does not prove this.",
                "Likewise, a source action must select the exact defect response to fix `p`;",
                "a leading analytic source jet fixes only a local leading order, not the full",
                "global `K_p` law. The carrier is the separately derived zero-morphology",
                "physical terminal branch, not an empirical residual baseline.",
                "",
                "In one frozen common-action completion these objects are not independent",
                "gains. A source-owned complete registration `I=iota(D_hat)` gives",
                "`B_ZDhat=B_ZI J_(I<-Dhat)` and the same gravity/observer terminal gives",
                "`v_carrier^2=O_G[Z_*(I=0)]`. Exact Schur elimination must retain any",
                "occupied internal-field contribution. The unresolved physical object is",
                "the full-support signed-descriptor-to-Parent-invariant registration,",
                "rather than three coefficients to fit independently.",
                "",
                "## Source-only numerical envelope and standard control",
                "",
                f"- plane separation: `{body['derived_geometry']['inner_outer_plane_separation_deg']:.6f} deg`;",
                f"- geometry-only scale `sin^2(Theta/2)`: `{geometric_amplitude:.9f}`;",
                f"- supported `K_1` range: `{np.min(kernel_p1[supported]):.6f}` to `{np.max(kernel_p1[supported]):.6f}`;",
                f"- maximum transition `|K_1-K_2|`: `{p_witness:.6f}`;",
                f"- fixed-inner-inclination projection `G_proj` range: `{np.min(projection_ratio_sq[supported]):.6f}` to `{np.max(projection_ratio_sq[supported]):.6f}`.",
                f"- maximum mirror-pair `|Delta G_proj|`: `{np.max(np.abs(mirror_projection_difference[supported])):.12f}`.",
                "",
                "The `G_proj` relation is standard circular tilted-ring projection and",
                "is usable only if the target terminal was reduced with the fixed inner",
                "inclination. It is a null/control calculation, not a Tau signal.",
                "",
                "## Verdict",
                "",
                "The exact mirror audit closes the orientation/null decision for this",
                "projection lane: `chi` is source-owned and terminal-visible, so it is",
                "retained. The source-path collision additionally refutes `K_1` as the",
                "complete registration. It does not close fundamental Parent handedness or",
                "prove a multicomponent physical coupling. The sharper physical blocker is",
                "whether one source-owned signed scalar factorization exists or the common",
                "action retains multiple descriptor directions. No endpoint is opened or",
                "rescored. The next",
                "admissible step is a source-owned full-support registration plus a frozen",
                "common gravity/observer calibration, followed by a genuinely new target.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(summary["numerical_summary"], indent=2))


if __name__ == "__main__":
    main()
