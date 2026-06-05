# NGC4088 Target-Functional Origin Gate

This gate decomposes the minimal Euler target into source factors and
records which parts are source grounded versus still ansatz-level.

## Verdict

The source factors are available and dimensionally consistent. The
multiplicative coupling and quadratic penalty are not yet Tau-side
derived, so the target functional remains conditional.

## Target Factors

| galaxy | factor_id | factor_symbol | factor_value | unit | origin_status | origin_evidence | remaining_obligation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | SIGMA_WARP_ORIENTATION | sigma_warp | 1 | dimensionless | THEORY_CONDITIONAL_ORIENTATION_SIGN | positive warp/asymmetry orientation lane | derive orientation sign from Tau-side readout geometry | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | Q_WARP_SOURCE_STRENGTH | q_warp | 1 | dimensionless | SOURCE_NATIVE_QUALITATIVE_GATE | qualitative warp/asymmetry source strength imported before endpoint scoring | replace qualitative q_warp=1 by source-measured amplitude in population tests | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | X_WARP_ONSET | x_w | 0.282353 | dimensionless | SOURCE_MEASURED_ONSET_FRACTION | x_w = R_warp/R_HI from residual-blind channel-map digitization protocol | independent digitization review and population transfer | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | VFLAT2_CARRIER | Vflat^2 | 29480.9 | km2_s2 | SOURCE_CATALOG_SCALE_CANDIDATE_NOT_DERIVED_CARRIER | catalog flat-speed-squared scale selected by conditional carrier rule | derive asymptotic carrier dominance from Tau-side closure/readout functional | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | MULTIPLICATIVE_COUPLING | sigma_warp * q_warp * x_w * Vflat^2 | 8324.02 | km2_s2 | TARGET_COMPOSITE_FORMULA_CONDITIONAL | composite target is dimensionally valid and Euler-solvable | derive multiplicative coupling rather than composing source factors by ansatz | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | QUADRATIC_TARGET_PENALTY | (lambda_w - target)^2 | 1 | formal | TARGET_PENALTY_NOT_TAU_SIDE_DERIVED | minimal convex penalty yields explicit stationarity | derive penalty form from closure/readout geometry | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | T1_SOURCE_FACTORS_AVAILABLE | PASS | sigma_warp, q_warp, x_w, and Vflat^2 are present before endpoint scoring | none at availability level | False | False | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | T2_DIMENSIONAL_PRODUCT_VALID | PASS | sigma_warp q_warp x_w Vflat^2 has km^2/s^2 units | none at dimensional level | False | False | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | T3_ONSET_FACTOR_SOURCE_GROUNDED | FORMULA_CONDITIONAL | x_w is measured by a residual-blind protocol but still needs independent review | complete independent digitization review | False | False | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | T4_ASYMPTOTIC_CARRIER_SOURCE_GROUNDED | FORMULA_CONDITIONAL | Vflat^2 is source/catalog grounded but not derived as a Tau-side carrier | derive asymptotic carrier dominance | False | False | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | T5_MULTIPLICATIVE_COUPLING_DERIVED | BLOCKED | the product form is selected by ansatz, not derived | derive why source strength, onset, orientation, and carrier multiply linearly | False | False | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | T6_QUADRATIC_PENALTY_DERIVED | BLOCKED | the quadratic target penalty is minimal and convex but not Tau-side derived | derive penalty geometry or replace with a derived closure cost | False | False | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |
| NGC4088 | T7_ENDPOINT_BLINDNESS | PASS | no observed velocity or residual score is used in target construction | keep endpoint testing separate | False | False | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |

## Summary

| galaxy | target_lambda_km2_s2 | n_factors | n_gates | n_pass | n_formula_conditional | n_blocked | target_origin_status | law_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 8324.02 | 6 | 7 | 3 | 2 | 2 | SOURCE_FACTORS_AVAILABLE_COUPLING_NOT_DERIVED | TARGET_TERM_NOT_TAU_SIDE_DERIVED | False | False | s4g75_ngc4088_target_functional_origin_gate_not_endpoint |

## Claim Boundary

This is not an endpoint test and not a law derivation. It preserves the
negative result that the target term itself still needs a Tau-side
origin.
