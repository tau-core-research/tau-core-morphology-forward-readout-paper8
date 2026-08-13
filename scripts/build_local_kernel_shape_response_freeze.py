#!/usr/bin/env python3
"""Freeze a value-plus-log-slope local morphology response."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/derived/local_kernel_shape_response_freeze_v01.json'
def main():
 r={'schema':'tau-core.paper8.local-kernel-shape-response-freeze.v01','status':'LOCAL_VALUE_SLOPE_KERNEL_RESPONSE_FROZEN_DIAGNOSTIC_SCORE_ALLOWED','formula':'v_body^2=v_Newton^2 exp(eta_f psi_f)','value_coordinate':'u=K(R)/K(R_s); phi=u/(1+u)','shape_coordinate':'s=abs(d log(K+eps)/d log R); q=s/(1+s)','combined_activation':'psi=phi*(1+q)','derivative':'centered numpy gradient on each source radial grid','epsilon':'1e-12 times max(abs(K),1)','eta_grid':[-4,-3.5,-3,-2.5,-2,-1.5,-1,-.75,-.5,-.25,0,.25,.5,.75,1,1.5,2,2.5,3,3.5,4],'eta_selection':'train-only galaxy-balanced RMSE independently by family','uses_vobs_or_residual':False,'channel_coordinates':[],'claim_boundary':'source-side diagnostic freeze; no holdout retuning, prospective status, or parent derivation'}
 OUT.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
if __name__=='__main__':main()
