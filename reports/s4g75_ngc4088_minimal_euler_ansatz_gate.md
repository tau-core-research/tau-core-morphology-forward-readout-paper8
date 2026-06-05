# NGC4088 Minimal Euler-Ansatz Gate

This gate performs the first explicit stationarity calculation for the
NGC4088 warp/asymmetry normalization. It is conditional on a quadratic
target functional and does not prove the Tau-side origin of that target.

## Verdict

Given the minimal quadratic target ansatz, the Euler condition gives
`lambda_w = sigma_warp q_warp x_w Vflat^2`. The algebra is explicit and
dimensionally consistent. The target functional itself remains blocked
as a Tau-side derivation.

## Ansatz

| galaxy | ansatz_id | functional_ansatz | stationarity_equation | solved_lambda_km2_s2 | solved_lambda_formula | proof_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | MINIMAL_QUADRATIC_TARGET_EULER_ANSATZ | J_min(lambda_w) = 1/2 kappa_lambda (lambda_w - sigma_warp q_warp x_w Vflat^2)^2 | dJ_min/dlambda_w = kappa_lambda (lambda_w - sigma_warp q_warp x_w Vflat^2) = 0 | 8324.02 | lambda_w = sigma_warp q_warp x_w Vflat^2 | EULER_SOLVES_TARGET_GIVEN_ANSATZ | s4g75_ngc4088_minimal_euler_ansatz_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | E1_DIMENSIONAL_TARGET_VALID | PASS | lambda_w and sigma q x_w Vflat^2 both carry km^2/s^2 | none at dimensional level | False | False | s4g75_ngc4088_minimal_euler_ansatz_gate_not_endpoint |
| NGC4088 | E2_STATIONARITY_ALGEBRA | PASS | dJ/dlambda_w=0 gives lambda_w=sigma q x_w Vflat^2 for kappa_lambda != 0 | none for the conditional ansatz algebra | False | False | s4g75_ngc4088_minimal_euler_ansatz_gate_not_endpoint |
| NGC4088 | E3_CONVEXITY | FORMULA_CONDITIONAL | kappa_lambda > 0 would make the target stationary point a minimum | derive positive kappa_lambda from Tau-side closure geometry | False | False | s4g75_ngc4088_minimal_euler_ansatz_gate_not_endpoint |
| NGC4088 | E4_TARGET_TERM_TAU_ORIGIN | BLOCKED | the quadratic target is chosen to encode the selected scale | derive the target term from Tau-side morphology/readout, not by reverse engineering | False | False | s4g75_ngc4088_minimal_euler_ansatz_gate_not_endpoint |
| NGC4088 | E5_WEIGHT_OR_STIFFNESS_DERIVATION | BLOCKED | kappa_lambda is not derived | derive or eliminate the closure stiffness without endpoint residuals | False | False | s4g75_ngc4088_minimal_euler_ansatz_gate_not_endpoint |
| NGC4088 | E6_NONTRIVIAL_SOURCE_COUPLING | FORMULA_CONDITIONAL | x_w and q_warp enter the target as source-side factors | derive why they enter multiplicatively and linearly | False | False | s4g75_ngc4088_minimal_euler_ansatz_gate_not_endpoint |
| NGC4088 | E7_ENDPOINT_BLINDNESS | PASS | the ansatz uses constants generated before endpoint scoring | keep endpoint evaluation separate | False | False | s4g75_ngc4088_minimal_euler_ansatz_gate_not_endpoint |

## Summary

| galaxy | ansatz_id | solved_lambda_km2_s2 | n_gates | n_pass | n_formula_conditional | n_blocked | euler_status | law_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | MINIMAL_QUADRATIC_TARGET_EULER_ANSATZ | 8324.02 | 7 | 3 | 2 | 2 | EULER_CONDITION_SOLVED_GIVEN_TARGET_ANSATZ | TARGET_FUNCTIONAL_NOT_TAU_SIDE_DERIVED | False | False | s4g75_ngc4088_minimal_euler_ansatz_gate_not_endpoint |

## Claim Boundary

This is a conditional Euler calculation, not a final physical law. It
does not use endpoint velocities or residuals.
