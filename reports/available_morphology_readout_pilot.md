# Available-data Morphology Readout Pilot

This report audits what can be checked today from existing local data.
It is not the final Paper 8 MORPHOLOGY-MATCHED-FORWARD-READOUT-GATE
because residual-blind morphology-family labels and per-family
forward `delta_g^K` score tables are not yet available.

## Main Verdict

- The full Paper 8 morphology-family endpoint is still blocked.
- The available 143-galaxy component proxy supports a narrower statement:
  the v02_core_like Tau-like/FixedTPG proxy group beats RAR, MOND, and
  Newtonian within that residual-guardrailed proxy group.
- This is not yet evidence that morphology-selected Tau Core families beat
  TGP, because the proxy group uses FixedTPG itself rather than distinct
  Paper 8 morphology-family formula outputs.
- The morphology-decomposition runner is mixed: some morphology splits improve
  over TPG/v6, others do not.
- Full-sample RMOND comparison is blocked until a frozen pointwise
  `V_RMOND(R)` prescription exists.

## Key Proxy Result

v02_core_like has n=6, FixedTPG rank-1 fraction=1.000, beats RAR fraction=1.000, beats MOND fraction=1.000, beats Newtonian fraction=1.000.

## Best Morphology-Decomposition Holdout Rows

| ybulge | group_key | n_groups | total_points | mean_delta_tau_minus_v6 | median_delta_tau_minus_v6 | improvement_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| 1.1 | type_bin | 4 | 835 | -1.99755 | -0.787096 | 0.75 |
| 1.1 | radius_bin | 4 | 835 | -1.92734 | -0.123083 | 0.75 |
| 1.1 | bulge_presence | 2 | 835 | -1.47886 | -1.47886 | 0.5 |

## Limited RMOND/MOND Gallery

HDDA/DTL is better than the combined RMOND/MOND comparator in 0.500 of the six gallery objects.
This is only an illustrative mixed-unit gallery check, not a Paper 8 endpoint.

## Required Next Action

Create `morphology_labels_predeclared.csv` and a per-family scored table
`matched_wrong_family_scores.csv` where each galaxy is evaluated under
all candidate morphology families. Only then can Paper 8 answer the
main question directly: matched Tau Core family versus wrong families,
shuffled labels, TGP, RMOND, MOND, RAR, and Newtonian.

## Wide Proxy Summary

| sample | model | n_galaxies | mean_rms_log10 | median_rms_log10 | pooled_rms_log10 |
| --- | --- | --- | --- | --- | --- |
| not_v02_core_like | RAR | 137 | 0.0859317 | 0.0676396 | 0.108692 |
| not_v02_core_like | MOND | 137 | 0.0863027 | 0.0677072 | 0.109081 |
| not_v02_core_like | FixedTPG | 137 | 0.0879554 | 0.0662074 | 0.108726 |
| not_v02_core_like | Newtonian | 137 | 0.267829 | 0.250109 | 0.290628 |
| v02_core_like_proxy | FixedTPG | 6 | 0.113723 | 0.102529 | 0.116133 |
| v02_core_like_proxy | RAR | 6 | 0.146568 | 0.13865 | 0.149465 |
| v02_core_like_proxy | MOND | 6 | 0.146888 | 0.138924 | 0.149772 |
| v02_core_like_proxy | Newtonian | 6 | 0.246039 | 0.232581 | 0.248296 |
