# SDP.81 standard corridor descriptor v01

Status: `STANDARD_CORRIDOR_COMPARATOR_DERIVED_TAU_PARENT_DEPTH_OPEN`; checks: **7/7**.

The frozen smooth SIE+external-shear model supplies four q1 path records without reading a spectral or velocity endpoint. The standard descriptor contains relative Fermat potential, local lens Jacobian, signed magnification, singular values and parity.

The relative Fermat-potential span is `0.743341 arcsec^2`; the absolute magnification range is `3.730` to `17.887`. The centered three-feature path descriptor has rank `3`.

The maximum local lens-Jacobi singular value is `1.038708` and `1` path exceeds unit operator norm. Together with the two negative-parity paths and the different typed domain, this forbids identifying the standard lens Jacobian directly with the parent loss contraction.

This closes the standard path-comparator object only. Fermat potential is not identified with Tau parent depth. The conditional FULLCONE map from an occupied causal-body Hessian to transfer is available, but PATHLIFT-C1 still requires fibre-basicness or four occupied common-parent lift keys. Covariance, observer resolution and calibration also remain frozen-source requirements before an endpoint.
