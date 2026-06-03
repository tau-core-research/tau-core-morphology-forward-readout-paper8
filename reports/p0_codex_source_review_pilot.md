# P0 Codex Source-Reviewed Pilot

This pilot runs the four P0 Codex/source-reviewed audit labels through
the already available exponential-disk and formula-shell score layers. It
is intentionally narrow: it does not launch the frozen 175-galaxy endpoint
and does not claim validation against MOND/RAR/TGP/Newtonian baselines.

## Verdict

Pilot decision: `P0_CODEX_SOURCE_REVIEW_PILOT_COMPLETE_NOT_ENDPOINT`.

Under the primary leave-one-galaxy-out all13 exponential-disk policy,
the P0 Tau readout beats TPG/v6 in 0.750
of cases and beats MOND in 0.250 of cases.
The formula-shell proxy slice is stronger against TPG/v6 on this P0 set,
but MOND remains a hard baseline. This is a useful pilot signal, not an
endpoint result.
This is not an endpoint result.

The score table now separates `k_obs`, `k_readout`,
`readout_proxy_source`, `promotion_status`, and `formula_shell`. In this
narrow pilot the scored shell is still the direct apparent
`K_exponential_disk` control. Rows whose `k_readout` requires projection,
bar/m=2, or compact-core overlay carry
`readout_proxy_overlay_not_scored=True`: they are not yet scored with their readout-proxy shell.

## Summary

| pilot_decision | n_galaxies | primary_amplitude_policy | n_k_obs_exponential_disk | n_distinct_k_readout | n_k_obs_direct | n_k_readout_proxy_promotions | n_readout_proxy_overlay_not_scored | primary_beats_tpg_v6_fraction | primary_beats_mond_fraction | primary_median_tau_minus_tpg_v6 | primary_median_tau_minus_mond | formula_shell_beats_wrong_fraction | formula_shell_beats_tpg_v6_fraction | formula_shell_beats_mond_fraction | source_native_beats_wrong_fraction | source_native_beats_tpg_v6_fraction | source_native_beats_mond_fraction | full_endpoint_manifest_rows_created | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P0_CODEX_SOURCE_REVIEW_PILOT_COMPLETE_NOT_ENDPOINT | 4 | leave_one_galaxy_out_beta_all13 | 4 | 4 | 1 | 3 | 3 | 0.75 | 0.25 | -0.02370912308604375 | 2.4173695930689894 | 1.0 | 1.0 | 0.25 | 0.75 | 0.0 | 0.0 | False | False | p0_codex_source_review_pilot_not_endpoint |

## Readout-Relevant Proxy Context

| readout_relevant_proxy_family | n_galaxies | median_review_confidence | n_direct_k_obs | n_proxy_promotions | uses_rotation_residuals | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| K_barred_expdisk_m2_overlay | 1 | 0.78 | 0 | 1 | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |
| K_clean_exponential_disk_control | 1 | 0.88 | 1 | 0 | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |
| K_expdisk_compact_core_overlay | 1 | 0.74 | 0 | 1 | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |
| K_projection_corrected_expdisk | 1 | 0.7 | 0 | 1 | False | False | p0_readout_relevant_morphology_proxy_not_endpoint |

The pilot above intentionally tests the direct apparent 4D
`K_exponential_disk` handle. The readout-relevant proxy layer records
which rows should later receive projection, bar, or compact-core
corrections before any stronger endpoint claim is attempted.

## P0 Scores

| galaxy | k_obs | k_readout | readout_proxy_source | promotion_status | formula_shell | scored_formula_shell | readout_proxy_overlay_not_scored | accepted_formula_family | review_confidence | manifest_caveat | narrow_dry_run_lane | rmse_tpg_v6 | rmse_mond | primary_tau_rmse | primary_tau_minus_tpg_v6 | primary_tau_minus_mond | primary_tau_beats_tpg_v6 | primary_tau_beats_mond | formula_shell_matched_beats_wrong_mean | formula_shell_matched_beats_tpg_v6 | formula_shell_matched_beats_mond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0100 | K_exponential_disk | K_projection_corrected_expdisk | p0_codex_source_review_caveat_mapping | K_OBS_TO_K_READOUT_PROXY | K_projection_corrected_expdisk | K_exponential_disk | True | K_exponential_disk | 0.7 | edge_projection_caveat | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 7.537919334963079 | 6.061732881040405 | 7.613790597695022 | 0.0758712627319431 | 1.552057716654617 | False | False | True | True | False |
| NGC0247 | K_exponential_disk | K_barred_expdisk_m2_overlay | p0_codex_source_review_caveat_mapping | K_OBS_TO_K_READOUT_PROXY | K_barred_expdisk_m2_overlay | K_exponential_disk | True | K_exponential_disk | 0.78 | bar_component_caveat | CAVEATED_NARROW_DRY_RUN_SUPPORT_POOL | 3.866312004062215 | 5.475417572666649 | 3.6681128037492337 | -0.1981992003129815 | -1.807304768917416 | True | True | True | True | True |
| NGC0300 | K_exponential_disk | K_clean_exponential_disk_control | p0_codex_source_review_caveat_mapping | K_OBS_DIRECT | K_clean_exponential_disk_control | K_exponential_disk | False | K_exponential_disk | 0.88 | none | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 9.83189803567648 | 5.607034629923943 | 9.799701297041354 | -0.0321967386351254 | 4.192666667117411 | True | False | True | True | False |
| NGC6503 | K_exponential_disk | K_expdisk_compact_core_overlay | p0_codex_source_review_caveat_mapping | K_OBS_TO_K_READOUT_PROXY | K_expdisk_compact_core_overlay | K_exponential_disk | True | K_exponential_disk | 0.74 | nuclear_component_caveat | STRICT_NARROW_DRY_RUN_READY_CANDIDATE | 7.537023161651215 | 4.239120184630891 | 7.5218016541142525 | -0.0152215075369621 | 3.2826814694833617 | True | False | True | True | False |

## Claim Boundary

This pilot consumes P0 source-reviewed labels only. It does not create full
endpoint-manifest rows, does not run the frozen endpoint, and does not
validate Tau Core. The frozen endpoint launch guard remains authoritative.

Claim boundary: `p0_codex_source_review_pilot_not_endpoint`.
