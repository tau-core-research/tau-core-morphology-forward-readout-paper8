# NGC3893 Replication Eligibility Audit v0.1

**Status:** `NGC3893_DISTURBED_CONTROL_PRIMARY_REPLICATION_BLOCKED`

NGC3893 was reached as residual-blind source rank 3. The dedicated source,
however, describes the NGC3893/3896 interaction, detected non-circular
motions, a common H I envelope/connecting arm, and a rotation-curve geometry
chosen to make the inner curve symmetric and minimize side scatter. Those are
useful properties for a disturbed-galaxy control, but they block an independent
primary odd-channel replication.

| gate | pass |
| --- | --- |
| source_only_rank_frozen | True |
| both_ghasp_halpha_sides | True |
| whisp_graphical_source_available | True |
| low_disturbance_primary_replication | False |
| independent_machine_readable_hi_radial_sides_acquired | True |
| side_curve_not_symmetry_targeted | False |

The WHISP graphical overview is cached. The searched WHISP lopsidedness source
package does not contain UGC6778/NGC3893. A later source audit found that the
checksum-frozen Verheijen--Sancisi Ursa Major table contains machine-readable
NGC3893 approaching/receding H I rows. This removes the data-availability
blocker but not the disturbed-control classification.

No channel statistic was run, so this object is neither a positive detection
nor a third negative channel test. It remains available as a predeclared
disturbed/non-circular-motion control. The next clean-candidate audit is
UGC08490 (NGC5204).
