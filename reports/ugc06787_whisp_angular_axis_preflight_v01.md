# UGC06787 WHISP Angular-Axis Preflight v0.1

**Status:** `WHISP_UGC06787_SOURCE_AXIS_PROXY_CALIBRATED_CENTER_AND_WCS_OPEN`

Three printed B1950 major ticks on each axis were frozen with `+/-1` source
pixel reading uncertainty. Linear fits give:

```text
RA scale:  -1.015220 seconds-of-time / pixel
Dec scale: -0.140351 arcmin / pixel
```

The source graphic does not provide a machine-readable center. Two independent
source-only center proxies were therefore retained rather than choosing one
post hoc:

| center proxy | H I p50 radius | H I p95 radius | H I max radius |
| --- | ---: | ---: | ---: |
| systemic-color centroid | 187.41 | 433.00 | 498.74 |
| approaching/receding midpoint | 182.28 | 358.89 | 426.72 |

The GHASP approaching-side support reaches `173.7` arcsec and lies
inside both graphical H I maximum-radius estimates. This establishes possible
angular support overlap, not a pointwise common radial transport.

Formal WCS, a source-frozen galaxy center, beam covariance, and the mapping of
GHASP approaching-side radii onto the WHISP side remain open. No endpoint
residual was opened and no physical `A_p` row is constructed.
