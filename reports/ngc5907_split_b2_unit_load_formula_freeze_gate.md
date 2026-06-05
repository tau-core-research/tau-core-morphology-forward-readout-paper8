# NGC5907 Split-B2 Unit-Load Formula Freeze Gate

Status: `NGC5907_SPLIT_B2_UNIT_LOAD_FORMULA_FREEZE_CAVEATED_READY_NOT_SCORED`

This gate freezes the NGC5907 split-B2 unit-load formula candidate before any
split-B2 scoring. The construction reads only source fields and the
Newtonian-carrier grid (`r`, `vn`); it does not read observed velocities.

## Summary

| galaxy | formula_id | formula_freeze_status | r_outer_kpc | x_w_formula_freeze | vflat_km_s | mu_load | lambda_split_km2_s2 | n_kernel_grid_rows | n_gates | n_pass_like | n_caveated | endpoint_scores_allowed | uses_vobs_or_residual_in_construction | future_separate_scoring_gate_required | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_SPLIT_B2_UNIT_LOAD_FREEZE_CAVEATED_V1 | NGC5907_SPLIT_B2_UNIT_LOAD_FORMULA_FREEZE_CAVEATED_READY_NOT_SCORED | 24 | 0.554167 | 215 | 1 | 25616.4 | 19 | 5 | 5 | 3 | False | False | True | ngc5907_split_b2_unit_load_formula_freeze_caveated_not_score |

## Frozen Manifest

| galaxy | formula_id | readout_family | independent_holdout_selector_status | carrier | formula_text | delta_text | kernel_text | source_load_text | denominator_id | denominator_caveat | r_outer_kpc | x_w_formula_freeze | vflat_km_s | sigma_warp | mu_load | lambda_split_km2_s2 | turn_on_power_frozen | dimension_check | inactive_window_limit | zero_source_limit | ngc7331_diagnostic_branch_relation | uses_vobs_or_residual_in_construction | formula_frozen_before_split_b2_scoring | endpoint_scores_allowed | future_separate_scoring_gate_required | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_SPLIT_B2_UNIT_LOAD_FREEZE_CAVEATED_V1 | K_warp_history_split_b2_unit_load | P0_PREDECLARED_SPLIT_B2_HOLDOUT_CANDIDATE_RHI_BLOCKED_OR_CAVEATED | v_Newtonian_baryonic | v_readout^2(R)=v_Newtonian_baryonic^2(R)+sigma_warp*mu_load*x_w*Vflat^2*ramp(R/R_outer;x_w) | Delta v^2_split(R)=sigma_warp*mu_load*x_w*Vflat^2*max(0,(R/R_outer-x_w)/(1-x_w)) | K_shape=ramp=max(0,(x-x_w)/(1-x_w)) | mu_load=1 conditional normalized split-load coordinate | D1_SOURCE_OPTICAL_WARP_OUTER_EDGE | uses source-native optical warp outer support, not SPARC HI radius | 24 | 0.554167 | 215 | 1 | 1 | 25616.4 | 1 | PASS: sigma, mu_load, x_w, and ramp are dimensionless; Vflat^2 supplies km^2/s^2 | PASS: R/R_outer<=x_w implies ramp=0 and carrier recovery | PASS: sigma_warp=0 or mu_load=0 gives Delta v^2=0 | same split-B2 unit-load shell, but frozen here before NGC5907 split-B2 scoring | False | True | False | True | ngc5907_split_b2_unit_load_formula_freeze_caveated_not_score |

## Source Fields

| field_id | observable | value | unit | status | role |
| --- | --- | --- | --- | --- | --- |
| SB2D1_WARP_START | optical_warp_start_radius | 13.3 | kpc | ACCEPTED_NUMERIC_SOURCE_FIELD | sets split-B2 turn-on numerator R_warp_start |
| SB2D2_WARP_OUTER_SUPPORT | optical_warp_outer_support_radius | 24 | kpc | PASS_CAVEATED_SOURCE_NATIVE_DENOMINATOR | sets split-B2 denominator R_outer when SPARC RHI is missing |
| SB2D3_SOURCE_XW | x_w_source_window | 0.554167 | dimensionless | DERIVED_FROM_SOURCE_WINDOW | defines ramp start in source-window coordinate |
| SB2D4_VFLAT | Vflat | 215 | km/s | SPARC_SOURCE_CATALOG_AVAILABLE | sets velocity-squared carrier scale Vflat^2 |
| SB2D5_WARP_DISPLACEMENT_CONTEXT | optical_warp_max_displacement | 1.7 | kpc | ACCEPTED_NUMERIC_SOURCE_FIELD_CONTEXT_ONLY | supports projection/warp context; not used as denominator |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N5907_SB2F1_HOLDOUT_SELECTOR | PASS_CAVEATED | P0_PREDECLARED_SPLIT_B2_HOLDOUT_CANDIDATE_RHI_BLOCKED_OR_CAVEATED | separate scoring gate must preserve caveated status |
| N5907_SB2F2_DENOMINATOR | PASS_CAVEATED | NGC5907_SPLIT_B2_DENOMINATOR_GATE_PASS_CAVEATED_NOT_ENDPOINT | replace with source-native HI denominator if acquired later |
| N5907_SB2F3_SOURCE_FIELDS | PASS_CAVEATED | warp start, outer support, x_w, Vflat frozen from source/catalog fields | do not reinterpret optical outer support as HI extent |
| N5907_SB2F4_DIMENSIONS_LIMITS | PASS | velocity-squared units and inactive/zero-source limits pass | none at formula-shell level |
| N5907_SB2F5_ENDPOINT_BLINDNESS | PASS | construction reads r and vn only; no vobs/residual columns | future scoring script must read this manifest unchanged |

## Formula

`v_readout^2(R)=v_Newtonian_baryonic^2(R)+sigma_warp*mu_load*x_w*Vflat^2*ramp(R/R_outer;x_w)`

with:

- `R_outer = 24 kpc`
- `x_w = 0.554167`
- `Vflat = 215 km/s`
- `mu_load = 1`
- `lambda_split = 25616.4 km^2/s^2`

## Claim Boundary

This is a caveated, pre-scoring formula freeze. It is not an endpoint result.
The caveat is that `R_outer` is the source-native optical warp outer support
radius, not a SPARC/HI radius.

`ngc5907_split_b2_unit_load_formula_freeze_caveated_not_score`
