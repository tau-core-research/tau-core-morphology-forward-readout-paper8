# NGC4183 Weak-Projection Null-Control Scoring Gate

Status: `NGC4183_ACCEPTED_NULL_CONTROL_INTERVAL_ENDPOINT_COMPLETE`

This gate controls when the separate NGC4183 interval-control scoring branch
may read observed rotation velocities.

## Summary

| scoring_gate_status | galaxy | accepted_control_allowed | formula_freeze_allowed | construction_reads_vobs | scoring_reads_vobs | endpoint_scores_allowed | primary_blocker | control_roadmap_status | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_ACCEPTED_NULL_CONTROL_INTERVAL_ENDPOINT_COMPLETE | NGC4183 | True | True | False | True | True | none | NGC4183_CONTROL_PROMOTION_ROADMAP_SCORING_COMPLETE_PRELIMINARY_CONTROL | ngc4183_weak_projection_null_control_scoring_gate_not_endpoint | none |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N4183_SCORE_G1_ACCEPTED_CONTROL | PASS | NGC4183_ACCEPTED_NULL_CONTROL_READY_NOT_SCORED | none |
| N4183_SCORE_G2_FORMULA_FREEZE | PASS | NGC4183_NULL_CONTROL_FORMULA_FROZEN_NOT_ENDPOINT | none |
| N4183_SCORE_G3_NO_PREMATURE_VOBS | PASS | blocked branch does not read observed velocities | keep blocked branch vobs-free |

## Interpretation

The accepted null-control interval endpoint has been run from the frozen manifest. Observed velocities were read only in the scoring block, and the branch remains interval-based rather than a residual-tuned point fit.
