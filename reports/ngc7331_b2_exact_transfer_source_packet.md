# NGC7331 B2 Exact Transfer Source Packet

This packet turns the NGC7331 exact-transfer worklist into concrete
residual-blind measurement and review templates. It does not fill the
measurements, freeze a formula, or score the rotation curve.

## Requirements

| galaxy | requirement_id | required_b2_field | required_status | source_class | acceptance_rule | blocks | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_B2_REQ_Q_WARP | q_warp | accepted_numeric_or_bounded_dimensionless_source_strength | source-native H I warp map or literature warp amplitude/asymmetry | q_warp must be fixed from residual-blind outer-warp geometry; allowed range is dimensionless and bounded before formula freeze | exact B2 source-load freeze | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_B2_REQ_SIGMA_WARP | sigma_warp | accepted_sign_or_orientation_convention | orientation/readout geometry, side convention, and added-readout vs attenuation review | sigma_warp must be frozen from source-side geometry without using endpoint residuals or baseline comparison | exact B2 source-load freeze | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_B2_REQ_EPSILON_CROSS | epsilon_cross_inputs | accepted_bound_or_explicit_uncertainty_packet | side asymmetry, orientation mismatch, history/context, and locality observables | cross-term inputs must either close a residual-blind bound or be carried as an explicit uncertainty interval | exact B2 source-load freeze or population-transfer claim | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |

## Measurement Templates

| galaxy | template_id | required_b2_field | measurement_field | unit | fill_rule | accepted_value | source_citation_or_cache | review_status | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_Q1_OUTER_WARP_EXTENT | q_warp | outer_warp_extent_or_amplitude | arcsec_or_kpc_or_dimensionless_ratio | measure source-native outer warp displacement, extent, or amplitude | <NA> | <NA> | MEASUREMENT_PENDING | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_Q2_LOCAL_DISK_REFERENCE | q_warp | local_disk_reference_extent | same_as_outer_warp_extent | use the same source frame as the outer-warp measurement | <NA> | <NA> | MEASUREMENT_PENDING | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_Q3_SIDE_WEIGHT | q_warp | side_weight_or_reliability | dimensionless | assign residual-blind side/panel reliability from source quality | <NA> | <NA> | MEASUREMENT_PENDING | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_S1_SIGN_CONVENTION | sigma_warp | added_readout_or_attenuation | sign_or_enum | freeze whether NGC7331 uses added-readout B2 sign or attenuation sign | <NA> | <NA> | MEASUREMENT_PENDING | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_S2_ORIENTATION_CONVENTION | sigma_warp | orientation_side_convention | text_plus_optional_angle | record which side/axis convention defines the sign | <NA> | <NA> | MEASUREMENT_PENDING | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_E1_ORIENTATION_MISMATCH | epsilon_cross_inputs | orientation_mismatch_bound | dimensionless_or_angle | bound source-side misalignment between ordinary disk and warp/readout layer | <NA> | <NA> | MEASUREMENT_PENDING | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_E2_SIDE_ASYMMETRY | epsilon_cross_inputs | side_asymmetry_bound | dimensionless | bound asymmetry between sides without rotation residuals | <NA> | <NA> | MEASUREMENT_PENDING | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_E3_HISTORY_CONTEXT | epsilon_cross_inputs | history_or_memory_context | categorical_or_dimensionless_proxy | record interaction/history context only if source-supported | <NA> | <NA> | MEASUREMENT_PENDING | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_E4_LOCALITY_ONSET_COUPLING | epsilon_cross_inputs | locality_onset_coupling_bound | dimensionless | bound whether cross terms remain local to the warp/onset lane | <NA> | <NA> | MEASUREMENT_PENDING | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_B2SP1_PACKET_SCOPE | PASS | q_warp, sigma_warp, and epsilon_cross source requirements are declared | none at packet-scope level | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_B2SP2_XW_VFLAT_CONTEXT | PASS_CONTEXT | upgrade gate has x_w and Vflat available; preview=30520.275307 km^2/s^2 | do not treat preview as formula or endpoint score | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_B2SP3_Q_WARP_TEMPLATE | BLOCKED_MEASUREMENT_PENDING | q_warp templates exist but no accepted measurement is filled | measure or bound q_warp from residual-blind H I/warp source | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_B2SP4_SIGMA_TEMPLATE | BLOCKED_REVIEW_PENDING | sigma_warp sign/orientation templates exist but convention is not frozen | freeze sign from source-side geometry | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_B2SP5_EPSILON_TEMPLATE | BLOCKED_MEASUREMENT_PENDING | epsilon_cross templates exist but no bound is filled | fill orientation, asymmetry, history, and locality inputs | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |
| NGC7331 | N7331_B2SP6_ENDPOINT_BLINDNESS | PASS | packet defines source templates only and reads no vobs/residual columns | keep endpoint scoring in a later separate script after formula freeze | False | False | ngc7331_b2_exact_transfer_source_packet_not_endpoint |

## Summary

| galaxy | source_packet_status | n_requirements | n_templates | n_gates | n_pass_like | n_blocked | q_warp_packet_ready | sigma_warp_packet_ready | epsilon_cross_packet_ready | q_warp_measurement_accepted | sigma_warp_frozen | epsilon_cross_bound_closed | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | population_claim_allowed | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | NGC7331_EXACT_TRANSFER_SOURCE_PACKET_BUILT_MEASUREMENTS_PENDING | 3 | 9 | 6 | 3 | 3 | True | True | True | False | False | False | False | False | False | False | fill and independently review q_warp, sigma_warp, and epsilon_cross source templates before exact B2 formula freeze | ngc7331_b2_exact_transfer_source_packet_not_endpoint |

## Interpretation

NGC7331 now has a concrete exact-transfer source-acquisition packet.
The packet makes the next work narrow: fill q_warp, freeze sigma_warp,
and close or explicitly carry epsilon_cross before any B2 formula freeze.
The existing x_w Vflat^2 scale remains a dimensional preview only.
