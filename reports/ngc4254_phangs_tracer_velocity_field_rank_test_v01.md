# NGC4254 PHANGS 2D tracer velocity-field rank test

Status: `TWO_DIMENSIONAL_TRACER_INNOVATION_DIAGNOSTIC`

The common quality mask has `86670` pixels and `5410` beam-independent samples. The frozen 25-mode innovation test gives `chi2=40600.37` for `25` dof (`p=0`); maximum absolute single-mode significance is `68.75`. A 12-sector spatial jackknife reduces the maximum absolute mode significance to `2.85`; this is the preferred robustness diagnostic, while the formal chi-square is retained for reproducibility. With a conservative `10 km/s` error floor the largest formal mode significance is `4.22`.

The test uses source-native CO and H-alpha velocity fields and no rotation residual. Any surviving contrast remains compatible with ordinary tracer and non-circular gas physics and does not identify time, path, quantum, or Tau origin.
