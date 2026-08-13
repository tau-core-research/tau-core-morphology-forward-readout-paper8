# NGC4254 FFL Primitive-Curvature Identifiability Audit v09

**Status:** `SOURCE_STATE_DOES_NOT_IDENTIFY_PRIMITIVE_FFL_CURVATURES_PROVED_NO_ENDPOINT`

**Claim boundary:** constructive source-state/Hessian identifiability no-go and measurement-covariance separation; not a physical curvature or gain derivation, channel detection, component recovery, or endpoint score.

## Constructive No-Go

Center a local FFL action on the same observed stationary source state
`(x0,c0,y0)`:

```text
A = (mu_R/2)||c-c0||^2
  + (kappa_X/2)||(c-c0)-(x-x0)||^2
  + (kappa_Y/2)||(c-c0)-iota(y-y0)||^2.
```

For every positive `kappa_X,kappa_Y`, the action and its first variation vanish
at the same state. Its second variation changes. Therefore the v07 morphology
coordinates and `q_shape_proxy` cannot determine the primitive curvatures.

The following dimensionless countermodels share
`q_shape_proxy=+0.09129505` and the same stationary state. Their
normalization is only an algebraic witness.

| kappa_X | kappa_Y | effective k | conditional gain | conditional terminal q |
|---:|---:|---:|---:|---:|
| 1.0 | 1.0 | 0.500000 | 0.333333 | 0.030432 |
| 1.0 | 9.0 | 0.900000 | 0.473684 | 0.043245 |
| 4.0 | 4.0 | 2.000000 | 0.666667 | 0.060863 |
| 2.0 | 8.0 | 1.600000 | 0.615385 | 0.056182 |

## Covariance Boundary

The v05 Monte Carlo and v07 source-systematic family measure uncertainty and
robustness of the estimator. They are not physical perturbations of the parent
action. A measurement-likelihood curvature such as `J^T Sigma^-1 J` becomes a
physical action Hessian only after an independently derived fluctuation law,
conjugate scale, and source-coordinate normalization. None is currently
available.

## Verdict

The stable `m=2` morphology direction is retained, but its physical stiffness
and terminal gain are not identified. The next finite target is one physically
normalized parent/source perturbation direction and its second variation. It
must come from the parent action, a controlled source response, or a separately
proved fluctuation bridge, not from a rotation residual or measurement noise.
