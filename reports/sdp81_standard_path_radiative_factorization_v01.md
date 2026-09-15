# SDP.81 standard path/radiative factorization v01

Status: `STANDARD_PATH_FUNCTIONAL_DERIVED_RADIATIVE_MIXED_JET_OPEN`. Checks: `8/8`. No spectral endpoint or sealed CO(10-9) header/pixels were read.

For source coefficients $S_{nk}(Z)$ and the ordinary smooth-lens plus aperture functional $L_{in}$,

$$F_{ik}(Z)=\sum_n L_{in}S_{nk}(Z),\qquad [D_Z\Phi_i]_{ka}=\sum_n L_{in}[D_ZS]_{nka}. $$

The normalized four-by-49 path matrix has rank `4`, leaving a `45`-dimensional spatial null per channel. In the separable control the maximum pathwise centered-log Jacobian spread is `4.371e-16`; common path gain cancels exactly. In the same-lens spatial--spectral countermodel it is `2.869e-01` without parent loss.

Therefore a nontrivial multipath spectral difference is not by itself evidence for parent attenuation. The remaining physical object is a source-owned CO(10-9) radiative mixed jet $D_ZS$, followed by the frozen line-specific beam/spectral response and covariance.
