# External Morphology Source Registry

This registry records where the missing accepted morphology inputs should
come from. It is a source-acquisition plan and crossmatch template, not a
claim that the accepted inputs have already been collected.

## Verdict

Use SPARC as the sample and baryonic/rotation baseline, S4G as the first
primary morphology/decomposition source, NED/NED-D as the identity and
distance/provenance layer, DustPedia as multiband fallback/validation, and
PHANGS only for optional high-quality non-axisymmetric branches. The next
practical step is to fill the 175-row crossmatch template before endpoint
launch is considered.

## Source Registry

| source_id | priority | url | use_for_fields | not_accepted_for_fields | residual_blind_role | coverage_expectation |
| --- | --- | --- | --- | --- | --- | --- |
| SPARC | sample_and_baseline | https://astronomy.case.edu/2016/08/26/sparc-galaxy-database/ | galaxy; inclination_deg; distance_frac_error; baryonic baseline; rotation curve | formula_family; kernel morphology parameters | endpoint sample and baryonic/rotation baseline, not final morphology source | full 175-galaxy sample |
| S4G | primary_morphology_decomposition | https://irsa.ipac.caltech.edu/data/SPITZER/S4G/overview.html | formula_family; scale_radius_kpc; compact_support_radius_kpc; ring_radius_kpc; bar_m2_strength; observable_provenance | rotation residual endpoints | primary 3.6 micron morphology/decomposition source where crossmatch exists | partial SPARC overlap; must be measured |
| NED_NEDD | identity_distance_provenance | https://ned.ipac.caltech.edu/ | galaxy identity; aliases; distance provenance; observable_provenance | endpoint-selected morphology family | crossmatch/provenance and distance consistency layer | broad coverage; quality varies by object |
| DustPedia | fallback_multiband_morphology | https://arxiv.org/abs/1708.05335 | scale_radius_kpc; compact_support_radius_kpc; tail_cutoff_radius_kpc; observable_provenance | velocity-field-only asymmetry claims | fallback and independent multiband morphology/source validation | partial SPARC overlap; must be measured |
| PHANGS | optional_velocity_field_morphology | https://www.phangs.org/home/data | bar_m2_strength; lopsided_m1_strength; ring_radius_kpc; non-axisymmetric caveat support | full 1D SPARC primary endpoint coverage | optional high-quality branch for bars, rings, asymmetry, and velocity-field support | small high-quality overlap; not primary full-sample source |

## Field-To-Source Map

| field | primary_source | secondary_source | fallback_policy | acceptance_check |
| --- | --- | --- | --- | --- |
| formula_family | S4G | DustPedia; NED_NEDD morphology references | leave row diagnostic-only if residual-blind family assignment is ambiguous | family assigned before endpoint scoring with source provenance |
| manifest_confidence | source-quality rubric over S4G/NED/DustPedia evidence | manual pre-scoring morphology audit log | low confidence rows remain in caveated/support outputs | confidence threshold frozen before endpoint scoring |
| manifest_caveat | geometry/catalog/source-quality caveat log | NED_NEDD distance and inclination provenance | caveat rather than drop unless predeclared exclusion applies | no caveat is based on bad endpoint residual performance |
| scale_radius_kpc | S4G | DustPedia | block active-family endpoint row if no accepted scale exists | positive physical scale, residual-blind method, provenance recorded |
| tail_inner_radius_kpc | S4G profile/decomposition or morphology feature log | DustPedia outer-disk morphology | scale-tail row remains diagnostic-only if transition is not source-defined | positive and <= tail_cutoff_radius_kpc; not chosen from residuals |
| tail_cutoff_radius_kpc | S4G outer-disk extent or DustPedia support radius | NED/DustPedia size provenance | scale-tail row remains diagnostic-only if support is not source-defined | positive and >= tail_inner_radius_kpc; not endpoint-selected |
| compact_support_radius_kpc | S4G decomposition | DustPedia compact-source morphology | compact row remains proxy-level if no compact support source exists | positive support radius with residual-blind provenance |
| thickness_h_over_rs | external vertical/thickness estimate or documented morphology proxy | source-quality caveat if no direct thickness observable exists | thick/flared row is caveated unless thickness proxy is predeclared | positive dimensionless ratio; not endpoint-tuned damping |
| ring_radius_kpc | S4G or PHANGS ring/resonance morphology | DustPedia/NED morphology notes | optional branch only; no primary 1D endpoint promotion | not selected from residual peak location |
| bar_m2_strength | PHANGS or S4G bar morphology | image morphology caveat only | velocity-field/full-morphology branch only | not inferred from 1D residual asymmetry |
| lopsided_m1_strength | PHANGS or external asymmetry morphology | image morphology caveat only | velocity-field/full-morphology branch only | not inferred from 1D residual asymmetry |
| observable_provenance | NED_NEDD plus source-specific dataset/method records | manual pre-scoring provenance ledger | row cannot enter claim-ready endpoint without provenance | dataset, method, and pre-scoring timestamp present |

## Crossmatch Template Summary

Rows: 175

All external source match fields are intentionally `TO_BE_CHECKED`. This
prevents the current proxy manifest from masquerading as accepted-source
coverage.

## Claim Boundary

A successful crossmatch would provide candidate accepted inputs for the
readiness gate. It would not by itself compute endpoint scores or validate
Tau Core against MOND, RAR, TGP, or Newtonian baselines.
