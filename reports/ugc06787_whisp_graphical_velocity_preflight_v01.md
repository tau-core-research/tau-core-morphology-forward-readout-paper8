# UGC06787 WHISP Graphical Velocity Preflight v0.1

**Status:** `WHISP_UGC06787_60ARCSEC_GRAPHICAL_VELOCITY_DIGITIZED_WORLD_TRANSPORT_OPEN`

The frozen 60 arcsec intensity-weighted velocity panel was cropped at source
pixel box `(537, 542, 701, 694)`. Only exact printed palette colors in the largest
8-connected component were retained; this removes the separate plotted beam
marker and isolated graphical pixels. The
legend is represented by 50 km/s bins with `+/-25 km/s` graphical
quantization; anti-aliased pixels and black background are excluded.

| quantity | value |
| --- | ---: |
| exact palette pixels | 2511 |
| approaching pixels | 585 |
| receding pixels | 1586 |
| systemic-ambiguous pixels | 340 |
| approaching/receding centroid separation | 40.118 pixels |

Both H I velocity sides are present in the graphical product. The GHASP-SPARC
packet currently contains only approaching-side Halpha rows, so a symmetric
H I-Halpha parity comparison remains blocked.

This preflight does not supply WCS, a calibrated FITS velocity field, beam
covariance, or common H I-Halpha radial coordinates. It cannot be promoted to
a physical `A_p` row. The next admissible step is source-side world-coordinate
calibration of the panel axes or direct cube/FITS acquisition.
