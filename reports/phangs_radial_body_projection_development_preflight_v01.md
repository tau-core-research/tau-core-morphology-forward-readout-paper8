# PHANGS radial body-projection development preflight v01

Status: `SOURCE_BODY_MATRIX_DEVELOPMENT_PREFLIGHT_RANK_GATE_PASSES_PARTIAL_COHORT`

No velocity or residual endpoint was opened. The source-only 20-by-8 body matrix has:

- `NGC1087`: rank `8`, complement dimension `12`, nonzero condition number `4.41`.
- `NGC1433`: rank `8`, complement dimension `12`, nonzero condition number `6.32`.
- `NGC1566`: rank `8`, complement dimension `12`, nonzero condition number `5.38`.
- `NGC1672`: rank `8`, complement dimension `12`, nonzero condition number `14.4`.
- `NGC7496`: rank `8`, complement dimension `12`, nonzero condition number `10.2`.

The radial edges are provisional source-only CO-support quantiles. The final matrix must be recomputed on the frozen terminal common-support edges; these values validate only numerical construction and conditioning.
