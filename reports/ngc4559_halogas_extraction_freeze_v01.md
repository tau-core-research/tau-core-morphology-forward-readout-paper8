# NGC4559 HALOGAS Extraction Freeze v0.1

**Status:** `NGC4559_HALOGAS_PIXEL_EXTRACTION_AND_REPLICATION_RULE_FROZEN_PIXELS_UNOPENED`

The geometry is source-frozen from Barbieri et al. (2005): kinematic center
`12:35:58.0 +27:57:32`, `i=67.2 +/- 0.6 deg`, receding
`PA=323 +/- 1.4 deg`, and `v_sys=810 +/- 4 km/s`. GHASP gives
`i=69 +/- 3 deg`
and approaching `PA=143 +/- 2 deg`,
equivalent to the same receding axis.

Four non-overlapping common rings are frozen at `42, 84, 126, 168 arcsec`,
each `42 arcsec` wide. This width is set by the LR beam, not by velocity-map
features. Only pixels with `|cos(theta)|>=0.8`, finite masked moments, and
positive moment-0 support enter. The side estimator is an
`I_HI*|cos(theta)|`-weighted median of `(v_los-v_sys)/cos(theta)`.

HR is primary and LR is mandatory replication. Beam-sized block bootstrap
uses `2000` draws with seed `4559001`. A channel-positive
replication would require zero odd contrast to be rejected independently in
both resolutions, matching GLS signs, compatible GLS means, and at least 75%
radius-wise sign agreement.

No HALOGAS pixel, SPARC velocity/residual, cross-tracer contrast, baseline
score, or required Tau amplitude was opened while freezing this protocol.
