# PHANGS radial body-projection holdout identifiability v01

Verdict: `PROVEN_FINITE_LINEAR_NO_GO`
Status: `CURRENT_PROJECTION_PACKET_DOES_NOT_IDENTIFY_GROUPED_HOLDOUT_BODY_INCREMENT`

## Claim

The frozen nuisance matrix and projector identify a body-orthogonal detection statistic, but do not identify grouped body-level predictive gain.

## Proof

For each development body, the same source matrix permits distinct terminals `S_g beta_1` and `S_g beta_2` because `beta_g` is not supplied by the source packet. The eight-dimensional body span plus the twelve-dimensional projector complement has rank 20, so an arbitrary per-body complement term saturates the terminal rather than predicts it. Finally, identical training data and an identical held-out source matrix admit both zero and nonzero held-out projected worlds. No estimator using only that packet can select between them.

## Suggested Fix

Keep the projected `Q` test as the one-shot body-orthogonal detection endpoint. Treat grouped holdout body increment as a later promotion stage requiring a separately frozen source-to-`beta` map and a low-dimensional, non-saturating source-to-complement law.
