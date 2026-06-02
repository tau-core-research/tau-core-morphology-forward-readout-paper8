# Predeclared Quality Gate Diagnostics

This diagnostic evaluates several predeclared quality gates under the
fixed train-selected shrinkage policy. It does not choose a gate by
peeking at individual galaxy residuals; it reports which quality rules
would be plausible candidates for a future endpoint protocol.

## Holdout Quality Gates

| quality_gate | n_galaxies | n_families_present | matched_beats_wrong_fraction | matched_rank1_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | mean_matched_minus_wrong | mean_matched_minus_tpg_v6 | mean_matched_minus_mond | gate_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean_manifest_proxy | 20 | 4 | 0.9 | 0.25 | 0.5 | 0.75 | -9.67091 | 0.181798 | -1.32058 | candidate_predeclared_gate |
| confidence_ge_0_75_and_clean | 20 | 4 | 0.9 | 0.25 | 0.5 | 0.75 | -9.67091 | 0.181798 | -1.32058 | candidate_predeclared_gate |
| no_large_distance_error | 26 | 4 | 0.884615 | 0.269231 | 0.538462 | 0.730769 | -10.4694 | 0.119053 | -1.09512 | candidate_predeclared_gate |
| no_low_inclination | 35 | 4 | 0.857143 | 0.285714 | 0.514286 | 0.657143 | -9.40436 | 0.346812 | -0.387137 | candidate_predeclared_gate |
| confidence_ge_0_85 | 30 | 4 | 0.833333 | 0.3 | 0.5 | 0.6 | -7.4704 | 0.435603 | -0.174831 | candidate_predeclared_gate |
| confidence_ge_0_75 | 32 | 4 | 0.84375 | 0.34375 | 0.53125 | 0.59375 | -9.05639 | 0.369193 | -0.102661 | specificity_only |
| all | 44 | 4 | 0.818182 | 0.272727 | 0.477273 | 0.613636 | -8.55421 | 0.316746 | -0.154499 | specificity_only |
| no_few_rotation_points | 36 | 4 | 0.777778 | 0.305556 | 0.5 | 0.555556 | -6.48205 | 0.365513 | 0.163051 | weak |

## Family Rows for All vs Clean Manifest Gate

| quality_gate | split | formula_family | n_galaxies | matched_beats_wrong_fraction | matched_beats_tpg_v6_fraction | matched_beats_mond_fraction | mean_matched_minus_wrong | mean_matched_minus_tpg_v6 | mean_matched_minus_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | holdout | K_compact_finite | 7 | 0.571429 | 0.571429 | 0.571429 | 0.934141 | 0.970021 | 1.21928 |
| all | holdout | K_exponential_disk | 7 | 0.714286 | 0.285714 | 0.285714 | -6.00703 | 0.923998 | 1.60433 |
| all | holdout | K_scale_tail_spiral | 20 | 0.9 | 0.4 | 0.7 | -15.869 | 0.148795 | -0.533757 |
| all | holdout | K_thick_flared | 10 | 0.9 | 0.7 | 0.7 | -2.3496 | -0.229722 | -1.58881 |
| clean_manifest_proxy | holdout | K_compact_finite | 2 | 0.5 | 0.5 | 1 | 0.769747 | 0.577674 | -0.465739 |
| clean_manifest_proxy | holdout | K_exponential_disk | 3 | 0.666667 | 0.666667 | 0.666667 | -5.11245 | 0.51928 | -0.34545 |
| clean_manifest_proxy | holdout | K_scale_tail_spiral | 8 | 1 | 0.25 | 0.75 | -20.3087 | 0.44724 | -1.12041 |
| clean_manifest_proxy | holdout | K_thick_flared | 7 | 1 | 0.714286 | 0.714286 | -2.45008 | -0.379307 | -2.2115 |

## Claim Boundary

A candidate quality gate is not a discovery claim. It is a proposed
predeclared observability rule for the next run. Any final Paper 8
endpoint must declare the quality gate before endpoint scoring and keep
the excluded/caveated rows as negative or limited-observability evidence.
