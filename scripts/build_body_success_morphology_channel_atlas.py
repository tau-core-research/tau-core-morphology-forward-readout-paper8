#!/usr/bin/env python3
"""Build a descriptive atlas of body-model success, morphology, and channel context."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/derived';REPORT=ROOT/'reports/body_success_morphology_channel_atlas_v01.md'
MORPH=['inclination_deg','distance_frac_error','r_median','r_max','mean_gas','mean_bulge','mean_log_sbdisk','peak_log_sb','scale_radius_proxy_kpc','tail_cutoff_radius_proxy_kpc','thickness_h_over_rs_proxy','bar_m2_proxy','lopsided_m1_proxy']
CHANNEL=['foreground_lens_geometry_weight','foreground_angular_weight','stellar_crowding_angular_weight']
def main():
 score=pd.read_csv(DATA/'local_kernel_invariant_response_scores_by_galaxy_v01.csv');m=pd.read_csv(DATA/'morphology_parameter_manifest.csv');a=pd.read_csv(DATA/'sparc_lightcone_disturbance_atlas_v02.csv');c=pd.read_csv(DATA/'continuous_lightcone_channel_proxy_v01.csv');d=score.merge(m,on=['galaxy','split','formula_family'],validate='one_to_one').merge(a[['galaxy','source_disturbance_class','asymmetry_3p6','theta1']],on='galaxy',how='left').merge(c,on='galaxy',how='left');d=d[d.split.eq('holdout')].copy();d['performance_class']=np.where(d.matched_minus_newton>=0,'body_failure',np.where(d.matched_minus_tpg_v6<0,'strong_success','partial_success'))
 rows=[]
 for cls,z in d.groupby('performance_class'):
  row={'performance_class':cls,'n_galaxies':len(z),'mean_body_minus_newton_km_s':float(z.matched_minus_newton.mean()),'mean_body_minus_tpg_km_s':float(z.matched_minus_tpg_v6.mean()),'mean_body_minus_mond_km_s':float(z.matched_minus_mond.mean()),'channel_complete_n':int(z[CHANNEL].notna().all(axis=1).sum())}
  for col in MORPH+['asymmetry_3p6','theta1']+CHANNEL:
   row[f'median_{col}']=float(z[col].median()) if z[col].notna().any() else None
  rows.append(row)
 summary=pd.DataFrame(rows).sort_values('performance_class');family=pd.crosstab(d.performance_class,d.formula_family);family_frac=family.div(family.sum(axis=1),axis=0)
 # Standardized exploratory contrasts against all other classes; train statistics avoid holdout scaling.
 full=score.merge(m,on=['galaxy','split','formula_family']);train=full[full.split.eq('train')];contrasts=[]
 for col in MORPH:
  mu=float(train[col].mean());sd=float(train[col].std(ddof=0)) or 1.;d[f'z_{col}']=(d[col]-mu)/sd
 for cls in ['strong_success','partial_success','body_failure']:
  inside=d[d.performance_class.eq(cls)];outside=d[~d.performance_class.eq(cls)]
  for col in MORPH:
   contrasts.append({'performance_class':cls,'feature':col,'standardized_mean_contrast':float(inside[f'z_{col}'].mean()-outside[f'z_{col}'].mean()),'n_inside':int(inside[col].notna().sum()),'n_outside':int(outside[col].notna().sum())})
 contrasts=pd.DataFrame(contrasts);top=contrasts.assign(abs_effect=contrasts.standardized_mean_contrast.abs()).sort_values(['performance_class','abs_effect'],ascending=[True,False]).groupby('performance_class').head(5)
 channel=d.dropna(subset=CHANNEL).copy();trc=score.merge(c,on='galaxy');trc=trc[trc.split.eq('train')];lx=np.log1p(channel[CHANNEL]);mu=np.log1p(trc[CHANNEL]).mean();sd=np.log1p(trc[CHANNEL]).std(ddof=0).replace(0,1);channel['channel_load_norm']=np.sqrt((((lx-mu)/sd)**2).sum(axis=1));channel_summary=channel.groupby('performance_class').agg(n=('galaxy','size'),median_channel_load=('channel_load_norm','median'),mean_channel_load=('channel_load_norm','mean')).reset_index()
 result={'schema':'tau-core.paper8.body-success-morphology-channel-atlas.v01','status':'BODY_SUCCESS_MORPHOLOGY_CHANNEL_DESCRIPTIVE_ATLAS_COMPLETE','body_model':'local value-only invariant response v01','classification':{'strong_success':'matched body RMSE < Newton RMSE and < TPG/v6 RMSE','partial_success':'matched body RMSE < Newton RMSE but >= TPG/v6 RMSE','body_failure':'matched body RMSE >= Newton RMSE regardless of TPG comparison'},'counts':dict(zip(summary.performance_class,summary.n_galaxies)),'channel_overlap_n':len(channel),'top_standardized_morphology_contrasts':top.to_dict(orient='records'),'physical_channel_detected':False,'retuning_allowed':False,'claim_boundary':'descriptive post-score atlas; generates hypotheses for new source-frozen tests but cannot retune the inspected holdout'};(DATA/'body_success_morphology_channel_atlas_v01.json').write_text(json.dumps(result,indent=2)+'\n');d.to_csv(DATA/'body_success_morphology_channel_atlas_galaxies_v01.csv',index=False);summary.to_csv(DATA/'body_success_morphology_channel_atlas_summary_v01.csv',index=False);family_frac.to_csv(DATA/'body_success_morphology_channel_atlas_family_fractions_v01.csv');contrasts.to_csv(DATA/'body_success_morphology_channel_atlas_contrasts_v01.csv',index=False);channel_summary.to_csv(DATA/'body_success_morphology_channel_atlas_channel_v01.csv',index=False)
 lines=['# Body-success morphology/channel atlas v01','',f"Status: `{result['status']}`",'',f"Holdout counts: `{result['counts']}`. Channel-complete overlap: `{len(channel)}`.",'','Top exploratory morphology contrasts (train-standardized):','']
 for cls,z in top.groupby('performance_class'):
  lines.append(f"- `{cls}`: "+', '.join(f"{r.feature}={r.standardized_mean_contrast:+.2f}" for r in z.itertuples()))
 lines+=['','Channel-load summaries:','']+[f"- `{r.performance_class}`: n={r.n}, median={r.median_channel_load:.3f}, mean={r.mean_channel_load:.3f}" for r in channel_summary.itertuples()]+['','This is a descriptive post-score atlas. It may nominate new source-frozen hypotheses but may not retune the inspected holdout. No physical channel is detected.']
 REPORT.write_text('\n'.join(lines)+'\n');print(result['status'])
if __name__=='__main__':main()
