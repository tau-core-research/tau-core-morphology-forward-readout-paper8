# NGC4088 B2 Population-Transfer Preflight Gate

This gate asks whether the frozen NGC4088 B2 source-load/carrier theorem
has already transferred to a population. It does not score rotations and
does not use endpoint residuals.

## Cases

| galaxy | case_role | candidate_protocol | source_protocol_status | exact_b2_source_load_protocol | same_carrier_rule_available | formula_frozen_before_scoring | uses_endpoint_scores_or_residual | population_transfer_status | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | reference_exact_protocol | K_warp_history_caveated_protocol | FROZEN_VFLAT2_CARRIER_CONDITIONAL_THEOREM_LAW_PROOF_OPEN | True | True | True | False | REFERENCE_SINGLE_GALAXY_CONDITIONAL_THEOREM | repeat exact source-load/carrier gate on independent warp/history galaxies before population claims | False | ngc4088_b2_population_transfer_preflight_gate_not_endpoint |
| NGC4013 | prospective_mixed_overlay_analogue | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | MIXED_FORMULA_FREEZE_READY_NOT_RETROACTIVE_ENDPOINT | False | False | False | False | PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER | derive separate mixed carrier-plus-overlay carrier rule or acquire exact warp/history source-load fields | False | ngc4088_b2_population_transfer_preflight_gate_not_endpoint |
| NGC5907 | prospective_projection_mixed_analogue | NGC5907_EXPDISK_PROJECTION_MIXED_FREEZE_V1 | MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING | False | False | True | False | PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER | projection-dominated mixed carrier is useful control evidence, not the NGC4088 warp/history source-load theorem | False | ngc4088_b2_population_transfer_preflight_gate_not_endpoint |
| NGC7331 | caveated_outer_warp_mixed_analogue | NGC7331_EXPDISK_VERTICAL_OUTER_WARP_MIXED_FREEZE_V1 | CAVEATED_MIXED_FORMULA_FREEZE_READY_PRIOR_TO_MIXED_SCORING | False | False | True | False | CAVEATED_PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER | broad outer-window caveat and missing numeric onset block exact B2 transfer use | False | ngc4088_b2_population_transfer_preflight_gate_not_endpoint |
| IC2574 | blocked_acquisition_control | not_source_rule_positive_mixed_case | NOT_APPLICABLE | False | False | False | False | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | False | ngc4088_b2_population_transfer_preflight_gate_not_endpoint |
| UGC05716 | blocked_acquisition_control | not_source_rule_positive_mixed_case | NOT_APPLICABLE | False | False | False | False | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | False | ngc4088_b2_population_transfer_preflight_gate_not_endpoint |
| NGC4183 | blocked_acquisition_control | not_source_rule_positive_mixed_case | NOT_APPLICABLE | False | False | False | False | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | False | ngc4088_b2_population_transfer_preflight_gate_not_endpoint |

## Summary

| population_transfer_preflight_status | n_cases | n_reference_exact_protocol | n_exact_transfer_ready_excluding_reference | n_partial_analogues | n_blocked_acquisition_controls | endpoint_scores_allowed | uses_vobs_or_residual | law_level_closed | population_claim_allowed | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| POPULATION_TRANSFER_PREFLIGHT_BUILT_EXACT_TRANSFER_BLOCKED_ANALOGUE_LANE_AVAILABLE | 7 | 1 | 0 | 3 | 3 | False | False | False | False | acquire or predeclare at least two independent exact warp/history source-load cases with x_w, q_warp, sigma_warp, Vflat, and cross-term source observables frozen before scoring | ngc4088_b2_population_transfer_preflight_gate_not_endpoint |

## Interpretation

The package now has one exact reference case, NGC4088, with a frozen
`Vflat^2` conditional carrier theorem. NGC4013, NGC5907, and NGC7331
are useful mixed overlay/projection analogues, but they are not exact
transfers of the NGC4088 warp/history source-load protocol. Therefore
the population-transfer lane is explicitly built but remains blocked for
claims until independent exact warp/history cases are source-frozen.
