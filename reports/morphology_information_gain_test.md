# Morphology Information Gain Test

This report assembles existing residual-blind Paper 8 endpoint layers into
a first information-gain diagnostic. It does not fit a new morphology
model and it is not an empirical validation claim.

## Information Levels

| information_level | level_name | input_layer | required_data | current_status | main_output | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | coarse_K_obs_formula_shell_proxy | coarse residual-blind metadata family label | SPARC metadata and available proxy morphology bins | RUNNABLE_PROXY | morphology_formula_shell_proxy_scores_by_galaxy.csv | coarse_proxy_not_final_readout_state |
| L1 | source_reviewed_K_readout_source_native_formulas | source-native bridge kernels with proxy morphology parameters | SPARC radii plus proxy scale/tail/core/thickness parameters | RUNNABLE_PROXY_STRONG_SPECIFICITY | source_native_readout_formula_scores_by_galaxy.csv | source_native_formula_shells_not_accepted_full_morphology |
| L2 | readout_state_vector_proxy | low-dimensional readout-state vector weights | accepted tail, compact, thickness, bar, memory, and regularity observables | RUNNABLE_PROXY_NEGATIVE_CURRENTLY | readout_mixture_proxy_scores_by_galaxy.csv | mixture_weights_proxy_only_not_endpoint |
| L3 | source_native_scales_with_train_selected_normalization | source-native kernels plus train-selected normalization policy | accepted scale/amplitude normalizers and residual-blind closure/readout scale | RUNNABLE_PROXY_NORMALIZATION_GATE | amplitude_shrinkage_path_scores_by_galaxy.csv:shrink_family_weight_0.40 | train_selected_policy_not_tau_side_normalization_law |
| L4 | velocity_field_HI_history_enriched | enriched morphology/kinematic evidence | velocity fields, HI maps, decompositions, history indicators | BLOCKED_DATA_NOT_ASSEMBLED | none | future_endpoint_only |

## Holdout Summary

| information_level | level_name | split | n_galaxies | median_rmse_level_prediction | mean_rmse_level_prediction | matched_beats_wrong_fraction | matched_rank1_fraction | beats_tpg_v6_fraction | beats_mond_fraction | median_minus_wrong | median_minus_tpg_v6 | median_minus_mond | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | coarse_K_obs_formula_shell_proxy | holdout | 44 | 14.0213 | 17.7468 | 0.5 | 0.29545454545454547 | 0.477273 | 0.590909 | -0.0012605214126067028 | 0.136226 | -0.41503 | information_gain_preflight_not_validation |
| L1 | source_reviewed_K_readout_source_native_formulas | holdout | 44 | 15.3531 | 18.938 | 0.8863636363636364 | 0.29545454545454547 | 0.477273 | 0.477273 | -13.974199559618807 | 0.644948 | 0.173401 | information_gain_preflight_not_validation |
| L2 | readout_state_vector_proxy | holdout | 44 | 15.3602 | 20.6973 |  |  | 0.5 | 0.454545 |  | 0.111816 | 0.298487 | information_gain_preflight_not_validation |
| L3 | source_native_scales_with_train_selected_normalization | holdout | 44 | 13.2154 | 17.9593 | 0.8181818181818182 | 0.2727272727272727 | 0.477273 | 0.613636 | -5.470945659132824 | 0.124458 | -0.950214 | information_gain_preflight_not_validation |

## Holdout Transition Diagnostics

| split | transition | n_common_galaxies | improvement_fraction | median_delta_rmse_curr_minus_prev | mean_delta_rmse_curr_minus_prev | interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | L0_to_L1 | 44 | 0.431818 | 0.575081 | 1.19116 | L0->L1_negative_or_overfit_proxy_warning | transition_diagnostic_not_monotonicity_proof |
| holdout | L1_to_L2 | 44 | 0.454545 | 0.445057 | 1.75933 | L1->L2_mixed_information_gain_signal | transition_diagnostic_not_monotonicity_proof |
| holdout | L2_to_L3 | 44 | 0.636364 | -0.602864 | -2.73804 | L2->L3_supports_information_gain | transition_diagnostic_not_monotonicity_proof |

## Data Acquisition Status

| source_family | local_artifact | available_count | status | notes | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| SPARC | external_sparc_master_table.csv | 175 | ACQUIRED_FULL_175 | residual-blind source layer; not a rotation endpoint score | source_availability_not_endpoint_validation |
| S4G | external_s4g_sparc_observable_candidates.csv | 75 | PARTIAL_SCALE_RADIUS_CANDIDATES | residual-blind source layer; not a rotation endpoint score | source_availability_not_endpoint_validation |
| DustPedia | morphology_information_gain_source_expansion.csv | 31 | FULL_SAMPLE_SOURCE_CANDIDATES | residual-blind source layer; not a rotation endpoint score | source_availability_not_endpoint_validation |
| HI_surveys | morphology_information_gain_source_expansion.csv | 171 | FULL_SAMPLE_SPARC_HI_READY | residual-blind source layer; not a rotation endpoint score | source_availability_not_endpoint_validation |
| PHANGS | morphology_information_gain_source_expansion.csv | 2 | FULL_SAMPLE_PUBLIC_SAMPLE_MATCHES | residual-blind source layer; not a rotation endpoint score | source_availability_not_endpoint_validation |
| L2_tail_candidates | morphology_information_gain_source_expansion.csv | 172 | SOURCE_CANDIDATE_NOT_ACCEPTED_WEIGHT | residual-blind source layer; not a rotation endpoint score | source_availability_not_endpoint_validation |
| L2_compact_candidates | morphology_information_gain_source_expansion.csv | 48 | SOURCE_CANDIDATE_NOT_ACCEPTED_WEIGHT | residual-blind source layer; not a rotation endpoint score | source_availability_not_endpoint_validation |
| L2_bar_candidates | morphology_information_gain_source_expansion.csv | 19 | SOURCE_CANDIDATE_NOT_ACCEPTED_WEIGHT | residual-blind source layer; not a rotation endpoint score | source_availability_not_endpoint_validation |
| L4_velocity_field_candidates | morphology_information_gain_source_expansion.csv | 0 | BLOCKED_NO_MUSE_READY_MATCHES | residual-blind source layer; not a rotation endpoint score | source_availability_not_endpoint_validation |
| readout_state_vector_components | readout_state_vector_gap_audit.csv | 0 | ENDPOINT_READY_COMPONENTS_MISSING | 422 proxy-only components; accepted L2 weights still blocked | source_availability_not_endpoint_validation |

## Current Verdict

The available layers show a strong L0->L1 specificity gain when moving from
naive formula shells to source-native bridge kernels. The current L2
mixture/readout-state proxy is not yet an improvement, which supports the
data-gate interpretation: mixture weights require accepted morphology-memory
and source-native observables rather than coarse present-day proxies.

## Claim Boundary

This is a morphology-information-gain preflight. It is useful only if all
information levels remain residual-blind. Any improvement caused by choosing
labels, scales, weights, or gates from rotation residuals is forbidden.
