# SDP.81 public reduced spectral-product audit v01

Status: `REDUCED_IMAGE_CUBES_CONFIRMED_NO_COMPACT_VISIBILITY_OR_SOURCE_CUBE_FOUND`. Endpoint authorized: `False`.

## Result

The official ALMA Datalink inventory for project `2011.0.00016.SV`, member OUS `uid://A002/X8fa7af/X12`, contains three endpoint-relevant product levels:

1. the allowed Band-4 and Band-6 raw ASDM executions, totaling 211,709,114,368 bytes;
2. official calibrated measurement-set packages totaling 54,009,047,808 bytes (`9,043,149,221` bytes for Band 4 and `44,965,898,587` bytes for Band 6);
3. reference-image packages totaling 1,599,101,806 bytes (`1,212,386,119` bytes for Band 4 and `386,715,687` bytes for Band 6).

The reference-package manifests were inspected without opening any Band-7 package. Band 4 contains an unsmoothed CO(5--4) cube, moment map, smoothed CO(5--4) cube, smoothed moment map and two continuum images. Band 6 contains a CO(8--7) cube, a continuum image and an H2O cube. The already-local allowed CO line cubes are:

- `SDP.81.Band4.CO_smooth_z3.042.fits`: 215,072,640 bytes, SHA-256 `b26f3e4cbff43bab9d6c4c082ff513788f9dcf20b2e640edf607dbc3fe34a656`;
- `SDP81_9exec.co87.R1uvtaper1000klambda.fits`: 180,855,360 bytes, SHA-256 `aeea985de1e590921a6282cdd9d017f0a888958e7e07b54d4d51435772475ea3`.

Together they are 395,928,000 bytes. They are restored image-plane spectral cubes, not calibrated visibilities or source-plane posterior cubes. The full-arc regularized inversion already tested this compact route and failed its frozen promotion threshold: 2.069% aggregate held-path median improvement versus 5%, with only 0.460 percentage points over the reflected-source control.

The Rybak et al. public source products contain velocity-integrated CO(5--4) and CO(8--7) maps and uncertainty maps, not spectral source cubes. No public compact product was found that simultaneously supplies channel-resolved source-plane emission and covariance/posterior draws, or target-and-line-only calibrated visibilities.

## Minimum admissible next acquisition

The smallest scientifically sufficient next object is therefore one of:

1. a source-plane CO(5--4) and CO(8--7) channel cube on a common velocity grid, plus covariance/posterior draws and the source-plane resolution operator; or
2. a target-only, line-SPW-only calibrated measurement-set cutout for both bands, with weights/flags and enough metadata to reproduce continuum subtraction.

The first route is preferred because it avoids a 54.009-GB transfer and preserves the authors' visibility-plane reconstruction likelihood. If neither compact object is supplied, the official calibrated packages are the smallest public visibility route presently identified. They are substantially smaller than the raw route but remain too large for the current resource-bounded iteration.

## Source request text

> We are performing an endpoint-blind reanalysis of the public SDP.81 CO(5--4) and CO(8--7) reference lines. Could you share either (a) the channel-resolved source-plane reconstructions on their native/common velocity grid, including covariance or posterior samples and the effective source-plane PSF/resolution operator, or (b) target-only, line-SPW-only calibrated measurement-set cutouts with weights, flags and continuum-subtraction metadata? We do not request or use the CO(10--9) data at this stage.

This text is a draft only; no message was sent.

## Claim boundary

This audit establishes the public product hierarchy and a 54.009-GB calibrated visibility alternative to the 211.709-GB raw route. It does not reconstruct a source cube, identify Nature's spectral response, increase transition readiness, authorize the CO(10--9) endpoint, or overturn the preserved negative restored-image result.
