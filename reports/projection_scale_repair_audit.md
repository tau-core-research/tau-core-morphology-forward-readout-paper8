# Projection / Scale Repair Audit

This audit identifies projection and scale-quality repair targets using
only residual-blind source and manifest fields. It computes no endpoint
scores and changes no lane assignment.

## Verdict

| split | repair_status | n_galaxies | n_holdout | n_caution | n_acquisition | n_existing_s4g_scale | n_velocity_field_source | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | NEEDS_DISTANCE_SCALE_SOURCE | 30 | 9 | 10 | 20 | 0 | 0 | False | projection_scale_repair_audit_not_endpoint |
| all | NEEDS_INCLINATION_PROJECTION_REVIEW | 26 | 8 | 13 | 13 | 9 | 0 | False | projection_scale_repair_audit_not_endpoint |
| all | NEEDS_VERTICAL_GEOMETRY_SOURCE | 34 | 10 | 18 | 16 | 25 | 0 | False | projection_scale_repair_audit_not_endpoint |
| all | NO_PROJECTION_SCALE_REPAIR_REQUIRED | 71 | 14 | 19 | 51 | 27 | 0 | False | projection_scale_repair_audit_not_endpoint |
| all | REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT | 14 | 3 | 6 | 8 | 14 | 0 | False | projection_scale_repair_audit_not_endpoint |

## Holdout Projection-Caveat Rows

| galaxy | formula_family | repair_status | projection_reason | has_s4g_scale_source | inclination_deg | distance_frac_error |
| --- | --- | --- | --- | --- | --- | --- |
| UGC03580 | K_compact_finite | NEEDS_DISTANCE_SCALE_SOURCE | large_distance_error | False | 63 | 0.251208 |
| F561-1 | K_scale_tail_spiral | NEEDS_INCLINATION_PROJECTION_REVIEW | low_inclination | False | 24 | 0.150602 |
| NGC4214 | K_scale_tail_spiral | NEEDS_INCLINATION_PROJECTION_REVIEW | low_inclination | True | 15 | 0.0487805 |
| NGC6946 | K_compact_finite | NEEDS_INCLINATION_PROJECTION_REVIEW | large_distance_error;low_inclination | False | 38 | 0.300725 |
| UGC02023 | K_scale_tail_spiral | NEEDS_INCLINATION_PROJECTION_REVIEW | large_distance_error;low_inclination;low_manifest_confidence | False | 19 | 0.298077 |
| UGC07261 | K_exponential_disk | NEEDS_INCLINATION_PROJECTION_REVIEW | large_distance_error;low_inclination;low_manifest_confidence | False | 30 | 0.3 |
| UGC11914 | K_compact_finite | NEEDS_INCLINATION_PROJECTION_REVIEW | large_distance_error;low_inclination | False | 31 | 0.301775 |
| F568-1 | K_thick_flared | NEEDS_VERTICAL_GEOMETRY_SOURCE | low_inclination;vertical_geometry_proxy_only | False | 26 | 0.106946 |
| NGC0024 | K_thick_flared | NEEDS_VERTICAL_GEOMETRY_SOURCE | vertical_geometry_proxy_only | True | 64 | 0.0493151 |
| NGC3726 | K_thick_flared | NEEDS_VERTICAL_GEOMETRY_SOURCE | vertical_geometry_proxy_only | True | 53 | 0.138889 |
| NGC3949 | K_thick_flared | NEEDS_VERTICAL_GEOMETRY_SOURCE | vertical_geometry_proxy_only | True | 55 | 0.138889 |
| NGC4088 | K_thick_flared | NEEDS_VERTICAL_GEOMETRY_SOURCE | vertical_geometry_proxy_only | True | 69 | 0.138889 |
| NGC4389 | K_thick_flared | NEEDS_VERTICAL_GEOMETRY_SOURCE | vertical_geometry_proxy_only | True | 50 | 0.138889 |
| NGC5985 | K_compact_finite | REPAIRABLE_WITH_EXISTING_SCALE_SOURCE_PLUS_DISTANCE_AUDIT | large_distance_error | True | 60 | 0.24937 |

## Claim Boundary

This is a source-acquisition and repair map, not an empirical validation
result. Repairable means source-side repairable, not endpoint-improving.
