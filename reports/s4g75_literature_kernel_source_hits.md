# S4G75 Literature Kernel Source Hits

This report records targeted literature/source hits for the remaining S4G75 kernel blockers. It is source acquisition only: no accepted label is created and no endpoint score is computed.

## Verdict

One strong direct vertical-profile source is recorded for NGC2683, but it requires a residual-blind mapping from a flare profile into the current thick/flared executable kernel. Several scale-tail rows have candidate HI atlas/profile source families, but no direct transition radius is extracted in this pass.

## Summary

| blocker_class | literature_status | endpoint_mapping_status | n_galaxies | galaxies | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| SCALE_TAIL_TRANSITION_MISSING | HI_ATLAS_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION | ATLAS_PROFILE_EXTRACTION_REQUIRED | 2 | UGC06917;UGC06983 | s4g75_literature_kernel_source_hits_not_endpoint |
| SCALE_TAIL_TRANSITION_MISSING | HI_ROTATION_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION | PROFILE_EXTRACTION_REQUIRED | 3 | UGC00891;UGC04499;UGC05829 | s4g75_literature_kernel_source_hits_not_endpoint |
| SCALE_TAIL_TRANSITION_MISSING | HI_WARP_PROFILE_CONTEXT_READY_TRANSITION_RADIUS_NOT_EXTRACTED | DIRECT_TRANSITION_EXTRACTION_REQUIRED | 1 | NGC4214 | s4g75_literature_kernel_source_hits_not_endpoint |
| VERTICAL_KERNEL_MISSING | DIRECT_LITERATURE_FLARE_PROFILE_READY_MAPPING_REQUIRED | MAPPING_REQUIRED_PROFILE_TO_THICK_FLARED_EXECUTABLE_KERNEL | 1 | NGC2683 | s4g75_literature_kernel_source_hits_not_endpoint |
| VERTICAL_KERNEL_MISSING | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS | SOURCE_SEARCH_STILL_REQUIRED | 6 | NGC0024;NGC3726;NGC3949;NGC4088;NGC3972;NGC4389 | s4g75_literature_kernel_source_hits_not_endpoint |

## Galaxy-Level Hits

| galaxy | formula_family | blocker_class | literature_status | source_authors_year | source_title | source_url | extracted_profile | endpoint_mapping_status | promotion_interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4214 | K_scale_tail_spiral | SCALE_TAIL_TRANSITION_MISSING | HI_WARP_PROFILE_CONTEXT_READY_TRANSITION_RADIUS_NOT_EXTRACTED | Lelli, Verheijen & Fraternali 2014 | Dynamics of Starbursting Dwarf Galaxies. III. A HI study of 18 nearby objects | https://arxiv.org/abs/1404.6252 | no machine-extracted tail transition radius in this pass | DIRECT_TRANSITION_EXTRACTION_REQUIRED | source is relevant for HI/warp morphology, but no direct tail inner/cutoff transition radius has been extracted |
| UGC06917 | K_scale_tail_spiral | SCALE_TAIL_TRANSITION_MISSING | HI_ATLAS_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION | Verheijen & Sancisi 2001 | The Ursa Major Cluster of Galaxies. IV: HI synthesis observations | https://arxiv.org/abs/astro-ph/0101404 | no galaxy-specific transition radius parsed in this pass | ATLAS_PROFILE_EXTRACTION_REQUIRED | candidate direct profile source exists, but the transition/break radius must be extracted residual-blind before promotion |
| UGC06983 | K_scale_tail_spiral | SCALE_TAIL_TRANSITION_MISSING | HI_ATLAS_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION | Verheijen & Sancisi 2001 | The Ursa Major Cluster of Galaxies. IV: HI synthesis observations | https://arxiv.org/abs/astro-ph/0101404 | no galaxy-specific transition radius parsed in this pass | ATLAS_PROFILE_EXTRACTION_REQUIRED | candidate direct profile source exists, but the transition/break radius must be extracted residual-blind before promotion |
| NGC0024 | K_thick_flared | VERTICAL_KERNEL_MISSING | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS |  |  |  |  | SOURCE_SEARCH_STILL_REQUIRED | no targeted source hit recorded in this pass |
| NGC2683 | K_thick_flared | VERTICAL_KERNEL_MISSING | DIRECT_LITERATURE_FLARE_PROFILE_READY_MAPPING_REQUIRED | Vollmer, Nehlig & Ibata 2016 | The flaring HI disk of the nearby spiral galaxy NGC 2683 | https://arxiv.org/abs/1512.07058 | flare height H=FWHM/2 rises from 0.5 kpc at R=9 kpc to 4 kpc at R=15 kpc, remains constant to R=22 kpc, then decreases; outer low-surface-density ring has vertical offset 1.3 kpc | MAPPING_REQUIRED_PROFILE_TO_THICK_FLARED_EXECUTABLE_KERNEL | direct vertical/flare source evidence exists, but the current executable endpoint uses a scalar h/Rs proxy; do not override endpoint fields until a residual-blind profile-to-kernel mapping is implemented |
| NGC3726 | K_thick_flared | VERTICAL_KERNEL_MISSING | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS |  |  |  |  | SOURCE_SEARCH_STILL_REQUIRED | no targeted source hit recorded in this pass |
| NGC3949 | K_thick_flared | VERTICAL_KERNEL_MISSING | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS |  |  |  |  | SOURCE_SEARCH_STILL_REQUIRED | no targeted source hit recorded in this pass |
| NGC4088 | K_thick_flared | VERTICAL_KERNEL_MISSING | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS |  |  |  |  | SOURCE_SEARCH_STILL_REQUIRED | no targeted source hit recorded in this pass |
| UGC00891 | K_scale_tail_spiral | SCALE_TAIL_TRANSITION_MISSING | HI_ROTATION_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION | van Zee et al. 1997 | van Zee et al. 1997 / SPARC vZ97 reference family | https://adsabs.harvard.edu/pdf/1997AJ....113.1638V | no direct tail transition radius parsed in this pass | PROFILE_EXTRACTION_REQUIRED | source family remains a candidate until the needed outer transition radius is extracted from the source-native profile |
| UGC04499 | K_scale_tail_spiral | SCALE_TAIL_TRANSITION_MISSING | HI_ROTATION_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION | Swaters et al. 2009 | The rotation curves shapes of late-type dwarf galaxies | https://arxiv.org/abs/0901.4222 | no direct tail transition radius parsed in this pass | PROFILE_EXTRACTION_REQUIRED | source family remains a candidate until the needed outer transition radius is extracted from the source-native profile |
| UGC05829 | K_scale_tail_spiral | SCALE_TAIL_TRANSITION_MISSING | HI_ROTATION_PROFILE_SOURCE_CANDIDATE_NEEDS_EXTRACTION | Swaters et al. 2009 | The rotation curves shapes of late-type dwarf galaxies | https://arxiv.org/abs/0901.4222 | no direct tail transition radius parsed in this pass | PROFILE_EXTRACTION_REQUIRED | source family remains a candidate until the needed outer transition radius is extracted from the source-native profile |
| NGC3972 | K_thick_flared | VERTICAL_KERNEL_MISSING | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS |  |  |  |  | SOURCE_SEARCH_STILL_REQUIRED | no targeted source hit recorded in this pass |
| NGC4389 | K_thick_flared | VERTICAL_KERNEL_MISSING | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS |  |  |  |  | SOURCE_SEARCH_STILL_REQUIRED | no targeted source hit recorded in this pass |

## Claim Boundary

A literature source hit is not endpoint eligibility. NGC2683 is a direct profile candidate, not a scalar h/Rs override. Tail-source hits remain profile-extraction tasks until a residual-blind transition radius is measured or a Tau-side promotion theorem is accepted.
