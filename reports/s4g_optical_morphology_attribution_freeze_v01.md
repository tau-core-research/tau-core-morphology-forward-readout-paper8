# S4G Optical Morphology Attribution Freeze v0.1

**Status:** `SOURCE_ONLY_RETROSPECTIVE_LOCK_READY`

This freeze reads no observed velocity, residual, score, RMSE,
MOND/TPG, or endpoint artifact. It fixes the source rows, feature
sets, split, imputation, standardization, model, metrics, controls,
and promotion rule before the separate scorer is run.

- rows: `76`
- train: `56`
- holdout: `20`
- baseline features: `10`
- morphology features: `14`
- baseline missingness flags: `1`
- morphology missingness flags: `5`

The split is deterministic from galaxy name and a frozen salt.
Because SPARC endpoints have been analyzed elsewhere in the program,
this is a retrospective lock, not a prospective blind validation.

No endpoint scoring is performed by this script.
