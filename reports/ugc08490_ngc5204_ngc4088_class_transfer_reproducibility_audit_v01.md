# UGC08490 / NGC5204 class-transfer reproducibility audit v01

Status: `REPRODUCIBILITY_AUDIT_PASS`

An independent implementation rebuilt the baryonic carrier, fixed-MOND
comparator, warp kernel, and wrong-onset control directly from the raw
endpoint and the pre-existing hashed freeze manifest.

- reproduced `x_w`: `0.450876299905`;
- reproduced primary RMSE: `29.703509883114 km/s`;
- reproduced wrong-onset RMSE: `31.640625391095 km/s`;
- reproduced fixed-MOND RMSE: `8.782045083335 km/s`;
- checks passed: `16/16`.

This audit validates numerical reproducibility and claim-boundary
preservation. It does not turn the retrospective endpoint into a
prospective or physically validating result.
