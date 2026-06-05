# NGC4183 Independent Source Review Memo

Date: `2026-06-05`

Status: `SOURCE_REVIEW_ACCEPTED_FREEZE_NOT_AUTHORIZED`

This memo records the current human-readable state of the NGC4183 residual-blind
source review for the weak-projection/null-control preparation lane. It is a
source-review memo only. It does not authorize formula freeze, endpoint
scoring, or any claim about fit quality.

## Reviewer Statement

Reviewer: `external_source_reviewer_v1`

Reviewer independence statement:

> I performed this review without using Tau Core residuals, endpoint fits,
> model scores, or morphology-matched fitting outcomes.

## Review Scope

The review checked only whether the source-native tilted-ring/projection inputs
for NGC4183 were transcribed correctly from the local Verheijen and Sancisi
2001 source material.

Reviewed source files:

- [page-013.png](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_pages/ngc4183_review/page-013.png)
- [ngc4183_table4_full_column_crop.png](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_pages/ngc4183_review/ngc4183_table4_full_column_crop.png)
- [page_84-084.png](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/external/literature/2001_verheijen_sancisi_pages/page_84-084.png)
- [ngc4183_tilted_ring_orientation_profile.csv](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/derived/ngc4183_tilted_ring_orientation_profile.csv)

Forbidden inputs for this review:

- Tau Core residual curves
- endpoint fits
- model scores
- morphology-matched fitting outcomes

## Decisions

- `source_identity_decision: ACCEPT`
- `radius_series_decision: ACCEPT`
- `orientation_series_decision: ACCEPT`
- `velocity_columns_decision: ACCEPT`
- `upper_bound_conclusion_decision: ACCEPT`

## Accepted Source Facts

- Table identity: the cited Table 4 block corresponds to `N4183` / `NGC4183`
- Radius series: `10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 141, 151, 161, 172, 183, 194, 205, 217, 229, 241` arcsec
- Number of extracted rows: `23`
- Inclination series: `i = 82 deg` throughout the extracted Table 4 rings
- Position angle series: `PA = 346..349 deg`
- Maximum absolute PA drift: `3.0 deg`
- Maximum absolute inclination drift: `0.0 deg`
- Outer `229` and `241` arcsec rows preserve missing approaching-side velocity entries rather than filling them

## Weak-Projection Interpretation

The reviewer accepted the source-side weak-projection/null-control conclusion as
consistent with the accepted orientation series:

- `gamma_projection_upper_bound = 0.00269837`
- `max_velocity_fractional_change = 0.00135010`

This acceptance is limited to source-side consistency. It means the current
orientation drift is small enough to support the existing weak-projection
preparation interpretation. It does not by itself authorize a formula freeze.

## Current Boundary

Current intake state:

- [ngc4183_tilted_ring_review_response_summary.csv](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/derived/ngc4183_tilted_ring_review_response_summary.csv): `NGC4183_TILTED_RING_REVIEW_RESPONSE_ACCEPTED_INDEPENDENT_SOURCE_ONLY_FREEZE_BLOCKED`
- [ngc4183_control_status_dashboard_summary.csv](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/derived/ngc4183_control_status_dashboard_summary.csv): first blocker remains `review_response_intake`

Interpretation:

- the source review is accepted
- the reviewer is treated as independent at intake level
- null-control formula freeze is still not authorized
- endpoint scoring remains blocked

## Overall Decision

`overall_decision: ACCEPT`

No source-transcription correction was identified, and no source-level issue was
found that would weaken the current NGC4183 weak-projection/null-control
preparation status.
