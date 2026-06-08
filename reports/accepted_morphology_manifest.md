# Accepted Morphology Manifest Draft

This report builds the first partial accepted morphology-observable manifest
from acquired external SPARC/S4G sources. It accepts only field-level
source-native observables where the provenance is residual-blind and
documented. It does not promote proxy morphology-family labels into
accepted endpoint labels.

## Verdict

Rows in manifest: 175.
Accepted S4G/SPARC scale-radius observables: 76.
Endpoint-ready rows: 0.

The manifest is a real data-acquisition upgrade, but it remains endpoint
blocked. The largest remaining blockers are external family-label audit and
family-specific source-native kernel observables for scale-tail, compact,
and thick/flared branches.

## Gate Status

| gate | gate_status | n_rows | n_pass | n_blocked | decision_rule |
| --- | --- | --- | --- | --- | --- |
| row_identity_ready | PASS | 175 | 175 | 0 | all rows preserve SPARC galaxy identity |
| scale_radius_source_observables | PARTIAL_PASS | 175 | 76 | 99 | S4G disk scale converted with SPARC distance |
| external_family_label_audit | BLOCKED | 175 | 0 | 175 | proxy family labels must be externally audited before endpoint use |
| family_kernel_completeness | BLOCKED | 175 | 14 | 161 | all family-specific kernel fields must be source-native |
| endpoint_eligibility | BLOCKED | 175 | 0 | 175 | field-level accepted observables do not by themselves authorize scoring |

## Family Summary

| formula_family | n_rows | n_scale_radius_accepted | n_family_label_review | n_kernel_complete | n_endpoint_ready |
| --- | --- | --- | --- | --- | --- |
| K_compact_finite | 29 | 7 | 29 | 0 | 0 |
| K_exponential_disk | 32 | 14 | 32 | 14 | 0 |
| K_scale_tail_spiral | 80 | 30 | 80 | 0 | 0 |
| K_thick_flared | 34 | 25 | 34 | 0 | 0 |

## Claim Boundary

This accepted morphology manifest draft is not an endpoint score.
This manifest is partial. It can be used to audit source coverage and to
prepare the frozen endpoint, but it must not be used as evidence that Tau
Core fits better than MOND, RAR, TGP, or Newtonian baselines. Endpoint
scores remain blocked until the accepted family labels and required
source-native observables pass the readiness gate.
