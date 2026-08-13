# NGC4559 HALOGAS H I-Halpha Replication v0.1

**Status:** `NGC4559_HALOGAS_HI_HALPHA_REPLICATION_NOT_POSITIVE`

| map | radius arcsec | H I odd km/s | Halpha odd km/s | Delta odd km/s |
| --- | ---: | ---: | ---: | ---: |
| HR | 42 | -5.33 | 4.58 | 9.92 |
| HR | 84 | -11.61 | 2.20 | 13.80 |
| HR | 126 | -6.38 | -8.23 | -1.86 |
| HR | 168 | -3.16 | -8.63 | -5.48 |
| LR | 42 | -9.73 | 4.58 | 14.31 |
| LR | 84 | -11.70 | 2.20 | 13.90 |
| LR | 126 | -4.47 | -8.23 | -3.76 |
| LR | 168 | -2.85 | -8.63 | -5.78 |

| resolution | GLS contrast | zero-null p |
| --- | ---: | ---: |
| HR | 2.79 +/- 5.86 km/s | 0.1639 |
| LR | 0.89 +/- 5.97 km/s | 0.1362 |

HR/LR radius-wise sign agreement is `1.00`. Replication
gates: `{'zero_odd_contrast_rejected_in_hr': False, 'zero_odd_contrast_rejected_in_lr': False, 'gls_mean_sign_agreement': True, 'hr_lr_gls_mean_difference_within_2sigma': True, 'minimum_same_sign_radius_fraction': True}`. Overall positive status is `False`.

This prospective test used the frozen WCS geometry, rings, wedge, mask,
weighted median, block bootstrap, and unchanged NGC3726 odd contrast. It did
not use SPARC velocities/residuals or baseline scores. Regardless of the gate
result, no observer-channel detection or physical `A_p` row is claimed:
moment-1 bias from extraplanar/non-bulk gas, Halpha tracer structure, and full
cross-tracer covariance remain physical alternatives.
