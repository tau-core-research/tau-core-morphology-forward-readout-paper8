# NGC4088 Physical Normalization-Law Gate

This audit separates a formula-consistent NGC4088 warp/asymmetry
normalization candidate from an accepted Tau-side physical readout law.

## Verdict

The candidate is dimensionally consistent and residual-blind, but it is
only formula-conditional. The remaining law-level blockers are the
Tau-side derivation of the scale, scale uniqueness, and population
transfer.

## Candidate Formula

| galaxy | formula_id | candidate_formula | expanded_prefactor | normalization_prefactor_km2_s2 | proof_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088-WARP-DELTA-V2-CANDIDATE-001 | delta_v2_warp(R;p) = sigma_warp q_warp x_w Vflat^2 C_warp(R/R_HI; x_w, p) | sigma_warp=1, q_warp=1, x_w=0.282353, Vflat^2=29480.89 km2_s2 | 8324.02 | FORMULA_CONDITIONAL_NOT_TAU_SIDE_LAW | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | DIMENSIONAL_CONSISTENCY | PASS | candidate maps a dimensionless source basis into delta v^2 units | none at dimensional-audit level | False | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |
| NGC4088 | PREFACTOR_REPRODUCED | PASS | normalization_prefactor = x_w * Vflat^2 for sigma=q=1 | derive why this product is physically selected | False | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |
| NGC4088 | SOURCE_ONSET_SUPPRESSION | PASS | delta v^2 vanishes at and inside the measured source onset | independent onset review remains separate | False | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |
| NGC4088 | POSITIVE_WARP_ORIENTATION | PASS | candidate warp/asymmetry contribution is nonnegative in this orientation | derive orientation sign from Tau-side readout geometry | False | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |
| NGC4088 | RESIDUAL_BLIND_EXPORT | PASS | candidate profile generation uses no observed velocity or endpoint score | keep endpoint scoring in a separate frozen protocol | False | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |
| NGC4088 | FORMULA_LEVEL_CANDIDATE | FORMULA_CONDITIONAL | candidate formula is executable and dimensionally consistent | not yet a Tau-side physical normalization law | False | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |
| NGC4088 | TAU_SIDE_VARIATIONAL_OR_CLOSURE_DERIVATION | BLOCKED | no derivation yet selects x_w Vflat^2 as the unique closure-readout scale | derive from Tau-side closure/readout principle or predeclare as theory axiom | False | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |
| NGC4088 | SCALE_UNIQUENESS | BLOCKED | other residual-blind scales could be considered without overfitting | show this scale beats alternatives by theory criteria before endpoint use | False | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |
| NGC4088 | POPULATION_TRANSFER | BLOCKED | normalization is currently one-galaxy source-filled | repeat on a predeclared warp/asymmetry source-rich sample | False | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |

## Summary

| galaxy | n_gates | n_pass | n_formula_conditional | n_blocked | normalization_prefactor_km2_s2 | law_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 9 | 5 | 1 | 3 | 8324.02 | FORMULA_CONDITIONAL_PHYSICAL_LAW_BLOCKED | False | s4g75_ngc4088_physical_normalization_law_gate_not_endpoint |

## Claim Boundary

This gate does not compare the candidate to observed velocities and does
not authorize endpoint scoring. It only states that the current
NGC4088 normalization is formula-conditional, not a derived final
Tau-side readout law.
