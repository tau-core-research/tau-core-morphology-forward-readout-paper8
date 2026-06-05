# Tau-Side E_tau L2 Endpoint Preflight

This preflight replaces the fixed proxy-bin source-evidence gate with
the residual-blind E_tau(g,K) evidence-measure candidate. It is not a
model-selection step and not validation.

## Holdout Verdict

- Holdout galaxies: 44
- Beats old L2 intake endpoint: 0.568
- Beats TPG/v6: 0.455
- Beats MOND: 0.545
- Median E_tau-minus-old-L2 RMSE: -0.236283

## Summary

| split | n_galaxies | median_rmse_tau_source_normalized_l2 | beats_old_l2_intake_fraction | beats_tpg_v6_fraction | beats_mond_fraction | median_source_norm_minus_old_l2_intake | median_source_norm_minus_tpg_v6 | median_source_norm_minus_mond | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | 44 | 14.1102 | 0.568182 | 0.454545 | 0.545455 | -0.236283 | 0.0663734 | -0.25148 | tau_side_evidence_measure_l2_endpoint_preflight_not_validation |
| train | 131 | 11.7901 | 0.549618 | 0.458015 | 0.48855 | -0.159714 | 0.220372 | 0.114766 | tau_side_evidence_measure_l2_endpoint_preflight_not_validation |

## Claim Boundary

This test uses E_tau as a candidate evidence measure. The conservative
proxy-bin ladder is derived inside the current Tau-side
readout-admission geometry, but the per-galaxy and per-component q_i
assignments are not yet accepted source-native observables. A better
or worse endpoint result must not be used to choose the evidence
measure or the q_i assignments.
