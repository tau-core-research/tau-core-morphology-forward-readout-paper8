# Morphology Inspection Queue

This queue prioritizes galaxies for residual-blind morphology review after
the morphology-memory/history proxy diagnostic. It is an acquisition and
audit plan only. It does not promote rotation-inferred readout choices to
accepted morphology labels.

## Verdict

The queue turns the current-shape/readout-history mismatch signal into a
concrete inspection order: which galaxies need image/decomposition review,
which memory/history observables to request, and which cases need external
sources beyond the current S4G crossmatch.

## Priority Counts

| inspection_priority_tier | n_galaxies |
| --- | --- |
| P0 | 4 |
| P1 | 18 |
| P2 | 56 |
| P3 | 97 |

## Focus Summary

| inspection_priority_tier | inspection_focus | n_galaxies | median_priority_score | n_s4g_matched | n_external_family_mismatches |
| --- | --- | --- | --- | --- | --- |
| P0 | outer_disk_tail_lsb_or_hi_extent | 2 | 98.0 | 2 | 2 |
| P0 | bar_m2_component;outer_disk_tail_lsb_or_hi_extent | 1 | 88.0 | 1 | 1 |
| P0 | edge_on_projection_degeneracy;outer_disk_tail_lsb_or_hi_extent | 1 | 88.0 | 1 | 1 |
| P1 | outer_disk_tail_lsb_or_hi_extent | 12 | 74.0 | 6 | 2 |
| P1 | thickness_flare_warp_or_projection | 3 | 73.0 | 2 | 1 |
| P1 | bar_m2_component;thickness_flare_warp_or_projection | 1 | 78.0 | 1 | 1 |
| P1 | edge_on_projection_degeneracy;thickness_flare_warp_or_projection | 1 | 83.0 | 1 | 1 |
| P1 | outer_disk_tail_lsb_or_hi_extent;thickness_flare_warp_or_projection | 1 | 78.0 | 1 | 0 |
| P2 | outer_disk_tail_lsb_or_hi_extent | 23 | 65.0 | 9 | 0 |
| P2 | thickness_flare_warp_or_projection | 13 | 58.0 | 9 | 0 |
| P2 | outer_disk_tail_lsb_or_hi_extent;thickness_flare_warp_or_projection | 7 | 60.0 | 6 | 0 |
| P2 | bulge_compact_core_or_central_support | 6 | 58.0 | 3 | 0 |
| P2 | bulge_compact_core_or_central_support;thickness_flare_warp_or_projection | 6 | 61.5 | 3 | 0 |
| P2 | bulge_compact_core_or_central_support;outer_disk_tail_lsb_or_hi_extent | 1 | 63.0 | 1 | 0 |
| P3 | outer_disk_tail_lsb_or_hi_extent | 43 | 40.0 | 15 | 0 |
| P3 | bulge_compact_core_or_central_support | 24 | 30.0 | 4 | 0 |
| P3 | thickness_flare_warp_or_projection | 16 | 48.0 | 8 | 0 |
| P3 | current_label_vs_readout_subtype_split | 7 | 10.0 | 1 | 0 |
| P3 | bulge_compact_core_or_central_support;outer_disk_tail_lsb_or_hi_extent | 2 | 45.0 | 0 | 0 |
| P3 | edge_on_projection_degeneracy | 2 | 28.0 | 2 | 0 |
| P3 | outer_disk_tail_lsb_or_hi_extent;thickness_flare_warp_or_projection | 2 | 50.0 | 0 | 0 |
| P3 | bar_m2_component | 1 | 38.0 | 1 | 0 |

## Top 20 Inspection Targets

| galaxy | inspection_priority_tier | inspection_priority_score | inspection_focus | current_proxy_family | rotation_inferred_family | s4g_match_status |
| --- | --- | --- | --- | --- | --- | --- |
| NGC0300 | P0 | 98 | outer_disk_tail_lsb_or_hi_extent | K_exponential_disk | K_scale_tail_spiral | S4G_MATCHED |
| NGC6503 | P0 | 98 | outer_disk_tail_lsb_or_hi_extent | K_exponential_disk | K_scale_tail_spiral | S4G_MATCHED |
| NGC0100 | P0 | 88 | edge_on_projection_degeneracy;outer_disk_tail_lsb_or_hi_extent | K_exponential_disk | K_scale_tail_spiral | S4G_MATCHED |
| NGC0247 | P0 | 88 | bar_m2_component;outer_disk_tail_lsb_or_hi_extent | K_exponential_disk | K_scale_tail_spiral | S4G_MATCHED |
| IC2574 | P1 | 83 | outer_disk_tail_lsb_or_hi_extent | K_scale_tail_spiral | K_exponential_disk | S4G_MATCHED |
| NGC3917 | P1 | 83 | outer_disk_tail_lsb_or_hi_extent | K_exponential_disk | K_scale_tail_spiral | S4G_MATCHED |
| NGC4183 | P1 | 83 | edge_on_projection_degeneracy;thickness_flare_warp_or_projection | K_exponential_disk | K_thick_flared | S4G_MATCHED |
| NGC6015 | P1 | 83 | outer_disk_tail_lsb_or_hi_extent | K_exponential_disk | K_scale_tail_spiral | S4G_MATCHED |
| UGC04483 | P1 | 83 | outer_disk_tail_lsb_or_hi_extent | K_scale_tail_spiral | K_exponential_disk | S4G_MATCHED |
| NGC3972 | P1 | 78 | outer_disk_tail_lsb_or_hi_extent;thickness_flare_warp_or_projection | K_thick_flared | K_scale_tail_spiral | S4G_MATCHED |
| UGC06930 | P1 | 78 | bar_m2_component;thickness_flare_warp_or_projection | K_exponential_disk | K_thick_flared | S4G_MATCHED |
| DDO170 | P1 | 75 | outer_disk_tail_lsb_or_hi_extent | K_scale_tail_spiral | K_exponential_disk | NO_S4G_MATCH |
| UGC05005 | P1 | 75 | outer_disk_tail_lsb_or_hi_extent | K_scale_tail_spiral | K_exponential_disk | NO_S4G_MATCH |
| ESO116-G012 | P1 | 73 | outer_disk_tail_lsb_or_hi_extent | K_exponential_disk | K_scale_tail_spiral | S4G_MATCHED |
| NGC0289 | P1 | 73 | thickness_flare_warp_or_projection | K_thick_flared | K_exponential_disk | S4G_MATCHED |
| NGC7793 | P1 | 73 | thickness_flare_warp_or_projection | K_exponential_disk | K_thick_flared | S4G_MATCHED |
| UGC07125 | P1 | 73 | outer_disk_tail_lsb_or_hi_extent | K_scale_tail_spiral | K_exponential_disk | S4G_MATCHED |
| DDO064 | P1 | 70 | thickness_flare_warp_or_projection | K_scale_tail_spiral | K_thick_flared | NO_S4G_MATCH |
| UGC07603 | P1 | 70 | outer_disk_tail_lsb_or_hi_extent | K_exponential_disk | K_scale_tail_spiral | NO_S4G_MATCH |
| UGC07866 | P1 | 70 | outer_disk_tail_lsb_or_hi_extent | K_scale_tail_spiral | K_exponential_disk | NO_S4G_MATCH |

## Claim Boundary

This is not an accepted morphology manifest, not a morphology validation,
and not an endpoint score. The queue is allowed to guide future
residual-blind source collection only.

Claim boundary: `morphology_inspection_queue_not_accepted_label_not_endpoint`.
