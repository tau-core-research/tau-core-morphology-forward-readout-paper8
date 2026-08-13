# NGC4254 Morphology-Phase Four-Role Audit v06

**Status:** `SOURCE_ONLY_MORPHOLOGY_PHASE_ROLE_AUDIT_COMPLETE_NO_ENDPOINT`

**Candidate verdict:** `AT_LEAST_ONE_INTERNAL_SOURCE_ROLE_CANDIDATE_SURVIVES`

**Claim boundary:** finite source-only audit of m=1/m=2 phase-anchored inverse role charts; not a parent role identification, physical q_det, complete covariance, channel/time/quantum signal, dark-matter replacement, or endpoint score.

## Frozen Construction

The four ordered roles are no longer anchored to an externally imposed disk
position angle.  For each finite candidate, the stellar map supplies an `m=1`
or `m=2` phase from annulus-normalized log-intensity contrast, and the roles are
the four consecutive 90-degree sectors measured from that phase.  The same
source-derived anchor is used for the observer-path, stellar-body, and gas-shape
vectors.

The six inherited annular relative vectors are projected onto the first two
eigenvectors of the already frozen H I beam-overlap screen.  Their eigenvalues
are `4.291134` and `1.458537` and together carry
`95.8279%` of the matrix trace.
This does not turn the overlap screen into a complete covariance.

## Finite Audit

| anchor | beam mode | baseline q | 72-source range | max source phase shift (deg) | measurement 95% q | P(baseline sign) | measurement phase p95 (deg) | joint internal gate |
|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| m=1 | 0 | -0.005313 | -0.010159, +0.071083 | 13.11 | -0.146165, +0.107631 | 0.555 | 26.02 | FAIL |
| m=1 | 1 | -0.067542 | -0.136915, +0.022027 | 13.11 | -0.222631, +0.109629 | 0.684 | 26.02 | FAIL |
| m=2 | 0 | +0.102089 | -0.117380, +0.166338 | 5.44 | +0.081284, +0.128387 | 0.996 | 3.94 | FAIL |
| m=2 | 1 | +0.139122 | +0.072787, +0.217141 | 5.44 | +0.027169, +0.264436 | 0.977 | 3.94 | PASS |

The phase limit is frozen at `22.5` degrees, half one
role-sector width. Passing requires sign and phase stability under both the 72
source-systematic scenarios and the separate 256-draw stellar-plus-independent-
CO measurement model.

## Validation

- A global stellar rescaling changes q by at most
  `1.527e-15`.
- Simultaneously rotating theta and the morphology anchor leaves every role
  label unchanged: `True`.
- A +/-`0.5` degree role-edge perturbation changes q by
  at most `0.034694`.
- The independent mask-corrected flux phase differs from the primary contrast
  phase by `m=1: 20.93`
  degrees and `m=2: 0.37`
  degrees. This is an estimator-consistency diagnostic, not a promotion gate.
- The `m=2` full-support role counts are
  `[106, 104, 104, 104]`. Its three relative role
  eigenvalues are
  `[1.01367, 0.876471, 0.521771]`
  with participation rank
  `2.8131/3`. Thus the
  beam screen does not collapse the candidate to one relative direction, but
  it is not a complete role covariance and does not authorize a diagonal
  four-role likelihood.
- Some inherited annulus-role cells contain only three map pixels. The radial
  eigenmode projection uses them as correlated source coordinates; it does not
  turn them into independent measurements. This remains a promotion blocker.

For the passing `m=2`, beam-mode-1 candidate, geometry-only, stellar-PSF-only,
and H2-conversion-only controls each preserve the baseline sign. The
measurement decomposition remains stellar-mode dominated; CO-only and the
robust-1 H I control do not select the candidate.

## Verdict

Passing internal harmonic/mode candidates:
`[{'harmonic': 2, 'beam_mode': 1}]`.

Even a passing candidate would remain a source-side inverse chart only. No
physical parent role, FFL eta, determinant transport, channel origin, time or
quantum terminal, dark-sector replacement, or endpoint score is identified.
