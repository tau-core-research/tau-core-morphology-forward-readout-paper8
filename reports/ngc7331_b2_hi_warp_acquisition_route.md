# NGC7331 B2 H I Warp Acquisition Route

This route identifies source-native or source-figure paths for filling
the NGC7331 exact-transfer packet. It is not a formula freeze and not
an endpoint score.

## Source Candidates

| galaxy | source_id | source_rank | source_type | source_url | source_status | supports_fields | source_evidence | line_refs | download_or_cache_status | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_HI_SRC1_BOSMA_NED_21CM | 1 | literature_figures_and_tilted_ring_context | https://ned.ipac.caltech.edu/level5/March05/Bosma/Bosma4_7.html | PRIMARY_CONTEXT_SOURCE_FIGURE_DIGITIZATION_CANDIDATE | q_warp;sigma_warp;epsilon_cross_inputs | NGC7331 H I distribution is warped; channel maps show outer parts deviating from the main plane; tilted-ring model has radial PA/inclination curves; warp starts near 0.5 Holmberg radius | Bosma/NED lines 31-36, 67-84 | WEB_SOURCE_AVAILABLE_NO_LOCAL_FIGURE_DIGITIZATION_CACHE | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |
| NGC7331 | N7331_HI_SRC2_THINGS_DATA_PRODUCTS | 2 | public_hi_data_product_route | https://arxiv.org/abs/0810.2125 | PUBLIC_DATA_ROUTE_CACHED_AND_AUDITED_WORKSHEET_READY | q_warp;epsilon_cross_inputs | THINGS provides high-resolution H I data products, including integrated maps, velocity fields, dispersion maps, and channel maps | THINGS arXiv abstract lines 38-41 | LOCAL_THINGS_MOMENT_MAP_CACHE_AUDITED | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |
| NGC7331 | N7331_HI_SRC3_THINGS_RADIAL_GAS_MOTION_TABLE | 3 | derived_things_kinematic_context | https://academic.oup.com/mnras/article/457/3/2642/2588886 | SECONDARY_CONTEXT_SOURCE_NOT_WARP_AMPLITUDE | epsilon_cross_inputs | NGC7331 appears in a THINGS radial gas-motion analysis with H I mass, SFR, and radial-flow context; data products include moment maps and cubes | MNRAS table lines 147-161 and data-product discussion lines 194-196 | WEB_SOURCE_AVAILABLE_NOT_DIRECT_Q_WARP | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |
| NGC7331 | N7331_HI_SRC4_PATRA_VERTICAL_CONTEXT | 4 | vertical_projection_context | https://arxiv.org/abs/1706.08615 | SUPPORTING_CONTEXT_SOURCE_ALREADY_CACHED | sigma_warp;epsilon_cross_inputs | Patra records NGC7331 vertical/projection context and possible outer-warp emission, useful for sign and cross-term review | local cached text lines 715-721, 960-971, 1009-1024 | LOCAL_TEXT_CACHE_AVAILABLE | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |

## Extraction Routes

| galaxy | route_id | route_priority | route_goal | input_product | measurement_rule | required_outputs | current_route_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_HI_ROUTE1_THINGS_MOMENT_MAP_EXTRACTION | 1 | source-native q_warp amplitude and side-asymmetry bound | THINGS NGC7331 moment-0 and moment-1 maps or data cube | measure outer H I ridge displacement/asymmetry relative to inner disk and normalize by local disk reference extent | q_warp;side_asymmetry_bound;orientation_mismatch_bound | PREFERRED_ROUTE_SOURCE_PRODUCTS_CACHED_WORKSHEET_READY | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |
| NGC7331 | N7331_HI_ROUTE2_BOSMA_FIGURE_DIGITIZATION | 2 | fallback q_warp and sign/context extraction | Bosma/NED channel-map and tilted-ring figures | digitize outer H I contour/ridge offset and radial PA/inclination turning from published figures using a predeclared worksheet | q_warp_candidate;sigma_warp_context;epsilon_cross_context | FALLBACK_ROUTE_FIGURE_CACHE_OR_SCREENSHOT_PENDING | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |
| NGC7331 | N7331_HI_ROUTE3_TILTED_RING_PROFILE_EXTRACTION | 3 | orientation/sign rule and cross-term bound | radial PA(R), inclination(R), and H I surface density profile | extract direction changes, sign reversals, and outer/inner plane mismatch from source-side ring geometry | sigma_warp;orientation_mismatch_bound;locality_onset_coupling | PROFILE_NUMERICS_NOT_EXTRACTED | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |
| NGC7331 | N7331_HI_ROUTE4_CONTEXT_ONLY_CROSS_TERM_REVIEW | 4 | nonzero cross-term obligation review | Bosma complex warp context plus Patra vertical/projection context | decide whether cross terms may be assumed negligible; current evidence says no | epsilon_cross_must_be_bounded_or_carried | CONTEXT_READY_BOUND_NOT_CLOSED | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_HIAG1_SOURCE_CANDIDATES_IDENTIFIED | PASS | Bosma/NED, THINGS, radial gas-motion, and Patra routes are identified | none at candidate-identification level | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |
| NGC7331 | N7331_HIAG2_SOURCE_NATIVE_HI_PRODUCT_CACHED | PASS | THINGS NGC7331 moment maps are locally cached and FITS-audited | build residual-blind q_warp/sign/cross-term measurement worksheet | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |
| NGC7331 | N7331_HIAG3_Q_WARP_MEASURABLE | BLOCKED_EXTRACTION_PENDING | q_warp requires actual H I ridge/asymmetry measurement | measure q_warp with a residual-blind worksheet | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |
| NGC7331 | N7331_HIAG4_SIGMA_SIGN_REVIEW | BLOCKED_SIGN_REVIEW_PENDING | Bosma complex warp/opposite-direction context prevents inherited sign | freeze added-readout/attenuation convention from source geometry | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |
| NGC7331 | N7331_HIAG5_ENDPOINT_BLINDNESS | PASS | route uses source candidates and geometry requirements only | future scoring must remain separate after formula freeze | False | False | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |

## Summary

| galaxy | hi_warp_acquisition_status | source_evidence_review_status | n_source_candidates | n_extraction_routes | n_gates | n_pass | n_blocked | preferred_next_route | fallback_next_route | q_warp_measurement_ready | sigma_warp_sign_ready | epsilon_cross_bound_ready | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | population_claim_allowed | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_HI_WARP_ACQUISITION_ROUTE_SOURCE_PRODUCTS_CACHED_WORKSHEET_READY | NGC7331_SOURCE_EVIDENCE_REVIEW_BUILT_EXACT_TRANSFER_STILL_BLOCKED | 4 | 4 | 5 | 3 | 2 | THINGS_QWARP_SIGN_CROSS_TERM_WORKSHEET | BOSMA_FIGURE_DIGITIZATION_WORKSHEET | False | False | False | False | False | False | False | build/fill residual-blind THINGS q_warp, sign, and cross-term worksheet | ngc7331_b2_hi_warp_acquisition_route_not_endpoint |

## Interpretation

The preferred next route is source-native THINGS H I map/cube acquisition.
If that remains unavailable, Bosma/NED figure digitization is the fallback.
Either route must produce q_warp, sigma_warp, and epsilon_cross inputs
without reading endpoint residuals.
