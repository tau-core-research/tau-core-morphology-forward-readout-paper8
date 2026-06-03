# P0 Missing-Data Source Acquisition Plan

This report operationalizes the requested source policy for the Paper 8
P0 review lane: use S4G, NED/NED-D, DustPedia, HI survey data, and PHANGS
where appropriate. It is a source-acquisition plan only, not an accepted morphology manifest and not an endpoint score.

## Verdict

P0 galaxies covered: 4.
Residual-blind source tasks: 52.
Required P0 source tasks: 28.

All tasks remain `TO_BE_ACQUIRED_RESIDUAL_BLIND`; no accepted label is
created and no Tau/MOND/RAR/TGP/Newtonian endpoint comparison is run.

## Source Family Summary

| source_family | url_or_catalog | n_p0_tasks | n_p0_galaxies | source_acquisition_status | accepted_label_output_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4G | https://irsa.ipac.caltech.edu/data/SPITZER/S4G/overview.html | 48 | 4 | TO_BE_ACQUIRED_RESIDUAL_BLIND | False | False | p0_missing_data_source_plan_not_label_not_endpoint |
| NED_NEDD | https://ned.ipac.caltech.edu/ | 32 | 4 | TO_BE_ACQUIRED_RESIDUAL_BLIND | False | False | p0_missing_data_source_plan_not_label_not_endpoint |
| DustPedia | https://arxiv.org/abs/1708.05335 | 44 | 4 | TO_BE_ACQUIRED_RESIDUAL_BLIND | False | False | p0_missing_data_source_plan_not_label_not_endpoint |
| HI_SURVEYS | THINGS; LITTLE_THINGS; WALLABY; HALOGAS | 32 | 4 | TO_BE_ACQUIRED_RESIDUAL_BLIND | False | False | p0_missing_data_source_plan_not_label_not_endpoint |
| PHANGS | https://www.phangs.org/home/data | 28 | 4 | TO_BE_ACQUIRED_RESIDUAL_BLIND | False | False | p0_missing_data_source_plan_not_label_not_endpoint |

## Galaxy Summary

| galaxy | n_source_tasks | n_required_tasks | n_pending_tasks | accepted_label_output_allowed | endpoint_scores_computed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| NGC0100 | 13 | 8 | 13 | False | False | p0_missing_data_source_plan_not_label_not_endpoint |
| NGC0247 | 13 | 8 | 13 | False | False | p0_missing_data_source_plan_not_label_not_endpoint |
| NGC0300 | 13 | 6 | 13 | False | False | p0_missing_data_source_plan_not_label_not_endpoint |
| NGC6503 | 13 | 6 | 13 | False | False | p0_missing_data_source_plan_not_label_not_endpoint |

## Required Task Extract

| galaxy | review_field | acquisition_priority | required_source_families | source_task |
| --- | --- | --- | --- | --- |
| NGC0100 | present_day_morphology_label | P0_REQUIRED | S4G;NED_NEDD;DustPedia | record residual-blind catalog/image morphology support and provenance |
| NGC0100 | outer_disk_lsb_tail_evidence | P0_REQUIRED | S4G;DustPedia;HI_SURVEYS | check outer-disk, low-surface-brightness, truncation, tail, and gas-extent support |
| NGC0100 | hi_extent_or_asymmetry_evidence | P0_REQUIRED | HI_SURVEYS;NED_NEDD | look for THINGS/LITTLE_THINGS/WALLABY/HALOGAS availability and record gas extent or asymmetry evidence |
| NGC0100 | edge_projection_caveat | P0_REQUIRED_PROJECTION_CHECK | NED_NEDD;S4G;DustPedia | record inclination, distance/projection caveats, and edge-on decomposition support |
| NGC0100 | vertical_flare_warp_evidence | P0_REQUIRED_PROJECTION_CHECK | S4G;DustPedia;HI_SURVEYS | look for edge/thick disk, flare, warp, or extended gas-plane evidence |
| NGC0100 | review_confidence | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | score source agreement, source coverage, and caveat severity before endpoint scoring |
| NGC0100 | residual_blind_family_recommendation | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | make a residual-blind family recommendation only after source evidence is logged |
| NGC0100 | review_sources_used | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | record exact source list, access path, and notes |
| NGC0247 | present_day_morphology_label | P0_REQUIRED | S4G;NED_NEDD;DustPedia | record residual-blind catalog/image morphology support and provenance |
| NGC0247 | outer_disk_lsb_tail_evidence | P0_REQUIRED | S4G;DustPedia;HI_SURVEYS | check outer-disk, low-surface-brightness, truncation, tail, and gas-extent support |
| NGC0247 | hi_extent_or_asymmetry_evidence | P0_REQUIRED | HI_SURVEYS;NED_NEDD | look for THINGS/LITTLE_THINGS/WALLABY/HALOGAS availability and record gas extent or asymmetry evidence |
| NGC0247 | bar_m2_evidence | P0_REQUIRED_NONAXISYMMETRIC_CHECK | S4G;PHANGS | record bar component, m=2 morphology, and velocity-field support where available |
| NGC0247 | ring_resonance_evidence | P0_REQUIRED_NONAXISYMMETRIC_CHECK | S4G;PHANGS;DustPedia | record ring, resonance, or spiral-structure evidence without using residual peaks |
| NGC0247 | review_confidence | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | score source agreement, source coverage, and caveat severity before endpoint scoring |
| NGC0247 | residual_blind_family_recommendation | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | make a residual-blind family recommendation only after source evidence is logged |
| NGC0247 | review_sources_used | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | record exact source list, access path, and notes |
| NGC0300 | present_day_morphology_label | P0_REQUIRED | S4G;NED_NEDD;DustPedia | record residual-blind catalog/image morphology support and provenance |
| NGC0300 | outer_disk_lsb_tail_evidence | P0_REQUIRED | S4G;DustPedia;HI_SURVEYS | check outer-disk, low-surface-brightness, truncation, tail, and gas-extent support |
| NGC0300 | hi_extent_or_asymmetry_evidence | P0_REQUIRED | HI_SURVEYS;NED_NEDD | look for THINGS/LITTLE_THINGS/WALLABY/HALOGAS availability and record gas extent or asymmetry evidence |
| NGC0300 | review_confidence | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | score source agreement, source coverage, and caveat severity before endpoint scoring |
| NGC0300 | residual_blind_family_recommendation | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | make a residual-blind family recommendation only after source evidence is logged |
| NGC0300 | review_sources_used | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | record exact source list, access path, and notes |
| NGC6503 | present_day_morphology_label | P0_REQUIRED | S4G;NED_NEDD;DustPedia | record residual-blind catalog/image morphology support and provenance |
| NGC6503 | outer_disk_lsb_tail_evidence | P0_REQUIRED | S4G;DustPedia;HI_SURVEYS | check outer-disk, low-surface-brightness, truncation, tail, and gas-extent support |
| NGC6503 | hi_extent_or_asymmetry_evidence | P0_REQUIRED | HI_SURVEYS;NED_NEDD | look for THINGS/LITTLE_THINGS/WALLABY/HALOGAS availability and record gas extent or asymmetry evidence |
| NGC6503 | review_confidence | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | score source agreement, source coverage, and caveat severity before endpoint scoring |
| NGC6503 | residual_blind_family_recommendation | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | make a residual-blind family recommendation only after source evidence is logged |
| NGC6503 | review_sources_used | P0_REQUIRED | S4G;NED_NEDD;DustPedia;HI_SURVEYS;PHANGS | record exact source list, access path, and notes |

## Claim Boundary

This layer is upstream of the accepted-manifest audit. It must not use
endpoint residual gain, required-S_tau diagnostics, best-fit Tau Core
readout families, MOND/RAR/TGP comparison scores, or post-hoc family
switching. Successful source acquisition would still require independent
promotion and readiness gates before any endpoint scoring.

Claim boundary: `p0_missing_data_source_plan_not_label_not_endpoint`.
