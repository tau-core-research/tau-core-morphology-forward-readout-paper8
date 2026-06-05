# NGC5907 Split-B2 Failure Mode Audit

Status: `NGC5907_SPLIT_B2_NEGATIVE_RESULT_FAILURE_MODE_AUDIT_COMPLETE`

This audit preserves the negative split-B2 result. It does not tune a new
formula.

## Summary

| galaxy | failure_audit_status | split_b2_rmse_km_s | best_baseline_model | best_baseline_rmse_km_s | best_existing_tau_context_model | best_existing_tau_context_rmse_km_s | primary_interpretation | formula_tuned | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_SPLIT_B2_NEGATIVE_RESULT_FAILURE_MODE_AUDIT_COMPLETE | 62.0882 | TPG_V6_v_v6 | 16.7855 | TAU_NGC5907_PROJECTION_ACCEPTED | 15.4952 | negative holdout: split-B2 added-readout does not transfer to NGC5907; projection/TPG-like lane remains favored | False | False | ngc5907_split_b2_failure_mode_audit_not_formula_tuning |

## Radial Zones

| galaxy | radial_zone | n_points | r_min_kpc | r_max_kpc | mean_kernel_ramp | split_b2_rmse_km_s | projection_rmse_km_s | tpg_v6_rmse_km_s | newtonian_rmse_km_s | split_b2_mean_bias_km_s | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | inner_inactive_ramp | 4 | 5.03 | 12.58 | 0 | 76.5089 | 32.516 | 32.516 | 76.5089 | -76.2069 | ngc5907_split_b2_failure_mode_audit_not_formula_tuning |
| NGC5907 | source_warp_window | 4 | 15.1 | 22.65 | 0.520794 | 39.7999 | 3.20103 | 4.76517 | 74.2457 | -36.4311 | ngc5907_split_b2_failure_mode_audit_not_formula_tuning |
| NGC5907 | beyond_source_window | 11 | 25.16 | 50.33 | 2.28462 | 62.8804 | 5.15034 | 9.69225 | 93.7333 | 53.1842 | ngc5907_split_b2_failure_mode_audit_not_formula_tuning |

## Failure Modes

| failure_mode | evidence | affected_zone | formula_implication | not_a_tuning_instruction | galaxy | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| INNER_CARRIER_UNDERPREDICTION | For R<R_warp_start the ramp is zero, so split-B2 reduces to the Newtonian carrier; NGC5907 requires a strong non-Newtonian/projection-like carrier already in this region. | inner_inactive_ramp | standalone Newtonian+added split-B2 is the wrong readout class | True | NGC5907 | ngc5907_split_b2_failure_mode_audit_not_formula_tuning |
| OUTER_ADDED_READOUT_OVERBOOST | Beyond the source optical warp window the linear ramp continues above unity and the added velocity-squared term overshoots. | beyond_source_window | NGC5907 prefers bounded projection/attenuation behavior, not an unbounded added warp-history ramp | True | NGC5907 | ngc5907_split_b2_failure_mode_audit_not_formula_tuning |
| MORPHOLOGY_LANE_MISMATCH | Existing projection and TPG-like baselines remain strong while split-B2 added readout fails. | global | NGC5907 supports projection-dominated readout classification over split-B2 added-readout transfer | True | NGC5907 | ngc5907_split_b2_failure_mode_audit_not_formula_tuning |

## Interpretation

The failed split-B2 holdout is informative. NGC5907 already needs a strong
projection/TGP-like carrier in the inner region where the split-B2 ramp is
inactive. In the outer region the added ramp overboosts. This points away from
an added warp-history readout and toward a bounded projection/attenuation
readout for this galaxy.

## Claim Boundary

`ngc5907_split_b2_failure_mode_audit_not_formula_tuning`
