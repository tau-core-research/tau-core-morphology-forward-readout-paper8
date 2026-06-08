# Source-Native Carrier Robustness

This stress test repeats the source-native readout formula preflight with
different frozen carriers for the train-only amplitude residual. Labels,
kernels, source proxies, and train/holdout splits are unchanged.

## Holdout Summary

| carrier_id | matched_beats_wrong_fraction | mean_matched_minus_wrong | p_mean_minus_wrong_at_least_as_good | p_beats_wrong_fraction_at_least_as_good | matched_beats_carrier_fraction | matched_beats_tpg_v6_fraction | matched_beats_newtonian_baryonic_fraction | matched_beats_mond_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tpg_v6 | 0.886364 | -17.6838 | 0.001998 | 0.00599401 | 0.477273 | 0.477273 | 0.818182 | 0.477273 |
| newtonian_baryonic | 0.954545 | -51.1311 | 0.000999001 | 0.000999001 | 0.795455 | 0.272727 | 0.795455 | 0.295455 |

## Holdout By Family

| carrier_id | formula_family | n_galaxies | matched_beats_wrong_fraction | mean_matched_minus_wrong | median_matched_minus_wrong | matched_beats_carrier_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| newtonian_baryonic | K_compact_finite | 7 | 0.714286 | 11.8643 | -1.76285 | 0.857143 |
| newtonian_baryonic | K_exponential_disk | 7 | 1 | -57.7842 | -57.9693 | 1 |
| newtonian_baryonic | K_scale_tail_spiral | 20 | 1 | -79.8704 | -70.9901 | 0.7 |
| newtonian_baryonic | K_thick_flared | 10 | 1 | -33.092 | -29.9298 | 0.8 |
| tpg_v6 | K_compact_finite | 7 | 0.571429 | 3.71475 | -0.427522 | 0.571429 |
| tpg_v6 | K_exponential_disk | 7 | 0.857143 | -15.1925 | -10.251 | 0.285714 |
| tpg_v6 | K_scale_tail_spiral | 20 | 1 | -30.7479 | -22.4516 | 0.4 |
| tpg_v6 | K_thick_flared | 10 | 0.9 | -8.2784 | -4.54121 | 0.7 |

## Freeze-Invariance Audit

| carrier_id | audit_field | status | evidence |
| --- | --- | --- | --- |
| tpg_v6 | labels_frozen | PASS | same source_native_readout_formula_labels.csv consumed for all carriers |
| tpg_v6 | kernels_frozen | PASS | same add_bridge_formula_kernels output; no carrier-dependent kernel code path |
| tpg_v6 | split_frozen | PASS | split column is read from the same point artifact and is not redrawn |
| tpg_v6 | only_carrier_changes | PASS | amplitude target changes from vobs^2-carrier^2; carrier_column=v_v6 |
| tpg_v6 | label_columns_snapshot | INFO | amplitude_policy,bar_m2_proxy,compact_support_radius_proxy_kpc,distance_frac_error,distance_quality,forbidden_inputs,formula_family,galaxy,hub_type,inc_bin,inclination_deg,inclination_error_deg,lopsided_m1_proxy,manifest_caveat,manifest_confidence,max_bulge,mean_bulge,mean_gas,mean_log_sbdisk,n_points,parameter_source,peak_log_sb,r_max,r_median,r_min,ring_radius_proxy_kpc,ring_width_proxy_kpc,role,scale_radius_proxy_kpc,split,tail_cutoff_radius_proxy_kpc,tail_inner_radius_proxy_kpc,thickness_h_over_rs_proxy,type_bin |
| newtonian_baryonic | labels_frozen | PASS | same source_native_readout_formula_labels.csv consumed for all carriers |
| newtonian_baryonic | kernels_frozen | PASS | same add_bridge_formula_kernels output; no carrier-dependent kernel code path |
| newtonian_baryonic | split_frozen | PASS | split column is read from the same point artifact and is not redrawn |
| newtonian_baryonic | only_carrier_changes | PASS | amplitude target changes from vobs^2-carrier^2; carrier_column=vn |
| newtonian_baryonic | label_columns_snapshot | INFO | amplitude_policy,bar_m2_proxy,compact_support_radius_proxy_kpc,distance_frac_error,distance_quality,forbidden_inputs,formula_family,galaxy,hub_type,inc_bin,inclination_deg,inclination_error_deg,lopsided_m1_proxy,manifest_caveat,manifest_confidence,max_bulge,mean_bulge,mean_gas,mean_log_sbdisk,n_points,parameter_source,peak_log_sb,r_max,r_median,r_min,ring_radius_proxy_kpc,ring_width_proxy_kpc,role,scale_radius_proxy_kpc,split,tail_cutoff_radius_proxy_kpc,tail_inner_radius_proxy_kpc,thickness_h_over_rs_proxy,type_bin |

## Claim Boundary

A positive matched-versus-wrong result under the Newtonian baryonic carrier
would support carrier robustness of morphology specificity. It would not by
itself establish population-level superiority over TPG/v6, MOND-like, RAR,
or Newtonian baselines.
