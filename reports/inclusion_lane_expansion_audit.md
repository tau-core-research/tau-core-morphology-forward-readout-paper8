# Inclusion Lane Expansion Audit

This audit increases usable sample coverage without weakening the
accepted-lane claim boundary. Strict rows are the only preendpoint
freeze candidates. Caution rows may be used only as support or
sensitivity lanes. Acquisition rows identify missing residual-blind
source data.

## Verdict

- Strict-ready candidates: 1/175
- Caution/proxy-supported rows: 66/175
- Analysis-includable strict+caution rows: 67/175
- Acquisition-required rows: 108/175
- Rows needing orientation source evidence: 108/175
- Rows needing projection/scale review: 104/175
- Rows needing memory/history source review: 171/175

The strict lane remains tiny. The practical expansion is the caution lane:
it keeps orientation-ready rows available for non-claim support analyses
while explicitly preserving their projection or memory/history caveats.

## Summary

| split | n_galaxies | strict_ready_count | caution_ready_count | analysis_includable_count | acquisition_required_count | orientation_required_count | projection_required_count | memory_required_count | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 175 | 1 | 66 | 67 | 108 | 108 | 104 | 171 | False | inclusion_lane_expansion_audit_not_endpoint |
| holdout | 44 | 0 | 16 | 16 | 28 | 28 | 30 | 43 | False | inclusion_lane_expansion_audit_not_endpoint |
| train | 131 | 1 | 50 | 51 | 80 | 80 | 74 | 128 | False | inclusion_lane_expansion_audit_not_endpoint |

## Lane Counts

| inclusion_lane | allowed_use | n_galaxies |
| --- | --- | --- |
| ACQUISITION_REQUIRED | source_acquisition_or_review_queue | 108 |
| CAUTION_READY_PROXY_SUPPORTED | support_lane_memory_history_proxy | 19 |
| CAUTION_READY_PROXY_SUPPORTED | support_lane_projection_caveat | 47 |
| STRICT_READY_CANDIDATE | strict_preendpoint_freeze_candidate | 1 |

## Acquisition Need Counts

| need | n_galaxies |
| --- | --- |
| needs_residual_blind_memory_history_source | 113 |
| needs_vertical_velocity_field_or_warp_flare_source | 108 |
| needs_distance_quality_or_scale_audit | 66 |
| needs_source_memory_flag_resolution | 58 |
| needs_projection_geometry_source_review | 34 |
| needs_projection_or_inclination_audit | 28 |
| needs_manifest_confidence_review | 6 |
| needs_accepted_q_i_assignment_and_normalization_law | 1 |

## Claim Boundary

This audit computes no endpoint scores and uses no rotation residuals.
Caution rows are not accepted evidence. They are only a way to avoid
throwing away informative galaxies while keeping the final endpoint claim
restricted to strict accepted lanes.
