#!/usr/bin/env python3
"""Score a bounded channel load acting only through body susceptibility."""
import json,sys
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/derived';REPORT=ROOT/'reports/body_conditioned_bounded_channel_score_v01.md';sys.path.insert(0,str(ROOT/'scripts'));SEED=20260712;N=10000
import run_source_native_readout_formula_endpoint as source
from run_local_kernel_invariant_response_score import add_phi,rmse
F=source.FORMULA_FAMILIES
def main():
 fr=json.loads((DATA/'body_conditioned_bounded_channel_freeze_v01.json').read_text());assert not fr['uses_vobs_or_residual'];base=json.loads((DATA/'local_kernel_invariant_response_score_v01.json').read_text());eta={x['family']:x['selected_eta'] for x in base['selected_family_eta']};p,_=source.load_points();p=source.add_bridge_formula_kernels(p).reset_index(drop=True)
 for f in F:p[f'phi_{f}']=add_phi(p,f);p[f'v_body_{f}']=p.vn*np.exp(.5*eta[f]*p[f'phi_{f}'])
 c=pd.read_csv(DATA/'continuous_lightcone_channel_proxy_v01.csv');d=p.merge(c,on='galaxy');cols=fr['channel_load_variables'];tr=d.split.eq('train');x=np.log1p(d[cols]);mu=x[tr].mean();sd=x[tr].std(ddof=0).replace(0,1);norm=np.sqrt((((x-mu)/sd)**2).sum(axis=1));d['channel_activation']=norm/(1+norm);grid=[]
 for lam in fr['lambda_grid']:
  z=d[tr].copy();pred=[]
  for _,row in z.iterrows():
   f=row.formula_family;pred.append(row[f'v_body_{f}']*np.exp(.5*lam*row[f'phi_{f}']*row.channel_activation))
  z['sq']=(np.array(pred)-z.vobs.to_numpy())**2;grid.append({'lambda':lam,'galaxy_balanced_rmse':float(np.sqrt(z.groupby('galaxy').sq.mean()).mean())})
 best=min(grid,key=lambda q:q['galaxy_balanced_rmse']);lam=best['lambda'];rows=[]
 for g,z in d.groupby('galaxy'):
  f=z.formula_family.iloc[0];body=z[f'v_body_{f}'].to_numpy();joint=body*np.exp(.5*lam*z[f'phi_{f}'].to_numpy()*z.channel_activation.to_numpy());rows.append({'galaxy':g,'split':z.split.iloc[0],'n_points':len(z),'channel_activation':float(z.channel_activation.iloc[0]),'rmse_body':rmse(z,body),'rmse_joint':rmse(z,joint),'rmse_tpg_v6':rmse(z,z.v_v6.to_numpy()),'rmse_mond':rmse(z,z.v_mond.to_numpy()),'joint_minus_body':rmse(z,joint)-rmse(z,body),'joint_minus_tpg':rmse(z,joint)-rmse(z,z.v_v6.to_numpy()),'joint_minus_mond':rmse(z,joint)-rmse(z,z.v_mond.to_numpy())})
 scores=pd.DataFrame(rows);h=scores[scores.split.eq('holdout')];obs=float(h.joint_minus_body.mean());rng=np.random.default_rng(SEED);null=[]
 # Shuffle only the galaxy-level activation while keeping body profiles fixed.
 acts=h.channel_activation.to_numpy();gal=list(h.galaxy)
 point_hold=d[d.galaxy.isin(gal)].copy()
 for _ in range(N):
  amap=dict(zip(gal,rng.permutation(acts)));delta=[]
  for g,z in point_hold.groupby('galaxy'):
   f=z.formula_family.iloc[0];body=z[f'v_body_{f}'].to_numpy();joint=body*np.exp(.5*lam*z[f'phi_{f}'].to_numpy()*amap[g]);delta.append(rmse(z,joint)-rmse(z,body))
  null.append(float(np.mean(delta)))
 pval=float((1+np.sum(np.array(null)<=obs))/(N+1));result={'schema':'tau-core.paper8.body-conditioned-bounded-channel-score.v01','status':'BODY_CONDITIONED_BOUNDED_CHANNEL_INCREMENTAL_PASS' if obs<0 and pval<=.05 else 'BODY_CONDITIONED_BOUNDED_CHANNEL_INCREMENTAL_FAIL','selected_lambda_train_only':lam,'lambda_train_grid':grid,'n_overlap_holdout':len(h),'mean_joint_minus_body_rmse_km_s':obs,'joint_beats_body_fraction':float((h.joint_minus_body<0).mean()),'joint_beats_tpg_fraction':float((h.joint_minus_tpg<0).mean()),'joint_beats_mond_fraction':float((h.joint_minus_mond<0).mean()),'shuffle_p_mean_gain':pval,'physical_capacity_measured':False,'time_origin_identified':False,'quantum_origin_identified':False,'physical_channel_detected':False,'claim_boundary':'bounded observational-load interaction with frozen body susceptibility; not OSCC capacity or physical channel-origin detection'};(DATA/'body_conditioned_bounded_channel_score_v01.json').write_text(json.dumps(result,indent=2)+'\n');scores.to_csv(DATA/'body_conditioned_bounded_channel_scores_by_galaxy_v01.csv',index=False);REPORT.write_text(f"# Body-conditioned bounded channel score v01\n\nStatus: `{result['status']}`\n\nTrain selected `lambda={lam}`. The `{len(h)}`-galaxy overlap holdout has mean joint-minus-body RMSE `{obs:+.4f} km/s`, joint wins `{result['joint_beats_body_fraction']:.3f}`, and shuffled-load `p={pval:.4f}`. Joint wins versus TPG/MOND are `{result['joint_beats_tpg_fraction']:.3f}` and `{result['joint_beats_mond_fraction']:.3f}`. The bounded load is not a measured information capacity and does not identify time or quantum origin.\n");print(result['status'])
if __name__=='__main__':main()
