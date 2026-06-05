# P0 DustPedia/HI/PHANGS Source Evidence

This report records the requested source acquisition pass for the four P0
galaxies. It queries DustPedia VizieR tables, the public PHANGS sample
table, and SPARC HI mass/radius fields. It does not classify morphology,
does not create accepted labels, and does not compute endpoint scores.

## Verdict

DustPedia direct matches are found for NGC0300 only in the queried tables.
PHANGS public sample coverage is not found for the four P0 galaxies,
including NGC0247. SPARC HI mass/radius evidence is present for all four
P0 galaxies, but HI morphology/asymmetry still requires review rather
than automatic label promotion.

## Combined Summary

| galaxy | dustpedia_status | phangs_status | hi_status | source_review_status | accepted_label_output_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0100 | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_SAMPLE_COVERAGE | HI_SOURCE_EVIDENCE_READY | SOURCE_EVIDENCE_PARTIAL_REVIEW_REQUIRED | False | False | p0_external_source_evidence_not_label_not_endpoint |
| NGC0247 | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_SAMPLE_COVERAGE | HI_SOURCE_EVIDENCE_READY | SOURCE_EVIDENCE_PARTIAL_REVIEW_REQUIRED | False | False | p0_external_source_evidence_not_label_not_endpoint |
| NGC0300 | MATCHED_SOURCE_EVIDENCE | NO_PHANGS_SAMPLE_COVERAGE | HI_SOURCE_EVIDENCE_READY | SOURCE_EVIDENCE_PARTIAL_REVIEW_REQUIRED | False | False | p0_external_source_evidence_not_label_not_endpoint |
| NGC6503 | NO_DIRECT_DUSTPEDIA_MATCH | NO_PHANGS_SAMPLE_COVERAGE | HI_SOURCE_EVIDENCE_READY | SOURCE_EVIDENCE_PARTIAL_REVIEW_REQUIRED | False | False | p0_external_source_evidence_not_label_not_endpoint |

## DustPedia Match Counts

| galaxy | match_status | n_tables |
| --- | --- | --- |
| NGC0100 | NO_DIRECT_MATCH | 9 |
| NGC0247 | NO_DIRECT_MATCH | 9 |
| NGC0300 | MATCHED_SOURCE_EVIDENCE | 7 |
| NGC0300 | NO_DIRECT_MATCH | 2 |
| NGC6503 | NO_DIRECT_MATCH | 9 |

## PHANGS

| galaxy | match_status | evidence_summary |
| --- | --- | --- |
| NGC0100 | NO_PHANGS_SAMPLE_COVERAGE | NGC0100 is not present in the public PHANGS sample table; downloaded fresh public PHANGS sample table |
| NGC0247 | NO_PHANGS_SAMPLE_COVERAGE | NGC0247 is not present in the public PHANGS sample table; downloaded fresh public PHANGS sample table |
| NGC0300 | NO_PHANGS_SAMPLE_COVERAGE | NGC0300 is not present in the public PHANGS sample table; downloaded fresh public PHANGS sample table |
| NGC6503 | NO_PHANGS_SAMPLE_COVERAGE | NGC6503 is not present in the public PHANGS sample table; downloaded fresh public PHANGS sample table |

## HI Evidence

| galaxy | match_status | mhi_1e9_msun | rhi_kpc | sparc_ref | dustpedia_hi_status |
| --- | --- | --- | --- | --- | --- |
| NGC0100 | HI_SOURCE_EVIDENCE_READY | 1.99 | 16.36 | dB02,Rh96 | NO_DIRECT_DUSTPEDIA_HI_MATCH |
| NGC0247 | HI_SOURCE_EVIDENCE_READY | 1.746 | 12.79 | Sa96,Ca90 | NO_DIRECT_DUSTPEDIA_HI_MATCH |
| NGC0300 | HI_SOURCE_EVIDENCE_READY | 0.936 | 9.2 | Sa96,CP90 | DUSTPEDIA_HI_MATCHED |
| NGC6503 | HI_SOURCE_EVIDENCE_READY | 1.744 | 14.05 | Be91,Be87 | NO_DIRECT_DUSTPEDIA_HI_MATCH |

## Claim Boundary

These source records may feed a source-assisted review draft. They are not
an accepted morphology manifest and not endpoint evidence.

Claim boundary: `p0_external_source_evidence_not_label_not_endpoint`.
