# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:30:41 2019

@author: menno
"""
import numpy as np

import sys
sys.path.append('../../../')

from A22DSE.Parameters.Par_Class_Atmos import Atmos


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
    q_D = 0.5*Atmos.rho*(1.4*anfp.V_cruise)**2*anfp.S
    
    #roskam: equation 5.26
    W_f=2*10.43*K_inl**1.42*(q_D/100)**0.283*(MTOMlbs/1000)**0.95*\
    (l_fuselage/h_fuselage)**0.71
    
    
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
    return W_f*Conv.ConversTool.lbs2kg
=======


