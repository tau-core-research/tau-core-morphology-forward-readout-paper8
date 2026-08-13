# NGC4321 PHANGS 2D tracer velocity-field rank test

Status: `TWO_DIMENSIONAL_TRACER_INNOVATION_DIAGNOSTIC`

The common quality mask has `114884` pixels and `4575` beam-independent samples. The frozen 25-mode innovation test gives `chi2=43005.59` for `25` dof (`p=0`); maximum absolute single-mode significance is `94.95`. A 12-sector spatial jackknife reduces the maximum absolute mode significance to `3.10` and gives a combined diagnostic `p=9.418e-54`; this is the preferred robustness diagnostic, while the formal chi-square is retained for reproducibility. With a conservative `10 km/s` error floor the largest formal mode significance is `13.57`.

The test uses source-native CO and H-alpha velocity fields and no rotation residual. Any surviving contrast remains compatible with ordinary tracer and non-circular gas physics and does not identify time, path, quantum, or Tau origin.
