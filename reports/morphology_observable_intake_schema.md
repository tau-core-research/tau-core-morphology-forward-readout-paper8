# Morphology Observable Intake Schema

This schema defines the residual-blind morphology observables needed for
the next Paper 8 endpoint run. It is a data-intake contract, not a fit
and not an empirical validation claim.

## Required Observable Fields

| field | required | scope | accepted_source | forbidden_source | acceptance_rule | failure_mode |
| --- | --- | --- | --- | --- | --- | --- |
| galaxy | True | all | catalog identifier before endpoint scoring | none | must uniquely match component/rotation-curve table | row cannot enter endpoint |
| formula_family | True | all | residual-blind morphology classification | vobs residual pattern; required_S_tau; best-fit formula choice | one of predeclared Tau Core morphology families | leakage risk; row becomes diagnostic-only |
| manifest_confidence | True | all | pre-scoring morphology-observable quality assessment | endpoint residual performance | numeric in [0,1]; threshold gate predeclared | quality gate cannot be audited |
| manifest_caveat | True | all | observability caveats from geometry/catalog quality | bad endpoint score after model application | must include none or explicit caveat tokens | cannot preserve limited-observability evidence |
| inclination_deg | True | primary quality gate | external geometry/catalog measurement | endpoint residual fit | used to apply no_low_inclination gate before scoring | primary endpoint lane cannot be reproduced |
| distance_frac_error | True | secondary quality gate | external distance estimate uncertainty | baseline-comparison outcome | used to apply no_large_distance_error support gate | secondary baseline lane cannot be reproduced |
| scale_radius_kpc | True | K_scale_tail_spiral; K_exponential_disk; K_thick_flared | morphology/light-profile decomposition before endpoint scoring | rotation residual shape or endpoint-selected scale | positive physical length with provenance | kernel scale remains proxy-level |
| tail_inner_radius_kpc | True | K_scale_tail_spiral | morphological transition or disk-structure feature | radius chosen to minimize residuals | positive and <= tail_cutoff_radius_kpc | scale-tail formula cannot be source-native |
| tail_cutoff_radius_kpc | True | K_scale_tail_spiral | outer disk/tail morphology extent | endpoint-selected truncation radius | positive and >= tail_inner_radius_kpc | tail response normalization is not reproducible |
| compact_support_radius_kpc | True | K_compact_finite | residual-blind compact-source morphology support | radius chosen from residual improvement | positive support radius with provenance | compact finite source row remains proxy-level |
| thickness_h_over_rs | True | K_thick_flared | vertical/thickness proxy or direct morphology estimate | endpoint-tuned damping factor | positive dimensionless ratio with uncertainty/caveat | thick/flared kernel cannot be audited |
| ring_radius_kpc | False | K_ring_resonance | external ring/resonance morphology | residual peak location | positive radius if ring family is included | ring row must remain caveated/proxy |
| bar_m2_strength | False | K_barred_m2 | image/velocity-field morphology before endpoint scoring | 1D residual asymmetry fit | only velocity-field/full morphology endpoint can promote this row | 1D SPARC row remains caveated proxy |
| lopsided_m1_strength | False | K_lopsided_m1 | image/velocity-field asymmetry before endpoint scoring | 1D residual asymmetry fit | only velocity-field/full morphology endpoint can promote this row | 1D SPARC row remains caveated proxy |
| observable_provenance | True | all | dataset name, measurement method, and pre-scoring timestamp | undocumented manual adjustment | must document source and residual-blind status | row cannot support a claim-safe endpoint |

## Acceptance Gates

| gate | pass_condition | status |
| --- | --- | --- |
| residual_blindness | No observable may use vobs residual gain, required_S_tau, or posthoc family choice. | required |
| primary_quality_gate_ready | inclination fields and low-inclination caveat must reproduce no_low_inclination lane. | required |
| family_kernel_parameters_ready | Each included formula family has all required scale/support/thickness fields. | required |
| provenance_ready | Every row records external morphology-observable provenance. | required |
| caveated_rows_preserved | Rows failing a quality gate remain in support/control outputs. | required |
| non_axisymmetric_caveat | m=1/m=2 rows are not promoted from 1D curves without velocity-field support. | required |

## Claim Boundary

The current available-data manifest remains a proxy manifest. A future
Paper 8 empirical run should not be treated as claim-ready until this
schema is populated from accepted residual-blind morphology observables
and the predeclared endpoint protocol is run without changing gates after
seeing scores.
