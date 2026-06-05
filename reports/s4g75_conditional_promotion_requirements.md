# S4G75 Conditional Kernel Promotion Requirements

This report records what must be proven or measured before the eight conditional S4G75 kernel rows can become strict kernel-ready endpoint rows. It is a requirement map, not an endpoint.

## Verdict

Conditional rows: 6.
Promotion gates: 1.

No conditional row is endpoint-eligible without either direct source-native measurement or a residual-blind Tau-side promotion theorem for its kernel observable.

## Family-Level Promotion Gates

| promotion_gate | formula_family | observable_driver_type | source_priority | n_galaxies | galaxies | direct_measurement_requirement | theorem_requirement | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | K_scale_tail_spiral | tail_inner_cutoff_candidate | P0_DIRECT_SOURCE_NATIVE_REQUIRED | 3 | NGC4214;UGC06917;UGC06983 | HI radial profile, outer-disk break radius, truncation radius, tail cutoff radius, or cited source-native transition radius | prove residual-blind admissibility of RHI as a conservative upper cutoff for the scale-tail readout kernel, with a fixed transition rule independent of endpoint residuals | s4g75_conditional_promotion_requirements_not_endpoint |
| TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | K_scale_tail_spiral | tail_inner_cutoff_candidate | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | 3 | UGC00891;UGC04499;UGC05829 | HI radial profile, outer-disk break radius, truncation radius, tail cutoff radius, or cited source-native transition radius | prove residual-blind admissibility of RHI as a conservative upper cutoff for the scale-tail readout kernel, with a fixed transition rule independent of endpoint residuals | s4g75_conditional_promotion_requirements_not_endpoint |

## Galaxy-Level Requirements

| galaxy | formula_family | source_priority | promotion_gate | direct_measurement_requirement | theorem_requirement | eligible_without_new_data | endpoint_scores_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4214 | K_scale_tail_spiral | P0_DIRECT_SOURCE_NATIVE_REQUIRED | TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | HI radial profile, outer-disk break radius, truncation radius, tail cutoff radius, or cited source-native transition radius | prove residual-blind admissibility of RHI as a conservative upper cutoff for the scale-tail readout kernel, with a fixed transition rule independent of endpoint residuals | False | False |
| UGC06917 | K_scale_tail_spiral | P0_DIRECT_SOURCE_NATIVE_REQUIRED | TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | HI radial profile, outer-disk break radius, truncation radius, tail cutoff radius, or cited source-native transition radius | prove residual-blind admissibility of RHI as a conservative upper cutoff for the scale-tail readout kernel, with a fixed transition rule independent of endpoint residuals | False | False |
| UGC06983 | K_scale_tail_spiral | P0_DIRECT_SOURCE_NATIVE_REQUIRED | TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | HI radial profile, outer-disk break radius, truncation radius, tail cutoff radius, or cited source-native transition radius | prove residual-blind admissibility of RHI as a conservative upper cutoff for the scale-tail readout kernel, with a fixed transition rule independent of endpoint residuals | False | False |
| UGC00891 | K_scale_tail_spiral | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | HI radial profile, outer-disk break radius, truncation radius, tail cutoff radius, or cited source-native transition radius | prove residual-blind admissibility of RHI as a conservative upper cutoff for the scale-tail readout kernel, with a fixed transition rule independent of endpoint residuals | False | False |
| UGC04499 | K_scale_tail_spiral | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | HI radial profile, outer-disk break radius, truncation radius, tail cutoff radius, or cited source-native transition radius | prove residual-blind admissibility of RHI as a conservative upper cutoff for the scale-tail readout kernel, with a fixed transition rule independent of endpoint residuals | False | False |
| UGC05829 | K_scale_tail_spiral | P1_PROMOTE_OR_CONFIRM_SOURCE_NATIVE | TAIL-HI-EXTENT-TO-TRANSITION-PROMOTION | HI radial profile, outer-disk break radius, truncation radius, tail cutoff radius, or cited source-native transition radius | prove residual-blind admissibility of RHI as a conservative upper cutoff for the scale-tail readout kernel, with a fixed transition rule independent of endpoint residuals | False | False |

## Claim Boundary

These promotion requirements are residual-blind. They cannot be satisfied by endpoint improvement, best-fit family choice, or residual shape. The source must constrain the readout kernel itself, or the Tau-side bridge must prove the proxy admissible before endpoint use.
