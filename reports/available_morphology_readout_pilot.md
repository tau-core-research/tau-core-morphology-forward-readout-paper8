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
- The 175-galaxy Tau-proxy runner gives a larger-sample check against TPG/v6
  and MOND, but it is still a proxy family rather than the final Paper 8
  morphology-family readout.
- Full-sample RMOND comparison is blocked until a frozen pointwise
  `V_RMOND(R)` prescription exists.

## Key Proxy Result

v02_core_like has n=6, FixedTPG rank-1 fraction=1.000, beats RAR fraction=1.000, beats MOND fraction=1.000, beats Newtonian fraction=1.000.

## Larger-Sample 175-Galaxy Proxy Runner

175-galaxy proxy runner holdout: n=44, Tau-proxy beats TPG/v6 fraction=0.659, mean Tau-TPG delta=-0.112452, Tau-proxy beats MOND fraction=0.591.

Best type-bin holdout rows by mean Tau-minus-TPG/v6 delta:

| split | type_bin | n_galaxies | mean_tau_minus_tpg_v6 | median_tau_minus_tpg_v6 | tau_beats_tpg_v6_fraction | mean_tau_minus_mond | median_tau_minus_mond | tau_beats_mond_fraction | tpg_v6_beats_mond_fraction | mean_rmse_tau_proxy | mean_rmse_tpg_v6 | mean_rmse_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | early_T_le_2 | 3 | -0.827931 | -0.766689 | 1 | 0.388905 | 0.027563 | 0.333333 | 0.333333 | 24.0051 | 24.833 | 23.6162 |
| holdout | late_T_6_8 | 10 | -0.0944443 | -0.101655 | 0.7 | 0.00586451 | 0.607583 | 0.5 | 0.5 | 12.4217 | 12.5161 | 12.4158 |
| holdout | irregular_T_ge_9 | 18 | -0.0529939 | -0.0253703 | 0.722222 | -0.752689 | -1.66534 | 0.611111 | 0.611111 | 12.8232 | 12.8762 | 13.5759 |
| holdout | mid_T_3_5 | 13 | -0.0435201 | 0.00631566 | 0.461538 | -1.02766 | -1.7185 | 0.692308 | 0.692308 | 26.4826 | 26.5261 | 27.5103 |

## 73-Galaxy Paper 1 Full-Baseline Layer

This layer contains Newtonian, MOND, RAR, projection, and several
Tau-core S_tau score variants, but it is an A/B/C residual-disturbance
sample rather than a Paper 8 morphology-family endpoint.

| tau_score | baseline | n_galaxies | mean_tau_minus_baseline | median_tau_minus_baseline | tau_beats_baseline_fraction |
| --- | --- | --- | --- | --- | --- |
| tau_core_s_soft | newtonian_baryonic | 73 | -0.408967 | -0.423855 | 0.945205 |
| tau_core_s_continuous | newtonian_baryonic | 73 | -0.29276 | -0.312436 | 0.917808 |
| tau_core_s_class | newtonian_baryonic | 73 | -0.243123 | -0.280565 | 0.60274 |
| tau_core_s_evidence | newtonian_baryonic | 73 | -0.243123 | -0.280565 | 0.60274 |
| tau_core_s_soft | projection_fixed | 73 | 0.0273698 | 0.0182482 | 0.39726 |
| tau_core_s_soft | mond_simple_mu | 73 | 0.0237252 | 0.0235818 | 0.424658 |
| tau_core_s_soft | rar_mcgaugh | 73 | 0.0249442 | 0.0257435 | 0.424658 |
| tau_core_s_continuous | mond_simple_mu | 73 | 0.139932 | 0.0743849 | 0.30137 |

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
