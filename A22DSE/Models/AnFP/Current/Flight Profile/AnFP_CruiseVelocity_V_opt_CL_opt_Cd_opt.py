# -*- coding: utf-8 -*-
"""
Created on Thu May  9 09:31:11 2019

@author: Nout
"""
import numpy as np
import os
from pathlib import Path
os.chdir(Path(__file__).parents[2])

from All_dic_Parameters import Parameters as par

def OptimumCruiseCond(M_dd, W_S, rho,Cd0, A, e):
#inputs: float Mdd: [-] mach drag divergence number
#        float W_S: [N/m2] wing loading weight over surface area
#       float rho : densitity at cruise altitude [kg/m3]
#       float Cd0: zero lift drag coefficients [-]
#       float A: aspect ratio [-]
#       float e: oswald efficiency factor [-]
#output: float V_opt: optimum cruise speed [m/s]
#       float CL_opt: optimum cruise CL [-]
    
#Description: this program calculates the optimum cruise velocity and mach number, if the 
#       mach number is higher than M_dd, then this is the optimum cruise mach number
    
    #import parameters from dic
    a = par.get('a_cruise')
    
    #find CL_opt & Cd_opt
    CL_opt = np.sqrt(Cd0/3*np.pi*A*e)               #formulas are from Flight and Orbital
    Cd_opt = 4/3*Cd0
    
    #calculate the optimum speed
    V_opt = np.sqrt(W_S*2/rho/CL_opt)
    M_opt = V_opt/a
    
    #calculate the limiting speed
    V_dd = M_dd*a
    
    #check if optimum speed is limited by drag divergence
    if V_opt>V_dd:
        V_opt = V_dd
        print("Mach drag divergence number was the limiting factor")
        CL_opt = W_S*2/rho/(V_opt**2)
    return(V_opt, CL_opt)