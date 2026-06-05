# NGC4183 Projection/Outer-Warp Formula Derivation

Status: `NGC4183_PROJECTION_OUTER_WARP_FORMULA_SHELL_DERIVED_FREEZE_BLOCKED`

This is a formula-shell derivation only.  It does not freeze the coefficient and
does not authorize endpoint scoring.

## Summary

| formula_derivation_status | galaxy | candidate_readout | rhi_kpc | p_edge | hi_extent_in_disk_scales | x_inner | coefficient_rule_frozen | numeric_warp_ramp_frozen | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_PROJECTION_OUTER_WARP_FORMULA_SHELL_DERIVED_FREEZE_BLOCKED | NGC4183 | K_expdisk_edge_on_projection_outer_warp_caveated | 15.9698 | 0.985148 | 5.72393 | 0.34941 | False | False | False | False | ngc4183_projection_outer_warp_formula_derivation_not_endpoint | source_blind_gamma_projection_coefficient_rule_or_freeze_blocker_resolution |

## Formula

| formula_id | formula | kernel | carrier | sign | amplitude_or_coefficient | coefficient_status | source_inputs | uses_vobs_or_residual | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N4183_PROJECTION_ATTENUATION_SHELL | v_readout^2(R)=v_carrier^2(R)*(1-gamma_proj*K_proj(R)) | K_proj(R)=p_edge*smoothstep((R/R_HI-x_inner)/(1-x_inner)) | smooth_exponential_disk_carrier | attenuation | gamma_proj | UNFROZEN_BLOCKS_FORMULA_FREEZE | R_HI_source_native_kpc; p_edge; Rdisk/RHI | False | False | False | ngc4183_projection_outer_warp_formula_derivation_not_endpoint |

## Derivation Steps

| step_id | definition_or_result | status | dimension_check | limit_check |
| --- | --- | --- | --- | --- |
| D1_CARRIER | v_carrier^2(R) is the predeclared smooth exponential-disk carrier | ASSUMPTION_FROM_EXISTING_SOURCE_LABEL | km^2/s^2 | carrier recovered when gamma_proj=0 |
| D2_PROJECTION_OBSERVABLE | p_edge = sin^2(i_HI) | DERIVED_FROM_SOURCE_NATIVE_HI_INCLINATION | dimensionless | p_edge -> 0 face-on; p_edge -> 1 edge-on |
| D3_RADIAL_KERNEL | K_proj(R)=p_edge*smoothstep((R/R_HI-x_inner)/(1-x_inner)) | FORMULA_SHELL_DERIVED | dimensionless | K_proj=0 inside inactive window; K_proj<=p_edge |
| D4_ATTENUATION_READOUT | v_readout^2(R)=v_carrier^2(R)*(1-gamma_proj*K_proj(R)) | FORMULA_CONDITIONAL_COEFFICIENT_UNFROZEN | km^2/s^2 because K_proj and gamma_proj are dimensionless | gamma_proj=0 or K_proj=0 recovers carrier |
| D5_OUTER_WARP_CAVEAT | outer warp statement can motivate caveat only, not a numeric added ramp | BLOCKS_WARP_RAMP_FREEZE | no numeric term introduced | no warp amplitude means no added-source contribution |

## Kernel Grid Preview

| x_R_over_RHI | R_kpc | x_inner | p_edge | activation | K_proj | uses_vobs_or_residual |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.0333333 | 0.532325 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.0666667 | 1.06465 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.1 | 1.59698 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.133333 | 2.1293 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.166667 | 2.66163 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.2 | 3.19395 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.233333 | 3.72628 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.266667 | 4.2586 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.3 | 4.79093 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.333333 | 5.32325 | 0.34941 | 0.985148 | 0 | 0 | False |
| 0.366667 | 5.85558 | 0.34941 | 0.985148 | 0.00207327 | 0.00204248 | False |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N4183_FORMULA_G1_LABEL_DERIVATION_ALLOWED | PASS | NARROW_REPLACEMENT_LABEL_SUPPORTED_FOR_FORMULA_DERIVATION_NOT_ENDPOINT | derive only; freeze separately |
| N4183_FORMULA_G2_DIMENSIONAL_CONSISTENCY | PASS | gamma_proj and K_proj dimensionless; carrier has velocity-squared units | none for shell |
| N4183_FORMULA_G3_KNOWN_LIMITS | PASS | gamma=0 and inactive kernel recover carrier; face-on p_edge tends to zero | none for shell |
| N4183_FORMULA_G4_COEFFICIENT_RULE | BLOCKED | gamma_proj is not source-frozen | derive/freeze gamma_proj without residuals |
| N4183_FORMULA_G5_WARP_RAMP | BLOCKED | outer warp is qualitative only | do not include added warp ramp unless onset/amplitude is acquired |

## Interpretation

The source-supported direction for NGC4183 is not a standalone added warp-ramp.
It is a projection-attenuation shell with an outer-warp caveat:

```text
K_proj(R) = p_edge * smoothstep((R/R_HI - x_inner) / (1 - x_inner))
v_readout^2(R) = v_carrier^2(R) * (1 - gamma_proj K_proj(R))
```

This shell is dimensionally consistent and has the right zero-overlay limits,
but it is not frozen because `gamma_proj` is not yet derived from source-side
evidence.  The qualitative outer-warp statement cannot be used as a numeric
added-source amplitude.
