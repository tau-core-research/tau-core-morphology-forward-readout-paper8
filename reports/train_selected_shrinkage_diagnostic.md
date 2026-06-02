# Train-Selected Shrinkage Diagnostic

This diagnostic selects the family-to-global shrinkage weight using train
split metrics only, then evaluates the selected policy on holdout. It is
designed to prevent reading the shrinkage weight directly from holdout.

## Train Selections

| selection_rule | selected_family_weight | selected_amplitude_path_id | train_balanced_score | train_baseline_score | train_specificity_score | train_specificity_ok | train_mond_win_ok | train_tpg_win_ok |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train_balanced_max | 0.4 | shrink_family_weight_0.40 | 1.8626 | 1.05966 | 0.801527 | True | True | False |
| train_specificity_then_baseline | 0.4 | shrink_family_weight_0.40 | 1.8626 | 1.05966 | 0.801527 | True | True | False |
| train_mond_gap_min_with_specificity | 0.4 | shrink_family_weight_0.40 | 1.8626 | 1.05966 | 0.801527 | True | True | False |
| train_tpg_gap_min_with_specificity | 0.4 | shrink_family_weight_0.40 | 1.8626 | 1.05966 | 0.801527 | True | True | False |

## Holdout Evaluation

| selection_rule | selected_family_weight | selected_amplitude_path_id | train_balanced_score | train_baseline_score | train_specificity_score | train_specificity_ok | train_mond_win_ok | train_tpg_win_ok | holdout_n_galaxies | holdout_matched_beats_wrong_fraction | holdout_matched_rank1_fraction | holdout_matched_beats_tpg_v6_fraction | holdout_matched_beats_mond_fraction | holdout_mean_matched_minus_wrong | holdout_median_matched_minus_wrong | holdout_mean_matched_minus_tpg_v6 | holdout_median_matched_minus_tpg_v6 | holdout_mean_matched_minus_mond | holdout_median_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train_balanced_max | 0.4 | shrink_family_weight_0.40 | 1.8626 | 1.05966 | 0.801527 | True | True | False | 44 | 0.818182 | 0.272727 | 0.477273 | 0.613636 | -8.55421 | -5.47095 | 0.316746 | 0.124458 | -0.154499 | -0.950214 |
| train_specificity_then_baseline | 0.4 | shrink_family_weight_0.40 | 1.8626 | 1.05966 | 0.801527 | True | True | False | 44 | 0.818182 | 0.272727 | 0.477273 | 0.613636 | -8.55421 | -5.47095 | 0.316746 | 0.124458 | -0.154499 | -0.950214 |
| train_mond_gap_min_with_specificity | 0.4 | shrink_family_weight_0.40 | 1.8626 | 1.05966 | 0.801527 | True | True | False | 44 | 0.818182 | 0.272727 | 0.477273 | 0.613636 | -8.55421 | -5.47095 | 0.316746 | 0.124458 | -0.154499 | -0.950214 |
| train_tpg_gap_min_with_specificity | 0.4 | shrink_family_weight_0.40 | 1.8626 | 1.05966 | 0.801527 | True | True | False | 44 | 0.818182 | 0.272727 | 0.477273 | 0.613636 | -8.55421 | -5.47095 | 0.316746 | 0.124458 | -0.154499 | -0.950214 |

## Claim Boundary

This is still a diagnostic, not a validated amplitude-normalization law.
A train-selected weight that transfers to holdout is evidence for a stable
normalization range, but the range must still be derived from Tau-side
source normalization before it can be used as a paper endpoint policy.
