# Mixed Readout Population Validation Gate

This gate states what would count as evidence for the mixed 4D readout
program. It does not score rotations and does not promote NGC4013
retroactively. It turns the proof idea into a predeclared population
protocol.

## Protocol

| gate_id | required_condition | pass_measure | failure_mode | claim_boundary |
| --- | --- | --- | --- | --- |
| MPG1_RESIDUAL_BLIND_LABEL | mixed candidates are selected from source fields before rotation scoring | source_rule_pass=True and diagnostic scores excluded as label inputs | mixed label chosen from RMSE, required S_tau, or wrong-family result | mixed_readout_population_validation_gate_not_endpoint |
| MPG2_FORMULA_FREEZE | carrier, overlay kernel, sign, amplitude, and radial window are frozen before scoring | formula_freeze_status is ready and uses_vobs_or_residual_in_construction=False | formula ingredient changed after observing endpoint residuals | mixed_readout_population_validation_gate_not_endpoint |
| MPG3_MATCHED_VS_PURE_CONTROLS | mixed readout beats its pure carrier and pure overlay controls | RMSE_mixed < RMSE_pure_carrier and RMSE_mixed < RMSE_pure_overlay | mixed shell acts only as an over-flexible or redundant correction | mixed_readout_population_validation_gate_not_endpoint |
| MPG4_MATCHED_VS_WRONG_AND_SHUFFLED | mixed matched labels beat wrong-family and shuffled-label controls | Delta_mixed > 0 and correct-family rank improves against shuffled/null labels | improvement also appears under wrong or shuffled labels | mixed_readout_population_validation_gate_not_endpoint |
| MPG5_BASELINE_COMPARISON | mixed readout is compared with Newtonian, MOND/RAR, and TPG/RMOND-facing baselines | baseline competitiveness reported without claiming universal superiority unless population endpoint passes | baseline comparison omitted or overclaimed | mixed_readout_population_validation_gate_not_endpoint |
| MPG6_NEGATIVE_CONTROL | non-mixed source-control galaxies should not be systematically improved by the mixed formula | mixed-readout improvement concentrates in source-rule-positive cases | mixed formula improves everything, suggesting excess flexibility | mixed_readout_population_validation_gate_not_endpoint |

## Current Cases And Controls

| galaxy | case_role | candidate_mixed_readout | source_rule_pass | formula_freeze_status | prospective_protocol_ready | retrospective_endpoint_allowed | population_validation_use | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | source_rule_positive_mixed_candidate | K_expdisk_warp_vertical_overlay | True | MIXED_FORMULA_FREEZE_READY_NOT_RETROACTIVE_ENDPOINT | True | False | prospective_protocol_case_only_not_validation | source-rule and formula-freeze pass, but existing mixed score is not retroactive endpoint validation |
| NGC5907 | source_rule_positive_mixed_formula_freeze_candidate | K_expdisk_projection_warp_vertical_overlay_review | True | MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING | True | False | prospective_protocol_case_only_not_validation | fresh mixed formula-freeze exists, but prior projection endpoint cannot be reused as mixed-readout evidence and no mixed endpoint score is run here |
| NGC7331 | caveated_source_rule_positive_mixed_formula_freeze_candidate | K_expdisk_thick_outer_warp_overlay_review | True | CAVEATED_MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING | True | False | caveated_prospective_protocol_case_only_not_validation | caveated vertical/outer-warp mixed formula-freeze exists, but broad outer window must be reported and no mixed endpoint score is run here |
| IC2574 | disturbed_tail_control_not_mixed | not_source_rule_positive_mixed_case | False | NOT_APPLICABLE | False | False | negative_or_acquisition_control | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING |
| UGC05716 | tail_asymmetry_candidate_control_not_mixed | not_source_rule_positive_mixed_case | False | NOT_APPLICABLE | False | False | negative_or_acquisition_control | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING |
| NGC4183 | expdisk_overlay_acquisition_candidate_context_only | not_source_rule_positive_mixed_case | False | NOT_APPLICABLE | False | False | negative_or_acquisition_control | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING |

## Endpoints To Run After Freeze

| endpoint_id | definition | pass_condition | status | claim_boundary |
| --- | --- | --- | --- | --- |
| DELTA_MIXED_PURE | mean or median RMSE(best pure carrier/overlay control) - RMSE(matched mixed readout) | > 0 on predeclared mixed source-rule-positive cases | NOT_RUN_POPULATION_ENDPOINT | mixed_readout_population_validation_gate_not_endpoint |
| DELTA_MIXED_WRONG | RMSE(wrong-family mean) - RMSE(matched mixed readout) | > 0 and correct family rank improves | NOT_RUN_POPULATION_ENDPOINT | mixed_readout_population_validation_gate_not_endpoint |
| SHUFFLED_MIXED_NULL | matched-vs-shuffled improvement under randomized mixed labels | predeclared matched labels beat shuffled/null labels | NOT_RUN_POPULATION_ENDPOINT | mixed_readout_population_validation_gate_not_endpoint |
| BASELINE_COMPETITIVENESS | mixed readout versus Newtonian, MOND/RAR proxy, TPG/v6/RMOND-facing proxy | reported with caveats; no universal superiority claim unless population endpoint passes | NOT_RUN_POPULATION_ENDPOINT | mixed_readout_population_validation_gate_not_endpoint |
| NON_MIXED_NEGATIVE_CONTROL | apply mixed formula only as forbidden/control lane to non-mixed source-rule-negative galaxies | mixed improvement is not systematic in non-mixed controls | NOT_RUN_POPULATION_ENDPOINT | mixed_readout_population_validation_gate_not_endpoint |

## Summary

| validation_gate_status | n_cases_listed | n_source_rule_positive_mixed_cases | n_prospective_protocol_ready_cases | min_independent_prospective_cases_required | endpoint_scores_run | diagnostic_scores_used_as_label_input | current_claim | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MIXED_POPULATION_VALIDATION_READY | 6 | 3 | 3 | 3 | False | False | NGC4013, NGC5907, and caveated NGC7331 supply frozen prospective mixed protocols, but no mixed endpoint scoring has been run here | run the predeclared mixed-population endpoints from unchanged frozen manifests, preserving NGC7331 broad-window caveats | mixed_readout_population_validation_gate_not_endpoint |

## Claim Boundary

The current package still does not have enough independent prospective
mixed protocols for population validation. Frozen protocol rows are
formula-preparation results only; population scoring remains blocked
until the minimum case count is reached and the scoring endpoints are
run from unchanged frozen manifests.
