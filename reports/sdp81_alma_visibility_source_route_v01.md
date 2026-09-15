# SDP.81 ALMA visibility source route v01

Status: `RAW_VISIBILITY_SOURCE_ROUTE_IDENTIFIED_ACQUISITION_NOT_EXECUTED`. Checks: `9/9`. Endpoint authorized: `False`.

The official ALMA archive manifest and calibration-script bundles separate 12 Band-4 CO(5-4) executions and 9 Band-6 CO(8-7) executions from 11 forbidden Band-7 CO(10-9) executions. The allowed raw ASDM payload is 211.709 GB. No Band-7 science package, FITS header, or pixel was opened.

This supplies a concrete endpoint-independent route to the missing source-plane spectral information, but does not supply the reconstruction itself. The next step is an authorized Band-4/Band-6-only download, official calibration, and visibility-plane source inversion with covariance and stability tests.

Claim boundary: This freezes a public, endpoint-independent acquisition route and proves Band-4/Band-6/Band-7 execution separation at the archive-manifest level. It is not a source-cube reconstruction, does not select a physical CO(10-9) profile law, does not increase transition readiness, and does not authorize or score the held-out endpoint.
