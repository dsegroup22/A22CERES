
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 13:53:27 2019

@author: Nout
"""
import numpy as np
# =============================================================================
# import os
# from pathlib import Path
# os.chdir(Path(__file__).parents[2])
# from All_dic_Parameters import Parameters as par
# =============================================================================

import sys
sys.path.append('../../')
from All_dic_Parameters import Parameters as par

#get parameters from dictionairy

        
def Sens_analysis(Wto, Wpl, Wcrew, Mres, Mff, Mtfo,R):
#inputs:    float Wto = takeoff weight can be in [N] or [kg], it doesn't matter
#           float Wpl = Payload weight can be in [N] or [kg], it doesn't matter
#           float Wcrew = weight of the crew, can be in [N] or [kg], it doesn't matter
#BUT BE CONSISTENT
#           float Mres = reserve fuel fraction [-]
#           float Mff = fuel fraction [-]
#           float Mtfo = trapped fuel fraction [-]
#
#           float R = total range [m]
#outputs:
#           float sens_pl = sensitivy of take off weight, with respect to payload weight.
#           eg. if sens_pl = 5.71, than for each extra kg in payload weight, the take off weight increases by 5.71 kg   
#
#Description: this program uses formulas from Roskamp chapter 2, to analyse the sensitivity  
#All formulas are retrieved from Roskamp pages 68-83        
    
    #convert weights into pounds and kilometers into nautical miles
    Wto = Wto*2.20462262 #[lbs]
    Wpl = Wpl*2.20462262 #[lbs]
    Wcrew = Wcrew*2.20462262 #[lbs]
    R = R*0.539956803 #[nm]
    
    #parameters from dictionairy
    V = par.get('V_cruise') #[m/s]
    c_j = par.get('c_j') #[s^-1]
    L_D = par.get('L_D') #[-]
    A = par.get('A') #[-]
    B = par.get('B') #[-]
    
    #convert dictionairy into imperial units
    V = V*1.94384449 #[kts]
    c_j = c_j*3600 #[hr^-1]
    
    #get parameters roskam coefficients
    C = 1-(1+Mres)*(1-Mff)-Mtfo #[-]                             #From roskam 2.7
    D = Wpl+Wcrew #[lbs]
    F = -B*Wto**2*((C*Wto*(1-B)-D)**-1)*(1+Mres)*Mff #[lbs]
    


    
# =============================================================================
#     #test parameters
#     C = 0.791
#     D = 31775
#     F = 369211
#     L_D = 16
#     c_j = 0.5
#     V = 473
# =============================================================================
    
    
    #get sensitivities 
    sens_pl = B*Wto*((D-C*(1-B)*Wto)**-1)                   #sens wrt payload weight [-]
    
    We = 10**((np.log10(Wto)-A)/B)                          #empty weight [lbs]
    
    sens_we = B*10**(B*np.log10(We)+A)/We                   #sens wrt empty weight [-]
    
    sens_R = F*c_j*(V*L_D)**-1                              #sens wrt range [lbs/nm]
    
    sens_cj = F*R*(V*L_D)**-1                               #sens wrt specific fuel consumption [lbshr]
    
    sens_L_D = -F*R*c_j*(V*L_D**2)**-1                      #sens wrt lift over drag ratio [lbs]
    
    #go back to metric units
    sens_R = sens_R/2.20462262/0.539956803 #[kg/km]
    sens_cj = sens_cj/2.20462262 #[kghr]
    sens_L_D = sens_L_D/2.20462262 #[kg]
    return (sens_pl, sens_we, sens_R, sens_cj, sens_L_D)

