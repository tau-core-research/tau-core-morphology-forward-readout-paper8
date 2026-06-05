# NGC5907 Projection-Dominated Freeze Gate

This gate freezes a residual-blind projection/warp/truncation/vertical
kernel protocol for the current source-field accepted NGC5907 control.
It does not score endpoints and does not validate Tau Core.

## Summary

| galaxy | proposed_readout_subfamily | n_source_fields | n_gates | n_pass_like | n_caveated | n_blocked | warp_r_inner_kpc | warp_r_outer_kpc | warp_displacement_kpc | thickness_h_over_rs | truncation_contrast | frozen_projection_bound | projection_freeze_status | accepted_subfamily_label_promoted | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | K_projection_dominated | 6 | 6 | 6 | 1 | 0 | 13.3 | 24 | 1.7 | 0.173321 | 0.738298 | 0.789128 | PROJECTION_PROTOCOL_BOUND_READY_NOT_ENDPOINT | True | False | ngc5907_projection_freeze_gate_not_endpoint |

## Source Fields

| field_id | observable | value | unit | status | source | source_line_refs | role | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1_WARP_RADIAL_RANGE | optical_warp_radial_range | 13.3-24 | kpc | ACCEPTED_NUMERIC_SOURCE_FIELD | ngc5907_sasaki_1987_surface_photometry_warp.txt | 9-23 | sets projection-dominated radial support | False | ngc5907_projection_freeze_gate_not_endpoint |
| P2_WARP_DISPLACEMENT | optical_warp_max_displacement | 1.7 | kpc | ACCEPTED_NUMERIC_SOURCE_FIELD | ngc5907_sasaki_1987_surface_photometry_warp.txt | 15-23 | sets projection displacement amplitude proxy | False | ngc5907_projection_freeze_gate_not_endpoint |
| P3_TRUNCATION_SCALES | disk_truncation_scale_lengths | 4.92;4.7;1.23 | kpc | ACCEPTED_NUMERIC_SOURCE_FIELD | ngc5907_sasaki_1987_surface_photometry_warp.txt | 9-15 | sets disk/truncation transition contrast | False | ngc5907_projection_freeze_gate_not_endpoint |
| P4_VERTICAL_KERNEL_RATIO | thickness_h_over_rs | 0.1733207190160832 | dimensionless | DIRECT_S4G_EDGEDISK_HZ_HR_READY | S4G_Table7 | Z:edgedisk_hz2_over_hr2 | direct S4G edge-disk vertical-kernel observable | False | ngc5907_projection_freeze_gate_not_endpoint |
| P5_INTERACTION_CONTEXT | interaction_warp_context | warp_and_dwarf_interaction_context_present | categorical | ACCEPTED_CONTEXT_SOURCE_FIELD | ngc5907_shang_1998_ring_warp_interaction.txt | title/abstract source | supports projection/history context, not amplitude by itself | False | ngc5907_projection_freeze_gate_not_endpoint |
| P6_VERTICAL_STRUCTURE_CONTEXT | edge_on_vertical_structure_source | CO_HI_Spitzer_vertical_structure_study_present | categorical | ACCEPTED_CONTEXT_SOURCE_FIELD | ngc5907_wiegert_2015_edge_on_ism.txt | 14-23;52-59 | supports edge-on projection sanity | False | ngc5907_projection_freeze_gate_not_endpoint |

## Gates

| galaxy | proposed_readout_subfamily | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | K_projection_dominated | PFG1_ACCEPTED_SOURCE_FIELDS | PASS | ACCEPTED_SUBFAMILY_SOURCE_FIELDS_ENDPOINT_STILL_BLOCKED | endpoint freeze still separate | False | False | ngc5907_projection_freeze_gate_not_endpoint |
| NGC5907 | K_projection_dominated | PFG2_DIMENSIONAL_WARP_RANGE | PASS | warp range 13.3-24 kpc; start/main_scale=2.7 | preserve projected-geometry caveat | False | False | ngc5907_projection_freeze_gate_not_endpoint |
| NGC5907 | K_projection_dominated | PFG3_VERTICAL_KERNEL_DIRECT | PASS | h/R=0.173321 from Z:edgedisk_hz2_over_hr2 | treat as source-native kernel observable, not endpoint fit | False | False | ngc5907_projection_freeze_gate_not_endpoint |
| NGC5907 | K_projection_dominated | PFG4_TRUNCATION_CONTRAST_READY | PASS | main/corrected/outer scales=4.92/4.7/1.23 kpc | do not tune transition against rotation residuals | False | False | ngc5907_projection_freeze_gate_not_endpoint |
| NGC5907 | K_projection_dominated | PFG5_FROZEN_PROJECTION_BOUND | PASS_CAVEATED | Pi_projection <= 0.789128 | protocol bound only; not final Tau-side projection coefficient law | False | False | ngc5907_projection_freeze_gate_not_endpoint |
| NGC5907 | K_projection_dominated | PFG6_ENDPOINT_BLINDNESS | PASS | all inputs are source fields or direct kernel observables; endpoint_scores_allowed=False | future scoring requires separately frozen endpoint protocol | False | False | ngc5907_projection_freeze_gate_not_endpoint |

## Interpretation

NGC5907 is now a projection-dominated protocol-ready control, not an
endpoint-ready validation case. The source layer supplies warp range, warp
displacement, disk/truncation scales, interaction context, and a direct S4G
edge-disk h/R observable. The frozen projection bound is a conservative
protocol quantity, not a fitted readout amplitude.
