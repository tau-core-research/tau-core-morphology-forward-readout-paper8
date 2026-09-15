# HALOGAS confirmatory candidate-pool audit v01

Status: `SOURCE_ACQUISITION_ONLY_HALOGAS_ALONE_INSUFFICIENT_FOR_CONFIRMATORY_N12`.

This audit reads the cached Heald et al. (2011) sample table, the HALOGAS DR1 Zenodo file manifest, the Paper 8 SPARC membership table, and the cached de Blok et al. (2008) source text for NGC925. It does not open a HALOGAS FITS image or calculate a new endpoint statistic; it imports the separately frozen NGC4062 result.

The 24-object HALOGAS sample leaves `7` moderate-inclination, endpoint-unopened objects after prior Paper 8 rotation/development exposure is removed, but source audit leaves `0` clean candidates. The frozen confirmatory minimum is 12.

NGC3198 is excluded because its diagnostic and replay scores were already opened. NGC5055 is excluded because it was in the Paper 8 SPARC training population. The first source-acquisition target is NGC925: the primary THINGS paper provides the centre, 3-arcsec sampling, mean inclination and PA, and an adopted radial geometry curve in Figure 68. Both adopted orientation curves are now reproducibly digitized into 93 rings. An independent residual-rescrambling Monte Carlo supplies 15 marginal orientation-error pairs, but its source declares the inner 250 arcsec non-identifiable. Six outer rings have adequate ideal beam capacity, yet the same outer disk is a documented minor-merger stream with warp/spiral ambiguity and anomalous gas. NGC925 is therefore demoted from a clean primary endpoint and retained only as a disturbed-system robustness/stronger-terminal case. NGC4062 was then frozen and opened as the only remaining clean HALOGAS case: HR and LR are both consistent with zero, while the sign is unstable between the two published systemic-velocity choices. Every remaining moderate-inclination unopened HALOGAS system is source-flagged as interacting, substantially warped, kinematically complex, or too poorly resolved for the clean lane. HALOGAS therefore has no further clean candidate under this protocol. These standard-physics limitations and the NGC4062 null result are not Tau evidence.

| galaxy | i (deg) | prior endpoint exposure | source geometry/status | status |
| --- | ---: | --- | --- | --- |
| NGC0672 | 70 | False | INTERACTING_COMPANION_CONTAMINATION | SOURCE_DEMOTED_FROM_CLEAN_CONFIRMATORY_LANE |
| NGC0891 | 84 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| NGC0925 | 54 | False | PHYSICAL_MC_ACQUIRED_INNER_NONIDENTIFIABLE_OUTER_TERMINAL_CONTAMINATED | SOURCE_DEMOTED_FROM_CLEAN_CONFIRMATORY_LANE |
| NGC0949 | 52 | False | HALOGAS_WARP_GT10_DEG_CONSTANT_GEOMETRY_ONLY | SOURCE_DEMOTED_FROM_CLEAN_CONFIRMATORY_LANE |
| UGC2082 | 89 | False | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_EDGE_ON_FOR_CURRENT_SIDE_GEOMETRY_PROTOCOL |
| NGC1003 | 67 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| NGC2403 | 62 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| UGC4278 | 90 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| NGC2541 | 67 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| NGC3198 | 71 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| NGC4062 | 68 | True | SOURCE_GEOMETRY_COMPLETE_TWO_RING_ENDPOINT_OPENED_NULL_AND_ZEROPOINT_UNSTABLE | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| NGC4244 | 90 | False | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_EDGE_ON_FOR_CURRENT_SIDE_GEOMETRY_PROTOCOL |
| NGC4258 | 71 | False | HALOGAS_WARP_STREAMING_ACTIVE_NUCLEUS_COMPLEX | SOURCE_DEMOTED_FROM_CLEAN_CONFIRMATORY_LANE |
| NGC4274 | 72 | False | HALOGAS_FEW_RESOLUTION_ELEMENTS_BEAM_SMEARING_LIMITED | SOURCE_DEMOTED_FROM_CLEAN_CONFIRMATORY_LANE |
| NGC4414 | 50 | False | HALOGAS_PA_WARP_WHOLE_CUBE_POOR_FIT | SOURCE_DEMOTED_FROM_CLEAN_CONFIRMATORY_LANE |
| NGC4448 | 71 | False | HALOGAS_FEW_RESOLUTION_ELEMENTS_BEAM_SMEARING_LIMITED | SOURCE_DEMOTED_FROM_CLEAN_CONFIRMATORY_LANE |
| NGC4559 | 69 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| NGC4565 | 90 | False | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_EDGE_ON_FOR_CURRENT_SIDE_GEOMETRY_PROTOCOL |
| UGC7774 | 90 | False | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_EDGE_ON_FOR_CURRENT_SIDE_GEOMETRY_PROTOCOL |
| NGC4631 | 85 | False | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_EDGE_ON_FOR_CURRENT_SIDE_GEOMETRY_PROTOCOL |
| NGC5023 | 90 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| NGC5055 | 55 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| NGC5229 | 90 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |
| NGC5585 | 51 | True | SIGNED_RADIAL_IPA_SOURCE_NOT_YET_ACQUIRED | EXCLUDED_PRIOR_ENDPOINT_EXPOSURE |

No new endpoint score is authorized by this audit. NGC925 endpoint access remains closed for the clean confirmatory lane; any later disturbed-system route requires a separately frozen stronger terminal or contamination treatment. A population claim additionally requires at least four eligible galaxies from an independent survey family or a preregistered change to the sample-size design.
