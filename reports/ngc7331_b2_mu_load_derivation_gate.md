# NGC7331 B2 mu_load conditional derivation gate

This gate does not score an endpoint. It records when the split B2
branch may use `mu_load=1` as a normalized protocol coordinate.

## Summary

| galaxy | mu_load_derivation_status | mu_load_protocol_value | source_scale_xw_vflat2_km2_s2 | derived_split_formula | n_assumptions | n_gates | n_pass | n_formula_conditional | n_open | n_blocked | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | claim_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | SPLIT_B2_UNIT_MU_LOAD_CONDITIONAL_DERIVATION_BUILT_ENDPOINT_BLOCKED | 1 | 30520.3 | Delta v^2=sigma_warp*x_w*Vflat^2*ramp(x;x_w) | 5 | 5 | 2 | 1 | 1 | 1 | False | False | False | mu_load=1 is conditionally derived as a normalized split-load coordinate, not as final Tau-side evidence or endpoint validation | ngc7331_b2_mu_load_derivation_gate_not_endpoint |

## Assumptions

| assumption_id | assumption_text | status | evidence | galaxy | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MU1_SPLIT_ROLE | q_shape is a morphology/kernel observable and is not identified with the source-load amplitude | SUPPORTED_BY_DIAGNOSTIC | NGC7331_B2_Q_ROLE_SEPARATION_DIAGNOSTIC_COMPLETE_NOT_ENDPOINT | NGC7331 | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint |
| MU2_MINIMAL_CARRIER | x_w Vflat^2 is the minimally factorized asymptotic source carrier for the split branch | FORMULA_CONDITIONAL | inherits the NGC4088 B2 asymptotic-carrier premise; not a final Tau-side law | NGC7331 | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint |
| MU3_NO_EXTRA_LOAD_OBSERVABLE | no independent residual-blind load observable is accepted beyond x_w, Vflat, sign, and the radial active window | CONDITIONAL_DEFAULT | current NGC7331 split gate lists candidates, but none is source-frozen as a primary load rule | NGC7331 | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint |
| MU4_NORMALIZED_LOAD_COORDINATE | mu_load is defined as the dimensionless coefficient left after factoring out x_w Vflat^2 | DEFINITION | Delta v^2 = sigma mu_load x_w Vflat^2 K_shape | NGC7331 | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint |
| MU5_ZERO_SOURCE_AND_INACTIVE_LIMITS | inactive window and zero-sign/zero-load limits recover the Newtonian carrier | PASS | ramp=0 for x<=x_w; mu_load=0 or sigma=0 gives Delta v^2=0 | NGC7331 | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint |

## Conditional theorem

| theorem_id | statement | proof_sketch | derived_formula | mathematical_status | tau_side_law_status | dimension_check | known_limits | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary | galaxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPLIT_B2_UNIT_LOAD_CONDITIONAL_THEOREM | Given role separation, minimal carrier factorization, and absence of an accepted independent load observable, the canonical dimensionless split-load coordinate is mu_load=1. | After factoring x_w Vflat^2 from the source-load term, mu_load is dimensionless. If no additional source-load observable is admitted, any non-unit constant is either a new unexplained scale or a fit parameter. The normalized coordinate choice therefore fixes the protocol constant to 1 until a residual-blind source observable replaces it. | Delta v^2_split(R)=sigma_warp x_w Vflat^2 ramp(R/R_HI;x_w) | CONDITIONAL_COORDINATE_NORMALIZATION | NOT_FINAL_LAW_SOURCE_LOAD_ORIGIN_OPEN | PASS: x_w and ramp are dimensionless; Vflat^2 has km^2/s^2 | inactive window recovers carrier; sigma=0 recovers carrier | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint | NGC7331 |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | galaxy | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MULD1_ROLE_SEPARATION | PASS | q_shape/mu_load split gate built | none for diagnostic role separation | NGC7331 | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint |
| MULD2_DIMENSIONLESS_MU | PASS | mu_load is dimensionless after factoring x_w Vflat^2 | none at dimensional level | NGC7331 | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint |
| MULD3_UNIT_LOAD_COORDINATE | FORMULA_CONDITIONAL | unit value follows as normalized coordinate if no extra load observable is admitted | derive Tau-side reason for minimal-load coordinate | NGC7331 | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint |
| MULD4_SOURCE_LOAD_ORIGIN | OPEN | HI support/history/vertical candidates are not source-frozen as mu_load laws | derive or acquire residual-blind mu_load observable | NGC7331 | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint |
| MULD5_ENDPOINT_ELIGIBILITY | BLOCKED | post-failure theory derivation gate only | predeclare and freeze a new split-B2 branch before scoring | NGC7331 | False | False | ngc7331_b2_mu_load_derivation_gate_not_endpoint |

## Verdict

`mu_load=1` is now a formula-conditional normalized split-load rule:
it is allowed only under the minimal-carrier, no-extra-load-observable
premise. It is not yet a final Tau-side law. If a residual-blind
HI-support, history, projection, or vertical-overlay load observable is
accepted later, it must replace or modify the unit-load coordinate before
any future endpoint freeze.
