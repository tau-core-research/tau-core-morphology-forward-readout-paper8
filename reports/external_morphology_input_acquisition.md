# External Morphology Input Acquisition

This report records the first actual external-source acquisition for the
Paper 8 accepted-observable path. It downloads SPARC Table 1 from the
official SPARC site and S4G Pipeline 4 tables from VizieR/CDS through
astroquery.

## Verdict

SPARC master rows acquired: 175.
S4G crossmatches acquired: 78.
S4G/SPARC-derived disk scale candidates acquired: 76.

These are candidate source observables, not a completed accepted manifest.
In particular, S4G disk scales can support `scale_radius_kpc` where matched,
but `formula_family`, confidence/caveat, tail transition radii, thickness,
and full provenance still require the accepted-source audit path.

## Family Acquisition Summary

| proxy_formula_family_for_scope | n_galaxies | n_s4g_matched | n_scale_acquired |
| --- | --- | --- | --- |
| K_compact_finite | 29 | 8 | 7 |
| K_exponential_disk | 32 | 15 | 14 |
| K_scale_tail_spiral | 80 | 30 | 30 |
| K_thick_flared | 34 | 25 | 25 |

## Claim Boundary

This acquisition does not compute endpoint scores and does not validate Tau
Core. It reduces the missing-input blocker by acquiring a source-native
S4G/SPARC disk-scale candidate subset.
