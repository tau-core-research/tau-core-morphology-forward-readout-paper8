# NGC4254 Direct Beam-Resolved m=2 Operator Audit v07

**Status:** `SOURCE_ONLY_DIRECT_BEAM_M2_OPERATOR_AUDIT_COMPLETE_NO_ENDPOINT`

**Candidate verdict:** `DIRECT_BEAM_M2_SOURCE_CANDIDATE_SURVIVES_INTERNAL_SPECIFICITY_GATE`

**Claim boundary:** finite source-only 4D-inverse audit of a direct beam-weighted m=2 role operator with an identically processed m=1 alternative-family control; not a parent-derived role, physical q_det, complete covariance, channel/time/quantum signal, dark-matter replacement, or endpoint score.

## Frozen Construction

The v06 `m=2`, `beam_mode=1` source candidate is tested without retaining any
annulus-by-role cell. The corresponding six-component radial beam eigenvector
is linearly interpolated onto source pixels. Observer-path, log-stellar, and
log-gas fields are each stripped of an all-role radial median baseline; their
remaining pixels are then projected directly within the four morphology-phase
roles and centered before the inherited `E_S` determinant proxy is evaluated.

The `m=1` phase family receives exactly the same operator and gates. It is an
alternative-family specificity control, not an asserted physically wrong
family. The `m=2` selection survives only if `m=2` passes and `m=1` does not.

## Finite Audit

| family | role | baseline q | 72-source range | max source phase shift (deg) | measurement 95% q | P(baseline sign) | measurement phase p95 (deg) | min role pixels | own gates |
|---:|---|---:|---:|---:|---:|---:|---:|---:|:---:|
| m=1 | alternative_m1_control | -0.043417 | -0.097965, +0.015498 | 13.11 | -0.126415, +0.074318 | 0.773 | 23.87 | 101 | FAIL |
| m=2 | target_m2 | +0.091295 | +0.046635, +0.101689 | 5.44 | +0.061153, +0.122944 | 0.996 | 3.66 | 101 | PASS |

Passing the own-family gate requires stable source and measurement sign,
source and measurement phase shifts below `22.5` degrees,
all three relative role directions in the beam screen, and at least one full
Gaussian beam area per angular role. Here one beam is
`56.299` pixels, so the frozen minimum is
`57` pixels.

## Validation

- The radial mode crosses zero at
  `[35.0854]`
  arcsec, implementing an inner-versus-outer contrast rather than six discrete
  annulus-role coordinates.
- Baseline full-role counts are `m=1:
  (103, 107, 103, 105)`
  and `m=2:
  (106, 104, 104, 104)`.
- A global stellar rescaling changes q by at most
  `1.110e-16`.
- Simultaneously rotating theta and its morphology anchor preserves every role
  label exactly: `True`.
- A +/-`0.5` degree role-edge perturbation changes q by
  at most `0.00750374`.
- The independent flux-phase estimator differs from the primary phase by
  `m=1: 20.927` degrees
  and `m=2: 0.365`
  degrees.

## Verdict

`m=2` own gates: `True`. `m=1` alternative-control own gates: `False`.
The source-only family-specificity gate is therefore
`True`.

This finite audit removes the sparse-cell blocker from the tested operator,
but it does not turn `q_shape_proxy` into physical `q_det`. No parent role,
complete channel, time or quantum terminal, dark-sector replacement, or
endpoint score is identified.
