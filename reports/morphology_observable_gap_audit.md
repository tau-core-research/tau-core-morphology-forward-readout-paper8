# Morphology Observable Gap Audit

This audit compares the current available-data proxy manifest against the
residual-blind morphology-observable intake schema. It is not an endpoint
score and not an empirical validation claim.

## Verdict

The current manifest is coverage-rich but acceptance-limited. It has broad
proxy coverage for the active morphology families, but most kernel-driving
fields are not accepted residual-blind observables yet. The next Paper 8
upgrade should therefore replace proxies with external/pre-scoring
morphology measurements rather than changing endpoint gates or tuning
formula families after seeing residuals.

- Missing required fields: 0
- Proxy fields requiring accepted-source upgrade: 9

## Field Status Counts

| availability_status | n_fields |
| --- | --- |
| accepted_available | 3 |
| not_in_current_family_set | 3 |
| proxy_available | 9 |

## Required/Optional Field Gap

| field | required | scope | manifest_source_field | availability_status | n_applicable_rows | n_available_rows | coverage_fraction | required_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| galaxy | True | all | galaxy | accepted_available | 175 | 175 | 1.0 | keep as pre-scoring catalog/geometry input |
| formula_family | True | all | formula_family | proxy_available | 175 | 175 | 1.0 | replace proxy with accepted residual-blind morphology observable |
| manifest_confidence | True | all | manifest_confidence | proxy_available | 175 | 175 | 1.0 | replace proxy with accepted residual-blind morphology observable |
| manifest_caveat | True | all | manifest_caveat | proxy_available | 175 | 175 | 1.0 | replace proxy with accepted residual-blind morphology observable |
| inclination_deg | True | primary quality gate | inclination_deg | accepted_available | 175 | 175 | 1.0 | keep as pre-scoring catalog/geometry input |
| distance_frac_error | True | secondary quality gate | distance_frac_error | accepted_available | 175 | 175 | 1.0 | keep as pre-scoring catalog/geometry input |
| scale_radius_kpc | True | K_scale_tail_spiral; K_exponential_disk; K_thick_flared | scale_radius_proxy_kpc | proxy_available | 146 | 146 | 1.0 | replace proxy with accepted residual-blind morphology observable |
| tail_inner_radius_kpc | True | K_scale_tail_spiral | tail_inner_radius_proxy_kpc | proxy_available | 80 | 80 | 1.0 | replace proxy with accepted residual-blind morphology observable |
| tail_cutoff_radius_kpc | True | K_scale_tail_spiral | tail_cutoff_radius_proxy_kpc | proxy_available | 80 | 80 | 1.0 | replace proxy with accepted residual-blind morphology observable |
| compact_support_radius_kpc | True | K_compact_finite | compact_support_radius_proxy_kpc | proxy_available | 29 | 29 | 1.0 | replace proxy with accepted residual-blind morphology observable |
| thickness_h_over_rs | True | K_thick_flared | thickness_h_over_rs_proxy | proxy_available | 34 | 34 | 1.0 | replace proxy with accepted residual-blind morphology observable |
| ring_radius_kpc | False | K_ring_resonance | ring_radius_proxy_kpc | not_in_current_family_set | 0 | 0 | 0.0 | not applicable to current 1D SPARC first-pass family set |
| bar_m2_strength | False | K_barred_m2 | bar_m2_proxy | not_in_current_family_set | 0 | 0 | 0.0 | not applicable to current 1D SPARC first-pass family set |
| lopsided_m1_strength | False | K_lopsided_m1 | lopsided_m1_proxy | not_in_current_family_set | 0 | 0 | 0.0 | not applicable to current 1D SPARC first-pass family set |
| observable_provenance | True | all | parameter_source | proxy_available | 175 | 175 | 1.0 | replace proxy with accepted residual-blind morphology observable |

## Family-Level Readiness

| formula_family | n_galaxies | required_fields_applicable | accepted_ready_required_fields | proxy_required_fields | missing_required_fields | readiness_status |
| --- | --- | --- | --- | --- | --- | --- |
| K_compact_finite | 29 | 8 | 3 | 5 | 0 | proxy_coverage_ready_acceptance_not_ready |
| K_exponential_disk | 32 | 8 | 3 | 5 | 0 | proxy_coverage_ready_acceptance_not_ready |
| K_scale_tail_spiral | 80 | 10 | 3 | 7 | 0 | proxy_coverage_ready_acceptance_not_ready |
| K_thick_flared | 34 | 9 | 3 | 6 | 0 | proxy_coverage_ready_acceptance_not_ready |

## Claim Boundary

This gap audit is not an endpoint score.

A field marked `proxy_available` may be useful for preparation diagnostics,
but it must not be promoted to discovery evidence. The accepted run needs
residual-blind morphology labels and kernel observables fixed before
endpoint scoring.
