# NGC2541 HALOGAS calibration nuisance audit v02

Status: `POST_OPEN_DESCRIPTIVE_DIAGNOSTIC_CALIBRATION_UNSTABLE`. All rows use the common fixed/variable sky-pixel intersection.

| centre_case | iterations | n_common_eligible_rings | fixed_mean_absolute_side_difference_kms | variable_mean_absolute_side_difference_kms | delta_mean_variable_minus_fixed_kms | fraction_common_rings_improved | median_next_step_arcsec | p95_next_step_arcsec |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NED | 4 | 21 | 11.769345 | 11.500848 | -0.268496 | 0.571429 | 0.265590 | 35.361137 |
| NED | 20 | 21 | 11.756661 | 11.537147 | -0.219514 | 0.619048 | 0.000000 | 29.671005 |
| JOZSA_FITTED | 4 | 21 | 5.616383 | 5.949320 | 0.332937 | 0.285714 | 0.265222 | 36.253374 |
| JOZSA_FITTED | 20 | 21 | 5.595662 | 5.975555 | 0.379892 | 0.285714 | 0.000000 | 27.593808 |
| NED_E_PLUS_4_ARCSEC | 4 | 21 | 10.028655 | 10.100038 | 0.071384 | 0.380952 | 0.269562 | 35.506555 |
| NED_E_PLUS_4_ARCSEC | 20 | 21 | 10.016134 | 10.104973 | 0.088839 | 0.333333 | 0.000000 | 28.579321 |
| NED_E_MINUS_4_ARCSEC | 4 | 21 | 13.027880 | 12.731896 | -0.295984 | 0.523810 | 0.263590 | 35.193039 |
| NED_E_MINUS_4_ARCSEC | 20 | 21 | 13.041780 | 12.815978 | -0.225801 | 0.476190 | 0.000000 | 29.666488 |
| NED_N_PLUS_4_ARCSEC | 4 | 21 | 13.192453 | 13.203862 | 0.011409 | 0.428571 | 0.265995 | 35.365830 |
| NED_N_PLUS_4_ARCSEC | 20 | 21 | 13.230942 | 13.217143 | -0.013799 | 0.428571 | 0.000000 | 29.673144 |
| NED_N_MINUS_4_ARCSEC | 4 | 21 | 10.074153 | 10.004001 | -0.070152 | 0.476190 | 0.263162 | 35.307961 |
| NED_N_MINUS_4_ARCSEC | 20 | 21 | 10.098384 | 10.035037 | -0.063346 | 0.476190 | 0.000000 | 28.698861 |

The NED-centred directional change is not stable under the source-published Józsa fitted kinematic centre or under four-arcsecond cardinal centre shifts. The four-iteration solver also lacks a demonstrated convergence tolerance.

The HR beam contains `17.393402` map pixels, whereas the v01 gate accepted only `8` pixels (`0.459945` beams) per side. Some source-ring spacings are below the synthesized beam, so pixel and ring independence must not be assumed.

Published inclination/PA uncertainties and their covariance are not propagated. The moment-1 terminal is intensity-weighted and remains vulnerable to warp overlap and extraplanar-gas bias.

Post-open standard-calibration diagnostic only. The sign of the small mean change is unstable under source-relevant centre choices; no Tau q_R, physical calibration law, Nature occupation, or dark-matter-replacement evidence follows.
