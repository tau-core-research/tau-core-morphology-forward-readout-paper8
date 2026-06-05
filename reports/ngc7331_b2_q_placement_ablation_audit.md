# NGC7331 B2 q-placement ablation audit

This is a diagnostic hiba-audit, not a new endpoint. It was run after
the negative exact B2 interval-control result to localize the failure
mode of the transferred NGC4088 B2 shell.

## Summary

| galaxy | audit_status | n_points | n_outer_active_points | source_q_warp_max | current_effective_q_power | current_rmse_km_s | current_outer_rmse_km_s | best_diagnostic_variant | best_diagnostic_rmse_km_s | no_q_unit_newtonian_ramp_rmse_km_s | no_q_unit_newtonian_ramp_outer_rmse_km_s | diagnostic_exponential_carrier_rmse_km_s | required_q_double_median | required_q_single_median | required_q_double_to_source_qmax_median_ratio | failure_mode | claim_status | construction_used_vobs | diagnostic_scoring_used_vobs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_B2_Q_PLACEMENT_ABLATION_DIAGNOSTIC_COMPLETE_NOT_ENDPOINT | 36 | 21 | 0.205796 | 2 | 56.2674 | 70.6815 | NEWTONIAN_vn__lambda_xw_vflat2__kernel_ramp__plus_added_readout | 21.7334 | 21.7334 | 19.446 | 23.9219 | 1.02432 | 1.04923 | 4.97737 | q_warp is effectively squared by the transferred protocol; NGC4088 had q_warp=1 so the issue was hidden, but NGC7331 has q_warp<1 and the outer correction is suppressed | diagnostic ablation only; variants inspected after negative interval-control audit and cannot be used as endpoints | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |

## Top diagnostic variants

| galaxy | diagnostic_variant_id | carrier_id | amplitude_id | kernel_id | sign_id | q_power_effective | amplitude_km2_s2 | rmse_km_s | mae_km_s | inner_rmse_km_s | outer_rmse_km_s | within_err_fraction | last_radius_prediction_km_s | construction_used_vobs | diagnostic_scoring_used_vobs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NEWTONIAN_vn__lambda_xw_vflat2__kernel_ramp__plus_added_readout | NEWTONIAN_vn | lambda_xw_vflat2 | kernel_ramp | plus_added_readout | 0 | 30520.3 | 21.7334 | 19.0392 | 24.5808 | 19.446 | 0.111111 | 267.303 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | EXPONENTIAL_DISK_CARRIER__lambda_q_xw_vflat2_cross_high__kernel_q_ramp__minus_attenuation | EXPONENTIAL_DISK_CARRIER | lambda_q_xw_vflat2_cross_high | kernel_q_ramp | minus_attenuation | 2 | 9349.63 | 23.143 | 19.0976 | 32.5022 | 12.7909 | 0.111111 | 227.975 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | EXPONENTIAL_DISK_CARRIER__lambda_q_xw_vflat2__kernel_q_ramp__minus_attenuation | EXPONENTIAL_DISK_CARRIER | lambda_q_xw_vflat2 | kernel_q_ramp | minus_attenuation | 2 | 6280.94 | 23.2041 | 19.1221 | 32.5022 | 12.9793 | 0.166667 | 230.372 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | EXPONENTIAL_DISK_CARRIER__lambda_q_xw_vflat2__kernel_q_ramp__plus_added_readout | EXPONENTIAL_DISK_CARRIER | lambda_q_xw_vflat2 | kernel_q_ramp | plus_added_readout | 2 | 6280.94 | 23.9219 | 20.5607 | 32.5022 | 15.0482 | 0.0833333 | 239.933 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | EXPONENTIAL_DISK_CARRIER__lambda_q_xw_vflat2__kernel_ramp__minus_attenuation | EXPONENTIAL_DISK_CARRIER | lambda_q_xw_vflat2 | kernel_ramp | minus_attenuation | 1 | 6280.94 | 24.0831 | 20.7507 | 32.5022 | 15.4828 | 0.0555556 | 210.7 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | EXPONENTIAL_DISK_CARRIER__lambda_xw_vflat2__kernel_q_ramp__minus_attenuation | EXPONENTIAL_DISK_CARRIER | lambda_xw_vflat2 | kernel_q_ramp | minus_attenuation | 1 | 30520.3 | 24.0831 | 20.7507 | 32.5022 | 15.4828 | 0.0555556 | 210.7 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | EXPONENTIAL_DISK_CARRIER__lambda_q_xw_vflat2_cross_high__kernel_q_ramp__plus_added_readout | EXPONENTIAL_DISK_CARRIER | lambda_q_xw_vflat2_cross_high | kernel_q_ramp | plus_added_readout | 2 | 9349.63 | 24.2014 | 21.2232 | 32.5022 | 15.7958 | 0.0555556 | 242.211 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | TPG_V6_v_v6__lambda_q_xw_vflat2_cross_high__kernel_q_ramp__minus_attenuation | TPG_V6_v_v6 | lambda_q_xw_vflat2_cross_high | kernel_q_ramp | minus_attenuation | 2 | 9349.63 | 24.8677 | 21.0713 | 33.9484 | 15.3917 | 0.166667 | 231.774 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | TPG_V6_v_v6__lambda_xw_vflat2__kernel_q_ramp__minus_attenuation | TPG_V6_v_v6 | lambda_xw_vflat2 | kernel_q_ramp | minus_attenuation | 1 | 30520.3 | 24.9663 | 21.6764 | 33.9484 | 15.663 | 0.0555556 | 214.804 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | TPG_V6_v_v6__lambda_q_xw_vflat2__kernel_ramp__minus_attenuation | TPG_V6_v_v6 | lambda_q_xw_vflat2 | kernel_ramp | minus_attenuation | 1 | 6280.94 | 24.9663 | 21.6764 | 33.9484 | 15.663 | 0.0555556 | 214.804 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | TPG_V6_v_v6__lambda_q_xw_vflat2__kernel_q_ramp__minus_attenuation | TPG_V6_v_v6 | lambda_q_xw_vflat2 | kernel_q_ramp | minus_attenuation | 2 | 6280.94 | 25.0299 | 21.3144 | 33.9484 | 15.836 | 0.166667 | 234.131 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | TPG_V6_v_v6__lambda_q_xw_vflat2__kernel_q_ramp__plus_added_readout | TPG_V6_v_v6 | lambda_q_xw_vflat2 | kernel_q_ramp | plus_added_readout | 2 | 6280.94 | 26.0923 | 23.5537 | 33.9484 | 18.5442 | 0.0555556 | 243.545 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |

## Required amplitude audit

| galaxy | kernel_id | required_lambda_median_km2_s2 | required_lambda_p25_km2_s2 | required_lambda_p75_km2_s2 | required_lambda_min_km2_s2 | required_lambda_max_km2_s2 | required_lambda_cv | source_lambda_qmax_km2_s2 | source_scale_xw_vflat2_km2_s2 | construction_used_vobs | diagnostic_scoring_used_vobs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | current_kernel_q_ramp | 155605 | 124803 | 234626 | 106938 | 1.87697e+06 | 1.32467 | 6280.94 | 30520.3 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |
| NGC7331 | ramp_only | 32022.9 | 25683.9 | 48285 | 22007.5 | 386272 | 1.32467 | 6280.94 | 30520.3 | False | True | False | ngc7331_b2_q_placement_ablation_diagnostic_only_not_endpoint |

## Interpretation

The transferred exact B2 protocol places `q_warp` both in `lambda_w` and
in `C_warp`, so the outer correction scales effectively as `q_warp^2`.
That was invisible in NGC4088 because its frozen protocol used
`q_warp=1`. It becomes a serious suppression in NGC7331, where the
source-side interval has `q_warp < 1`. The diagnostic no-q unit-ramp
variant is not an endpoint, but its improved RMSE localizes the failure
to the q-placement/source-load law rather than to the ramp shape alone.
