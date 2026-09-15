from __future__ import annotations

import json
import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_sdp81_parent_path_lift_gate_v01.py"
RESULT = ROOT / "data/derived/sdp81_parent_path_lift_gate_v01.json"


def test_sdp81_parent_path_lift_gate_fails_closed() -> None:
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["status"] == "PREFLIGHT_NOT_ENDPOINT"
    assert result["source_checks_passed"] == result["source_checks_total"] == 8
    assert result["physical_requirements_materialized"] == 0
    assert result["endpoint_authorized"] is False
    assert len(result["observed_4d_path_keys"]) == 4
    assert len(result["homogeneous_fiber_generator_reduction_contract"]) == 4
    assert len(result["parent_hessian_equivariance_certificate_contract"]) == 4
    assert len(result["source_symmetry_reconstruction_contract"]) == 5
    assert len(result["minimum_direct_occupied_lift_acquisition_contract"]) == 9
    assert len(result["lift_occurrence_pushforward_contract"]) == 6
    assert len(result["complete_action_induced_selector_contract"]) == 11
    assert not any(result["typed_standard_lens_exclusions"].values())
    assert result["input"]["spectral_or_velocity_endpoint_read"] is False
    assert result["observed_4d_incidence_status"]["positive_counting_measure_materialized"] is True
    assert result["observed_4d_incidence_status"]["parent_lift_measure_materialized"] is False


def test_descriptor_injected_physical_strings_cannot_authorize(tmp_path: Path) -> None:
    spec = importlib.util.spec_from_file_location("lift_gate", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    descriptor = json.loads((ROOT / "data/derived/sdp81_standard_corridor_descriptor_v01.json").read_text(encoding="utf-8"))
    descriptor["physical_parent_packet_key"] = "fake"
    descriptor["parent_hessian_nature_occupation_key"] = "fake"
    descriptor["parent_lift_fiber_basicness_certificate"] = "fake"
    for index, path in enumerate(descriptor["paths"]):
        path["occupied_parent_lift_key"] = f"fake-{index}"

    injected = tmp_path / "descriptor.json"
    injected.write_text(json.dumps(descriptor), encoding="utf-8")
    module.DESCRIPTOR = injected
    module.PHYSICAL_MANIFEST = tmp_path / "absent-physical-manifest.json"
    module.OUT = tmp_path / "result.json"
    module.REPORT = tmp_path / "report.md"
    module.main()
    result = json.loads(module.OUT.read_text(encoding="utf-8"))
    assert result["source_checks"]["standard_descriptor_contains_no_physical_authorization_fields"] is False
    assert result["physical_requirements_materialized"] == 0
    assert result["endpoint_authorized"] is False
    assert result["status"] == "PREFLIGHT_NOT_ENDPOINT"


def test_hash_only_self_asserted_physical_manifest_cannot_authorize(tmp_path: Path) -> None:
    spec = importlib.util.spec_from_file_location("lift_gate_manifest", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def artifact_record(name: str) -> dict[str, str]:
        path = tmp_path / name
        path.write_text("self-asserted", encoding="utf-8")
        return {
            "artifact": str(path.relative_to(tmp_path)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }

    parent_key = "self-asserted-parent-key"
    projection = {
        **artifact_record("projection.txt"),
        "source_owned": True,
    }
    hessian = {
        **artifact_record("hessian.txt"),
        "physical_parent_packet_key": parent_key,
        "positivity_certificate_pass": True,
        "source_observer_interior_block_split": ["source", "observer", "interior"],
    }
    nature = {
        **artifact_record("nature.txt"),
        "status": "INDEPENDENT_PHYSICAL_OCCUPATION_EVIDENCE",
        "independent_of_terminal_endpoint": True,
    }
    manifest = {
        "schema": "tau-core.paper8.sdp81-parent-lift-physical-source-manifest.v01",
        "status": "PHYSICAL_PARENT_LIFT_SOURCE_PACKET_FROZEN",
        "spectral_or_velocity_endpoint_read": False,
        "physical_parent_packet_key": parent_key,
        "pi_4D_source_definition": projection,
        "occupied_parent_hessian": hessian,
        "nature_occupation_evidence": nature,
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    module.ROOT = tmp_path
    module.DESCRIPTOR = ROOT / "data/derived/sdp81_standard_corridor_descriptor_v01.json"
    module.PHYSICAL_MANIFEST = manifest_path
    module.OUT = tmp_path / "result.json"
    module.REPORT = tmp_path / "report.md"
    module.main()
    result = json.loads(module.OUT.read_text(encoding="utf-8"))
    assert result["physical_requirements"]["independent_nature_occupation_evidence"] is False
    assert result["physical_requirements"]["typed_parent_hessian_and_projection_packet"] is False
    assert result["endpoint_authorized"] is False
    assert result["status"] == "PREFLIGHT_NOT_ENDPOINT"


def test_sdp81_parent_path_lift_gate_is_deterministic() -> None:
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    first = RESULT.read_bytes()
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    assert RESULT.read_bytes() == first
