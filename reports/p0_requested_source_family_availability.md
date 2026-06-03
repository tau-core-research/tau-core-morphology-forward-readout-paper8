# P0 Requested Source-Family Availability Audit

This audit tests the P0 source-acquisition plan against currently available
source paths. It is an availability preflight only: it does not classify
galaxies, does not create accepted morphology labels, and does not compute
endpoint scores.

## Verdict

P0 source-family rows: 20.
Rows still requiring residual-blind external acquisition: 0.

S4G is partially source-ready for the P0 galaxies through existing
crossmatches and disk-scale candidates. NED/NED-D lookup paths are ready.
DustPedia is directly matched only for NGC0300 in the acquired tables.
HI mass/radius evidence is ready for all four P0 galaxies through SPARC,
while HI morphology/asymmetry review remains pending. PHANGS public sample
coverage is not found for the four P0 galaxies, including NGC0247.

## Source Summary

| source_family | n_p0_galaxies | n_source_family_rows | n_partial_source_ready | n_lookup_ready | n_to_be_queried | n_no_coverage | n_review_pending | endpoint_scores_computed | accepted_label_output_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DustPedia | 4 | 4 | 0 | 0 | 0 | 3 | 1 | False | False | p0_requested_source_availability_not_label_not_endpoint |
| HI_SURVEYS | 4 | 4 | 0 | 0 | 0 | 0 | 4 | False | False | p0_requested_source_availability_not_label_not_endpoint |
| NED_NEDD | 4 | 4 | 0 | 4 | 0 | 0 | 0 | False | False | p0_requested_source_availability_not_label_not_endpoint |
| PHANGS | 4 | 4 | 0 | 0 | 0 | 4 | 0 | False | False | p0_requested_source_availability_not_label_not_endpoint |
| S4G | 4 | 4 | 4 | 0 | 0 | 0 | 0 | False | False | p0_requested_source_availability_not_label_not_endpoint |

## Availability Rows

| galaxy | source_family | n_required_plan_tasks | availability_status | availability_evidence |
| --- | --- | --- | --- | --- |
| NGC0100 | S4G | 7 | PARTIAL_SOURCE_READY | S4G crossmatch and Pipeline 4 disk-scale candidate already acquired; label/audit still pending |
| NGC0100 | NED_NEDD | 6 | LOOKUP_READY | NED lookup URL is present for identity/provenance review |
| NGC0100 | DustPedia | 7 | NO_DIRECT_DUSTPEDIA_MATCH | DustPedia was queried; no direct normalized-name match was found in the acquired tables |
| NGC0100 | HI_SURVEYS | 6 | HI_SOURCE_EVIDENCE_READY_REVIEW_PENDING | SPARC HI mass/radius evidence is available; HI morphology/asymmetry review remains pending |
| NGC0100 | PHANGS | 3 | NO_PHANGS_SAMPLE_COVERAGE | PHANGS public sample was queried; this galaxy is not covered |
| NGC0247 | S4G | 7 | PARTIAL_SOURCE_READY | S4G crossmatch and Pipeline 4 disk-scale candidate already acquired; label/audit still pending |
| NGC0247 | NED_NEDD | 5 | LOOKUP_READY | NED lookup URL is present for identity/provenance review |
| NGC0247 | DustPedia | 6 | NO_DIRECT_DUSTPEDIA_MATCH | DustPedia was queried; no direct normalized-name match was found in the acquired tables |
| NGC0247 | HI_SURVEYS | 5 | HI_SOURCE_EVIDENCE_READY_REVIEW_PENDING | SPARC HI mass/radius evidence is available; HI morphology/asymmetry review remains pending |
| NGC0247 | PHANGS | 5 | NO_PHANGS_COVERAGE_FOR_REQUIRED_OPTIONAL_BRANCH | PHANGS public sample was queried; NGC0247 is not covered, so this optional branch remains unsupported |
| NGC0300 | S4G | 5 | PARTIAL_SOURCE_READY | S4G crossmatch and Pipeline 4 disk-scale candidate already acquired; label/audit still pending |
| NGC0300 | NED_NEDD | 5 | LOOKUP_READY | NED lookup URL is present for identity/provenance review |
| NGC0300 | DustPedia | 5 | MATCHED_SOURCE_EVIDENCE_REVIEW_PENDING | DustPedia direct source evidence is acquired, but morphology review is still pending |
| NGC0300 | HI_SURVEYS | 5 | HI_SOURCE_EVIDENCE_READY_REVIEW_PENDING | SPARC HI mass/radius evidence is available; HI morphology/asymmetry review remains pending |
| NGC0300 | PHANGS | 3 | NO_PHANGS_SAMPLE_COVERAGE | PHANGS public sample was queried; this galaxy is not covered |
| NGC6503 | S4G | 5 | PARTIAL_SOURCE_READY | S4G crossmatch and Pipeline 4 disk-scale candidate already acquired; label/audit still pending |
| NGC6503 | NED_NEDD | 5 | LOOKUP_READY | NED lookup URL is present for identity/provenance review |
| NGC6503 | DustPedia | 5 | NO_DIRECT_DUSTPEDIA_MATCH | DustPedia was queried; no direct normalized-name match was found in the acquired tables |
| NGC6503 | HI_SURVEYS | 5 | HI_SOURCE_EVIDENCE_READY_REVIEW_PENDING | SPARC HI mass/radius evidence is available; HI morphology/asymmetry review remains pending |
| NGC6503 | PHANGS | 3 | NO_PHANGS_SAMPLE_COVERAGE | PHANGS public sample was queried; this galaxy is not covered |

## Claim Boundary

This is not an accepted morphology manifest and not an endpoint score. It
only tells the review pipeline where source evidence is already partly
available and where residual-blind acquisition is still needed.

Claim boundary: `p0_requested_source_availability_not_label_not_endpoint`.
