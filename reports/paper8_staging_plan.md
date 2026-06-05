# Paper 8 staging plan

Status: STAGING_PLAN_ONLY_NOT_STAGED

This plan translates the reproduction changeset inventory into a conservative staging recommendation. No files are staged by this report.

| group | action | files |
|---|---|---:|
| hold_external_cache_policy_review | do_not_stage_by_default | 58 |
| stage_code_tests | stage | 146 |
| stage_commit_scope_audits | stage | 6 |
| stage_derived_repro_artifacts | stage | 567 |
| stage_paper_docs_package | stage | 21 |

Default recommendation:

- Stage code, tests, paper/docs/package files, derived CSVs, reports, figures, and the two inventory reports.
- Do not stage `data/external/literature/*` by default; keep it local or move it under an explicit source-cache/provenance policy.
- If full offline reproducibility is required, stage only source-cache files with explicit licensing/provenance approval.

This preserves the paper result and reproducibility ledgers while avoiding accidental inclusion of large source PDFs/images.
