#!/usr/bin/env python3
"""Freeze a source-side curvature-onset morphology response."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/derived/kernel_curvature_onset_response_freeze_v01.json'
def main():
 r={'schema':'tau-core.paper8.kernel-curvature-onset-response-freeze.v01','status':'KERNEL_CURVATURE_ONSET_RESPONSE_FROZEN_DIAGNOSTIC_SCORE_ALLOWED','transition_radius':'argmax abs(d2 log(K+eps)/d(log R)^2) over interior radial points','edge_exclusion':'exclude first and last max(2,ceil(0.1*N)) grid points','phase_coordinate':'xi=R/R_transition','onset_activation':'a=xi^2/(1+xi^2)','value_coordinate':'u=K/K(R_s); phi=u/(1+u)','combined_activation':'psi_transition=phi*(0.5+a)','formula':'v_body^2=v_Newton^2 exp(eta_f psi_transition)','eta_grid':[-4,-3.5,-3,-2.5,-2,-1.5,-1,-.75,-.5,-.25,0,.25,.5,.75,1,1.5,2,2.5,3,3.5,4],'eta_selection':'train-only galaxy-balanced RMSE independently by family','uses_vobs_or_residual':False,'channel_coordinates':[],'claim_boundary':'source-side curvature-onset diagnostic freeze; not prospective or parent-derived'};OUT.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
if __name__=='__main__':main()
