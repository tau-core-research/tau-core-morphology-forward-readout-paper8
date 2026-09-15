# EDGE--CALIFA confirmatory endpoint v02: independent reproducibility audit

Status: `PASS_WITH_PROVENANCE_LIMITATIONS_NEGATIVE_ENDPOINT_CONFIRMED`

## Result

The independent audit passed 32/32 executable checks. It rebuilt the 7 x 20
terminal packet, all five-zone occupied-sector covariance matrices, source projections,
Q scores, per-galaxy control contrasts, and exact inference without importing the endpoint
or scoring implementation.

- exact primary result: 77/128 = `0.6015625`;
- reconstructed mean D: `-0.058679293503004`;
- positive D count: `4/7`;
- max-T adjusted control p-values: `[0.9765625, 0.9453125, 0.3359375]`;
- reconstructed endpoint status: `SOURCE_DEVELOPED_EXTERNAL_MORPHOLOGY_ALIGNMENT_PREVALIDATION_FAIL`;
- failed executable checks: `none`.

| Galaxy | independently reconstructed D |
| --- | ---: |
| IC4566 | -0.134569371944429 |
| NGC2730 | 0.921937739257448 |
| NGC3811 | 0.110201943959885 |
| NGC6004 | 0.959250379664052 |
| NGC6060 | -1.05943835527742 |
| NGC6186 | -1.98689134631831 |
| NGC6301 | 0.77875395613775 |

The negative prevalidation status is therefore numerically reproduced. It is not a positive
Tau Core signal and does not identify physics beyond the declared standard comparator.

## Hash and structure audit

The public HDF5 packet matches the frozen size, MD5, and SHA-256. The current preregistration,
scoring contract, source matrices, endpoint script, implementation manifest, calibration table,
and endpoint JSON satisfy their recorded hash relations. The coefficient CSV has SHA-256
`f567e6a399cfbefd59c022c3f350d2a52317f12ef443f61986f3b975a7449ec9` and all 140 rows reproduce from the raw packet;
the largest coefficient residual is
`3.553e-15 km/s`.

For every galaxy, the standard source has rank 8 with a rank-12 complement. The correct and
three wrong-family sources have rank 16 with rank-4 complements; the independently rebuilt
projectors annihilate their source columns below the audit tolerance, and every terminal
covariance is positive definite and rank 20.

## Reproducibility limits

- `freeze_chronology_not_externally_anchored`: The current bytes and their internal hash chain agree, but local sidecars do not independently prove that preregistration and implementation bytes predated endpoint opening. A trusted commit, release, registry, or timestamp is required for that historical claim.
- `implementation_manifest_runtime_trust_gap`: The endpoint runtime reads the implementation manifest to obtain the expected script hash but does not first pin that manifest to its sidecar or another immutable anchor. The present audit verifies the current manifest sidecar and script relation only.
- `coefficient_csv_not_in_original_endpoint_provenance`: The original endpoint JSON/sidecar does not bind the coefficient CSV. This audit records its current SHA-256 and independently reconstructs every coefficient from the hash-matched raw packet.
- `external_raw_packet_not_vendored`: Full matrix-level reproduction requires the 84,941,807-byte public HDF5 packet. It is identified by DOI, MD5 and SHA-256 but is not stored in the repository.
- `negative_endpoint_not_tau_specific`: The reproduced failure is a negative result for this development-informed proxy only. It neither validates nor falsifies the general Tau Core architecture, and the declared standard/eDIG span is not exhaustive.

## Claim boundary

This audit confirms the saved numerical negative endpoint conditional on the hash-matched raw packet and current artifacts. It does not establish freeze chronology, a Tau-specific law, a beyond-standard component, dark-sector physics, or exhaustive conventional comparison.
