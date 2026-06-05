# NGC7331 Outer-Warp / Vertical Caveat Gate

This residual-blind gate maps the existing NGC7331 vertical source
fields into dimensionless readout inputs and records that the outer-warp
caveat should be treated as mixed-overlay context rather than ignored.
It does not score rotation curves.

## Summary

| galaxy | candidate_mixed_readout | audit_decision | rdisk_kpc | rhi_kpc | intrinsic_h_mid_kpc | projected_hwhm_kpc | intrinsic_h_over_Rs_mid | projected_hwhm_over_Rs | projected_hwhm_over_RHI | vertical_activation_candidate | outer_warp_context_present | outer_warp_numeric_onset_available | uses_vobs_or_residual_in_construction | endpoint_scores_allowed | formula_freeze_attempt_allowed | caveat_gate_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | K_expdisk_thick_outer_warp_overlay_review | CAVEATED_ACCEPTED_SOURCE_FIELDS_NOT_ENDPOINT_READY | 5.02 | 27.01 | 0.15 | 0.5 | 0.0298805 | 0.0996016 | 0.0185117 | 0.63081 | True | False | False | False | True | CAVEAT_MAPPED_TO_MIXED_OVERLAY_CONTEXT_FORMULA_FREEZE_ALLOWED | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |

## Source Fields

| field_id | observable | value | unit | status | source | source_line_refs | role | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N7331_V1_MOLECULAR_SCALEHEIGHT_RANGE | molecular_scaleheight_range | 0.1-0.2 | kpc | ACCEPTED_NUMERIC_SOURCE_FIELD | ngc7331_patra_2018_molecular_scale_height.txt | 16-24;715-721;984-986 | sets intrinsic vertical thickness range | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |
| N7331_V2_EDGE_ON_PROJECTED_HWHM | edge_on_projected_hwhm | 0.5 | kpc | ACCEPTED_NUMERIC_SOURCE_FIELD | ngc7331_patra_2018_molecular_scale_height.txt | 23-26;955-981;1033-1037 | sets projected observable vertical thickness | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |
| N7331_V3_H_OVER_RS_INTRINSIC_MID | intrinsic_h_over_Rs_mid | 0.029880478087649404 | dimensionless | DERIVED_FROM_ACCEPTED_VERTICAL_SOURCE_AND_SPARC_RDISK | Patra2018NGC7331ScaleHeight + SPARC Rdisk | scaleheight lines from Patra; Rdisk from SPARC metadata | dimensionless vertical kernel amplitude candidate | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |
| N7331_V4_PROJECTED_HWHM_OVER_RS | projected_hwhm_over_Rs | 0.09960159362549802 | dimensionless | DERIVED_FROM_ACCEPTED_VERTICAL_SOURCE_AND_SPARC_RDISK | Patra2018NGC7331ScaleHeight + SPARC Rdisk | edge-on HWHM lines from Patra; Rdisk from SPARC metadata | dimensionless projected-thickness overlay amplitude candidate | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |
| N7331_P1_INCLINATION_REVIEW | inclination_review_range | 72-80;adopted_76 | deg | ACCEPTED_NUMERIC_SOURCE_FIELD | ngc7331_patra_2018_molecular_scale_height.txt | 108-110;864-867;960-965;1028-1031 | projection-safety context | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |
| N7331_W1_OUTER_WARP_CAVEAT | possible_outer_warp_caveat | possible_extra_outer_emission_from_warp | categorical | CAVEAT_CONFIRMED_AS_OVERLAY_CONTEXT | ngc7331_patra_2018_molecular_scale_height.txt | 960-968 | blocks pure thick-regular acceptance; supports mixed outer-warp overlay review | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |
| N7331_W2_HI_WARP_CONTEXT | outer_hi_warp_context | direct_and_kinematic_HI_warp_context_present | categorical | CONTEXT_SOURCE_FIELD_REVIEW_READY | https://ned.ipac.caltech.edu/level5/March05/Bosma/Bosma5_5.html | NED Level 5 Bosma warp discussion | supports outer-warp overlay context; no numeric warp radius extracted here | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_CG1_SOURCE_QUEUE_CANDIDATE | PASS_CAVEATED | P1_CAVEATED_VERTICAL_OVERLAY_CANDIDATE | candidate source rule supports formula-freeze attempt only, not endpoint scoring | False | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |
| NGC7331 | N7331_CG2_VERTICAL_NUMERIC_MAPPING | PASS | intrinsic_h_over_Rs_mid=0.0298805; projected_hwhm_over_Rs=0.0996016 | treat projected HWHM as overlay observable, not intrinsic scaleheight | False | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |
| NGC7331 | N7331_CG3_OUTER_WARP_CAVEAT | PASS_CAVEATED | possible_extra_outer_emission_from_warp | outer warp lacks numeric onset; may only define a broad outer-window caveat | False | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |
| NGC7331 | N7331_CG4_HI_WARP_CONTEXT | PASS_CONTEXT_ONLY | Bosma review records NGC7331 as just edge-on enough to see the warp directly in the HI distribution and just face-on enough to infer it from kinematics; these are consistent with each other. | no endpoint kernel may use a fitted warp radius from this context alone | False | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |
| NGC7331 | N7331_CG5_ENDPOINT_BLINDNESS | PASS | uses source fields, SPARC scale metadata, and literature context only | scoring must remain separate and formula must freeze before scoring | False | False | ngc7331_outer_warp_vertical_caveat_gate_not_endpoint |

## Claim Boundary

This gate does not prove that the mixed NGC7331 readout fits the galaxy.
It only allows a formula-freeze attempt: the vertical amplitudes are
source-derived, while the outer-warp term is context/caveat-only until
a numeric HI/projection onset is extracted.
