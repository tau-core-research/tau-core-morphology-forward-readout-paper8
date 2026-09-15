import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_halogas_candidate_pool_is_endpoint_blind_and_does_not_overfill_n12():
    subprocess.run(
        [sys.executable, "scripts/audit_multigalaxy_halogas_confirmatory_candidate_pool_v01.py"],
        cwd=ROOT,
        check=True,
    )
    payload = json.loads(
        (ROOT / "data/derived/multigalaxy_halogas_confirmatory_candidate_pool_v01.json").read_text()
    )
    assert payload["status"] == "SOURCE_ACQUISITION_ONLY_HALOGAS_ALONE_INSUFFICIENT_FOR_CONFIRMATORY_N12"
    assert payload["n_halogas_galaxies"] == 24
    assert payload["n_endpoint_unopened_moderate_candidates"] == 7
    assert payload["n_clean_source_candidates"] == 0
    assert payload["halogas_clean_shortfall"] == 12
    assert payload["priority_order"] == []
    assert payload["next_clean_source_acquisition_target"] is None
    assert payload["ngc4062_endpoint"]["confirmatory_pass"] is False
    assert payload["ngc4062_endpoint"]["velocity_zero_point_sign_stable"] is False
    assert payload["ngc0925_source_constants"]["digitized_ring_count"] == 93
    assert "TERMINAL_CLEANLINESS_FAIL" in payload["ngc0925_source_constants"]["outer_only_status"]
    assert payload["endpoint_pixels_read_by_this_audit"] is False
    assert "does not create a new score" in payload["claim_boundary"]

    protocol = json.loads(
        (ROOT / "data/protocols/multigalaxy_signed_morphology_side_consistency_confirmatory_v01.json").read_text()
    )
    assert {"NGC2541", "NGC3198", "NGC5055"} <= set(protocol["development_cases_excluded"])
    assert protocol["current_source_pool_audit"]["endpoint_unopened_moderate_inclination_candidates"] == 8
    assert protocol["current_source_pool_audit"]["endpoint_pixels_opened_by_audit"] is False
