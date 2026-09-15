import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data/protocols/multigalaxy_signed_morphology_side_consistency_confirmatory_v01.json"


def test_confirmatory_protocol_preserves_independent_population_claim_boundary():
    payload = json.loads(PROTOCOL.read_text())

    assert payload["status"] == "SOURCE_ONLY_CONFIRMATORY_PROTOCOL_FROZEN_ENDPOINTS_NOT_ACQUIRED"
    assert payload["freeze_stage"] == "before confirmatory endpoint-map access"
    assert "NGC2541" in payload["development_cases_excluded"]
    assert payload["minimum_confirmatory_galaxies"] >= 12
    assert payload["inference_unit"] == "galaxy"
    assert payload["galaxy_weighting"] == "equal"
    assert payload["promotion_gate"]["max_T_adjusted_p_A_at_most"] <= 0.01
    assert payload["promotion_gate"]["max_T_adjusted_p_D_at_most"] <= 0.01
    assert payload["promotion_gate"]["all_eligibility_and_nuisance_conditions_required"] is True
    assert "would not derive or select a physical q_R" in payload["claim_boundary"]
