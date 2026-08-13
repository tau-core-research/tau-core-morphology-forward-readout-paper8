# NGC4254 FFL uncertainty-source acquisition v04

Status: `SOURCE_UNCERTAINTY_ACQUISITION_PARTIAL_CO_EXACT_HI_CONTROL_STELLAR_INPUTS_READY`

This residual-blind pass acquired the source products required to replace the v03 equal-weight source scenarios with measurement-informed uncertainty constructions. No observed rotation endpoint, dark-discrepancy residual, or terminal score was read.

## Acquired source families

- `PHANGS_ALMA_CO21`: 2 products
- `S4G_IRAC`: 16 products
- `SPITZER_IRAC`: 1 products
- `VIVA_HI`: 2 products

## What is now available

- CO: the official PHANGS `broad_emom0` map is acquired and exactly matches the frozen `broad_mom0` spatial grid.
- H I: the public VIVA spectral cube is acquired, but its robust-1 CLEAN beam differs from the robust-5, UV-tapered beam recorded in the frozen moment-0 history. It is therefore a noise/channel-correlation control only. The exact parent cube or a source-native moment-0 error map remains missing; the atlas noise value is also only a cross-check.
- H I control check: the outer-field line-free channels give median robust noise `0.457` mJy/beam versus the VIVA atlas value `0.41` mJy/beam, with median clipped adjacent-channel correlation `0.171`. These values characterize the nonidentical robust-1 control cube only.
- Stellar: the P1 channel mosaics, coverage maps, P2 masks, P3 radial-error profiles, P5 ICA mask/color/nonstellar products, and IRAC handbook are acquired. S4G does not distribute a P5 pixelwise stellar uncertainty map in this product directory, so the uncertainty must be constructed and kept separate from the global mass-to-light scale.

## Claim boundary

source-native uncertainty acquisition and product-identity audit only; not a complete covariance, morphology attribution, channel signal, or endpoint score.

Machine-readable manifest: `data/derived/ngc4254_ffl_uncertainty_source_acquisition_v04.json`.
Source ledger: `data/derived/ngc4254_ffl_uncertainty_source_ledger_v04.csv`.
