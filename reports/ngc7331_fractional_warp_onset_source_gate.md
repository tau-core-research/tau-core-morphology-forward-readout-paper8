# NGC7331 Fractional Warp-Onset Source Gate

This source-only gate tightens the NGC7331 outer-warp caveat without
changing the already scored V1 mixed endpoint. It records a source
fractional onset statement and an approximate kpc conversion, but any
formula update is replay/holdout-only.

## Summary

| galaxy | source_gate_status | previous_outer_warp_numeric_onset_available | fractional_warp_onset_available | approx_warp_onset_arcmin | approx_warp_onset_kpc | approx_warp_onset_over_Rdisk | approx_warp_onset_over_RHI | v1_broad_window_inner_kpc | v1_broad_window_outer_kpc | candidate_v2_window_inner_kpc | candidate_v2_window_outer_kpc | formula_update_allowed_for_current_endpoint | replay_or_holdout_required | uses_vobs_or_residual_in_construction | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | FRACTIONAL_WARP_ONSET_SOURCE_READY_REPLAY_REQUIRED | False | True | 3.375 | 14.4317 | 2.87484 | 0.534309 | 5.02 | 27.01 | 14.4317 | 27.01 | False | True | False | False | ngc7331_fractional_warp_onset_source_gate_not_endpoint |

## Source Fields

| field_id | observable | value | unit | status | source | source_line_refs | role | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N7331_FW1_HOLMBERG_SIZE | holmberg_major_axis_size | 13.5 | arcmin | ACCEPTED_SOURCE_NUMERIC_FIELD | https://ned.ipac.caltech.edu/level5/March05/Bosma/Bosma4_7.html | lines 5-6 | sets Holmberg-system angular major-axis size for fractional onset conversion | False | False | ngc7331_fractional_warp_onset_source_gate_not_endpoint |
| N7331_FW2_FRACTIONAL_WARP_ONSET | warp_onset_fraction_of_holmberg_radius | 0.5 | dimensionless | ACCEPTED_SOURCE_FRACTIONAL_FIELD | https://ned.ipac.caltech.edu/level5/March05/Bosma/Bosma4_7.html | lines 80-84 | source-anchors the outer-warp onset fraction without using rotation residuals | False | False | ngc7331_fractional_warp_onset_source_gate_not_endpoint |
| N7331_FW3_APPROX_ONSET_KPC | approx_warp_onset_radius | 14.4317 | kpc | DERIVED_FROM_BOSMA_FRACTION_AND_SPARC_DISTANCE | Bosma Holmberg fraction + SPARC distance | Bosma lines 5-6 and 80-84; SPARC D_Mpc | candidate V2 outer-window inner radius; not applied to the already scored V1 endpoint | False | False | ngc7331_fractional_warp_onset_source_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | N7331_FW_G1_SOURCE_STATEMENT_PRESENT | PASS | Bosma/NED states NGC7331 warp starts at 0.5 times the Holmberg radius | none at source-statement level | False | False | ngc7331_fractional_warp_onset_source_gate_not_endpoint |
| NGC7331 | N7331_FW_G2_KPC_CONVERSION_AVAILABLE | PASS_CAVEATED | 0.5*R_Ho=3.375 arcmin; SPARC D=14.700 Mpc gives R_onset=14.432 kpc | conversion depends on pairing the Bosma Holmberg size with the SPARC distance | False | False | ngc7331_fractional_warp_onset_source_gate_not_endpoint |
| NGC7331 | N7331_FW_G3_ENDPOINT_PROTOCOL_BOUNDARY | BLOCKED_REPLAY_REQUIRED | accepted NGC7331 V1 endpoint was already scored with broad Rdisk-to-RHI window | use this onset only in a predeclared V2 replay/holdout or future endpoint | False | False | ngc7331_fractional_warp_onset_source_gate_not_endpoint |

## Claim Boundary

This gate is not an endpoint score and not a post-hoc improvement of the
accepted NGC7331 V1 result. The candidate V2 window may be used only in
a predeclared replay/holdout lane or a future source-selected case.
