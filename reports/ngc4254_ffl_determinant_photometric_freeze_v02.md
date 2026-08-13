# NGC4254 Photometric FFL Determinant Freeze v02

**Status:** `SOURCE_ONLY_PHOTOMETRIC_FFL_PROXY_WITH_BEAM_SCREEN_FROZEN_NOT_ENDPOINT_READY`

**Claim boundary:** source-only photometric determinant-shape proxy plus minimum HI-beam overlap screen; not physical q_det, a complete covariance, channel/time detection, or endpoint score.

## Result

The v02 primary uses only the S4G photometric center, PA, and thin-disk
inclination plus the existing stellar/H2/HI surface-density fields. It reads no
velocity field, rotation curve, fitted residual, or dark-discrepancy label.

| annulus (arcsec) | primary q_shape | primary Delta_uv | photometric q range | sign stable | min Delta_uv |
|---:|---:|---:|---:|:---:|---:|
| 5-15 | +0.358486 | 0.908998 | [+0.080331, +0.560962] | yes | 0.088712 |
| 15-25 | -0.149543 | 0.696761 | [-0.434389, +0.105434] | no | 0.552279 |
| 25-35 | +0.335164 | 0.990284 | [+0.147567, +0.542272] | yes | 0.345393 |
| 35-45 | +0.659141 | 0.959627 | [+0.224515, +0.788547] | yes | 0.925640 |
| 45-55 | -0.421177 | 0.998400 | [-0.421177, -0.254552] | yes | 0.987734 |
| 55-65 | -0.256363 | 0.999998 | [-0.532926, -0.066578] | yes | 0.343294 |

The four outer annuli from 25 to 65 arcsec retain the same sign under all eight
predeclared photometric variants: the S4G global primary, its published
`PA/Ell` one-sigma controls, the `q0=0.2` thickness control, and both S4G
exponential-disk component geometries. The 15--25 arcsec sign is not stable.
The innermost annulus reaches `Delta_uv=0.088712`
under one disk-component control and is therefore geometrically ill-conditioned
for that control. No threshold was used to remove it.

## Minimum H I Beam Screen

The VIVA FITS HISTORY records an elliptical CLEAN beam of
`37.703 x 32.946`
arcsec at PA `42.40` degrees.
Integrating its exact Gaussian autocorrelation over the six primary annulus
masks gives adjacent-bin
correlations

```text
0.969, 0.924, 0.910, 0.911, 0.906
```

and a participation effective rank of
`1.748` for six radial rows. The
six values are therefore not six independent radial measurements.

This matrix is only a minimum support-overlap screen. The determinant proxy
uses nonlinear quadrant medians and combines H I, CO, and stellar fields, so a
complete endpoint covariance must additionally propagate tracer beams,
calibration, geometry variants, and terminal measurement noise.

## Decision

The former Halpha-geometry dependence has been removed from the primary
center/PA/inclination. Source-side determinant computability survives, and the
outer sign pattern is photometrically stable. Physical amplitude and endpoint
authorization remain blocked: the parent role map, physical `eta`, primitive
curvatures, terminal gain, paired-side involution, and complete covariance are
not yet available. No channel, time, quantum, or dark-matter conclusion is
drawn.
