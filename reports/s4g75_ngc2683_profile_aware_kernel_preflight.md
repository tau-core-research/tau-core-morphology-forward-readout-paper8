# NGC2683 Profile-Aware Thick/Flared Kernel Preflight

This diagnostic compares the current scalar h/Rs thick/flared shell with a source-native flare-profile shell for NGC2683. It is not accepted validation.

## Verdict

| galaxy | policy | n_points | n_profile_mapped_points | n_unmapped_points | beta_delta_v2_amplitude | scalar_rmse_K_thick_flared | profile_rmse_K_thick_flared | unclipped_profile_rmse_K_thick_flared | profile_minus_scalar_rmse | unclipped_profile_minus_scalar_rmse | n_profile_points_exceeding_current_clip | scalar_rmse_tpg_v6 | scalar_rmse_mond | accepted_endpoint_ready | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC2683 | mapped_only_source_profile_policy | 7 | 7 | 0 | -522.962 | 9.10068 | 9.10075 | 9.10522 | 6.86666e-05 | 0.00454151 | 3 | 8.97368 | 8.87682 | False | False | True | s4g75_ngc2683_profile_aware_kernel_preflight_not_validation |
| NGC2683 | hybrid_profile_mapped_scalar_unmapped_policy | 11 | 7 | 4 | -522.962 | 10.3319 | 10.3319 | 10.3344 | 3.84899e-05 | 0.00254598 | 3 | 10.3148 | 14.151 | False | False | True | s4g75_ngc2683_profile_aware_kernel_preflight_not_validation |

A positive profile-minus-scalar RMSE means the current naive profile insertion worsens the stress score. That is a useful failure signal: the direct flare profile should feed a profile-aware readout kernel, not simply a pointwise scalar substitution.

## Point-Level Comparison

| r | mapping_status | scalar_h_over_rs | profile_policy_h_over_rs | profile_effective_h_over_rs_clipped | profile_h_over_rs_exceeds_current_clip | scalar_kernel_K_thick_flared | profile_kernel_K_thick_flared | unclipped_profile_kernel_K_thick_flared | scalar_v_K_thick_flared | profile_v_K_thick_flared | unclipped_profile_v_K_thick_flared | profile_minus_scalar_v | unclipped_profile_minus_scalar_v |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.89 | PROFILE_MAPPED | 0.202408 | 0.226281 | 0.226281 | False | 0.303817 | 0.297664 | 0.297664 | 182.137 | 182.146 | 182.146 | 0.00883277 | 0.00883277 |
| 5.77 | PROFILE_MAPPED | 0.202408 | 0.226281 | 0.226281 | False | 0.376618 | 0.372243 | 0.372243 | 205.089 | 205.095 | 205.095 | 0.00557712 | 0.00557712 |
| 8.66 | PROFILE_MAPPED | 0.202408 | 0.226281 | 0.226281 | False | 0.316098 | 0.313964 | 0.313964 | 195.226 | 195.229 | 195.229 | 0.00285766 | 0.00285766 |
| 11.54 | PROFILE_MAPPED | 0.202408 | 0.545702 | 0.545702 | False | 0.245003 | 0.23085 | 0.23085 | 196.379 | 196.398 | 196.398 | 0.0188439 | 0.0188439 |
| 14.43 | PROFILE_MAPPED | 0.202408 | 1.48574 | 0.75 | True | 0.191315 | 0.180099 | 0.163097 | 187.161 | 187.176 | 187.2 | 0.0156686 | 0.0394187 |
| 17.31 | PROFILE_MAPPED | 0.202408 | 1.81024 | 0.75 | True | 0.154576 | 0.14879 | 0.133644 | 181.538 | 181.546 | 181.568 | 0.00833336 | 0.030147 |
| 20.2 | PROFILE_MAPPED | 0.202408 | 1.81024 | 0.75 | True | 0.12917 | 0.125954 | 0.116037 | 176.365 | 176.37 | 176.385 | 0.00476796 | 0.0194694 |
| 23.08 | MAPPING_REQUIRED_AFTER_22_KPC | 0.202408 | 0.202408 | 0.202408 | False | 0.111082 | 0.111082 | 0.111082 | 171.631 | 171.631 | 171.631 | 0 | 0 |
| 28.85 | MAPPING_REQUIRED_AFTER_22_KPC | 0.202408 | 0.202408 | 0.202408 | False | 0.0870973 | 0.0870973 | 0.0870973 | 164.547 | 164.547 | 164.547 | 0 | 0 |
| 31.74 | MAPPING_REQUIRED_AFTER_22_KPC | 0.202408 | 0.202408 | 0.202408 | False | 0.0787104 | 0.0787104 | 0.0787104 | 161.583 | 161.583 | 161.583 | 0 | 0 |
| 34.62 | MAPPING_REQUIRED_AFTER_22_KPC | 0.202408 | 0.202408 | 0.202408 | False | 0.0718578 | 0.0718578 | 0.0718578 | 158.91 | 158.91 | 158.91 | 0 | 0 |

## Claim Boundary

This preflight computes stress RMSEs for kernel development only. It does not create an accepted endpoint row and does not resolve the post-22 kpc source-profile ambiguity.
