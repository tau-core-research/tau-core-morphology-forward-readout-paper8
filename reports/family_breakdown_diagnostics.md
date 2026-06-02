# Family Breakdown Diagnostic

This diagnostic uses only the train-selected shrinkage policy and breaks
the result down by residual-blind morphology family. It does not refit
per family and does not choose a new endpoint policy.

## Selected Policies

| selection_rule | selected_family_weight | selected_amplitude_path_id |
| --- | --- | --- |
| train_balanced_max | 0.4 | shrink_family_weight_0.40 |
| train_specificity_then_baseline | 0.4 | shrink_family_weight_0.40 |
| train_mond_gap_min_with_specificity | 0.4 | shrink_family_weight_0.40 |
| train_tpg_gap_min_with_specificity | 0.4 | shrink_family_weight_0.40 |

## Holdout Family Breakdown

| formula_family | n_galaxies | matched_beats_wrong_fraction | matched_rank1_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | mean_matched_minus_wrong | mean_matched_minus_tpg_v6 | mean_matched_minus_mond | specificity_status | baseline_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K_thick_flared | 10 | 0.9 | 0.1 | 0.7 | 0.7 | -2.3496 | -0.229722 | -1.58881 | strong | competitive_with_mond_and_tpg |
| K_scale_tail_spiral | 20 | 0.9 | 0.25 | 0.4 | 0.7 | -15.869 | 0.148795 | -0.533757 | strong | mond_competitive_tpg_blocked |
| K_exponential_disk | 7 | 0.714286 | 0.285714 | 0.285714 | 0.285714 | -6.00703 | 0.923998 | 1.60433 | weak | baseline_blocked |
| K_compact_finite | 7 | 0.571429 | 0.571429 | 0.571429 | 0.571429 | 0.934141 | 0.970021 | 1.21928 | weak | tpg_competitive_mond_blocked |

## Train Family Breakdown

| formula_family | n_galaxies | matched_beats_wrong_fraction | matched_rank1_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | mean_matched_minus_wrong | mean_matched_minus_tpg_v6 | mean_matched_minus_mond | specificity_status | baseline_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K_compact_finite | 22 | 0.5 | 0.5 | 0.5 | 0.590909 | -0.159719 | 0.0671286 | 0.313404 | weak | tpg_competitive_mond_blocked |
| K_exponential_disk | 25 | 0.76 | 0.4 | 0.4 | 0.48 | -4.405 | 0.334221 | 0.499725 | weak | baseline_blocked |
| K_scale_tail_spiral | 60 | 0.966667 | 0.383333 | 0.483333 | 0.616667 | -14.4314 | 0.0462168 | -0.567382 | strong | mond_competitive_tpg_blocked |
| K_thick_flared | 24 | 0.708333 | 0.0416667 | 0.541667 | 0.583333 | -2.87547 | -0.14126 | -1.63752 | weak | tpg_competitive_mond_blocked |

## Interpretation Boundary

The useful question is not only whether the global endpoint improves.
The family breakdown identifies which morphology families preserve
matched-vs-wrong specificity and which families remain blocked by
TPG/v6 or MOND comparators. This is a preparation diagnostic, not an
empirical validation claim.
