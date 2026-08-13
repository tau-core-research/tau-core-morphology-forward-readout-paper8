#!/usr/bin/env python3
"""Score the frozen signed declining-transition morphology response."""
import json,sys
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/derived';REPORT=ROOT/'reports/signed_kernel_transition_response_score_v01.md';sys.path.insert(0,str(ROOT/'scripts'))
import run_source_native_readout_formula_endpoint as source
F=source.FORMULA_FAMILIES
def rmse(s,p):return float(np.sqrt(np.mean((p-s.vobs.to_numpy())**2)))
def activation(points,f):
 out=np.zeros(len(points))
 for _,idx in points.groupby('galaxy').groups.items():
  z=points.loc[idx].sort_values('r');r=z.r.to_numpy();k=z[f'kernel_{f}'].to_numpy();rs=float(z.scale_radius_proxy_kpc.iloc[0]);eps=1e-12*max(float(np.max(np.abs(k))),1.);den=max(abs(float(np.interp(rs,r,k))),eps);u=np.maximum(k/den,0);phi=u/(1+u);s=np.gradient(np.log(np.maximum(np.abs(k),eps)),np.log(np.maximum(r,1e-8)),edge_order=1);out[z.index]=phi*(1-np.tanh(s))/2
 return out
def main():
 fr=json.loads((DATA/'signed_kernel_transition_response_freeze_v01.json').read_text());assert not fr['uses_vobs_or_residual'];p,_=source.load_points();p=source.add_bridge_formula_kernels(p).reset_index(drop=True)
 for f in F:p[f'psi_{f}']=activation(p,f)
 tr=p[p.split.eq('train')];eta={};fits=[]
 for f in F:
  z=tr[tr.formula_family.eq(f)];grid=[]
  for e in fr['eta_grid']:
   pred=z.vn.to_numpy()*np.exp(.5*e*z[f'psi_{f}'].to_numpy());q=pd.DataFrame({'g':z.galaxy,'sq':(pred-z.vobs.to_numpy())**2});grid.append({'eta':e,'galaxy_balanced_rmse':float(np.sqrt(q.groupby('g').sq.mean()).mean())})
  b=min(grid,key=lambda x:x['galaxy_balanced_rmse']);eta[f]=b['eta'];fits.append({'family':f,'selected_eta':b['eta'],'grid':grid})
 for f in F:p[f'v_signed_{f}']=p.vn*np.exp(.5*eta[f]*p[f'psi_{f}'])
 rows=[]
 for g,z in p.groupby('galaxy'):
  mf=z.formula_family.iloc[0];fs={f:rmse(z,z[f'v_signed_{f}'].to_numpy()) for f in F};m=fs[mf];w=np.mean([v for f,v in fs.items() if f!=mf]);base={'newton':rmse(z,z.vn.to_numpy()),'tpg_v6':rmse(z,z.v_v6.to_numpy()),'mond':rmse(z,z.v_mond.to_numpy())};rows.append({'galaxy':g,'split':z.split.iloc[0],'formula_family':mf,'n_points':len(z),'rmse_matched':m,'matched_minus_wrong':m-w,**{f'matched_minus_{k}':m-v for k,v in base.items()},**{f'rmse_{f}':v for f,v in fs.items()}})
 scores=pd.DataFrame(rows).sort_values(['split','galaxy']);h=scores[scores.split.eq('holdout')]
 def sm(c):v=h[c];return {'win_fraction':float((v<0).mean()),'mean_delta_km_s':float(v.mean())}
 r={'schema':'tau-core.paper8.signed-kernel-transition-response-score.v01','status':'SIGNED_DECLINING_KERNEL_TRANSITION_HOLDOUT_SCORED','selected_family_eta':fits,'n_holdout_galaxies':len(h),'n_holdout_points':int(h.n_points.sum()),'matched_vs_wrong':sm('matched_minus_wrong'),'matched_vs_newton':sm('matched_minus_newton'),'matched_vs_tpg_v6':sm('matched_minus_tpg_v6'),'matched_vs_mond':sm('matched_minus_mond'),'channel_coordinates_used':[],'claim_boundary':'retrospective signed-transition diagnostic; not prospective, parent-derived, or validation'};(DATA/'signed_kernel_transition_response_score_v01.json').write_text(json.dumps(r,indent=2)+'\n');scores.to_csv(DATA/'signed_kernel_transition_response_scores_by_galaxy_v01.csv',index=False);REPORT.write_text(f"# Signed declining-kernel transition score v01\n\nStatus: `{r['status']}`\n\nHoldout wins versus wrong/Newton/TPG/MOND: `{r['matched_vs_wrong']['win_fraction']:.3f}`, `{r['matched_vs_newton']['win_fraction']:.3f}`, `{r['matched_vs_tpg_v6']['win_fraction']:.3f}`, `{r['matched_vs_mond']['win_fraction']:.3f}`. Mean TPG/MOND deltas: `{r['matched_vs_tpg_v6']['mean_delta_km_s']:.3f}`, `{r['matched_vs_mond']['mean_delta_km_s']:.3f} km/s`.\n");print(r['status'])
if __name__=='__main__':main()
