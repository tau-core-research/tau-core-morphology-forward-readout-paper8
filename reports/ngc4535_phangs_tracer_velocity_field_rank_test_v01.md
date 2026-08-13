# NGC4535 PHANGS 2D tracer velocity-field rank test

Status: `TWO_DIMENSIONAL_TRACER_INNOVATION_DIAGNOSTIC`

The common quality mask has `32285` pixels and `2007` beam-independent samples. The frozen 25-mode innovation test gives `chi2=13859.95` for `25` dof (`p=0`); maximum absolute single-mode significance is `41.43`. A 12-sector spatial jackknife reduces the maximum absolute mode significance to `2.04` and gives a combined diagnostic `p=1.327e-06`; this is the preferred robustness diagnostic, while the formal chi-square is retained for reproducibility. With a conservative `10 km/s` error floor the largest formal mode significance is `6.18`.

The test uses source-native CO and H-alpha velocity fields and no rotation residual. Any surviving contrast remains compatible with ordinary tracer and non-circular gas physics and does not identify time, path, quantum, or Tau origin.
