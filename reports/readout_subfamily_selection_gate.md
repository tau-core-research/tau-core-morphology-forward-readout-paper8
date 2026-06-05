# Readout-Subfamily Selection Gate

This gate records the next refinement implied by the multi-galaxy atlas:
coarse projected 4D morphology families are useful handles, but they are
not always the final Tau Core readout classes. A galaxy may require a
readout-relevant subfamily selected by residual-blind source observables.

## Gate Status

| gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| RSF1_COARSE_FAMILY_NOT_FINAL_READOUT | PASS | K_obs and K_readout are already separated; 4D projected morphology is not automatically the Tau-side readout class | keep parent-family labels as handles, not final physical taxonomy | False | readout_subfamily_selection_gate_not_endpoint |
| RSF2_SUBFAMILY_MOTIVATED_BY_STRESS_CASE | PASS | NGC4088 generic family RMSE exceeds targeted warp bounded RMSE by 30.8843 km/s | repeat on multiple warp/history-rich galaxies | False | readout_subfamily_selection_gate_not_endpoint |
| RSF3_RESIDUAL_BLIND_SUBFAMILY_OBSERVABLES | PENDING | registry lists required source observables for each subfamily | fill accepted residual-blind subfamily observables before endpoint use | False | readout_subfamily_selection_gate_not_endpoint |
| RSF4_NO_ENDPOINT_SUBFAMILY_SELECTION | PASS | best Tau family/subfamily rows remain diagnostic-only and are not promoted to accepted labels | freeze subfamily selection rule before future endpoint scoring | False | readout_subfamily_selection_gate_not_endpoint |

## NGC4088 Stress Case

| galaxy | coarse_parent_family | motivated_subfamily | generic_tau_matched_rmse_kms | best_generic_baseline_model | best_generic_baseline_rmse_kms | targeted_warp_fixed_tau_rmse_kms | targeted_warp_bounded_tau_rmse_kms | diagnostic_delta_generic_minus_targeted_bounded_kms | interpretation | endpoint_scores_allowed | validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | K_thick_flared | K_warp_history_coupled | 37.8114 | NEWTONIAN_vn | 25.3963 | 12.1897 | 6.92711 | 30.8843 | coarse_family_insufficient_correct_subfamily_matters | False | False | readout_subfamily_selection_gate_not_endpoint |

## Subfamily Registry

| parent_family | subfamily | readout_interpretation | required_residual_blind_observables | candidate_formula_layer | current_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| K_thick_flared | K_thick_regular | smooth vertically extended disk without strong warp/history coupling | vertical scale height or edge-on thickness; low warp/asymmetry evidence; projection-safe inclination | thick/flared damped vertical kernel | candidate_subfamily_pending_source_rule | False | readout_subfamily_selection_gate_not_endpoint |
| K_thick_flared | K_flared_outer_disk | outer disk flaring modulates vertical readout in the outskirts | outer thickness/flare gradient; HI extent; projection caveat audit | radially varying thick/flared kernel | candidate_subfamily_pending_source_rule | False | readout_subfamily_selection_gate_not_endpoint |
| K_thick_flared | K_warp_history_coupled | warp/history/background morphology layer cross-couples into the 4D readout | warp onset; warp asymmetry; HI disturbance; interaction/memory evidence; epsilon_cross source bound | warp p1/p2 branch plus bounded epsilon_cross modulation | motivated_by_NGC4088_targeted_diagnostic_not_accepted_endpoint | False | readout_subfamily_selection_gate_not_endpoint |
| K_thick_flared | K_projection_dominated | apparent thickness/flare is dominated by viewing/projection uncertainty | edge-on geometry; inclination uncertainty; dust lane/projection flags; velocity-field sanity check | projection-corrected or endpoint-blocked thick/flared shell | control_or_blocker_subfamily | False | readout_subfamily_selection_gate_not_endpoint |
| K_scale_tail_spiral | K_smooth_n2_tail | smooth source-tail branch with n=2 TGP-like asymptotic form | HI radius; outer-disk/tail transition; stable tail support | n=2 scale-tail readout | candidate_subfamily_pending_source_rule | False | readout_subfamily_selection_gate_not_endpoint |
| K_scale_tail_spiral | K_disturbed_outer_tail | asymmetric or environmentally disturbed outer tail | HI asymmetry; outer lopsidedness; environment/interaction evidence | tail plus memory/asymmetry modulation | candidate_subfamily_pending_source_rule | False | readout_subfamily_selection_gate_not_endpoint |
| K_exponential_disk | K_clean_expdisk | present-day exponential disk is a close proxy for readout-relevant morphology | S4G/SPARC scale radius; no strong bar/ring/projection caveat; stable disk component | Freeman/Bessel exponential-disk shell | candidate_subfamily_pending_source_rule | False | readout_subfamily_selection_gate_not_endpoint |
| K_exponential_disk | K_expdisk_overlay | exponential disk with bar, compact core, projection, or memory/history overlay | bar/core/projection/history flags; overlay source support | exponential shell plus overlay component | candidate_subfamily_pending_source_rule | False | readout_subfamily_selection_gate_not_endpoint |
| K_compact_finite | K_true_compact | compact finite source dominates the readout support | bulge/core support; compact scale; limited extended disk influence | compact finite-source exterior response | candidate_subfamily_pending_source_rule | False | readout_subfamily_selection_gate_not_endpoint |
| K_compact_finite | K_compact_plus_disk | compact core exists but extended disk/tail still controls part of readout | bulge-to-disk decomposition; disk scale; compact support radius | compact shell plus disk/tail overlay | candidate_subfamily_pending_source_rule | False | readout_subfamily_selection_gate_not_endpoint |

## Claim Boundary

This is a protocol and taxonomy refinement, not an endpoint score. The
NGC4088 comparison motivates the subfamily layer because the generic
thick/flared family is weak while the targeted warp/history branch is
strong. The subfamily cannot be accepted until selected by residual-blind
observables and repeated on a larger matched set.
