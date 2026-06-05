# S4G75 Vertical Source Search Audit

This audit records targeted vertical/flare source-search evidence for the thick/flared blockers. It deliberately records negative searches and general context sources without promoting them to kernel readiness.

## Verdict

NGC2683 remains the only row with a direct profile source. NGC3972 and NGC4088 still need galaxy-specific vertical scale, flare, warp, or gas-plane-thickness extraction. HALOGAS and Patra 2020 are useful context for extraplanar/scale-height physics, but they are not direct NGC3972/NGC4088 kernel inputs in this pass.

## Summary

| galaxy | n_source_checks | any_direct_profile | statuses | kernel_relevance | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC2683 | 1 | True | DIRECT_PROFILE_SOURCE_ALREADY_REGISTERED | DIRECT_PROFILE_READY_FOR_MAPPING_NOT_ENDPOINT | False | s4g75_vertical_source_search_audit_not_endpoint |
| NGC3972 | 4 | False | HI_MORPHOLOGY_SOURCE_READY_VERTICAL_KERNEL_NOT_EXTRACTED;OBJECT_CONTEXT_ONLY_NOT_VERTICAL_KERNEL;WHISP_URSA_MAJOR_OBSERVING_PARAMETERS_ONLY;HALOGAS_TEXT_SEARCH_NEGATIVE_FOR_OBJECT | OBJECT_HI_MORPHOLOGY_READY_NOT_VERTICAL_KERNEL;CONTEXT_ONLY_NOT_KERNEL_INPUT;OBJECT_HI_OBSERVING_CONTEXT_NOT_VERTICAL_KERNEL;GENERAL_EPG_CONTEXT_NOT_GALAXY_KERNEL | False | s4g75_vertical_source_search_audit_not_endpoint |
| NGC4088 | 4 | False | WHISP_WARP_ASYMMETRY_SOURCE_READY_PROFILE_NOT_EXTRACTED;HI_KINEMATIC_ASYMMETRY_SOURCE_READY_NOT_VERTICAL_KERNEL;HALOGAS_TEXT_SEARCH_NEGATIVE_FOR_OBJECT;GENERAL_HI_SCALE_HEIGHT_CONTEXT_ONLY | OBJECT_WARP_ASYMMETRY_READY_NEEDS_PROFILE_EXTRACTION;OBJECT_HI_ASYMMETRY_READY_NOT_VERTICAL_KERNEL;GENERAL_EPG_CONTEXT_NOT_GALAXY_KERNEL;THEORY_CONTEXT_NOT_OBJECT_KERNEL | False | s4g75_vertical_source_search_audit_not_endpoint |

## Source Checks

| galaxy | source_status | source_authors_year | source_title | source_url | kernel_relevance | direct_profile_extracted | endpoint_scores_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC2683 | DIRECT_PROFILE_SOURCE_ALREADY_REGISTERED | Vollmer, Nehlig & Ibata 2016 | The flaring HI disk of the nearby spiral galaxy NGC 2683 | https://arxiv.org/abs/1512.07058 | DIRECT_PROFILE_READY_FOR_MAPPING_NOT_ENDPOINT | True | False |
| NGC3972 | HI_MORPHOLOGY_SOURCE_READY_VERTICAL_KERNEL_NOT_EXTRACTED | O'Brien et al. 2016 | Baryonic distributions in galaxy dark matter haloes I | https://academic.oup.com/mnras/article/460/1/689/2608817 | OBJECT_HI_MORPHOLOGY_READY_NOT_VERTICAL_KERNEL | False | False |
| NGC3972 | OBJECT_CONTEXT_ONLY_NOT_VERTICAL_KERNEL | NASA/Hubble object page | NGC 3972 HST/NASA object context | https://science.nasa.gov/asset/hubble/ngc-3972/ | CONTEXT_ONLY_NOT_KERNEL_INPUT | False | False |
| NGC3972 | WHISP_URSA_MAJOR_OBSERVING_PARAMETERS_ONLY | Verheijen & Sancisi 2001 | The Ursa Major Cluster of Galaxies. IV: HI synthesis observations | https://www.aanda.org/articles/aa/pdf/2001/18/aa10469.pdf | OBJECT_HI_OBSERVING_CONTEXT_NOT_VERTICAL_KERNEL | False | False |
| NGC3972 | HALOGAS_TEXT_SEARCH_NEGATIVE_FOR_OBJECT | Marasco et al. 2019 | HALOGAS: the properties of extraplanar HI in disc galaxies | https://arxiv.org/abs/1909.04048 | GENERAL_EPG_CONTEXT_NOT_GALAXY_KERNEL | False | False |
| NGC4088 | WHISP_WARP_ASYMMETRY_SOURCE_READY_PROFILE_NOT_EXTRACTED | Verheijen & Sancisi 2001 | The Ursa Major Cluster of Galaxies. IV: HI synthesis observations | https://www.aanda.org/articles/aa/pdf/2001/18/aa10469.pdf | OBJECT_WARP_ASYMMETRY_READY_NEEDS_PROFILE_EXTRACTION | False | False |
| NGC4088 | HI_KINEMATIC_ASYMMETRY_SOURCE_READY_NOT_VERTICAL_KERNEL | O'Brien et al. 2018 | Baryonic distributions in galaxy dark matter haloes II | https://academic.oup.com/mnras/article/476/4/5127/4907988 | OBJECT_HI_ASYMMETRY_READY_NOT_VERTICAL_KERNEL | False | False |
| NGC4088 | HALOGAS_TEXT_SEARCH_NEGATIVE_FOR_OBJECT | Marasco et al. 2019 | HALOGAS: the properties of extraplanar HI in disc galaxies | https://arxiv.org/abs/1909.04048 | GENERAL_EPG_CONTEXT_NOT_GALAXY_KERNEL | False | False |
| NGC4088 | GENERAL_HI_SCALE_HEIGHT_CONTEXT_ONLY | Patra 2020 | HI scale height in spiral galaxies | https://arxiv.org/abs/2009.11299 | THEORY_CONTEXT_NOT_OBJECT_KERNEL | False | False |

## Claim Boundary

General HI flaring or EPG literature can justify a future theorem lane, but it cannot fill a galaxy-specific kernel observable unless the needed profile/bound is extracted residual-blind for that galaxy.
