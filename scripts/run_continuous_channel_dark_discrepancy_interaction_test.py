#!/usr/bin/env python3
"""Test continuous observational channel loads against the full dark discrepancy."""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/derived';REPORT=ROOT/'reports/continuous_channel_dark_discrepancy_interaction_v01.md';sys.path.insert(0,str(ROOT/'scripts'))
from run_dark_discrepancy_morphology_channel_interaction_test import standard,predict,mse,TARGET
N=2000;SEED=20260711
def main():
 m=pd.read_csv(DATA/'s4g_optical_morphology_attribution_source_features_v02.csv');a=pd.read_csv(DATA/'sparc_lightcone_disturbance_atlas_v02.csv');c=pd.read_csv(DATA/'continuous_lightcone_channel_proxy_v01.csv');t=pd.read_csv(TARGET)[['galaxy','outer3_required_clock_factor_median']]
 d=m.merge(a[['galaxy','asymmetry_3p6','source_disturbance_class']],on='galaxy').merge(c,on='galaxy').merge(t,on='galaxy').sort_values('galaxy').reset_index(drop=True);tr=d.split.eq('train').to_numpy();te=~tr;y=-2*np.log(d.outer3_required_clock_factor_median)
 base=standard(d[['sparc_t_type','log_distance_mpc','inclination_deg','log_l36','log_reff_kpc','log_sbeff','log_rdisk_kpc','log_sbdisk','log_mhi','log_rhi_kpc']].to_numpy(),tr);src=standard(np.c_[d.s4g_bar_present,d.asymmetry_3p6,d.source_disturbance_class.str[1:].astype(float)],tr);ch=standard(np.log1p(d[['foreground_lens_geometry_weight','foreground_angular_weight','stellar_crowding_angular_weight']].to_numpy()),tr);inter=np.column_stack([src[:,i]*ch[:,j] for i in range(3) for j in range(3)])
 xs={'baseline':base,'source':np.c_[base,src],'continuous_channel':np.c_[base,ch],'additive':np.c_[base,src,ch],'interaction':np.c_[base,src,ch,inter]};err={k:mse(y[te],predict(x,y,tr,te)) for k,x in xs.items()};gain=err['additive']-err['interaction'];rng=np.random.default_rng(SEED);null=[]
 for _ in range(N):
  cp=ch[rng.permutation(len(d))];ip=np.column_stack([src[:,i]*cp[:,j] for i in range(3) for j in range(3)]);null.append(err['additive']-mse(y[te],predict(np.c_[base,src,cp,ip],y,tr,te)))
 p=float((1+np.sum(np.array(null)>=gain))/(N+1));q=float(np.quantile(null,.95));result={'schema':'continuous_channel_dark_discrepancy_interaction_v01','status':'CONTINUOUS_CHANNEL_DARK_DISCREPANCY_INTERACTION_PASS' if gain>0 and p<=.05 and gain>q else 'CONTINUOUS_CHANNEL_DARK_DISCREPANCY_INTERACTION_FAIL','n_galaxies':len(d),'target':'log outer3 vobs^2/vbar^2; no TPG subtraction','holdout_mse':err,'interaction_mse_reduction':gain,'shuffle_p':p,'shuffle_q95':q,'interaction_information_candidate':bool(gain>0 and p<=.05 and gain>q),'physical_channel_detected':False,'claim_boundary':'continuous observational-load proxy test; not physical time/lightcone transfer detection'};(DATA/'continuous_channel_dark_discrepancy_interaction_v01.json').write_text(json.dumps(result,indent=2)+'\n');REPORT.write_text(f"# Continuous channel-load dark-discrepancy interaction\n\nStatus: `{result['status']}`\n\nThe full outer `v_obs^2/v_bar^2` target is used without TPG subtraction. Holdout MSE values are `{err}`. Interaction reduction is `{gain:+.6f}`, shuffle `p={p:.4f}`, `q95={q:.6f}`. The variables are continuous observational-load proxies, not a physical time/lightcone transfer.\n");print(result)
if __name__=='__main__':main()
