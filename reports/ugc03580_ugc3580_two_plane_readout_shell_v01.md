# UGC03580 / UGC3580 bounded two-plane readout shell v01

Status: `FORMULA_SHELL_DERIVED_ENDPOINT_BLOCKED`

## Derived source coordinate

For a ring normal `n(R)` and the source-defined inner and outer plane
normals, define

```text
d_in(R)  = 1 - n_in dot n(R)
d_out(R) = 1 - n_out dot n(R)
K_p(R)   = d_in(R)^p / [d_in(R)^p + d_out(R)^p],   p>0.
```

Because both defects are nonnegative, `0<=K_p<=1`. For distinct
reference planes it is exactly zero on the inner plane, exactly one
on the outer plane, and changes to `1-K_p` when the plane labels are
swapped. Coincident planes deactivate the construction and set `K_p=0`.
The primary `p=1` coordinate is only the minimal affine-defect convention.

## Exact mirror fibre of the raw descriptor

The raw pair `(d_in,d_out)` fixes the projection of the ring normal into
the span of the two reference normals but generically leaves a two-point
mirror fibre. With `c=(n_in x n_out)/|n_in x n_out|`, the signed control
`chi=c dot n` completes the oriented descriptor, while `chi^2` is already
fixed by the raw defects. A local rank test misses this discrete ambiguity;
quotienting it requires exact equality of every terminal on the mirror pair.
Jozsa (2007) Table 6 publishes the oriented spin-normal components
toward west, north, and the observer, while the UGC3580 captions identify
the approaching side as southeast. Thus the signed record is source-owned.
Moreover, the standard fixed-inner-inclination projection is not mirror-even:

```text
G_proj(R_c n)-G_proj(n)
  = 4 chi (ell dot c)[(ell dot n)-chi(ell dot c)]/sin(i_inner)^2.
```

On supported rings its maximum absolute difference is `0.142726674696`
and its RMS difference is `0.046534679366`.
Therefore `chi` must be retained in the complete projection descriptor.
This is representation correctness under a standard projection, not evidence
for fundamental Parent handedness or a Tau-specific `chi` coupling.
No endpoint is used in this control.

## Scalar-registration boundary

`K_1` cannot replace the complete signed descriptor. It is unchanged
on every raw-descriptor mirror pair even though the standard projection
can change. The source path supplies a stronger within-path witness:
the level `K_1=0.925` occurs at `228.939929970`
and `275.245362641 arcsec`, while
the projection changes from `0.998056542027`
to `1.084700249348` and `chi`
has opposite signs. The neighboring targets 0.900 and 0.950 reproduce
the collision, so it is not a tuned level choice.

This refutes `K_1` as a complete shared coordinate; it does not prove
that every Parent action must couple to two independent components. A
source-derived rank-one factorization through another signed scalar remains
logically possible. Until it is proved, the safe action handoff retains
`D_hat` or an exactly fibre-equivalent descriptor.

## Complete registration versus scalar interaction

The separate MBA-2P-P6 theory audit constructs the exact decoder

$$
\mathcal N(\widehat D)
=A_{ab}^{-1}(1-d_{\mathrm{in}},1-d_{\mathrm{out}},\chi)^T
$$

and a positive graph action whose unique zero is this decoder. On the
complete signed two-plane descriptor surface the decoder differential
restricted to the physical tangent has rank two. Because the decoder
is explicit in the square, this proves conditional existence and
consistency rather than deeper source selection. A later scalar
invariant I_K=f(N) has pointwise rank at
most one, so it is a partial interaction input rather than the complete
orientation register.

The UGC03580 radial path is one-dimensional and has registration
pullback rank at most one. It can refute K_1 through the repeated fibre
but cannot establish Nature-level rank-two occupation. The graph-action
theory audit passes 22/22 checks and is not counted in the 62/62 Paper 8
source-shell audit.

## What the body does not determine

For every `p>0`, `0<=a<=1`, and sign `s=+/-1`,

```text
v_(p,a,s)^2 = v_carrier^2 * [1 + s*a*K_p]
```

is dimensionally valid, bounded, nonnegative and has the same carrier
recovery limit. Distinct choices give distinct curves. This explicit
counterfamily proves that the two-plane body alone cannot select the
terminal exponent, amplitude, sign or carrier.

## Exact Parent-response specialization

After the body has been solved and frozen, a regular post-body action gives

```text
D_K Z_* = -H_Z^{-1} B_ZK,
Gamma   = -L_G H_Z^{-1} B_ZK,
delta v_G^2(R) = [Gamma K](R).
```

Positive `H_Z` guarantees a regular stable response, but it does not fix
the sign or scale of the mixed block or the physical terminal covector.
The scalar shell with one constant `a` follows only if the complete radial
operator factorizes so that `[Gamma K_p]/(v_carrier^2 K_p)=s*a` is constant
where `K_p` is nonzero. The current source packet does not prove this.
Likewise, a source action must select the exact defect response to fix `p`;
a leading analytic source jet fixes only a local leading order, not the full
global `K_p` law. The carrier is the separately derived zero-morphology
physical terminal branch, not an empirical residual baseline.

In one frozen common-action completion these objects are not independent
gains. A source-owned complete registration `I=iota(D_hat)` gives
`B_ZDhat=B_ZI J_(I<-Dhat)` and the same gravity/observer terminal gives
`v_carrier^2=O_G[Z_*(I=0)]`. Exact Schur elimination must retain any
occupied internal-field contribution. The unresolved physical object is
the full-support signed-descriptor-to-Parent-invariant registration,
rather than three coefficients to fit independently.

## Source-only numerical envelope and standard control

- plane separation: `14.296629 deg`;
- geometry-only scale `sin^2(Theta/2)`: `0.015484869`;
- supported `K_1` range: `0.000000` to `0.992276`;
- maximum transition `|K_1-K_2|`: `0.149874`;
- fixed-inner-inclination projection `G_proj` range: `0.994091` to `1.096849`.
- maximum mirror-pair `|Delta G_proj|`: `0.142726674696`.

The `G_proj` relation is standard circular tilted-ring projection and
is usable only if the target terminal was reduced with the fixed inner
inclination. It is a null/control calculation, not a Tau signal.

## Verdict

The exact mirror audit closes the orientation/null decision for this
projection lane: `chi` is source-owned and terminal-visible, so it is
retained. The source-path collision additionally refutes `K_1` as the
complete registration. It does not close fundamental Parent handedness or
prove a multicomponent physical coupling. The sharper physical blocker is
whether one source-owned signed scalar factorization exists or the common
action retains multiple descriptor directions. No endpoint is opened or
rescored. The next
admissible step is a source-owned full-support registration plus a frozen
common gravity/observer calibration, followed by a genuinely new target.
