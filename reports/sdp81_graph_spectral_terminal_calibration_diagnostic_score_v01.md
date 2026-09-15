# SDP.81 graph-spectral terminal-calibration score v01

Status: `RETROSPECTIVE_DIAGNOSTIC_ONLY_NOT_ENDPOINT`. Verdict: `CANONICAL_BASIS_DERIVED_MONOTONE_ASSIGNMENT_NOT_SUPPORTED`.

The declared P6 graph removes arbitrary Helmert-column ordering. The monotone assignment beats lossless in `9/9` geometries, but never every wrong path assignment; its exact assignment-rank range is `0.375--0.417`. The reverse control gives `0.083--0.333`, and the isotropic control gives `0.333--0.375`.

Across all 120 stiffness-to-mode permutations, the monotone assignment ranks `39--81/120` (`p=0.325--0.675`); the reverse ranks `55--97/120`. There are `3` distinct best assignments across the nine covariance geometries.

The P6 graph gives a canonical mode basis, but the source-frozen monotone WR-T19 assignment is not selected by this endpoint: its exact path-assignment rank range is worse than the predeclared reverse control, and its rank within all 120 stiffness-to-mode assignments is only mid-pack. That comparison is retrospective and the depth remains a 4D Fermat proxy. It neither chooses a replacement assignment nor validates a parent-to-terminal calibration or Nature occupation.
