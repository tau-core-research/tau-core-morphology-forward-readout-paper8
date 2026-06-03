# Baseline Success Morphology Audit

This audit asks where TPG/MOND/Newton/RAR-style baselines succeed and
what those success zones suggest in Tau Core morphology/readout language.
It is descriptive only: no model is refit and no endpoint claim is made.

## 175-Galaxy TPG/MOND/Tau Holdout Summary

| split | winner_tau_tpg_mond | n_galaxies | mean_manifest_confidence | mean_gas | mean_bulge | mean_log_sbdisk | mean_inclination_deg | current_memory_match_fraction | low_inclination_fraction | large_distance_error_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | mond | 12 | 0.8625 | 0.237975 | 0 | 1.11062 | 56.75 | 0.333333 | 0.25 | 0.416667 |
| holdout | tau_matched | 16 | 0.859375 | 0.175344 | 0.11212 | 1.36156 | 65.625 | 0.5625 | 0.0625 | 0.3125 |
| holdout | tpg_v6 | 16 | 0.8 | 0.306517 | 0.0532677 | 0.906736 | 53.625 | 0 | 0.3125 | 0.5 |

## 175-Galaxy Family x Winner Counts

| split | formula_family | winner_tau_tpg_mond | n_galaxies |
| --- | --- | --- | --- |
| holdout | K_compact_finite | tau_matched | 4 |
| holdout | K_compact_finite | tpg_v6 | 3 |
| holdout | K_exponential_disk | mond | 4 |
| holdout | K_exponential_disk | tau_matched | 2 |
| holdout | K_exponential_disk | tpg_v6 | 1 |
| holdout | K_scale_tail_spiral | mond | 5 |
| holdout | K_scale_tail_spiral | tau_matched | 3 |
| holdout | K_scale_tail_spiral | tpg_v6 | 12 |
| holdout | K_thick_flared | mond | 3 |
| holdout | K_thick_flared | tau_matched | 7 |

## Available Conventional Baseline Summary

| audit_source | available_best_model | n_galaxies | joined_to_primary_175 | current_memory_match_fraction |
| --- | --- | --- | --- | --- |
| paper1_73_baseline_pivot | mond_simple_mu | 22 | 22 | 0.590909 |
| paper1_73_baseline_pivot | newtonian_baryonic | 5 | 5 | 0 |
| paper1_73_baseline_pivot | projection_fixed | 32 | 32 | 0.21875 |
| paper1_73_baseline_pivot | rar_mcgaugh | 14 | 14 | 0.428571 |
| wide_fixed_tpg_proxy_ranks | FixedTPG | 58 | 58 | 0.241379 |
| wide_fixed_tpg_proxy_ranks | MOND | 57 | 57 | 0.596491 |
| wide_fixed_tpg_proxy_ranks | Newtonian | 8 | 8 | 0.125 |
| wide_fixed_tpg_proxy_ranks | RAR | 20 | 20 | 0.4 |

## Interpretation

In the current holdout split, TPG/v6 success is concentrated in
scale-tail/irregular rows with low current-vs-readout agreement. Tau Core
language reads this as a possible smooth closure-like or memory-integrated
readout regime rather than a direct present-day morphology match.

MOND success is more compatible with simple radial/low-acceleration or
diffuse-disk effective scaling regimes. Newtonian success, where visible
in the smaller conventional tables, should be interpreted as a quiet or
regular baryonic-readout regime, not as evidence against morphology
specificity in other regimes.

The next scientific step is to predeclare these success zones as controls:
regular/current-readout-consistent galaxies should not require a strong
Tau residual, while memory/projection/tail cases should be tested with
source-native readout-state observables.

Claim boundary: `baseline_success_morphology_audit_not_endpoint_not_validation`.
