# PHANGS post-open resolved-morphology diagnostic v01

Status: `NEGATIVE_RESULT_PRESERVED_POSTOPEN_DIAGNOSTIC`.

The original four-galaxy endpoint remains failed and closed because every body missed the frozen 12-sector covariance gate. This retrospective diagnostic substitutes diagonal formal covariance with fixed 5, 10 and 20 km/s error floors; it cannot repair the endpoint.

## Sensitivity summary

| error_floor_km_s | q_primary | dof_primary | p_primary_formal | individual_p_below_0_05 | q_radial_reversal | primary_below_reversal_global | primary_below_reversal_count | radial_control_pass | q_phase_rotation | primary_below_phase_global | primary_below_phase_count | phase_control_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 2148.43 | 48 | 0 | 4 | 2152.91 | True | 2 | False | 2156.03 | True | 1 | False |
| 10 | 745.847 | 48 | 6.36413e-126 | 4 | 758.408 | True | 2 | False | 711.969 | False | 1 | False |
| 20 | 211.865 | 48 | 1.82865e-22 | 2 | 216.585 | True | 2 | False | 199.112 | False | 1 | False |

The formal body-orthogonal contrast is nonzero at every floor, but the matched resolved morphology does not pass both radial-reversal and phase-rotation specificity controls. Ordinary tracer dynamics, incomplete body description, spatial covariance and incomplete angular coverage remain stronger explanations.
