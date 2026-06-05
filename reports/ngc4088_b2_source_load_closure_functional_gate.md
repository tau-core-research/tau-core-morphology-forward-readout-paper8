# NGC4088 B2 Source-Load Closure Functional Gate

This gate constructs an explicit conditional closure functional for the
NGC4088 frozen warp/history normalization. It does not use endpoint
velocities, residuals, or score ranks.

## Functional

| galaxy | functional_id | kernel | source_load | functional | euler_equation | stationary_solution | numeric_lambda_w_km2_s2 | formula_freeze_alignment_pass | mathematical_status | tau_side_law_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B2_SOURCE_LOAD_CLOSURE_FUNCTIONAL | C_warp(R/R_HI; x_w,p) | Lambda_tau = sigma_warp q_warp x_w Vflat^2 | J_load[lambda_w] = 1/2 kappa_lambda || (lambda_w - Lambda_tau) C_warp ||_W^2 | dJ_load/dlambda_w = kappa_lambda <C_warp,C_warp>_W (lambda_w - Lambda_tau) = 0 | lambda_w = Lambda_tau = sigma_warp q_warp x_w Vflat^2 | 8795.11 | True | EULER_DERIVED_FROM_CONDITIONAL_SOURCE_LOAD_FUNCTIONAL | SOURCE_LOAD_AND_CARRIER_ORIGIN_OPEN | ngc4088_b2_source_load_closure_functional_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | SL1_KERNEL_IS_RESIDUAL_BLIND_AND_DIMENSIONLESS | PASS | C_warp is frozen from source-side x_w, p, q_warp and is dimensionless | none at kernel/dimension level | False | False | ngc4088_b2_source_load_closure_functional_gate_not_endpoint |
| NGC4088 | SL2_SOURCE_LOAD_ALIGNED_TO_FREEZE | PASS | Lambda_tau computed from frozen sigma, q_warp, x_w, and Vflat reproduces lambda_w | none at formula-freeze alignment level | False | False | ngc4088_b2_source_load_closure_functional_gate_not_endpoint |
| NGC4088 | SL3_EULER_STATIONARITY | PASS | for kappa_lambda>0 and nonzero kernel norm, dJ/dlambda_w=0 yields lambda_w=Lambda_tau | derive kappa_lambda and norm weight from Tau-side closure geometry | False | False | ngc4088_b2_source_load_closure_functional_gate_not_endpoint |
| NGC4088 | SL4_ZERO_SOURCE_LIMIT | PASS | sigma_warp=0 or q_warp=0 gives Lambda_tau=0 and the stationary correction vanishes | none at zero-source limit level | False | False | ngc4088_b2_source_load_closure_functional_gate_not_endpoint |
| NGC4088 | SL5_INACTIVE_WINDOW_LIMIT | PASS | C_warp=0 for R/R_HI <= x_w, so the readout recovers the carrier in the inactive window | none at inactive-window limit level | False | False | ngc4088_b2_source_load_closure_functional_gate_not_endpoint |
| NGC4088 | SL6_SOURCE_LOAD_ORIGIN | OPEN | the source-load form is explicit but not derived as the unique Tau-side closure load | derive why Lambda_tau must be sigma_warp q_warp x_w Vflat^2 | False | False | ngc4088_b2_source_load_closure_functional_gate_not_endpoint |
| NGC4088 | SL7_ASYMPTOTIC_CARRIER_ORIGIN | OPEN | ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED | derive Vflat^2 as the forced asymptotic carrier | False | False | ngc4088_b2_source_load_closure_functional_gate_not_endpoint |
| NGC4088 | SL8_CROSS_TERM_BOUND | OPEN | CROSS_TERMS_DECLARED_NOT_SUPPRESSED | prove cross-term suppression or freeze a source-side uncertainty interval | False | False | ngc4088_b2_source_load_closure_functional_gate_not_endpoint |

## Summary

| galaxy | closure_functional_status | numeric_lambda_w_km2_s2 | formula_freeze_alignment_pass | n_gates | n_pass | n_open | law_level_closed | endpoint_scores_allowed | uses_vobs_or_residual | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | SOURCE_LOAD_CLOSURE_FUNCTIONAL_CONSTRUCTED_CONDITIONALLY | 8795.11 | True | 8 | 5 | 3 | False | False | False | derive the source-load origin, the Vflat^2 carrier theorem, and the cross-term suppression bound | ngc4088_b2_source_load_closure_functional_gate_not_endpoint |

## Interpretation

The closure-functional premise is now sharper: given the source-load
`Lambda_tau = sigma_warp q_warp x_w Vflat^2`, the explicit norm-square
functional has an Euler equation whose stationary solution is the frozen
normalization. This is still not a final Tau-side physical law, because
the source-load origin, forced `Vflat^2` carrier theorem, and cross-term
suppression remain open.
