# NGC4088 Epsilon-Cross Readout Sensitivity Audit

This audit propagates the residual-blind epsilon_cross protocol bound
through the generated NGC4088 readout profile. It does not compare to
observed rotation residuals and does not authorize endpoint scoring.

## Summary

| galaxy | audit_id | numeric_epsilon_cross_bound | linear_sharp_bound_reference | active_bound_expression | active_bound_source | n_terms | n_branches | n_scenarios | max_leading_delta_v2 | max_abs_cross_increment_v2 | sensitivity_status | promotion_implication | n_pass | n_warn | n_blocked | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_EPSILON_CROSS_READOUT_SENSITIVITY_AUDIT | 0.6875 | 1.375 | |epsilon_cross| <= 0.5*f_PA*f_R + 0.5*f_R*f_q + 0.5*f_q*f_mem | adjacent_locality_chain_bound | 4 | 2 | 5 | 7921.12 | 5445.77 | CROSS_TERM_BOUND_MODERATE | cross-term bound may be usable after source-uncertainty stress tests | 4 | 0 | 0 | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | RSA1_NUMERIC_BOUND_AVAILABLE | PASS | active epsilon_cross bound=0.6875; linear term sum=1.375 | none | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | RSA2_ENDPOINT_BLINDNESS | PASS | audit propagates generated source-native profiles and does not compute residual scores | keep observed velocity columns contextual only | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | RSA3_BOUND_TIGHTNESS | PASS | |epsilon_cross| <= 0.6875 gives max |cross increment| <= 5445.77 km2/s2 | stress-test under source uncertainty | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | RSA4_SIGN_STABILITY | PASS | negative epsilon scenario can invert the leading correction if bound exceeds one | preserve sign-stable bound | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |

## Scenario Audit

| galaxy | branch_id | epsilon_cross_scenario | lambda_multiplier | min_corrected_delta_v2 | max_corrected_delta_v2 | max_abs_cross_increment_v2 | max_leading_delta_v2 | sign_flip_possible | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | p1 | -0.6875 | 0.3125 | 0 | 2475.35 | 5445.77 | 7921.12 | False | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | p1 | -0.34375 | 0.65625 | 0 | 5198.24 | 2722.89 | 7921.12 | False | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | p1 | 0 | 1 | 0 | 7921.12 | 0 | 7921.12 | False | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | p1 | 0.34375 | 1.34375 | 0 | 10644 | 2722.89 | 7921.12 | False | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | p1 | 0.6875 | 1.6875 | 0 | 13366.9 | 5445.77 | 7921.12 | False | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | p2 | -0.6875 | 0.3125 | 0 | 2384.53 | 5245.98 | 7630.51 | False | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | p2 | -0.34375 | 0.65625 | 0 | 5007.52 | 2622.99 | 7630.51 | False | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | p2 | 0 | 1 | 0 | 7630.51 | 0 | 7630.51 | False | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | p2 | 0.34375 | 1.34375 | 0 | 10253.5 | 2622.99 | 7630.51 | False | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |
| NGC4088 | p2 | 0.6875 | 1.6875 | 0 | 12876.5 | 5245.98 | 7630.51 | False | False | False | s4g75_ngc4088_epsilon_cross_readout_sensitivity_audit_not_endpoint |

## Claim Boundary

The audit estimates cross-term readout sensitivity only. A loose bound is
a preserved negative/preparatory result, not a failure of the whole Tau
Core morphology program and not endpoint evidence.
