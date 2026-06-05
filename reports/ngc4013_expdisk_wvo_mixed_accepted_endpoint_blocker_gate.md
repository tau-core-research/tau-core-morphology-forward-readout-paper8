# NGC4013 Mixed Accepted-Endpoint Blocker Gate

This gate records why the strong NGC4013 exponential-disk + WVO mixed
curve cannot be promoted to an accepted single-galaxy endpoint in the
current package, despite being source-frozen and endpoint-blind at formula
construction level.

## Summary

| galaxy | formula_id | blocker_status | source_rule_ready | formula_frozen_for_future_scoring | endpoint_blind_construction | prior_diagnostic_dependency | retrospective_endpoint_scores_allowed | endpoint_scores_allowed | frozen_protocol_rmse_km_s | best_local_baseline_rmse_km_s | wrong_mixed_mean_rmse_km_s | wrong_mixed_best_rmse_km_s | matched_beats_all_wrong_mixed_families | n_gates | n_pass_like | n_blocked | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | MIXED_ACCEPTED_ENDPOINT_BLOCKED_RETROACTIVE_PROTOCOL_READY | True | True | True | True | False | False | 10.6148 | 10.8802 | 12.1321 | 11.367 | True | 5 | 3 | 2 | predeclare replay/holdout endpoint lane or use this formula only on future source-selected cases | ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_not_score |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | N4013_MAEB1_SOURCE_RULE_READY | PASS | K_expdisk_warp_vertical_overlay | none at source-rule level | False | ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_not_score |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | N4013_MAEB2_FORMULA_FROZEN_BEFORE_FUTURE_SCORING | PASS | MIXED_FORMULA_FREEZE_READY_NOT_RETROACTIVE_ENDPOINT | may be reused only prospectively or in a predeclared replay lane | False | ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_not_score |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | N4013_MAEB3_ENDPOINT_BLIND_CONSTRUCTION | PASS | frozen manifest construction uses source rule and WVO freeze manifest only | scoring must remain separate | False | ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_not_score |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | N4013_MAEB4_RETROACTIVE_ENDPOINT_BLOCKER | BLOCKED_RETROACTIVE_ENDPOINT | mixed expdisk+WVO lane was developed after NGC4013 wrong-family/control inspection | do not promote the existing NGC4013 mixed score to accepted endpoint evidence | False | ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_not_score |
| NGC4013 | NGC4013_EXPDISK_WVO_MIXED_FREEZE_V1 | N4013_MAEB5_REPLAY_OR_HOLDOUT_REQUIREMENT | BLOCKED_REPLAY_REQUIRED | accepted endpoint would require a predeclared replay protocol, new source-frozen galaxy, or holdout rule fixed before scoring | define prospective replay/holdout lane before any accepted NGC4013 mixed endpoint claim | False | ngc4013_expdisk_wvo_mixed_accepted_endpoint_blocker_not_score |

## Interpretation

The formula is useful and prospective-ready, but the existing NGC4013 score
is retrospective because the mixed branch was developed after inspecting the
NGC4013 wrong-family/control context. Therefore it remains a frozen-reference
row rather than an accepted endpoint row. Promotion requires a predeclared
replay/holdout lane or application to future source-selected cases.
