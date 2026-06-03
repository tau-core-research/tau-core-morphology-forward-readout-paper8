# Exponential-Disk Failure and Scale-Sensitivity Audit

This audit varies only the accepted S4G/SPARC scale radius multiplier
inside the exponential-disk Freeman/Bessel shell and uses a
leave-one-galaxy-out amplitude policy. It does not launch the frozen
endpoint.

## Verdict

The strict lane remains mixed under 0.75, 1.0, and 1.25 scale multipliers.
This points to a readout-normalization or morphology-subtype issue rather
than a simple single-scale correction.

## Strict-Lane Scale Sensitivity

| narrow_dry_run_lane | scale_multiplier | n_galaxies | mean_rmse_tau | mean_rmse_tpg_v6 | mean_rmse_mond | median_tau_minus_tpg_v6 | median_tau_minus_mond | beats_tpg_v6_fraction | beats_mond_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 0.75 | 6 | 8.73098443389106 | 8.558661162885608 | 6.954746714231061 | -0.0013433321248959018 | 1.7017000944246936 | 0.5 | 0.16666666666666666 |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 1.0 | 6 | 8.739932929821478 | 8.558661162885608 | 6.954746714231061 | -0.005777848728334867 | 1.7624461567943528 | 0.5 | 0.3333333333333333 |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 1.25 | 6 | 8.779006245442257 | 8.558661162885608 | 6.954746714231061 | 0.08855291331056092 | 1.8344063252799208 | 0.3333333333333333 | 0.3333333333333333 |

## Failure Classes at Scale Multiplier 1.0

| narrow_dry_run_lane | failure_class | n_galaxies |
| --- | --- | --- |
| CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | beats_both | 2 |
| CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | beats_mond_only | 4 |
| CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | beats_neither | 1 |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | beats_mond_only | 2 |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | beats_neither | 1 |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | beats_tpg_only | 3 |

## Best Multiplier Per Galaxy

| galaxy | narrow_dry_run_lane | scale_multiplier | failure_class | tau_minus_tpg_v6 | tau_minus_mond | external_family_label_caveat |
| --- | --- | --- | --- | --- | --- | --- |
| NGC0100 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 1.25 | beats_neither | 0.010126880141044126 | 1.486313334063718 | edgedisk_component_orientation_caveat;large_distance_error |
| NGC0247 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 0.75 | beats_both | -0.2851158360696724 | -1.8942214046741066 | bar_component_present |
| NGC4010 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 1.25 | beats_mond_only | 0.2797851752799403 | -0.7193666214820027 | edgedisk_component_orientation_caveat |
| NGC4183 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 0.75 | beats_both | -0.13104789452046628 | -3.9963479978130847 | edgedisk_component_orientation_caveat |
| NGC4559 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 1.0 | beats_mond_only | 1.1346701063243696 | -2.465322408165111 | bar_component_present;large_distance_error |
| UGC06930 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 0.75 | beats_mond_only | 0.038174384003861306 | -3.4472431251846585 | bar_component_present;low_inclination |
| UGC07089 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 1.25 | beats_mond_only | 0.341911767715148 | -2.913487569232373 | edgedisk_component_orientation_caveat |
| NGC0300 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 0.75 | beats_tpg_only | -0.23304706155357202 | 3.9918163441989645 | none |
| NGC3917 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 0.75 | beats_tpg_only | -0.21934587581439846 | 0.04260598909439128 | none |
| NGC5585 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 1.25 | beats_mond_only | 0.06278903180750106 | -0.3922873005299454 | large_distance_error |
| NGC6015 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 0.75 | beats_neither | 0.8985041457996434 | 3.5268398602574145 | large_distance_error |
| NGC6503 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 0.75 | beats_tpg_only | -0.029941537684318398 | 3.2679614393360055 | none |
| NGC7793 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 1.25 | beats_both | -6.44317675257966e-05 | -0.334555369642227 | none |

## Claim Boundary

This is a failure/sensitivity diagnostic, not an endpoint score and not a
validation of Tau Core. The scale multipliers are diagnostic probes, not
post-hoc selected formula parameters.
