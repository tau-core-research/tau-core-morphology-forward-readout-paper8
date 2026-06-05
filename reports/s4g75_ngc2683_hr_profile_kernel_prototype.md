# NGC2683 H(R)-Aware Thick/Flared Kernel Prototype

This diagnostic replaces local scalar thickness with a residual-blind nonlocal radial flare-profile operator. It is not accepted validation.

## Prototype Rule

For each radius R, the effective h/Rs is computed as a source-weighted local average of H(R') over the NGC2683 flare profile, with locality width fixed to the S4G/SPARC disk scale. Two post-22 kpc closure policies bracket the source ambiguity.

## Verdict

| galaxy | post22_policy | n_points | locality_width_kpc | beta_delta_v2_amplitude | scalar_rmse_K_thick_flared | hr_profile_rmse_K_thick_flared | hr_profile_minus_scalar_rmse | rmse_tpg_v6 | rmse_mond | h_over_rs_min | h_over_rs_median | h_over_rs_max | accepted_endpoint_ready | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC2683 | post22_hold_plateau_upper | 11 | 2.20965 | -522.962 | 10.3319 | 10.3357 | 0.00380286 | 10.3148 | 14.151 | 0.226287 | 1.46227 | 1.81024 | False | False | True | s4g75_ngc2683_hr_profile_kernel_prototype_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | 11 | 2.20965 | -522.962 | 10.3319 | 10.3349 | 0.00302911 | 10.3148 | 14.151 | 0.226287 | 0.830768 | 1.76375 | False | False | True | s4g75_ngc2683_hr_profile_kernel_prototype_not_validation |

## Point-Level Comparison

| post22_policy | r | scalar_h_over_rs | hr_profile_effective_h_over_rs | scalar_kernel_K_thick_flared | hr_profile_kernel_K_thick_flared | scalar_v_K_thick_flared | hr_profile_v_K_thick_flared | hr_profile_minus_scalar_v |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| post22_hold_plateau_upper | 2.89 | 0.202408 | 0.226287 | 0.303817 | 0.297663 | 182.137 | 182.146 | 0.00883518 |
| post22_hold_plateau_upper | 5.77 | 0.202408 | 0.226815 | 0.376618 | 0.372147 | 205.089 | 205.095 | 0.00570068 |
| post22_hold_plateau_upper | 8.66 | 0.202408 | 0.241921 | 0.316098 | 0.312569 | 195.226 | 195.231 | 0.00472624 |
| post22_hold_plateau_upper | 11.54 | 0.202408 | 0.375737 | 0.245003 | 0.238012 | 196.379 | 196.389 | 0.00930907 |
| post22_hold_plateau_upper | 14.43 | 0.202408 | 0.830768 | 0.191315 | 0.178237 | 187.161 | 187.179 | 0.0182702 |
| post22_hold_plateau_upper | 17.31 | 0.202408 | 1.46227 | 0.154576 | 0.138709 | 181.538 | 181.561 | 0.0228529 |
| post22_hold_plateau_upper | 20.2 | 0.202408 | 1.76756 | 0.12917 | 0.116465 | 176.365 | 176.384 | 0.0188344 |
| post22_hold_plateau_upper | 23.08 | 0.202408 | 1.80886 | 0.111082 | 0.102326 | 171.631 | 171.644 | 0.0133389 |
| post22_hold_plateau_upper | 28.85 | 0.202408 | 1.81024 | 0.0870973 | 0.0825585 | 164.547 | 164.554 | 0.00721245 |
| post22_hold_plateau_upper | 31.74 | 0.202408 | 1.81024 | 0.0787104 | 0.0752467 | 161.583 | 161.588 | 0.00560497 |
| post22_hold_plateau_upper | 34.62 | 0.202408 | 1.81024 | 0.0718578 | 0.0691279 | 158.91 | 158.915 | 0.00449188 |
| post22_linear_taper_to_inner_height | 2.89 | 0.202408 | 0.226287 | 0.303817 | 0.297663 | 182.137 | 182.146 | 0.00883518 |
| post22_linear_taper_to_inner_height | 5.77 | 0.202408 | 0.226815 | 0.376618 | 0.372147 | 205.089 | 205.095 | 0.00570068 |
| post22_linear_taper_to_inner_height | 8.66 | 0.202408 | 0.241921 | 0.316098 | 0.312569 | 195.226 | 195.231 | 0.00472624 |
| post22_linear_taper_to_inner_height | 11.54 | 0.202408 | 0.375737 | 0.245003 | 0.238012 | 196.379 | 196.389 | 0.00930907 |
| post22_linear_taper_to_inner_height | 14.43 | 0.202408 | 0.830768 | 0.191315 | 0.178237 | 187.161 | 187.179 | 0.0182702 |
| post22_linear_taper_to_inner_height | 17.31 | 0.202408 | 1.4622 | 0.154576 | 0.13871 | 181.538 | 181.561 | 0.0228515 |
| post22_linear_taper_to_inner_height | 20.2 | 0.202408 | 1.76375 | 0.12917 | 0.116504 | 176.365 | 176.384 | 0.0187776 |
| post22_linear_taper_to_inner_height | 23.08 | 0.202408 | 1.75496 | 0.111082 | 0.102715 | 171.631 | 171.644 | 0.0127462 |
| post22_linear_taper_to_inner_height | 28.85 | 0.202408 | 1.22619 | 0.0870973 | 0.0847805 | 164.547 | 164.55 | 0.00368156 |
| post22_linear_taper_to_inner_height | 31.74 | 0.202408 | 0.872952 | 0.0787104 | 0.0777965 | 161.583 | 161.584 | 0.00147888 |
| post22_linear_taper_to_inner_height | 34.62 | 0.202408 | 0.583382 | 0.0718578 | 0.0715459 | 158.91 | 158.911 | 0.000513146 |

## Claim Boundary

This is a profile-kernel development diagnostic. The post-22 kpc closure policies are explicit prototype brackets, not source-validated laws, and the stress scores do not authorize endpoint promotion.
