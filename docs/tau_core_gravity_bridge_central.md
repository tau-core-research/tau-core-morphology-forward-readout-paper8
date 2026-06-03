# Tau Core Gravity Bridge Central Architecture

This page is the local Paper 8 bridge entrypoint. It records the morphology
layer discipline used by the morphology-matched forward-readout gate.

## Scope

The Paper 8 bridge does not assume that present-day visual morphology is a
fundamental Tau-side class. It uses observed morphology as a residual-blind
source handle, then separates that handle from the readout-relevant proxy used
to choose a candidate 4D readout shell.

This distinction is a Tau Core bridge consequence: the bridge treats galaxy
morphology as a projection/readout structure, not merely as a 4D visual label.

## Core Chain

```text
Tau-side configuration / morphology
    -> projection and 4D readout
    -> observed 4D morphology handle K_obs
    -> residual-blind source review, caveats, and provenance
    -> readout-relevant morphology proxy K_readout
    -> predeclared 4D readout formula shell F_{K_readout}
    -> forward delta_g or delta_v^2 pilot score
```

`K_obs` is the apparent or catalogue-supported 4D morphology handle. It may be
a thin disk, thick/flared disk, bar, ring, compact component, tail, lopsided
feature, or other projected morphology descriptor.

`K_readout` is the predeclared readout-relevant morphology proxy. It is the
object allowed to select the formula shell. It may equal `K_obs`, but this is
not assumed.

## Main Clarification

Observed 4D morphology handles are not fundamental Tau-side classes. Thin disk,
thick disk, bar, ring, compact, tail, scale-tail, and lopsided labels are
projected 4D morphology handles unless an additional Tau-side or source-review
argument promotes them to readout-relevant proxies.

Therefore the formula-selection rule is:

```text
F = F_{K_readout}
```

not automatically:

```text
F = F_{K_obs}
```

This prevents a present-day visual exponential disk from being silently treated
as a clean exponential-disk readout when the source evidence points to
projection, bar, compact-core, outer-disk, or morphology-history caveats.

## Memory / History Layer

The bridge also permits a morphology-memory or history proxy layer. A galaxy's
current observed 4D shape may be an incomplete proxy for the readout-relevant
morphology if the solved readout encodes delayed, integrated, or projection
filtered structure.

This layer is only a hypothesis layer until populated by residual-blind source
evidence. Rotation-curve-inferred readout families may motivate review, but
they cannot define accepted morphology labels or endpoint families.

Forbidden inputs for `K_readout` include:

```text
endpoint residual gain
required-S_tau diagnostic
best-fit Tau Core readout family
MOND/RAR/TGP comparison score
post-hoc family switching
per-galaxy residual tuning
```

## P0 Example

The current P0 source-reviewed rows all have the apparent 4D handle
`K_exponential_disk`, but the bridge layer separates them into different
readout-relevant proxy rows:

| Galaxy | K_obs | K_readout proxy |
| --- | --- | --- |
| NGC0100 | K_exponential_disk | K_projection_corrected_expdisk |
| NGC0247 | K_exponential_disk | K_barred_expdisk_m2_overlay |
| NGC0300 | K_exponential_disk | K_clean_exponential_disk_control |
| NGC6503 | K_exponential_disk | K_expdisk_compact_core_overlay |

This is not an endpoint label and not an empirical Tau Core validation. It is a
bridge-consistent source-review distinction.

## Consequences For Paper 8

The plain `K_exponential_disk` P0 pilot is a weak or control-style test unless
the row is a clean exponential-disk control. For caveated rows, the correct
next test is the predeclared `K_readout` shell or overlay family, not the raw
observed 4D handle.

The central endpoint remains claim-bounded:

```text
Does the predeclared morphology/readout family rank better than wrong families
and shuffled labels, while remaining competitive against Newtonian, MOND/RAR,
and TGP-like baselines?
```

The bridge does not yet claim that these readout proxies are final Tau-side
classes, that Tau Core is empirically validated, or that MOND/RAR/TGP
comparators have been superseded.

## Baseline Success As Readout-Regime Control

The bridge also records the complementary control reading: if a conventional or
historical baseline already fits a galaxy well, that success may itself mark a
Tau Core readout regime.

```text
Newtonian good fit
    -> quiet / regular baryonic-readout regime.

MOND or RAR good fit
    -> scalarized radial low-acceleration or diffuse-disk regime.

TPG good fit
    -> smooth closure-like or memory-integrated readout regime.

Tau matched-family good fit
    -> current morphology proxy may be close to K_readout.
```

This matters because Paper 8 should not claim that Tau Core must beat every
baseline everywhere. A stronger claim-safe endpoint is that baseline success
zones and Tau-family success zones map to distinct predeclared
morphology/readout regimes. Baseline winners may therefore become controls,
especially for galaxies whose present-day 4D morphology is regular, scalarized,
or historically/memory integrated.
