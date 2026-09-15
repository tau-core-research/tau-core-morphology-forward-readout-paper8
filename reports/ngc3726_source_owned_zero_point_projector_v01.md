# NGC3726 source-owned velocity-zero-point projector v0.1

**Status:** `SOURCE_DERIVED_ZERO_POINT_PROJECTOR_PASS_OPENED_SHAPE_NULL_NOT_REJECTED`

For each tracer, a fixed systemic-velocity shift changes the receding-minus-approaching line-of-sight odd contrast with derivative `-2`. The two independent tracer zero points therefore generate columns `(-2,+2)` repeated at every radius. Those columns are collinear and span one common radial nuisance mode.

The covariance-weighted projector passes annihilation, idempotence, weighted self-adjointness, finite-shift invariance, and constant-mode controls. Six common radii leave five radial shape degrees of freedom. The already opened shape-only statistic is `chi2=9.1784` for `5` degrees of freedom (`p=0.1022`), so zero remains unrejected.

This improves the method, not the empirical status. It removes any radius-independent relative velocity-zero-point offset exactly, but it also removes every constant radial signal. No morphology-specific nonconstant template is supplied, and missing beam/center/PA/radial covariance remains. Because NGC3726 was opened before this audit, it is an independent-survey development control rather than a new confirmatory endpoint.
