# NGC5907 Projection-Dominated Endpoint Diagnostic

This diagnostic runs an explicit projection-dominated solved-response
formula from the NGC5907 projection freeze gate. It does not promote an
accepted endpoint label and does not validate Tau Core.

## Formula

The diagnostic uses the source-frozen attenuation form

`v_proj(R)^2 = v_TPG(R)^2 * (1 - gamma_proj K_proj(R))`,

where `gamma_proj = 0.5 * Pi_projection * h/R`, and `K_proj(R)` is a
smooth source-windowed warp/truncation kernel frozen by the NGC5907
projection gate.

## Scores

| galaxy | n_points | rmse_newton | rmse_tpg_v6 | rmse_mond | rmse_generic_promoted_thick_flared | rmse_projection_dominated | projection_minus_tpg_v6 | projection_minus_mond | projection_minus_generic_promoted | pi_projection_bound | h_over_r | gamma_projection | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC5907 | 19 | 86.4837 | 16.7855 | 18.5954 | 17.0253 | 15.4952 | -1.29031 | -3.10017 | -1.5301 | 0.789128 | 0.173321 | 0.0683861 | False | ngc5907_projection_endpoint_diagnostic_not_validation |

## Claim Boundary

This is a one-galaxy diagnostic endpoint. It is allowed only as a
formula-inspection run; the accepted-manifest audit still keeps endpoint
eligibility disabled.

## Figure

paper8_submission_source/figures/fig05_ngc5907_projection_endpoint_diagnostic.png
