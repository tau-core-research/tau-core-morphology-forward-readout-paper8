# Morphology Information Gain Source Expansion

This all-sample source expansion maps residual-blind source coverage for
the L2/L4 morphology-information-gain layers. It does not classify
galaxies, does not promote accepted labels, and does not compute endpoint
scores.

## Full-Sample Coverage

| coverage_field | n_galaxies | fraction | claim_boundary |
| --- | --- | --- | --- |
| sparc_hi_ready | 171 | 0.977143 | source_expansion_not_label_not_endpoint |
| s4g_scale_ready | 75 | 0.428571 | source_expansion_not_label_not_endpoint |
| s4g_bar_ready | 19 | 0.108571 | source_expansion_not_label_not_endpoint |
| s4g_compact_component_ready | 35 | 0.2 | source_expansion_not_label_not_endpoint |
| dustpedia_any_match | 31 | 0.177143 | source_expansion_not_label_not_endpoint |
| dustpedia_hi_match | 31 | 0.177143 | source_expansion_not_label_not_endpoint |
| dustpedia_physical_match | 29 | 0.165714 | source_expansion_not_label_not_endpoint |
| dustpedia_dust_profile_match | 31 | 0.177143 | source_expansion_not_label_not_endpoint |
| phangs_sample_match | 2 | 0.0114286 | source_expansion_not_label_not_endpoint |
| phangs_muse_ready | 0 | 0 | source_expansion_not_label_not_endpoint |
| phangs_alma_ready | 2 | 0.0114286 | source_expansion_not_label_not_endpoint |
| q_tail_candidate | 172 | 0.982857 | source_expansion_not_label_not_endpoint |
| q_expdisk_scale_candidate | 75 | 0.428571 | source_expansion_not_label_not_endpoint |
| q_bar_candidate | 19 | 0.108571 | source_expansion_not_label_not_endpoint |
| q_compact_candidate | 48 | 0.274286 | source_expansion_not_label_not_endpoint |
| q_memory_candidate | 172 | 0.982857 | source_expansion_not_label_not_endpoint |
| l4_velocity_field_candidate | 0 | 0 | source_expansion_not_label_not_endpoint |

## Holdout Coverage

| coverage_field | n_galaxies | fraction | claim_boundary |
| --- | --- | --- | --- |
| sparc_hi_ready | 43 | 0.977273 | source_expansion_not_label_not_endpoint |
| s4g_scale_ready | 21 | 0.477273 | source_expansion_not_label_not_endpoint |
| s4g_bar_ready | 6 | 0.136364 | source_expansion_not_label_not_endpoint |
| s4g_compact_component_ready | 7 | 0.159091 | source_expansion_not_label_not_endpoint |
| dustpedia_any_match | 10 | 0.227273 | source_expansion_not_label_not_endpoint |
| dustpedia_hi_match | 10 | 0.227273 | source_expansion_not_label_not_endpoint |
| dustpedia_physical_match | 9 | 0.204545 | source_expansion_not_label_not_endpoint |
| dustpedia_dust_profile_match | 10 | 0.227273 | source_expansion_not_label_not_endpoint |
| phangs_sample_match | 0 | 0 | source_expansion_not_label_not_endpoint |
| phangs_muse_ready | 0 | 0 | source_expansion_not_label_not_endpoint |
| phangs_alma_ready | 0 | 0 | source_expansion_not_label_not_endpoint |
| q_tail_candidate | 44 | 1 | source_expansion_not_label_not_endpoint |
| q_expdisk_scale_candidate | 21 | 0.477273 | source_expansion_not_label_not_endpoint |
| q_bar_candidate | 6 | 0.136364 | source_expansion_not_label_not_endpoint |
| q_compact_candidate | 14 | 0.318182 | source_expansion_not_label_not_endpoint |
| q_memory_candidate | 44 | 1 | source_expansion_not_label_not_endpoint |
| l4_velocity_field_candidate | 0 | 0 | source_expansion_not_label_not_endpoint |

## Claim Boundary

These are source candidates only. L2 readout-state weights still require
accepted morphology-memory, HI/tail, compact/core, bar, thickness/flare,
and normalization rules before endpoint use.
