# UGC03580 / UGC3580 unchanged NGC4088-class transfer endpoint v01

Status: `RETROSPECTIVE_CLASS_TRANSFER_REJECTS_UNCAPPED_UNIVERSAL_LAW`

The Jozsa warp onset and unchanged NGC4088 formula were frozen by a
separate script before this scorer opened the local pointwise endpoint.
Because UGC03580 was used in earlier repository endpoint analyses, this is
a retrospective replication rather than a prospective blind prediction.

## Full-endpoint scores

| model_id | role | valid_full_endpoint | rmse_km_s | bias_km_s | chi2_per_point | endpoint_fit_parameters | imported_summary_scalars |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PSEUDO_ISOTHERMAL_TWO_PARAMETER_ENDPOINT_FIT | fit_aided_standard_comparator | True | 14.9891 | 8.41415 | 20.2567 | 2 | 0 |
| NFW_TWO_PARAMETER_ENDPOINT_FIT | fit_aided_standard_comparator | True | 17.392 | 10.3739 | 29.5881 | 2 | 0 |
| CONTROL_WRONG_UGC08490_ONSET | morphology_control | True | 24.557 | -5.09768 | 186.584 | 0 | 2 |
| CONTROL_WRONG_NGC4088_ONSET | morphology_control | True | 25.2919 | -6.14747 | 194.46 | 0 | 2 |
| TPG_V6_FIXED | fixed_standard_comparator | True | 25.4945 | 19.6321 | 78.7312 | 0 | 0 |
| MOND_FIXED_A0 | fixed_standard_comparator | True | 27.1727 | 22.8705 | 94.3758 | 0 | 0 |
| TAU_WARP_TRANSFER_SOURCE_HI_DENOMINATOR_SENSITIVITY | predeclared_sensitivity | True | 27.6774 | -3.32955 | 266.367 | 0 | 2 |
| NEWTONIAN_BARYONIC | fixed_standard_comparator | True | 36.012 | -12.8175 | 434.291 | 0 | 0 |
| TAU_WARP_TRANSFER_SOURCE_SPEED_SENSITIVITY | predeclared_sensitivity | True | 36.1659 | -1.91191 | 434.19 | 0 | 1 |
| TAU_WARP_TRANSFER_PRIMARY | matched_frozen_transfer | True | 38.0353 | -1.01221 | 471.926 | 0 | 2 |
| CONTROL_WRONG_P2 | morphology_control | True | 80.5607 | 9.35439 | 1839.75 | 0 | 2 |
| CONTROL_WRONG_SIGN | morphology_control | False |  |  |  | 0 | 2 |

## Radial-zone scores

| zone | model_id | n_points | rmse_km_s | bias_km_s |
| --- | --- | --- | --- | --- |
| pre_onset | TAU_WARP_TRANSFER_PRIMARY | 42 | 28.7422 | -5.72609 |
| pre_onset | TAU_WARP_TRANSFER_SOURCE_HI_DENOMINATOR_SENSITIVITY | 42 | 27.5423 | -5.04256 |
| pre_onset | CONTROL_WRONG_NGC4088_ONSET | 42 | 23.7563 | -2.67767 |
| pre_onset | CONTROL_WRONG_UGC08490_ONSET | 42 | 24.8376 | -3.30882 |
| pre_onset | NEWTONIAN_BARYONIC | 42 | 28.7422 | -5.72609 |
| pre_onset | MOND_FIXED_A0 | 42 | 28.7122 | 25.1745 |
| pre_onset | TPG_V6_FIXED | 42 | 26.8436 | 22.8153 |
| onset_to_RHI | TAU_WARP_TRANSFER_PRIMARY | 2 | 45.0944 | -34.4447 |
| onset_to_RHI | TAU_WARP_TRANSFER_SOURCE_HI_DENOMINATOR_SENSITIVITY | 2 | 15.5564 | -14.2571 |
| onset_to_RHI | CONTROL_WRONG_NGC4088_ONSET | 2 | 38.5671 | -38.5644 |
| onset_to_RHI | CONTROL_WRONG_UGC08490_ONSET | 2 | 27.4628 | -27.4555 |
| onset_to_RHI | NEWTONIAN_BARYONIC | 2 | 68.5961 | -68.5631 |
| onset_to_RHI | MOND_FIXED_A0 | 2 | 4.32394 | 4.1772 |
| onset_to_RHI | TPG_V6_FIXED | 2 | 4.58375 | -4.29802 |
| beyond_RHI | TAU_WARP_TRANSFER_PRIMARY | 3 | 98.709 | 87.2703 |
| beyond_RHI | TAU_WARP_TRANSFER_SOURCE_HI_DENOMINATOR_SENSITIVITY | 3 | 34.9263 | 27.9377 |
| beyond_RHI | CONTROL_WRONG_NGC4088_ONSET | 3 | 33.5997 | -33.1133 |
| beyond_RHI | CONTROL_WRONG_UGC08490_ONSET | 3 | 17.5553 | -15.2366 |
| beyond_RHI | NEWTONIAN_BARYONIC | 3 | 74.9335 | -74.9334 |
| beyond_RHI | MOND_FIXED_A0 | 3 | 3.69758 | 3.07726 |
| beyond_RHI | TPG_V6_FIXED | 3 | 8.98525 | -8.97987 |
| within_RHI_all | TAU_WARP_TRANSFER_PRIMARY | 44 | 29.6815 | -7.03148 |
| within_RHI_all | TAU_WARP_TRANSFER_SOURCE_HI_DENOMINATOR_SENSITIVITY | 44 | 27.1127 | -5.4614 |
| within_RHI_all | CONTROL_WRONG_NGC4088_ONSET | 44 | 24.6236 | -4.30889 |
| within_RHI_all | CONTROL_WRONG_UGC08490_ONSET | 44 | 24.9629 | -4.40639 |
| within_RHI_all | NEWTONIAN_BARYONIC | 44 | 31.6614 | -8.58232 |
| within_RHI_all | MOND_FIXED_A0 | 44 | 28.0672 | 24.22 |
| within_RHI_all | TPG_V6_FIXED | 44 | 26.2447 | 21.5829 |

## Decisive checks

- source-frozen onset: `x_w=0.904564` or `18.064 kpc`;
- endpoint-informed preferred onset (diagnostic only): `x_w=0.400000`;
- primary full RMSE: `38.0353 km/s`;
- primary within-R_HI RMSE: `29.6815 km/s`;
- Newtonian full RMSE: `36.0120 km/s`;
- fixed MOND full/within-R_HI RMSE: `27.1727` / `28.0672 km/s`;
- wrong UGC08490-onset full RMSE: `24.5570 km/s`;
- best two-parameter halo RMSE: `14.9891 km/s`.

## Verdict

The source-correct UGC03580 onset does not replicate the NGC4088 class-law success. It improves the Newtonian comparison inside R_HI only modestly, loses to fixed MOND there, loses to earlier wrong-onset controls, and the unchanged uncapped kernel overshoots beyond R_HI. This rejects the current one-component uncapped law as a universal warp-class rotation law; it does not reject source-native warp morphology or Tau Core in general.
The three points beyond the catalog R_HI expose an additional structural
failure: the unchanged linear kernel is uncapped and grows without a
source-supported outer saturation rule. Adding a cap now would be a new
law, not a repair of this endpoint. It must be derived source-side and then
tested on another target.

Claim boundary: `retrospective_class_replication_negative_not_tau_falsification`.
