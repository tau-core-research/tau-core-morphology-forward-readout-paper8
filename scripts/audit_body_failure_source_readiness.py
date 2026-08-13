#!/usr/bin/env python3
"""Audit source-native morphology readiness of the strict body failures."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/derived';REPORT=ROOT/'reports/body_failure_source_readiness_v01.md'
def main():
 atlas=pd.read_csv(DATA/'body_success_morphology_channel_atlas_galaxies_v01.csv');fail=atlas[atlas.performance_class.eq('body_failure')];acc=pd.read_csv(DATA/'accepted_morphology_manifest.csv');d=fail[['galaxy','formula_family','inclination_deg','matched_minus_newton','matched_minus_tpg_v6']].merge(acc,on=['galaxy','formula_family'],suffixes=('','_accepted'),how='left');rows=[]
 for _,r in d.iterrows():
  missing=str(r.get('missing_required_fields','')) if pd.notna(r.get('missing_required_fields')) else ''
  accepted=str(r.get('accepted_observable_status',''))
  complete=accepted=='ACCEPTED_SOURCE_OBSERVABLE' and not missing
  if r.formula_family=='K_thick_flared': needed='vertical_scale_height_kpc;h_over_Rs;flare_or_warp_radius_kpc;gas_plane_thickness'
  else: needed='source_native_scale_radius_kpc;tail_onset_kpc;tail_support_or_HI_radius_kpc;gas_support_profile'
  priority='P0' if r.galaxy in ['NGC4088','NGC4389','UGC04305','UGC07577'] else 'P1'
  caveat=[]
  if r.inclination_deg<40:caveat.append('low_inclination')
  if r.galaxy=='CamB':caveat+=['asymmetric_drift_dominant','same_HI_family_overlap']
  rows.append({'galaxy':r.galaxy,'formula_family':r.formula_family,'source_ready_for_refined_body':complete,'current_source_status':accepted or 'missing','current_missing_fields':missing,'required_refined_fields':needed,'priority':priority,'measurement_caveat':';'.join(caveat),'endpoint_rescoring_allowed':False})
 out=pd.DataFrame(rows).sort_values(['priority','formula_family','galaxy']);result={'schema':'tau-core.paper8.body-failure-source-readiness.v01','status':'ALL_STRICT_BODY_FAILURES_REQUIRE_SOURCE_REFINEMENT','n_failures':len(out),'n_refined_source_ready':int(out.source_ready_for_refined_body.sum()),'n_scale_tail':int((out.formula_family=='K_scale_tail_spiral').sum()),'n_thick_flared':int((out.formula_family=='K_thick_flared').sum()),'cam_b_literature_candidate':{'source':'Begum, Chengalur & Hopp (2003), arXiv:astro-ph/0301194','evidence':'regular HI field aligned with HI and optical axes; rotation traced beyond four optical scale lengths','boundary':'same broad HI family as kinematic endpoint and asymmetric-drift dominated; context only'},'rescoring_allowed':False,'claim_boundary':'source-readiness audit triggered by post-score failures; may prioritize independent acquisition but cannot retune or rescore inspected holdout'};(DATA/'body_failure_source_readiness_v01.json').write_text(json.dumps(result,indent=2)+'\n');out.to_csv(DATA/'body_failure_source_readiness_v01.csv',index=False);lines=['# Body-failure source readiness audit v01','',f"Status: `{result['status']}`",'',f"All `{len(out)}` strict failures lack a complete source-native refined-body record. Scale-tail failures require measured scale, onset, outer support, and gas-support profiles; thick/flared failures require vertical height, h/Rs, flare/warp onset, or gas-plane thickness. No endpoint rescoring is allowed from this post-score audit.",''];lines += [f"- `{r.galaxy}` ({r.formula_family}, {r.priority}): missing `{r.required_refined_fields}`; caveat `{r.measurement_caveat or 'none'}`." for r in out.itertuples()];REPORT.write_text('\n'.join(lines)+'\n');print(result['status'])
if __name__=='__main__':main()
