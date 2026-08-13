#!/usr/bin/env python3
"""Aggregate the frozen scalar common-channel tests without evidence summation."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/derived"


def load(name):
    return json.loads((DATA / name).read_text())


def main():
    oriented_a = load("ugc08490_oriented_channel_covariance_audit_v02.json")
    oriented_b = load("ugc07323_oriented_channel_covariance_audit_v02.json")
    ngc4254 = load("ngc4254_common_mode_multitracer_v01.json")
    geometry = load("ngc4254_cross_wedge_geometry_sensitivity_v06.json")
    optical = load("ngc4254_optical_line_common_mode_v07.json")
    ngc3351 = load("ngc3351_common_mode_multitracer_v01.json")
    multipath = load("sdp81_q1_multipath_centroid_v02.json")
    rows = [
        {"family":"side-odd reciprocal scalar","objects":"UGC08490 + UGC07323",
         "result":"rejected as complete pointwise law in both preflights",
         "gate_pass":False,"reason":"distributed common-q incompatibility without stable global side bias"},
        {"family":"same-galaxy tracer-independent common scalar","objects":"NGC4254",
         "result":"tracer agreement rejected and geometry-confounded",
         "gate_pass":False,"reason":f"CO/Halpha p={ngc4254['tracer_agreement_p']:.4g}; geometry all-significant={geometry['all_formal_residual_tests_p_below_0_01']}"},
        {"family":"same-instrument line-independent common scalar","objects":"NGC4254 MUSE lines",
         "result":"line consistency rejected","gate_pass":False,
         "reason":f"five-line control p={optical['all_optical_vs_halpha_p']:.4g}"},
        {"family":"cross-galaxy reproducible common scalar","objects":"NGC4254 -> NGC3351",
         "result":"not replicated","gate_pass":False,
         "reason":f"NGC3351 common p={ngc3351['common_zero_p']:.4g}; tracer p={ngc3351['tracer_agreement_p']:.4g}"},
        {"family":"same-source multipath scalar shift","objects":"SDP.81 q1",
         "result":"target window not exceptional","gate_pass":False,
         "reason":f"rolling-window upper-tail fraction={multipath['empirical_upper_tail_fraction']:.3f}"},
    ]
    result = {
        "schema":"common_channel_exclusion_matrix_v01",
        "rows":rows,
        "all_universal_scalar_gates_pass":all(x["gate_pass"] for x in rows),
        "excluded_candidate_family":"one universal tracer-independent scalar common/reciprocal channel law as complete explanation of current endpoints",
        "not_excluded":["body-conditioned finite-rank channel","frequency/polarization selective channel",
                        "noncommutative or transition-sensitive channel","common mode below current systematics",
                        "parent-readout effect not represented by these observables"],
        "physical_channel_detected":False,
        "dark_matter_replacement_supported":False,
        "claim_boundary":"joint constraint matrix; correlated tests are not summed as independent evidence",
    }
    (DATA/"common_channel_exclusion_matrix_v01.json").write_text(json.dumps(result,indent=2)+"\n")
    lines=["# Common-channel exclusion matrix v01","",
           "The rows are joint constraints, not statistically independent evidence to be summed.","",
           "| candidate family | objects | result | gate |","| --- | --- | --- | --- |"]
    for x in rows: lines.append(f"| {x['family']} | {x['objects']} | {x['result']} | FAIL |")
    lines += ["",f"**Excluded candidate family:** {result['excluded_candidate_family']}.","",
              "This does not exclude the listed complex/body-conditioned families and does not detect a physical channel."]
    (ROOT/"reports/common_channel_exclusion_matrix_v01.md").write_text("\n".join(lines)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__": main()
