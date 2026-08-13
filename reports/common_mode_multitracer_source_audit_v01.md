# Common-mode multitracer source audit v01

The conditional statistic is
`G_spec(R)=sqrt((1+z_plus)(1+z_minus))`. This audit does not evaluate it.

| role | galaxy | MUSE reference (km/s) | optical velocity layers | CO moment-1 |
| --- | --- | ---: | ---: | --- |
| primary | NGC4254 | 2387.790 | 4 | km.s-1 |
| replication | NGC3351 | 774.736 | 4 | km.s-1 |

Both local packets can reconstruct absolute velocities within each native
product. MUSE velocities are systemic-subtracted in BARYCENT; CO uses the
radio Doppler convention in LSRK. The source-derived convention and the
Astropy ICRS/LSRK direction transform are now frozen without fitting an offset.
NGC4254 is frozen as the first method preflight and NGC3351 as replication.
Pixel scoring remains closed until frame transport, WCS/PSF, geometry, radial
pairing, masks, velocity conventions, conventional baselines, and covariance
are frozen.

**Claim boundary:** source eligibility only; no common channel, effective
time readout, or Tau Core signal has been measured.
