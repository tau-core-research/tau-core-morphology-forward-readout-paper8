# Morphology Observable Source Upgrade Plan

This plan converts the gap audit into a residual-blind source collection
protocol. It is not a data source claim, not an endpoint score, and not
an empirical validation result.

## Verdict

The next Paper 8 upgrade is source replacement, not endpoint redesign.
The active proxy manifest needs accepted morphology sources for the
P0 bookkeeping/label fields (4 fields) and P1 active-family kernel
observables (5 fields). Optional ring, bar, and lopsided branches
should stay caveated unless external morphology or velocity-field support
is added before scoring.

## Field Upgrade Plan

| field | current_availability_status | current_manifest_source_field | upgrade_priority | accepted_source_class | extraction_rule | leak_guard | promotion_gate | endpoint_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| formula_family | proxy_available | formula_family | P0 | residual-blind image/decomposition morphology classification | assign one predeclared Tau Core family before endpoint scoring | no vobs residuals, required_S_tau, or best-fit formula choice | family label documented with source and pre-scoring timestamp | must be upgraded before discovery-style endpoint claim |
| manifest_confidence | proxy_available | manifest_confidence | P0 | pre-scoring morphology-observable quality rubric | score confidence from source quality and feature clarity only | no endpoint performance or baseline comparison input | thresholds frozen before the endpoint run | must be upgraded before discovery-style endpoint claim |
| manifest_caveat | proxy_available | manifest_caveat | P0 | geometry/catalog/source-quality caveat log | record low inclination, distance uncertainty, weak feature, or none | no caveat added because the model scored poorly | caveated rows preserved in support/control outputs | must be upgraded before discovery-style endpoint claim |
| scale_radius_kpc | proxy_available | scale_radius_proxy_kpc | P1 | light-profile or morphology decomposition scale length | use pre-scoring disk scale/support length with units and uncertainty | no radius chosen from residual shape or endpoint score | positive physical scale with provenance | must be upgraded before discovery-style endpoint claim |
| tail_inner_radius_kpc | proxy_available | tail_inner_radius_proxy_kpc | P1 | outer-disk morphology transition feature | measure transition radius before applying the readout formula | no radius chosen to minimize velocity residuals | positive and not larger than tail_cutoff_radius_kpc | must be upgraded before discovery-style endpoint claim |
| tail_cutoff_radius_kpc | proxy_available | tail_cutoff_radius_proxy_kpc | P1 | outer disk/tail extent morphology observable | measure tail support/cutoff before endpoint scoring | no endpoint-selected truncation radius | positive and not smaller than tail_inner_radius_kpc | must be upgraded before discovery-style endpoint claim |
| compact_support_radius_kpc | proxy_available | compact_support_radius_proxy_kpc | P1 | compact-source morphology support radius | measure compact support from residual-blind source morphology | no support radius chosen from residual improvement | positive support radius with provenance | must be upgraded before discovery-style endpoint claim |
| thickness_h_over_rs | proxy_available | thickness_h_over_rs_proxy | P1 | vertical thickness/flaring observable or documented proxy | record dimensionless thickness ratio and uncertainty/caveat | no damping factor tuned to endpoint residuals | positive ratio with source and caveat status | must be upgraded before discovery-style endpoint claim |
| ring_radius_kpc | not_in_current_family_set | ring_radius_proxy_kpc | P2 | external ring/resonance morphology measurement | include only if ring family enters a predeclared endpoint lane | no residual-peak-selected ring radius | ring branch remains caveated until source-native fields exist | optional branch; keep out of current primary 1D endpoint |
| bar_m2_strength | not_in_current_family_set | bar_m2_proxy | P2_velocity_field | image or velocity-field m=2 morphology observable | promote only in a velocity-field/full-morphology branch | no 1D residual asymmetry fit | not promoted from 1D SPARC curves alone | optional branch; keep out of current primary 1D endpoint |
| lopsided_m1_strength | not_in_current_family_set | lopsided_m1_proxy | P2_velocity_field | image or velocity-field m=1 asymmetry observable | promote only in a velocity-field/full-morphology branch | no 1D residual asymmetry fit | not promoted from 1D SPARC curves alone | optional branch; keep out of current primary 1D endpoint |
| observable_provenance | proxy_available | parameter_source | P0 | dataset, method, and pre-scoring timestamp ledger | document every family label and kernel observable source | no undocumented manual adjustment | all rows have auditable residual-blind provenance | must be upgraded before discovery-style endpoint claim |

## Collection Batches

| batch | purpose | fields | entry_condition | exit_condition |
| --- | --- | --- | --- | --- |
| B0_protocol_lock | freeze endpoint lanes, amplitude policy, forbidden inputs, and source intake schema | all protocol fields | current package reproduced | source collection begins without changing endpoint gates |
| B1_core_labels_and_quality | replace proxy family labels, confidence, caveats, and provenance | formula_family; manifest_confidence; manifest_caveat; observable_provenance | source catalogs/images chosen before scoring | every row has residual-blind family label and provenance |
| B2_active_family_kernel_observables | replace proxy kernel-driving fields for active 1D SPARC morphology families | scale_radius_kpc; tail_inner_radius_kpc; tail_cutoff_radius_kpc; compact_support_radius_kpc; thickness_h_over_rs | B1 complete | all active-family required fields accepted or row explicitly caveated |
| B3_optional_non_axisymmetric_extension | prepare ring, bar, and lopsided branches without promoting them from 1D residuals | ring_radius_kpc; bar_m2_strength; lopsided_m1_strength | external morphology or velocity-field support exists | non-axisymmetric branch declared as separate endpoint or kept caveated |
| B4_blind_endpoint_run | run the frozen matched-vs-wrong family endpoint on accepted observables | all promoted fields | B1 and B2 complete with no missing required accepted fields | matched/wrong, shuffled-K, Newtonian, MOND, RAR, and TGP comparisons reported |

## Claim Boundary

Completing this plan would still not by itself prove Tau Core.

Completing this plan would make the endpoint auditable; it would still not
by itself prove Tau Core or guarantee a baseline win. The empirical claim
can only be assessed after the frozen protocol is rerun on the accepted
observables.
