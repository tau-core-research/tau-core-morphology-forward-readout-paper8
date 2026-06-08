# Accepted Morphology Manifest Audit

This audit inspects the partial accepted morphology manifest without running
endpoint scores. It separates field-level source acceptance, external
family-label support candidates, and remaining endpoint blockers.

## Verdict

The closest near-term lane is the exponential-disk family-label audit pool:
14 rows have an accepted S4G/SPARC scale radius and no missing
kernel field beyond the external family-label audit. These rows are not
endpoint-ready; they are the next audit pool.

## Audit Lanes

| audit_lane | n_rows |
| --- | --- |
| NEAR_TERM_EXPONENTIAL_DISK_FAMILY_LABEL_AUDIT_POOL | 14 |
| NO_S4G_MATCH_EXTERNAL_SOURCE_NEEDED | 97 |
| PARTIAL_SCALE_READY_KERNEL_BLOCKED | 62 |
| S4G_MATCHED_BUT_NO_ACCEPTED_SCALE | 2 |

## S4G Component Support

| s4g_component_support_status | n_rows |
| --- | --- |
| NO_ACCEPTED_SCALE_TO_AUDIT | 99 |
| S4G_EDGEDISK_SUPPORT_CAVEATED | 9 |
| S4G_EXPDISK_SUPPORT | 48 |
| S4G_EXPDISK_WITH_BAR_CAVEAT | 19 |

## Family/Lane Summary

| formula_family | audit_lane | n_rows | n_accepted_scale | n_s4g_matched |
| --- | --- | --- | --- | --- |
| K_compact_finite | NO_S4G_MATCH_EXTERNAL_SOURCE_NEEDED | 21 | 0 | 0 |
| K_compact_finite | PARTIAL_SCALE_READY_KERNEL_BLOCKED | 7 | 7 | 7 |
| K_compact_finite | S4G_MATCHED_BUT_NO_ACCEPTED_SCALE | 1 | 0 | 1 |
| K_exponential_disk | NEAR_TERM_EXPONENTIAL_DISK_FAMILY_LABEL_AUDIT_POOL | 14 | 14 | 14 |
| K_exponential_disk | NO_S4G_MATCH_EXTERNAL_SOURCE_NEEDED | 17 | 0 | 0 |
| K_exponential_disk | S4G_MATCHED_BUT_NO_ACCEPTED_SCALE | 1 | 0 | 1 |
| K_scale_tail_spiral | NO_S4G_MATCH_EXTERNAL_SOURCE_NEEDED | 50 | 0 | 0 |
| K_scale_tail_spiral | PARTIAL_SCALE_READY_KERNEL_BLOCKED | 30 | 30 | 30 |
| K_thick_flared | NO_S4G_MATCH_EXTERNAL_SOURCE_NEEDED | 9 | 0 | 0 |
| K_thick_flared | PARTIAL_SCALE_READY_KERNEL_BLOCKED | 25 | 25 | 25 |

## Near-Term Exponential-Disk Audit Pool

| galaxy | scale_radius_kpc | s4g_disk_component_source | s4g_model_components | manifest_caveat | s4g_component_support_status |
| --- | --- | --- | --- | --- | --- |
| NGC4183 | 2.5281069868391675 | Z:edgedisk_hr2 | Z | none | S4G_EDGEDISK_SUPPORT_CAVEATED |
| NGC0100 | 1.2193294483812045 | Z:edgedisk_hr2 | Z | large_distance_error | S4G_EDGEDISK_SUPPORT_CAVEATED |
| NGC0247 | 4.0018082876406345 | D:expdisk_hr3 | D;BAR | none | S4G_EXPDISK_WITH_BAR_CAVEAT |
| NGC0300 | 1.534398989732565 | D:expdisk_hr3 | D | none | S4G_EXPDISK_SUPPORT |
| NGC3917 | 3.360628171466791 | D:expdisk_hr3 | B;D | none | S4G_EXPDISK_SUPPORT |
| NGC4010 | 2.301214530367252 | Z:edgedisk_hr2 | Z | none | S4G_EDGEDISK_SUPPORT_CAVEATED |
| NGC4559 | 2.1554796680624935 | D:expdisk_hr3 | D;BAR;N | large_distance_error | S4G_EXPDISK_WITH_BAR_CAVEAT |
| NGC5585 | 1.5577077456186188 | D:expdisk_hr3 | B;D | large_distance_error | S4G_EXPDISK_SUPPORT |
| NGC6015 | 2.7626597230842966 | D:expdisk_hr3 | D;N | large_distance_error | S4G_EXPDISK_SUPPORT |
| NGC6503 | 0.899249968469682 | D:expdisk_hr3 | D;N | none | S4G_EXPDISK_SUPPORT |
| NGC7793 | 1.3135069498792606 | D:expdisk_hr3 | D;N | none | S4G_EXPDISK_SUPPORT |
| UGC06930 | 2.6808231529361786 | D:expdisk_hr3 | D;BAR | low_inclination | S4G_EXPDISK_WITH_BAR_CAVEAT |
| UGC07089 | 1.498363762021143 | Z:edgedisk_hr2 | Z | none | S4G_EDGEDISK_SUPPORT_CAVEATED |
| UGC08286 | 1.204106339170835 | Z:edgedisk_hr2 | Z | none | S4G_EDGEDISK_SUPPORT_CAVEATED |

## Claim Boundary

This audit is not an endpoint score and not a validation of Tau Core. It does
not promote proxy family labels into accepted labels.
This audit does not promote proxy family labels. It identifies which
rows should be audited next using external residual-blind morphology support.
