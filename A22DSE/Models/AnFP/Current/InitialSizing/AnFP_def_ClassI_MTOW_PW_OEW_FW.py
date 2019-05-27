# -*- coding: utf-8 -*-
"""
Created on Mon May  6 16:24:35 2019

@author: Nout
"""
#from ... import get_range
def Class_I_estimate(PW,Mfrac_PWMTOW, Mfrac_OEWMTOW, range_req):
#============================================================================#
#inputs:
#   float PW:               payload weight desired payload weight per flight
#   float Mfrac_PWMTOW:     payload fraction (estimate)
#   float range_req:        
#outputs:
#   float MTOW: maximum takeoff weight from first class estimation
#   float PW: payload weight 
#   float OEW: operational empty weight from first class estimation
#   float FW: fuel weight from first class estimation    
#
#
#Description: Tries Mpl/MTOW to compute Wf/MTOW which results in a range
#             If range meets the range requirement for combustion, then
#               proper Mpl/MTOW is found, which results in MTOW. 
#============================================================================#
    
    
    
    Requirement = False
    while Requirement == False:
        Mfrac_WFMTOW= 1-Mfrac_PWMTOW-Mfrac_OEWMTOW
        
        Range = get_range(Mfrac_WFMTOW)                                      
        if Range>range_req:                                                     #compare the range which originates from the fuel fraction
             Requirement = True                                                 #if requirements is satisfied, fuel fraction is correct.
        else:                                                                   
            if Mfrac_PWMTOW>0:                                                  #if not satisfied, use different payload and fuel fractions.
                Mfrac_PWMTOW = Mfrac_PWMTOW-0.01
            else:
                failure = 'start with higher Mfrac_PWMTOW'
                return(failure)
            
            
    MTOW = PW/Mfrac_PWMTOW
    FW = MTOW*Mfrac_WFMTOW
    OEW = MTOW*Mfrac_OEWMTOW       
    
    return (MTOW, PW, OEW, FW)