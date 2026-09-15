from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from two_plane_morphology_common_v01 import (  # noqa: E402
    fixed_inclination_projection_ratio_sq,
    two_plane_barycentric_kernel,
)


def test_ugc03580_two_plane_readout_shell_reproducibility() -> None:
    scripts = [
        "scripts/build_ugc03580_ugc3580_two_plane_body_v01.py",
        "scripts/build_ugc03580_ugc3580_two_plane_readout_shell_v01.py",
        "scripts/audit_ugc03580_ugc3580_two_plane_readout_shell_v01.py",
    ]
    for script in scripts:
        subprocess.run([sys.executable, script], cwd=ROOT, check=True, capture_output=True)

    summary = json.loads(
        (ROOT / "data/derived/ugc03580_ugc3580_two_plane_readout_shell_v01.json").read_text(
            encoding="utf-8"
        )
    )
    audit = json.loads(
        (
            ROOT
            / "data/derived/ugc03580_ugc3580_two_plane_readout_shell_reproducibility_audit_v01.json"
        ).read_text(encoding="utf-8")
    )
    assert summary["status"] == "FORMULA_SHELL_DERIVED_ENDPOINT_BLOCKED"
    assert summary["endpoint_values_used"] is False
    assert summary["terminal_formula_selected"] is False
    assert summary["endpoint_allowed"] is False
    assert summary["theorem_audit"]["bounded_coordinate"] == "PROVEN"
    assert summary["theorem_audit"]["raw_descriptor_mirror_fibre"] == "PROVEN"
    assert (
        summary["theorem_audit"]["one_signed_coordinate_completes_oriented_geometry"]
        == "PROVEN"
    )
    assert (
        summary["theorem_audit"]["terminal_nonidentifiability_from_body_alone"]
        == "PROVEN_BY_EXPLICIT_COUNTERFAMILY"
    )
    assert audit["status"] == "REPRODUCIBILITY_AUDIT_PASS"
    assert audit["checks_passed"] == audit["checks_total"]
    assert summary["source_action_specialization"]["local_response"] == "D_K Z_*=-H_Z^{-1} B_ZK"
    assert audit["conditional_completion"]["current_status"] == (
        "K1_REFUTED_AS_COMPLETE_DESCRIPTOR_SIGNED_REGISTRATION_AND_OCCUPATION_OPEN"
    )
    fibre = summary["exact_registration_fibre"]
    assert (
        fibre["status"]
        == "EXACT_GEOMETRIC_FIBRE_CHI_RETAINED_FOR_COMPLETE_PROJECTION_STACK"
    )
    assert fibre["complete_projection_stack_decision"] == "RETAIN_CHI"
    assert fibre["supported_signs"] == [-1, 1]
    assert fibre["maximum_abs_chi_sq_identity_residual"] < 1.0e-13
    assert fibre["maximum_supported_abs_mirror_projection_difference"] > 0.1
    assert summary["standard_projection_control"][
        "mirror_even_on_supported_source_fibre"
    ] is False
    assert (
        summary["theorem_audit"]["chi_retention_for_complete_projection_stack"]
        == "PROVEN"
    )
    scalar_boundary = summary["scalar_registration_boundary"]
    assert scalar_boundary["status"] == "K1_REFUTED_AS_COMPLETE_SHARED_DESCRIPTOR"
    assert scalar_boundary["complete_shared_descriptor"] is False
    collision = scalar_boundary["selected_witness"]
    assert np.isclose(collision["target_K1"], 0.925)
    assert abs(collision["roots"][0]["K1"] - collision["roots"][1]["K1"]) < 1.0e-12
    assert collision["radial_separation_arcsec"] > 40.0
    assert collision["roots"][0]["chi"] * collision["roots"][1]["chi"] < 0.0
    assert abs(collision["projection_difference"]) > 0.08
    witness = audit["source_action_countermodel"]
    assert witness["minimum_H_Z_eigenvalue"] > 0.0
    assert np.isclose(witness["Gamma_after_B_ZK_sign_flip"], -witness["Gamma"])
    assert np.isclose(witness["Gamma_after_B_ZK_scale_times_three"], 3.0 * witness["Gamma"])
    pullback = audit["common_action_pullback_witness"]
    assert pullback["same_visible_K_projection_residual"] < 1.0e-14
    assert not np.isclose(pullback["Gamma_visible_lift"], pullback["Gamma_hidden_lift"])
    assert np.isclose(
        pullback["Gamma_visible_lift"],
        pullback["Gamma_visible_lift_after_exact_schur_reduction"],
    )
    assert np.isclose(
        pullback["Gamma_hidden_lift"],
        pullback["Gamma_hidden_lift_after_exact_schur_reduction"],
    )


def test_two_plane_kernel_theorem_properties() -> None:
    inner = np.array([0.0, 0.0, 1.0])
    outer = np.array([1.0, 0.0, 0.0])
    midpoint = np.array([1.0, 0.0, 1.0]) / np.sqrt(2.0)
    normals = np.vstack((inner, midpoint, outer))

    kernel = two_plane_barycentric_kernel(normals, inner, outer, power=1.0)
    swapped = two_plane_barycentric_kernel(normals, outer, inner, power=1.0)
    assert np.all((kernel >= 0.0) & (kernel <= 1.0))
    assert np.allclose(kernel[[0, 2]], [0.0, 1.0])
    assert np.allclose(kernel + swapped, 1.0)
    assert np.allclose(
        two_plane_barycentric_kernel(normals, inner, inner, power=1.0),
        0.0,
    )
    with pytest.raises(ValueError, match="strictly positive"):
        two_plane_barycentric_kernel(normals, inner, outer, power=0.0)


def test_fixed_inclination_projection_control() -> None:
    factors = fixed_inclination_projection_ratio_sq(np.array([30.0, 60.0]), 30.0)
    assert np.allclose(factors, [1.0, 3.0])
    with pytest.raises(ValueError, match="face-on"):
        fixed_inclination_projection_ratio_sq(np.array([30.0]), 0.0)
