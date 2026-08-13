# GHASP-SPARC Source-Only Candidate Federation v0.1

**Status:** `GHASP_FULL_FEDERATION_SOURCE_ONLY_CANDIDATES_RANKED_NOT_ENDPOINT`

GHASP VI and VII jointly expose 9713 side-labelled Halpha rotation
points in 175 release-specific curves for 173
distinct galaxies. UGC3382 and UGC11300 occur in both releases and both
provenance rows are retained. Alias-aware matching through the
203-object GHASP identity table yields 26 SPARC overlaps;
25 have both Halpha sides and
21 have an exact public WHISP overview
entry. The earlier exact-primary-name match found only one overlap because it
missed UGC/NGC aliases.

## Blind source ranking

| rank | galaxy | Halpha points | approaching / receding | max R / D25 | WHISP page | inclination | score |
| ---: | --- | ---: | ---: | ---: | --- | ---: | ---: |
| 1 | NGC3726 | 190 | 85 / 105 | 0.99 | True | 53 | 19 |
| 2 | NGC4559 | 175 | 80 / 95 | 0.67 | True | 67 | 18 |
| 3 | NGC3893 | 76 | 37 / 39 | 1.24 | True | 49 | 18 |
| 4 | UGC08490 | 76 | 31 / 45 | 0.83 | True | 50 | 18 |
| 5 | UGC04305 | 79 | 24 / 55 | 1.14 | True | 40 | 17 |
| 6 | UGC11914 | 77 | 35 / 42 | 0.70 | True | 31 | 17 |
| 7 | UGC07323 | 72 | 36 / 36 | 1.22 | True | 47 | 17 |
| 8 | UGC02455 | 55 | 25 / 30 | 1.21 | True | 51 | 17 |
| 9 | NGC5985 | 50 | 16 / 34 | 1.05 | True | 60 | 16 |
| 15 | UGC11557 | 46 | 23 / 23 | 1.11 | True | 30 | 14 |

The ranking uses only source availability, side balance, angular radial
coverage, and quoted geometry/uncertainty fields. It does not use SPARC
`vobs`, rotation residuals, required channel amplitudes, or baseline model
scores. The first acquisition target is **NGC3726**; this is a
data-quality choice, not a physical result.

No row is yet a common-coordinate H I-Halpha observable. Direct source-native
H I products, WCS/center transport, beam matching, uncertainty covariance, and
the channel statistic must be frozen before any endpoint access.
