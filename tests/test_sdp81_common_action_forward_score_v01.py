from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
COMPILER = ROOT / "scripts/compile_sdp81_common_action_forward_model_v01.py"
SCORER = ROOT / "scripts/run_sdp81_common_action_endpoint_v01.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def positive_common_hessian(coupling_scale: float = 1.0) -> np.ndarray:
    rng = np.random.default_rng(42017)
    generator = np.eye(14) + 0.07 * rng.normal(size=(14, 14))
    generator[:10, 10:12] *= coupling_scale
    generator[10:12, :10] *= coupling_scale
    return generator.T @ generator + 0.8 * np.eye(14)


def test_source_compiler_fails_closed_without_physical_manifest() -> None:
    subprocess.run([sys.executable, str(COMPILER)], cwd=ROOT, check=True)
    result = json.loads((ROOT / "data/derived/sdp81_common_action_forward_model_v01.json").read_text())
    assert result["status"] == "FORMULA_SHELL_DERIVED_ENDPOINT_BLOCKED"
    assert result["inputs"]["spectral_or_velocity_endpoint_read"] is False
    assert result["endpoint_authorized"] is False
    assert result["retrospective_only"] is True


def test_source_compiler_builds_authorized_synthetic_fixture(tmp_path: Path) -> None:
    module = load_module(COMPILER, "common_action_compile_main")
    path_ids = [f"q1_path_{index}" for index in range(1, 5)]
    gate = {
        "source_checks_passed": 8,
        "source_checks_total": 8,
        "endpoint_authorized": True,
        "observed_4d_path_keys": path_ids,
    }
    gate_path = tmp_path / "gate.json"
    gate_path.write_text(json.dumps(gate), encoding="utf-8")
    basis = module.helmert_zero_sum_basis(6)
    hessian = positive_common_hessian()
    manifest = {
        "transfer_semantics": "relaxed_lift",
        "dimensions": {
            "source_mode": 5,
            "observer_mode": 5,
            "parent_lift": 2,
            "internal_channel": 2,
        },
        "common_action_paths": [
            {
                "path_id": path_id,
                "common_postbody_hessian": (hessian + 0.01 * index * np.eye(14)).tolist(),
            }
            for index, path_id in enumerate(path_ids)
        ],
        "terminal_calibration": {
            "centered_log_channel_basis": basis.tolist(),
            "mode_noise_covariance_by_path": {
                path_id: (0.01 * np.eye(5)).tolist() for path_id in path_ids
            },
        },
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    module.ROOT = tmp_path
    module.GATE = gate_path
    module.PHYSICAL_MANIFEST = manifest_path
    module.OUT = tmp_path / "result.json"
    module.REPORT = tmp_path / "report.md"
    module.main()
    result = json.loads(module.OUT.read_text())
    assert result["status"] == "FORMULA_FROZEN_ENDPOINT_AUTHORIZED_RETROSPECTIVE_ONLY"
    assert result["endpoint_authorized"] is True
    assert len(result["compiled_paths"]) == 4
    assert result["leave_one_path_out_identifiability"]["all_folds_identifiable"] is True


def test_endpoint_runner_does_not_open_endpoint_when_blocked() -> None:
    subprocess.run([sys.executable, str(SCORER)], cwd=ROOT, check=True)
    result = json.loads((ROOT / "data/derived/sdp81_common_action_endpoint_v01.json").read_text())
    assert result["status"] == "FORMULA_SHELL_DERIVED_ENDPOINT_BLOCKED"
    assert result["spectral_endpoint_read"] is False
    assert result["score_emitted"] is False


def test_nested_schur_compiler_limits_and_stability() -> None:
    module = load_module(COMPILER, "common_action_compiler")
    hessian = positive_common_hessian()
    fixed = module.compile_transfer(hessian, 5, 5, 2, 2, "fixed_lift")
    relaxed = module.compile_transfer(hessian, 5, 5, 2, 2, "relaxed_lift")
    assert fixed["maximum_transfer_singular_value"] < 1.0
    assert relaxed["maximum_transfer_singular_value"] < 1.0
    difference = np.asarray(fixed["fixed_boundary_hessian"]) - np.asarray(relaxed["relaxed_boundary_hessian"])
    assert np.linalg.eigvalsh(difference).min() > -1.0e-10
    perturbed = module.compile_transfer(hessian + 1.0e-8 * np.eye(14), 5, 5, 2, 2, "relaxed_lift")
    assert np.linalg.norm(np.asarray(perturbed["selected_transfer"]) - np.asarray(relaxed["selected_transfer"])) < 1.0e-6

    boundary = hessian[:10, :10]
    hidden = hessian[10:, 10:]
    decoupled = np.block(
        [[boundary, np.zeros((10, 4))], [np.zeros((4, 10)), hidden]]
    )
    decoupled_fixed = module.compile_transfer(decoupled, 5, 5, 2, 2, "fixed_lift")
    decoupled_relaxed = module.compile_transfer(decoupled, 5, 5, 2, 2, "relaxed_lift")
    assert np.allclose(
        decoupled_fixed["fixed_boundary_hessian"],
        decoupled_relaxed["relaxed_boundary_hessian"],
        atol=1.0e-12,
    )


def test_loo_forward_score_recovers_common_source_and_rejects_wrong_assignment() -> None:
    module = load_module(SCORER, "common_action_scorer")
    mode_dim = 5
    source = np.array([0.3, -0.2, 0.1, 0.25, -0.15])
    transfers = []
    for index in range(4):
        diagonal = np.array([0.45, 0.55, 0.65, 0.75, 0.85]) + 0.035 * index * np.array([1, -1, 1, -1, 1])
        transfers.append(np.diag(diagonal))
    observed = np.asarray([transfer @ source for transfer in transfers])
    covariances = [0.01 * np.eye(mode_dim) for _ in range(4)]
    score = module.score_controls(observed, transfers, covariances)
    assert score["matched"]["total_mahalanobis_chi2"] < 1.0e-20
    assert score["matched_beats_wrong_median"] is True
    assert score["matched_beats_every_wrong_assignment"] is True


def test_loo_identifiability_rejects_hidden_source_mode() -> None:
    module = load_module(COMPILER, "common_action_identifiability")
    transfers = []
    for index in range(4):
        transfer = np.diag([0.5, 0.6, 0.7, 0.8, 0.0])
        transfers.append({"path_id": f"p{index}", "selected_transfer": transfer.tolist()})
    calibration = {
        "mode_noise_covariance_by_path": {
            f"p{index}": (0.01 * np.eye(5)).tolist() for index in range(4)
        }
    }
    result = module.audit_loo_identifiability(transfers, calibration)
    assert result["all_folds_identifiable"] is False
    assert all(fold["stacked_transfer_rank"] == 4 for fold in result["folds"])


def test_centered_log_terminal_is_gain_invariant() -> None:
    compiler = load_module(COMPILER, "common_action_basis")
    scorer = load_module(SCORER, "common_action_modes")
    basis = compiler.helmert_zero_sum_basis(6)
    spectra = np.array([[1.0, 1.2, 0.9, 1.4, 1.1, 0.8], [0.8, 1.0, 1.3, 0.7, 1.2, 1.4]])
    modes = scorer.centered_log_modes(spectra, basis)
    gained = scorer.centered_log_modes(spectra * np.array([[3.0], [0.25]]), basis)
    assert np.allclose(modes, gained, atol=1.0e-12)
