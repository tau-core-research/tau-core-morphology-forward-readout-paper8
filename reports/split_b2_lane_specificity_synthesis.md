# Split-B2 Lane-Specificity Synthesis

Status: `SPLIT_B2_LANE_SPECIFICITY_SYNTHESIS_COMPLETE`

This synthesis preserves both the NGC7331 split-B2 diagnostic improvement and
the NGC5907 split-B2 negative holdout. It does not tune a formula and it does
not claim population validation.

## Summary

| synthesis_status | universal_split_b2_rule_status | lane_specificity_status | ngc7331_role | ngc5907_role | population_validation_status | formula_tuned | endpoint_scores_allowed | recommended_next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPLIT_B2_LANE_SPECIFICITY_SYNTHESIS_COMPLETE | REJECTED_BY_CURRENT_EVIDENCE | SUPPORTED_PRELIMINARY_NOT_VALIDATED | positive_same_curve_diagnostic | negative_caveated_independent_control | OPEN | False | False | predeclare another added-readout candidate from source fields, or strengthen projection/readout lane taxonomy before more scoring | split_b2_lane_specificity_synthesis_not_population_validation |

## Cases

| galaxy | case_role | readout_lane_under_test | status | primary_metric | split_b2_rmse_km_s | comparison_model | comparison_rmse_km_s | delta_vs_comparison_km_s | interpretation | endpoint_evidence_strength | formula_tuned_in_synthesis | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | diagnostic_origin_same_curve | split_B2_added_warp_history | POSITIVE_DIAGNOSTIC_NOT_ENDPOINT | RMSE | 21.7334 | EXPONENTIAL_DISK_CARRIER | 23.473 | -1.73956 | split-B2 unit-load repairs the failed exact-transfer q-role diagnostic on the same galaxy; useful but not independent | DIAGNOSTIC_ONLY | False | split_b2_lane_specificity_synthesis_not_population_validation |
| NGC5907 | independent_caveated_holdout | split_B2_added_warp_history | NEGATIVE_HOLDOUT_PRELIMINARY_CONTROL | RMSE | 62.0882 | TAU_NGC5907_PROJECTION_ACCEPTED | 15.4952 | 46.593 | negative holdout: split-B2 added-readout does not transfer to NGC5907; projection/TPG-like lane remains favored | CAVEATED_NEGATIVE_CONTROL | False | split_b2_lane_specificity_synthesis_not_population_validation |

## Gates

| gate_id | gate_status | evidence | consequence | claim_boundary |
| --- | --- | --- | --- | --- |
| SB2LS_G1_PRESERVE_NGC7331_DIAGNOSTIC | PASS | NGC7331 split-B2 repair improves the failed same-curve exact-transfer diagnostic | keep as q-role/source-load diagnostic, not validation | split_b2_lane_specificity_synthesis_not_population_validation |
| SB2LS_G2_PRESERVE_NGC5907_NEGATIVE | PASS | NGC5907 split-B2 holdout RMSE is much worse than projection/TPG-like context | do not universalize split-B2 added-readout | split_b2_lane_specificity_synthesis_not_population_validation |
| SB2LS_G3_UNIVERSAL_SPLIT_B2_RULE | REJECTED_BY_CURRENT_EVIDENCE | positive same-curve diagnostic plus negative independent holdout | split-B2 is not a universal morphology readout formula | split_b2_lane_specificity_synthesis_not_population_validation |
| SB2LS_G4_LANE_SPECIFICITY | SUPPORTED_PRELIMINARY | projection-dominated NGC5907 rejects added split-B2 but accepts projection/TPG-like readout | readout-lane selection is physically/scientifically central, not cosmetic | split_b2_lane_specificity_synthesis_not_population_validation |
| SB2LS_G5_POPULATION_VALIDATION | OPEN | only one diagnostic origin and one caveated negative holdout | requires more predeclared galaxies before population claim | split_b2_lane_specificity_synthesis_not_population_validation |

## Next Cases

| galaxy | split_b2_holdout_status | sparc_status | split_b2_blockers | recommended_next_action | recommended_lane_after_synthesis | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | P0_PREDECLARED_SPLIT_B2_HOLDOUT_CANDIDATE_RHI_BLOCKED_OR_CAVEATED | SPARC_RHI_MISSING_OR_ZERO | sparc_rhi_missing_or_zero | build NGC5907 split-B2 denominator gate; if source-native denominator passes, freeze split-B2 formula before any scoring | projection lane remains accepted; split-B2 lane negative control | split_b2_lane_specificity_synthesis_not_population_validation |
| NGC4013 | P1_RETROSPECTIVE_ANALOGUE_HAS_RHI_NOT_CLEAN_HOLDOUT | SPARC_VFLAT_RHI_READY | retrospective_or_reference_case;exact_b2_fields_incomplete | use as secondary analogue after a fresh residual-blind source freeze | secondary analogue only after fresh source freeze | split_b2_lane_specificity_synthesis_not_population_validation |
| NGC4183 | P1_SOURCE_ACQUISITION_REQUIRED_HAS_SPARC_RHI_VFLAT | SPARC_VFLAT_RHI_READY | source_acquisition_required;numeric_warp_activation_missing | acquire source-native warp/history observables before formula freeze | source acquisition before any split-B2 scoring | split_b2_lane_specificity_synthesis_not_population_validation |

## Interpretation

The evidence now argues against treating split-B2 as a universal Tau Core
readout formula. NGC7331 remains useful because it exposed and repaired a
q-role/source-load issue. NGC5907 is useful in the opposite direction: it
rejects the added split-B2 lane while projection/TPG-like readouts remain
strong.

This is a good scientific outcome for the bridge because it supports the
central Paper 8 idea: morphology/readout lane selection matters. The right
question is not whether one Tau formula fits all galaxies, but whether the
source-selected readout lane explains which baseline-like behavior should be
strong.

## Claim Boundary

`split_b2_lane_specificity_synthesis_not_population_validation`
