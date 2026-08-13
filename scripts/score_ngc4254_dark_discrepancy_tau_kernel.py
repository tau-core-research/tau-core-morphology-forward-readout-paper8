#!/usr/bin/env python3
"""Score fixed TPG and MOND responses on the NGC4254 dark discrepancy."""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/derived'; REPORT=ROOT/'reports/ngc4254_dark_discrepancy_tau_kernel_score_v01.md'
A0=1.2e-10; KPC_M=3.085677581491367e19

def main():
    d=pd.read_csv(DATA/'ngc4254_radial_dark_discrepancy_sensitivity_v01.csv').dropna(subset=['vobs_km_s','vbar_km_s']).copy()
    an=(d.vbar_km_s.to_numpy()*1000)**2/(d.radius_kpc.to_numpy()*KPC_M)
    x=A0/an; vn=d.vbar_km_s.to_numpy(); obs=d.vobs_km_s.to_numpy()
    d['v_newton']=vn
    d['v_tpg_v6']=vn*(1+0.360*np.log1p(x))
    d['v_mond']=vn*np.sqrt((1+np.sqrt(1+4*x))/2)
    d['delta_v2_observed']=obs**2-vn**2
    d['delta_v2_tpg']=d.v_tpg_v6**2-vn**2
    d['delta_v2_mond']=d.v_mond**2-vn**2
    rows=[]
    for key,g in d.groupby(['star_scale','h2_scale','height_pc']):
        row=dict(zip(['star_scale','h2_scale','height_pc'],key))
        for model in ['newton','tpg_v6','mond']:
            row[f'rmse_{model}_km_s']=float(np.sqrt(np.mean((g[f'v_{model}']-g.vobs_km_s)**2)))
        row['spearman_delta_v2_tpg']=float(spearmanr(g.delta_v2_observed,g.delta_v2_tpg).statistic)
        row['spearman_delta_v2_mond']=float(spearmanr(g.delta_v2_observed,g.delta_v2_mond).statistic)
        rows.append(row)
    scores=pd.DataFrame(rows); scores.to_csv(DATA/'ngc4254_dark_discrepancy_tau_kernel_sensitivity_v01.csv',index=False)
    nominal=scores[(scores.star_scale==1)&(scores.h2_scale==1)&(scores.height_pc==300)].iloc[0]
    result={'schema':'ngc4254_dark_discrepancy_tau_kernel_score_v01','status':'NGC4254_FIXED_TPG_DARK_DISCREPANCY_SHAPE_DIAGNOSTIC','n_models':len(scores),'n_radial_bins':int(d[d.star_scale.eq(1)&d.h2_scale.eq(1)&d.height_pc.eq(300)].shape[0]),'nominal_rmse_km_s':{m:float(nominal[f'rmse_{m}_km_s']) for m in ['newton','tpg_v6','mond']},'nominal_delta_v2_spearman':{'tpg_v6':float(nominal.spearman_delta_v2_tpg),'mond':float(nominal.spearman_delta_v2_mond)},'model_win_counts':{m:int((scores[f'rmse_{m}_km_s']==scores[[f'rmse_{x}_km_s' for x in ['newton','tpg_v6','mond']]].min(axis=1)).sum()) for m in ['newton','tpg_v6','mond']},'ngc4254_parameters_fitted':False,'tau_kernel_origin_identified':False,'channel_origin_identified':False,'claim_boundary':'single-galaxy coarse radial fixed-form comparison; shape agreement is not morphology/channel attribution or dark-matter exclusion'}
    (DATA/'ngc4254_dark_discrepancy_tau_kernel_score_v01.json').write_text(json.dumps(result,indent=2)+'\n')
    REPORT.write_text(f"# NGC4254 dark-discrepancy Tau-kernel score\n\nStatus: `{result['status']}`\n\nNo NGC4254 parameter is fitted. Nominal RMSE values are Newton `{result['nominal_rmse_km_s']['newton']:.2f}`, fixed TPG/v6 `{result['nominal_rmse_km_s']['tpg_v6']:.2f}`, and MOND `{result['nominal_rmse_km_s']['mond']:.2f} km/s`. The observed-versus-predicted discrepancy-shape Spearman coefficients are TPG `{result['nominal_delta_v2_spearman']['tpg_v6']:.3f}` and MOND `{result['nominal_delta_v2_spearman']['mond']:.3f}`. Across 27 baryonic models the win counts are `{result['model_win_counts']}`. This tests a fixed radial response shape, not Tau morphology or channel origin.\n")
    print(result)
if __name__=='__main__': main()
