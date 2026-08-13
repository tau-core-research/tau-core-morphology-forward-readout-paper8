#!/usr/bin/env python3
"""Test compact source x path interactions on the full outer dark discrepancy."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/derived'; REPORT=ROOT/'reports/dark_discrepancy_morphology_channel_interaction_v01.md'
TARGET=ROOT.parent/'tau-core-theory/source_material/tau_core_foundations/numerical_checks/tau_core_galactic_clock_channel_reparameterization_v01_galaxies.csv'; SEED=20260711; N=2000

def standard(a,train):
    a=np.asarray(a,float); med=np.nanmedian(a[train],axis=0); a=np.where(np.isnan(a),med,a); mu=a[train].mean(0); sd=a[train].std(0); return (a-mu)/np.where(sd>1e-12,sd,1)
def predict(x,y,tr,te):
    a=np.c_[np.ones(tr.sum()),x[tr]]; b=np.c_[np.ones(te.sum()),x[te]]; p=np.eye(a.shape[1]);p[0,0]=0; return b@np.linalg.solve(a.T@a+p,a.T@y[tr])
def mse(a,b):return float(np.mean((a-b)**2))

def main():
    morph=pd.read_csv(DATA/'s4g_optical_morphology_attribution_source_features_v02.csv')
    path=pd.read_csv(DATA/'sparc_lightcone_disturbance_atlas_v02.csv')
    target=pd.read_csv(TARGET)[['galaxy','outer3_required_clock_factor_median']]
    d=morph.merge(path[['galaxy','asymmetry_3p6','source_disturbance_class','foreground_candidate_count','foreground_inverse_angle_weight']],on='galaxy').merge(target,on='galaxy').sort_values('galaxy').reset_index(drop=True)
    tr=d.split.eq('train').to_numpy();te=~tr; y=-2*np.log(d.outer3_required_clock_factor_median.to_numpy())
    base=standard(d[['sparc_t_type','log_distance_mpc','inclination_deg','log_l36','log_reff_kpc','log_sbeff','log_rdisk_kpc','log_sbdisk','log_mhi','log_rhi_kpc']].to_numpy(),tr)
    source=standard(np.c_[d.s4g_bar_present,d.asymmetry_3p6,d.source_disturbance_class.str[1:].astype(float)],tr)
    channel=standard(np.c_[np.log1p(d.foreground_candidate_count),np.log1p(d.foreground_inverse_angle_weight)],tr)
    interaction=np.column_stack([source[:,i]*channel[:,j] for i in range(3) for j in range(2)])
    variants={'baseline':base,'source':np.c_[base,source],'channel':np.c_[base,channel],'source_channel_additive':np.c_[base,source,channel],'source_channel_interaction':np.c_[base,source,channel,interaction]}
    errors={k:mse(y[te],predict(x,y,tr,te)) for k,x in variants.items()}; gain=errors['source_channel_additive']-errors['source_channel_interaction']
    rng=np.random.default_rng(SEED);null=[]
    for _ in range(N):
        cp=channel[rng.permutation(len(d))]; ip=np.column_stack([source[:,i]*cp[:,j] for i in range(3) for j in range(2)])
        xp=np.c_[base,source,cp,ip]; null.append(errors['source_channel_additive']-mse(y[te],predict(xp,y,tr,te)))
    p=float((1+np.sum(np.asarray(null)>=gain))/(N+1)); q95=float(np.quantile(null,.95))
    result={'schema':'dark_discrepancy_morphology_channel_interaction_v01','status':'DARK_DISCREPANCY_SOURCE_CHANNEL_INTERACTION_SIGNAL_PASS' if gain>0 and p<=.05 and gain>q95 else 'DARK_DISCREPANCY_SOURCE_CHANNEL_INTERACTION_SIGNAL_FAIL','n_galaxies':len(d),'n_train':int(tr.sum()),'n_holdout':int(te.sum()),'target':'log outer3 vobs^2/vbar^2; no TPG subtraction','holdout_mse':errors,'interaction_mse_reduction_vs_additive':gain,'channel_row_shuffle_p':p,'channel_row_shuffle_q95':q95,'path_nonzero_count':int((d.foreground_candidate_count>0).sum()),'interaction_information_candidate':bool(gain>0 and p<=.05 and gain>q95),'physical_channel_detected':False,'claim_boundary':'retrospective compact interaction test with incomplete/imbalanced SIMBAD path proxy; even a pass is incremental information, not physical channel causation'}
    (DATA/'dark_discrepancy_morphology_channel_interaction_v01.json').write_text(json.dumps(result,indent=2)+'\n')
    REPORT.write_text(f"# Dark-discrepancy morphology x channel interaction\n\nStatus: `{result['status']}`\n\nThe target is the full outer `v_obs^2/v_bar^2` discrepancy; no TPG term is subtracted. Holdout MSE values are `{errors}`. Adding the six compact source x path terms changes MSE by `{gain:+.6f}` relative to the additive source+path model; path-row shuffle gives `p={p:.4f}` and `q95={q95:.6f}`. Only `{result['path_nonzero_count']}/{len(d)}` objects have a nonzero foreground-count proxy, so this is not a physical lightcone-channel test.\n")
    print(result)
if __name__=='__main__':main()
