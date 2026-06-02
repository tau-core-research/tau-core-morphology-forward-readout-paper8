# Exponential-Disk Family-Label Audit

This audit strengthens the near-term exponential-disk pool using S4G
component decompositions only. It is residual-blind and does not compute
endpoint scores.

## Verdict

Audited near-term exponential-disk rows: 13.
Strict external expdisk support: 6.
Caveated external disk support: 7.

All audited rows retain an external disk-family support label, but only the
strict subset is proposed as the first narrow dry-run candidate lane. The
barred and edge-on rows remain useful support rows with caveats.

## Status Summary

| external_family_label_status | narrow_dry_run_lane | n_rows | mean_label_confidence | endpoint_scores_computed |
| --- | --- | --- | --- | --- |
| ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 3 | 0.85 | False |
| ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 4 | 0.85 | False |
| ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 6 | 1.0 | False |

## Audited Rows

| galaxy | external_family_label | external_family_label_status | external_family_label_confidence | external_family_label_caveat | narrow_dry_run_lane | scale_radius_kpc | s4g_name | s4g_disk_component_source | s4g_model_components | s4g_model_quality_values | inclination_deg | distance_frac_error | external_family_label_source | external_family_label_method | observable_provenance | residual_blind_certification | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0100 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | 0.85 | edgedisk_component_orientation_caveat;large_distance_error | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 1.2193294483812045 | NGC0100 | Z:edgedisk_hr2 | Z | 4.0 | 89.0 | 0.3 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| NGC0247 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR | 0.85 | bar_component_present | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 4.0018082876406345 | NGC0247 | D:expdisk_hr3 | D;BAR | 5.0 | 74.0 | 0.051351351351 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| NGC4010 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | 0.85 | edgedisk_component_orientation_caveat | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 2.301214530367252 | NGC4010 | Z:edgedisk_hr2 | Z | 4.0 | 89.0 | 0.138888888889 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| NGC4183 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | 0.85 | edgedisk_component_orientation_caveat | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 2.5281069868391675 | NGC4183 | Z:edgedisk_hr2 | Z | 4.0 | 82.0 | 0.138888888889 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| NGC4559 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR | 0.85 | bar_component_present;large_distance_error | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 2.1554796680624935 | NGC4559 | D:expdisk_hr3 | D;BAR;N | 5.0 | 67.0 | 0.3 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| UGC06930 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR | 0.85 | bar_component_present;low_inclination | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 2.6808231529361786 | UGC06930 | D:expdisk_hr3 | D;BAR | 5.0 | 32.0 | 0.138888888889 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| UGC07089 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | 0.85 | edgedisk_component_orientation_caveat | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 1.498363762021143 | UGC07089 | Z:edgedisk_hr2 | Z | 4.0 | 80.0 | 0.138888888889 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| NGC0300 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | 1.0 | none | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 1.534398989732565 | NGC0300 | D:expdisk_hr3 | D | 5.0 | 42.0 | 0.048076923077 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| NGC3917 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | 1.0 | none | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 3.360628171466791 | NGC3917 | D:expdisk_hr3 | B;D | 5.0 | 79.0 | 0.138888888889 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| NGC5585 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | 1.0 | large_distance_error | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 1.5577077456186188 | NGC5585 | D:expdisk_hr3 | B;D | 5.0 | 51.0 | 0.300283286119 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| NGC6015 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | 1.0 | large_distance_error | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 2.7626597230842966 | NGC6015 | D:expdisk_hr3 | D;N | 5.0 | 60.0 | 0.3 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| NGC6503 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | 1.0 | none | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 0.899249968469682 | NGC6503 | D:expdisk_hr3 | D;N | 5.0 | 74.0 | 0.049520766773 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |
| NGC7793 | K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | 1.0 | none | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 1.3135069498792606 | NGC7793 | D:expdisk_hr3 | D;N | 5.0 | 47.0 | 0.049861495845 | VizieR_J/ApJS/219/4_S4G_Pipeline4 | S4G component model contains expdisk or edgedisk decomposition component | SPARC_Lelli2016c.mrt;VizieR_J/ApJS/219/4_S4G_Pipeline4 | pre_endpoint_external_catalog_query | False | external_family_label_audit_not_endpoint_score_not_empirical_validation |

## Claim Boundary

This is not an endpoint score, not a claim that Tau Core fits these galaxies
better than baselines, and not a final Paper 8 result. It only promotes
the near-term family-label audit pool from proxy-label review to external
S4G-supported disk-family labels.
