# NGC4088 Warp/Asymmetry Extraction Gate

This gate records what the WHISP/Ursa Major source can and cannot provide for the NGC4088 thick/flared closure-source branch.

## Verdict

NGC4088 now has object-specific warp/asymmetry evidence suitable for formula-development work. It is not endpoint-ready because the source does not yet provide a residual-blind radial warp, flare, or closure source profile.

## Extractable Source-Native Observables

| galaxy | source_native_inclination_deg | source_native_position_angle_deg | source_native_hi_diameter_arcmin | source_native_hi_flux_jy_kms | source_native_w20_kms | source_native_w50_kms | warp_presence_flag | pv_asymmetry_flag | pa_asymmetry_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 69 | 231 | 8.5 | 102.9 | 371.4 | 342.1 | True | True | True |

## Missing Profile-Kernel Observables

warp_onset_radius
theta_warp_R_or_PA_R_profile
vertical_height_H_R
radial_closure_source_profile
residual_blind_mapping_rule

## Summary

| galaxy | extractable_observable_count | missing_profile_kernel_observable_count | closure_source_development_allowed | closure_source_endpoint_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 7 | 5 | True | False | False | s4g75_ngc4088_warp_asymmetry_extraction_gate_not_endpoint |

## Claim Boundary

The source permits a warp/asymmetry closure-source development lane, but not endpoint scoring. A usable readout kernel still needs a predeclared mapping from source-native warp/asymmetry observables to a radial closure-source profile.
