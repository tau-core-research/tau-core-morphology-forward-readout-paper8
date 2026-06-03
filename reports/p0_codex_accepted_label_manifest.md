# P0 Codex Source-Reviewed Label Manifest

This manifest records the four P0 labels that passed the Codex/source
review response and response-to-manifest gate. It is a P0 audit manifest
only. It does not create full endpoint-manifest rows and does not compute
endpoint scores.

P0 audit manifest only.

## Summary

| p0_label_manifest_decision | n_galaxies | n_p0_codex_source_review_accepted | n_blocked | full_endpoint_manifest_rows_created | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| P0_CODEX_SOURCE_REVIEW_LABELS_CREATED_NOT_ENDPOINT | 4 | 4 | 0 | False | False | p0_codex_accepted_labels_not_endpoint |

## Manifest

| galaxy | accepted_label_status | accepted_formula_family | review_confidence | manifest_caveat |
| --- | --- | --- | --- | --- |
| NGC0100 | P0_CODEX_SOURCE_REVIEW_ACCEPTED_FOR_AUDIT | K_exponential_disk | 0.7 | edge_projection_caveat |
| NGC0247 | P0_CODEX_SOURCE_REVIEW_ACCEPTED_FOR_AUDIT | K_exponential_disk | 0.78 | bar_component_caveat |
| NGC0300 | P0_CODEX_SOURCE_REVIEW_ACCEPTED_FOR_AUDIT | K_exponential_disk | 0.88 | none |
| NGC6503 | P0_CODEX_SOURCE_REVIEW_ACCEPTED_FOR_AUDIT | K_exponential_disk | 0.74 | nuclear_component_caveat |

## Claim Boundary

These labels are residual-blind source-review labels for the P0 audit lane.
They are not empirical validation, not a MOND/RAR/TGP/Newtonian comparison,
and not a launch of the frozen 175-galaxy endpoint.

Claim boundary: `p0_codex_accepted_labels_not_endpoint`.
