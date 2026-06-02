# Accepted Observable Manifest Template Validation

This report validates the empty accepted-observable manifest template. The
template is intentionally blocked: it carries galaxy identifiers and
pre-scoring geometry fields, but it does not promote proxy morphology
fields into accepted discovery inputs.

## Verdict

The accepted manifest template is collection-ready but endpoint-blocked.
It contains 175 galaxy rows. Required morphology/source fields
remain blocked in 9 schema fields until accepted residual-blind
sources are entered. This is a guardrail, not a negative empirical result.

## Status Counts

| template_validation_status | n_fields |
| --- | --- |
| blocked_missing_required_accepted_source | 9 |
| not_applicable_current_template | 3 |
| template_prefilled | 3 |

## Field Validation

| field | required | scope | n_applicable_rows | n_present_rows | n_missing_rows | template_validation_status | accepted_source_rule | forbidden_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| galaxy | True | all | 175 | 175 | 0 | template_prefilled | catalog identifier before endpoint scoring | none |
| formula_family | True | all | 175 | 0 | 175 | blocked_missing_required_accepted_source | residual-blind morphology classification | vobs residual pattern; required_S_tau; best-fit formula choice |
| manifest_confidence | True | all | 175 | 0 | 175 | blocked_missing_required_accepted_source | pre-scoring morphology-observable quality assessment | endpoint residual performance |
| manifest_caveat | True | all | 175 | 0 | 175 | blocked_missing_required_accepted_source | observability caveats from geometry/catalog quality | bad endpoint score after model application |
| inclination_deg | True | primary quality gate | 175 | 175 | 0 | template_prefilled | external geometry/catalog measurement | endpoint residual fit |
| distance_frac_error | True | secondary quality gate | 175 | 175 | 0 | template_prefilled | external distance estimate uncertainty | baseline-comparison outcome |
| scale_radius_kpc | True | K_scale_tail_spiral; K_exponential_disk; K_thick_flared | 146 | 0 | 146 | blocked_missing_required_accepted_source | morphology/light-profile decomposition before endpoint scoring | rotation residual shape or endpoint-selected scale |
| tail_inner_radius_kpc | True | K_scale_tail_spiral | 80 | 0 | 80 | blocked_missing_required_accepted_source | morphological transition or disk-structure feature | radius chosen to minimize residuals |
| tail_cutoff_radius_kpc | True | K_scale_tail_spiral | 80 | 0 | 80 | blocked_missing_required_accepted_source | outer disk/tail morphology extent | endpoint-selected truncation radius |
| compact_support_radius_kpc | True | K_compact_finite | 29 | 0 | 29 | blocked_missing_required_accepted_source | residual-blind compact-source morphology support | radius chosen from residual improvement |
| thickness_h_over_rs | True | K_thick_flared | 34 | 0 | 34 | blocked_missing_required_accepted_source | vertical/thickness proxy or direct morphology estimate | endpoint-tuned damping factor |
| ring_radius_kpc | False | K_ring_resonance | 0 | 0 | 0 | not_applicable_current_template | external ring/resonance morphology | residual peak location |
| bar_m2_strength | False | K_barred_m2 | 0 | 0 | 0 | not_applicable_current_template | image/velocity-field morphology before endpoint scoring | 1D residual asymmetry fit |
| lopsided_m1_strength | False | K_lopsided_m1 | 0 | 0 | 0 | not_applicable_current_template | image/velocity-field asymmetry before endpoint scoring | 1D residual asymmetry fit |
| observable_provenance | True | all | 175 | 0 | 175 | blocked_missing_required_accepted_source | dataset name, measurement method, and pre-scoring timestamp | undocumented manual adjustment |

## Claim Boundary

A future endpoint run should consume a populated accepted manifest, not this
empty template and not the proxy manifest. Passing this validator is a data
readiness condition only; it would not by itself prove Tau Core or guarantee
a better fit than MOND, RAR, TGP, or Newtonian baselines.
