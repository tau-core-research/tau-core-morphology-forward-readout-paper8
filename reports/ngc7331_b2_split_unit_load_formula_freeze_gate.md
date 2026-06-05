# NGC7331 split-B2 unit-load formula-freeze candidate

This freezes the split-B2 unit-load branch as a diagnostic/theory
candidate without reading observed velocities. It is not an accepted
same-curve endpoint because the branch was identified after the
NGC7331 exact-transfer failure audit.

## Summary

| galaxy | formula_id | formula_freeze_status | lambda_split_km2_s2 | x_w_formula_freeze | vflat_km_s | mu_load | n_kernel_grid_rows | n_gates | n_pass | n_formula_conditional | n_blocked | uses_vobs_or_residual_in_construction | formula_frozen_before_endpoint_scoring | endpoint_scores_allowed | future_predeclared_protocol_candidate | claim_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_SPLIT_B2_UNIT_LOAD_FREEZE_DIAGNOSTIC_V1 | NGC7331_SPLIT_B2_UNIT_LOAD_FORMULA_FREEZE_DIAGNOSTIC_READY_NOT_ENDPOINT | 30520.3 | 0.534309 | 239 | 1 | 36 | 5 | 3 | 1 | 1 | False | False | False | True | diagnostic formula-freeze candidate only; not an accepted NGC7331 endpoint because branch selection followed the failure audit | ngc7331_b2_split_unit_load_formula_freeze_diagnostic_not_endpoint |

## Manifest

| galaxy | formula_id | readout_family | parent_failed_formula_id | branch_origin | mu_load_origin | carrier | formula_text | delta_text | kernel_text | source_load_text | q_shape_handling | q_shape_interval | x_w_formula_freeze | rhi_kpc | vflat_km_s | sigma_warp | mu_load | lambda_split_km2_s2 | turn_on_power_frozen | dimension_check | inactive_window_limit | zero_source_limit | ngc4088_recovery_limit | selection_caveat | uses_vobs_or_residual_in_construction | formula_frozen_before_endpoint_scoring | endpoint_scores_allowed | future_predeclared_protocol_candidate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_SPLIT_B2_UNIT_LOAD_FREEZE_DIAGNOSTIC_V1 | K_warp_history_split_b2_unit_load | NGC7331_EXACT_B2_TRANSFER_INTERVAL_FREEZE_V1 | NGC7331_B2_SPLIT_Q_SOURCE_LOAD_THEORY_GATE_BUILT_ENDPOINT_BLOCKED | SPLIT_B2_UNIT_MU_LOAD_CONDITIONAL_DERIVATION_BUILT_ENDPOINT_BLOCKED | v_Newtonian_baryonic | v_readout^2(R)=v_Newtonian_baryonic^2(R)+sigma_warp*mu_load*x_w*Vflat^2*ramp(R/R_HI;x_w) | Delta v^2_split(R)=sigma_warp*mu_load*x_w*Vflat^2*max(0,(R/R_HI-x_w)/(1-x_w)) | K_shape=ramp=max(0,(x-x_w)/(1-x_w)) | mu_load=1 conditional normalized split-load coordinate | q_shape interval is carried as morphology evidence and is not multiplied into both amplitude and kernel | [0.0079404475812108, 0.2057957876154617] | 0.534309 | 27.01 | 239 | 1 | 1 | 30520.3 | 1 | PASS: sigma, mu_load, x_w, and ramp are dimensionless; Vflat^2 supplies km^2/s^2 | PASS: R/R_HI<=x_w implies ramp=0 and carrier recovery | PASS: sigma_warp=0 or mu_load=0 gives Delta v^2=0 | recovers the original NGC4088 protocol when q_shape=1 and mu_load=1 | branch identified after NGC7331 exact-transfer failure; not an accepted endpoint freeze for this same scored curve | False | False | False | True | ngc7331_b2_split_unit_load_formula_freeze_diagnostic_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | galaxy | formula_id | endpoint_scores_allowed | uses_vobs_or_residual_in_construction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPLITB2F1_PARENT_FAILURE_LOCALIZED | PASS | NGC7331_B2_SPLIT_Q_SOURCE_LOAD_THEORY_GATE_BUILT_ENDPOINT_BLOCKED | none for diagnostic freeze candidate | NGC7331 | NGC7331_SPLIT_B2_UNIT_LOAD_FREEZE_DIAGNOSTIC_V1 | False | False | ngc7331_b2_split_unit_load_formula_freeze_diagnostic_not_endpoint |
| SPLITB2F2_MU_LOAD_CONDITIONAL | FORMULA_CONDITIONAL | SPLIT_B2_UNIT_MU_LOAD_CONDITIONAL_DERIVATION_BUILT_ENDPOINT_BLOCKED | derive final Tau-side source-load origin or acquire accepted residual-blind load observable | NGC7331 | NGC7331_SPLIT_B2_UNIT_LOAD_FREEZE_DIAGNOSTIC_V1 | False | False | ngc7331_b2_split_unit_load_formula_freeze_diagnostic_not_endpoint |
| SPLITB2F3_DIMENSIONS_LIMITS | PASS | velocity-squared units and inactive/zero-source limits pass | none at dimensional/protocol level | NGC7331 | NGC7331_SPLIT_B2_UNIT_LOAD_FREEZE_DIAGNOSTIC_V1 | False | False | ngc7331_b2_split_unit_load_formula_freeze_diagnostic_not_endpoint |
| SPLITB2F4_ENDPOINT_BLIND_CONSTRUCTION | PASS | grid uses r and vn only; no vobs/residual columns | none for construction blindness | NGC7331 | NGC7331_SPLIT_B2_UNIT_LOAD_FREEZE_DIAGNOSTIC_V1 | False | False | ngc7331_b2_split_unit_load_formula_freeze_diagnostic_not_endpoint |
| SPLITB2F5_SAME_CURVE_ENDPOINT_ELIGIBILITY | BLOCKED_POST_FAILURE_BRANCH | branch selected after exact B2 failure audit on NGC7331 | use only as diagnostic or predeclare for independent holdout/population test | NGC7331 | NGC7331_SPLIT_B2_UNIT_LOAD_FREEZE_DIAGNOSTIC_V1 | False | False | ngc7331_b2_split_unit_load_formula_freeze_diagnostic_not_endpoint |

## Interpretation

The freeze candidate repairs the q-role conflation by carrying the
`q_shape` interval as morphology evidence and using the conditional
normalized split-load coordinate `mu_load=1`. The resulting branch may
be used for future predeclared holdout/population tests, but on NGC7331
it remains diagnostic because its selection followed a failed transfer
audit.
