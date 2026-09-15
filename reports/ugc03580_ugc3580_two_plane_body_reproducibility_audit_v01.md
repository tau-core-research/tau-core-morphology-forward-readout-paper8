# UGC03580 two-plane body reproducibility audit v01

Status: `REPRODUCIBILITY_AUDIT_PASS`

Independent checks passed: `25/25`.

The audit independently reconstructs the spherical ring normals,
inner/outer plane angle, bounded tilt defect and four source-only
support/weighting/resolution sensitivities. It also inspects the
builder and output schemas for endpoint-bearing paths or columns.

All primary sensitivity shifts remain below the published 2.5 deg
Table 4 uncertainty. This is a geometry robustness result only; it
does not select a velocity kernel or validate Tau Core.
