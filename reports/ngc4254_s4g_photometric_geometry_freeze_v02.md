# NGC4254 S4G Photometric Geometry Freeze v02

**Status:** `SOURCE_ONLY_S4G_PHOTOMETRIC_GEOMETRY_FROZEN`

**Claim boundary:** velocity-independent photometric geometry freeze; not a parent role identity, channel/time signal, dynamical inclination proof, or endpoint score.

## Primary Geometry

The primary geometry is selected directly from the unique `Flag=ok` NGC4254
row in the local S4G global catalog:

| quantity | frozen value |
|---|---:|
| center RA | 184.70677000 deg |
| center Dec | 14.41649000 deg |
| photometric PA | 76.600 deg east of north |
| photometric PA uncertainty | 5.900 deg |
| ellipticity | 0.203000 |
| ellipticity uncertainty | 0.015000 |
| axis ratio | 0.797000 |
| thin-disk inclination | 37.155429 deg |
| outer-isophote range | 161--187 arcsec |

The inclination follows `i=acos(1-Ell)`. No velocity map, rotation curve,
fitted residual, or dark-discrepancy label is read.

The field meanings and units are those of the official S4G Pipeline 4
`galaxies` table. The published Table 1 gives the NGC4254 uncertainties used
below.

## Mandatory Controls

The catalog `PA +/- 5.9 deg` and `Ell +/- 0.015` controls are retained in
addition to the primary. The finite-thickness control with `q0=0.2` gives
`i=38.056176 deg`. The two S4G exponential-disk components
have `(PA,q,i)=(85.06,
0.813,
35.610)` and
`(53.80,
0.789,
37.908)`. They are retained
as source-side controls because NGC4254 is asymmetric; neither may be selected
or discarded using a terminal score.

## Comparison With The Retired Primary Geometry

The earlier kinematic geometry used `PA=68.100`
deg and `i=34.400 deg`. The new source-only primary
therefore changes PA by
`+8.500`
deg and inclination by
`+2.755`
deg. The old values remain a provenance comparison only.

The six radial windows are inherited unchanged from the earlier protocol,
whose freeze certifies that no velocity pixel was read. This removes
kinematic dependence from center/PA/inclination, but full endpoint readiness
still requires the mandatory photometric controls, beam covariance, and the
physical FFL source/gain construction.
