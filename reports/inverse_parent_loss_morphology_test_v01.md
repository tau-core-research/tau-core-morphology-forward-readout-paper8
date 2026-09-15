# Inverse parent-loss morphology test v01

Status: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`.

This held-out test asks whether residual-blind source morphology predicts
the endpoint-derived `kappa_required` atlas. It does not infer a parent law.

## Held-out summary

| baseline_id | model_id | selected_alpha | holdout_mean_galaxy_rmse_kappa | rmse_ratio_to_zero | mean_delta_rmse_vs_zero | bootstrap_ci_lower | bootstrap_ci_upper | paired_sign_flip_p_lower | galaxy_win_fraction | point_pearson_r | point_spearman_r |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| newtonian_baryonic | radial_only | 0.01 | 0.311055 | 0.525268 | -0.281128 | -0.367803 | -0.186476 | 1.99996e-05 | 0.795455 | 0.34304 | 0.365877 |
| newtonian_baryonic | morphology_proxy | 10 | 0.266815 | 0.450563 | -0.325367 | -0.406488 | -0.238116 | 1.99996e-05 | 0.840909 | 0.62731 | 0.667649 |
| newtonian_baryonic | combined | 10 | 0.247059 | 0.417201 | -0.345123 | -0.421034 | -0.26551 | 1.99996e-05 | 0.886364 | 0.680117 | 0.697262 |
| tpg_v6 | radial_only | 0.01 | 0.242296 | 1.00727 | 0.00174864 | -0.00619117 | 0.00956593 | 0.662107 | 0.431818 | 0.0568734 | 0.0218017 |
| tpg_v6 | morphology_proxy | 100 | 0.241701 | 1.00479 | 0.00115314 | -0.0139934 | 0.0163765 | 0.555089 | 0.454545 | 0.0475268 | -0.0526443 |
| tpg_v6 | combined | 10 | 0.229484 | 0.954008 | -0.0110634 | -0.0411012 | 0.017155 | 0.233655 | 0.522727 | 0.362955 | 0.300589 |
| mond_fixed | radial_only | 0.01 | 0.244441 | 0.993933 | -0.00149208 | -0.0195591 | 0.0164988 | 0.436391 | 0.522727 | 0.0771973 | 0.0843749 |
| mond_fixed | morphology_proxy | 100 | 0.242127 | 0.984524 | -0.00380612 | -0.028942 | 0.0202518 | 0.381972 | 0.522727 | 0.180392 | 0.0880331 |
| mond_fixed | combined | 10 | 0.228759 | 0.930168 | -0.0171739 | -0.0533489 | 0.0171157 | 0.181916 | 0.477273 | 0.406814 | 0.343222 |

## Incremental comparisons

| baseline_id | comparison_id | mean_delta_rmse_left_minus_right | bootstrap_ci_lower | bootstrap_ci_upper | paired_sign_flip_p_lower | left_win_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| newtonian_baryonic | morphology_beyond_radial | -0.0442392 | -0.0755437 | -0.0141575 | 0.00357993 | 0.613636 |
| newtonian_baryonic | orientation_added_to_morphology | -0.0155254 | -0.0385323 | 0.00812544 | 0.103778 | 0.568182 |
| newtonian_baryonic | observer_added_to_morphology | -0.0197566 | -0.04108 | 0.0017153 | 0.0399792 | 0.636364 |
| tpg_v6 | morphology_beyond_radial | -0.000595505 | -0.0115274 | 0.00990314 | 0.459711 | 0.386364 |
| tpg_v6 | orientation_added_to_morphology | -0.0123052 | -0.0340078 | 0.00889218 | 0.133277 | 0.568182 |
| tpg_v6 | observer_added_to_morphology | -0.0122165 | -0.034322 | 0.00885136 | 0.140117 | 0.5 |
| mond_fixed | morphology_beyond_radial | -0.00231404 | -0.0140281 | 0.00873545 | 0.346933 | 0.522727 |
| mond_fixed | orientation_added_to_morphology | -0.0135783 | -0.0353499 | 0.00773819 | 0.115598 | 0.568182 |
| mond_fixed | observer_added_to_morphology | -0.0133678 | -0.0352332 | 0.00861787 | 0.121118 | 0.522727 |

A morphology improvement relative to radius alone is an empirical
association with the inverse target, not identification of morphological
parent loss. Conventional source and measurement covariates remain direct
alternatives. A later source-frozen law must predict untouched endpoints.
