# S4G75 Closure-Source Generalization Gate

This gate prevents the NGC2683 closure-source prototype from being generalized automatically. It records which thick/flared rows are ready for profile-aware closure-source development and which still need data.

## Verdict

| generalization_status | n_galaxies | galaxies | median_inclination | claim_boundary |
| --- | --- | --- | --- | --- |
| EDGE_ON_VERTICAL_PROFILE_SEARCH_REQUIRED | 1 | NGC3972 | 77 | s4g75_closure_source_generalization_gate_not_endpoint |
| HIGH_INCLINATION_WARP_FLARE_SEARCH_REQUIRED | 1 | NGC4088 | 69 | s4g75_closure_source_generalization_gate_not_endpoint |
| INSUFFICIENT_VERTICAL_PROFILE_SUPPORT | 4 | NGC0024;NGC3726;NGC3949;NGC4389 | 54 | s4g75_closure_source_generalization_gate_not_endpoint |
| PROFILE_CLOSURE_SOURCE_READY_PROTOTYPE_ONLY | 1 | NGC2683 | 80 | s4g75_closure_source_generalization_gate_not_endpoint |

Only NGC2683 is currently profile-source ready, and even there the status is prototype-only. No S4G75 row is authorized for closure-source endpoint scoring by this gate.

## Galaxy-Level Gate

| galaxy | inclination_deg | literature_status | vertical_source_checks | vertical_search_statuses | generalization_status | generalization_reason | next_action | closure_source_endpoint_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0024 | 64 | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS | 0 |  | INSUFFICIENT_VERTICAL_PROFILE_SUPPORT | current source support does not provide a direct vertical or flare profile | keep as proxy/theorem-development row; do not use closure-source endpoint kernel | False |
| NGC2683 | 80 | DIRECT_LITERATURE_FLARE_PROFILE_READY_MAPPING_REQUIRED | 1 | DIRECT_PROFILE_SOURCE_ALREADY_REGISTERED | PROFILE_CLOSURE_SOURCE_READY_PROTOTYPE_ONLY | direct flare profile exists; closure-source prototype improves NGC2683 stress diagnostic | develop and predeclare a population-level H(R)/warp closure-source kernel before endpoint use | False |
| NGC3726 | 53 | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS | 0 |  | INSUFFICIENT_VERTICAL_PROFILE_SUPPORT | current source support does not provide a direct vertical or flare profile | keep as proxy/theorem-development row; do not use closure-source endpoint kernel | False |
| NGC3949 | 55 | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS | 0 |  | INSUFFICIENT_VERTICAL_PROFILE_SUPPORT | current source support does not provide a direct vertical or flare profile | keep as proxy/theorem-development row; do not use closure-source endpoint kernel | False |
| NGC4088 | 69 | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS | 4 | WHISP_WARP_ASYMMETRY_SOURCE_READY_PROFILE_NOT_EXTRACTED;HI_KINEMATIC_ASYMMETRY_SOURCE_READY_NOT_VERTICAL_KERNEL;HALOGAS_TEXT_SEARCH_NEGATIVE_FOR_OBJECT;GENERAL_HI_SCALE_HEIGHT_CONTEXT_ONLY | HIGH_INCLINATION_WARP_FLARE_SEARCH_REQUIRED | inclination is high enough for flare/warp evidence to matter, but direct source profile is missing | search resolved HI/kinematic/warp literature before closure-source promotion | False |
| NGC3972 | 77 | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS | 4 | HI_MORPHOLOGY_SOURCE_READY_VERTICAL_KERNEL_NOT_EXTRACTED;OBJECT_CONTEXT_ONLY_NOT_VERTICAL_KERNEL;WHISP_URSA_MAJOR_OBSERVING_PARAMETERS_ONLY;HALOGAS_TEXT_SEARCH_NEGATIVE_FOR_OBJECT | EDGE_ON_VERTICAL_PROFILE_SEARCH_REQUIRED | high inclination makes a vertical/warp source search plausible, but no direct profile is recorded | perform residual-blind literature/data extraction for vertical scale, flare, warp, or gas-plane thickness | False |
| NGC4389 | 50 | NO_TARGETED_LITERATURE_HIT_RECORDED_THIS_PASS | 0 |  | INSUFFICIENT_VERTICAL_PROFILE_SUPPORT | current source support does not provide a direct vertical or flare profile | keep as proxy/theorem-development row; do not use closure-source endpoint kernel | False |

## Claim Boundary

The NGC2683 sensitivity result is a formula-development signal. A population-level closure-source endpoint requires predeclared source criteria, direct profile extraction for additional galaxies, and a fixed kernel rule before endpoint scoring.
