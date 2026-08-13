# NGC3726 H I-Halpha Angular Transport Freeze v0.1

**Status:** `NGC3726_HI_HALPHA_ANGULAR_TRANSPORT_AND_ODD_CONTRAST_FROZEN`

Six H I radii (`40, 60, 80, 100, 120, 140 arcsec`) lie inside the two-sided
GHASP Halpha support. Separate approaching and receding interpolation brackets
and weights are frozen before tracer velocity differences are evaluated.

The comparison returns both published deprojected curves to line-of-sight
equivalents, `u=Vrot sin(i)`. The primary statistic is the cross-tracer
side-odd contrast

```text
Delta_O = (u_rec-u_app)_Halpha - (u_rec-u_app)_HI.
```

The secondary statistic compares side-even means. Quoted measurement errors
and shared inclination uncertainties are propagated. SPARC `vobs`, rotation
residuals, baseline scores, and required Tau amplitudes are not read by this
freeze.

A nonzero `Delta_O` will be a two-tracer discrepancy diagnostic, not by itself
an observer-channel detection. Beam smearing, gas-phase structure,
non-circular motion, center choice, and remaining geometry differences stay
as conventional alternatives.
