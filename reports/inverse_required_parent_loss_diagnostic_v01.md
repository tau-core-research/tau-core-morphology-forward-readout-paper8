# Inverse required parent-loss diagnostic v01

Status: `DIAGNOSTIC_ONLY_NOT_ENDPOINT`.

## Exact inverse

For the declared effective shell

$$v_{\rm obs}^2=v_{\rm base}^2/(1-\ell_{\rm req}),$$

the measurements determine

$$g_{\rm req}=v_{\rm obs}/v_{\rm base},\qquad
\kappa_{\rm req}=\log g_{\rm req},\qquad
\ell_{\rm req}=1-(v_{\rm base}/v_{\rm obs})^2.$$

Positive `loss_required` means that this inverse-attenuation convention
needs an apparent boost relative to the selected baseline. Negative values
cannot be represented by a positive loss in this one-parameter shell.

## Results

| baseline_id | n_points | n_galaxies | median_gain | median_kappa | median_loss | point_fraction_positive_loss | point_fraction_positive_loss_95 | point_fraction_negative_loss_95 | galaxy_fraction_median_positive | galaxy_fraction_majority_positive_95 | holdout_zero_kappa_rmse | holdout_constant_rmse_ratio | holdout_fixed_cubic_rmse_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| newtonian_baryonic | 3389 | 175 | 1.6576 | 0.505368 | 0.636049 | 0.936855 | 0.867513 | 0.0212452 | 0.982857 | 0.908571 | 0.642451 | 0.572827 | 0.563298 |
| tpg_v6 | 3389 | 175 | 1.0106 | 0.0105456 | 0.0208703 | 0.527589 | 0.341399 | 0.208616 | 0.485714 | 0.302857 | 0.304345 | 0.995333 | 0.994348 |
| mond_fixed | 3389 | 175 | 0.975498 | -0.0248074 | -0.0508661 | 0.423724 | 0.268811 | 0.279729 | 0.36 | 0.194286 | 0.319388 | 0.965956 | 0.965543 |

Against baryons alone the median required gain is 1.658
and 86.8% of points
require positive loss at the propagated 95% level. This is the familiar
mass-discrepancy pattern expressed in the chosen inverse coordinates.
Against frozen TPG/v6 the median gain is 1.011 and the
fixed radial law has holdout RMSE ratio 0.994;
against fixed MOND they are 0.975 and
0.966. Thus the remaining inverse
field after either non-Newtonian baseline is sign-mixed and is not captured
well by one universal cubic radial profile.

The fixed cubic is trained only on the 131-galaxy development split and
evaluated on the 44-galaxy holdout. A ratio below one indicates that one
universal radial shape improves on zero required log-gain.

## What is and is not reconstructed

At each measured radius the endpoint fixes one scalar combination. It does
not split that number into parent morphology, spatial calibration, temporal
calibration and terminal calibration. If

$$\kappa_{\rm req}=\kappa_D-\kappa_T+\kappa_M+\kappa_{\rm cal},$$

then arbitrary component shifts whose signed sum is zero leave every
measurement unchanged. This is the inverse gauge/null family. Additional
independent observables or a source-side law are needed to choose one member.

The strongest conventional counterinterpretation is that the reconstructed
field absorbs baseline incompleteness, baryonic modelling and measurement or
deprojection systematics. Therefore the output is an empirical target for a
future Tau derivation, not evidence that the target is parent morphological
loss and not a dark-matter replacement result.
