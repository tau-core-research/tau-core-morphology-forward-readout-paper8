# UGC03580 / UGC3580 radial two-plane body proxy v01

Status: `SOURCE_ACQUISITION_ONLY`

## What changed

The former scalar body proxy retained only a warp onset. This source-only
reconstruction instead uses every published UGC3580 Table 6 ring orientation
while deliberately omitting the published rotation-velocity columns and all
SPARC endpoint values.

For each radius the local plane is represented by the source normal

```text
n(R) = (sin(i) sin(PA), -sin(i) cos(PA), cos(i)) in S2.
```

Adjacent rings are connected by shortest great-circle interpolation. The
source-native bounded morphology defect is

```text
delta_tilt(R) = 1 - n_inner dot n(R),    0 <= delta_tilt <= 2.
```

It is a descriptor, not a velocity kernel.

## Primary source geometry

- supported rings: `17` through `375 arcsec`;
- outer-plane rings: `5` over `240-375 arcsec`;
- reconstructed inner/outer separation: `14.297 deg`;
- independent Table 4 summary: `13.9 +/- 2.5 deg` (`z=0.159`);
- maximum supported bounded defect: `0.037542`;
- maximum connection gradient: `3.715 deg/kpc`.

## Validation

- maximum orientation/table-normal disagreement: `0.0845 deg`;
- maximum published-tip reconstruction residual: `0.0927 deg`;
- maximum inner-plane defect through 150 arcsec: `0.000e+00`;
- maximum sampled SLERP unit-norm error: `1.110e-16`;
- density-weighted outer-plane sensitivity: `1.487 deg`;
- include-420-arcsec support sensitivity: `1.806 deg`;
- maximum leave-one-outer-ring-out shift: `1.365 deg`.

## Claim boundary

This closes a source-representation defect: UGC03580 is no longer reduced
to one onset radius. It does not show that the refined morphology explains
the rotation curve. A readout shell, amplitude and carrier still have to be
derived without endpoint access and then frozen on a genuinely new target.
The object is a localized galaxy-scale body proxy, not a separately seeded
universe-level Tau morphological body.

Source PDF SHA-256: `15b4ae9e2bb3268509e75b40e62def8cc4664a117fdcccafae8afb7f170ec8ba`.
Source table SHA-256: `fb27253af89e667395eca2ccec23055b79dd74ee0fe38bbc5e26ae800ba4e568`.
