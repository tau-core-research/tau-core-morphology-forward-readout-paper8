# NGC5907 Split-B2 Denominator Gate

Status: `NGC5907_SPLIT_B2_DENOMINATOR_GATE_PASS_CAVEATED_NOT_ENDPOINT`

This gate freezes the radial-coordinate denominator needed by a future NGC5907
split-B2 holdout formula. It does not score an endpoint.

## Summary

| galaxy | denominator_gate_status | selected_denominator_id | selected_r_outer_kpc | x_w_source_window | warp_span_kpc | sparc_rhi_kpc | vflat_km_s | n_candidates | n_gates | n_pass_like | n_blocked | formula_freeze_allowed_next | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | NGC5907_SPLIT_B2_DENOMINATOR_GATE_PASS_CAVEATED_NOT_ENDPOINT | D1_SOURCE_OPTICAL_WARP_OUTER_EDGE | 24 | 0.554167 | 10.7 | 0 | 215 | 3 | 5 | 4 | 1 | True | False | False | ngc5907_split_b2_denominator_gate_not_endpoint |

## Denominator Candidates

| denominator_id | r_outer_kpc | x_w | status | interpretation | caveat |
| --- | --- | --- | --- | --- | --- |
| D0_SPARC_RHI | 0 | <NA> | BLOCKED_SPARC_RHI_ZERO_OR_MISSING | clean HI support denominator if nonzero | blocked for this galaxy because SPARC RHI_kpc=0 |
| D1_SOURCE_OPTICAL_WARP_OUTER_EDGE | 24 | 0.5541666666666667 | PASS_CAVEATED_SOURCE_NATIVE_DENOMINATOR | outer edge of the source-native optical warp support window | optical warp support denominator, not HI extent; use only as predeclared caveated holdout route |
| D2_DISK_SCALE_LENGTH | 5.34 | 2.4906367041198503 | REJECTED_WRONG_ROLE | disk scale, not outer support radius | would make x_w>1 and inactive-window semantics fail |

## Frozen Source Fields

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
| SB2D_G1_SELECTOR | PASS_CAVEATED | P0_PREDECLARED_SPLIT_B2_HOLDOUT_CANDIDATE_RHI_BLOCKED_OR_CAVEATED | denominator must be frozen before formula scoring |
| SB2D_G2_SPARC_RHI_ROUTE | BLOCKED | SPARC RHI_kpc=0 | do not use SPARC RHI for NGC5907 split-B2 |
| SB2D_G3_SOURCE_NATIVE_DENOMINATOR | PASS_CAVEATED | Sasaki optical warp source window 13.3-24 kpc | mark endpoint as caveated unless a source-native HI denominator is acquired |
| SB2D_G4_DIMENSIONAL_AND_LIMITS | PASS | x_w=0.554167 is dimensionless and lies in (0,1) | none at radial-coordinate level |
| SB2D_G5_ENDPOINT_BLINDNESS | PASS | uses SPARC catalog and source-field freeze only; no vobs/residual columns | future scoring must read a formula freeze manifest unchanged |

## Interpretation

The clean SPARC-RHI route is blocked because the NGC5907 SPARC row has
`RHI_kpc=0`. A caveated residual-blind denominator is nevertheless available
from the source-native optical warp support window: the Sasaki source gives the
warp from 13.3 to 24.0 kpc, so the split-B2 coordinate can be frozen as
`x_w = 13.3 / 24.0 = 0.554167`.

This is not the same as an HI support radius. Therefore any split-B2 NGC5907
formula using this denominator must be labelled caveated and predeclared before
scoring.

## Claim Boundary

`ngc5907_split_b2_denominator_gate_not_endpoint`
