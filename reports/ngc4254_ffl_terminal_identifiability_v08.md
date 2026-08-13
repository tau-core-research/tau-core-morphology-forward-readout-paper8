# NGC4254 FFL Terminal Identifiability Audit v08

**Status:** `SOURCE_ONLY_TERMINAL_IDENTIFIABILITY_NO_GO_PROVED_NO_ENDPOINT`

**Claim boundary:** algebraic source-to-terminal identifiability result using the frozen v07 q_shape proxy; not a physical gain derivation, channel-component recovery, time/quantum/gravity attribution, dark-matter replacement, or endpoint score.

## Source Input

The v07 direct `m=2` source operator survives its internal specificity gate
with baseline `q_shape_proxy=+0.09129505` and 72-scenario source range
`[+0.04663451,+0.10168901]`. This audit accepts that source-coordinate result
without promoting it to physical `q_det`.

## Single-Terminal No-Go

Suppose the conditional complete spectral law is reduced to one scalar
terminal with an unknown source-to-terminal gain `g`:

```text
beta_read = (beta_dyn + tanh(g q_shape))
            / (1 + beta_dyn tanh(g q_shape)).
```

For every admissible `beta_dyn` and `beta_obs`, nonzero `q_shape` and an
unconstrained real gain give

```text
g_req = atanh[(beta_obs-beta_dyn)/(1-beta_obs beta_dyn)] / q_shape.
```

Substitution recovers `beta_obs` exactly. The fixed-seed numerical identity
check over `10000` pairs has maximum error
`1.665e-16`. Therefore a freely fitted gain makes one scalar
endpoint saturated and nonfalsifiable. The gain must come from the primitive
curvatures and normalization, or be frozen independently, before scoring.

## Multi-Readout Rank Condition

For `K` claimed channel components, write the required terminal coordinates as

```text
q_req = A c.
```

Within this fixed linear component model, the component vector `c` is
identifiable only if the terminal sensitivity matrix `A` is independently
frozen and has full column rank `K`. Merely naming several readouts does not
supply independent scalar rows. If both `A` and `c` are
unknown, `A -> A S` and `c -> S^-1 c` leave every prediction unchanged for any
invertible `S`.

Side-resolved spectra can conditionally separate a common sector from a
differential sector, but those two observables do not by themselves identify
time, quantum, gravity, or other physical components.

## Verdict

The robust v07 morphology coordinate is real at the declared source-audit
level. What remains missing is not just more endpoint data: it is the physical
gain and a source-frozen, full-rank terminal sensitivity matrix. Until those
exist, neither channel presence nor channel-component decomposition is
identified, and endpoint scoring remains closed.
