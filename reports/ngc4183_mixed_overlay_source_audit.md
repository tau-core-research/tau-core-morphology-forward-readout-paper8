# NGC4183 Mixed-Overlay Source Audit

Status: `NGC4183_MIXED_OVERLAY_SOURCE_AUDIT_LOCAL_SOURCE_PRESENT_REVIEW_REQUIRED_NOT_FREEZE_READY`

This is a residual-blind source-acquisition/preflight audit, not an endpoint
score.  It checks whether NGC4183 has enough source-native morphology/readout
information to advance from the mixed-overlay future worklist toward a formula
freeze.

## Summary

| source_audit_status | galaxy | candidate_lane | candidate_readout | manifest_status_before_audit | n_sources | n_freeze_usable_numeric_fields | has_galaxy_specific_hi_source | has_outer_warp_context | has_projection_context | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary | next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4183_MIXED_OVERLAY_SOURCE_AUDIT_LOCAL_SOURCE_PRESENT_REVIEW_REQUIRED_NOT_FREEZE_READY | NGC4183 | L_mixed_overlay | K_expdisk_bar_core_projection_history_overlay_review | BLOCKED_REQUIRED_SOURCE_FIELDS_MISSING | 3 | 4 | True | True | True | False | False | ngc4183_mixed_overlay_source_audit_not_endpoint | independent_review_of_source_native_hi_fields_and_overlay_observable_sheet |

## Sources

| source_id | source_role | ngc4183_specific | source_status | usable_for_freeze |
| --- | --- | --- | --- | --- |
| SPARC_MASTER | rotation_curve_and_global_baryonic_metadata | True | SOURCE_NATIVE_ACCEPTED | True |
| VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | source_native_hi_orientation_projection_and_warp_context | True | GALAXY_SPECIFIC_SOURCE_PRESENT_REVIEW_REQUIRED | False |
| VANEYMEREN_2011_WHISP_LOPSIDEDNESS_CONTEXT | method_and_population_context_only | False | CONTEXT_ONLY_NOT_FREEZE_INPUT | False |

## Field Audit

| field_id | value | unit | source_id | field_status | freeze_usable | notes |
| --- | --- | --- | --- | --- | --- | --- |
| disk_scale_Rdisk_kpc | 2.79 | kpc | SPARC_MASTER | ACCEPTED_NUMERIC_RESIDUAL_BLIND | True | SPARC disk scale field; does not use vobs residuals. |
| RHI_kpc | 16.07 | kpc | SPARC_MASTER | ACCEPTED_NUMERIC_RESIDUAL_BLIND | True | SPARC H I radius is nonzero and can support a source-window denominator. |
| Vflat_km_s | 110.6 | km/s | SPARC_MASTER | ACCEPTED_NUMERIC_RESIDUAL_BLIND | True | Global velocity scale only; not a residual fit. |
| inclination_deg_sparc | 82.0 | deg | SPARC_MASTER | ACCEPTED_NUMERIC_EDGE_ON_CAVEATED | True | High inclination supports a projection/overlay caveat. |
| hi_position_angle_deg_source_native | 347.0 | deg | VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | SOURCE_PRESENT_REVIEW_REQUIRED | False | OCR block reports total H I map position angle; needs independent review before freezing. |
| hi_inclination_deg_source_native | 83.0 | deg | VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | SOURCE_PRESENT_REVIEW_REQUIRED | False | OCR block reports total H I map inclination; source-native but still review-gated. |
| hi_diameter_arcmin_source_native | 6.1 | arcmin | VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | SOURCE_PRESENT_REVIEW_REQUIRED | False | Potential direct support radius proxy; must be converted/reviewed before formula freeze. |
| outer_warp_context | slightly warped in the outer regions | context | VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | ACCEPTED_CONTEXT_CAVEATED | False | Supports mixed-overlay/projection review, but is not yet a numeric warp kernel. |
| edge_on_projection_context | optical-axis inclination likely too high | context | VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI | ACCEPTED_CONTEXT_CAVEATED | False | Supports projection/overlay lane, not standalone added-source scoring. |
| bar_core_history_overlay_observables | <NA> | mixed | PENDING | BLOCKED_REQUIRED_FIELD_MISSING | False | Needed by current NGC4183 mixed-overlay worklist before formula freeze. |

## Gates

| gate_id | gate_status | evidence | remaining_obligation |
| --- | --- | --- | --- |
| N4183_G1_RESIDUAL_BLIND_SOURCE_AUDIT | PASS | uses SPARC metadata and cached literature, not endpoint residuals | none for source-audit scope |
| N4183_G2_GALAXY_SPECIFIC_HI_SOURCE | PASS_REVIEW_REQUIRED | Verheijen & Sancisi 2001 NGC4183 H I block is locally cached | independent review of PA/inc/HI diameter and usable kernel inputs |
| N4183_G3_MIXED_OVERLAY_FREEZE_INPUTS | BLOCKED | bar/core/projection/history overlay observables remain missing | build galaxy-specific overlay observable sheet before formula freeze |
| N4183_G4_FORMULA_FREEZE | BLOCKED | source-native numeric overlay kernel is not frozen | freeze lane, carrier, kernel, amplitude rule after source review |

## Local H I Source Excerpt

`VERHEIJEN_SANCISI_2001_URSA_MAJOR_HI` contains a galaxy-specific NGC4183 block.
The OCR is usable for preflight but must be independently reviewed before any
numeric formula freeze:

>  /  / 1 12 / 02Aug93 / 12:10:47 / 43:58:35 / 1415.95 / 932 / 37.4 / 40 / 36-2700-72 / 11.8 17.2 / 2.5 / 127 / 4.15 / 8.30 / 5.93 /  / 2.97 / Contour levels for N4183 / Channel maps: /  =3.86 (K) /  =1.75 (K) / Cleaned continuum map: /  =1.51 (K) / Position-Velocity diagrams: /  =3.34 (K) / Raw continuum map: / M. A. W. Verheijen and R. Sancisi: The Ursa Major cluster of galaxies / Length of observation / (hours) / Date of observation / Field center, (1950) / Æ (1950) / Central frequency / (MHz) / (km s−1 ) / Vhel of central channel / Primary beam FWHM (arcmin) / Nr. of interferometers / Baselines (min-max-incr) / (m) / Synthesized beam ( Æ ) (arcsec) / Bandwidth / (MHz) / Number of channels / Channel separation / (km s−1 ) / Velocity resolution / (km s−1 ) / rms noise in one channel / (K) / K-mJy conversion, / equiv. of 1mJy/beam / (K) / Velocity fields: / 925.5 n 20 (km s−1 ) / Residual velocity field: / n 5 (km s−1 ) / Integrated HI map: / 1.06, 2.13, 3.19 / 4.26 ( 1021 atoms cm−2 ) /   /   /  / Results from WSRT data / From continuum map: / 21-cm flux density / central point source (mJy) / extended source (mJy) / From global profile: / Integrated HI-flux (Jy km s−1 ) / Hel. systemic velocity (km s−1 ) / HI profile width, 20% (km s−1 ) / 50% (km s−1 ) / From velocity field: / Hel. systemic velocity (km s−1 ) / Dynamical center, (1950) / Æ (1950) / From total HI map: / Geometric center, (1950) / Æ (1950) / Position angle / (deg) / Inclination angle / (deg) / Diameter of HI disk (arcmin) / <1.5 (3) / <5.8 (3) /  0.7 /  1.0 /  1.2 /  1.5 / 925.5  1.5 / 48.9 / 930.1 / 249.6 / 232.5 / 12:10:46.2 / 43:58:33 / 12:10:45.8 / 43:58:41 / 347 / 83 / 6.1 / Note: This galaxy is slightly warped in / the outer regions. The inclination derived from the optical axis 

## Verdict

NGC4183 is strengthened from a purely context-only mixed-overlay candidate to a
local-source-present candidate.  The source-native H I block supports an
edge-on/projection and slight-outer-warp review path.  It does not yet authorize
formula freeze or endpoint scoring because the mixed-overlay kernel observables
and coefficient rules are still not independently frozen.
