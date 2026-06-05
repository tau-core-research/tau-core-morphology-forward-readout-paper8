# NGC7331 B2 Exact Transfer Upgrade Gate

This gate checks whether NGC7331 can move from outer-warp analogue to
exact NGC4088-style B2 source-load transfer. It is not an endpoint score.

## Fields

| galaxy | field_id | required_b2_field | field_status | value | unit | source_basis | source_status | exact_transfer_use | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_ET1_XW | x_w | SOURCE_ONSET_AVAILABLE_REPLAY_ONLY | 0.5343091911302521 | dimensionless | Bosma/NED fractional Holmberg onset converted with SPARC distance and R_HI | FRACTIONAL_WARP_ONSET_SOURCE_READY_REPLAY_REQUIRED | available for future exact transfer formula-freeze only; not retroactive V1 update | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ET2_Q_WARP | q_warp | SOURCE_ONLY_Q_WARP_INTERVAL_CARRIED | [0.0079404475812108, 0.2057957876154617] | dimensionless | source-only review carries full THINGS centroid/envelope q_warp interval | FORMULA_FREEZE_INPUT_READY_INTERVAL_CARRIED | available for exact B2 freeze as an explicit interval, not a scalar point | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ET3_SIGMA_WARP | sigma_warp | MOM1_SIGN_CONTEXT_CARRIED_TO_FORMULA_FREEZE | MOM1_CONTEXT_CONSISTENT_RECEDING_SIDE_ORIENTATION_CARRIED_TO_FORMULA_FREEZE | dimensionless_sign | CAVEAT_CONFIRMED_AS_OVERLAY_CONTEXT; CONTEXT_SOURCE_FIELD_REVIEW_READY | FORMULA_FREEZE_INPUT_READY_SIGN_CONTEXT_CARRIED | available as carried sign-context input; exact formula must state sign convention | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ET4_VFLAT | Vflat | SOURCE_CATALOG_AVAILABLE | 239.0 | km_s | SPARC external master table | ACCEPTED_CATALOG_FIELD | available carrier input | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ET5_EPSILON_CROSS | epsilon_cross_inputs | CONSERVATIVE_EPSILON_CROSS_BOUND_CARRIED | CARRY_CONSERVATIVE_SOURCE_BOUND_0.488571397976179_WITH_Q_OBSERVABLE_AMBIGUITY | dimensionless_bound_inputs | source-only review carries conservative MOM1/q-observable ambiguity bound | FORMULA_FREEZE_INPUT_READY_BOUND_CARRIED | available for exact B2 freeze as an explicit uncertainty/cross-term caveat | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ET6_UNIT_Q_SIGMA_LAMBDA_PREVIEW | lambda_preview_not_formula | DERIVED_PREVIEW_NOT_FORMULA_FREEZE | 30520.27530655113 | km2_s2 | x_w * Vflat^2 assuming q=sigma=1 only as a diagnostic preview | NOT_A_FREEZE_INPUT | for dimensional preview only; must not be scored or called a formula | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_ETG1_XW_ONSET | PASS_REPLAY_ONLY | x_w=0.534309 from fractional outer-warp onset gate | use only in future exact-transfer freeze/replay, not retroactive V1 endpoint update | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ETG2_VFLAT_CARRIER | PASS | SPARC Vflat=239 km/s | none at source-catalog carrier field level | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ETG3_Q_WARP | PASS_INTERVAL_CARRIED | q_warp interval carried: [0.0079404475812108, 0.2057957876154617] | carry q interval into exact-transfer formula freeze | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ETG4_SIGMA_WARP | PASS_CONTEXT_CARRIED | MOM1_CONTEXT_CONSISTENT_RECEDING_SIDE_ORIENTATION_CARRIED_TO_FORMULA_FREEZE | state the exact added-readout/attenuation sign in the freeze gate | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ETG5_EPSILON_CROSS | PASS_BOUND_CARRIED | CARRY_CONSERVATIVE_SOURCE_BOUND_0.488571397976179_WITH_Q_OBSERVABLE_AMBIGUITY | carry conservative epsilon_cross caveat into exact-transfer formula freeze | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ETG6_DIMENSION_PREVIEW | PASS_NOT_FREEZE | x_w * Vflat^2 has velocity-squared units | do not score the preview lambda without q/sigma/cross-term freeze | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | N7331_ETG7_ENDPOINT_BLINDNESS | PASS | all fields are source-side or catalog-side; no vobs residuals are read | keep any future scoring in a separate endpoint script | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |

## Worklist

| galaxy | work_item | missing_field | preferred_source | acceptance_rule | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | W1_EXACT_TRANSFER_FORMULA_FREEZE_GATE | none_at_input_gate | validated q interval, MOM1 sign context, and conservative epsilon_cross bound | freeze exact-transfer formula without reading vobs or endpoint residuals | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | W2_INTERVAL_PROPAGATION | point_q_warp_not_selected | CARRY_INTERVAL source-only review response | carry q_warp interval rather than collapsing to a scalar unless a future source theorem selects one observable | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |
| NGC7331 | W3_ENDPOINT_GATE_AFTER_FREEZE | endpoint_score_not_allowed_yet | future formula-freeze manifest | only a separate endpoint gate may read vobs after the freeze manifest is fixed | False | False | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |

## Summary

| galaxy | exact_transfer_upgrade_status | source_candidate_status_from_manifest | x_w_available | vflat_available | q_warp_available | sigma_warp_available | epsilon_cross_inputs_available | unit_q_sigma_lambda_preview_km2_s2 | n_gates | n_pass_like | n_blocked | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | population_claim_allowed | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXACT_TRANSFER_UPGRADE_FORMULA_FREEZE_INPUT_READY_NOT_ENDPOINT | PARTIAL_EXACT_TRANSFER_CANDIDATE_SOURCE_GAPS | True | True | True | True | True | 30520.3 | 7 | 7 | 0 | True | False | False | False | build exact B2 transfer formula-freeze gate carrying q interval and epsilon caveat | ngc7331_b2_exact_transfer_upgrade_gate_not_endpoint |

## Interpretation

NGC7331 has now cleared the response-pending source-input blocker: q_warp is carried as a THINGS centroid/envelope interval, MOM1 supplies orientation context, and epsilon_cross is carried as a conservative source-side caveat. This is formula-freeze input readiness, not an endpoint result; a separate exact-transfer formula-freeze gate must still be built before any scoring.
