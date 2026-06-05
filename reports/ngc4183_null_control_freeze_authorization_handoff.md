# NGC4183 Null-Control Freeze Authorization Handoff

Date: `2026-06-05`

Status: `FREEZE_AUTHORIZATION_RESPONSE_REQUIRED`

This handoff is the shortest remaining step between the already accepted
NGC4183 source-review state and the null-control freeze gate.

It does not reopen source transcription. It only asks for an explicit
freeze-authorization decision on top of the accepted source-review record.

## Input File

- [ngc4183_null_control_freeze_authorization_template.csv](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/derived/ngc4183_null_control_freeze_authorization_template.csv)

## What Must Stay Fixed

Do not change these accepted source-review decisions:

- `source_identity_decision = ACCEPT`
- `radius_series_decision = ACCEPT`
- `orientation_series_decision = ACCEPT`
- `velocity_columns_decision = ACCEPT`
- `upper_bound_conclusion_decision = ACCEPT`

Those decisions are already captured in:

- [ngc4183_tilted_ring_independent_review_response_template.csv](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/derived/ngc4183_tilted_ring_independent_review_response_template.csv)
- [ngc4183_tilted_ring_review_response_summary.csv](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/derived/ngc4183_tilted_ring_review_response_summary.csv)

## Only Missing Decision

The remaining question is:

- should the accepted independent source review also authorize null-control formula freeze?

Required output fields:

- `freeze_authorization_decision`
- `may_freeze_null_control_after_review`
- `freeze_authorization_verdict`
- optional `freeze_authorization_notes`

## Allowed Outcomes

Use one of these:

1. `AUTHORIZE_FREEZE`
   Set `may_freeze_null_control_after_review = True`.
   Use an explicit verdict such as `INDEPENDENT_SOURCE_REVIEW_ACCEPTED_FREEZE_AUTHORIZED`.

2. `DO_NOT_AUTHORIZE_FREEZE`
   Keep `may_freeze_null_control_after_review = False`.
   Use an explicit verdict such as `INDEPENDENT_SOURCE_REVIEW_ACCEPTED_FREEZE_NOT_AUTHORIZED`.

3. `NEEDS_MORE_REVIEW`
   Keep `may_freeze_null_control_after_review = False`.
   Use an explicit verdict explaining the missing condition.

## Forbidden Inputs

The freeze-authorization decision must remain residual-blind.

Do not use:

- Tau Core residuals
- endpoint fits
- model scores
- morphology-matched fitting outcomes

## If Freeze Is Authorized

Then the minimum mechanical follow-up is:

1. copy `may_freeze_null_control_after_review = True` and the verdict into [ngc4183_tilted_ring_independent_review_response_template.csv](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/data/derived/ngc4183_tilted_ring_independent_review_response_template.csv)
2. rerun:
   - `scripts/build_ngc4183_tilted_ring_review_response_intake.py`
   - `scripts/build_ngc4183_null_control_freeze_readiness_gate.py`
   - `scripts/build_ngc4183_null_control_formula_freeze_gate.py`
   - `scripts/build_ngc4183_accepted_null_control_gate.py`
   - `scripts/run_ngc4183_weak_projection_null_control_scoring_gate.py`

## If Freeze Is Not Authorized

Preserve the current state:

- `NGC4183_TILTED_RING_REVIEW_RESPONSE_ACCEPTED_INDEPENDENT_SOURCE_ONLY_FREEZE_BLOCKED`

That still leaves the source-review lane accepted while keeping endpoint use
blocked.
