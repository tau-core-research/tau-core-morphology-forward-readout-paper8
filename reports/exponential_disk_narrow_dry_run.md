# Exponential-Disk Narrow Dry-Run

This diagnostic runs the accepted-scale exponential-disk readout shell on the
S4G-supported exponential-disk audit pool. It is not the frozen Paper 8
endpoint, because the sample is tiny and two amplitude policies are
explicitly pool-fit diagnostics.
This diagnostic is not the frozen Paper 8 endpoint.

## Verdict

The calculation is now executable on the audited rows. Interpret it only as
a dry-run sanity check of the accepted-scale exponential-disk lane.

Strict-lane summary:

| narrow_dry_run_lane | amplitude_policy | n_galaxies | mean_rmse_tau | mean_rmse_tpg_v6 | mean_rmse_mond | median_tau_minus_tpg_v6 | median_tau_minus_mond | beats_tpg_v6_fraction | beats_mond_fraction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | frozen_global_train_beta | 6 | 9.014797448531171 | 8.558661162885608 | 6.954746714231061 | 0.5170424681910073 | 2.4479049324705 | 0.16666666666666666 | 0.3333333333333333 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | pool_fit_beta_all13 | 6 | 8.48501837017574 | 8.558661162885608 | 6.954746714231061 | -0.10413605155558026 | 1.2499749716233 | 0.6666666666666666 | 0.3333333333333333 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | pool_fit_beta_strict6 | 6 | 8.59881741978909 | 8.558661162885608 | 6.954746714231061 | 0.3660446454929054 | 1.660568948047994 | 0.5 | 0.16666666666666666 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |

## Amplitudes

| amplitude_policy | beta_delta_v2_amplitude | fit_scope | overfit_diagnostic |
| --- | --- | --- | --- |
| frozen_global_train_beta | -1003.8829388432548 | full Paper 8 train split from source-native formula preflight | False |
| pool_fit_beta_all13 | 218.093059057366 | all 13 audited exponential-disk rows | True |
| pool_fit_beta_strict6 | 3607.069971851181 | 6 strict S4G expdisk-supported rows | True |

## Summary

| narrow_dry_run_lane | amplitude_policy | n_galaxies | mean_rmse_tau | mean_rmse_tpg_v6 | mean_rmse_mond | median_tau_minus_tpg_v6 | median_tau_minus_mond | beats_tpg_v6_fraction | beats_mond_fraction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | frozen_global_train_beta | 7 | 8.854211096310156 | 9.008999864267581 | 11.200168489319273 | -0.23663795662571374 | -3.2946095028847893 | 0.5714285714285714 | 0.7142857142857143 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |
| CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | pool_fit_beta_all13 | 7 | 9.119403932434675 | 9.008999864267581 | 11.200168489319273 | 0.07717882376765406 | -2.9063374041763375 | 0.2857142857142857 | 0.8571428571428571 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |
| CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | pool_fit_beta_strict6 | 7 | 13.267357968074789 | 9.008999864267581 | 11.200168489319273 | 3.589803681845014 | 2.320378892973171 | 0.0 | 0.42857142857142855 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | frozen_global_train_beta | 6 | 9.014797448531171 | 8.558661162885608 | 6.954746714231061 | 0.5170424681910073 | 2.4479049324705 | 0.16666666666666666 | 0.3333333333333333 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | pool_fit_beta_all13 | 6 | 8.48501837017574 | 8.558661162885608 | 6.954746714231061 | -0.10413605155558026 | 1.2499749716233 | 0.6666666666666666 | 0.3333333333333333 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |
| STRICT_NARROW_DRY_RUN_READY_CANDIDATE | pool_fit_beta_strict6 | 6 | 8.59881741978909 | 8.558661162885608 | 6.954746714231061 | 0.3660446454929054 | 1.660568948047994 | 0.5 | 0.16666666666666666 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |
| ALL_13_AUDITED_EXPONENTIAL_DISK_SUPPORT | frozen_global_train_beta | 13 | 8.928327874258319 | 8.801151232860516 | 9.240743054663177 | 0.08302907340214549 | -0.25565194584695394 | 0.38461538461538464 | 0.5384615384615384 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |
| ALL_13_AUDITED_EXPONENTIAL_DISK_SUPPORT | pool_fit_beta_all13 | 13 | 8.826610596007473 | 8.801151232860516 | 9.240743054663177 | 0.003912743261314411 | -0.3305781946133868 | 0.46153846153846156 | 0.6153846153846154 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |
| ALL_13_AUDITED_EXPONENTIAL_DISK_SUPPORT | pool_fit_beta_strict6 | 13 | 11.112646945789082 | 8.801151232860516 | 9.240743054663177 | 2.17651663841726 | 1.850448501987584 | 0.23076923076923078 | 0.3076923076923077 | narrow_dry_run_diagnostic_not_frozen_endpoint_not_validation |

## Galaxy Scores

| galaxy | n_points | narrow_dry_run_lane | external_family_label_status | external_family_label_caveat | scale_radius_kpc | rmse_tpg_v6 | rmse_mond | rmse_tau_exp_disk_frozen_global_train_beta | tau_exp_disk_frozen_global_train_beta_minus_tpg_v6 | tau_exp_disk_frozen_global_train_beta_minus_mond | tau_exp_disk_frozen_global_train_beta_beats_tpg_v6 | tau_exp_disk_frozen_global_train_beta_beats_mond | rmse_tau_exp_disk_pool_fit_beta_all13 | tau_exp_disk_pool_fit_beta_all13_minus_tpg_v6 | tau_exp_disk_pool_fit_beta_all13_minus_mond | tau_exp_disk_pool_fit_beta_all13_beats_tpg_v6 | tau_exp_disk_pool_fit_beta_all13_beats_mond | rmse_tau_exp_disk_pool_fit_beta_strict6 | tau_exp_disk_pool_fit_beta_strict6_minus_tpg_v6 | tau_exp_disk_pool_fit_beta_strict6_minus_mond | tau_exp_disk_pool_fit_beta_strict6_beats_tpg_v6 | tau_exp_disk_pool_fit_beta_strict6_beats_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0100 | 21 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | edgedisk_component_orientation_caveat;large_distance_error | 1.2193294483812045 | 7.537919334963079 | 6.061732881040405 | 7.301281378337365 | -0.23663795662571374 | 1.2395484972969602 | True | False | 7.615098158730733 | 0.07717882376765406 | 1.553365277690328 | False | False | 9.631335079313578 | 2.093415744350499 | 3.5696021982731727 | False | False |
| NGC0247 | 26 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR | bar_component_present | 4.0018082876406345 | 3.866312004062215 | 5.475417572666649 | 6.298719315889417 | 2.432407311827202 | 0.8233017432227676 | False | False | 3.6880900816450497 | -0.1782219224171655 | -1.7873274910215997 | True | True | 11.951357157994702 | 8.085045153932487 | 6.475939585328052 | False | False |
| NGC4010 | 12 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | edgedisk_component_orientation_caveat | 2.301214530367252 | 10.799199499954586 | 11.798351296716529 | 9.585873701638993 | -1.2133257983155925 | -2.2124775950775355 | True | True | 11.077181967391306 | 0.27798246743672017 | -0.7211693293252228 | False | True | 15.721598708748099 | 4.922399208793513 | 3.9232474120315697 | False | False |
| NGC4183 | 23 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | edgedisk_component_orientation_caveat | 2.5281069868391675 | 6.489693491114096 | 10.354993594406714 | 6.841535878389914 | 0.35184238727581807 | -3.5134577160168003 | False | True | 6.47782197153882 | -0.011871519575276324 | -3.8771716228678947 | True | True | 8.666210129531356 | 2.17651663841726 | -1.6887834648753586 | False | True |
| NGC4559 | 32 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR | bar_component_present;large_distance_error | 2.1554796680624935 | 15.385306161864646 | 18.985298676354127 | 14.39749336852071 | -0.9878127933439362 | -4.587805307833417 | True | True | 15.601070876693633 | 0.21576471482898718 | -3.3842277996604935 | False | True | 18.97510984370966 | 3.589803681845014 | -0.010188832644466572 | False | True |
| UGC06930 | 10 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR | bar_component_present;low_inclination | 2.6808231529361786 | 7.129942401878801 | 10.615359911067321 | 7.320750408182532 | 0.19080800630373052 | -3.2946095028847893 | False | True | 7.172876382236344 | 0.042933980357543255 | -3.4424835288309765 | False | True | 10.495490471269793 | 3.365548069390992 | -0.11986943979752773 | False | True |
| UGC07089 | 12 | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | edgedisk_component_orientation_caveat | 1.498363762021143 | 11.854626156035648 | 15.11002549298317 | 10.233823623212158 | -1.6208025328234896 | -4.876201869771011 | True | True | 12.203688088806832 | 0.3490619327711837 | -2.9063374041763375 | False | True | 17.43040438595634 | 5.575778229920692 | 2.320378892973171 | False | False |
| NGC0300 | 25 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | none | 1.534398989732565 | 9.83189803567648 | 5.607034629923943 | 10.938448962424388 | 1.106550926747909 | 5.3314143325004455 | False | False | 9.612618299616006 | -0.21927973606047324 | 4.005583669692063 | True | False | 7.457483131911527 | -2.3744149037649525 | 1.850448501987584 | True | False |
| NGC3917 | 17 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | none | 3.360628171466791 | 6.899654025227952 | 6.637702160319162 | 8.152579974837693 | 1.2529259496097405 | 1.5148778145185302 | False | False | 6.707473292101533 | -0.1921807331264187 | 0.06977113178237104 | True | False | 8.108391554427566 | 1.208737529199614 | 1.4706893941084038 | False | False |
| NGC5585 | 24 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | large_distance_error | 1.5577077456186188 | 7.910184029247681 | 8.365260361585127 | 7.174600938353657 | -0.735583090894024 | -1.1906594232314704 | True | True | 8.090123271892335 | 0.17993924264465377 | -0.2751370896927927 | False | True | 11.380480522439045 | 3.4702964931913645 | 3.015220160853918 | False | False |
| NGC6015 | 44 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | large_distance_error | 2.7626597230842966 | 13.450865436024902 | 10.82252972156713 | 14.401921299004771 | 0.9510558629798691 | 3.57939157743764 | False | False | 13.25270853303136 | -0.19815690299354216 | 2.430178811464229 | True | False | 10.655094567833958 | -2.795770868190944 | -0.16743515373317308 | True | True |
| NGC6503 | 31 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | none | 0.899249968469682 | 7.537023161651215 | 4.239120184630891 | 7.62005223505336 | 0.08302907340214549 | 3.3809320504224694 | False | False | 7.520931791666473 | -0.01609136998474181 | 3.281811607035582 | True | False | 7.360905526154639 | -0.1761176354965759 | 3.121785341523748 | True | False |
| NGC7793 | 46 | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | none | 1.3135069498792606 | 5.722342289485416 | 6.0568332273601175 | 5.801181281513164 | 0.07883899202774725 | -0.25565194584695394 | False | True | 5.726255032746731 | 0.003912743261314411 | -0.3305781946133868 | False | True | 6.630549215967803 | 0.9082069264823867 | 0.5737159886076855 | False | False |

## Claim Boundary

This dry-run is not an endpoint score, not a validation of Tau Core, and not
a claim of superiority over MOND, RAR, TGP, or Newtonian baselines. The
pool-fit amplitudes are overfit diagnostics; the frozen-global amplitude is
the only non-pool-fit comparison in this report.
