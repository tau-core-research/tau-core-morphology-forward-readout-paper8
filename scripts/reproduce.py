#!/usr/bin/env python3
"""One-command reproduction check for the Paper 8 / Paper 1 package.

After the Paper 8/Paper 9 split this script intentionally reproduces only the
internal-preflight morphology-matched forward-readout paper.  Projection,
time-readout, UGC12506, and beta-closure candidate/control material now lives in
the Paper 9 repository.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper8_submission_source"


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("$ " + " ".join(cmd) + f"  # cwd={cwd}")
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "1767225600")
    subprocess.run(cmd, cwd=cwd, check=True, env=env)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    paper1_commands = [
        "scripts/generate_paper8_artifacts.py",
        "scripts/audit_paper8_foundations.py",
        "scripts/run_available_morphology_readout_pilot.py",
        "scripts/build_morphology_parameter_manifest.py",
        "scripts/run_morphology_matched_proxy_endpoint.py",
        "scripts/run_morphology_formula_shell_proxy_endpoint.py",
        "scripts/run_source_native_readout_formula_endpoint.py",
        "scripts/run_readout_mixture_proxy_endpoint.py",
        "scripts/run_manifest_confidence_diagnostics.py",
        "scripts/run_amplitude_policy_diagnostics.py",
        "scripts/run_amplitude_shrinkage_path.py",
        "scripts/run_train_selected_shrinkage_diagnostic.py",
        "scripts/run_family_breakdown_diagnostics.py",
        "scripts/run_family_observable_quality_diagnostics.py",
        "scripts/audit_baseline_success_morphology.py",
        "scripts/run_predeclared_quality_gate_diagnostics.py",
        "scripts/run_quality_gate_shuffled_null_diagnostics.py",
        "scripts/run_endpoint_decision_matrix.py",
        "scripts/build_predeclared_endpoint_protocol.py",
        "scripts/build_readiness_upgrade_audit.py",
        "scripts/build_morphology_observable_intake_schema.py",
        "scripts/run_morphology_observable_gap_audit.py",
        "scripts/build_morphology_observable_source_upgrade_plan.py",
        "scripts/build_accepted_observable_manifest_template.py",
        "scripts/run_accepted_manifest_readiness_gate.py",
        "scripts/run_frozen_endpoint_launch_guard.py",
        "scripts/build_external_morphology_source_registry.py",
        "scripts/acquire_external_morphology_inputs.py",
        "scripts/build_accepted_morphology_manifest.py",
        "scripts/audit_accepted_morphology_manifest.py",
        "scripts/audit_exponential_disk_family_labels.py",
        "scripts/build_narrow_accepted_exponential_disk_manifest.py",
        "scripts/run_narrow_accepted_exponential_disk_population_endpoint.py",
        "scripts/build_source_native_readout_robustness.py",
        "scripts/run_source_native_carrier_robustness.py",
        "scripts/run_inverse_required_rapidity_diagnostic_v01.py",
        "scripts/run_inverse_required_parent_loss_diagnostic_v01.py",
        "scripts/freeze_ngc2541_signed_descriptor_source_geometry_v01.py",
        "scripts/run_ngc2541_halogas_independent_side_consistency_endpoint_v01.py",
        "scripts/audit_ngc2541_halogas_side_consistency_robustness_v01.py",
        "scripts/audit_ngc2541_halogas_calibration_nuisance_v02.py",
        "scripts/freeze_ngc0925_signed_descriptor_source_geometry_v01.py",
        "scripts/audit_ngc0925_physical_geometry_uncertainty_v02.py",
        "scripts/audit_ngc0925_outer_only_source_support_v01.py",
        "scripts/freeze_ngc4062_halogas_confirmatory_endpoint_v01.py",
        "scripts/run_ngc4062_halogas_confirmatory_endpoint_v01.py",
        "scripts/audit_ngc4062_velocity_zero_point_orthogonalization_v01.py",
        "scripts/audit_ngc3726_source_owned_zero_point_projector_v01.py",
        "scripts/freeze_ngc3893_disturbed_control_v01.py",
        "scripts/run_ngc3893_disturbed_control_v01.py",
        "scripts/audit_multigalaxy_halogas_confirmatory_candidate_pool_v01.py",
        "scripts/audit_sdp81_rybak2020_source_blind_pdr_preflight_v01.py",
        "scripts/audit_sdp81_open_transition_profile_lift_gate_v01.py",
        "scripts/freeze_sdp81_alma_visibility_source_route_v01.py",
        "scripts/audit_sdp81_reference_image_source_route_v01.py",
        "scripts/run_sdp81_full_arc_regularized_source_inversion_v02.py",
        "scripts/audit_sdp81_co109_common_action_source_gate_v01.py",
    ]
    for script in paper1_commands:
        run([sys.executable, script])

    if shutil.which("tectonic") is None:
        raise SystemExit("tectonic is required to compile paper8_submission_source/main.tex")
    run(["tectonic", "main.tex"], cwd=SOURCE)
    run([sys.executable, "scripts/build_arxiv_source.py"])
    run([sys.executable, "-m", "pytest", "-q"])
    print(f"paper8_pdf_sha256: {sha256(SOURCE / 'main.pdf')}")
    print("PAPER8_INTERNAL_PREFLIGHT_REPRODUCTION_COMPLETE")


if __name__ == "__main__":
    main()
