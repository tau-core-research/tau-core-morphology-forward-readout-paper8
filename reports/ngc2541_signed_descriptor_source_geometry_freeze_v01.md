# NGC2541 / UGC4284 signed-descriptor source freeze v01

| status | n_support_rings | basis_condition_number | maximum_decoder_error | chain_rule_max_error | reference_projection_ratio_min | reference_projection_ratio_max | endpoint_values_used | endpoint_scoring_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SOURCE_GEOMETRY_READY_TERMINAL_CALIBRATION_AND_UNTOUCHED_ENDPOINT_BLOCKED | 25 | 6.5726929 | 8.025154e-16 | 1.0521128e-10 | 0.81865323 | 1.0310746 | False | False |

The freeze uses only the radius and orientation columns of Jozsa (2007) Table 6 plus the source-published inner/outer ranges. Rotation velocity, SPARC residuals and baseline scores are not used.

The complete signed descriptor reconstructs the unit ring normals and passes `D_Dhat G_ref=P_R J_OS`. The latter is only a fixed-reference projection sensitivity. Physical scoring remains blocked until an untouched endpoint and its inclination-reduction provenance are frozen.
