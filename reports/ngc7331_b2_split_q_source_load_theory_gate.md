# NGC7331 B2 split q/source-load theory gate

This gate is built after the NGC7331 exact B2 interval-control failure
and the q-role diagnostic. It does not score an endpoint. It rewrites
the B2 shell so `q_shape` and `mu_load` are no longer identified by
default.

## Summary

| galaxy | split_gate_status | recommended_next_branch | source_scale_xw_vflat2_km2_s2 | q_shape_interval | mu_load_status | n_formula_branches | n_mu_load_candidates | n_gates | n_pass_like | n_open | n_blocked | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | claim_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_B2_SPLIT_Q_SOURCE_LOAD_THEORY_GATE_BUILT_ENDPOINT_BLOCKED | B2_SPLIT_UNIT_KERNEL_LOAD | 30520.3 | [0.0079404475812108, 0.2057957876154617] | OPEN_NOT_TAU_SIDE_DERIVED | 3 | 4 | 6 | 4 | 1 | 1 | False | False | False | theory reformulation only; q_shape/mu_load split required before any future NGC7331 B2 point branch | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |

## Formula branches

| branch_id | formula_text | effective_q_power | kernel_text | source_load_text | ngc4088_limit | ngc7331_status | theory_status | galaxy | dimension_check | inactive_window_limit | zero_source_limit | uses_vobs_or_residual_in_construction | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B2_ORIGINAL_IDENTIFIED_Q | Delta v^2 = sigma_warp q_shape x_w Vflat^2 * q_shape ramp(x;x_w) | 2 | K_shape = q_shape ramp | mu_load identified with q_shape | recovers original protocol when q_shape=1 | DIAGNOSTICALLY_REJECTED_FOR_TRANSFER | FORMULA_CONDITIONAL_Q_ROLE_CONFLATED | NGC7331 | PASS: x_w, q_shape, mu_load, sigma_warp, and ramp are dimensionless; Vflat^2 supplies km^2/s^2 | PASS: ramp=0 for x<=x_w | PASS if sigma_warp=0 or mu_load=0; original branch also zeroes if q_shape=0 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |
| B2_SPLIT_UNIT_KERNEL_LOAD | Delta v^2 = sigma_warp mu_load x_w Vflat^2 * ramp(x;x_w) | 0 | K_shape = ramp; q_shape carried as morphology evidence | mu_load independent Tau-side source-load handle | recovers original protocol when q_shape=1 and mu_load=1 | BEST_DIAGNOSTIC_SHAPE_REPAIR_NOT_ENDPOINT | PREFERRED_NEXT_THEORY_BRANCH_MU_LOAD_OPEN | NGC7331 | PASS: x_w, q_shape, mu_load, sigma_warp, and ramp are dimensionless; Vflat^2 supplies km^2/s^2 | PASS: ramp=0 for x<=x_w | PASS if sigma_warp=0 or mu_load=0; original branch also zeroes if q_shape=0 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |
| B2_SPLIT_Q_KERNEL_LOAD | Delta v^2 = sigma_warp mu_load x_w Vflat^2 * q_shape ramp(x;x_w) | 1 | K_shape = q_shape ramp | mu_load independent Tau-side source-load handle | recovers original protocol when q_shape=1 and mu_load=1 | POSSIBLE_BUT_REQUIRES_LARGE_MU_LOAD | SECONDARY_BRANCH_MU_LOAD_AND_Q_KERNEL_ROLE_OPEN | NGC7331 | PASS: x_w, q_shape, mu_load, sigma_warp, and ramp are dimensionless; Vflat^2 supplies km^2/s^2 | PASS: ramp=0 for x<=x_w | PASS if sigma_warp=0 or mu_load=0; original branch also zeroes if q_shape=0 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |

## Residual-blind mu_load candidates

| candidate_id | mu_load_rule | source_basis | available_value | residual_blind | freeze_status | remaining_obligation | galaxy | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MU0_UNIT_ASYMPTOTIC_LOAD | mu_load = 1 | minimal source-load normalization after separating q_shape; uses x_w Vflat^2 as carrier scale | 1.0 | True | CANDIDATE_RULE_READY_NOT_LAW_DERIVED | derive why the split source-load coefficient is unity from Tau-side closure/readout structure | NGC7331 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |
| MU_VERTICAL_OVERLAY_CONTEXT | mu_load = f(vertical_activation, projection_context) | existing NGC7331 vertical/outer-warp caveat layer; vertical_activation_candidate=0.63081 | 0.6308100929614875 | True | CONTEXT_AVAILABLE_FUNCTION_NOT_DERIVED | derive the mapping from vertical/projection evidence to mu_load | NGC7331 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |
| MU_CROSS_CONTEXT_BOUND | mu_load interval widened by epsilon_cross | MOM1 sign/cross review carries conservative bound epsilon_cross=0.488571 | 0.488571397976179 | True | BOUND_AVAILABLE_NOT_PRIMARY_LOAD_RULE | keep as uncertainty/cross-term bound, not as primary source-load fit | NGC7331 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |
| MU_HI_SUPPORT_OR_HISTORY_COHERENCE | mu_load = F(HI support, warp coherence, history memory) | scientifically motivated by bridge, but no accepted numeric NGC7331 source observable is frozen yet | <NA> | True | SOURCE_OBSERVABLE_MISSING | define and extract residual-blind support/coherence/history observable | NGC7331 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | galaxy | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B2S1_FAILURE_LOCALIZED | PASS | NGC7331_B2_Q_ROLE_SEPARATION_DIAGNOSTIC_COMPLETE_NOT_ENDPOINT | none for failure localization | NGC7331 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |
| B2S2_Q_SHAPE_SOURCE_AVAILABLE | PASS_INTERVAL | [0.0079404475812108, 0.2057957876154617] | rename/use as q_shape; do not identify with mu_load by default | NGC7331 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |
| B2S3_DIMENSIONS_LIMITS | PASS | split formulas are dimensionally valid and recover inactive window | none at dimensional/protocol level | NGC7331 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |
| B2S4_MU_LOAD_SOURCE_ORIGIN | OPEN | unit, vertical, cross, and HI/history candidates listed | derive or source-freeze mu_load before any endpoint freeze | NGC7331 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |
| B2S5_SIGN_CONTEXT | CARRIED_CAVEATED | NGC7331_THINGS_MOM1_SIGN_CROSS_REVIEW_BUILT_FREEZE_BLOCKED | freeze sign convention independently if point branch is built | NGC7331 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |
| B2S6_ENDPOINT_ELIGIBILITY | BLOCKED | post-failure diagnostic only | new formula branch must be predeclared and frozen before scoring | NGC7331 | False | False | ngc7331_b2_split_q_source_load_theory_gate_not_endpoint |

## Verdict

The current exact-transfer failure is best treated as a source-load
role-confusion failure, not as proof that the B2 radial ramp is useless.
The next admissible path is to derive or source-freeze an independent
`mu_load` before scoring. The most economical theory branch is
`B2_SPLIT_UNIT_KERNEL_LOAD`, but it remains blocked until `mu_load=1`
or another source-load rule is derived from Tau-side closure/readout
structure rather than endpoint residuals.
