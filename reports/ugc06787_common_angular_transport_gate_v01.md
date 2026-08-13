# UGC06787 Common Angular Transport Gate v0.1

**Status:** `UGC06787_ANGULAR_FIRST_TRANSPORT_RULE_FROZEN_WORLD_AXIS_CALIBRATION_OPEN`

Three source packets use materially different physical-distance conventions:

| source | distance or implied distance | kpc/arcsec |
| --- | ---: | ---: |
| GHASP native `r/r2` median | 18.902 Mpc | 0.091639 |
| WHISP overview | 16.000 Mpc | 0.077570 |
| SPARC master | 21.300 Mpc | 0.103265 |

The largest distance is `1.331` times
the smallest. A direct kpc merge would therefore create a scale mismatch that
could masquerade as a radial channel effect.

The transport rule is frozen as:

```text
GHASP native angular radius r2
<-> WHISP source-figure angular axes
first;

one declared distance conversion
only after angular support and geometry agree.
```

GHASP reaches `173.7` arcsec on its available approaching
side. The WHISP graphical panel still needs an explicit source-axis pixel to
sky calibration before common angular overlap can be computed.

No endpoint residual was opened. No physical `A_p` row is constructed.
