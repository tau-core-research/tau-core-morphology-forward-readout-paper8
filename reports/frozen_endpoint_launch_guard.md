# Frozen Endpoint Launch Guard

This guard decides whether the frozen Paper 8 endpoint protocol may be
launched. It does not compute endpoint scores and it is not an empirical
validation result.

This launch guard is not an endpoint score.

## Verdict

Launch status: `LAUNCH_BLOCKED`.
Readiness decision: `BLOCKED_ACCEPTED_OBSERVABLES_MISSING`.

The current package must not run the discovery-style endpoint on the proxy
manifest or on the empty accepted template. This preserves the blind
protocol boundary.

## Launch Guard

| launch_status | readiness_decision | primary_endpoint_lane | amplitude_policy | blocked_gate_count | guard_reason | endpoint_scores_computed | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LAUNCH_BLOCKED | BLOCKED_ACCEPTED_OBSERVABLES_MISSING | no_low_inclination | train_selected_family_to_global_shrinkage_0_40 | 4 | accepted residual-blind observables missing | False | populate accepted manifest and rerun readiness gate |

## Blockers

| gate | blocked_missing_rows | field_group | next_action |
| --- | --- | --- | --- |
| residual_blind_family_labels_ready | 175 | formula_family | populate accepted residual-blind fields before endpoint scoring |
| quality_and_caveat_ready | 350 | manifest_confidence; manifest_caveat | populate accepted residual-blind fields before endpoint scoring |
| active_kernel_observables_ready | 369 | scale_radius_kpc; tail_inner_radius_kpc; tail_cutoff_radius_kpc; compact_support_radius_kpc; thickness_h_over_rs | populate accepted residual-blind fields before endpoint scoring |
| provenance_ready | 175 | observable_provenance | populate accepted residual-blind fields before endpoint scoring |

## Claim Boundary

A blocked launch is a protocol safeguard, not a negative empirical result.
An authorized launch would only permit the frozen endpoint calculation; it
would not by itself prove Tau Core or guarantee superiority over MOND, RAR,
TGP, or Newtonian baselines.
