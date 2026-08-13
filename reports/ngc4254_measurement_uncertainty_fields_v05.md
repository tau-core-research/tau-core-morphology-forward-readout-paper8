# NGC4254 Measurement-Uncertainty Fields v05

**Status:** `PARTIAL_MEASUREMENT_UNCERTAINTY_FIELDS_BUILT_HI_CONTROL_ONLY`

**Claim boundary:** source-only partial measurement uncertainty construction; not a complete covariance, physical FFL determinant, channel/time/quantum signal, dark-matter replacement, or endpoint score.

## Result

The PHANGS CO broad-moment error image now supplies an exact-grid molecular
measurement field.  The S4G stellar layer is a documented conditional
reconstruction from the P1 coverage maps, the NGC4254-specific P3 local and
large-scale sky noise, and the P5 two-component ICA colors.  Its pixel noise,
two sky modes, and two coherent ICA-color modes remain separate.

The public VIVA cube is robust-1 while the frozen H I moment-0 product records
robust-5 imaging.  Therefore `HI_CTL01`, `HI_CTL10`, and `HI_CTL49` are only
channel-count controls.  They are not an H I covariance estimate for the map
used by the morphology inverse.

## Field Scale

| extension | median (Msun/pc2) | p16 | p84 |
|---|---:|---:|---:|
| `STAR_PIX` | 4.15884 | 3.94244 | 4.41514 |
| `STAR_SKY1` | 5.01202 | 5.01202 | 5.01202 |
| `STAR_SKY2` | -5.74531 | -5.74531 | -5.74531 |
| `STAR_ICA1` | 6.78909 | 2.96061 | 21.3948 |
| `STAR_ICA2` | 5.92373 | 1.40057 | 18.2083 |
| `H2_IND` | 0.414593 | 0.340798 | 0.526237 |
| `H2_CORR` | 4.19471 | 3.23938 | 4.92426 |
| `HI_CTL01` | 0.0585043 | 0.0585043 | 0.0585043 |
| `HI_CTL10` | 0.215967 | 0.215967 | 0.215967 |
| `HI_CTL49` | 0.484959 | 0.484959 | 0.484959 |

## Validation

- Every field is finite on the retained uncertainty-common source mask; one of
  the 1758 inherited pixels is excluded because the exact CO error map has no
  finite matched uncertainty there.
- No velocity pixel, rotation curve, residual, or terminal endpoint enters the
  construction.
- A global stellar mass-to-light rescaling is deliberately omitted because it
  cancels exactly from the centered logarithmic stellar shape vector.
- The P5 stellar-plus-nonstellar reconstruction check has median fractional
  absolute mismatch
  `0.0626516`;
  this quantifies why the ICA modes remain conditional rather than exact P5
  covariance modes.

## Remaining Blocker

An exact H I contribution still requires the robust-5 parent cube or a released
pixel covariance/noise product for the frozen moment-0 image.  Until then the
combined covariance and endpoint scoring remain closed.
