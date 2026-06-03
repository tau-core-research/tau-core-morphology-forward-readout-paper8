# P0 External Imaging Request Manifest

This manifest prepares residual-blind external image and catalogue review
for the four P0 morphology-inspection targets. It records coordinates,
recommended fields of view, and source URLs. It does not download, classify,
or interpret images.

## P0 Requests

| galaxy | ra_deg | dec_deg | suggested_fov_arcmin | inspection_focus | s4g_model_components |
| --- | --- | --- | --- | --- | --- |
| NGC0100 | 6.01182 | 16.48639 | 8.0 | edge_on_projection_degeneracy;outer_disk_tail_lsb_or_hi_extent | Z |
| NGC0247 | 11.78564 | -20.7604 | 29.745 | bar_m2_component;outer_disk_tail_lsb_or_hi_extent | D;BAR |
| NGC0300 | 13.72283 | -37.68438 | 20.288 | outer_disk_tail_lsb_or_hi_extent | D |
| NGC6503 | 267.36047 | 70.14434 | 10.03 | outer_disk_tail_lsb_or_hi_extent | D;N |

## Requested Source Summary

| source | n_requests | median_fov_arcmin |
| --- | --- | --- |
| deep_optical_or_ir_outer_disk_profile | 4 | 15.158999999999999 |
| hi_extent_or_asymmetry | 4 | 15.158999999999999 |
| residual_blind_multiband_image_morphology_label | 4 | 15.158999999999999 |
| bar_length_and_m2_component | 1 | 29.745 |
| velocity_field_if_available | 1 | 29.745 |

## Claim Boundary

This is not an accepted morphology manifest, not image-based validation,
and not an endpoint score. It is a source-request layer for future
residual-blind morphology inspection.

Claim boundary: `p0_external_imaging_request_not_morphology_label_not_endpoint`.
