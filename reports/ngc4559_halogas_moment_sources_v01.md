# NGC4559 HALOGAS Moment Source Acquisition v0.1

**Status:** `NGC4559_HALOGAS_HR_LR_MOMENT0_MOMENT1_FITS_ACQUIRED_PIXELS_UNOPENED`

The source-only GHASP federation selected NGC4559 as rank 2 before any H I
pixel inspection. Four public HALOGAS Data Release 1 FITS products are cached
and verified against the archive MD5 values.

| product | FITS shape | unit | beam |
| --- | --- | --- | --- |
| NGC4559-HR_mom0m.fits | [1024, 1024] | JY/BEAM.km/s | 28.38 x 13.10 arcsec |
| NGC4559-HR_mom1m.fits | [1024, 1024] | km/s | 28.38 x 13.10 arcsec |
| NGC4559-LR_mom0m.fits | [1024, 1024] | JY/BEAM.km/s | 41.15 x 31.89 arcsec |
| NGC4559-LR_mom1m.fits | [1024, 1024] | km/s | 41.15 x 31.89 arcsec |

Only FITS headers were opened. Pixel values, SPARC velocities, residuals, and
model scores remain closed. The 415 MB HR/LR cubes were not downloaded because
the moment maps are sufficient to freeze a first WCS, center, beam, annulus,
and major-axis wedge extraction protocol.

Next gate: freeze that extraction protocol from source geometry before reading
the moment-map pixels, then apply the unchanged H I-Halpha odd-contrast
statistic used for NGC3726.
