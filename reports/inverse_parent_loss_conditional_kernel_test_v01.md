# Inverse parent-loss conditional-kernel test v01

Status: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`.

The diagnostic tests radial B-splines, morphology-conditioned spline
interactions, and a morphology-plus-observer version on the frozen
131/44 galaxy split. Knot count and ridge strength are selected only
inside grouped training cross-validation.

## Held-out results

| baseline_id | model_id | knots | alpha | rmse_ratio_to_zero | mean_delta_rmse_vs_zero | ci_lower | ci_upper | p_lower | galaxy_win_fraction | pearson_r | spearman_r |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| newtonian_baryonic | radial_spline | 4 | 10 | 0.526293 | -0.280521 | -0.365718 | -0.19069 | 0.00019996 | 0.727273 | 0.317916 | 0.354403 |
| newtonian_baryonic | morphology_kernel | 4 | 10 | 0.449949 | -0.32573 | -0.41161 | -0.240965 | 0.00019996 | 0.840909 | 0.62595 | 0.6612 |
| newtonian_baryonic | morphology_observer_kernel | 4 | 10 | 0.416622 | -0.345466 | -0.419837 | -0.268682 | 0.00019996 | 0.886364 | 0.682766 | 0.690712 |
| tpg_v6 | radial_spline | 6 | 10 | 1.00542 | 0.00130316 | -0.00613008 | 0.00891921 | 0.637273 | 0.454545 | 0.0319513 | 0.0152134 |
| tpg_v6 | morphology_kernel | 6 | 100 | 1.00381 | 0.000916204 | -0.0140666 | 0.0158998 | 0.545291 | 0.5 | 0.0192389 | -0.0832922 |
| tpg_v6 | morphology_observer_kernel | 6 | 100 | 0.963019 | -0.00889574 | -0.0297183 | 0.0115665 | 0.222755 | 0.477273 | 0.361558 | 0.218603 |
| mond_fixed | radial_spline | 6 | 10 | 0.991873 | -0.00199878 | -0.02082 | 0.0155993 | 0.420916 | 0.522727 | 0.0654181 | 0.0864407 |
| mond_fixed | morphology_kernel | 6 | 100 | 0.985151 | -0.00365179 | -0.0279009 | 0.020539 | 0.374925 | 0.522727 | 0.143951 | 0.0119055 |
| mond_fixed | morphology_observer_kernel | 6 | 100 | 0.941019 | -0.0145054 | -0.044599 | 0.0143615 | 0.177764 | 0.5 | 0.414672 | 0.281101 |

## Incremental tests

| baseline_id | left | right | mean_delta_rmse | ci_lower | ci_upper | p_lower | left_win_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| newtonian_baryonic | morphology_kernel | radial_spline | -0.0452096 | -0.0794044 | -0.0136161 | 0.00559888 | 0.568182 |
| newtonian_baryonic | morphology_observer_kernel | morphology_kernel | -0.0197354 | -0.0407972 | 0.00109458 | 0.0383923 | 0.636364 |
| tpg_v6 | morphology_kernel | radial_spline | -0.00038696 | -0.0103408 | 0.00911026 | 0.468106 | 0.409091 |
| tpg_v6 | morphology_observer_kernel | morphology_kernel | -0.00981194 | -0.024155 | 0.00355013 | 0.0845831 | 0.5 |
| mond_fixed | morphology_kernel | radial_spline | -0.00165301 | -0.0126779 | 0.0088018 | 0.388122 | 0.477273 |
| mond_fixed | morphology_observer_kernel | morphology_kernel | -0.0108536 | -0.0249201 | 0.00301715 | 0.075185 | 0.5 |

## Family-label shuffle control

| baseline_id | matched_beats_shuffle_fraction | permutation_p |
| --- | --- | --- |
| newtonian_baryonic | 0.8 | 0.225806 |
| tpg_v6 | 0.8 | 0.225806 |
| mond_fixed | 0.8 | 0.225806 |

Because the target is reconstructed from the endpoint, these are
retrodictive structure tests. They do not identify a parent kernel,
Nature occupation, or a dark-matter replacement law.
