# SDP.81 smooth lens-operator geometry validation

Status: `SMOOTH_OPERATOR_MULTIPLICITY_AND_CONFIGURATION_REPRODUCED_G_WCS_OPEN`

The frozen Inoue best-fit SIE+external-shear model was translated to lenstronomy with `phi_e=90 deg + theta_e` and `phi_gamma=theta_gamma`. It produces multiplicities `{'q1': 4, 'd1': 2, 'd2': 2}`, reproducing the published q1 quadruple and d1/d2 doubles. The predicted q1 positions also reproduce the published A/B/C/D image configuration. This validates the relative smooth-lens geometry, not its absolute ALMA pixel registration. Image G still requires an independently anchored WCS centroid before ray tracing.
