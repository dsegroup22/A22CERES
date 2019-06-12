# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:13:22 2019

@author: Nout
"""
import numpy as np

def GetMaxLiftHorTail():
    
    clmax_h = -0.8
    #rho_cruise =
    #v_cruise = 
    #S = anfp.S
    #F_max_htail = 0.5*clmax_h*rho_cruise*v_gust**2*S
    F_max_htail = 0.5*1.2*0.008*230**2*40
    return F_max_htail

def NormalStress(Aircraft, x_from_tail, d):
    """
    DESCRIPTION:
        calculates normal stress in crossection, given an location from the tail,
        and the diameter of the cone at a given point.
    """
    #get shortcuts
    struc= Aircraft.ParStruc
   
    #get parameters
    FoS = 1.5 #safety factor
    
    max_normal_stress = struc.max_yield_stress
    F_max_htail = GetMaxLiftHorTail()
    
    #functions
    Moment = F_max_htail*x_from_tail

    ymax = d
    
    t_skin_min = FoS*Moment*ymax/(np.pi*(d/2)**3*max_normal_stress)
    
    return t_skin_min

test = True

if test:
    import os
    from pathlib import Path
    os.chdir(Path(__file__).parents[5])
    from A22DSE.Parameters.Par_Class_Conventional import Conv

