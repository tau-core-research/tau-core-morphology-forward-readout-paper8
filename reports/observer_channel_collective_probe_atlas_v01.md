# Observer-Channel Collective Probe Atlas v0.1

**Status:** `COLLECTIVE_PROBE_ATLAS_BUILT_NO_INJECTIVE_A_MATRIX`

## Verdict

The atlas separates physical probe candidates, body-coordinate inputs,
pipeline/nuisance controls, and cross-domain architecture candidates. No row
yet supplies a constructed physical `A_p`, so `ker A`, `sigma_min(A)`, and
collective injectivity cannot be evaluated.

The first `OC-P02` angular statistic is frozen and evaluated on source-ranked
NGC3726, then prospectively replicated with HR/LR HALOGAS maps on NGC4559.
Neither galaxy rejects zero odd contrast, while the two NGC4559 resolutions
agree internally. Source-ranked NGC3893 is blocked as a primary replication
because its dedicated source reports interaction, non-circular motions, and a
symmetry-targeted curve construction; it remains a disturbed control and does
not count as a third negative test. The immediate route continues with the
clean-candidate audit of UGC08490, without retuning the statistic. It is
followed by `OC-P06` (same-pixel
multi-line centroid/width) and the source-blind path map needed to promote
`OC-P01` beyond a single-galaxy diagnostic.

## Atlas

| probe_id | probe_family | operator_role | readiness | priority |
| --- | --- | --- | --- | --- |
| OC-P01 | hi_side_parity | physical_channel_candidate | DIAGNOSTIC_READY_SINGLE_GALAXY_NOT_A_MATRIX_ROW | 1 |
| OC-P02 | hi_halpha_cospatial_kinematics | physical_tracer_probe_candidate | TWO_SOURCE_RANKED_TRACER_TESTS_ZERO_NULL_NOT_REJECTED | 1 |
| OC-P03 | co_halpha_cospatial_kinematics | physical_tracer_probe_candidate | SOURCE_EXISTS_DIRECT_SPARC_PILOT_BLOCKED | 2 |
| OC-P04 | gas_stellar_kinematics | physical_tracer_probe_candidate | PRIORITY_2_CROSSMATCH_AND_MODEL_AUDIT | 2 |
| OC-P05 | hi_imaging_weight_replication | pipeline_control_not_physical_probe | CONTROL_READY_DO_NOT_COUNT_TOWARD_INJECTIVITY | 0 |
| OC-P06 | spectral_centroid_width_multiline | physical_channel_probe_candidate | PRIORITY_1_MULTILINE_PACKET_REQUIRED | 1 |
| OC-P07 | morphology_onset_body_coordinate | body_coordinate_control_not_channel_probe | BODY_CALIBRATION_CONTROL_DO_NOT_COUNT_TOWARD_A_INJECTIVITY | 0 |
| OC-P08 | dynamics_weak_lensing | cross_readout_probe_candidate | THEORY_HIGH_VALUE_EMPIRICALLY_BLOCKED | 3 |
| OC-P09 | multipath_time_delay | architecture_analogue_not_current_galaxy_probe | ARCHITECTURE_CONTROL_NOT_PAPER8_PROBE | 3 |
| OC-P10 | strong_lensing_stellar_kinematics | cross_readout_probe_candidate | CROSS_DOMAIN_METHOD_CANDIDATE_NOT_PAPER8_ROW | 3 |
| OC-P11 | distance_inclination_systematics | nuisance_control_not_physical_probe | CONTROL_REQUIRED_DO_NOT_COUNT_TOWARD_INJECTIVITY | 0 |
| OC-P12 | proper_motion_transverse_kinematics | physical_kinematic_probe_candidate | LONG_HORIZON_CANDIDATE | 4 |

## Concrete Coverage Audit

```text
PHANGS-ALMA public sample x SPARC overlap: ['NGC2903', 'NGC3521']
PHANGS-MUSE flag inside that overlap:       []
GHASP VI+VII alias-aware x SPARC overlap:    26
GHASP overlaps with both Halpha sides:       25
Top residual-blind source candidate:         NGC3726
NGC3726 H I and Halpha two-side support:      True
NGC3726 odd-contrast zero-null p:              0.1489
NGC3726 observer channel detected:             False
NGC4559 HALOGAS moment products acquired:      4
NGC4559 HALOGAS pixels opened:                  False
NGC4559 HR/LR zero-null p:                      0.1639 / 0.1362
NGC4559 replication positive:                   False
NGC3893 primary replication eligible:           False
NGC3893 role:                                    DISTURBED_CONVENTIONAL_ASYMMETRY_CONTROL_NOT_PRIMARY_CHANNEL_REPLICATION
Next clean source candidate:                     UGC08490
UGC06787 WHISP graphical H I acquired:      True
UGC06787 formal WCS ready:                   False
```

The current local tables therefore do not provide an immediate PHANGS
CO-Halpha-SPARC pilot. NGC2903 and NGC3521 are the two ALMA/SPARC overlaps,
but neither carries the MUSE flag in the frozen public sample table.

## Rules

```text
natural vs robust weighting is a pipeline replication, not a new physical row;
morphology onset is a body-coordinate input, not a channel row;
distance/inclination variations enter the uncertainty N, not positive rank;
different galaxies may be stacked only after common-parent transport;
lensing/time-delay systems constrain architecture but are not SPARC rows;
no endpoint residual may select the tracer, radial support, sign, or weighting.
```

## Claim Boundary

This is a source-backed acquisition and identifiability worklist. It does not
construct the physical probe matrix, prove `ker A=0`, estimate
`sigma_min(A)`, detect an observer-time channel, or validate Tau Core.
