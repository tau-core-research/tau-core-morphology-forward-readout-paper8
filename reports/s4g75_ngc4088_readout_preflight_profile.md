# NGC4088 Readout Preflight Profile

This report exports the NGC4088-specific readout candidate on the local
SPARC/TPG point radii. It is not a fit or endpoint score.

## Verdict

The filled NGC4088 source-side lane can now be evaluated as a concrete
radial candidate profile. This is still a profile export only: it does not
decide whether the law is correct or whether it beats any baseline.

## Summary

| galaxy | n_points | r_hi_kpc | max_delta_v2_p1 | max_delta_v2_p2 | max_v_candidate_p1 | max_v_candidate_p2 | profile_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | 12 | 22.253 | 7921.12 | 7630.51 | 190.381 | 189.582 | PREDECLARED_READOUT_EXPORT_NOT_ENDPOINT | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |

## First Rows

| galaxy | split | r | x_R_over_RHI | vn | v_v6 | v_mond | vobs | delta_v2_warp_candidate_p1 | delta_v2_warp_candidate_p2 | v_warp_candidate_p1 | v_warp_candidate_p2 | uses_vobs_for_generation | endpoint_scores_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | holdout | 1.74 | 0.0781918 | 96.9585 | 115.178 | 117.441 | 84.9 | 0 | 0 | 96.9585 | 96.9585 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 3.5 | 0.157282 | 127.47 | 154.382 | 157.338 | 136 | 0 | 0 | 127.47 | 127.47 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 5.24 | 0.235474 | 171.208 | 202.518 | 206.514 | 162 | 0 | 0 | 171.208 | 171.208 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 6.98 | 0.313666 | 189.424 | 226.419 | 230.837 | 179 | 363.203 | 59.5415 | 190.381 | 189.582 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 8.72 | 0.391858 | 177.32 | 222.421 | 226.388 | 182 | 1270.15 | 208.222 | 180.866 | 177.907 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 10.47 | 0.470499 | 169.962 | 222.034 | 225.594 | 179 | 2182.32 | 719.7 | 176.265 | 172.066 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 12.19 | 0.547792 | 163.94 | 222.109 | 225.323 | 174 | 3078.84 | 1263.49 | 173.076 | 167.749 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 13.94 | 0.626434 | 151.086 | 215.382 | 218.145 | 171 | 3991 | 1987.67 | 163.762 | 157.526 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 15.68 | 0.704625 | 141.233 | 210.57 | 213.157 | 168 | 4897.95 | 3043.3 | 157.622 | 151.624 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 17.42 | 0.782817 | 133.58 | 207.122 | 209.765 | 165 | 5804.9 | 4098.93 | 153.781 | 148.13 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 19.28 | 0.866402 | 126.405 | 203.716 | 206.629 | 171 | 6774.4 | 5656.65 | 150.84 | 147.088 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |
| NGC4088 | holdout | 21.48 | 0.965265 | 118.916 | 199.86 | 203.334 | 174 | 7921.12 | 7630.51 | 148.533 | 147.552 | False | False | False | s4g75_ngc4088_readout_preflight_profile_not_endpoint |

## Claim Boundary

The observed velocity columns are carried only as contextual source-package
fields. They are not used to generate the candidate profile in this
artifact, and this report does not compute an endpoint score or a fit
quality judgment.
