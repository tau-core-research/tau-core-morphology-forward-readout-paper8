# NGC2683 Flare Closure-Source Kernel Prototype

This diagnostic treats radial flare structure as a separate closure source. It is not accepted validation.

## Prototype Rule

The source profile is the positive radial gradient of log H(R), optionally plus a localized ring-offset source near the saturation/outer-ring region. A nonlocal source-weighted average is evaluated at each rotation radius with locality width fixed to the S4G/SPARC disk scale.

## Verdict

| galaxy | post22_policy | closure_policy | n_points | locality_width_kpc | beta_delta_v2_amplitude | scalar_rmse_K_thick_flared | closure_source_rmse_K_thick_flared | closure_source_minus_scalar_rmse | rmse_tpg_v6 | rmse_mond | closure_kernel_min | closure_kernel_median | closure_kernel_max | accepted_endpoint_ready | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC2683 | post22_hold_plateau_upper | flare_gradient_source | 11 | 2.20965 | -522.962 | 10.3319 | 10.2031 | -0.128714 | 10.3148 | 14.151 | 1.23989e-14 | 0.0105068 | 1.47391 | False | False | True | s4g75_ngc2683_flare_closure_source_prototype_not_validation |
| NGC2683 | post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 11 | 2.20965 | -522.962 | 10.3319 | 10.1787 | -0.153128 | 10.3148 | 14.151 | 4.64623e-05 | 0.0795902 | 1.47401 | False | False | True | s4g75_ngc2683_flare_closure_source_prototype_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | flare_gradient_source | 11 | 2.20965 | -522.962 | 10.3319 | 10.2031 | -0.128714 | 10.3148 | 14.151 | 4.28508e-15 | 0.0105068 | 1.47391 | False | False | True | s4g75_ngc2683_flare_closure_source_prototype_not_validation |
| NGC2683 | post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 11 | 2.20965 | -522.962 | 10.3319 | 10.1787 | -0.153128 | 10.3148 | 14.151 | 4.64623e-05 | 0.0795902 | 1.47401 | False | False | True | s4g75_ngc2683_flare_closure_source_prototype_not_validation |

## Point-Level Comparison

| post22_policy | closure_policy | r | scalar_kernel_K_thick_flared | closure_source_kernel_K_thick_flared | scalar_v_K_thick_flared | closure_source_v_K_thick_flared | closure_minus_scalar_v |
| --- | --- | --- | --- | --- | --- | --- | --- |
| post22_hold_plateau_upper | flare_gradient_source | 2.89 | 0.303817 | 0.000189046 | 182.137 | 182.572 | 0.435377 |
| post22_hold_plateau_upper | flare_gradient_source | 5.77 | 0.376618 | 0.0105068 | 205.089 | 205.555 | 0.466248 |
| post22_hold_plateau_upper | flare_gradient_source | 8.66 | 0.316098 | 0.185796 | 195.226 | 195.401 | 0.174444 |
| post22_hold_plateau_upper | flare_gradient_source | 11.54 | 0.245003 | 0.888962 | 196.379 | 195.52 | -0.859318 |
| post22_hold_plateau_upper | flare_gradient_source | 14.43 | 0.191315 | 1.47391 | 187.161 | 185.36 | -1.80057 |
| post22_hold_plateau_upper | flare_gradient_source | 17.31 | 0.154576 | 0.942397 | 181.538 | 180.399 | -1.13832 |
| post22_hold_plateau_upper | flare_gradient_source | 20.2 | 0.12917 | 0.181907 | 176.365 | 176.287 | -0.0782063 |
| post22_hold_plateau_upper | flare_gradient_source | 23.08 | 0.111082 | 0.00835927 | 171.631 | 171.787 | 0.156427 |
| post22_hold_plateau_upper | flare_gradient_source | 28.85 | 0.0870973 | 1.49354e-07 | 164.547 | 164.685 | 0.138348 |
| post22_hold_plateau_upper | flare_gradient_source | 31.74 | 0.0787104 | 5.3259e-11 | 161.583 | 161.71 | 0.127323 |
| post22_hold_plateau_upper | flare_gradient_source | 34.62 | 0.0718578 | 1.23989e-14 | 158.91 | 159.028 | 0.118195 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 2.89 | 0.303817 | 0.000189046 | 182.137 | 182.572 | 0.435377 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 5.77 | 0.376618 | 0.0105068 | 205.089 | 205.555 | 0.466248 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 8.66 | 0.316098 | 0.185796 | 195.226 | 195.401 | 0.174444 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 11.54 | 0.245003 | 0.888963 | 196.379 | 195.52 | -0.859318 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 14.43 | 0.191315 | 1.47401 | 187.161 | 185.36 | -1.8007 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 17.31 | 0.154576 | 0.945164 | 181.538 | 180.395 | -1.14233 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 20.2 | 0.12917 | 0.207145 | 176.365 | 176.25 | -0.115645 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 23.08 | 0.111082 | 0.0795902 | 171.631 | 171.679 | 0.0479711 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 28.85 | 0.0870973 | 0.0172198 | 164.547 | 164.658 | 0.111005 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 31.74 | 0.0787104 | 0.0014783 | 161.583 | 161.708 | 0.124932 |
| post22_hold_plateau_upper | flare_gradient_plus_ring_offset_source | 34.62 | 0.0718578 | 4.64623e-05 | 158.91 | 159.028 | 0.118119 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 2.89 | 0.303817 | 0.000189046 | 182.137 | 182.572 | 0.435377 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 5.77 | 0.376618 | 0.0105068 | 205.089 | 205.555 | 0.466248 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 8.66 | 0.316098 | 0.185796 | 195.226 | 195.401 | 0.174444 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 11.54 | 0.245003 | 0.888962 | 196.379 | 195.52 | -0.859318 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 14.43 | 0.191315 | 1.47391 | 187.161 | 185.36 | -1.80057 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 17.31 | 0.154576 | 0.942397 | 181.538 | 180.399 | -1.13832 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 20.2 | 0.12917 | 0.181907 | 176.365 | 176.287 | -0.0782063 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 23.08 | 0.111082 | 0.00835927 | 171.631 | 171.787 | 0.156427 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 28.85 | 0.0870973 | 1.49354e-07 | 164.547 | 164.685 | 0.138348 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 31.74 | 0.0787104 | 5.32515e-11 | 161.583 | 161.71 | 0.127323 |
| post22_linear_taper_to_inner_height | flare_gradient_source | 34.62 | 0.0718578 | 4.28508e-15 | 158.91 | 159.028 | 0.118195 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 2.89 | 0.303817 | 0.000189046 | 182.137 | 182.572 | 0.435377 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 5.77 | 0.376618 | 0.0105068 | 205.089 | 205.555 | 0.466248 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 8.66 | 0.316098 | 0.185796 | 195.226 | 195.401 | 0.174444 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 11.54 | 0.245003 | 0.888963 | 196.379 | 195.52 | -0.859318 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 14.43 | 0.191315 | 1.47401 | 187.161 | 185.36 | -1.8007 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 17.31 | 0.154576 | 0.945164 | 181.538 | 180.395 | -1.14233 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 20.2 | 0.12917 | 0.207145 | 176.365 | 176.25 | -0.115645 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 23.08 | 0.111082 | 0.0795902 | 171.631 | 171.679 | 0.0479711 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 28.85 | 0.0870973 | 0.0172198 | 164.547 | 164.658 | 0.111005 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 31.74 | 0.0787104 | 0.0014783 | 161.583 | 161.708 | 0.124932 |
| post22_linear_taper_to_inner_height | flare_gradient_plus_ring_offset_source | 34.62 | 0.0718578 | 4.64623e-05 | 158.91 | 159.028 | 0.118119 |

## Claim Boundary

This is a formula-development preflight. The closure-source policies are explicit prototype rules and are not source-validated endpoint laws. Stress scores do not authorize label or endpoint promotion.
