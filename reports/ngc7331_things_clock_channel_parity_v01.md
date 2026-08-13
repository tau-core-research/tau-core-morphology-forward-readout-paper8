# NGC7331 THINGS Clock-Channel Parity Diagnostic v0.1

**Status:** `SIMPLE_COMMON_MULTIPLICATIVE_CLOCK_CHANNEL_INCOMPATIBLE_SINGLE_GALAXY`

## Odd/Even Velocity-Field Result

| product | rings | outer rings | outer median abs odd (km/s) | outer median abs even (km/s) | outer even/odd |
| --- | ---: | ---: | ---: | ---: | ---: |
| natural | 24 | 11 | 211.916750 | 3.821469 | 0.018141 |
| robust | 25 | 12 | 211.026000 | 4.879578 | 0.023486 |

## Simple Multiplicative Clock Test

The outer SPARC diagnostic requires `N_ch=0.573922`, equivalent
to multiplying the inferred odd velocity by `1.742398`. If
that factor multiplies the full spectral redshift `1+z`, it also predicts a
common even shift of approximately `222565.363 km/s`.
The larger observed outer median even shift across the two THINGS products is
only `4.879578 km/s`, a ratio of
`4.561e+04`.

Thus a common multiplicative spectral-clock factor large enough to explain the
outer velocity discrepancy is kinematically incompatible with this frozen
single-galaxy velocity field.

## Differential Observer-To-Point Path Channel

The older Tau Core hypothesis assigns a distinct observer-to-emission-point
path object to each disk side. Parameterize its first parity component by

```text
A_plus  = A_bar (1 + delta)
A_minus = A_bar (1 - delta).
```

Then

```text
beta_inferred = (beta_dynamic + delta) / (1 + delta beta_dynamic).
```

Using the mean of the two outer odd summaries
`211.471375 km/s` and the cross-packet SPARC ratio gives
`delta_req=3.005526e-04`, corresponding to a
fractional side-to-side channel difference of
`6.011052e-04`.

This is only a kinematic scale estimate. No path kernel has been fitted or
tested. It demonstrates that the common-factor rejection does not reject the
differential observer-position/light-cone channel class.

## Boundary

This rejects only the common full-`1+z` multiplier. A differential
observer-to-point light-cone channel, nonlinear map anchored at the systemic
redshift, tracer-dependent quantum-access map, or a channel that changes
dynamics rather than spectral readout requires a different frozen formula and
different controls.
