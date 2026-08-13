#!/usr/bin/env python3
"""Build continuous observational lightcone-load proxies from object-level cones."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/derived';THETA0=0.25

def main():
    o=pd.read_csv(DATA/'sparc_simbad_lightcone_objects_v01.csv'); rows=[]
    for galaxy,g in o.groupby('target_galaxy'):
        w=1/(g.separation_arcmin.to_numpy()**2+THETA0**2); zt=float(g.target_redshift.iloc[0])
        fg=g.is_foreground_candidate.astype(bool).to_numpy(); bg=g.is_background_control.astype(bool).to_numpy(); st=g.is_stellar_crowding_control.astype(bool).to_numpy(); zo=g.object_redshift.to_numpy()
        lens=np.nansum(w[fg]*np.clip(zo[fg]*(zt-zo[fg])/max(zt,1e-9)**2,0,None))
        rows.append({'galaxy':galaxy,'foreground_lens_geometry_weight':lens,'foreground_angular_weight':float(w[fg].sum()),'stellar_crowding_angular_weight':float(w[st].sum()),'background_angular_control_weight':float(w[bg].sum()),'stellar_crowding_count':int(st.sum()),'foreground_redshift_count':int(fg.sum()),'background_redshift_count':int(bg.sum())})
    out=pd.DataFrame(rows); out.to_csv(DATA/'continuous_lightcone_channel_proxy_v01.csv',index=False)
    result={'schema':'continuous_lightcone_channel_proxy_v01','status':'CONTINUOUS_OBSERVATIONAL_CHANNEL_LOAD_PROXY_BUILT_NOT_PHYSICAL_TRANSFER','n_galaxies':len(out),'nonzero_counts':{c:int((out[c]>0).sum()) for c in ['foreground_lens_geometry_weight','stellar_crowding_angular_weight','background_angular_control_weight']},'physical_time_channel_variable':False,'limitations':['no homogeneous object mass proxy','no distances for stellar foregrounds','SIMBAD selection is heterogeneous','background term is a negative control and not on the observer-source path'],'claim_boundary':'continuous angular observational-load proxy; not lightcone stress-energy integral, lensing convergence, time dilation, or Tau channel'}
    (DATA/'continuous_lightcone_channel_proxy_v01.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
if __name__=='__main__':main()
