# NGC4088 Tau-Side Scale Derivation Gate

This gate records the missing derivation behind the conditional
`MINIMAL_SOURCE_ONSET_ASYMPTOTIC_CARRIER_RULE`. It is not an endpoint
test and not a proof of a final 4D readout law.

## Verdict

The selected `x_w * Vflat^2` carrier has dimensional support and a
residual-blind onset input, but the Tau-side physical law remains
blocked. The missing pieces are asymptotic carrier dominance, a
closure/readout functional, and population transfer.

## Conditional Skeleton

| galaxy | selected_scale_id | conditional_statement | derived_formula_if_all_gates_pass | current_status | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| NGC4088 | CURRENT_XW_VFLAT2 | If the Tau-side warp/asymmetry closure readout is local at the source onset, asymptotically carried by the catalog flat-speed scale, autonomous from external closure comparators, and minimal in source factors, then the dimensionful carrier reduces to x_w * Vflat^2. | delta_v2_warp(R;p) = sigma_warp q_warp x_w Vflat^2 C_warp(R/R_HI; x_w, p) | DERIVATION_SKELETON_NOT_PROOF | s4g75_ngc4088_tau_side_scale_derivation_gate_not_endpoint |

## Derivation Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | G1_DIMENSIONAL_LIMIT | PASS | x_w and C_warp are dimensionless; Vflat^2 carries km^2/s^2 | none at dimensional level | False | False | s4g75_ngc4088_tau_side_scale_derivation_gate_not_endpoint |
| NGC4088 | G2_SOURCE_ONSET_LOCALITY | FORMULA_CONDITIONAL | x_w is residual-blind and source-measured from the WHISP channel-map protocol | derive why the source onset enters linearly in the Tau-side readout scale | False | False | s4g75_ngc4088_tau_side_scale_derivation_gate_not_endpoint |
| NGC4088 | G3_ASYMPTOTIC_CARRIER_DOMINANCE | BLOCKED | the rule selects Vflat^2, but no Tau-side closure functional yet proves asymptotic carrier dominance | derive Vflat^2 as the asymptotic readout carrier rather than a catalog convenience | False | False | s4g75_ngc4088_tau_side_scale_derivation_gate_not_endpoint |
| NGC4088 | G4_EXTERNAL_COMPARATOR_AUTONOMY | FORMULA_CONDITIONAL | the selection rule rejects v_v6 and other TPG-like comparator normalizers | derive comparator autonomy from Tau-side readout closure, not just by protocol choice | False | False | s4g75_ngc4088_tau_side_scale_derivation_gate_not_endpoint |
| NGC4088 | G5_MINIMAL_SOURCE_FACTOR_RULE | FORMULA_CONDITIONAL | the rule rejects composite x_w * c_g * median(v_n^2)-type carriers | derive minimal single-source-factor preference or state it as a Tau-side axiom | False | False | s4g75_ngc4088_tau_side_scale_derivation_gate_not_endpoint |
| NGC4088 | G6_TAU_SIDE_CLOSURE_FUNCTIONAL | BLOCKED | no variational or closure-readout functional has yet generated the selected carrier | construct the Tau-side closure functional whose solved scale is x_w * Vflat^2 | False | False | s4g75_ngc4088_tau_side_scale_derivation_gate_not_endpoint |
| NGC4088 | G7_POPULATION_TRANSFER | BLOCKED | the gate is currently one-galaxy NGC4088-specific | repeat the same residual-blind derivation gate on a predeclared warp/asymmetry sample | False | False | s4g75_ngc4088_tau_side_scale_derivation_gate_not_endpoint |

## Summary

| galaxy | selected_scale_id | n_gates | n_pass | n_formula_conditional | n_blocked | derivation_status | law_status_after_derivation_gate | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | CURRENT_XW_VFLAT2 | 7 | 1 | 3 | 3 | DERIVATION_BLOCKED_SELECTION_RULE_AUDITED | NOT_DERIVED_TAU_SIDE_LAW | False | False | s4g75_ngc4088_tau_side_scale_derivation_gate_not_endpoint |

## Claim Boundary

This derivation gate preserves the negative result: a conditional
selection rule has been audited, but the Tau-side law has not been
derived. No observed rotation velocities or endpoint residuals are used.
