# NGC4088 Warp/History Accepted Endpoint Gate

This gate promotes the frozen NGC4088 warp/history formula to caveated
single-galaxy endpoint-score eligibility. It does not score the curve.

## Summary

| galaxy | accepted_readout_subfamily | formula_id | n_gates | n_pass_like | n_caveated | n_blocked | lambda_w_km2_s2 | endpoint_scores_allowed | accepted_endpoint_freeze_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | K_warp_history_caveated_protocol | NGC4088_WARP_HISTORY_FREEZE_V1 | 5 | 5 | 1 | 0 | 8795.11 | True | CAVEATED_ACCEPTED_ENDPOINT_FREEZE_READY | ngc4088_warp_history_accepted_endpoint_gate_not_score |

## Accepted Manifest

| galaxy | accepted_readout_subfamily | formula_id | source_formula_freeze_manifest | source_kernel_grid | formula_text | kernel_text | amplitude_rule | baseline_carrier | x_w_formula_freeze | q_warp | sigma_warp | vflat_km_s | lambda_w_km2_s2 | turn_on_power_frozen | formula_frozen_before_endpoint_scoring | uses_vobs_or_residual_in_construction | posthoc_retuning_allowed | endpoint_scores_allowed | caveat_b1 | caveat_b2 | caveat_b3 | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | K_warp_history_caveated_protocol | NGC4088_WARP_HISTORY_FREEZE_V1 | ngc4088_warp_history_formula_freeze_manifest.csv | ngc4088_warp_history_formula_freeze_kernel_grid.csv | v_readout^2(R)=v_Newtonian_baryonic^2(R)+lambda_w*C_warp(R/R_HI;x_w,p) | C_warp(x;x_w,p)=q_warp*max(0,(x-x_w)/(1-x_w))^p | lambda_w=sigma_warp*q_warp*x_w*Vflat^2 | v_Newtonian_baryonic | 0.298333 | 1 | 1 | 171.7 | 8795.11 | 1 | True | False | False | True | accepted for formula freeze from residual-blind WHISP graphical overview; direct source-coordinate H I/FITS product remains uncached | physical-normalization law is formula-conditional, not final Tau-side law | scale uniqueness is protocol-level, not law-level uniqueness | ngc4088_warp_history_accepted_endpoint_gate_not_score |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | N4088_AEG1_FORMULA_FROZEN | PASS | NGC4088_WARP_HISTORY_FORMULA_FREEZE_READY_LAW_CAVEATED_NOT_SCORE | none for endpoint scoring; law-level caveats remain | True | ngc4088_warp_history_accepted_endpoint_gate_not_score |
| NGC4088 | N4088_AEG2_DASHBOARD_READY | PASS | FORMULA_FREEZE_READY_ENDPOINT_GATE_REQUIRED | none if dashboard says endpoint gate required | True | ngc4088_warp_history_accepted_endpoint_gate_not_score |
| NGC4088 | N4088_AEG3_ENDPOINT_BLIND_CONSTRUCTION | PASS | frozen manifest/kernel grid do not use vobs or residuals | scoring script may read vobs only after this gate | True | ngc4088_warp_history_accepted_endpoint_gate_not_score |
| NGC4088 | N4088_AEG4_CAVEATS_DECLARED | PASS_CAVEATED | B1 graphical WHISP caveat, B2 law-level open, B3 law-level open | claim must remain preliminary single-galaxy control | True | ngc4088_warp_history_accepted_endpoint_gate_not_score |
| NGC4088 | N4088_AEG5_NO_RETUNING_RULE | PASS | posthoc_retuning_allowed=False; p=1 and lambda_w are frozen before scoring | changing p, sign, carrier, x_w, or lambda after scoring demotes the row to diagnostic | True | ngc4088_warp_history_accepted_endpoint_gate_not_score |

## Claim Boundary

This is a caveated accepted endpoint gate. The next scoring script must
read the frozen formula unchanged. The result may be reported only as a
single-galaxy preliminary control endpoint, not as empirical validation.
