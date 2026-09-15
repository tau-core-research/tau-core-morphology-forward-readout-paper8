from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_edge_califa_rotation_morphology_confirmatory_endpoint_v02_reproducibility.py"
AUDIT = ROOT / "data/derived/edge_califa_rotation_morphology_confirmatory_endpoint_v02_reproducibility_audit.json"
ENDPOINT = ROOT / "data/derived/edge_califa_rotation_morphology_confirmatory_endpoint_v02.json"
COEFFICIENTS = ROOT / "data/derived/edge_califa_rotation_morphology_confirmatory_endpoint_v02_coefficients.csv"
RAW = Path(os.environ.get("EDGE_CALIFA_HDF5", "/tmp/edge_carma.2d_smo7.hdf5"))


def load_module():
    specification = importlib.util.spec_from_file_location("edge_v02_reproducibility_audit", SCRIPT)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def test_saved_audit_confirms_exact_negative_result() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    inference = audit["reconstructed_exact_inference"]
    assert audit["status"] == "PASS_WITH_PROVENANCE_LIMITATIONS_NEGATIVE_ENDPOINT_CONFIRMED"
    assert audit["failed_error_checks"] == []
    assert inference["n_exact_sign_vectors"] == 128
    assert inference["primary_tail_count"] == 77
    assert inference["primary_exact_one_sided_p"] == 0.6015625
    assert inference["control_max_t_adjusted_p"] == [0.9765625, 0.9453125, 0.3359375]
    assert audit["reconstructed_status"].endswith("PREVALIDATION_FAIL")


def test_saved_coefficients_have_exact_frozen_7_by_20_structure() -> None:
    endpoint = json.loads(ENDPOINT.read_text(encoding="utf-8"))
    frame = pd.read_csv(COEFFICIENTS)
    names = endpoint["galaxies_opened_once"]
    modes = ["m1_cos", "m1_sin", "m2_cos", "m2_sin"]
    expected = [(name, zone, mode) for name in names for zone in range(5) for mode in modes]
    observed = list(zip(frame["galaxy"], frame["zone"].astype(int), frame["mode"]))
    assert frame.shape[0] == 7 * 20
    assert observed == expected


def test_exact_test_is_recomputed_from_saved_q_scores() -> None:
    module = load_module()
    endpoint = json.loads(ENDPOINT.read_text(encoding="utf-8"))
    rows = []
    for name in endpoint["galaxies_opened_once"]:
        scores = endpoint["galaxies"][name]["scores"]
        rows.append([
            scores[label]["q"] - scores["correct"]["q"]
            for label in module.CONTROL_LABELS
        ])
    inference = module.exact_shared_sign_tests(np.asarray(rows))
    assert inference["primary_tail_count"] == 77
    assert inference["primary_exact_one_sided_p"] == 77 / 128
    assert inference["control_max_t_adjusted_p"] == [125 / 128, 121 / 128, 43 / 128]


@pytest.mark.skipif(not RAW.is_file(), reason="hash-pinned public EDGE HDF5 packet is not cached")
def test_full_independent_raw_reconstruction() -> None:
    module = load_module()
    audit = module.build_audit(RAW)
    assert audit["failed_error_checks"] == []
    assert audit["coefficient_structure"]["n_rows"] == 140
    assert audit["coefficient_structure"]["maximum_absolute_raw_reconstruction_residual_km_s"] < 1.0e-12
    assert all(item["rank_and_null_gate_pass"] for item in audit["reconstructed_galaxies"].values())
