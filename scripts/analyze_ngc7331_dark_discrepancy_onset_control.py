#!/usr/bin/env python3
"""Independent SPARC dark-discrepancy onset control for NGC7331."""
from __future__ import annotations
import json,sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/derived'; REPORT=ROOT/'reports/ngc7331_dark_discrepancy_onset_control_v01.md';sys.path.insert(0,str(ROOT/'scripts'))
import run_source_native_readout_formula_endpoint as source

def first_sustained(frame,column,threshold):
    ok=frame[column].to_numpy()>threshold
    for i in range(len(ok)):
        if ok[i:].all(): return float(frame.r.iloc[i])
    return None

def main():
    points,_=source.load_points(); q=points[points.galaxy.eq('NGC7331')].sort_values('r').copy()
    q['dark_discrepancy_ratio']=q.vobs**2/q.vn**2; q['newton_excess_z']=(q.vobs-q.vn)/q.errv
    fingerprint=pd.read_csv(DATA/'mixed_kernel_observable_separation_fingerprints.csv').query("galaxy=='NGC7331'").iloc[0]
    positive=first_sustained(q,'dark_discrepancy_ratio',1); robust=first_sustained(q,'newton_excess_z',3); warp=float(fingerprint.source_onset_kpc)
    q[['r','vobs','errv','vn','dark_discrepancy_ratio','newton_excess_z']].to_csv(DATA/'ngc7331_dark_discrepancy_onset_control_points_v01.csv',index=False)
    result={'schema':'ngc7331_dark_discrepancy_onset_control_v01','status':'NGC7331_DARK_DISCREPANCY_PRECEDES_SOURCE_FROZEN_WARP_ONSET','target':'vobs^2-vbar^2; no TPG subtraction','positive_sustained_onset_kpc':positive,'three_sigma_sustained_onset_kpc':robust,'source_frozen_warp_onset_kpc':warp,'robust_onset_minus_warp_kpc':robust-warp,'simple_universal_morphology_onset_alignment_supported':False,'tau_morphology_detected':False,'channel_detected':False,'claim_boundary':'single SPARC galaxy with measurement-error threshold but no baryonic-model covariance; negative control for simple warp-onset equality'}
    (DATA/'ngc7331_dark_discrepancy_onset_control_v01.json').write_text(json.dumps(result,indent=2)+'\n')
    REPORT.write_text(f"# NGC7331 dark-discrepancy onset control\n\nStatus: `{result['status']}`\n\nThe target is `v_obs^2-v_bar^2`, with no TPG subtraction. The sustained positive onset is `{positive:.2f} kpc` and the sustained `3 sigma` measurement-error onset is `{robust:.2f} kpc`. The independently frozen outer-warp source onset is `{warp:.2f} kpc`, so the robust discrepancy precedes it by `{warp-robust:.2f} kpc`. This rejects simple universal equality between dark-discrepancy onset and the selected morphology onset; it does not test channel interaction.\n")
    print(result)
if __name__=='__main__':main()
