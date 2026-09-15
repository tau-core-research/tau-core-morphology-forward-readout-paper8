# UGC08490 / NGC5204 unchanged NGC4088-class transfer freeze v01

Status: `RETROSPECTIVE_SOURCE_FROZEN_CLASS_TRANSFER_READY_NOT_SCORED`

The NGC4088 warp/history formula is copied without changing its sign,
binary warp activation, or linear turn-on. The UGC08490-specific onset
comes from the promoted TiRiFiC two-plane warp body; `R_HI` and the
primary `Vflat` come from the published SPARC master row. No pointwise
`vobs` value or endpoint residual is read by this freeze step.

## Frozen values

- harmonized warp onset: `3.516835 kpc`;
- `x_w = 0.450876300`;
- primary `Vflat = 78.600 km/s`;
- primary `lambda_w = 2785.495746 km^2/s^2`;
- predeclared external-source sensitivity `V = 82.500 km/s`,
  giving `lambda_w = 3068.776816 km^2/s^2`;
- `q_warp=1`, `sigma_warp=+1`, and `p=1` are unchanged class-law choices.

## Epistemic boundary

This is not a prospective blind endpoint: UGC08490 was opened in earlier,
different tracer analyses. It is nevertheless a valid frozen-formula
retrospective transfer check because the current pointwise endpoint and
its residuals did not select the transfer parameters. The use of catalog
`Vflat` means this is not a fully kinematically independent amplitude
prediction; it primarily tests whether the source-selected warp onset and
unchanged radial law transfer.

Manifest SHA-256: `24afaae684cfb53700f969c4114278636c7aaf42a2a74a891952b7e1ab66db17`.
