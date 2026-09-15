# UGC03580 signed-descriptor standard projection control score v01

| status | n_points | best_model | projection_factor_min | projection_factor_max | construction_used_vobs_or_residual | scoring_used_vobs |
| --- | --- | --- | --- | --- | --- | --- |
| DIAGNOSTIC_STANDARD_PROJECTION_CONTROL_SCORED_NOT_TAU_ENDPOINT | 47 | TPG_V6_UNCORRECTED | 1.03166 | 1.08295 | False | True |

## Carrier comparison

| carrier | rmse_uncorrected_km_s | rmse_projection_control_km_s | delta_rmse_projection_minus_uncorrected_km_s | projection_improves_rmse |
| --- | --- | --- | --- | --- |
| NEWTONIAN | 36.012 | 35.3948 | -0.617205 | True |
| TPG_V6 | 25.4945 | 28.5964 | 3.10188 | False |
| MOND | 27.1727 | 30.7036 | 3.53085 | False |

## All declared models

| model_id | role | valid_full_endpoint | n_points | rmse_km_s | mae_km_s | bias_km_s | chi2 | chi2_per_point | aic_known_errors | bic_known_errors | endpoint_fit_parameters | imported_summary_scalars | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TPG_V6_UNCORRECTED | fixed_baseline | True | 47 | 25.4945 | 21.7887 | 19.6321 | 3700.37 | 78.7312 | 3700.37 | 3700.37 | 0 | 0 | ugc03580_standard_projection_systematics_control_not_tau_endpoint |
| MOND_UNCORRECTED | fixed_baseline | True | 47 | 27.1727 | 23.4837 | 22.8705 | 4435.66 | 94.3758 | 4435.66 | 4435.66 | 0 | 0 | ugc03580_standard_projection_systematics_control_not_tau_endpoint |
| TPG_V6_SOURCE_PROJECTION_CONTROL | standard_projection_systematics_control | True | 47 | 28.5964 | 24.7311 | 23.7188 | 4940.05 | 105.107 | 4940.05 | 4940.05 | 0 | 0 | ugc03580_standard_projection_systematics_control_not_tau_endpoint |
| MOND_SOURCE_PROJECTION_CONTROL | standard_projection_systematics_control | True | 47 | 30.7036 | 27.6428 | 27.0912 | 6159.85 | 131.061 | 6159.85 | 6159.85 | 0 | 0 | ugc03580_standard_projection_systematics_control_not_tau_endpoint |
| NEWTONIAN_SOURCE_PROJECTION_CONTROL | standard_projection_systematics_control | True | 47 | 35.3948 | 28.9702 | -9.98121 | 18882.6 | 401.758 | 18882.6 | 18882.6 | 0 | 0 | ugc03580_standard_projection_systematics_control_not_tau_endpoint |
| NEWTONIAN_UNCORRECTED | fixed_baseline | True | 47 | 36.012 | 28.8054 | -12.8175 | 20411.7 | 434.291 | 20411.7 | 20411.7 | 0 | 0 | ugc03580_standard_projection_systematics_control_not_tau_endpoint |

This is a diagnostic standard-systematics control, not a Tau endpoint. It cannot be interpreted as evidence for parent morphology or as a dark-matter replacement.
