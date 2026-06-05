# S4G75 Promoted Kernel-Observable Fill

This table keeps the original filled-kernel candidates as a control and overrides only rows where S4G Table 7 supplies a direct source-native kernel measurement. It is not an endpoint result.

## Verdict

Rows with direct kernel overrides: 2.

## Override Rows

| galaxy | formula_family | promotion_override_source | promotion_override_previous_value | promotion_override_new_value | compact_support_radius_kpc | thickness_h_over_rs |
| --- | --- | --- | --- | --- | --- | --- |
| NGC5985 | K_compact_finite | B:sersic_Re | 10.71 | 0.735239339935394 | 0.735239 | nan |
| NGC5907 | K_thick_flared | Z:edgedisk_hz2_over_hr2 | 0.22 | 0.1733207190160832 | nan | 0.173321 |

## Summary

| formula_family | promotion_override_status | compact_observable_status | thickness_observable_status | tail_observable_status | n_galaxies | galaxies | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| K_compact_finite | DIRECT_KERNEL_MEASUREMENT_OVERRIDE | DIRECT_S4G_BULGE_RE_READY | NOT_APPLICABLE | NOT_APPLICABLE | 1 | NGC5985 | s4g75_promoted_kernel_observable_fill_not_endpoint |
| K_scale_tail_spiral | NO_DIRECT_KERNEL_OVERRIDE | NOT_APPLICABLE | NOT_APPLICABLE | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | 6 | UGC00891;UGC04499;NGC4214;UGC05829;UGC06917;UGC06983 | s4g75_promoted_kernel_observable_fill_not_endpoint |
| K_thick_flared | DIRECT_KERNEL_MEASUREMENT_OVERRIDE | NOT_APPLICABLE | DIRECT_S4G_EDGEDISK_HZ_HR_READY | NOT_APPLICABLE | 1 | NGC5907 | s4g75_promoted_kernel_observable_fill_not_endpoint |
| K_thick_flared | NO_DIRECT_KERNEL_OVERRIDE | NOT_APPLICABLE | SOURCE_CONSTRAINED_FORMULA_CANDIDATE | NOT_APPLICABLE | 7 | NGC0024;NGC2683;NGC3726;NGC3949;NGC3972;NGC4088;NGC4389 | s4g75_promoted_kernel_observable_fill_not_endpoint |

## Claim Boundary

Only direct S4G Table 7 kernel measurements are promoted. Scale-tail RHI-only rows remain conditional because no direct outer-transition profile has been supplied.
