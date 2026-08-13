# NGC4254 Common H I Resolution Source Cube v03

**Status:** `COMMON_HI_RESOLUTION_SOURCE_CUBE_BUILT_APPROXIMATE_NOT_ENDPOINT_READY`

**Claim boundary:** source-only beam-matched morphology input with explicit stellar-PSF limitation; not a complete noise covariance, physical FFL response, channel detection, or endpoint score.

The stellar and CO-derived surface-density fields are now convolved on the
common VIVA grid to the exact elliptical H I CLEAN beam
`37.703 x 32.946` arcsec at PA
`42.40` degrees. H I is retained at its native target beam. The
CO matching kernel subtracts its recorded circular `1.781` arcsec
native beam in Gaussian covariance space.

The supplied stellar FITS header contains no native PSF. The primary therefore
uses the explicit approximation that it is negligible compared with the H I
beam, while 0, 2, and 4 arcsec circular native-PSF controls are frozen for the
downstream sensitivity pass. This is a declared systematic limitation, not an
estimated error distribution.

The common mask contains `1758` pixels. Normalized
convolution requires at least `0.5` kernel support, but no
moment0 uncertainty maps or calibration covariance are present. The product is
therefore suitable for a beam-matched source-shape sensitivity calculation,
not for a complete covariance or endpoint significance claim.
