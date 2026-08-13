# Same-body joint H I/H-alpha conditional information v01

Status: `SHARED_SOURCE_PRECISION_GAIN_MEASURED_DISTINCT_TRACER_MODE_NOT_DETECTED`

The two tracers are treated as noisy views of one shared radial side-odd source. The full block covariance uses persisted tracer covariance matrices and an unfitted cross-noise sensitivity.

At the nominal `30 km/s`, `rho=0` convention, mean joint information is `13.113` bits per profile. H I adds `1.408` bits beyond H-alpha; H-alpha adds `4.392` bits beyond H I. Mean redundant information is `7.313` bits. Both increments remain positive over all declared source-scale and cross-noise sensitivities.

Positive conditional information here is a precision gain: both declared tracer Jacobians are identities on the same source, so stacked rank does not grow. The covariance-aware contrast tests also do not reject the shared-source innovation null. No distinct tracer mode, gas-physics, geometry, path, observer-time, or quantum-access origin is identified.
