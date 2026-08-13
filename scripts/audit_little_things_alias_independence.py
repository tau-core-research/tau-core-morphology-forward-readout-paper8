#!/usr/bin/env python3
"""Audit physical-identity overlap using SIMBAD aliases, not exact names."""
from __future__ import annotations
import json,re
from pathlib import Path
import pandas as pd
from astroquery.simbad import Simbad
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/derived';REPORT=ROOT/'reports/little_things_alias_independence_audit_v01.md'
CATALOGS=('DDO','UGC','NGC','IC','F','HARO')
def keys(value):
 text=str(value).upper().replace('_',' ').replace('-',' ');out=set()
 for cat in CATALOGS:
  for num in re.findall(rf'\b{cat}\s*0*(\d+)\b',text):out.add(f'{cat}{int(num)}')
 compact=re.sub(r'[^A-Z0-9]','',text)
 if compact in ('WLM','CVNIDWA'):out.add(compact)
 return out
def main():
 freeze=pd.read_csv(DATA/'little_things_prospective_scoring_freeze_v01.csv');hist=pd.read_csv(DATA/'external_sparc_master_table.csv');historical=set().union(*(keys(x) for x in hist.Galaxy));rows=[]
 for _,r in freeze.iterrows():
  query=str(r.galaxy).replace('_',' ');ids=[];status='OK'
  try:
   table=Simbad.query_objectids(query);ids=[] if table is None else [str(x) for x in table['id']]
  except Exception as exc:status=f'QUERY_FAILED:{type(exc).__name__}'
  alias_keys=set().union(keys(query),*(keys(x) for x in ids));overlap=sorted(alias_keys&historical);rows.append({'galaxy':r.galaxy,'query':query,'simbad_status':status,'alias_keys':';'.join(sorted(alias_keys)),'historical_overlap_keys':';'.join(overlap),'alias_physical_overlap':bool(overlap),'old_exact_overlap':bool(r.exact_name_overlap_with_historical_175),'old_prospective_freeze':bool(r.prospective_name_freeze),'corrected_independent_name_gate':not bool(overlap)})
 out=pd.DataFrame(rows);out.to_csv(DATA/'little_things_alias_independence_audit_v01.csv',index=False);false_new=out[(~out.old_exact_overlap)&out.alias_physical_overlap];result={'schema':'tau-core.paper8.little-things-alias-independence-audit.v01','status':'ALIAS_OVERLAP_FOUND_PROSPECTIVE_NAME_GATE_CORRECTION_REQUIRED' if len(false_new) else 'NO_ADDITIONAL_ALIAS_OVERLAP','n_objects':len(out),'n_alias_overlaps':int(out.alias_physical_overlap.sum()),'n_missed_by_exact_name':len(false_new),'missed_objects':false_new.galaxy.tolist(),'corrected_independent_count':int(out.corrected_independent_name_gate.sum()),'ddo50_ugc04305_overlap_confirmed':bool(out.loc[out.galaxy.eq('DDO_50'),'alias_physical_overlap'].iloc[0]),'claim_boundary':'identity/provenance audit only; alias-overlap objects are not independent external tests'};(DATA/'little_things_alias_independence_audit_v01.json').write_text(json.dumps(result,indent=2)+'\n');REPORT.write_text(f"# LITTLE THINGS alias-independence audit v01\n\nStatus: `{result['status']}`\n\nSIMBAD alias normalization finds `{result['n_alias_overlaps']}` physical overlaps, `{result['n_missed_by_exact_name']}` missed by the exact-name gate: `{result['missed_objects']}`. Corrected independent count: `{result['corrected_independent_count']}` of `{len(out)}`. Alias-overlap objects cannot count as independent external tests.\n");print(result['status'])
if __name__=='__main__':main()
