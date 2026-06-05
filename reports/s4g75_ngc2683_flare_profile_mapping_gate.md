# NGC2683 Flare-Profile Mapping Gate

This gate maps the source-native NGC2683 HI flare profile onto the rotation-curve radii without using endpoint residuals. It does not authorize endpoint scoring.

## Source Profile

Source: Vollmer_Nehlig_Ibata_2016_NGC2683_HI_flare, https://arxiv.org/abs/1512.07058.

The source profile used here is:

```text
H(R) = 0.5 kpc for the inner representative region before R = 9 kpc
H(R) rises exponentially from 0.5 kpc at R = 9 kpc to 4 kpc at R = 15 kpc
H(R) remains 4 kpc until R = 22 kpc
after R = 22 kpc the source says the flare decreases but does not provide a single executable formula
outer ring vertical offset = 1.3 kpc
```

## Verdict

Rotation points checked: 11.
Profile-mapped points: 7.
Unmapped post-saturation points: 4.

The direct profile is stronger than the old scalar proxy, but it is not yet an endpoint override. The missing step is a residual-blind profile-to-thick/flared-kernel readout rule.

## Summary

| galaxy | n_rotation_points | n_profile_mapped_points | n_unmapped_post_saturation_points | scale_radius_kpc | current_scalar_h_over_rs_proxy | mapped_profile_h_over_rs_min | mapped_profile_h_over_rs_median | mapped_profile_h_over_rs_max | profile_exponential_scale_kpc | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC2683 | 11 | 7 | 4 | 2.20965 | 0.202408 | 0.226281 | 0.545702 | 1.81024 | 2.88539 | False | False | s4g75_ngc2683_flare_profile_mapping_gate_not_endpoint |

## Point-Level Mapping

| radius_kpc | current_scalar_h_over_rs_proxy | flare_height_kpc | flare_h_over_rs_profile | mapping_region | mapping_status |
| --- | --- | --- | --- | --- | --- |
| 2.89 | 0.202408 | 0.5 | 0.226281 | INNER_THIN_DISK_HEIGHT_REPRESENTATIVE | PROFILE_MAPPED |
| 5.77 | 0.202408 | 0.5 | 0.226281 | INNER_THIN_DISK_HEIGHT_REPRESENTATIVE | PROFILE_MAPPED |
| 8.66 | 0.202408 | 0.5 | 0.226281 | INNER_THIN_DISK_HEIGHT_REPRESENTATIVE | PROFILE_MAPPED |
| 11.54 | 0.202408 | 1.20581 | 0.545702 | EXPONENTIAL_FLARE_RISE | PROFILE_MAPPED |
| 14.43 | 0.202408 | 3.28297 | 1.48574 | EXPONENTIAL_FLARE_RISE | PROFILE_MAPPED |
| 17.31 | 0.202408 | 4 | 1.81024 | SATURATED_FLARE_PLATEAU | PROFILE_MAPPED |
| 20.2 | 0.202408 | 4 | 1.81024 | SATURATED_FLARE_PLATEAU | PROFILE_MAPPED |
| 23.08 | 0.202408 | nan | nan | POST_SATURATION_DECREASE_UNSPECIFIED | MAPPING_REQUIRED_AFTER_22_KPC |
| 28.85 | 0.202408 | nan | nan | POST_SATURATION_DECREASE_UNSPECIFIED | MAPPING_REQUIRED_AFTER_22_KPC |
| 31.74 | 0.202408 | nan | nan | POST_SATURATION_DECREASE_UNSPECIFIED | MAPPING_REQUIRED_AFTER_22_KPC |
| 34.62 | 0.202408 | nan | nan | POST_SATURATION_DECREASE_UNSPECIFIED | MAPPING_REQUIRED_AFTER_22_KPC |

## Claim Boundary

The NGC2683 literature source provides a direct flare profile. This pass does not convert it into an accepted scalar h/Rs value and does not score an endpoint. Radii beyond 22 kpc remain unmapped because the source states a decrease but does not provide a unique executable post-saturation profile.
