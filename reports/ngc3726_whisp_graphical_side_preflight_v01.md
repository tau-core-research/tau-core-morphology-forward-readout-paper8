# NGC3726 WHISP Graphical Side Preflight v0.1

**Status:** `NGC3726_HI_HALPHA_TWO_SIDE_SOURCE_SUPPORT_CONFIRMED_COMMON_TRANSPORT_OPEN`

The frozen 60-arcsec WHISP intensity-weighted velocity panel was cropped at
source pixel box `(537, 542, 701, 694)`. Exact palette pixels in the largest
8-connected component were retained. Red/orange/yellow and
light-blue/blue/purple provide robust opposite-side classes; both green
classes are deliberately left systemic-ambiguous.

| source support | approaching | receding | ambiguous |
| --- | ---: | ---: | ---: |
| WHISP graphical pixels | 1631 | 1916 | 641 |
| GHASP Halpha points | 85 | 105 | n/a |

Both tracers therefore have two-side source support. This removes the
UGC06787 single-Halpha-side blocker, but it does not yet compare the tracers:
the graphical H I panel lacks formal WCS/FITS transport, beam matching, and
uncertainty covariance. No physical `A_p` row or endpoint result is created.
