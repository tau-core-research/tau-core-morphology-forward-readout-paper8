# NGC4062 velocity-zero-point orthogonalization audit v0.1

**Status:** `POST_OPEN_ORTHOGONALIZATION_DERIVED_FUTURE_FREEZE_REQUIRED`

For a future radial contrast vector $d$, covariance $C$, and a source-frozen velocity-zero-point tangent matrix $G$, the covariance-weighted residual maker is

```text
P_perp = I - G (G^T C^-1 G)^+ G^T C^-1.
```

It obeys $P_\perp G=0$, $P_\perp^2=P_\perp$, and covariance-weighted self-adjointness. Consequently $P_\perp(d+G\eta)=P_\perp d$: an additive systemic-velocity nuisance cannot create the projected signal. With two rings and one nuisance direction, however, only one radial degree of freedom remains.

The opened 769-to-758 km/s secants are diagnostic only. They retain just `0.000910666` (HR) and `2.52332e-05` (LR) of the covariance-weighted information in a constant radial signal. The projected post-open zero tests also remain non-significant (HR $p=0.253$; LR $p=0.299$), but these are not new confirmatory scores.

The decisive counterexample is exact: if the desired signal template and the nuisance tangent are both $(1,1)^T$, projection removes the entire signal. A future terminal is identifiable only if `rank([G,s]) = rank(G) + 1`, with a predeclared minimum retained-information rule. Because the present weighted-median tangent was estimated from opened reductions, the physical/source-owned $G$ is still missing. NGC4062 remains a failed, calibration-limited endpoint.
