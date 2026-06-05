# NGC7331 THINGS H I Product Audit

This audit verifies that the cached THINGS NGC7331 H I moment maps are
readable and suitable as source-native inputs for a later residual-blind
q_warp/sign/cross-term worksheet. It does not measure q_warp and does
not score an endpoint.

## FITS Audit

| galaxy | product_id | audit_status | local_cache_path | shape | bunit | ctype1 | ctype2 | cdelt1 | cdelt2 | n_pixels | n_finite | finite_fraction | min_value | max_value | median_value | p95_value | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NA_MOM0 | PASS_FITS_READABLE | /Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/ngc7331_things_hi_route/NGC_7331_NA_MOM0_THINGS.FITS | 1x1x1024x1024 | JY/B*M/S | RA---SIN | DEC--SIN | -0.000416667 | 0.000416667 | 1048576 | 1048576 | 1 | -16.8522 | 258.243 | 0 | 7.2928 | False | False | ngc7331_things_hi_product_audit_not_endpoint |
| NGC7331 | NA_MOM1 | PASS_FITS_READABLE | /Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/ngc7331_things_hi_route/NGC_7331_NA_MOM1_THINGS.FITS | 1x1x1024x1024 | METR/SEC | RA---SIN | DEC--SIN | -0.000416667 | 0.000416667 | 1048576 | 103012 | 0.0982399 | 536011 | 1.13185e+06 | 777840 | 1.056e+06 | False | False | ngc7331_things_hi_product_audit_not_endpoint |
| NGC7331 | NA_MOM2 | PASS_FITS_READABLE | /Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/ngc7331_things_hi_route/NGC_7331_NA_MOM2_THINGS.FITS | 1x1x1024x1024 | METR/SEC | RA---SIN | DEC--SIN | -0.000416667 | 0.000416667 | 1048576 | 103012 | 0.0982399 | 0 | 273838 | 12946.1 | 37117.3 | False | False | ngc7331_things_hi_product_audit_not_endpoint |
| NGC7331 | RO_MOM0 | PASS_FITS_READABLE | /Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/ngc7331_things_hi_route/NGC_7331_RO_MOM0_THINGS.FITS | 1x1x1024x1024 | JY/B*M/S | RA---SIN | DEC--SIN | -0.000416667 | 0.000416667 | 1048576 | 1048576 | 1 | -72.7713 | 277.323 | 0 | 6.38255 | False | False | ngc7331_things_hi_product_audit_not_endpoint |
| NGC7331 | RO_MOM1 | PASS_FITS_READABLE | /Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/ngc7331_things_hi_route/NGC_7331_RO_MOM1_THINGS.FITS | 1x1x1024x1024 | METR/SEC | RA---SIN | DEC--SIN | -0.000416667 | 0.000416667 | 1048576 | 101607 | 0.0969 | 535721 | 1.13194e+06 | 780531 | 1.05803e+06 | False | False | ngc7331_things_hi_product_audit_not_endpoint |
| NGC7331 | RO_MOM2 | PASS_FITS_READABLE | /Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/ngc7331_things_hi_route/NGC_7331_RO_MOM2_THINGS.FITS | 1x1x1024x1024 | METR/SEC | RA---SIN | DEC--SIN | -0.000416667 | 0.000416667 | 1048576 | 101607 | 0.0969 | 0 | 341282 | 9925.1 | 42130.3 | False | False | ngc7331_things_hi_product_audit_not_endpoint |

## Summary

| galaxy | things_hi_product_audit_status | n_products_audited | n_readable | n_missing | worksheet_ready | q_warp_measurement_ready | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | population_claim_allowed | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_THINGS_HI_PRODUCTS_AUDITED_WORKSHEET_READY | 6 | 6 | 0 | True | False | False | False | False | False | build residual-blind map worksheet defining inner-disk reference, outer ridge mask, and side weights | ngc7331_things_hi_product_audit_not_endpoint |
