# NGC4088 Kernel-to-Velocity Normalization Candidate

This report is the first NGC4088-specific candidate bridge from the
filled closure-source basis to a delta-v-squared readout scale. It is not
an endpoint score, fit, or validation result.

## Verdict

NGC4088 now has a theory-conditional kernel-to-velocity normalization
candidate built on the filled source-side onset control. The remaining
open issue is whether this normalization law is the right physical
readout law, not whether a residual-blind onset exists.

## Constants

| galaxy | constant_name | constant_value | unit | role | proof_status | rationale | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | sigma_warp_orientation | 1 | dimensionless | positive closure-source orientation | THEORY_CONDITIONAL | warp/asymmetry closure-source lane is treated as a positive outer residual readout channel | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | q_warp | 1 | dimensionless | source-side warp strength | SOURCE_NATIVE_QUALITATIVE_GATE | qualitative source strength imported from the NGC4088 warp/asymmetry extraction gate | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | c_warp_candidate | 0.282353 | dimensionless | source-normalization candidate | XW_FILLED_SOURCE_FRACTION | first compact normalization candidate uses the filled x_w fraction as a residual-blind onset/closure scale | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | velocity_scale_candidate | 29480.9 | km2_s2 | dimensionful delta-v-squared scale | SOURCE_CATALOG_SCALE_CANDIDATE | uses catalog flat-speed squared as a simple source-side scale carrier for candidate normalization only | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | onset_over_rdisk | 2.43534 | dimensionless | secondary scale check | DERIVED_FROM_FILLED_ONSET | tracks whether the filled onset sits in the outer disk relative to SPARC Rdisk | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |

## Candidate Profile

| galaxy | x_R_over_RHI | radius_kpc_candidate | filled_x_warp_onset | x_warp_uncertainty | turn_on_power_control | filled_basis_value | normalization_prefactor_km2_s2 | delta_v2_warp_candidate | normalization_status | accepted_for_endpoint | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 0 | 0 | 0.282353 | 0.0705882 | 1 | 0 | 8324.02 | 0 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.1 | 2.2253 | 0.282353 | 0.0705882 | 1 | 0 | 8324.02 | 0 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.2 | 4.45059 | 0.282353 | 0.0705882 | 1 | 0 | 8324.02 | 0 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.282353 | 6.28319 | 0.282353 | 0.0705882 | 1 | 0 | 8324.02 | 0 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.4 | 8.90118 | 0.282353 | 0.0705882 | 1 | 0.163934 | 8324.02 | 1364.59 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.6 | 13.3518 | 0.282353 | 0.0705882 | 1 | 0.442623 | 8324.02 | 3684.4 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.8 | 17.8024 | 0.282353 | 0.0705882 | 1 | 0.721311 | 8324.02 | 6004.21 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 1 | 22.253 | 0.282353 | 0.0705882 | 1 | 1 | 8324.02 | 8324.02 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0 | 0 | 0.282353 | 0.0705882 | 2 | 0 | 8324.02 | 0 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.1 | 2.2253 | 0.282353 | 0.0705882 | 2 | 0 | 8324.02 | 0 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.2 | 4.45059 | 0.282353 | 0.0705882 | 2 | 0 | 8324.02 | 0 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.282353 | 6.28319 | 0.282353 | 0.0705882 | 2 | 0 | 8324.02 | 0 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.4 | 8.90118 | 0.282353 | 0.0705882 | 2 | 0.0268745 | 8324.02 | 223.704 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.6 | 13.3518 | 0.282353 | 0.0705882 | 2 | 0.195915 | 8324.02 | 1630.8 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 0.8 | 17.8024 | 0.282353 | 0.0705882 | 2 | 0.52029 | 8324.02 | 4330.9 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 1 | 22.253 | 0.282353 | 0.0705882 | 2 | 1 | 8324.02 | 8324.02 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |

## Summary

| galaxy | turn_on_power_control | n_profile_rows | filled_x_warp_onset | r_hi_kpc | vflat_km_s | max_delta_v2_candidate | median_delta_v2_candidate | normalization_status | accepted_for_endpoint | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 1 | 8 | 0.282353 | 22.253 | 171.7 | 8324.02 | 682.296 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |
| NGC4088 | 2 | 8 | 0.282353 | 22.253 | 171.7 | 8324.02 | 111.852 | THEORY_CONDITIONAL_FILLED_SOURCE_RULE | False | s4g75_ngc4088_kernel_to_velocity_normalization_candidate_not_endpoint |

## Claim Boundary

This candidate is dimensionally explicit and source-filled, but it remains
theory-conditional. It does not compare against observed velocity
endpoints and does not authorize matched-family or baseline claims.
