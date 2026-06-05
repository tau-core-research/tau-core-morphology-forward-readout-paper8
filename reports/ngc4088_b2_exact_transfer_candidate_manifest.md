# NGC4088 B2 Exact Transfer Candidate Manifest

This manifest defines what would count as an exact transfer of the
NGC4088 B2 source-load law. It does not score curves and does not use
endpoint residuals.

## Candidates

| galaxy | preflight_population_transfer_status | candidate_status | accepted_exact_field_count | required_exact_field_count | x_w_status | q_warp_status | sigma_warp_status | vflat_status | epsilon_cross_inputs_status | source_summary | next_action | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | REFERENCE_SINGLE_GALAXY_CONDITIONAL_THEOREM | REFERENCE_EXACT_PROTOCOL_NOT_INDEPENDENT_TRANSFER | 5 | 5 | SOURCE_FROZEN_CAVEATED_ACCEPTED | PROTOCOL_ACCEPTED_Q_MEMORY_REVIEW | PROTOCOL_FROZEN_POSITIVE_SIGN | SOURCE_CATALOG_AVAILABLE | PARTIAL_NUMERIC_BOUND_AVAILABLE_NOT_FULLY_CLOSED | x_w=0.2983326403051493; q=1.0; sigma=1.0; Vflat=171.7 | use as reference; acquire independent exact transfer galaxies rather than counting this row as population transfer | False | False | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |
| NGC4013 | PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER | ANALOGUE_WITH_ONSET_CONTEXT_NOT_EXACT_TRANSFER | 1 | 5 | OVERLAY_OR_WARP_ACTIVATION_AVAILABLE_NOT_EXACT_XW | MISSING_EXACT_Q_WARP_REVIEW | OVERLAY_CONTEXT_AVAILABLE_NOT_EXACT_SIGN_RULE | SOURCE_CATALOG_AVAILABLE | MISSING_EXACT_CROSS_TERM_OBSERVABLES | final_hi_scaleheight_central;line_of_sight_warp_onset;rotational_lag_profile | acquire exact warp/history x_w, q_warp, sigma_warp, and cross-term observables from source-native H I/velocity-field morphology | False | False | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |
| NGC5907 | PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER | ANALOGUE_WITH_ONSET_CONTEXT_NOT_EXACT_TRANSFER | 1 | 5 | OVERLAY_OR_WARP_ACTIVATION_AVAILABLE_NOT_EXACT_XW | MISSING_EXACT_Q_WARP_REVIEW | OVERLAY_CONTEXT_AVAILABLE_NOT_EXACT_SIGN_RULE | SOURCE_CATALOG_AVAILABLE | MISSING_EXACT_CROSS_TERM_OBSERVABLES | disk_truncation_scale_lengths;edge_on_vertical_structure_source;interaction_warp_context;optical_warp_max_displacement;optical_warp_radial_range | acquire exact warp/history x_w, q_warp, sigma_warp, and cross-term observables from source-native H I/velocity-field morphology | False | False | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |
| NGC7331 | CAVEATED_PARTIAL_ANALOGUE_NOT_EXACT_B2_TRANSFER | PARTIAL_EXACT_TRANSFER_CANDIDATE_SOURCE_GAPS | 2 | 5 | FRACTIONAL_OUTER_WARP_ONSET_AVAILABLE_REPLAY_ONLY | MISSING_EXACT_Q_WARP_REVIEW | MISSING_EXACT_SIGN_RULE | SOURCE_CATALOG_AVAILABLE | MISSING_EXACT_CROSS_TERM_OBSERVABLES | fractional_onset=True; approx_x_w=0.5343091911302521 | convert outer-warp replay onset into exact source-load review only if q_warp, sigma_warp, and epsilon_cross fields are source-frozen | False | False | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |
| NGC4183 | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | ACQUISITION_REQUIRED_FOR_EXACT_TRANSFER | 1 | 5 | MISSING_EXACT_XW | MISSING_EXACT_Q_WARP_REVIEW | MISSING_EXACT_SIGN_RULE | SOURCE_CATALOG_AVAILABLE | MISSING_EXACT_CROSS_TERM_OBSERVABLES | nan | acquire exact warp/history x_w, q_warp, sigma_warp, and cross-term observables from source-native H I/velocity-field morphology | False | False | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |

## Requirements

| requirement_id | required_field | definition | accepted_source_status_needed | forbidden_inputs | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| ET1_X_W | x_w | source-native warp/history onset fraction normalized to R_HI or an equivalent frozen source scale | numeric residual-blind onset accepted before scoring | vobs residuals; endpoint score ranks; best-fit readout family; required-S_tau diagnostic | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |
| ET2_Q_WARP | q_warp | source-side warp/history strength or accepted bounded strength proxy | numeric or bounded residual-blind source review | vobs residuals; endpoint score ranks; best-fit readout family; required-S_tau diagnostic | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |
| ET3_SIGMA_WARP | sigma_warp | orientation/sign rule for added-readout or attenuation convention | source-side orientation/readout rule frozen before scoring | vobs residuals; endpoint score ranks; best-fit readout family; required-S_tau diagnostic | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |
| ET4_VFLAT | Vflat | source/catalog asymptotic carrier value | catalog/source value independent of endpoint residuals | vobs residuals; endpoint score ranks; best-fit readout family; required-S_tau diagnostic | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |
| ET5_EPSILON_CROSS_INPUTS | epsilon_cross_inputs | orientation, side-asymmetry, memory/history, and locality inputs needed to bound cross terms | closed or explicitly carried source-side uncertainty interval | vobs residuals; endpoint score ranks; best-fit readout family; required-S_tau diagnostic | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |

## Summary

| exact_transfer_candidate_manifest_status | n_cases | n_reference_rows | n_exact_transfer_ready | n_partial_or_analogue_candidates | n_requirements | endpoint_scores_allowed | uses_vobs_or_residual | population_claim_allowed | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXACT_TRANSFER_CANDIDATE_MANIFEST_BUILT_NO_READY_INDEPENDENT_CASE | 5 | 1 | 0 | 3 | 5 | False | False | False | prioritize NGC7331 for exact-transfer upgrade, then search/acquire additional source-native warp/history cases with all five fields | ngc4088_b2_exact_transfer_candidate_manifest_not_endpoint |

## Interpretation

NGC4088 remains the exact reference case. NGC7331 is the closest current
upgrade target because it has a residual-blind fractional outer-warp
onset, but it still lacks exact q_warp, sigma_warp, and cross-term source
observables. NGC4013, NGC5907, and NGC4183 remain useful analogues or
acquisition targets, not exact B2 transfer cases.
