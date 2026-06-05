# Readout-Lane Taxonomy Update

Status: `READOUT_LANE_TAXONOMY_UPDATE_COMPLETE_NOT_ENDPOINT`

This update adds a readout-lane layer above the existing morphology subfamily
registry. It incorporates the NGC7331/NGC5907 split-B2 contrast without tuning
any formula.

## Summary

| taxonomy_update_status | n_lanes | n_subfamilies_mapped | universal_split_b2_rule_status | lane_specificity_status | endpoint_scores_allowed | formula_tuned | recommended_next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| READOUT_LANE_TAXONOMY_UPDATE_COMPLETE_NOT_ENDPOINT | 4 | 10 | REJECTED_BY_CURRENT_EVIDENCE | SUPPORTED_PRELIMINARY_NOT_VALIDATED | False | False | readout-lane freeze gate for each candidate galaxy before formula scoring | readout_lane_taxonomy_update_not_endpoint |

## Readout Lanes

| readout_lane | core_interpretation | typical_formula_shell | required_residual_blind_evidence | positive_reference | negative_reference | current_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L_added_source | morphology/history source adds a velocity-squared response on top of a carrier | v_readout^2 = v_carrier^2 + lambda_K K(R) | warp/history source activation; source-load rule; bounded support or tail window; sign rule | NGC7331 diagnostic only; NGC4088 targeted warp/history diagnostics | NGC5907 split-B2 caveated holdout | LANE_CANDIDATE_NOT_UNIVERSAL | False | readout_lane_taxonomy_update_not_endpoint |
| L_projection_attenuation | observed 4D readout is dominated by projection/deprojection/attenuation of a carrier | v_readout^2 = v_carrier^2 (1 - gamma_K K_proj(R)) | edge-on/projection geometry; warp window; vertical or dust/projection context; velocity-field sanity | NGC5907 projection accepted endpoint context | standalone added split-B2 fails on NGC5907 | SUPPORTED_FOR_NGC5907_CONTEXT_NOT_POPULATION_VALIDATED | False | readout_lane_taxonomy_update_not_endpoint |
| L_mixed_overlay | smooth carrier remains active while an overlay source-window modifies the readout | v_mix^2 = v_smooth^2 +/or * overlay(K_source) | smooth disk/decomposition scale plus warp/projection/vertical/bar/history overlay observables | NGC5907 mixed projection context; NGC4013 mixed reference path | requires anti-residual source rule before scoring | PROTOCOL_READY_FOR_SOURCE_RULE_CASES | False | readout_lane_taxonomy_update_not_endpoint |
| L_clean_carrier | baseline-like carrier already captures the readout when morphology is regular/stable | v_readout = v_carrier | low disturbance evidence; no strong projection/history/overlay activation; stable present morphology | baseline-strong galaxies in Paper 8 controls | fails where source-windowed overlay evidence is strong | OPEN_CONTROL_LANE | False | readout_lane_taxonomy_update_not_endpoint |

## Subfamily to Lane Map

| subfamily | primary_lane | secondary_lane | selection_rule | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| K_warp_history_coupled | L_added_source | L_mixed_overlay | use added lane only when source fields imply a real source-load/history term; otherwise treat as mixed/blocked | False | readout_lane_taxonomy_update_not_endpoint |
| K_projection_dominated | L_projection_attenuation | L_mixed_overlay | projection evidence selects bounded attenuation, not added source ramp | False | readout_lane_taxonomy_update_not_endpoint |
| K_expdisk_overlay | L_mixed_overlay | L_clean_carrier | smooth disk carrier plus overlay evidence; reject if overlay has no source field | False | readout_lane_taxonomy_update_not_endpoint |
| K_clean_expdisk | L_clean_carrier | L_mixed_overlay | clean carrier unless source-blind overlay/projection/history evidence is present | False | readout_lane_taxonomy_update_not_endpoint |
| K_thick_regular | L_clean_carrier | L_projection_attenuation | regular vertical thickness is carrier-like unless edge-on/projection caveat dominates | False | readout_lane_taxonomy_update_not_endpoint |
| K_flared_outer_disk | L_mixed_overlay | L_projection_attenuation | outer flare modifies carrier; projection lane if geometry dominates source fields | False | readout_lane_taxonomy_update_not_endpoint |
| K_smooth_n2_tail | L_added_source | L_clean_carrier | tail/source support may add a TGP-like term if source window and amplitude are frozen | False | readout_lane_taxonomy_update_not_endpoint |
| K_disturbed_outer_tail | L_added_source | L_mixed_overlay | disturbed tails require asymmetry/history source evidence and bounded support | False | readout_lane_taxonomy_update_not_endpoint |
| K_true_compact | L_clean_carrier | L_mixed_overlay | compact lane only with source-supported compact support; otherwise compact+disk overlay | False | readout_lane_taxonomy_update_not_endpoint |
| K_compact_plus_disk | L_mixed_overlay | L_clean_carrier | compact and disk supports both active; freeze decomposition before scoring | False | readout_lane_taxonomy_update_not_endpoint |

## Case Updates

| galaxy | new_lane_status | assigned_lane_for_claims | evidence | claim_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | SAME_CURVE_ADDED_SOURCE_DIAGNOSTIC_ONLY | L_added_source_diagnostic_not_endpoint | split-B2 unit-load improves q-role diagnostic but branch was identified on same curve | diagnostic q-role/source-load repair; not independent validation | False | readout_lane_taxonomy_update_not_endpoint |
| NGC5907 | PROJECTION_LANE_FAVORED_ADDED_SOURCE_REJECTED | L_projection_attenuation | negative holdout: split-B2 added-readout does not transfer to NGC5907; projection/TPG-like lane remains favored | negative split-B2 control plus projection/TPG-like lane preference | False | readout_lane_taxonomy_update_not_endpoint |
| NGC4013 | MIXED_ANALOGUE_REQUIRES_FRESH_SOURCE_FREEZE | L_mixed_overlay_pending | existing mixed reference path is retrospective; needs fresh residual-blind source freeze | secondary analogue only, not clean holdout yet | False | readout_lane_taxonomy_update_not_endpoint |
| NGC4183 | SOURCE_ACQUISITION_REQUIRED | lane_unassigned | SPARC RHI/Vflat available but galaxy-specific activation fields missing | none before source acquisition | False | readout_lane_taxonomy_update_not_endpoint |

## Gates

| gate_id | gate_status | evidence | consequence | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| RLTU_G1_SPLIT_B2_UNIVERSALITY | REJECTED_BY_CURRENT_EVIDENCE | NGC7331 positive diagnostic and NGC5907 negative holdout | do not use split-B2 as a universal forward readout formula | False | readout_lane_taxonomy_update_not_endpoint |
| RLTU_G2_LANE_SPECIFICITY | SUPPORTED_PRELIMINARY_NOT_VALIDATED | same evidence supports lane-specific interpretation | freeze readout lane before formula scoring | False | readout_lane_taxonomy_update_not_endpoint |
| RLTU_G3_PROJECTION_VS_ADDED_SEPARATION | PASS | NGC5907 projection/TPG-like readouts are strong while added split-B2 is weak | projection-dominated source evidence should veto standalone added-ramp transfer | False | readout_lane_taxonomy_update_not_endpoint |
| RLTU_G4_SUBFAMILY_LINK | PASS_CAVEATED | subfamily registry mapped to lane taxonomy; source rules still incomplete | subfamily acceptance must now also declare a readout lane | False | readout_lane_taxonomy_update_not_endpoint |
| RLTU_G5_ENDPOINT_USE | BLOCKED | taxonomy update only; no new endpoint protocol frozen | future scoring requires lane freeze plus formula freeze | False | readout_lane_taxonomy_update_not_endpoint |

## Interpretation

The taxonomy now separates source-added readouts from projection/attenuation
readouts. This is the main lesson of the split-B2 audit: NGC7331 supports a
same-curve source-load diagnostic, while NGC5907 rejects the added split-B2
lane and favors projection/TPG-like behavior. Therefore future endpoint work
must freeze the readout lane before freezing the formula.

## Claim Boundary

`readout_lane_taxonomy_update_not_endpoint`
