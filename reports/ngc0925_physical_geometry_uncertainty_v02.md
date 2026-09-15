# NGC925 physical geometry-uncertainty audit v02

Status: `PHYSICAL_MC_ACQUIRED_GEOMETRY_IDENTIFIABILITY_FAIL_ENDPOINT_BLOCKED`.

Schmidt et al. (2016) supply an independent THINGS tilted-ring analysis. Its Figure 19 is vector-valued, so the 15 inclination and 15 position-angle points and their vertical error bars are extracted from exact paths rather than raster pixels. The error bars are physical marginal standard deviations from 100 residual-rescrambling Monte Carlo fits; the authors checked convergence with runs as long as 2500 iterations. Cross-ring and joint inclination/position-angle covariance were not published.

The source itself declares the geometry inside 250 arcsec non-identifiable because the nearly solid-body rotation does not separate inclination from rotation speed. Consequently the inner error bars cannot repair or validate the earlier de Blok descriptor. Only the 270-arcsec Schmidt ring lies both in the source-claimed robust outer region and within the 15--291 arcsec de Blok extraction. There the inclination gap is `0.878 deg` (`1.23` Schmidt marginal MC sigmas), and the PA gap is `3.773 deg` (`2.91` such sigmas); the respective PA one-sigma intervals do not overlap. These ratios are not cross-source significances because the de Blok physical covariance and cross-source systematics are unavailable.

The correct preflight verdict is therefore not 'uncertainty closed'. NGC925 remains endpoint-blocked pending a prospectively frozen outer-only support test or demotion to a nonconfirmatory case. The paper's generic 5/10-arcsec centre-offset tests inform sensitivity bounds but do not supply source-specific centre alternatives or weights. No HALOGAS endpoint pixel is read.
