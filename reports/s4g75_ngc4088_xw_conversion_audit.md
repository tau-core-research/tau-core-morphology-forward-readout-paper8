# NGC4088 x_w Conversion Audit

This report is the first machine-readable conversion gate from the frozen
channel-map digitization response into the dimensionless warp-onset
control `x_w = R_warp / R_HI`.

## Verdict

The current package is correctly blocked until the digitization response
template is filled and validated. No `x_w` value is accepted yet.

## Audit

| galaxy | conversion_status | digitization_validation_status | side_combination_rule_applied | hi_diameter_arcmin | hi_radius_arcmin | r_hi_kpc | combined_onset_arcmin | combined_onset_kpc | x_warp_onset | x_warp_uncertainty | dimension_check_passed | crosscheck_page77_consistency | accepted_for_mapping_rule | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | XW_READY_FOR_MAPPING_RULE | READY_FOR_XW_CONVERSION_AUDIT | MIN_SIDE | 8.5 | 4.25 | 22.253 | 1.2 | 6.28319 | 0.282353 | 0.0705882 | True | CONSISTENT_WITH_PAGE77_PA_BEND | True | False | False | s4g75_ngc4088_xw_conversion_audit_not_endpoint |

## Summary

| galaxy | xw_conversion_decision | n_missing_required_fields | accepted_for_mapping_rule | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| NGC4088 | XW_READY_FOR_MAPPING_RULE | 0 | True | False | s4g75_ngc4088_xw_conversion_audit_not_endpoint |

## Claim Boundary

A passing conversion audit would only make `x_w` available as an input to
the residual-blind mapping-rule lane. It would still not authorize
endpoint scoring or a validation claim.
