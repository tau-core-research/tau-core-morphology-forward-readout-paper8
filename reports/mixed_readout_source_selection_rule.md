# Mixed Readout Source-Selection Rule

This report predeclares a residual-blind source rule for selecting a
mixed smooth-carrier plus source-windowed overlay readout candidate.
It does not authorize endpoint scoring. Passing cases move only to a
formula-freeze gate.

## Protocol

| rule_id | rule_kind | definition | allowed_inputs | forbidden_inputs | endpoint_effect | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| MXR1_SMOOTH_CARRIER | required_source_gate | A smooth disk carrier is allowed only when source-side disk/decomposition evidence gives a disk-like component and a numeric disk scale before endpoint scoring. | S4G/SPARC/decomposition disk component fields; source-native disk scale | vobs residuals; RMSE ranks; best Tau family; required S_tau diagnostics | does not score; only allows mixed formula-freeze worklist entry | mixed_readout_source_selection_rule_not_endpoint |
| MXR2_OVERLAY_MODIFIER | required_source_gate | A source-windowed overlay modifier is allowed only with residual-blind warp/projection/vertical/lag source evidence and at least one numeric activation or amplitude field. | warp onset; projection/warp window; h/R; extended-component fraction; lag-map context | endpoint residual sign; post-hoc radial error pattern | does not score; only supplies the formula-freeze target | mixed_readout_source_selection_rule_not_endpoint |
| MXR3_COMPACT_ONLY_VETO | required_source_gate | A mixed smooth+overlay label can replace a compact-only proxy only if compact-only support is absent, rejected, or source-caveated before scoring. | bulge/decomposition review; compact support radius review | compact family RMSE weakness | prevents using mixed label as a residual-rescue path | mixed_readout_source_selection_rule_not_endpoint |
| MXR4_SCORE_EXCLUSION | claim_boundary_gate | Diagnostic mixed scores may be recorded only as motivation for a future source-blind rule; they cannot promote the label. | source ledgers and frozen source fields | mixed diagnostic RMSE as label evidence | keeps all promoted cases formula-freeze-blocked until a separate freeze gate passes | mixed_readout_source_selection_rule_not_endpoint |

## Evaluated Cases

| galaxy | candidate_mixed_readout | carrier_rule | overlay_rule | smooth_component_source | disk_scale_kpc | compact_lane_decision | warp_onset_kpc | h_over_r | extended_component_fraction | lag_context | smooth_carrier_gate | overlay_modifier_gate | anti_compact_gate | forbidden_inputs_excluded_gate | source_rule_pass | formula_freeze_required | endpoint_scores_allowed | diagnostic_scores_allowed | case_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | K_expdisk_warp_vertical_overlay | smooth_disk_carrier_from_source_component_and_disk_scale | source_windowed_warp_vertical_lag_overlay | Z:edgedisk;N:psf | 3.53 | COMPACT_ENDPOINT_NOT_SOURCE_SUPPORTED | 10 | 0.232932 | 0.2 | accepted_context | True | True | True | True | True | True | False | True | MIXED_SOURCE_RULE_PASS_FORMULA_FREEZE_REQUIRED | mixed_readout_source_selection_rule_not_endpoint |

## Summary

| rule_status | n_cases_evaluated | n_source_rule_pass | n_endpoint_scores_allowed | endpoint_scores_allowed | formula_freeze_required_for_passing_cases | diagnostic_scores_used_as_label_input | next_required_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MIXED_SOURCE_RULE_PREDECLARED_NOT_ENDPOINT | 1 | 1 | 0 | False | True | False | mixed_readout_formula_freeze_gate | mixed_readout_source_selection_rule_not_endpoint |

## Claim Boundary

A passing source-rule case means that the mixed readout is supported by
residual-blind source evidence beyond intuition. It is not an empirical
validation and not an endpoint result until a separate formula-freeze
gate passes and a separate scoring script reads the frozen manifest.
