# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:30:41 2019

@author: menno
"""
import numpy as np
import scipy.integrate as integrate
import sys
sys.path.append('../../../')
from A22DSE.Models.STRUC.current.Loadingdiagram import Loading_Diagrams
from A22DSE.Parameters.Par_Class_Conventional import Conv


def WingWeight(Aircraft):
    anfp=Aircraft.ParAnFP
    layout=Aircraft.ParLayoutConfig
    struc=Aircraft.ParStruc
    MTOW=struc.MTOW
    b=anfp.b
    Sweep_EA=anfp.Sweep_50
    Sweep_25=anfp.Sweep_25
    S=anfp.S
    A=anfp.A
    c_r=anfp.c_r
    c_t=anfp.c_t
    taper=anfp.taper
    t_c=anfp.tc
    eta_t=0.84
    I_2_t=0.36
    t_ref=1
    k_rib=0.5*10**-3
    
    #still needs safety factors
    sigma_t=3*10**9
    sigma_c=1*10**9
    
    
    R_in=0.8 #dummy
    rho=2000
    n_ult=2.5
    
    eta_cp=1/(3*n_ult)*(4/np.pi+(n_ult-1)*(1+2*taper)/(1+taper))+0.02*np.sin(Sweep_25)
    sigma_r=(0.5*(1/sigma_t+1.25/sigma_c))**-1
    R_cant=A*(1+taper)/(4*t_c*np.cos(Sweep_EA))
    b_st=b/2/np.cos(Sweep_EA)

    #not used
    V,M=Loading_Diagrams(Aircraft)
    A=M/eta_t/sigma_t
    localA = lambda x:  A[int(round(x/(b/2)))]
    W_BL=2*g*rho*integrate.quad(localA,0,b_st)[0]
    
    W_BL2=I_2_t*rho*g/sigma_r*n_ult*MTOW*g*R_cant*eta_cp/eta_t*b_st



    
    
    
    sigma_shear=0.5*sigma_r
    W_SL=1.2*n_ult*MTOW*g*eta_cp*b_st*rho*g/sigma_shear

    W_IP_T=0.05*W_BL
    
    
    W_rib=k_rib*rho*S*g*(t_ref+t_c*(c_r+c_t)/2)
    
    
    W_id_box=I_2_t*n_ult*R_in*MTOW*g*eta_cp*b_st*rho*g/sigma_r*(1.05*R_cant/eta_t+3.67)
    
    return W_id_box