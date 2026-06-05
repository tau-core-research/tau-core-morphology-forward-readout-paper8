# Remaining Caveat Closure Roadmap

This roadmap ranks the remaining caveats after the four-case caveat
reduction audit. It is not an endpoint score and does not change any
endpoint status.

## Summary

| roadmap_status | n_cases | n_replay_ready_without_new_source | n_replay_completed_without_v1_update | n_predeclared_replay_gates_built_without_endpoint | n_remaining_caveat_action_gates_built_without_endpoint | n_retrospective_or_population_blocked | n_source_or_law_blocked | endpoint_statuses_changed | endpoint_scores_recomputed | endpoint_scores_allowed | uses_vobs_or_residual | uses_replay_endpoint_summary | uses_predeclared_replay_gate_summary | uses_remaining_caveat_action_summary | v1_endpoint_updated | next_recommended_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REMAINING_CAVEAT_CLOSURE_ROADMAP_UPDATED_AFTER_NGC4088_ACTION_GATE_NOT_ENDPOINT | 4 | 0 | 1 | 1 | 1 | 3 | 0 | False | False | False | False | True | True | True | False | B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION_FOR_NGC4088 | remaining_caveat_closure_roadmap_not_endpoint |

## Roadmap

| galaxy | remaining_caveat_class | current_status | next_gate | closure_route | can_close_without_new_endpoint_data | endpoint_scores_allowed_now | priority | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | B2_B3_LAW_LEVEL_OPEN_B1_PROVENANCE_UPGRADE_OPTIONAL | NGC4088_REMAINING_CAVEAT_ACTION_GATE_BUILT_NOT_ENDPOINT | B2_SOURCE_LOAD_ORIGIN_AND_ASYMPTOTIC_CARRIER_DERIVATION | endpoint is already caveated-control scored; B1 is formula-freeze closed with WHISP graphical provenance caveat; direct H I is a provenance upgrade, while the primary open theory gate is B2 source-load-origin/asymptotic-carrier derivation | False | False | P1_SOURCE_AND_THEORY | remaining_caveat_closure_roadmap_not_endpoint |
| NGC4013 | PREDECLARED_REPLAY_GATE_BUILT_FUTURE_DATA_REQUIRED | NGC4013_PREDECLARED_REPLAY_HOLDOUT_GATE_BUILT_ENDPOINT_STILL_BLOCKED | FUTURE_UNINSPECTED_HOLDOUT_OR_SOURCE_SELECTED_ANALOGUE | the frozen expdisk+WVO protocol is transferable, but the same-curve replay is blocked; reduce further only with future uninspected holdout data or an exact source-selected analogue | False | False | P2_POPULATION_SCALE | remaining_caveat_closure_roadmap_not_endpoint |
| NGC5907 | SMALL_N_CONTROL_CONTEXT | ACCEPTED_MIXED_ENDPOINT_FREEZE_READY | POPULATION_REPLAY_OR_MORE_FRESH_ANALOGUES | do not change the accepted single-galaxy endpoint; reduce only by adding fresh source-selected population rows | False | False | P2_POPULATION_SCALE | remaining_caveat_closure_roadmap_not_endpoint |
| NGC7331 | BROAD_WINDOW_REPLAY_REDUCED_V1_NOT_UPDATED | NGC7331_V2_V3_REPLAY_HOLDOUT_PRELIMINARY_CONTROL_RESULT | POPULATION_REPLAY_OR_SOURCE_ANALOGUE_CONFIRMATION | V3 replay reduces the broad-window caveat for the replay path; keep the accepted V1 endpoint unchanged and reduce further only by population replay or fresh source-selected analogues | False | False | P2_POPULATION_SCALE | remaining_caveat_closure_roadmap_not_endpoint |

## Prior Audit Snapshot

| galaxy | caveat_reduction_status | caveat_reduced | remaining_caveat | endpoint_status_changed | endpoint_scores_recomputed | uses_vobs_or_residual_in_reduction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | RETROSPECTIVE_CAVEAT_ISOLATED_NOT_REMOVED | False | needs a predeclared replay/holdout lane or future source-selected analogue to reduce the retrospective caveat | False | False | False | remaining_caveat_closure_roadmap_not_endpoint |
| NGC5907 | PRIOR_PROJECTION_CAVEAT_REDUCED_TO_CONTROL_CONTEXT | True | small-N and single-galaxy control status remain | False | False | False | remaining_caveat_closure_roadmap_not_endpoint |
| NGC7331 | BROAD_WINDOW_CAVEAT_REDUCED_FOR_REPLAY_NOT_RETROACTIVE_ENDPOINT | True | accepted V1 row remains broad-window caveated; V2/V3 replay result is not retroactive endpoint update | False | False | False | remaining_caveat_closure_roadmap_not_endpoint |
| NGC4088 | B1_PROVENANCE_CAVEAT_REDUCED_LAW_LEVEL_CAVEATS_REMAIN | True | WHISP graphical-overview provenance caveat travels with the formula; B2 physical normalization and B3 scale uniqueness remain law-level caveats | False | False | False | remaining_caveat_closure_roadmap_not_endpoint |

## Interpretation

The NGC7331 replay path, NGC4013 predeclared replay gate, and NGC4088 remaining-caveat action gate have all been built. NGC4088 is already a caveated accepted single-galaxy control endpoint; its B1 graphical WHISP x_w is closed for formula freeze but remains a provenance caveat. The next scientific action is therefore B2 law-level work: derive the Tau-side source-load origin, final carrier law/population transfer, and cross-term bound. The frozen Vflat^2 carrier theorem narrows the asymptotic-carrier part, but does not close the final Tau-side law; B3 law-level uniqueness then follows as the dependent caveat. No endpoint status is changed by this roadmap.
