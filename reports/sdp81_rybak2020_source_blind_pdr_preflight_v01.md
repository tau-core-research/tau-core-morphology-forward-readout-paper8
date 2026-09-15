# SDP.81 Rybak-2020 CO(10-9)-blind PDR preflight v01

Status: `SOURCE_ACQUIRED_PDR_AMPLITUDE_PARTIAL_SPECTRAL_REGISTRATION_BLOCKED`. Endpoint authorized: `False`.

The official 200-pc source products supply 288 pixels with S/N >= 3 in CII, FIR, CO(3-2), CO(5-4), and CO(8-7). No CO(10-9) header or pixel was read.

A solar-metallicity `wk2006` PDR fit using CII/FIR, CII/CO(5-4), CII/CO(3-2), and CO(8-7)/CO(5-4) gives median log n=4.95, median log G0=3.25, and a blind median CO(10-9)/CO(5-4) prediction of 0.2310. Only 80/288 pixels have reduced chi2 < 5, and the median 68% relative predictive half-width is 0.363.

Verdict: the independent maps materially close source acquisition and provide a standard-physics integrated-amplitude prior, but they do not determine the six-channel, four-path terminal Jacobian. The held-out endpoint remains sealed.

Next finite action: combine the accepted source pixels with an independently frozen velocity/profile model and the ordinary lens/aperture operator, then test whether the resulting five-mode terminal registration is full rank before opening CO(10-9).
