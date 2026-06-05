# NGC7331 B2 q-role separation diagnostic

This diagnostic follows the failed NGC7331 exact B2 interval-control
audit. It is not an endpoint and does not promote a new formula.

## Summary

| galaxy | audit_status | current_formula | recommended_theory_fix | source_q_shape_max | current_rmse_km_s | unit_load_unit_shape_reference_rmse_km_s | required_mu_load_if_ramp_kernel_median | required_mu_load_if_q_kernel_median | claim_status | construction_used_vobs | diagnostic_scoring_used_vobs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_B2_Q_ROLE_SEPARATION_DIAGNOSTIC_COMPLETE_NOT_ENDPOINT | Delta v^2 = q_warp^2 x_w Vflat^2 ramp | split q_warp into q_shape and mu_load before any future freeze | 0.205796 | 56.2674 | 21.7334 | 1.04923 | 5.09842 | diagnostic-only formula-role separation; no endpoint promotion | False | True | False | ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint |

## Role split

| role_id | formula | q_shape_factor | mu_load_factor | effective_q_power | interpretation | status | galaxy | construction_used_vobs | diagnostic_scoring_used_vobs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| current_identified_role | Delta v^2 = q_warp^2 x_w Vflat^2 ramp | 0.205796 | 0.205796 | 2 | NGC4088-degenerate convention; suppresses NGC7331 because q_warp<1 | DIAGNOSTIC_FAILURE_MODE | NGC7331 | False | True | False | ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint |
| shape_only_q_role | Delta v^2 = mu_load x_w Vflat^2 q_shape ramp | 0.205796 | 5.09842 | 1 | keeps q_warp as spatial source strength; requires separate load coefficient | POST_FAILURE_DIAGNOSTIC_ONLY | NGC7331 | False | True | False | ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint |
| load_not_shape_q_role | Delta v^2 = mu_load x_w Vflat^2 ramp | 1 | 1.04923 | 0 | treats THINGS q_warp as not the B2 radial kernel amplitude | POST_FAILURE_DIAGNOSTIC_ONLY | NGC7331 | False | True | False | ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint |

## Diagnostic scores

| galaxy | role_id | mu_load_used | kernel_uses_q_shape | rmse_km_s | outer_rmse_km_s | inner_rmse_km_s | last_radius_prediction_km_s | construction_used_vobs | diagnostic_scoring_used_vobs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | unit_load_unit_shape_reference | 1 | False | 21.7334 | 19.446 | 24.5808 | 267.303 | False | True | False | ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint |
| NGC7331 | shape_only_q_role_median_mu | 5.09842 | True | 22.2894 | 20.4964 | 24.5808 | 272.148 | False | True | False | ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint |
| NGC7331 | load_not_shape_q_role_median_mu | 1.04923 | False | 22.2894 | 20.4964 | 24.5808 | 272.148 | False | True | False | ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint |
| NGC7331 | current_identified_role | 0.205796 | True | 56.2674 | 70.6815 | 24.5808 | 143.573 | False | True | False | ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint |

## Required source-load coefficient

| galaxy | quantity | median | p25 | p75 | min | max | source_q_shape_max | median_to_source_q_shape_ratio | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | required_mu_load_if_kernel_is_ramp | 1.04923 | 0.841534 | 1.58206 | 0.721078 | 12.6563 | 0.205796 | 5.09842 | False | ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint |
| NGC7331 | required_mu_load_if_kernel_is_q_shape_ramp | 5.09842 | 4.08917 | 7.68754 | 3.50385 | 61.4991 | 0.205796 | 24.7742 | False | ngc7331_b2_q_role_separation_diagnostic_only_not_endpoint |

## Verdict

The B2 transfer should not identify the radial kernel strength and the
source-load amplitude by default. NGC4088 could not expose this because
`q_warp=1`; NGC7331 does expose it because the source q interval is well
below one. The next theory task is to derive a Tau-side `mu_load` or
other source-load coefficient independently of the observed rotation
residuals, while keeping `q_shape` as a source morphology/kernel handle.
