# NGC925 signed source-geometry partial freeze v01

Status: `SOURCE_GEOMETRY_DIGITIZATION_COMPLETE_ENDPOINT_BLOCKED_PHYSICAL_UNCERTAINTY`.

The cached de Blok et al. (2008) EPS contains one 561 x 756 grayscale JPEG. The script extracts that raster directly, rather than digitizing a rescaled PDF screenshot. It uses the source Table 2 value `i=66.0 deg` and traces the thick adopted PA curve in Figure 68. The source definition makes PA the counter-clockwise sky angle from north to the receding major axis, so the approaching axis is fixed at `PA+180 deg` modulo 360 degrees.

The nominal 3-arcsec table contains `93` rings from `15` to `291` arcsec. Its mean digitized PA is `286.608 deg`, within `0.008 deg` of the independently printed mean `286.6 deg`. The adopted inclination curve is traced separately; its mean is `64.861 deg`, rather than incorrectly treating the printed `66.0 deg` summary as a constant radial law. A 486-member axis-anchor and path-smoothness ensemble supplies a raster sensitivity envelope; its largest PA and inclination 90% widths are `4.195 deg` and `7.771 deg`.

This envelope is not a physical uncertainty model. The paper does not supply a machine-readable ring covariance for the adopted geometry, and NGC925 has a bar, a reported inclination trend, and known tilted-ring degeneracy in its nearly solid-body region. Endpoint access therefore remains blocked until physical orientation uncertainty/covariance, centre alternatives, common footprint, beam blocks, solver tolerance, and wrong-family controls are frozen. No HALOGAS endpoint pixel is read by this script.
