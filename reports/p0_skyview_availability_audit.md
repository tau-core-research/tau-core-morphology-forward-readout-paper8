# P0 SkyView Availability Audit

This audit checks whether the P0 external imaging requests return at least
one SkyView image for DSS2 Red, 2MASS-K, and WISE W1. It does not download,
classify, or interpret images, and it does not write temporary SkyView FITS
URLs to disk.

## Availability Summary

| survey | n_galaxies | n_available | n_unavailable | median_image_count |
| --- | --- | --- | --- | --- |
| 2MASS-K | 4 | 4 | 0 | 1.0 |
| DSS2 Red | 4 | 4 | 0 | 1.0 |
| WISE 3.4 | 4 | 4 | 0 | 1.0 |

## Per-Request Availability

| galaxy | survey | suggested_fov_arcmin | skyview_image_count | availability_status | query_status |
| --- | --- | --- | --- | --- | --- |
| NGC0100 | DSS2 Red | 8.0 | 1 | AVAILABLE | QUERY_OK |
| NGC0100 | 2MASS-K | 8.0 | 1 | AVAILABLE | QUERY_OK |
| NGC0100 | WISE 3.4 | 8.0 | 1 | AVAILABLE | QUERY_OK |
| NGC0247 | DSS2 Red | 29.745 | 1 | AVAILABLE | QUERY_OK |
| NGC0247 | 2MASS-K | 29.745 | 1 | AVAILABLE | QUERY_OK |
| NGC0247 | WISE 3.4 | 29.745 | 1 | AVAILABLE | QUERY_OK |
| NGC0300 | DSS2 Red | 20.288 | 1 | AVAILABLE | QUERY_OK |
| NGC0300 | 2MASS-K | 20.288 | 1 | AVAILABLE | QUERY_OK |
| NGC0300 | WISE 3.4 | 20.288 | 1 | AVAILABLE | QUERY_OK |
| NGC6503 | DSS2 Red | 10.03 | 1 | AVAILABLE | QUERY_OK |
| NGC6503 | 2MASS-K | 10.03 | 1 | AVAILABLE | QUERY_OK |
| NGC6503 | WISE 3.4 | 10.03 | 1 | AVAILABLE | QUERY_OK |

## Claim Boundary

This is image-source availability only. It is not a morphology label, not
image-based validation, and not an endpoint score.

Claim boundary: `p0_skyview_availability_not_image_classification_not_endpoint`.
