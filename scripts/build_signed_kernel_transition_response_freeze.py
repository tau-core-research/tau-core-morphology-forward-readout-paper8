#!/usr/bin/env python3
"""Freeze a signed declining-transition morphology response."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/derived/signed_kernel_transition_response_freeze_v01.json'
def main():
 r={'schema':'tau-core.paper8.signed-kernel-transition-response-freeze.v01','status':'SIGNED_DECLINING_KERNEL_TRANSITION_FROZEN_DIAGNOSTIC_SCORE_ALLOWED','formula':'v_body^2=v_Newton^2 exp(eta_f psi_minus)','value_coordinate':'u=K/K(R_s); phi=u/(1+u)','signed_slope':'s=d log(K+eps)/d log R','declining_selector':'q_minus=(1-tanh(s))/2','combined_activation':'psi_minus=phi*q_minus','eta_grid':[-4,-3.5,-3,-2.5,-2,-1.5,-1,-.75,-.5,-.25,0,.25,.5,.75,1,1.5,2,2.5,3,3.5,4],'eta_selection':'train-only galaxy-balanced RMSE independently by family','uses_vobs_or_residual':False,'channel_coordinates':[],'claim_boundary':'source-side signed-transition diagnostic freeze; not prospective or parent-derived'};OUT.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
if __name__=='__main__':main()
