# Readout-Subfamily External Source Acquisition

This pass records targeted external source hits for the first-pass
readout-subfamily evidence matrix. It is residual-blind: no endpoint
score, best-fit readout, or required-S_tau diagnostic is used to promote
a label.

## By Galaxy

| galaxy | proposed_readout_subfamily | post_acquisition_status | n_items | n_external_hits | n_review_ready | galaxy_external_hits | galaxy_matched_hits | galaxy_hit_ids |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IC2574 | K_disturbed_outer_tail | REVIEW_READY_NOT_ACCEPTED | 3 | 3 | 3 | 3 | 3 | hi_asymmetry_map;environment_history;outer_tail_transition |
| IC2574 | K_disturbed_outer_tail | SOURCE_SEARCH_STILL_REQUIRED | 1 | 0 | 0 | 3 | 3 | hi_asymmetry_map;environment_history;outer_tail_transition |
| IC4202 | K_true_compact | SOURCE_SEARCH_STILL_REQUIRED | 3 | 1 | 0 | 1 | 1 | compact_support_radius |
| NGC4013 | K_true_compact | REVIEW_READY_NOT_ACCEPTED | 1 | 1 | 1 | 1 | 1 | disk_overlay_check |
| NGC4013 | K_true_compact | SOURCE_SEARCH_STILL_REQUIRED | 2 | 0 | 0 | 1 | 1 | disk_overlay_check |
| NGC4088 | K_warp_history_coupled | SOURCE_SEARCH_STILL_REQUIRED | 4 | 0 | 0 | 0 | 0 |  |
| NGC4183 | K_expdisk_overlay | SOURCE_SEARCH_STILL_REQUIRED | 3 | 1 | 0 | 1 | 1 | bar_core_projection_history_overlay |
| NGC5907 | K_projection_dominated | REVIEW_READY_NOT_ACCEPTED | 3 | 3 | 3 | 3 | 3 | velocity_field_sanity;vertical_or_warp_source;projection_geometry |
| NGC7331 | K_thick_regular | REVIEW_READY_NOT_ACCEPTED | 1 | 1 | 1 | 1 | 1 | vertical_scale_or_thickness |
| NGC7331 | K_thick_regular | SOURCE_SEARCH_STILL_REQUIRED | 2 | 0 | 0 | 1 | 1 | vertical_scale_or_thickness |
| UGC05716 | K_disturbed_outer_tail | SOURCE_SEARCH_STILL_REQUIRED | 4 | 1 | 0 | 1 | 1 | hi_asymmetry_map |
| UGC12506 | K_expdisk_overlay | SOURCE_SEARCH_STILL_REQUIRED | 3 | 0 | 0 | 1 | 0 | disk_scale_overlay |

## Review-Ready Source Hits

| galaxy | proposed_readout_subfamily | evidence_id | source_status | source_authors_year | source_title | source_url | promotion_relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IC2574 | K_disturbed_outer_tail | hi_asymmetry_map | DIRECT_HI_CONTEXT_READY_REVIEW_REQUIRED | de Blok et al. / MNRAS 2020 source family | 5 deg x 5 deg deep HI survey of the M81 group - II. HI distribution and kinematics of IC 2574 and HIJASS J1021+68 | https://academic.oup.com/mnras/article/493/2/2618/5734519 | candidate source for disturbed-tail/HI-envelope subfamily; asymmetry and tail-transition radii still need extraction |
| IC2574 | K_disturbed_outer_tail | outer_tail_transition | DIRECT_ASYMMETRY_CONTEXT_READY_REVIEW_REQUIRED | Sánchez-Salcedo & Hidalgo-Gámez 2002 | A New Look at the Holes of IC 2574 | https://astronomia.unam.mx/journals/rmxaa/article/view/2002rmxaa..38...39s | candidate evidence for K_disturbed_outer_tail; needs accepted extraction/audit |
| IC2574 | K_disturbed_outer_tail | environment_history | DIRECT_HI_CONTEXT_READY_REVIEW_REQUIRED | Walter & Brinks 1999 | Holes and Shells in the Interstellar Medium of the Nearby Dwarf Galaxy IC 2574 | https://arxiv.org/abs/astro-ph/9904002 | supports morphology-memory/disturbed-gas review; not a tail-transition measurement by itself |
| NGC4013 | K_true_compact | disk_overlay_check | DIRECT_HI_WARP_CONTEXT_READY_REVIEW_REQUIRED | Zschaechner & Rand 2015 | The HI Kinematics of NGC 4013: a Steep and Radially Shallowing Extra-planar Rotational Lag | https://arxiv.org/abs/1506.05123 | warns compact-only classification may need disk/warp overlay review |
| NGC5907 | K_projection_dominated | projection_geometry | DIRECT_OPTICAL_WARP_CONTEXT_READY_REVIEW_REQUIRED | Sasaki 1987 | Surface Photometry of the Warping Edge-on Galaxy NGC 5907 | https://academic.oup.com/pasj/article/39/6/849/8078264 | supports projection/warp review; no endpoint label promotion |
| NGC5907 | K_projection_dominated | velocity_field_sanity | DIRECT_WARP_INTERACTION_CONTEXT_READY_REVIEW_REQUIRED | Shang et al. 1998 | Ring structure and warp of NGC 5907 -- Interaction with dwarf galaxies | https://arxiv.org/abs/astro-ph/9806395 | supports projection/warp/history audit for K_projection_dominated or warp overlay |
| NGC5907 | K_projection_dominated | vertical_or_warp_source | DIRECT_VERTICAL_CONTEXT_READY_REVIEW_REQUIRED | Wiegert et al. 2015 | The Interstellar Medium and Star Formation in Edge-On Galaxies. II. NGC 4157, 4565, and 5907 | https://arxiv.org/abs/1408.5905 | candidate source for projection/vertical sanity; needs subfamily-specific extraction |
| NGC7331 | K_thick_regular | vertical_scale_or_thickness | DIRECT_VERTICAL_CONTEXT_READY_REVIEW_REQUIRED | Patra 2018 | Molecular scale height in NGC 7331 | https://arxiv.org/abs/1706.08615 | candidate source for K_thick_regular vertical-scale acceptance; needs mapping into h/Rs |

## All Targeted Source Hits

| galaxy | evidence_id | matched_evidence_row | source_status | source_authors_year | source_title | source_url | promotion_relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IC2574 | hi_asymmetry_map | True | DIRECT_HI_CONTEXT_READY_REVIEW_REQUIRED | de Blok et al. / MNRAS 2020 source family | 5 deg x 5 deg deep HI survey of the M81 group - II. HI distribution and kinematics of IC 2574 and HIJASS J1021+68 | https://academic.oup.com/mnras/article/493/2/2618/5734519 | candidate source for disturbed-tail/HI-envelope subfamily; asymmetry and tail-transition radii still need extraction |
| IC2574 | environment_history | True | DIRECT_HI_CONTEXT_READY_REVIEW_REQUIRED | Walter & Brinks 1999 | Holes and Shells in the Interstellar Medium of the Nearby Dwarf Galaxy IC 2574 | https://arxiv.org/abs/astro-ph/9904002 | supports morphology-memory/disturbed-gas review; not a tail-transition measurement by itself |
| IC2574 | outer_tail_transition | True | DIRECT_ASYMMETRY_CONTEXT_READY_REVIEW_REQUIRED | Sánchez-Salcedo & Hidalgo-Gámez 2002 | A New Look at the Holes of IC 2574 | https://astronomia.unam.mx/journals/rmxaa/article/view/2002rmxaa..38...39s | candidate evidence for K_disturbed_outer_tail; needs accepted extraction/audit |
| NGC4013 | disk_overlay_check | True | DIRECT_HI_WARP_CONTEXT_READY_REVIEW_REQUIRED | Zschaechner & Rand 2015 | The HI Kinematics of NGC 4013: a Steep and Radially Shallowing Extra-planar Rotational Lag | https://arxiv.org/abs/1506.05123 | warns compact-only classification may need disk/warp overlay review |
| NGC5907 | velocity_field_sanity | True | DIRECT_WARP_INTERACTION_CONTEXT_READY_REVIEW_REQUIRED | Shang et al. 1998 | Ring structure and warp of NGC 5907 -- Interaction with dwarf galaxies | https://arxiv.org/abs/astro-ph/9806395 | supports projection/warp/history audit for K_projection_dominated or warp overlay |
| NGC5907 | vertical_or_warp_source | True | DIRECT_VERTICAL_CONTEXT_READY_REVIEW_REQUIRED | Wiegert et al. 2015 | The Interstellar Medium and Star Formation in Edge-On Galaxies. II. NGC 4157, 4565, and 5907 | https://arxiv.org/abs/1408.5905 | candidate source for projection/vertical sanity; needs subfamily-specific extraction |
| NGC5907 | projection_geometry | True | DIRECT_OPTICAL_WARP_CONTEXT_READY_REVIEW_REQUIRED | Sasaki 1987 | Surface Photometry of the Warping Edge-on Galaxy NGC 5907 | https://academic.oup.com/pasj/article/39/6/849/8078264 | supports projection/warp review; no endpoint label promotion |
| NGC7331 | vertical_scale_or_thickness | True | DIRECT_VERTICAL_CONTEXT_READY_REVIEW_REQUIRED | Patra 2018 | Molecular scale height in NGC 7331 | https://arxiv.org/abs/1706.08615 | candidate source for K_thick_regular vertical-scale acceptance; needs mapping into h/Rs |
| NGC4183 | bar_core_projection_history_overlay | True | HI_WARP_SAMPLE_CONTEXT_REVIEW_REQUIRED | García-Ruiz et al. 2002 / WHISP source family | Warps and lopsidedness in HI disks from WHISP edge-on samples | https://arxiv.org/abs/1103.4928 | candidate projection/overlay source path for NGC4183; primary paper/table extraction still required |
| UGC05716 | hi_asymmetry_map | True | HI_PROFILE_SOURCE_CANDIDATE_REVIEW_REQUIRED | Swaters et al. 2009 | The rotation curves shapes of late-type dwarf galaxies | https://astroweb.case.edu/ssm/papers/AAv505p577.pdf | candidate source for disturbed-tail review; specific HI asymmetry/transition extraction still missing |
| IC4202 | compact_support_radius | True | NO_TARGETED_EXTERNAL_SOURCE_HIT_THIS_PASS |  |  |  | query S4G/NED/SIMBAD/decomposition next |
| UGC12506 | disk_scale_overlay | False | NO_TARGETED_EXTERNAL_SOURCE_HIT_THIS_PASS |  |  |  | query S4G/NED/decomposition and overlay/projection review next |

## Source Hit Summary

| galaxy | source_status | n_hits | matched_hits | evidence_ids | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| IC2574 | DIRECT_ASYMMETRY_CONTEXT_READY_REVIEW_REQUIRED | 1 | 1 | outer_tail_transition | readout_subfamily_external_source_acquisition_not_endpoint |
| IC2574 | DIRECT_HI_CONTEXT_READY_REVIEW_REQUIRED | 2 | 2 | hi_asymmetry_map;environment_history | readout_subfamily_external_source_acquisition_not_endpoint |
| IC4202 | NO_TARGETED_EXTERNAL_SOURCE_HIT_THIS_PASS | 1 | 1 | compact_support_radius | readout_subfamily_external_source_acquisition_not_endpoint |
| NGC4013 | DIRECT_HI_WARP_CONTEXT_READY_REVIEW_REQUIRED | 1 | 1 | disk_overlay_check | readout_subfamily_external_source_acquisition_not_endpoint |
| NGC4183 | HI_WARP_SAMPLE_CONTEXT_REVIEW_REQUIRED | 1 | 1 | bar_core_projection_history_overlay | readout_subfamily_external_source_acquisition_not_endpoint |
| NGC5907 | DIRECT_OPTICAL_WARP_CONTEXT_READY_REVIEW_REQUIRED | 1 | 1 | projection_geometry | readout_subfamily_external_source_acquisition_not_endpoint |
| NGC5907 | DIRECT_VERTICAL_CONTEXT_READY_REVIEW_REQUIRED | 1 | 1 | vertical_or_warp_source | readout_subfamily_external_source_acquisition_not_endpoint |
| NGC5907 | DIRECT_WARP_INTERACTION_CONTEXT_READY_REVIEW_REQUIRED | 1 | 1 | velocity_field_sanity | readout_subfamily_external_source_acquisition_not_endpoint |
| NGC7331 | DIRECT_VERTICAL_CONTEXT_READY_REVIEW_REQUIRED | 1 | 1 | vertical_scale_or_thickness | readout_subfamily_external_source_acquisition_not_endpoint |
| UGC05716 | HI_PROFILE_SOURCE_CANDIDATE_REVIEW_REQUIRED | 1 | 1 | hi_asymmetry_map | readout_subfamily_external_source_acquisition_not_endpoint |
| UGC12506 | NO_TARGETED_EXTERNAL_SOURCE_HIT_THIS_PASS | 1 | 0 | disk_scale_overlay | readout_subfamily_external_source_acquisition_not_endpoint |

## Claim Boundary

A source hit is not an accepted subfamily label. The review-ready rows
must still be audited for the exact observable required by the subfamily
gate, such as warp onset, HI asymmetry, compact support radius, projection
safety, or vertical scale mapping.
