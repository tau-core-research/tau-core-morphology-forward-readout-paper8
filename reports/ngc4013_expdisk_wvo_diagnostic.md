# NGC4013 Exponential-Disk + Warp/Vertical-Overlay Diagnostic

This diagnostic applies the already frozen NGC4013 overlay kernel to the
exponential-disk carrier. It is not an accepted endpoint because the mixed
carrier was motivated by the wrong-family control audit.

## Scores

| galaxy | n_points | rmse_newton | rmse_tpg_v6 | rmse_mond | rmse_exponential_disk | rmse_warp_vertical_overlay | rmse_expdisk_wvo_diagnostic | mixed_minus_expdisk | mixed_minus_wvo | mixed_minus_tpg_v6 | formula_id | overlay_formula_id | diagnostic_status | endpoint_scores_allowed | diagnostic_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | 36 | 65.6913 | 12.2739 | 14.3342 | 10.8802 | 11.4505 | 10.6148 | -0.265449 | -0.835737 | -1.65915 | NGC4013_EXPDISK_WVO_DIAGNOSTIC_V1 | NGC4013_WARP_VERTICAL_OVERLAY_V1 | DIAGNOSTIC_ONLY_NOT_ENDPOINT | False | True | ngc4013_expdisk_warp_vertical_overlay_diagnostic_not_endpoint |

## Claim Boundary

This is a diagnostic hypothesis test. It can motivate a future residual-blind
mixed-readout source rule, but cannot validate or promote the mixed family.

## Figure

paper8_submission_source/figures/fig08_ngc4013_expdisk_wvo_diagnostic.png
