# NGC4088 Warp-Onset Extraction Protocol

This protocol defines how the missing NGC4088 warp-onset control `x_w = R_warp/R_HI` may be supplied without using rotation residuals.

## Verdict

The mapping shell is ready, but the onset is not. NGC4088 has global HI geometry and qualitative warp/asymmetry evidence, yet no accepted source-native radial onset. The next admissible step is a PA profile, warp-angle profile, or frozen channel-map digitization.

## Accepted Source Classes

| accepted_source_class | source_observable | onset_definition | dimension_check | residual_blind_requirement | endpoint_allowed_after_extraction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| RADIAL_PA_PROFILE | PA(R) from tilted-ring HI model or digitized source-native PA profile | first R where |PA(R)-PA_inner| exceeds predeclared PA threshold for contiguous outer bins | x_w = R_onset_kpc / R_HI_kpc must satisfy 0 < x_w < 1 | PA profile and threshold are selected without Vobs residuals | False | s4g75_ngc4088_warp_onset_extraction_protocol_not_endpoint |
| RADIAL_WARP_ANGLE_PROFILE | theta_warp(R) or inclination/line-of-nodes warp profile from HI model | first R where theta_warp(R) exceeds predeclared angle threshold for contiguous outer bins | x_w = R_onset_kpc / R_HI_kpc must satisfy 0 < x_w < 1 | warp profile and threshold are selected without Vobs residuals | False | s4g75_ngc4088_warp_onset_extraction_protocol_not_endpoint |
| CHANNEL_MAP_DIGITIZATION | digitized channel-map ridge or major-axis bend from source figure | first R where outer ridge departs from inner disk PA beyond predeclared angular tolerance | requires angular-to-kpc conversion using source distance; then 0 < x_w < 1 | digitization protocol, tolerance, and side-combination rule are frozen before scoring | False | s4g75_ngc4088_warp_onset_extraction_protocol_not_endpoint |
| TEXT_ONLY_QUALITATIVE_WARP | text says warp/asymmetry is present but gives no radial onset | not accepted for x_w | insufficient dimensional information | may support development lane only | False | s4g75_ngc4088_warp_onset_extraction_protocol_not_endpoint |

## Current NGC4088 Status

| galaxy | R_HI_kpc_for_normalization | current_best_source_class | current_source_status | x_warp_onset_available | x_warp_onset_value | acceptable_next_routes | blocked_reason | closure_mapping_status | uses_vobs_or_residual | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 22.253 | TEXT_ONLY_QUALITATIVE_WARP_PLUS_GLOBAL_HI_GEOMETRY | WARP_PRESENT_ONSET_NOT_EXTRACTED | False |  | RADIAL_PA_PROFILE;RADIAL_WARP_ANGLE_PROFILE;CHANNEL_MAP_DIGITIZATION | no source-native radial onset or PA/theta profile has been extracted | MAPPING_RULE_DEFINED_ONSET_BLOCKED | False | False | False | s4g75_ngc4088_warp_onset_extraction_protocol_not_endpoint |

## Summary

| galaxy | n_accepted_source_classes | x_warp_onset_available | R_HI_kpc_for_normalization | protocol_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 3 | False | 22.253 | RESIDUAL_BLIND_EXTRACTION_PROTOCOL_READY_ONSET_MISSING | False | s4g75_ngc4088_warp_onset_extraction_protocol_not_endpoint |

## Claim Boundary

A text-only warp statement is not enough to compute `x_w`. Even after `x_w` is extracted, endpoint scoring remains blocked until amplitude normalization and the 4D readout map are fixed residual-blind.
