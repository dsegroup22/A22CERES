# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:30:41 2019

@author: menno
"""
import numpy as np
import os
from pathlib import Path
os.chdir(Path(__file__).parents[3])

#exports in Newtons

def FuselageWeight(Aircraft):
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    
    h_fuselage=config.h_fuselage    #[m]
    w_fuselage=config.w_fuselage    #[m]

    l_fuselage=config.l_fuselage    #[m]
    K_inl=1.                      #roskam page 77 part V
    MTOMlbs = struc.MTOW/Aircraft.ConversTool.lbs2kg
    q_Dpsf = anfp.q_dive/Aircraft.ConversTool.psf2Pa
    
    
    #Roskam part V (Chapter 5.3)
    #roskam: equation 5.26 (commercial)
    W_f=2*10.43*K_inl**1.42*(q_Dpsf/100)**0.283*(MTOMlbs/1000)**0.95*\
    (l_fuselage/h_fuselage)**0.71

    #roskam: equation 5.28 (military)
    W_f_mil=2*11.03*K_inl**1.23*(q_Dpsf/100)**0.245*(MTOMlbs/1000)**0.98*\
    (l_fuselage/h_fuselage)**0.61
    
    
#    torenbeek method  (Chapter 8.3.3)  
    l_ref=1.5 #[m]
    n_ult=anfp.n_ult
    d_fuselage=np.average([h_fuselage,w_fuselage])    
    
    C_shell=60          #[N/m^3]
    Omega_fl=160        #[N/m^2]
    
    W_shell=C_shell*d_fuselage**2*l_fuselage
    W_bulkheads=C_shell*d_fuselage**2*l_ref
    
    W_fl=Omega_fl*n_ult**0.5*d_fuselage*l_fuselage
    W_f_tor=W_shell+W_bulkheads+W_fl
    return W_f*Aircraft.ConversTool.lbf2N,W_f_mil*Aircraft.ConversTool.lbf2N,W_f_tor #[N]


    
    

