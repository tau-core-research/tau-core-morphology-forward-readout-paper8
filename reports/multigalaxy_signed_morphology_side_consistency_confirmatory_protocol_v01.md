# Multigalaxy signed-morphology side-consistency confirmatory protocol v01

Status: `SOURCE_ONLY_CONFIRMATORY_PROTOCOL_FROZEN_ENDPOINTS_NOT_ACQUIRED`.

The NGC2541 exercise showed that a small favorable ring statistic can reverse
under source-relevant centre choices and can be exaggerated by unequal pixel
footprints, sub-beam cells, correlated rings, and an unconverged coordinate
solve. NGC2541 is therefore a development object and is excluded from the
confirmatory population. NGC3198 is also excluded because its diagnostic and
replay scores were already opened, and NGC5055 is excluded because it belonged
to the Paper 8 SPARC training population.

A checksum-verified, endpoint-blind audit of the 24-object HALOGAS DR1 source
manifest leaves eight moderate-inclination candidates after those prior
exposures and the current edge-on exclusion are applied: NGC0672, NGC0925,
NGC0949, NGC4062, NGC4258, NGC4274, NGC4414, and NGC4448. HALOGAS alone is
therefore four galaxies short of the frozen minimum of 12. NGC0925 is the
first source-acquisition target because a primary THINGS analysis publishes
its centre, mean geometry, and an adopted radial inclination/position-angle
curve. The source JPEG has now been directly and reproducibly digitized into
93 three-arcsec rings. The raster sensitivity envelope is frozen separately
from the still-missing physical orientation uncertainty and covariance, so no
HALOGAS endpoint pixels may yet be opened.

The frozen inference unit is one galaxy. For candidate geometry `a`, the
side-consistency loss is

```text
e_g,r^(a) = |vhat_+,g,r^(a) - vhat_-,g,r^(a)|
L_g^(a)   = sum_r w_g,r e_g,r^(a).
```

All geometries use the same finite sky-pixel intersection and covariance-aware,
source-frozen radial weights. The two primary galaxy-level gains are

```text
A_g = L_g^(fixed) - L_g^(morphology)
D_g = mean_k[L_g^(wrong_family_k) - L_g^(morphology)].
```

Thus `A_g > 0` tests whether the signed morphology improves the fixed standard
geometry, while `D_g > 0` tests whether any gain is specific to the frozen
morphology rather than generic geometric flexibility.

The wrong-family controls are radial reversal, tangent mirror, a `pi/2`
position-angle rotation, and a donor morphology profile selected only through
preregistered support matching. Centre choices, orientation uncertainties,
beam-block covariance, solver convergence, radial zones, and moment-1 or
extraplanar-gas limitations are mandatory nuisance outputs.

Confirmation requires at least 12 previously unopened eligible galaxies,
equal galaxy weights, exact shared-sign permutations, max-T adjusted
`p_A <= 0.01` and `p_D <= 0.01`, positive medians, at least 60% positive
galaxy-level gains for both metrics, and positive leave-one-galaxy-out means.
Failure of any eligibility or nuisance condition blocks promotion.

Even a pass would establish only a predeclared population-level
morphology/readout calibration signal. It would not derive or select a physical
`q_R`, prove the Tau parent morphology, establish Nature occupation, or replace
dark matter.
