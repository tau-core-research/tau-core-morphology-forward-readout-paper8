# Readout-Subfamily Observable Intake

This first-pass intake proposes readout-relevant subfamilies from
residual-blind manifest/source fields. It is not an accepted label layer
and it does not compute endpoint scores.

## Gate Status

| gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| SOI1_SCHEMA_DEFINED | PASS | subfamily observable fields and forbidden sources are recorded | none | False | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |
| SOI2_FIRST_PASS_MANIFEST_POPULATED | PASS | 9 atlas galaxies receive first-pass subfamily proposals | extend to larger source-rich set | False | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |
| SOI3_NO_ENDPOINT_SELECTION | PASS | subfamily choices use manifest/source proxy fields, not vobs scores | preserve this boundary during audit | False | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |
| SOI4_ACCEPTED_SOURCE_READY | PENDING | all rows remain first-pass/proxy-only or diagnostic; no accepted subfamily labels promoted | fill accepted residual-blind observables per missing_for_acceptance | False | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |

## Observable Fields

| field | accepted_source_path | proxy_source_path | used_for_subfamilies | forbidden_source | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| warp_onset_or_outer_bend | HI velocity field; optical/IR outer-disk warp review; source-extracted warp onset | manifest_caveat; inclination/projection caveat; NGC4088 source-bound warp lane | K_warp_history_coupled;K_flared_outer_disk;K_projection_dominated | rotation residual shape; best-fitting Tau branch | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |
| hi_asymmetry_or_tail_support | HI maps/asymmetry indices; resolved HI radius and outer profile | SPARC RHI/MHI; gas-rich/irregular flag; literature source hits | K_smooth_n2_tail;K_disturbed_outer_tail;K_warp_history_coupled | outer rotation residual improvement | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |
| projection_safety | inclination uncertainty; dust lane/projection review; velocity-field sanity check | SPARC inclination; inc_bin; manifest_caveat | K_projection_dominated;K_clean_expdisk;K_thick_regular | bad model fit after deprojection | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |
| clean_disk_support | S4G/SPARC disk scale and no bar/ring/warp caveat from residual-blind review | type_bin; scale_radius_proxy_kpc; manifest_caveat | K_clean_expdisk | readout family inferred from rotation endpoint | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |
| bar_core_overlay_support | S4G component decomposition; bar/core/nuclear support | mean_bulge; max_bulge; p0 source review caveats where available | K_expdisk_overlay;K_compact_plus_disk;K_true_compact | residual peak/ring chosen from fit | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |
| vertical_or_flare_support | edge-on thickness; flare gradient; vertical profile; HI warp/flare evidence | thickness_h_over_rs_proxy; inc_bin; vertical_geometry_proxy_only caveat | K_thick_regular;K_flared_outer_disk;K_warp_history_coupled | endpoint-selected damping factor | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |
| morphology_history_memory_support | residual-blind interaction/environment/history review | morphological_memory_history_proxy flags; source-side interaction evidence | K_warp_history_coupled;K_disturbed_outer_tail;K_expdisk_overlay | rotation-inferred family as accepted label | readout_subfamily_observable_intake_not_endpoint_not_accepted_label |

## First-Pass Subfamily Summary

| formula_family | proposed_readout_subfamily | subfamily_status | n_galaxies |
| --- | --- | --- | --- |
| K_compact_finite | K_true_compact | proxy_only | 2 |
| K_exponential_disk | K_expdisk_overlay | proxy_only | 2 |
| K_scale_tail_spiral | K_disturbed_outer_tail | proxy_only | 2 |
| K_thick_flared | K_projection_dominated | proxy_only | 1 |
| K_thick_flared | K_thick_regular | proxy_only | 1 |
| K_thick_flared | K_warp_history_coupled | diagnostic_subfamily_not_accepted | 1 |

## First-Pass Manifest

| galaxy | formula_family | proposed_readout_subfamily | subfamily_selection_reason | missing_for_acceptance | subfamily_status |
| --- | --- | --- | --- | --- | --- |
| IC2574 | K_scale_tail_spiral | K_disturbed_outer_tail | gas-rich diffuse/irregular source proxy suggests tail/history sensitivity | HI asymmetry maps; outer-tail transition radius; environment review | proxy_only |
| IC4202 | K_compact_finite | K_true_compact | bulge/core support is high enough for compact-dominant proxy | compact support radius and bulge/core decomposition | proxy_only |
| NGC4013 | K_compact_finite | K_true_compact | bulge/core support is high enough for compact-dominant proxy | compact support radius and bulge/core decomposition | proxy_only |
| NGC4088 | K_thick_flared | K_warp_history_coupled | source-bound warp/history lane already exists for NGC4088 | warp onset/asymmetry; HI disturbance; interaction/history; epsilon_cross bound | diagnostic_subfamily_not_accepted |
| NGC4183 | K_exponential_disk | K_expdisk_overlay | exponential disk has caveat, bulge/core/projection, or memory mismatch proxy | bar/core/projection/history overlay source review | proxy_only |
| NGC5907 | K_thick_flared | K_projection_dominated | edge-on or projection-sensitive thick/flared morphology | projection/deprojection audit; dust lane review; velocity-field sanity check | proxy_only |
| NGC7331 | K_thick_flared | K_thick_regular | vertical proxy exists but no accepted flare/warp source | direct vertical scale or flare-gradient source | proxy_only |
| UGC05716 | K_scale_tail_spiral | K_disturbed_outer_tail | gas-rich diffuse/irregular source proxy suggests tail/history sensitivity | HI asymmetry maps; outer-tail transition radius; environment review | proxy_only |
| UGC12506 | K_exponential_disk | K_expdisk_overlay | exponential disk has caveat, bulge/core/projection, or memory mismatch proxy | bar/core/projection/history overlay source review | proxy_only |

## Claim Boundary

The intake is a residual-blind proposal layer. It is designed to be
audited before endpoint scoring. The next step is to replace proxy reasons
with accepted source observables such as HI asymmetry, warp onset, bar/core
decomposition, vertical flare, and projection-safety evidence.
