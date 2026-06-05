# Tau-Side Source-Normalized L2 Endpoint Preflight

This run implements a residual-blind, theory-conditional Tau-side
source-normalization rule. It uses no observed velocity endpoint, no
rotation residual, no required-S_tau diagnostic, and no best-family
selection. It is not yet an accepted physical normalization law.
This is not an accepted physical normalization law.

## Normalization Rule

```text
normalized_shape_gK(r) = kernel_gK(r) / median_r |kernel_gK(r)|
c_g = median_r max(v_v6^2 - v_n^2, 0) / median_r v_v6^2
delta v_gK^2(r) = sigma_K e_gK w_gK c_g median_r(v_n^2) normalized_shape_gK(r)
```

The signs are predeclared: compact/tail positive, exponential/thick
negative. These signs and evidence gates are loaded from the
Tau-side source-normalization derivation manifest, not selected from
endpoint residuals. The manifest marks the orientation signs as
theory-conditional bridge derivations and the proxy attenuation as the
coarse executable representative of the conservative Tau-side
readout-admission product, not an empirical fit.

## Holdout Verdict

- Holdout galaxies: 44
- Beats old L2 intake endpoint: 0.568
- Beats TPG/v6: 0.455
- Beats MOND: 0.545
- Median source-normalized-minus-old-L2 RMSE: -0.271648

## Summary

| split | n_galaxies | median_rmse_tau_source_normalized_l2 | beats_old_l2_intake_fraction | beats_tpg_v6_fraction | beats_mond_fraction | median_source_norm_minus_old_l2_intake | median_source_norm_minus_tpg_v6 | median_source_norm_minus_mond | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | 44 | 14.1508 | 0.568182 | 0.454545 | 0.545455 | -0.271648 | 0.0698845 | -0.316241 | tau_side_source_normalization_formula_conditional_not_validation |
| train | 131 | 11.786 | 0.541985 | 0.450382 | 0.48855 | -0.0899372 | 0.292308 | 0.148575 | tau_side_source_normalization_formula_conditional_not_validation |

## Rule Scale Summary

| split | n_galaxies | median_closure_fraction | median_source_vn2 | median_net_signed_strength |
| --- | --- | --- | --- | --- |
| holdout | 44 | 0.71306 | 1645.47 | 328.909 |
| train | 131 | 0.726255 | 1667.43 | 444.845 |

## Claim Boundary

This is a theory-conditional source-normalization candidate. A positive
or negative endpoint result here is not validation. The weakest step is
source-native promotion of the orientation signs plus accepted
per-galaxy evidence assignments before endpoint freeze.
