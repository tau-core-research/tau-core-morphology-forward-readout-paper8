# Paper 8 reproduction changeset inventory

Status: COMMIT_SCOPE_AUDIT_ONLY

This report inventories the current dirty working tree after a successful Paper 8 reproduction run. It is not a scientific result and does not change endpoint status.

## Layer summary

| layer | files | size bytes |
|---|---:|---:|
| bridge_docs | 1 | 89164 |
| derived_data | 413 | 5399476 |
| external_source_cache | 58 | 66744610 |
| figure_sources | 3 | 105117 |
| paper_source_pdf_figures | 15 | 2064860 |
| reports | 154 | 2487220 |
| scripts | 145 | 1530045 |
| tests | 1 | 332292 |
| top_level_package | 2 | 1152665 |

## Status by layer

| git status | layer | files |
|---|---|---:|
| M | bridge_docs | 1 |
| ?? | derived_data | 412 |
| M | derived_data | 1 |
| ?? | external_source_cache | 58 |
| M | figure_sources | 3 |
| ?? | paper_source_pdf_figures | 9 |
| M | paper_source_pdf_figures | 6 |
| ?? | reports | 141 |
| M | reports | 13 |
| ?? | scripts | 139 |
| M | scripts | 6 |
| M | tests | 1 |
| M | top_level_package | 2 |

## Suggested commit grouping

1. Paper and bridge text: README.md, paper8_submission_source, docs, refs, arXiv package.
2. Reproducible code and tests: scripts and tests.
3. Reproducible derived artifacts: data/derived, reports, figures.
4. Source cache/provenance artifacts: data/external and cached preview/source images.

Recommended default if preserving a complete reproduction package: commit all four groups together only after reviewing external cache size and provenance needs.
