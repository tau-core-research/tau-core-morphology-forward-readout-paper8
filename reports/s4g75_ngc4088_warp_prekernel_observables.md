# NGC4088 Warp Pre-Kernel Observables

This report normalizes source-native NGC4088 warp/asymmetry evidence into dimensionless pre-kernel observables. It does not construct an endpoint closure-source kernel.

## Verdict

The WHISP HI diameter combined with the SPARC distance reconstructs the outer HI scale consistently with SPARC RHI. This supports a residual-blind normalization layer for a future warp/asymmetry readout. The radial warp profile and closure-source mapping remain missing.

## Observables

| observable | value | unit | source | interpretation |
| --- | --- | --- | --- | --- |
| R_HI_from_WHISP_diameter_kpc | 22.253 | kpc | Verheijen_Sancisi_2001_HI_diameter_x_SPARC_distance | source-native HI radial extent reconstructed from angular diameter |
| R_HI_over_SPARC_Rdisk | 8.62518 | dimensionless | WHISP_HI_diameter;SPARC_Rdisk | outer HI extent normalized by SPARC disk scale |
| R_HI_over_S4G_scale_radius | 6.83464 | dimensionless | WHISP_HI_diameter;S4G_scale_radius | outer HI extent normalized by S4G disk scale |
| WHISP_vs_SPARC_RHI_fractional_difference | 0.000133002 | dimensionless | WHISP_HI_diameter;SPARC_RHI | catalog consistency check, not a fitted parameter |
| qualitative_warp_asymmetry_score | 1 | dimensionless | Verheijen_Sancisi_2001_qualitative_flags | binary evidence score for formula development only |

## Summary

| galaxy | n_prekernel_observables | hi_radius_from_whisp_kpc | sparc_rhi_kpc | whisp_vs_sparc_rhi_fractional_difference | profile_kernel_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 5 | 22.253 | 22.25 | 0.000133002 | PREKERNEL_READY_PROFILE_KERNEL_BLOCKED | False | s4g75_ngc4088_warp_prekernel_observables_not_endpoint |

## Claim Boundary

These are pre-kernel observables for formula development. They are not accepted kernel observables and cannot be used for endpoint scoring until a residual-blind radial warp/asymmetry profile and mapping rule are supplied.
