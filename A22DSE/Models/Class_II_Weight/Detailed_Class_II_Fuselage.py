# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:30:41 2019

@author: menno
"""
import numpy as np
import sys
sys.path.append('../../../')

from A22DSE.Parameters.Par_Class_Conventional import Conv

def FuselageWeight(Aircraft):
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    
    h_fuselage=config.h_fuselage
    w_fuselage=config.w_fuselage
    
    l_fuselage=config.l_fuselage
    K_inl=1.25
    MTOMlbs = struc.MTOW/Conv.ConversTool.lbs2kg
    
    
#    torenbeek method    
#    l_ref=1.5 #[m]
#    n_ult=2.5
#    d_fuselage=np.average([h_fuselage,w_fuselage])    
#    
#    C_shell=60 #[N/m^3]
#    Omega_fl=160 #[N/m^2]
#    
#    W_shell=C_shell*d_fuselage**2*l_fuselage
#    W_bulkheads=C_shell*d_fuselage**2*l_ref
#    W_fl=Omega_fl*n_ult**0.5*d_fuselage*l_fuselage
#    W_fus=W_shell+W_bulkheads+W_fl
    return 