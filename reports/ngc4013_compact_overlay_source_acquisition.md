# NGC4013 Compact/Overlay Source Acquisition

This pass acquires compact-support and overlay evidence for NGC4013.
It preserves a negative result: the local S4G Pipeline 4 table contains
no Sersic bulge component with an effective radius for NGC4013.

## Summary

| galaxy | n_acquired_source_rows | s4g_components | has_s4g_bulge_component | s4g_edge_disk_hr_kpc | s4g_edge_disk_hz_kpc | s4g_edge_disk_h_over_r | extended_component_scaleheight_kpc | extended_component_mass_fraction | compact_support_radius_acquired | bulge_core_decomposition_decision | compact_lane_decision | replacement_lane_recommendation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | 4 | Z:edgedisk;N:psf | False | 2.39023 | 0.55676 | 0.232932 | 3 | 0.2 | False | NO_S4G_BULGE_COMPONENT_ONLY_NUCLEAR_PSF_AND_BOXY_BULGE_CONTEXT | COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED | PROMOTE_WARP_VERTICAL_OVERLAY_PREFLIGHT_NOT_ENDPOINT | False | ngc4013_compact_overlay_source_acquisition_not_endpoint |

## Acquired Source Rows

| galaxy | source_id | source_file | source_line_refs | observable | extracted_value | numeric_value | unit | acquisition_status | compact_lane_impact | overlay_lane_impact | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | S4G_PIPELINE4_TABLE7_LOCAL | data/derived/external_s4g_table7.csv | Seq=1004; components C=Z,N | s4g_component_decomposition | Z edgedisk + N nuclear_psf; no B bulge component |  | categorical | ACQUIRED_NEGATIVE_COMPACT_EVIDENCE | NO_S4G_BULGE_RE; compact support radius not acquired | edge-disk component supports vertical/projection review | False | ngc4013_compact_overlay_source_acquisition_not_endpoint |
| NGC4013 | S4G_PIPELINE4_EDGE_DISK_GEOMETRY | data/derived/external_s4g_table7.csv | Seq=1004; C=Z; Fn=edgedisk | s4g_edge_disk_hr_hz | hr=27.39 arcsec; hz=6.38 arcsec | 2.39022617;0.556759508;0.232931727 | kpc;kpc;dimensionless | ACQUIRED_VERTICAL_KERNEL_EVIDENCE | not compact support | source-native stellar edge-disk h/R supports vertical-overlay kernel | False | ngc4013_compact_overlay_source_acquisition_not_endpoint |
| NGC4013 | COMERON2011_VERTICAL_DECOMPOSITION | data/external/literature/ngc4013_comeron_2011_unusual_vertical_mass_distribution.txt | 11-20;67-70;167-180;188-192 | thin_thick_extended_component_decomposition | thin+thick disk plus extra extended component; z_EC about 3 kpc; EC about 20 percent mass | 3.0;0.20 | kpc;mass_fraction | ACQUIRED_EXTENDED_VERTICAL_COMPONENT_EVIDENCE | supports non-compact vertical/extended morphology rather than compact-only endpoint | strong support for warp/vertical-overlay candidate | False | ngc4013_compact_overlay_source_acquisition_not_endpoint |
| NGC4013 | COMERON2011_BOXY_BULGE_CAVEAT | data/external/literature/ngc4013_comeron_2011_unusual_vertical_mass_distribution.txt | 76-83;89-92 | boxy_bulge_or_edge_on_bar_context | boxy bulge noted as possible edge-on bar or merger consequence; profile bins avoid bulge influence |  | context | ACQUIRED_COMPACT_CAVEAT_NOT_RADIUS | boxy-bulge context does not provide compact support radius | supports bar/merger/vertical-history caveat | False | ngc4013_compact_overlay_source_acquisition_not_endpoint |

## Interpretation

The missing compact/bulge blocker is not resolved by finding a compact
support radius. It is resolved in the opposite direction: the currently
available S4G and literature sources do not support a compact endpoint
lane. They support a warp/vertical-overlay preflight lane, with endpoint
scoring still blocked until a source-frozen overlay formula is defined.
