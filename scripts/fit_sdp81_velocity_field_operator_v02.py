#!/usr/bin/env python3
"""Run the frozen full-signal-window SDP.81 velocity operator."""

from __future__ import annotations

import fit_sdp81_velocity_field_operator_v01 as operator


operator.CHANNELS = list(range(47, 58))
operator.SCHEMA = "tau_core.paper8.sdp81-velocity-field-operator.v02"
operator.OUT = operator.DATA / "sdp81_velocity_field_operator_v02.json"
operator.REPORT = operator.ROOT / "reports/sdp81_velocity_field_operator_v02.md"


if __name__ == "__main__":
    operator.main()
