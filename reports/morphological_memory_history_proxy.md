# Morphological Memory / History Proxy Diagnostic

This diagnostic records a conservative proxy layer for the possibility that
the currently observed morphology is not the full readout-relevant
morphological state. A galaxy may have had a different earlier structure,
or the Tau Core readout may encode an integrated morphology/history
component rather than only the present catalog shape.

The layer combines source-side morphology/context flags with the
rotation-inferred readout-family diagnostic. Because the rotation-inferred
component is not residual-blind, this is a hypothesis generator only.

## Verdict

Current proxy family and rotation-inferred family disagree in 113/175 rows.
Within the 13 externally supported exponential-disk rows, 9/13 do not infer the exponential-disk readout family.
Of those external exponential-disk rows, 6 are scale-tail readout-memory candidates and 3 are vertical/projection readout-memory candidates.

This is not evidence that the historical morphology is known. It is a
reproducible triage layer for deciding where a future residual-blind
history/memory observable should be collected.

## Proxy Classes

| memory_history_proxy_class | n_galaxies | n_rotation_current_mismatches | n_external_rows | n_external_mismatches | median_rotation_margin |
| --- | --- | --- | --- | --- | --- |
| current_readout_consistent_no_memory_proxy_flag | 62 | 0 | 4 | 0 | 3.092565157114432 |
| scale_tail_current_with_expdisk_readout_memory_candidate | 32 | 32 | 0 | 0 | 1.301843198115415 |
| thick_flared_proxy_with_alternate_readout_memory_candidate | 30 | 30 | 0 | 0 | 1.3159196263303041 |
| generic_current_vs_rotation_readout_mismatch_candidate | 17 | 17 | 0 | 0 | 0.5023480727386387 |
| compact_proxy_with_alternate_readout_memory_candidate | 15 | 15 | 0 | 0 | 0.4154349036827405 |
| expdisk_proxy_with_scale_tail_readout_memory_candidate | 10 | 10 | 0 | 0 | 3.3383918796467746 |
| expdisk_current_with_scale_tail_readout_memory_candidate | 6 | 6 | 6 | 6 | 1.4156829038883325 |
| expdisk_current_with_vertical_projection_memory_candidate | 3 | 3 | 3 | 3 | 0.2532895720555812 |

## External Exponential-Disk Subset

| external_family_label | memory_history_proxy_class | rotation_inferred_family | n_galaxies | n_matches_external | median_margin |
| --- | --- | --- | --- | --- | --- |
| K_exponential_disk | current_readout_consistent_no_memory_proxy_flag | K_exponential_disk | 4 | 4 | 1.3478018493848438 |
| K_exponential_disk | expdisk_current_with_scale_tail_readout_memory_candidate | K_scale_tail_spiral | 6 | 0 | 1.4156829038883325 |
| K_exponential_disk | expdisk_current_with_vertical_projection_memory_candidate | K_thick_flared | 3 | 0 | 0.2532895720555812 |

## Claim Boundary

This proxy is not an accepted morphology label and not an endpoint score.
The morphological memory / history proxy is not an accepted morphology
label, not an endpoint score, not empirical validation, and not proof that
Tau Core has recovered galaxy history. It is a pre-endpoint hypothesis
layer that marks possible current-shape/readout-history mismatches for
future residual-blind testing.

Claim boundary: `morphological_memory_proxy_not_accepted_label_not_endpoint_validation`.
