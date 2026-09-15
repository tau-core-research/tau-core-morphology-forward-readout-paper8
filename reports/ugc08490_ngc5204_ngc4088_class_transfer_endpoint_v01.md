# UGC08490 / NGC5204 unchanged NGC4088-class transfer endpoint v01

Status: `RETROSPECTIVE_CLASS_TRANSFER_NEGATIVE`

The source-side formula and target parameters were frozen and hashed before
this script opened the pointwise SPARC endpoint. UGC08490 had nevertheless
been inspected in earlier, different tracer analyses, so this remains a
retrospective transfer test.

## Model scores

| model_id | role | valid_full_endpoint | rmse_km_s | bias_km_s | chi2_per_point | endpoint_fit_parameters | imported_summary_scalars |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NFW_TWO_PARAMETER_ENDPOINT_FIT | fit_aided_standard_comparator | True | 1.1953 | 0.0434881 | 0.104931 | 2 | 0 |
| PSEUDO_ISOTHERMAL_TWO_PARAMETER_ENDPOINT_FIT | fit_aided_standard_comparator | True | 1.54797 | -0.0253448 | 0.175983 | 2 | 0 |
| MOND_FIXED_A0 | fixed_standard_comparator | True | 8.78205 | -8.18912 | 5.6642 | 0 | 0 |
| TPG_V6_FIXED | fixed_standard_comparator | True | 12.7501 | -12.6082 | 11.9391 | 0 | 0 |
| TAU_WARP_TRANSFER_SOURCE_SPEED_SENSITIVITY | predeclared_sensitivity | True | 28.9461 | -26.2109 | 61.5358 | 0 | 1 |
| TAU_WARP_TRANSFER_PRIMARY | matched_frozen_transfer | True | 29.7035 | -27.4499 | 64.7982 | 0 | 2 |
| CONTROL_WRONG_NGC4088_ONSET | morphology_control | True | 31.6406 | -30.8969 | 73.5254 | 0 | 2 |
| CONTROL_WRONG_P2 | morphology_control | True | 31.9043 | -27.7252 | 74.7557 | 0 | 2 |
| NEWTONIAN_BARYONIC | fixed_standard_comparator | True | 44.8712 | -44.0553 | 147.871 | 0 | 0 |
| CONTROL_WRONG_SIGN | morphology_control | False |  |  |  | 0 | 2 |

## Radial diagnosis

| zone | model_id | n_points | rmse_km_s | bias_km_s |
| --- | --- | --- | --- | --- |
| pre_onset | TAU_WARP_TRANSFER_PRIMARY | 10 | 35.8329 | -34.7575 |
| pre_onset | MOND_FIXED_A0 | 10 | 11.3893 | -11.128 |
| pre_onset | TPG_V6_FIXED | 10 | 12.5637 | -12.2613 |
| post_onset | TAU_WARP_TRANSFER_PRIMARY | 20 | 26.1046 | -23.7961 |
| post_onset | MOND_FIXED_A0 | 20 | 7.12943 | -6.71968 |
| post_onset | TPG_V6_FIXED | 20 | 12.8423 | -12.7816 |

## Decisive checks

- frozen source-correct onset: `x_w=0.450876`;
- endpoint-informed preferred onset (diagnostic only): `x_w=0.493695`;
- frozen transfer RMSE: `29.7035 km/s`;
- fixed MOND RMSE: `8.7820 km/s`;
- wrong NGC4088-onset control RMSE: `31.6406 km/s`;
- best two-parameter halo-fit RMSE: `1.1953 km/s`;
- matched transfer beats fixed MOND: `False`;
- matched transfer beats the wrong-onset control: `True`.

The block-bootstrap comparison is descriptive because radial points and the
catalog `Vflat` input are not independent. Its role is robustness auditing,
not a discovery p-value.

## Interpretation

The source-correct outer-warp law does not transfer as a complete rotation-law explanation if it fails the fixed MOND and wrong-onset controls. This is a negative result for the current universal class-law transfer, not a falsification of Tau Core or of morphology-conditioned readouts in general.
The failure mode is physically informative: the promoted warp begins only
after the large inner baryonic discrepancy is already present. Therefore an
outer-warp body can be a genuine morphology component without being the
complete carrier of the galaxy's rotation discrepancy.

No endpoint-informed repair is promoted. Any revised body/readout law must be
derived and tested on a new target.

Claim boundary: `retrospective_single_galaxy_class_transfer_negative_not_tau_falsification`.
