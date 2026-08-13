# UGC06787 WHISP H I Source Acquisition v0.1

**Status:** `WHISP_UGC06787_GRAPHICAL_HI_VELOCITY_FIELD_ACQUIRED_FITS_OPEN`

The public WHISP object page, graphical overview, and observation/reduction
notes are cached with SHA-256 provenance. The `791 x 1024` overview contains
total-H I and intensity-weighted velocity fields at full, 30 arcsec, and
60 arcsec resolution, plus a global profile and major-axis position-velocity
diagram.

## Observation Metadata

| field | value |
| --- | ---: |
| quality | reasonable |
| bandwidth | 4.96 MHz |
| channels | 127 |
| central velocity | 1176.0 km/s |
| channel separation | 8.27 km/s |
| full-resolution beam | 13.8 x 12.6 arcsec |
| cleaned-map rms | 0.63 mJy/beam |

## Product Boundary

No direct FITS or cube link is present on the public object page. The graphical
velocity fields are source-native and sufficient for a declared coarse
digitization preflight, but they are not a calibrated source-coordinate cube
and cannot yet define a physical `A_p` row.

Next finite action: freeze the overview panel geometry and color-to-velocity
legend, digitize the 60 arcsec field with an explicit quantization error, and
compare only source-side radial support/side coverage with the GHASP Halpha
points. Endpoint residuals remain closed.
