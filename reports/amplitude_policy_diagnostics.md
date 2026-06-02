# Amplitude Policy Diagnostics

This diagnostic keeps the source-native bridge formula kernels fixed and
changes only the amplitude policy. It asks whether the current TPG/MOND
baseline weakness is caused by amplitude normalization rather than by
morphology-family formula specificity.

## Holdout Policy Summary

| amplitude_policy | split | n_galaxies | matched_beats_wrong_fraction | matched_rank1_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | mean_matched_minus_wrong | median_matched_minus_wrong | mean_matched_minus_tpg_v6 | median_matched_minus_tpg_v6 | mean_matched_minus_mond | median_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| family_unconstrained | holdout | 44 | 0.886364 | 0.295455 | 0.477273 | 0.477273 | -17.6838 | -13.9742 | 1.29546 | 0.644948 | 0.824211 | 0.173401 |
| family_attractive_only | holdout | 44 | 0.886364 | 0.295455 | 0.272727 | 0.5 | -17.8331 | -13.5918 | 1.07774 | 0 | 0.60649 | -0.014838 |
| global_unconstrained | holdout | 44 | 0.590909 | 0.25 | 0.545455 | 0.568182 | -0.123899 | -0.130072 | -0.0970081 | -0.0497158 | -0.568253 | -1.76237 |
| global_attractive_only | holdout | 44 | 0.113636 | 0.159091 | 0 | 0.590909 | -1.00929e-16 | 0 | 0 | 0 | -0.471245 | -1.49111 |
| family_shrink_50_to_global | holdout | 44 | 0.863636 | 0.295455 | 0.477273 | 0.636364 | -10.3006 | -6.92273 | 0.456422 | 0.268663 | -0.0148234 | -0.504027 |

## Amplitudes

| amplitude_policy | formula_family | beta_delta_v2_amplitude | raw_family_beta | raw_global_beta | is_negative | kernel | formula_source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| family_unconstrained | K_compact_finite | 108797 | 108797 | -300.552 | False | kernel_K_compact_finite | tau_core_gravity_rmond_compact_finite_source_readout_formula_001 |
| family_unconstrained | K_scale_tail_spiral | 758.092 | 758.092 | -300.552 | False | kernel_K_scale_tail_spiral | tau_core_gravity_rmond_scale_tail_spiral_readout_formula_001:n=2 |
| family_unconstrained | K_exponential_disk | -1003.88 | -1003.88 | -300.552 | True | kernel_K_exponential_disk | tau_core_gravity_rmond_exponential_disk_readout_formula_001:Freeman_Bessel |
| family_unconstrained | K_thick_flared | -522.962 | -522.962 | -300.552 | True | kernel_K_thick_flared | tau_core_gravity_rmond_thick_flared_disk_readout_formula_001:constant_h_exponential_vertical |
| family_attractive_only | K_compact_finite | 108797 | 108797 | -300.552 | False | kernel_K_compact_finite | tau_core_gravity_rmond_compact_finite_source_readout_formula_001 |
| family_attractive_only | K_scale_tail_spiral | 758.092 | 758.092 | -300.552 | False | kernel_K_scale_tail_spiral | tau_core_gravity_rmond_scale_tail_spiral_readout_formula_001:n=2 |
| family_attractive_only | K_exponential_disk | 0 | -1003.88 | -300.552 | False | kernel_K_exponential_disk | tau_core_gravity_rmond_exponential_disk_readout_formula_001:Freeman_Bessel |
| family_attractive_only | K_thick_flared | 0 | -522.962 | -300.552 | False | kernel_K_thick_flared | tau_core_gravity_rmond_thick_flared_disk_readout_formula_001:constant_h_exponential_vertical |
| global_unconstrained | K_compact_finite | -300.552 | 108797 | -300.552 | True | kernel_K_compact_finite | tau_core_gravity_rmond_compact_finite_source_readout_formula_001 |
| global_unconstrained | K_scale_tail_spiral | -300.552 | 758.092 | -300.552 | True | kernel_K_scale_tail_spiral | tau_core_gravity_rmond_scale_tail_spiral_readout_formula_001:n=2 |
| global_unconstrained | K_exponential_disk | -300.552 | -1003.88 | -300.552 | True | kernel_K_exponential_disk | tau_core_gravity_rmond_exponential_disk_readout_formula_001:Freeman_Bessel |
| global_unconstrained | K_thick_flared | -300.552 | -522.962 | -300.552 | True | kernel_K_thick_flared | tau_core_gravity_rmond_thick_flared_disk_readout_formula_001:constant_h_exponential_vertical |
| global_attractive_only | K_compact_finite | 0 | 108797 | -300.552 | False | kernel_K_compact_finite | tau_core_gravity_rmond_compact_finite_source_readout_formula_001 |
| global_attractive_only | K_scale_tail_spiral | 0 | 758.092 | -300.552 | False | kernel_K_scale_tail_spiral | tau_core_gravity_rmond_scale_tail_spiral_readout_formula_001:n=2 |
| global_attractive_only | K_exponential_disk | 0 | -1003.88 | -300.552 | False | kernel_K_exponential_disk | tau_core_gravity_rmond_exponential_disk_readout_formula_001:Freeman_Bessel |
| global_attractive_only | K_thick_flared | 0 | -522.962 | -300.552 | False | kernel_K_thick_flared | tau_core_gravity_rmond_thick_flared_disk_readout_formula_001:constant_h_exponential_vertical |
| family_shrink_50_to_global | K_compact_finite | 54248.4 | 108797 | -300.552 | False | kernel_K_compact_finite | tau_core_gravity_rmond_compact_finite_source_readout_formula_001 |
| family_shrink_50_to_global | K_scale_tail_spiral | 228.77 | 758.092 | -300.552 | False | kernel_K_scale_tail_spiral | tau_core_gravity_rmond_scale_tail_spiral_readout_formula_001:n=2 |
| family_shrink_50_to_global | K_exponential_disk | -652.217 | -1003.88 | -300.552 | True | kernel_K_exponential_disk | tau_core_gravity_rmond_exponential_disk_readout_formula_001:Freeman_Bessel |
| family_shrink_50_to_global | K_thick_flared | -411.757 | -522.962 | -300.552 | True | kernel_K_thick_flared | tau_core_gravity_rmond_thick_flared_disk_readout_formula_001:constant_h_exponential_vertical |

## Claim Boundary

This is not a new endpoint claim. It is an amplitude-policy stress test.
A policy that improves baseline comparison must still be justified from
Tau-side source normalization, not selected post hoc for fit quality.
