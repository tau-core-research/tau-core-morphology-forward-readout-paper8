# Rotation-Inferred Morphology Diagnostic

This inverse diagnostic asks which Tau Core readout family is preferred by
the rotation-curve score table. It intentionally violates the residual-blind
direction required for the main Paper 8 endpoint, so it is a hypothesis
generator only.
This inverse diagnostic is a hypothesis generator only.

## Verdict

Rotation-inferred family matches the predeclared proxy family in 0.354 of rows.
For the 13 externally supported exponential-disk rows, it matches the external label in 0.308 of rows.

This is useful for model development and subtype discovery, but it must not
be used as accepted morphology evidence.

## Inferred Family Counts

| rotation_inferred_family | n_galaxies |
| --- | --- |
| K_compact_finite | 21 |
| K_exponential_disk | 71 |
| K_scale_tail_spiral | 63 |
| K_thick_flared | 20 |

## Predeclared vs Rotation-Inferred Summary

| predeclared_formula_family | rotation_inferred_family | n_galaxies | n_matches_predeclared | median_margin |
| --- | --- | --- | --- | --- |
| K_compact_finite | K_compact_finite | 14 | 14 | 3.2431763237671145 |
| K_compact_finite | K_exponential_disk | 12 | 0 | 0.5038156240544343 |
| K_compact_finite | K_scale_tail_spiral | 3 | 0 | 0.05422678241290235 |
| K_exponential_disk | K_compact_finite | 2 | 0 | 3.647914266765147 |
| K_exponential_disk | K_exponential_disk | 10 | 10 | 1.0435748431508083 |
| K_exponential_disk | K_scale_tail_spiral | 16 | 0 | 2.9420036612747635 |
| K_exponential_disk | K_thick_flared | 4 | 0 | 0.2081726057966975 |
| K_scale_tail_spiral | K_compact_finite | 2 | 0 | 2.6088141967343352 |
| K_scale_tail_spiral | K_exponential_disk | 32 | 0 | 1.301843198115415 |
| K_scale_tail_spiral | K_scale_tail_spiral | 34 | 34 | 3.354007787117899 |
| K_scale_tail_spiral | K_thick_flared | 12 | 0 | 0.4203332293829978 |
| K_thick_flared | K_compact_finite | 3 | 0 | 4.317158010285873 |
| K_thick_flared | K_exponential_disk | 17 | 0 | 0.9879766843570224 |
| K_thick_flared | K_scale_tail_spiral | 10 | 0 | 1.418124146473049 |
| K_thick_flared | K_thick_flared | 4 | 4 | 0.18761572192056208 |

## External Exponential-Disk Rows

| external_family_label | external_family_label_status | rotation_inferred_family | n_galaxies | n_matches_external | median_margin |
| --- | --- | --- | --- | --- | --- |
| K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR | K_exponential_disk | 1 | 1 | 1.9894933497187406 |
| K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR | K_scale_tail_spiral | 1 | 0 | 0.7656179906500422 |
| K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_BAR | K_thick_flared | 1 | 0 | 0.2532895720555812 |
| K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | K_exponential_disk | 2 | 2 | 1.3478018493848438 |
| K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | K_scale_tail_spiral | 1 | 0 | 1.0026032060994714 |
| K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_CAVEATED_EDGEON | K_thick_flared | 1 | 0 | 0.36399102976518627 |
| K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | K_exponential_disk | 1 | 1 | 0.37842525123867077 |
| K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | K_scale_tail_spiral | 4 | 0 | 2.526401404895473 |
| K_exponential_disk | ACCEPTED_EXTERNAL_EXPONENTIAL_DISK_LABEL_STRONG | K_thick_flared | 1 | 0 | 0.03137946343992226 |

## Claim Boundary

This diagnostic is not residual-blind, not an endpoint score, and not a
validation of Tau Core. It can suggest morphology-subtype splits to test
later with external labels.
It must not be used as accepted morphology evidence.
