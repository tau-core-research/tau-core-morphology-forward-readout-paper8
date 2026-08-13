# NGC4254 Partial Measurement Propagation v05

**Status:** `PARTIAL_MEASUREMENT_PROPAGATION_COMPLETE_HI_CONTROL_ONLY_NO_ENDPOINT`

**Claim boundary:** conditional source-only uncertainty propagation through a 4D inverse shape proxy; not a parent-role identification, complete covariance, channel/time/quantum signal, dark-matter replacement, or endpoint score.

## Primary Conditional Result

The source-only Monte Carlo propagates the reconstructed stellar measurement
modes and the exact PHANGS CO error-map field through the already frozen
four-quadrant inverse operator.  It does not read any rotation endpoint.

| annulus (arcsec) | baseline q | median q | 95% interval | P(baseline sign) | measurement/v03-systematic std |
|---:|---:|---:|---:|---:|---:|
| 5-15 | -0.06029 | -0.05975 | -0.06413, -0.05380 | 1.000 | 0.079 |
| 15-25 | -0.03614 | -0.03487 | -0.04482, -0.02631 | 1.000 | 0.153 |
| 25-35 | +0.03473 | +0.03361 | +0.02476, +0.04147 | 1.000 | 0.137 |
| 35-45 | +0.02461 | +0.02698 | +0.00461, +0.05108 | 0.980 | 0.530 |
| 45-55 | -0.03996 | -0.05159 | -0.13548, +0.14227 | 0.820 | 2.557 |
| 55-65 | -0.09912 | -0.09620 | -0.21903, +0.09132 | 0.855 | 2.954 |

Under this partial model, the annulus indices with at least 95% conditional
sign support are
`[0, 1, 2, 3]`.
The median ratio of measurement standard deviation to the earlier v03 source-
systematic standard deviation is
`0.3412`.
The one-pixel CO-uncertainty mask refinement shifts the matched v03 baseline by
at most
`4.77951e-14`.

CO measurement noise alone preserves the baseline sign in annuli
`[0, 1, 2, 3, 4, 5]`.
For the outer two annuli, the median ratio of stellar-only to combined
measurement standard deviation is
`1.0018`,
so their measurement instability is stellar-mode dominated in this model.

The earlier v03 source-systematic family preserves sign only in annuli
`[5]`.
No annulus currently passes both separate checks:
`[]`.
This is a robustness intersection, not a combined posterior probability.

## H I Control

The widest robust-1 control (`49` line channels) changes the annular standard
deviation by a median of
`+0.000654`.
This is only a sensitivity result: the robust-1 cube is not the parent of the
robust-5 H I moment map used in the inverse.

## Interpretation

This run measures whether known source-map uncertainty can erase or preserve
the inverse proxy.  It cannot identify a parent morphology, channel sector,
terminal time/quantum readout, or dark-matter alternative.  Geometry and source
model systematics from v03 remain part of the total uncertainty, and exact H I
covariance remains blocked.
