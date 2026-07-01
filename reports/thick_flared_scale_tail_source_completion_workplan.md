# Thick/Flared and Scale-Tail Source-Completion Workplan

**Doc class:** source-completion workplan

**Reader role:** Paper 8 replay maintainer

**Status:** `MORPHOLOGY_SOURCE_COMPLETION_REQUIRED`

**Canonical parent:** `reports/morphology_observable_source_upgrade_plan.md`

Canonical data artifact:

```text
data/derived/thick_flared_scale_tail_source_completion_v1.csv
```

## Purpose

This workplan selects the simplest Paper 8 routes that can still produce
useful galaxy-rotation demonstrations without turning into curve fitting:
vertical/thick-flared kernels and scale-tail kernels.

## Priority Routes

### 1. Thick/flared or vertical-overlay kernels

Required source observables:

```text
inclination
scale-height or thickness proxy
H I flare / warp support
vertical overlay window
source provenance
```

Allowed use:

```text
source-frozen vertical/projection-sensitive replay
```

Blocked use:

```text
do not infer thickness, vertical window, or amplitude from residual shape
do not reuse clock/time evidence unless a non-overlap ledger exists
```

### 2. Scale-tail kernels

Required source observables:

```text
outer H I extent
surface-density tail
break or transition radius
diffuse LSB context
source-native uncertainty interval
```

Allowed use:

```text
source-native scale-tail replay
```

Blocked use:

```text
do not infer the transition radius from the rotation residual
do not use MOND/RAR residuals to set the tail load
```

## Why These First

These two routes are still close to the 1D SPARC setting but more informative
than a generic exponential disk proxy. They can test whether a better
source-side morphology description changes the predicted readout in the
expected direction.

## Deferred Routes

Barred and lopsided kernels are not rejected, but they are deferred:

```text
K_m2_barred -> velocity-field program
K_m1_lopsided -> velocity-field program
```

They should not be promoted as clean 1D endpoint tests.

## Claim Boundary

A successful replay after this source completion would support:

```text
source-frozen morphology/readout preflight
```

It would not establish a universal weak-field law or population-level
validation.
