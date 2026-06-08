# Readout-Lane Freeze Gate

Status: `READOUT_LANE_FREEZE_GATE_COMPLETE_NOT_ENDPOINT`

This gate freezes allowed and blocked readout lanes for the current key cases
before any future formula scoring. It does not score endpoints.

## Summary

| lane_freeze_status | n_galaxies | n_frozen_pass_like | n_pending_or_blocked | split_b2_universal_rule_status | endpoint_scores_allowed | uses_vobs_or_residual_for_lane_selection | n_future_population_protocol_candidates | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| READOUT_LANE_FREEZE_GATE_COMPLETE_NOT_ENDPOINT | 4 | 4 | 1 | REJECTED_BY_CURRENT_EVIDENCE | False | False | 1 | readout_lane_freeze_gate_not_endpoint |

## Lane Assignments

| galaxy | proposed_subfamily | frozen_lane | lane_freeze_status | allowed_formula_shells | blocked_formula_shells | source_evidence | diagnostic_evidence | remaining_obligation | future_population_protocol_candidate | uses_vobs_or_residual_for_lane_selection | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | K_thick_regular | L_added_source_diagnostic_not_endpoint | DIAGNOSTIC_ONLY_NOT_ENDPOINT | split-B2 unit-load only as q-role/source-load diagnostic | same-curve split-B2 promotion as independent validation | CAVEATED_ACCEPTED_SOURCE_FIELDS_NOT_ENDPOINT_READY | split-B2 repair identified on NGC7331 after exact-transfer failure | needs independent added-readout holdout before validation claim | False | False | False | readout_lane_freeze_gate_not_endpoint |
| NGC5907 | K_projection_dominated | L_projection_attenuation | FROZEN_PASS_CAVEATED | bounded projection/attenuation; mixed projection overlay | standalone added split-B2 ramp; unbounded added warp-history ramp | ACCEPTED_SUBFAMILY_SOURCE_FIELDS_ENDPOINT_STILL_BLOCKED | negative holdout: split-B2 added-readout does not transfer to NGC5907; projection/TPG-like lane remains favored | population validation and source-native HI denominator remain open | False | False | False | readout_lane_freeze_gate_not_endpoint |
| NGC4013 | K_true_compact | L_mixed_overlay_protocol_ready_not_retroactive | FROZEN_PASS_CAVEATED_PROSPECTIVE_ONLY | mixed smooth-carrier plus warp/vertical overlay | retroactive endpoint promotion from existing mixed score | RECLASSIFICATION_REVIEW_REQUIRED | fresh source-freeze review passed; prior score remains forbidden as label evidence | repeat on future predeclared cases; no retroactive validation | True | False | False | readout_lane_freeze_gate_not_endpoint |
| NGC4183 | K_expdisk_overlay | L_projection_attenuation_weak_control_after_review | PREFLIGHT_PASS_WEAK_CONTROL_REVIEW_REQUIRED_NOT_ENDPOINT | near-carrier/null-control projection bound after independent source review | strong projection endpoint; standalone added warp ramp; broad bar/core/history overlay | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | gamma bound 0.00269837; velocity fractional bound 0.0013501; freeze readiness NGC4183_NULL_CONTROL_FREEZE_BLOCKED_REVIEW_REQUIRED | independent profile review before optional null-control freeze | False | False | False | readout_lane_freeze_gate_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| RLF_G1_TAXONOMY_AVAILABLE | PASS | readout_lane_taxonomy_update completed | none | False | readout_lane_freeze_gate_not_endpoint |
| RLF_G2_NGC5907_PROJECTION_FREEZE | PASS_CAVEATED | projection lane favored; added split-B2 rejected | keep caveats and do not run standalone added ramp | False | readout_lane_freeze_gate_not_endpoint |
| RLF_G3_NGC7331_DIAGNOSTIC_BOUNDARY | PASS | positive split-B2 is same-curve diagnostic only | independent added-readout holdout required | False | readout_lane_freeze_gate_not_endpoint |
| RLF_G4_PENDING_CASES | PASS_CAVEATED | NGC4013 is prospective-only protocol ready after fresh source-freeze review; NGC4183 is a completed accepted null-control interval endpoint on its own narrow control branch | NGC4013 needs separate prospective scoring gate; NGC4183 should retain its single-galaxy null-control boundary rather than being treated as mixed validation | False | readout_lane_freeze_gate_not_endpoint |
| RLF_G5_ENDPOINT_USE | BLOCKED | lane freeze is not a formula freeze and not a score | future endpoint scoring requires separate formula freeze | False | readout_lane_freeze_gate_not_endpoint |

## Operational Consequence

NGC5907 may continue as a projection/attenuation or mixed projection case, but
standalone added split-B2 ramp scoring is blocked by the lane freeze. NGC7331
keeps the split-B2 result only as a same-curve diagnostic. NGC4013 is now
prospective-only mixed-overlay protocol ready. NGC4183 has progressed beyond
preflight into a completed accepted null-control interval endpoint on its own
weak-projection control branch: large projection corrections are source-side
disfavored, the frozen interval has been scored without residual-selected point
tuning, and the remaining obligation is to preserve that narrow single-galaxy
control interpretation.

## Claim Boundary

`readout_lane_freeze_gate_not_endpoint`
