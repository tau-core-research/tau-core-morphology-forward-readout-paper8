# P0 Readout-Relevant Morphology Proxy

This layer separates the apparent 4D morphology label from the possible
Tau-side readout-relevant morphology proxy. The current P0 Codex/source
review labels all have an apparent 4D `K_exponential_disk` handle, but
source-side caveats suggest different readout-relevant corrections.

## Summary

| readout_relevant_proxy_family | n_galaxies | median_review_confidence | uses_rotation_residuals | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| K_barred_expdisk_m2_overlay | 1 | 0.78 | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |
| K_clean_exponential_disk_control | 1 | 0.88 | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |
| K_expdisk_compact_core_overlay | 1 | 0.74 | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |
| K_projection_corrected_expdisk | 1 | 0.7 | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |

## Proxy Rows

| galaxy | observed_4d_family_label | observed_4d_morphology_label | manifest_caveat | review_confidence | readout_relevant_proxy_family | readout_proxy_components | proxy_reason | pilot_implication | uses_rotation_residuals | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0100 | K_exponential_disk | edge-on disk; S4G Z edge-disk component; projection-caveated | edge_projection_caveat | 0.7 | K_projection_corrected_expdisk | K_exponential_disk+projection_or_thick_flared_correction | apparent 4D disk label is projection-contaminated; readout may require edge/thickness correction | plain K_exponential_disk is expected to be a weak control, not final readout | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |
| NGC0247 | K_exponential_disk | disk with S4G BAR component; barred-disk caveat | bar_component_caveat | 0.78 | K_barred_expdisk_m2_overlay | K_exponential_disk+barred_spiral_m2_overlay | apparent disk label has bar support; 1D expdisk readout may miss non-axisymmetric m=2 structure | plain K_exponential_disk is a baseline component; bar overlay should be tested separately | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |
| NGC0300 | K_exponential_disk | disk/spiral; S4G D component; DustPedia direct match | none | 0.88 | K_clean_exponential_disk_control | K_exponential_disk | source-reviewed 4D disk label has no current source-side correction caveat | plain K_exponential_disk is the appropriate first control | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |
| NGC6503 | K_exponential_disk | disk/spiral; S4G D component with nuclear component caveat | nuclear_component_caveat | 0.74 | K_expdisk_compact_core_overlay | K_exponential_disk+compact_finite_core_overlay | apparent disk label has nuclear/compact caveat; readout may include compact-core contribution | plain K_exponential_disk may underfit inner/transition structure | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |

## Interpretation

The thin/thick disk, bar, ring, compact, and tail labels are treated here
as projected 4D morphology handles, not as proven fundamental Tau-side
classes. A future endpoint should predeclare whether it tests the observed
4D handle directly or a source-justified readout-relevant proxy.
They are not as proven fundamental Tau-side classes.

This explains why a plain P0 `K_exponential_disk` pilot can be weak: only
one row is a clean exponential-disk control, while the other rows carry
projection, bar, or compact/nuclear correction caveats.

## Claim Boundary

This proxy does not use rotation residuals, does not compute endpoint scores,
and does not validate Tau Core. It is a pre-endpoint architecture layer for
separating observed 4D morphology from readout-relevant morphology.

Claim boundary: `p0_readout_relevant_morphology_proxy_not_endpoint`.
