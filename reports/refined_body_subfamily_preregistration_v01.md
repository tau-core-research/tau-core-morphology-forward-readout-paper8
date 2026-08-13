# Refined body-subfamily preregistration v01

Status: `SOURCE_ACQUISITION_ONLY`

This freezes a residual-blind test of four refined morphological-body families. The motivating P0 failures are explicitly excluded from endpoint evidence, including all aliases. Classification and radial activation must be determined from source-native morphology and kinematics before rotation-curve scoring is opened.

## Frozen decision order

1. Resolve physical aliases and remove every historical or motivating object.
2. Acquire all required source fields and classify without `vobs` or residual access.
3. Freeze family, kernel, amplitude policy, sign, and active radial zone.
4. Score matched, wrong-family, and Newtonian controls in a separate process.
5. Test a channel only on cross-tracer residual structure left after the matched refined body.

## Population verdict

The refined-body route passes only if the matched-minus-wrong-family mean RMSE difference is negative with a one-sided galaxy permutation `p <= 0.05`, the matched family beats the best wrong family in at least `60%` of independent galaxies, and its gain is stronger inside the source-frozen active zone. At least five independent galaxies per family and twenty total are required.

No universal superiority over Newton, MOND, or TPG is assumed. Every comparison is reported, including negative results.

## Frozen families

### `K_scale_tail_turbulent_holey`

- Motivating objects, excluded from endpoint evidence: `UGC04305;DDO_50;Holmberg_II`.
- Required fields: `HI_hole_catalog;HI_velocity_dispersion_profile;hole_covering_fraction;outer_HI_support_radius`.
- Classification: resolved HI holes plus a published or source-measurable non-thermal dispersion profile across the optical disk.
- Kernel change: smooth scale-tail carrier multiplied by a bounded radial porosity-dispersion modulation.
- Active zone: published HI-hole support union outer turbulent HI disk.

### `K_disturbed_tidal_history`

- Motivating objects, excluded from endpoint evidence: `UGC07577;DDO_125`.
- Required fields: `companion_or_stream_detection;projected_stream_support;kinematic_asymmetry;interaction_confidence`.
- Classification: independent tidal stream or companion evidence and a source-side disturbed-kinematics flag.
- Kernel change: coarse carrier plus a bounded asymmetric outer-support term restricted to the source-marked disturbance zone.
- Active zone: source-marked stream or disturbed outer-disk support.

### `K_warped_asymmetric_disturbed_disk`

- Motivating objects, excluded from endpoint evidence: `NGC4088;UGC7081`.
- Required fields: `warp_onset_radius;tilted_ring_PA_profile;approaching_receding_asymmetry;outer_HI_radius`.
- Classification: source-measured warp onset plus significant side-to-side or position-angle asymmetry.
- Kernel change: thick/flared carrier split into symmetric vertical and signed warp-asymmetry components.
- Active zone: R greater than or equal to the source-frozen warp onset.

### `K_bar_dominated_non_circular`

- Motivating objects, excluded from endpoint evidence: `NGC4389;UGC7514`.
- Required fields: `bar_length;bar_position_angle;harmonic_non_circular_amplitude;bar_confidence`.
- Classification: independently measured stellar bar and a source-side non-circular velocity harmonic.
- Kernel change: thick/flared carrier with a compact bar-windowed non-circular component.
- Active zone: R less than or equal to the source-frozen bar length.

## Claim boundary

This document is a preregistration, not evidence that any refined family is physically correct. It also does not identify time, quantum, capacity, light-cone, or other channel physics. Such attribution is permitted only after a source-frozen refined-body score leaves a reproducible cross-tracer remainder.
