# NGC3726 H I-Halpha Channel Preflight v0.1

**Status:** `NGC3726_TWO_TRACER_ODD_CONTRAST_NULL_NOT_REJECTED_PATTERN_DIAGNOSTIC`

The source-ranked, frozen six-radius comparison returns both published curves
to line-of-sight equivalents before forming the side-odd contrast.

| radius arcsec | Halpha odd km/s | H I odd km/s | Delta odd km/s |
| ---: | ---: | ---: | ---: |
| 40 | -16.76 | -15.97 | -0.79 |
| 60 | -21.63 | -9.58 | -12.04 |
| 80 | -8.91 | 1.60 | -10.50 |
| 100 | 12.19 | 12.78 | -0.59 |
| 120 | 28.00 | 13.58 | 14.43 |
| 140 | 26.99 | 8.78 | 18.20 |

The covariance-aware GLS mean is
`1.90 +/- 3.53 km/s`
(`z=0.54`). The zero-vector statistic is
`chi2=9.47` for `6`
degrees of freedom (`p=0.1489`). A constant contrast
is itself a poor description when its p-value is small; here the constant-fit
value is `p=0.1022`.

The six-radius odd pattern changes sign and the two tracer odd profiles are
strongly correlated (`r=0.886`). The
covariance-aware zero-contrast null is **not rejected**, and neither is a
constant contrast at the conventional 5% threshold. This is therefore a
pattern diagnostic and negative/indeterminate channel preflight, not evidence
for an observer/path channel. Beam smearing,
center and position-angle uncertainty, radial covariance, non-circular motion,
and phase-dependent H I/Halpha morphology are not yet in the covariance model.
No SPARC velocity, residual, MOND/RAR/RMOND/TPG score, or required Tau
amplitude was used.
