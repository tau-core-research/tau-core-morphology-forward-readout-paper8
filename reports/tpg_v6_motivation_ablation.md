# TPG/v6 motivation ablation

Status: `TPG_V6_STRUCTURAL_MOTIVATION_ABLATION_COMPLETE`

The logarithm is conditionally forced by multiplicative finite-capacity loading and additive response. The acceleration ratio `a0/aN(R)` supplies a local, dimensionless activation coordinate and automatically turns the response off in the Newtonian limit.

Frozen TPG/v6 holdout mean galaxy RMSE is `17.643 km/s`. Replacing `alpha=0.360` by the cosmological candidate `0.366` changes this by `+0.023 km/s`. Refitting alpha on train gives `0.3908` and changes holdout by `+0.336 km/s`.

The generalized DTL train grid selects `gamma=1.0`, `beta=1.0`, `alpha=0.3908`. See the CSV artifacts for linear, bounded, logarithmic, and generalized controls.

The test diagnoses where the empirical strength resides. It does not derive `a0`, the metric normalization, or the ordered-disk branch from the Tau parent.
