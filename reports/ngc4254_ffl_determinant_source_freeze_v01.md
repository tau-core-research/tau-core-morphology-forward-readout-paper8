# NGC4254 Source-Only FFL Determinant Proxy Freeze v01

**Status:** `SOURCE_ONLY_FFL_DETERMINANT_PROXY_FROZEN_NOT_ENDPOINT_READY`

**Claim boundary:** source-only four-role inverse proxy; not a parent role identification, physical channel/time/quantum signal, dark-matter replacement, or endpoint score.

## Purpose

This freeze asks only whether one endpoint-unread, four-role 4D inverse chart
can instantiate the determinant contraction before any terminal score. It does
not identify the parent role chart or infer the morphological body from a
readout. The formula and map extraction are blind to velocity pixels, but the
inherited center/PA/inclination values have a prior Halpha-kinematic provenance.

## Frozen Construction

- Four roles: the four deprojected disk quadrants fixed by the source-frozen
  center, position angle, and inclination.
- `u_OS`: centered quadrant medians of `sin(i) sin(theta)`, a geometry-only
  observer-source path proxy.
- `v_M`: centered log quadrant medians of stellar surface density, a
  stabilized-body shape proxy.
- `eta_shape`: centered log quadrant medians of `Sigma_H2 + Sigma_HI`, a
  source-side third-shape proxy.
- Radial windows: the already frozen 5--65 arcsec annuli. No annulus was added,
  removed, or moved using a velocity endpoint.
- Relative space: the fixed oriented orthonormal basis of
  `E_S = 1^perp subset R^4` recorded in the JSON manifest.

For each annulus the recorded scalar is

```text
q_shape_proxy = det(u_OS, v_M, eta_shape) / ||u_OS x v_M||.
```

`Delta_uv = ||u_OS x v_M||/(||u_OS|| ||v_M||)` is reported as a conditioning
diagnostic only. No conditioning threshold selects the rows.

## Frozen Rows

| annulus (arcsec) | quadrant pixels | Delta_uv | q_shape proxy | gas-shape fraction in span(u,v) |
|---:|---:|---:|---:|---:|
| 5-15 | 6/6/4/5 | 0.880629 | +0.172982 | 0.919814 |
| 15-25 | 8/8/12/11 | 0.947815 | -0.158442 | 0.985763 |
| 25-35 | 16/17/16/17 | 0.981110 | +0.225833 | 0.903217 |
| 35-45 | 20/20/17/19 | 0.837151 | +0.208527 | 0.574865 |
| 45-55 | 27/26/28/29 | 0.983490 | -0.224387 | 0.900679 |
| 55-65 | 31/32/32/30 | 0.524360 | -0.438272 | 0.788580 |

## Provenance And Leakage Boundary

- Geometry input SHA-256: `1cb01af987064014f3ae30285c72d854dffac0f9f8966729a8ca8b3bfc00f29e`
- Surface-density input SHA-256: `1ec5ac541ca9f9284b182566362eb47eae72c491a1c80df933e0520dd7c763a1`
- Velocity, rotation-curve, fitted-residual, and dark-discrepancy inputs read:
  **none**.
- The inherited geometry is source-frozen but was originally obtained from a
  PHANGS Halpha kinematic geometry. A later Halpha endpoint therefore requires
  an independently sourced morphology geometry or an explicit dependence
  control; a distinct held-out tracer remains another option.
- The surface-density file uses fixed stellar, CO-to-H2, and HI conversions;
  those assumptions are inherited rather than fitted here.

## What This Does Not Establish

The quadrant chart is a 4D inverse candidate, not a physical identification of
the parent roles. `eta_shape` is not yet the physical FFL terminal load, and
the missing `kappa_X/kappa_Y` normalization prevents a physical amplitude or
time-readout prediction. The approximately 37 arcsec HI beam also correlates
the narrower radial annuli, so the rows are not independent observations.

The freeze therefore establishes source-side computability only. It reports no
channel detection, no time or quantum signal, no dark-matter replacement, and
no endpoint validation.
