# NGC5907 Projection Accepted-Endpoint Freeze Gate

This gate is not a rotation score. It freezes the projection-dominated
readout formula before endpoint scoring and records that the construction
does not use observed rotation residuals.

## Summary

| galaxy | accepted_readout_subfamily | n_gates | n_pass | n_blocked | formula_id | gamma_projection | endpoint_scores_allowed | accepted_endpoint_freeze_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | K_projection_dominated | 5 | 5 | 0 | NGC5907_PROJECTION_ATTENUATION_V1 | 0.0683861 | True | ACCEPTED_ENDPOINT_FREEZE_READY | ngc5907_projection_accepted_endpoint_freeze_gate_not_score |

## Frozen Manifest

| galaxy | accepted_readout_subfamily | formula_id | formula_text | kernel_text | sign_rule | amplitude_rule | baseline_carrier | r_in_kpc | r_out_kpc | truncation_contrast | pi_projection | h_over_r | gamma_projection | formula_frozen_before_endpoint_scoring | uses_vobs_or_residual_in_construction | posthoc_retuning_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | K_projection_dominated | NGC5907_PROJECTION_ATTENUATION_V1 | v_proj^2(R)=v_TPG^2(R)*(1-gamma_proj*K_proj(R)) | K_proj=smoothstep((R-r_in)/(r_out-r_in))*(1+truncation_contrast*smoothstep((R-r_in)/(r_out-r_in)))/(1+truncation_contrast) | attenuation_not_added_gravity | gamma_proj=0.5*Pi_projection*h_over_r | v_TPG | 13.3 | 24 | 0.738298 | 0.789128 | 0.173321 | 0.0683861 | True | False | False | True | ngc5907_projection_accepted_endpoint_freeze_gate_not_score |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | AEG1_ACCEPTED_SOURCE_SUBFAMILY | PASS | ACCEPTED_SUBFAMILY_SOURCE_FIELDS_ENDPOINT_STILL_BLOCKED | none for NGC5907 source-field endpoint eligibility | True | ngc5907_projection_accepted_endpoint_freeze_gate_not_score |
| NGC5907 | AEG2_SOURCE_FROZEN_PROJECTION_PROTOCOL | PASS | PROJECTION_PROTOCOL_BOUND_READY_NOT_ENDPOINT | none; scoring must use this frozen protocol unchanged | True | ngc5907_projection_accepted_endpoint_freeze_gate_not_score |
| NGC5907 | AEG3_FORMULA_FREEZE_BEFORE_SCORING | PASS | formula/sign/amplitude/window are written in the freeze manifest before endpoint scoring | future endpoint runs must read this manifest, not infer formula from v_obs | True | ngc5907_projection_accepted_endpoint_freeze_gate_not_score |
| NGC5907 | AEG4_ENDPOINT_BLIND_CONSTRUCTION | PASS | construction inputs are source fields, direct kernel observables, and the predeclared TPG carrier | v_obs may be read only by the separate scoring script | True | ngc5907_projection_accepted_endpoint_freeze_gate_not_score |
| NGC5907 | AEG5_NO_RETUNING_RULE | PASS | posthoc_retuning_allowed=False; amplitude is gamma_proj=0.5*Pi_projection*h_over_r | changing sign, amplitude, carrier, or window after scoring demotes the row to diagnostic | True | ngc5907_projection_accepted_endpoint_freeze_gate_not_score |

## Claim Boundary

If the formula sign, amplitude rule, carrier, or radial window is changed
after seeing endpoint scores, the row must be demoted back to diagnostic.
