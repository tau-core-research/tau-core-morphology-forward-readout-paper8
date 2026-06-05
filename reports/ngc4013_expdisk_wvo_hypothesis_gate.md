# NGC4013 Exponential-Disk + Warp/Vertical-Overlay Hypothesis Gate

This gate creates a mixed-readout diagnostic hypothesis. It is not an
accepted endpoint label because the exponential-disk carrier was motivated
by a wrong-family control result as well as source-side disk evidence.

## Summary

| galaxy | mixed_readout_candidate | carrier | overlay_formula_id | n_source_fields | n_gates | n_endpoint_blocked | hypothesis_status | endpoint_scores_allowed | diagnostic_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | K_expdisk_warp_vertical_overlay | K_exponential_disk | NGC4013_WARP_VERTICAL_OVERLAY_V1 | 5 | 4 | 1 | DIAGNOSTIC_ONLY_MIXED_READOUT_HYPOTHESIS | False | True | ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint |

## Source Fields

| field_id | field_name | field_value | field_status | interpretation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| MIX1_EDGE_DISK_COMPONENT | s4g_edge_disk_component | Z:edgedisk;N:psf | SOURCE_SUPPORTS_SMOOTH_DISK_CARRIER | S4G decomposition has an edge-disk component; no compact bulge component is present. | False | ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint |
| MIX2_VERTICAL_OVERLAY | s4g_edge_disk_h_over_r | 0.2329317269076305 | SOURCE_SUPPORTS_VERTICAL_OVERLAY | The edge-disk h/R field supports a vertical/projection overlay kernel. | False | ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint |
| MIX3_EXTENDED_COMPONENT | extended_component_mass_fraction | 0.2 | SOURCE_SUPPORTS_EXTENDED_VERTICAL_COMPONENT | The extended component supports a non-compact vertical overlay lane. | False | ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint |
| MIX4_WARP_VERTICAL_LABEL | replacement_label_status | CAVEATED_REPLACEMENT_LABEL_PROMOTED_ENDPOINT_SCORE_ALLOWED | CAVEATED_SOURCE_GATE_PRESENT | The warp/vertical overlay label is caveated endpoint-score allowed. | False | ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint |
| MIX5_WRONG_FAMILY_SIGNAL | wrong_family_best_rmse | 10.880207082032724 | ENDPOINT_DIAGNOSTIC_SIGNAL_NOT_LABEL_INPUT | The exponential-disk family beat the pure overlay endpoint in the control audit; this cannot promote a label by itself. | False | ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint |

## Gates

| galaxy | mixed_readout_candidate | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | diagnostic_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | K_expdisk_warp_vertical_overlay | MIXG1_COMPACT_REJECTED | PASS | COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED | none for rejecting the compact-only lane | False | True | ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint |
| NGC4013 | K_expdisk_warp_vertical_overlay | MIXG2_SMOOTH_DISK_SOURCE_SUPPORT | PASS_CAVEATED | S4G components=Z:edgedisk;N:psf; edge disk h/R=0.232932 | derive a residual-blind rule for when the exponential-disk carrier is selected | False | True | ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint |
| NGC4013 | K_expdisk_warp_vertical_overlay | MIXG3_WARP_VERTICAL_FORMULA_AVAILABLE | PASS | NGC4013_WARP_VERTICAL_OVERLAY_V1 | none at overlay-kernel level | False | True | ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint |
| NGC4013 | K_expdisk_warp_vertical_overlay | MIXG4_SCORE_INFERENCE_CAVEAT | BLOCKED_FOR_ENDPOINT | NEGATIVE_RESULT_MATCHED_DOES_NOT_BEAT_ALL_WRONG_FAMILIES | mixed family is diagnostic-only until selected by source rules before scoring | False | True | ngc4013_expdisk_warp_vertical_overlay_hypothesis_not_endpoint |

## Claim Boundary

The mixed readout may be inspected diagnostically. Promotion requires a
future residual-blind source rule selecting the exponential-disk carrier
before endpoint scoring.
