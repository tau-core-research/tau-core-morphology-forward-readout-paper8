# Theory-completed scale-tail kernel v02

Status: `THEORY_MOTIVATED_KERNEL_CANDIDATE_HISTORICAL_HOLDOUT_AND_OPENED_EXTERNAL_DIAGNOSTIC`

The candidate replaces the dimensionful additive tail with a source-normalized, bounded, multiplicative composite response:

```text
u=K_tail(R)/K_tail(R_cut)
phi=u/(1+u)
v_v02^2=v_TPG^2 exp(eta phi)
```

Historical train selects `phi_tail_bounded` and gives `eta=0.073191446`. On historical scale-tail holdout it beats TPG/v6 in `0.400` and MOND in `0.650` of galaxies. On the already opened LITTLE THINGS primary lane the corresponding diagnostic fractions are `0.500` and `0.500`.

The external v02 result is not prospective because the sample was inspected before this kernel was defined. The formula does not identify physical time or quantum operators.
