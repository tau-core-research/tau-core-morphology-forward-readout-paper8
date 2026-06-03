# Readout-State Vector Intake Schema and Gap Audit

This report records the source-observable gate required before the
readout-mixture idea can be promoted from a proxy diagnostic to an
accepted Tau-side readout-state vector. It computes no endpoint score.

Total accepted component inputs currently ready: 0.

## Intake Schema

| readout_component | weight_channel | required_observable | accepted_source_path | failure_mode |
| --- | --- | --- | --- | --- |
| K_exponential_disk | w_K_exponential_disk | accepted disk scale/decomposition and clean disk label | S4G/SPARC scale radius plus external family-label audit | disk weight remains present-day 4D proxy rather than readout-state weight |
| K_scale_tail_spiral | w_K_scale_tail_spiral | accepted outer-disk/HI extent, tail, LSB, or asymmetry support | HI surveys;deep optical/IR outer-disk review;DustPedia fallback | tail weight remains gas/LSB heuristic |
| K_compact_finite | w_K_compact_finite | accepted compact core, bulge, nuclear component, or finite support | S4G decomposition;NED/SIMBAD notes;high-resolution imaging review | compact weight remains bulge-fraction proxy |
| K_thick_flared | w_K_thick_flared | accepted vertical thickness, flare, warp, or projection-sensitive support | edge-on morphology review;HI warp/flare evidence;PHANGS/S4G support | vertical weight remains inclination/thickness proxy |
| normalization | amplitude_normalization | source-native family-to-global or component normalization rule | Tau-side source-normalization derivation plus residual-blind scale observables | mixture may carry correct components but wrong amplitude scale |
| memory_history | history_memory_correction | accepted morphology-memory/history or current-shape/readout mismatch evidence | residual-blind visual/decomposition/HI history review | K_obs may be incorrectly promoted to K_readout |

## Gap Summary

| readout_component | component_status | n_rows | n_galaxies | endpoint_ready_components |
| --- | --- | --- | --- | --- |
| K_compact_finite | MISSING_ACCEPTED_COMPONENT_INPUT | 143 | 143 | 0 |
| K_compact_finite | PROXY_MEMORY_SIGNAL_NEEDS_ACCEPTED_SOURCE | 32 | 32 | 0 |
| K_exponential_disk | MISSING_ACCEPTED_COMPONENT_INPUT | 175 | 175 | 0 |
| K_scale_tail_spiral | MISSING_ACCEPTED_COMPONENT_INPUT | 84 | 84 | 0 |
| K_scale_tail_spiral | PROXY_MEMORY_SIGNAL_NEEDS_ACCEPTED_SOURCE | 91 | 91 | 0 |
| K_thick_flared | MISSING_ACCEPTED_COMPONENT_INPUT | 51 | 51 | 0 |
| K_thick_flared | PROXY_MEMORY_SIGNAL_NEEDS_ACCEPTED_SOURCE | 124 | 124 | 0 |
| memory_history | NO_MEMORY_PROXY_FLAG | 62 | 62 | 0 |
| memory_history | PROXY_MEMORY_SIGNAL_NEEDS_ACCEPTED_SOURCE | 113 | 113 | 0 |
| normalization | MISSING_TAU_SIDE_NORMALIZATION_RULE | 175 | 175 | 0 |

## Verdict

The current mixture weights remain proxy weights. The next run needs
accepted residual-blind source observables for component weights,
morphology-memory/history correction, and source normalization before
the mixture can be scored as a frozen endpoint.

Claim boundary: `readout_state_vector_intake_not_endpoint_not_accepted_state`.
