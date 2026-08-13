# NGC4254 FFL Source Systematics v03

**Status:** `BEAM_MATCHED_SOURCE_SYSTEMATICS_FROZEN_MEASUREMENT_COVARIANCE_NOT_IDENTIFIABLE`

**Claim boundary:** equal-weight source-systematic sensitivity ensemble and exact beam-overlap rank; not a probability model, complete measurement covariance, physical q_det, channel signal, or endpoint score.

The source-only proxy was recomputed after matching stellar and CO maps to the
exact VIVA H I beam. The finite ensemble crosses eight predeclared S4G
photometric geometries, three stellar native-PSF assumptions, and the inherited
0.7/1.0/1.3 molecular-conversion controls. No velocity, rotation curve,
residual, or dark-discrepancy value is read.

| annulus | unmatched q | matched q | all-systematic range | sign stable | min Delta_uv |
|---:|---:|---:|---:|:---:|---:|
| 5-15 | +0.358486 | -0.060291 | [-0.063737, +0.042259] | no | 0.168432 |
| 15-25 | -0.149543 | -0.036137 | [-0.050855, +0.053366] | no | 0.653372 |
| 25-35 | +0.335164 | +0.034726 | [-0.005856, +0.112592] | no | 0.720921 |
| 35-45 | +0.659141 | +0.024608 | [-0.014943, +0.070868] | no | 0.857116 |
| 45-55 | -0.421177 | -0.039956 | [-0.078753, +0.012365] | no | 0.877250 |
| 55-65 | -0.256363 | -0.099116 | [-0.144488, -0.049471] | yes | 0.657884 |

Beam matching changes the primary sign in radial indices
`[0]`. Across all 72 source
scenarios, only indices `[5]` retain a
fixed sign. The one-factor decomposition attributes the sign instability to
the photometric geometry ensemble: the stellar-PSF and H2-conversion controls
alone preserve every primary sign. A global stellar conversion factor cancels from the centered-log
body tangent to numerical precision (maximum q change
`1.367e-15`), so it is verified as an invariance rather
than counted repeatedly in the scenario covariance.

The equal-weight scenario covariance is an engineering sensitivity summary,
not a probability distribution. Separately, the exact H I beam-overlap matrix
has participation effective rank `1.748` for six radial
rows. With no moment0 error maps or calibration covariance and with nonlinear
quadrant medians, a complete q covariance is not identifiable from the
available products. A diagonal six-row likelihood is forbidden.

This closes beam matching and finite source-systematic propagation for the
proxy, but it does not authorize endpoint scoring. Physical `eta`, primitive
`kappa_X/kappa_Y`, terminal gain, role-to-probe identity, paired-side
involution, and an untouched side-resolved terminal remain open.
