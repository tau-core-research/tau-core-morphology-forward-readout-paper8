# NGC4088 Closure-Functional Requirement Gate

This gate specifies what a Tau-side closure/readout functional would
need to prove before the selected NGC4088 warp/asymmetry normalization
can be promoted from conditional formula to derived readout law.

## Verdict

The source basis and dimensionful carrier candidate are available, but
the functional itself is not constructed. The Euler/closure condition
that would solve for `lambda_w = x_w Vflat^2` remains blocked.

## Functional Requirement

| galaxy | functional_id | required_form | solved_scale_if_derived | readout_formula_if_derived | current_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_WARP_ASYMMETRY_CLOSURE_FUNCTIONAL_REQUIREMENT | J_tau[lambda_w] = closure_cost(lambda_w; Q_D, Q_N, x_w, C_warp) + asymptotic_carrier_penalty(lambda_w; Vflat^2) + autonomy_penalty(lambda_w; external_comparators) | lambda_w = sigma_warp q_warp x_w Vflat^2 | delta_v2_warp(R;p) = lambda_w C_warp(R/R_HI; x_w, p) | FUNCTIONAL_REQUIREMENT_NOT_CONSTRUCTED | s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | F1_SOURCE_BASIS_AVAILABLE | PASS | C_warp(R/R_HI; x_w, p) exists as a residual-blind filled source basis | none at basis-availability level | False | False | s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint |
| NGC4088 | F2_DIMENSIONFUL_CARRIER_CANDIDATE_AVAILABLE | PASS | x_w * Vflat^2 is selected by the conditional scale-selection gate | derive the carrier rather than selecting it by protocol | False | False | s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint |
| NGC4088 | F3_FUNCTIONAL_VARIABLE_DECLARED | FORMULA_CONDITIONAL | lambda_w can parameterize the warp/asymmetry delta-v-squared amplitude | derive lambda_w as a Tau-side readout variable | False | False | s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint |
| NGC4088 | F4_CLOSURE_COST_DEFINED | BLOCKED | no explicit Tau-side closure_cost has been constructed | define a residual-blind closure/readout cost from Tau-side morphology and slice mismatch | False | False | s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint |
| NGC4088 | F5_EULER_CONDITION_DERIVED | BLOCKED | no stationarity equation currently yields lambda_w = x_w * Vflat^2 | derive dJ_tau/dlambda_w = 0 and solve it without endpoint residuals | False | False | s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint |
| NGC4088 | F6_ASYMPTOTIC_CARRIER_TERM_DERIVED | BLOCKED | ASYMPTOTIC_CARRIER_DOMINANCE_NOT_DERIVED | derive why the asymptotic term is Vflat^2 rather than another source-native carrier | False | False | s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint |
| NGC4088 | F7_COMPARATOR_AUTONOMY_DERIVED | FORMULA_CONDITIONAL | selection protocol excludes external TPG-like comparators | derive comparator autonomy as a functional constraint | False | False | s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint |
| NGC4088 | F8_POPULATION_TRANSFER_REQUIRED | BLOCKED | DERIVATION_BLOCKED_SELECTION_RULE_AUDITED | apply the same functional requirement gate to a predeclared warp/asymmetry sample | False | False | s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint |

## Summary

| galaxy | functional_id | n_gates | n_pass | n_formula_conditional | n_blocked | functional_status | law_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_WARP_ASYMMETRY_CLOSURE_FUNCTIONAL_REQUIREMENT | 8 | 2 | 2 | 4 | CLOSURE_FUNCTIONAL_REQUIREMENT_SPECIFIED_NOT_DERIVED | NO_TAU_SIDE_EULER_CLOSURE_DERIVATION_YET | False | False | s4g75_ngc4088_closure_functional_requirement_gate_not_endpoint |

## Claim Boundary

This is a derivation-requirement ledger, not a derivation. It preserves
the negative result that no Tau-side closure functional currently
generates the selected scale law.
